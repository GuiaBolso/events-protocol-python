import logging
import json

from events_protocol.core.logging.logger import Logger
from events_protocol.core.context import EventContextHolder
from datetime import datetime 

class PicpayLogger(logging.Logger):

    logger_name = 'events_protocol'
    version: str = "UNDEFINED"
    is_production_environment: bool = True
    internal_logger: logging.Logger = None

    def __init__(
        cls, 
        level: int= logging.INFO,
        environment: str= "PRD",
    ) -> None:
        if cls.logger_name in logging.root.manager.loggerDict.keys():
            cls.internal_logger = logging.getLogger(cls.logger_name)
            cls.is_production_environment = IS_PROD_ENV
        else:
            cls.create_logger_with_environment(cls.logger_name, environment)
        super().__init__(cls.logger_name, level)
        
    @classmethod
    def set_version(cls, version: str):
        cls.version = version

    def create_logger_with_environment(
        self, 
        name: str = __name__,
        environment: str = "PRD",
    ):
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

    def __dev_log(self, level, msg, *args, **kawrgs):
        self.internal_logger.log(level, msg)

    def __prod_log(self, level, msg, *args, **kwargs):
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
        _msg = dict(
            timestamp_app=datetime.utcnow().astimezone().isoformat(timespec="milliseconds"),
            message=msg,
            log_type="APPLICATION",
            log_level=logging.getLevelName(level),
            event=event_info,
        )

        msg = str(json.dumps(_msg))

        self.internal_logger.log(level, msg)

    def _log(self, level, msg, *args, **kwargs):
        if self.is_production_environment:
            self.__prod_log(level, msg)
        else:
            self.__dev_log(level, msg)