from contextvars import ContextVar


class EventContext:
    __slots__ = ["__id", "__flow_id"]

    def __init__(self, id, flow_id):
        self.__id = id
        self.__flow_id = flow_id

    @property
    def id(self):
        return self.__id

    @property
    def flow_id(self):
        return self.__flow_id


_context: ContextVar[EventContext] = ContextVar("event_context", default=None)
