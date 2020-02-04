import json
import typing

from events_protocol.core.context import EventContextHolder
from events_protocol.core.exception import (
    EventException,
    EventParsingException,
    EventNotFoundException,
)
from events_protocol.core.logging.mixins.loggable import LoggableMixin
from events_protocol.core.model.base import ValidationError
from events_protocol.core.model.event import Event, ResponseEvent
from events_protocol.server.handler.event_handler import EventHandler
from events_protocol.server.handler.event_handler_discovery import EventDiscovery

from events_protocol.core.builder import EventBuilder


class EventProcessor(LoggableMixin):
    event_discovery = EventDiscovery
    event_validator = Event

    @classmethod
    async def process_event(cls, raw_event: str) -> str:
        try:
            event: Event = cls.parse_event(raw_event)
        except EventException as exc:
            return EventBuilder.error_for(exc).to_json()
        try:
            async with EventContextHolder.with_context(event.id, event.flow_id, event.name) as _:
                event_handler: EventHandler = EventDiscovery.get(event.name, event.version)
                response: ResponseEvent = await event_handler.handle(event)
                return response.to_json()
        except EventException as exc:
            return EventBuilder.error_for(exc, event).to_json()

    @classmethod
    def parse_event(cls, str_event: str) -> Event:
        try:
            event = cls.event_validator.from_json(str_event)
            return event

        except ValidationError as exc:
            cls.logger.exception(
                "Error in event schema validation", exc, extra=dict(event=json.dumps(str_event)),
            )
            raise EventParsingException(exc.to_dict())
        except Exception as exc:
            cls.logger.exception(
                "Error in parser schema procedure", exc, extra=dict(event=json.dumps(str_event)),
            )
            raise EventParsingException(dict(error="Unknown error"))
