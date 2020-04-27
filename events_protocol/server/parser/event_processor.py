import json

from events_protocol.core.context import EventContextHolder
from events_protocol.core.exception import (
    EventException,
    EventParsingException,
)
from events_protocol.core.logging.mixins.loggable import LoggableMixin
from events_protocol.core.model.base import ValidationError
from events_protocol.core.model.event import Event, ResponseEvent
from events_protocol.server.handler.event_handler import EventHandler, AsyncEventHandler
from events_protocol.server.handler.event_handler_discovery import EventDiscovery

from events_protocol.core.builder import EventBuilder


class EventProcessor(LoggableMixin):
    event_discovery = EventDiscovery
    event_validator = Event

    @classmethod
    def process_event(cls, raw_event: str) -> str:
        event = None
        try:
            event: Event = cls.parse_event(raw_event)
            with EventContextHolder.with_context(
                event.id, event.flow_id, event.name, event.version
            ) as _:
                event_handler: EventHandler = EventDiscovery.get(event.name, event.version)
                response: ResponseEvent = event_handler.handle(event)
                return response.to_json()
        except EventException as exception:
            return EventBuilder.error_for(exception, event).to_json()

    @classmethod
    def parse_event(cls, str_event: str) -> Event:
        try:
            event = cls.event_validator.from_json(str_event)
            return event

        except ValidationError as exception:
            cls.logger.exception(
                "Error in event schema validation",
                exception,
                extra=dict(event=json.dumps(str_event)),
            )
            raise EventParsingException(exception.to_dict())
        except Exception as exception:
            cls.logger.exception(
                "Error in parser schema procedure",
                exception,
                extra=dict(event=json.dumps(str_event)),
            )
            raise EventParsingException(dict(error="Unknown error"))


class AsyncEventProcessor(EventProcessor):
    @classmethod
    async def process_event(cls, raw_event: str) -> str:
        event = None
        try:
            event: Event = cls.parse_event(raw_event)
            async with EventContextHolder.with_async_context(
                event.id, event.flow_id, event.name, event.version, event.user_id
            ) as _:
                event_handler: AsyncEventHandler = EventDiscovery.get(event.name, event.version)
                response: ResponseEvent = await event_handler.handle(event)
                return response.to_json()
        except EventException as exception:
            return EventBuilder.error_for(exception, event).to_json()
