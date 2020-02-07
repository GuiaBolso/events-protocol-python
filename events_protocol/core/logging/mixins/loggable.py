from events_protocol.core.logging import JsonLogger


class LoggableMixin:
    logger = JsonLogger()
