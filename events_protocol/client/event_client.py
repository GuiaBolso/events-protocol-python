from typing import Optional

from .http import HttpClient
from .model.response import Response
from .exception.request_exception import TimeoutException, FailedDependencyException, BadProtocolException
from ..core.model.event import RequestEvent, ResponseEvent, RawEvent
from ..core.validation.strict_event_validator import StrictEventValidator
from ..core.exception.event_exception import EventValidationException


class EventClient:
    def __init__(self):
        self.http_client = HttpClient()
        self.event_validator = StrictEventValidator()
        self.default_timeout = 60000

    def send_event(self, url: str, request_event: RequestEvent, timeout: Optional[int] = None) -> Response:
        try:
            response = self.http_client.post(
                url=url,
                headers={
                    'Content-Type': 'application/json',
                    'charset': 'UTF-8',
                },
                payload=request_event.to_json(),
                timeout=timeout or self.default_timeout
            )
            event = self.parse_event(response)
        except TimeoutException as e:
            pass
        except FailedDependencyException as e:
            pass
        except BadProtocolException as e:
            pass
        else:
            if event.is_success:
                pass
            return response

    def parse_event(self, raw_response: str) -> ResponseEvent:
        try:
            raw_event = RawEvent.from_json(raw_response)
            return self.event_validator.validate_as_response_event(raw_event)
        except EventValidationException as e:
            raise BadProtocolException(e.message)
