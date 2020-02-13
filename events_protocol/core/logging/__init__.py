import json
import logging
import queue
import sys
from logging.handlers import QueueHandler, QueueListener

from events_protocol.core.context import EventContextHolder

logging.basicConfig(level=logging.INFO, format="%(message)s")
_queue = queue.Queue(-1)
_queue_handler = QueueHandler(_queue)
_handler = logging.NullHandler()
_queue_listener = QueueListener(_queue, _handler)

_logger = logging.getLogger("gb.application")
_logger.addHandler(_queue_handler)
_queue_listener.start()


class JsonLogger(logging.LoggerAdapter):
    def __init__(self,):
        self.logger = _logger

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            _msg = dict(
                level=logging.getLevelName(level),
                message=msg,
                context=EventContextHolder.get().to_dict(),
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
            msg = json.dumps(_msg)
            self.logger.log(level, msg, *args, **kwargs)
