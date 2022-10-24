from glob import glob
import logging
import json

from events_protocol.core.logging.logger import Logger
from events_protocol.core.context import EventContextHolder
from datetime import datetime 

class PicpayLogger(logging.Logger):
    """
    Create and format loggers in the PicPay standard format

    Parameters
    ----------
    level: int
        Logging level. Set using the enum defined in the logging std library 

    Returns
    -------
    logging.Logger
        Interface to use the logs of the logging library 
    """

    logger_name = 'events_protocol'
    version: str = "UNDEFINED"
    is_production_environment: bool = True
    internal_logger: logging.Logger = None

    def __init__(
        cls, 
        level: int= logging.INFO,
        environment: str= "PRD",
    ) -> None:
        """
        Custom constructor to create the loggers in the PicPay standard

        Parameters
        ----------
        level: int
            Logging level. Set using the enum defined in the logging std library 

        environment: str
            Set the current environment that will be used in the application.
            If it's PRD or HML it will format the logger in the PicPay application standards.
            Otherwise it'll use development settings
        """
        if cls.logger_name in logging.root.manager.loggerDict.keys():
            cls.internal_logger = logging.getLogger(cls.logger_name)
            cls.is_production_environment = IS_PROD_ENV
        else:
            cls.__create_logger_with_environment(cls.logger_name, environment)
        super().__init__(cls.logger_name, level)
        
    @classmethod
    def set_version(cls, version: str) -> None:
        """
        Set application version that will be logged

        Parameters
        ----------
        version: str
            Application version
        """
        cls.version = version

    def __create_logger_with_environment(
        self, 
        name: str = "events_protocol",
        environment: str = "PRD",
    ) -> None:
        """
        Creates the logger using the desired environment 

        Parameters
        ----------
        name: str
            Application version

        environment: str
            Set the current environment that will be used in the application.
            If it's PRD or HML it will format the logger in the PicPay application standards.
            Otherwise it'll use development settings
            Default PRD
        """
        if "IS_PROD_ENV" not in globals(): 
            global IS_PROD_ENV
        if environment.upper() == ('PRD' or 'HML'):
            self.is_production_environment = True
            self.internal_logger = Logger.get_logger(
                name, 
                level= logging.ERROR,
                log_format="%(message)s"
            )
            IS_PROD_ENV = True
        else:
            self.is_production_environment = False
            self.internal_logger = Logger.get_logger(
                name, 
                level= logging.INFO
            )
            IS_PROD_ENV = False

    def __dev_log(self, level, message, *args, **kawrgs):
        """
        Default logger. Used for development environment.

        Parameters
        ----------
        level: int
            Logging level. Set using the enum defined in the logging std library 

        message: str
            Message that will be send to the logger
        """
        self.internal_logger.log(level, message)

    def __prod_log(self, level, message, *args, **kwargs):
        """
        Production format logger. Used for production and QA environment.

        Parameters
        ----------
        level: int
            Logging level. Set using the enum defined in the logging std library 

        message: str
            Message that will be send to the logger
        """
        event_context = EventContextHolder.get()
        event_info = dict(
            EventID=event_context.id,
            FlowID=event_context.flow_id,
            UserId=str(event_context.user_id),
            UserType=event_context.user_type,
            Operation="{}:v{}".format(event_context.event_name, event_context.event_version),
            logger=__name__,
            LoggerName=__name__,
            ApplicationVersion=self.version,
        )
        _message = dict(
            timestamp_app=datetime.utcnow().astimezone().isoformat(timespec="milliseconds"),
            message=message,
            log_type="APPLICATION",
            log_level=logging.getLevelName(level),
            event=event_info,
        )

        message = str(json.dumps(_message))

        self.internal_logger.log(level, message)

    def _log(self, level, message, *args, **kwargs):
        if self.is_production_environment:
            self.__prod_log(level, message)
        else:
            self.__dev_log(level, message)