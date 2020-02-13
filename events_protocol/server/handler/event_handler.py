import typing
from abc import ABC, abstractmethod

from events_protocol.core.exception import EventException, MissingEventInformationException
from events_protocol.core.model.base import CamelPydanticMixin
from events_protocol.core.model.event import Event, RequestEvent, ResponseEvent, ValidationError


class EventHandler(ABC):
    _SCHEMA: CamelPydanticMixin = None

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
