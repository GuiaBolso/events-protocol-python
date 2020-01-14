from typing import Any

from .model.event import RawEvent, ResponseEvent, RequestEvent
from .exception.event_exception import EventValidationException


class EventValidator:
    def validate_as_response_event(self, raw_event: RawEvent) -> ResponseEvent:
        return ResponseEvent(
            name=self.__get_required_property(raw_event, "name"),
            version=self.__get_required_property(raw_event, "version"),
            id=self.__get_required_property(raw_event, "id"),
            flow_id=self.__get_required_property(raw_event, "flow_id"),
            payload=self.__get_required_property(raw_event, "payload"),
            identity=self.__get_required_property(raw_event, "identity"),
            auth=self.__get_required_property(raw_event, "auth"),
            metadata=self.__get_required_property(raw_event, "metadata"),
        )

    def validate_as_request_event(self, raw_event: RawEvent) -> RequestEvent:
        return RequestEvent(
            name=self.__get_required_property(raw_event, "name"),
            version=self.__get_required_property(raw_event, "version"),
            id=self.__get_required_property(raw_event, "id"),
            flow_id=self.__get_required_property(raw_event, "flow_id"),
            payload=self.__get_required_property(raw_event, "payload"),
            identity=self.__get_required_property(raw_event, "identity"),
            auth=self.__get_required_property(raw_event, "auth"),
            metadata=self.__get_required_property(raw_event, "metadata"),
        )

    def __get_required_property(self, raw_event: RawEvent, property_name: str) -> Any:
        property_ = getattr(raw_event, property_name, None)
        if property_ is None:
            raise EventValidationException(property_name)
        return property_
