import typing
from enum import Enum, unique


from events_protocol.core.utils.class_property import ClassProperty


def iter_enum(input_enum: typing.List[Enum]) -> typing.Any:
    for item in input_enum:
        if isinstance(item, Enum):
            yield item.value
        else:
            yield item


class EventType(Enum):
    def all(cls):
        return iter_enum(cls)

    @classmethod
    def is_in(cls, item: typing.Any):
        if isinstance(item, Enum):
            item = item.value
        return item in iter_enum(cls)

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
