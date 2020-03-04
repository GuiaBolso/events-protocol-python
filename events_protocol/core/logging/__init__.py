import json
import logging
import queue
import re
import sys
import typing
from logging.handlers import QueueHandler, QueueListener

from events_protocol.core.context import EventContextHolder
from datetime import datetime as dt


def _get_klass_name(klass: typing.Any) -> str:
    # Simple and effective
    return re.sub(r"|".join(map(re.escape, ["<class", "'", ">", " "])), "", str(klass))


_logger: logging.LoggerAdapter = None


def _get_logger() -> logging.LoggerAdapter:
    global _logger
    if _logger:
        return _logger
    logging.basicConfig(level=logging.INFO)
    _queue = queue.Queue(-1)
    _queue_handler = QueueHandler(_queue)
    _handler = logging.StreamHandler(sys.stdout)
    _queue_listener = QueueListener(_queue, _handler)

    _logger = logging.getLogger("gb.events_protocol")
    if _logger.hasHandlers():
        _logger.handlers.clear()
    _logger.addHandler(_queue_handler)
    _logger.propagate = False
    _queue_listener.start()
    return _logger


class JsonLogger(logging.LoggerAdapter):
    version: str = "NOTDEFINED"

    @classmethod
    def set_version(cls, version: str):
        cls.version = version

    def __init__(self, klass=None):
        self.logger = _get_logger()
        self.klass = _get_klass_name(klass)

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            event_context = EventContextHolder.get()
            _msg = dict(
                severity=logging.getLevelName(level),
                logmessage=msg,
                EventID=event_context.id,
                FlowID=event_context.flow_id,
                UserId=event_context.user_id,
                Operation="{}:v{}".format(event_context.event_name, event_context.event_version),
                logger=self.klass,
                LoggerName=self.logger.name,
                logdate=dt.utcnow().isoformat(),
                ApplicationVersion=self.version,
            )

            extra = kwargs.pop("extra", None)
            if extra:
                if isinstance(extra, dict):
                    extra = json.dumps(extra)
                if not isinstance(extra, str):
                    extra_type = type(extra)
                    raise TypeError(
                        "Extra param needs to be dict or str, not {}".format(extra_type)
                    )
                _msg["extra"] = extra
            if level == logging.ERROR and kwargs.get("exc_info"):
                args = tuple()
                fmt = logging.Formatter()
                _exc = sys.exc_info()
                _msg["stackTrace"] = fmt.formatException(_exc)

                kwargs["exc_info"] = False
            msg = json.dumps(_msg)
            self.logger.log(level, msg, *args, **kwargs)
