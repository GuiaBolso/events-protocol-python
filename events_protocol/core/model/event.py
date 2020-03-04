from typing import Any, Dict, Generic, Optional
from uuid import uuid4

from .base import CamelPydanticMixin
from .event_type import EventErrorType, EventSuccessType, EventType

PayloadType = Dict[str, Any]


class Event(CamelPydanticMixin):
    name: str
    version: int
    payload: PayloadType = dict()
    id: Optional[str] = str(uuid4())
    flow_id: Optional[str] = str(uuid4())
    identity: Optional[Dict[str, Any]] = dict()
    auth: Optional[Dict[str, Any]] = dict()
    metadata: Optional[Dict[str, Any]] = dict()

    def payload_as(self, clazz: CamelPydanticMixin) -> CamelPydanticMixin:
        return clazz(**self.payload)

    def identity_as(self, clazz: Generic) -> Generic:
        return clazz.from_dict(self.identity)

    def auth_as(self, clazz: Generic) -> Generic:
        return clazz.from_dict(self.auth)

    @property
    def user_id(self) -> Optional[int]:
        if self.identity is not None:
            user = self.identity.get("userId")
            if user:
                return int(user)

    @property
    def origin(self) -> Optional[str]:
        if self.metadata is not None:
            return self.metadata.get("origin")


class ResponseEvent(Event):
    @staticmethod
    def from_event(
        event: Event, event_type: EventType = EventSuccessType.SUCCESS
    ) -> "ResponseEvent":
        response_event = ResponseEvent.from_object(event)
        response_event.name = f"{response_event.name}:{event_type}"
        return response_event

    @property
    def is_success(self) -> bool:
        return self.event_type == EventSuccessType.SUCCESS

    @property
    def is_redirect(self) -> bool:
        return self.event_type == EventSuccessType.REDIRECT

    @property
    def is_error(self) -> bool:
        return EventErrorType.is_in(self.event_type)

    @property
    def _event_name(self) -> str:
        return self.name.split(":")[-1]

    @property
    def event_type(self) -> EventType:
        return EventSuccessType.get_type(self._event_name) or EventErrorType.get_type(
            self._event_name
        )

    @property
    def error_type(self) -> EventErrorType:
        if self.is_error:
            return EventErrorType.get_type(self._event_name)
        raise ValueError("This is not an error event.")


class RequestEvent(Event):
    pass


class EventMessage(CamelPydanticMixin):
    code: str
    parameters: Dict[str, Optional[Any]]
