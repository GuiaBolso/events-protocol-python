import typing
from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar
from uuid import UUID

from events_protocol.core.model.base import BaseModel

IdType = typing.Union[str, UUID]


class EventContext(BaseModel):
    id: typing.Optional[IdType]
    flow_id: typing.Optional[IdType]
    event_name: typing.Optional[str]
    event_version: typing.Optional[int]
    user_id: typing.Optional[str]


_context: ContextVar[EventContext] = ContextVar("event_context", default=None)


class EventContextHolder:
    @staticmethod
    def get() -> EventContext:
        return _context.get() or EventContext()

    @staticmethod
    def set(event_context: EventContext) -> None:
        _context.set(event_context)

    @staticmethod
    def clean() -> None:
        _context.set(None)

    @classmethod
    @contextmanager
    def with_context(
        cls,
        context_id: IdType,
        context_flow_id: IdType,
        event_name: str,
        event_version: int,
        user_id: str = None,
    ):
        try:
            event_context = EventContext(
                id=context_id,
                flow_id=context_flow_id,
                event_name=event_name,
                user_id=user_id,
                event_version=event_version,
            )
            cls.set(event_context)
            yield cls.get()
        finally:
            cls.clean()

    @classmethod
    @asynccontextmanager
    async def with_async_context(
        cls,
        context_id: IdType,
        context_flow_id: IdType,
        event_name: str,
        event_version: int,
        user_id: str = None,
    ):
        try:
            event_context = EventContext(
                id=context_id,
                flow_id=context_flow_id,
                event_name=event_name,
                user_id=user_id,
                event_version=event_version,
            )
            cls.set(event_context)
            yield cls.get()
        finally:
            cls.clean()
