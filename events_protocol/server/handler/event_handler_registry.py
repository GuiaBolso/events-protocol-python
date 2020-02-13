import typing
from abc import ABC, abstractmethod
from unittest import TestCase

from .event_handler_discovery import EventDiscovery
from .event_handler import EventHandler
from events_protocol.core.model.base import CamelPydanticMixin


class EventRegister(ABC):
    event_name: str
    event_version: typing.Union[None, int]
    event_handler: EventHandler

    @classmethod
    def register(cls):
        """Call this method on startup application
        """
        EventDiscovery.add(cls.event_name, cls.event_handler, cls.event_version or 1)
