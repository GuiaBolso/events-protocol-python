from asyncio.log import logger
import logging
from events_protocol.core.logging.logger import Logger
from events_protocol.core.logging.picpay_logger import PicpayLogger

class LoggableMixin:
    logger = PicpayLogger() 

