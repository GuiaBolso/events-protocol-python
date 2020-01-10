class BaseRequestException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TimeoutException(BaseRequestException):
    pass


class FailedDependencyException(BaseRequestException):
    pass


class BadProtocolException(BaseRequestException):
    pass
