import logging
from logging import StreamHandler
from typing import List
from functools import update_wrapper

class Logger(logging.LoggerAdapter):
    """This classe is responsible to be an interface for other classes and
    modules use the logging with the Events Protocol format.

    Returns
    -------
    Events Protocol.package.utils.Logger
        This classe is responsible to be an interface for other classes and modules use the logging with the Events Protocol format
    """

    HANDLERS: List[StreamHandler] = [logging.StreamHandler()]
    
    def __init__(
        self,
        log_name: str,
        log_format: str = "$BOLD%(asctime)s$RESET %(name)-12s %(levelname)-18s %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
        level: int = logging.INFO,
        _custom_formatter: logging.Formatter = None,
    ) -> None:
        """Custom Logger constructor.

        Parameters
        ----------
        log_name : str
            The name of the logger instance.
        log_format : str, optional
            The log format, by default "$BOLD%(asctime)s$RESET %(name)-12s %(levelname)-18s %(message)s"
        date_format : _type_, optional
            The date format, by default "%Y-%m-%d %H:%M:%S"
        level : int, optional
            The logger level, you can use the ones predefined inside the logging module, or provide an int according to
             the following pattern: CRITICAL/FATAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10, NOTSET = 0.
             For more information: https://docs.python.org/3/library/logging.html#levels, by default 20 (INFO).
        _custom_formatter : logging.Formatter, optional
            Replaces the Events Protocol ColoredFormatter by the formatter provided and will ignore the log_format parameter.
        """
        if _custom_formatter is None:
            # The default logging Formatter.
            # self.log_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
            color_format = ColoredFormatter.formatter_message(log_format, True)
            self.log_formatter = ColoredFormatter(color_format, datefmt=date_format)

        else:
            self.log_formatter = _custom_formatter

        self.level = level
        self.log = self._create_log(log_name)

        if not self.log.hasHandlers():
            self.log.propagate = False
            self.__default_handlers = self.HANDLERS
            self.__add_default_handlers()

        self.log.setLevel(level)

    @staticmethod
    def _create_log(log_name: str) -> logging.Logger:
        """Creates the logger object.

        Parameters
        ----------
        log_name : str
            The name of the logger.

        Returns
        -------
        logging.Logger
            return the logging.Logger with the logger name provided.
        """
        return logging.getLogger(log_name)

    def add_handler(
        self,
        handler: logging.Handler,
        set_formatter: bool = True,
        formatter: logging.Formatter = None,
    ) -> None:
        """Method to add a new handler to the logger with the defined formatter
        and level.

        Parameters
        ----------
        handler : Handler
            The handler class to be added in the logger.
        set_formatter : bool, optional
            If the level and Formatter should be applied, by default True
        formatter: logging.Formatter, optional
            The custom formatter to be set in the handler.
        """
        if set_formatter:
            if formatter is None:
                handler.setFormatter(self.log_formatter)
            else:
                handler.setFormatter(formatter)
            handler.setLevel(self.level)
        self.log.addHandler(handler)

    def __add_default_handlers(self):
        """Method to add the default handlers."""
        for handler in self.__default_handlers:
            self.add_handler(handler)

    @classmethod
    def get_logger(
        cls,
        log_name: str,
        log_format: str = "$BOLD%(asctime)s$RESET %(name)-12s %(levelname)-18s %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
        level: int = logging.INFO,
        _custom_formatter: logging.Formatter = None,
    ) -> logging.Logger:
        """Get a logger object with Events Protocol Colored Formatter.

        Parameters
        ----------
        log_name : str
            Name of the logger instance
        log_format : str, optional
           Format of the logger message, by default "$BOLD%(asctime)s$RESET %(name)-12s %(levelname)-18s %(message)s"
        date_format : str, optional
            Date format of the logger message, by default "%Y-%m-%d %H:%M:%S"
        level : int, optional
            The logger level, you can use the ones predefined inside the logging module, or provide an int according to
             the following pattern: CRITICAL/FATAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10, NOTSET = 0.
             For more information: https://docs.python.org/3/library/logging.html#levels, by default 20 (INFO).
        _custom_formatter : logging.Formatter, optional
            Replaces the Events Protocol ColoredFormatter by the formatter provided and will ignore the log_format parameter.
        Returns
        -------
        logging.Logger
            The formatted logger.
        """
        logger = cls(
            log_name=log_name,
            log_format=log_format,
            date_format=date_format,
            level=level,
            _custom_formatter=_custom_formatter,
        )
        return logger.log

class ColoredFormatter(logging.Formatter):
    """Events Protocol's Custom Colored Formatter for Logging.

    Returns
    -------
     Events Protocol.package.utils.ColoredFormatter
        This class is responsible for setting the format for Events Protocol Loggings, by the default set timestamp and the module
        name with bold and will use the following color scheme:
            GREEN: DEBUG
            BLUE: INFO
            YELLOW: WARNING
            RED: ERROR
            MAGENTA: CRITICAL
    """

    # These are the sequences need to get colored output
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[%dm"
    BOLD_SEQ = "\033[1m"
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    COLORS = {
        "DEBUG": GREEN,
        "INFO": BLUE,
        "WARNING": YELLOW,
        "ERROR": RED,
        "CRITICAL": MAGENTA,
    }

    def __init__(self, msg: str, datefmt: str = "%Y-%m-%d %H:%M:%S", use_color: bool = True):
        """ColoredFormatter class constructor.

        Parameters
        ----------
        msg : str
            The message to be printed out.
        datefmt : str
            The date format, by default "%Y-%m-%d %H:%M:%S"
        use_color : bool
            Flag to signalize if the output should be colored or not.
        """
        logging.Formatter.__init__(self, msg, datefmt=datefmt)
        self.use_color = use_color

    def format(self, record: logging.LogRecord):
        """Method responsible for formatting the record.

        Parameters
        ----------
        record: logging.LogRecord
            The LogRecord with the message to be printed out.

        Returns
        -------
        str
            The message formatted.
        """
        levelname = record.levelname
        if self.use_color and levelname in self.COLORS:
            levelname_color = (
                self.COLOR_SEQ % (30 + self.COLORS[levelname]) + levelname + self.RESET_SEQ
            )
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

    @classmethod
    def formatter_message(cls, message: str, use_color: bool = True):
        """The method to parse the Events Protocol format string.

        Parameters
        ----------
        message : str
            The message to be formatted.
        use_color : bool
            Flag to signalize if the output should be colored or not.

        Returns
        -------
        str
            The message formatted.
        """
        if use_color:
            message = message.replace("$RESET", cls.RESET_SEQ).replace("$BOLD", cls.BOLD_SEQ)
        else:
            message = message.replace("$RESET", "").replace("$BOLD", "")
        return message


def logger_monitor(package_name: str = None, level: int = logging.INFO):
    """A logger decorator to monitor legacy methods and functions.

    Parameters
    ----------
    package_name : str, optional.
        The name of the package where the function or method is located. To get automatically use the __name__ variable.
    level : int, optional.
        The level of logger to be shown, by default: logging.INFO

    Returns
    -------
    """

    def inner_function(function):
        """The wrapper for the function or method.

        Parameters
        ----------
        function : FunctionType
            The function or method to be wrapped.

        Returns
        -------
            The result of the function or method.
        """

        def wrapper(*args):
            """The logger wrapper.

            Parameters
            ----------
            args : tuple
                The arguments of the function

            Returns
            -------
            """
            # Formats the name of the logger. If the package is provided attach it to the beginning of the logger name.
            logger_name = ""
            if package_name is not None:
                logger_name = f"{package_name}."
            logger_name += f"{function}".split(" ")[1]

            logger = Logger.get_logger(logger_name, level=level)
            logger.debug(f"Using the logger monitor decorator in {logger_name}.")

            try:
                result = function(*args)
                return result

            except Exception as e:
                msg = (
                    f"An error occurred during the execution of {function} from {package_name}. "
                    f"\nError Type: {type(e)} {str(e)}"
                )
                logger.error(msg, exc_info=True)

        update_wrapper(wrapper, function)
        return wrapper

    return inner_function
