import typing
from abc import ABC, abstractmethod
from unittest import TestCase

from events_protocol.core.model.base import PascalPydanticMixin


class EventHandler(ABC):
    schema: PascalPydanticMixin = None
    response_schema: PascalPydanticMixin = None

    @abstractmethod
    async def execute(self, payload: PascalPydanticMixin, user_id: int = None):
        raise NotImplementedError
