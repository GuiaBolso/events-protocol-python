from logging import LoggerAdapter

from events_protocol.core.logging import JsonLogger


class LoggableMixin:
    logger = JsonLogger()
