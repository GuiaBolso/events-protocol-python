from uuid import uuid4
from typing import Optional, Dict

from .http import HttpClient
from .exception.request_exception import BadProtocolException
from ..core.model.event import RequestEvent, ResponseEvent, RawEvent
from ..core.validation import EventValidator


class EventClient:
    def __init__(self):
        self.http_client = HttpClient()
        self.event_validator = EventValidator()
        self.default_timeout = 60000

    def send_event(
        self,
        url: str,
        name: str,
        version: int,
        payload: Optional[Dict] = {},
        id: str = None,
        flow_id: str = None,
        identity: Dict = {},
        auth: Dict = {},
        metadata: Dict = {},
        timeout: Optional[int] = None,
    ) -> ResponseEvent:
        request_event = self.build_request_event(
            name, version, payload, id, flow_id, identity, auth, metadata
        )
        return self.send_request_event(url, request_event, timeout)

    def send_request_event(
        self, url: str, request_event: RequestEvent, timeout: Optional[int] = None
    ) -> ResponseEvent:
        response = self.http_client.post(
            url=url,
            headers={"Content-Type": "application/json", "charset": "UTF-8",},
            payload=request_event.to_json(),
            timeout=timeout or self.default_timeout,
        )
        return self.parse_event(response)

    def parse_event(self, raw_response: str) -> ResponseEvent:
        try:
            raw_event = RawEvent.from_json(raw_response)
            # TODO: Verify if this bellow line is necessary
            return self.event_validator.validate_as_response_event(raw_event)
        except KeyError as e:
            raise BadProtocolException("Error on parsing event response")

    def build_request_event(
        self,
        name: str,
        version: int,
        payload: Dict,
        id: str = None,
        flow_id: str = None,
        identity: Dict = {},
        auth: Dict = {},
        metadata: Dict = {},
    ):
        return RequestEvent(
            name=name,
            version=version,
            payload=payload,
            id=id or str(uuid4()),
            flow_id=flow_id or str(uuid4()),
            identity=identity,
            auth=auth,
            metadata=metadata,
        )
