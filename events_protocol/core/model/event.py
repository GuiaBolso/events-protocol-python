from abc import ABC
from typing import Any, Dict, Generic, Optional, Union
from uuid import UUID, uuid4

from .base import PascalPydanticMixin
from .event_error_type import EventErrorType


class Event(PascalPydanticMixin):
    name: str
    version: int
    payload: Dict[str, Any]
    id: Optional[str] = str(uuid4())
    flow_id: Optional[str] = str(uuid4())
    identity: Optional[Dict[str, Any]] = dict
    auth: Optional[Dict[str, Any]] = dict
    metadata: Optional[Dict[str, Any]] = dict

    def payload_as(self, clazz: Generic) -> Generic:
        return clazz.from_dict(self.payload)

    def identity_as(self, clazz: Generic) -> Generic:
        return clazz.from_dict(self.identity)

    def auth_as(self, clazz: Generic) -> Generic:
        return clazz.from_dict(self.auth)

    @property
    def user_id(self) -> Optional[int]:
        if self.identity is not None:
            return int(self.identity.get("userId"))

    @property
    def origin(self) -> Optional[str]:
        if self.metadata is not None:
            return self.metadata.get("origin")


class ResponseEvent(Event):
    @property
    def is_success(self) -> bool:
        return self.name.endswith(":response")

    @property
    def is_redirect(self) -> bool:
        return self.name.endswith(":redirect")

    @property
    def is_error(self) -> bool:
        return not self.is_success and not self.is_redirect

    @property
    def error_type(self) -> EventErrorType:
        if self.is_error:
            error = self.name.split(":")[-1]
            return EventErrorType.get_error_type(error)
        raise ValueError("This is not an error event.")


class RequestEvent(Event):
    pass


class EventMessage(PascalPydanticMixin):
    code: str
    parameters: Dict[str, Optional[Any]]
