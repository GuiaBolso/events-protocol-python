import typing
from abc import ABC, abstractmethod
from unittest import TestCase

from events_protocol.core.exception import EventException, MissingEventInformationException
from events_protocol.core.model.base import PascalPydanticMixin
from events_protocol.core.model.event import Event, RequestEvent, ResponseEvent, ValidationError


class EventHandler(ABC):
    _SCHEMA: PascalPydanticMixin = None

    @abstractmethod
    async def handle(cls, event: RequestEvent) -> ResponseEvent:
        raise NotImplementedError

    @classmethod
    def parse_event(cls, event: Event) -> PascalPydanticMixin:
        try:
            return event.payload_as(cls._SCHEMA)
        except ValidationError as exc:
            raise MissingEventInformationException(parameters=exc.to_dict())
