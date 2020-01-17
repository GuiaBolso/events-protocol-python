from enum import Enum, unique


@unique
class EventErrorType(Enum):
    GENERIC = "error"
    BAD_REQUEST = "badRequest"
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "notFound"
    FORBIDDEN = "forbidden"
    USER_DENIED = "userDenied"
    RESOURCE_DENIED = "resourceDenied"
    EXPIRED = "expired"
    UNKNOWN = "unknown"

    @classmethod
    def get_error_type(cls, error: str):
        try:
            return cls(error)
        except ValueError:
            return cls.UNKNOWN
