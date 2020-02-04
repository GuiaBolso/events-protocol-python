import typing
from abc import ABC, abstractmethod
from unittest import TestCase

from .event_handler_discovery import EventDiscovery
from .event_handler import EventHandler
from events_protocol.core.model.base import PascalPydanticMixin


class EventRegister(ABC):
    event_name: str
    event_version: typing.Union[None, int]
    event_handler: EventHandler

    def __init_subclass__(cls):
        """Register event when every child class is instantiated from this interface class
        """
        EventDiscovery.add(cls.event_name, cls.event_handler, cls.event_version or 1)
