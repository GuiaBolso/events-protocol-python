from typing import Optional

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
