from uuid import uuid4
from typing import Optional, Dict

from .http import HttpClient
from .exception.request_exception import BadProtocolException
from ..core.model.event import RequestEvent, ResponseEvent
from ..core.context import _context


class EventClient:
    def __init__(self, url: str):
        self.url = url
        self.http_client = HttpClient()
        self.default_timeout = 60000

    def send_event(
        self,
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
        return self.send_request_event(request_event, timeout)

    def send_request_event(
        self, request_event: RequestEvent, timeout: Optional[int] = None
    ) -> ResponseEvent:
        response = self.http_client.post(
            url=self.url,
            headers={"Content-Type": "application/json", "charset": "UTF-8",},
            payload=request_event.to_json(),
            timeout=timeout or self.default_timeout,
        )
        return self.parse_event(response)

    def parse_event(self, raw_response: str) -> ResponseEvent:
        try:
            return ResponseEvent.from_json(raw_response)
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
    ) -> RequestEvent:
        context_id = getattr(_context.get(), "id", None)
        context_flow_id = getattr(_context.get(), "flow_id", None)

        return RequestEvent(
            name=name,
            version=version,
            payload=payload,
            id=context_id or id or str(uuid4()),
            flow_id=context_flow_id or flow_id or str(uuid4()),
            identity=identity,
            auth=auth,
            metadata=metadata,
        )
