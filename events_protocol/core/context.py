from contextvars import ContextVar


class EventContext:
    __slots__ = ["id", "flow_id"]

    def __init__(self, id, flow_id):
        self.id = id
        self.flow_id = flow_id


_context: ContextVar[EventContext] = ContextVar("event_context", default=None)
