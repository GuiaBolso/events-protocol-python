from typing import Any, Dict, Optional

from .model.event_type import EventErrorType


class EventException(RuntimeError):
    _CODE: str = ""
    _TYPE: EventErrorType = EventErrorType.GENERIC

    def __init__(
        self, parameters: Dict[str, Optional[Any]], expected: bool = False,
    ):
        super().__init__(self._CODE, parameters, self._TYPE, expected)
        self.parameters = parameters
        self.expected = expected

    @property
    def code(self) -> str:
        return self._CODE

    @property
    def event_error_type(self) -> EventErrorType:
        return self._TYPE


class MessagebleEventException(EventException):
    def __init__(self, message: str):
        super().__init__(parameters={"message": message})


class EventNotFoundException(MessagebleEventException):
    _CODE = "EVENT_NOT_FOUND"
    _TYPE = EventErrorType.NOT_FOUND


class MissingEventInformationException(EventException):
    _CODE = "MISSING_FIELDS"
    _TYPE = EventErrorType.BAD_REQUEST


class EventParsingException(EventException):
    _CODE = "INVALID_COMMUNICATION_PROTOCOL"
    _TYPE = EventErrorType.BAD_PROTOCOL


class EventFailedDependencyException(MessagebleEventException):
    _CODE = "FAILED_DEPENDENCY"


class EventTimeoutException(MessagebleEventException):
    _CODE = "EVENT_TIMEOUT"
