from typing import Dict, Any, Optional

from .model.event_error_type import EventErrorType


class EventException(RuntimeError):
    def __init__(
        self,
        code: str,
        parameters: Dict[str, Optional[Any]],
        event_error_type: EventErrorType = EventErrorType.GENERIC,
        expected: bool = False,
    ):
        super().__init__(code, parameters, event_error_type, expected)
        self.code = code
        self.parameters = parameters
        self.event_error_type = event_error_type
        self.expected = expected


class MissingEventInformationException(EventException):
    pass


class EventValidationException(EventException):
    __CODE = "INVALID_COMMUNICATION_PROTOCOL"
    __TYPE = EventErrorType.BAD_REQUEST

    def __init__(self, property_name: str) -> None:
        super().__init__(
            code=self.__CODE,
            parameters={"missingProperty": property_name,},
            event_error_type=self.__TYPE,
        )


class EventFailedDependencyException(EventException):
    __CODE = "FAILED_DEPENDENCY"
    __TYPE = EventErrorType.GENERIC

    def __init__(self, message: str):
        super().__init__(
            code=self.__CODE, parameters={"message": message,}, event_error_type=self.__TYPE,
        )


class EventTimeoutException(EventException):
    __CODE = "EVENT_TIMEOUT"
    __TYPE = EventErrorType.GENERIC

    def __init__(self, message: str):
        super().__init__(
            code=self.__CODE, parameters={"message": message,}, event_error_type=self.__TYPE,
        )
