from dataclasses import dataclass
import typing
from abc import ABC, abstractmethod

from events_protocol.core.exception import MissingEventInformationException
from events_protocol.core.model.base import CamelPydanticMixin
from events_protocol.core.model.event import Event, RequestEvent, ResponseEvent
from events_protocol.core.model.base import ValidationError

@dataclass
class EventHandler(ABC):
    event_name: str
    event_version: typing.Union[None, int]
    _SCHEMA: CamelPydanticMixin = None

    def __post_init__(self) -> None:
        from .event_handler_discovery import EventDiscovery
            
        EventDiscovery.add(self.event_name, self, self.event_version or 1)

    @abstractmethod
    def handle(cls, event: RequestEvent) -> ResponseEvent:
        raise NotImplementedError

    @classmethod
    def parse_event(cls, event: Event) -> CamelPydanticMixin:
        try:
            return event.payload_as(cls._SCHEMA)
        except ValidationError as exception:
            raise MissingEventInformationException(parameters=exception.to_dict())

class AsyncEventHandler(EventHandler, ABC):
    _SCHEMA: CamelPydanticMixin = None

    @abstractmethod
    async def handle(cls, event: RequestEvent) -> ResponseEvent:
        raise NotImplementedError
