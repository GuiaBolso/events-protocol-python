from events_protocol.core.logging import JsonLogger


class LoggableMixin:
    logger = JsonLogger()

    def __new__(cls, *args, **kwargs):
        cls.logger = JsonLogger(cls)
        return super().__new__(cls)
