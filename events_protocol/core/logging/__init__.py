import json
import logging
import queue
import sys
import typing
from logging.handlers import QueueHandler, QueueListener

from events_protocol.core.context import EventContext

logging.basicConfig(level=logging.INFO, format="%(message)s")
_q = queue.Queue(-1)
_qh = QueueHandler(_q)
_h = logging.NullHandler()
_ql = QueueListener(_q, _h)

_logger = logging.getLogger("gb.application")
_logger.addHandler(_qh)
_ql.start()


class JsonLogger(logging.LoggerAdapter):
    _context: EventContext

    def __init__(
        self, context: EventContext = None
    ):
        self.logger = _logger
        self._context = context or EventContext("UNDEFINED", "UNDEFINED")

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            _msg = dict(
                level=logging.getLevelName(level),
                message=msg,
                context=self._context.to_dict()
            )
            extra = kwargs.pop("extra", None)
            if extra:
                _msg["extra"] = extra
            if level == logging.ERROR and kwargs.get("exc_info"):
                args = tuple()
                fmt = logging.Formatter()
                _exc = sys.exc_info()
                exc = json.dumps(fmt.formatException(_exc))
                _msg["stacktrace"] = exc

                kwargs["exc_info"] = False
            self.logger.log(level, msg, *args, **kwargs)


DEFAULT_LOGGER_ADAPTER = JsonLogger(context=None)
