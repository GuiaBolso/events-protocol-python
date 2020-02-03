from typing import Dict, Any, Optional

from .model.event_error_type import EventErrorType


class EventException(RuntimeError):
    _CODE: str = None
    _TYPE: EventErrorType = EventErrorType.GENERIC

    def __init__(self,
                 parameters: Dict[str, Optional[Any]],
                 expected: bool = False,):
        super().__init__(self._CODE, parameters, self._TYPE, expected)
        self.code = self._CODE
        self.parameters = parameters
        self.event_error_type = self._TYPE
        self.expected = expected


class MessagebleEventException(EventException):
    def __init__(self, message: str):
        super().__init__(parameters={"message": message})


class EventNotFoundException(MessagebleEventException):
    _CODE = "EVENT_NOT_FOUND"
    _TYPE = EventErrorType.NOT_FOUND


class MissingEventInformationException(EventException):
    pass


class EventValidationException(EventException):
    __CODE = "INVALID_COMMUNICATION_PROTOCOL"
    __TYPE = EventErrorType.BAD_REQUEST

    def __init__(self, property_name: str) -> None:
        super().__init__(
            parameters={"missingProperty": property_name, },
        )


class EventFailedDependencyException(MessagebleEventException):
    _CODE = "FAILED_DEPENDENCY"


class EventTimeoutException(MessagebleEventException):
    _CODE = "EVENT_TIMEOUT"
