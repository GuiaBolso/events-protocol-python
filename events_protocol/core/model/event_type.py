import typing
from enum import Enum, unique


class EventType(Enum):
    @classmethod
    def is_in(cls, item: typing.Any) -> bool:
        try:
            cls(item)
            return True
        except ValueError:
            return False

    def __str__(self) -> str:
        return str(self.value)


@unique
class EventErrorType(EventType):
    GENERIC = "error"
    BAD_PROTOCOL = "badProtocol"
    BAD_REQUEST = "badRequest"
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "notFound"
    FORBIDDEN = "forbidden"
    USER_DENIED = "userDenied"
    RESOURCE_DENIED = "resourceDenied"
    EXPIRED = "expired"
    UNKNOWN = "unknown"

    @classmethod
    def get_type(cls, error: str) -> "EventErrorType":
        try:
            return cls(error)
        except ValueError:
            return cls.UNKNOWN


@unique
class EventSuccessType(EventType):
    SUCCESS = "response"
    REDIRECT = "redirect"

    @classmethod
    def get_type(cls, success: str) -> typing.Optional["EventSuccessType"]:
        try:
            return cls(success)
        except ValueError:
            return None
