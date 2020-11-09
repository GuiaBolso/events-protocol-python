import typing
from uuid import uuid4

from events_protocol.core.exception import EventException
from events_protocol.core.model.event import (
    Event,
    EventMessage,
    PayloadType,
    ResponseEvent,
)
from events_protocol.core.model.event_type import EventSuccessType
from events_protocol.core.logging.mixins.loggable import LoggableMixin


class EventBuilder(LoggableMixin):
    @classmethod
    def error_for(
        cls,
        exception: typing.Union[EventException],
        event: typing.Optional[Event] = Event(name="", version=1, id=str(uuid4())),
        id_flow=str(uuid4()),
        loggable=True,
    ) -> ResponseEvent:
        event_name = (
            f"{event.name}:{exception.event_error_type}"
            if event.name
            else f"{exception.event_error_type}"
        )

        event_message = EventMessage(code=exception.code, parameters=exception.parameters).to_dict()
        response_event = ResponseEvent.from_object(event)
        response_event.name = event_name
        response_event.payload = event_message
        if loggable:
            cls.logger.error("Event finished with error", extra=response_event.json())
        return response_event

    @classmethod
    def response_for(
        cls,
        event: Event,
        payload: PayloadType,
        event_type: EventSuccessType = EventSuccessType.SUCCESS,
        loggable=True,
    ) -> ResponseEvent:
        response_event = ResponseEvent.from_object(event)
        response_event.name = f"{response_event.name}:{event_type}"
        response_event.payload = payload
        return response_event
