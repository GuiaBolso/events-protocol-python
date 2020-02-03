from logging import LoggerAdapter

from gb_ import DEFAULT_LOGGER_ADAPTER, JsonLogger


class LoggableMixin:
    _logger: LoggerAdapter = None

    def set_logger(self, logger: LoggerAdapter) -> None:
        self._logger = logger

    @property
    def logger(self) -> LoggerAdapter:
        """Return a new adapter to avoid memory leak or bad log context
         usage. Unless the object already has a well configured logger adapter

        Returns
        -------
        LoggerAdapter
        """
        if self._logger:
            return self._logger
        else:
            return JsonLogger()
