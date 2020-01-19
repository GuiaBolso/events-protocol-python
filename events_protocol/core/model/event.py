from abc import ABC
from uuid import uuid4
from dataclasses import dataclass, field
from typing import Dict, Generic, Optional, Any

from dataclasses_json import dataclass_json, LetterCase

from .event_error_type import EventErrorType


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Event(ABC):
    name: str
    version: int
    payload: Dict[str, Any]
    id: Optional[str] = field(default_factory=lambda: str(uuid4()))
    flow_id: Optional[str] = field(default_factory=lambda: str(uuid4()))
    identity: Optional[Dict[str, Any]] = field(default_factory=dict)
    auth: Optional[Dict[str, Any]] = field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

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


@dataclass
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


@dataclass
class RequestEvent(Event):
    pass


@dataclass
class EventMessage:
    code: str
    parameters: Dict[str, Optional[Any]]
