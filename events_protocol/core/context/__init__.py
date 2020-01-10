from contextvars import ContextVar

from .event_context import EventContext


_context: ContextVar[EventContext] = ContextVar('event_context', default=None)


class EventContextHolder:

    @staticmethod
    def get_context() -> EventContext:
        return _context.get()
    
    @staticmethod
    def set_context(event_context: EventContext) -> None:
        _context.set(event_context)

    @staticmethod
    def clean() -> None:
        _context.set(None)
