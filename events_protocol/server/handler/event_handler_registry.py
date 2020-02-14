import typing
from abc import ABC

from .event_handler_discovery import EventDiscovery
from .event_handler import EventHandler


class EventRegister(ABC):
    event_name: str
    event_version: typing.Union[None, int]
    event_handler: EventHandler

    @classmethod
    def register_event(cls):
        """Call this method on startup application
        """
        EventDiscovery.add(cls.event_name, cls.event_handler, cls.event_version or 1)
