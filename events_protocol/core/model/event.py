from abc import ABC
from uuid import UUID
from dataclasses import dataclass
from typing import Dict, Generic, Optional, Any

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Event(ABC):
    name: str
    version: int
    id: UUID
    flow_id: UUID
    payload: Dict
    identity: Dict
    auth: Dict
    metadata: Dict

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
        return not self.is_success and not self.is_error

    def get_error_type(self) -> None:
        raise NotImplementedError('Method "get_error_type" is not implemented yet')


@dataclass
class RequestEvent(Event):
    pass


@dataclass
class EventMessage:
    code: str
    parameters: Dict[str, Optional[Any]]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RawEvent:
    name: Optional[str]
    version: Optional[int]
    id: Optional[UUID]
    flow_id: Optional[UUID]
    payload: Optional[Dict[str, Optional[Any]]]
    identity: Optional[Dict[str, Optional[Any]]]
    auth: Optional[Dict[str, Optional[Any]]]
    metadata: Optional[Dict[str, Optional[Any]]]
