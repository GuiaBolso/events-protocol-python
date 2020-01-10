from uuid import UUID
from typing import Dict, Any, Optional

from ..model.event import RequestEvent
from ..exception.event_exception import MissingEventInformationException


class EventBuilder:
    def __init__(
        self,
        name: str,
        version: int,
        id: UUID,
        flow_id: UUID,
        payload: Any,
        identity: Any,
        auth: Any,
        metadata: Any,
    ) -> None:
        self.name = name
        self.version = version
        self.id = id
        self.flow_id = flow_id
        self.payload = payload
        self.identity = identity
        self.auth = auth
        self.metadata = metadata

    def build_request_event(self) -> RequestEvent:
        self.__validate_fields()
        return RequestEvent(
            name=self.name
            version=self.version
        )
    
    def __validate_fields(self):
        if not self.name:
            raise MissingEventInformationException("Missing event name.")
        elif not self.version:
            raise MissingEventInformationException("Missing event version.")
        elif not self.id:
            raise MissingEventInformationException("Missing event id.")
        elif not self.flow_id:
            raise MissingEventInformationException("Missing event flow_id.")
