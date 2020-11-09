import re
import typing

from events_protocol.core.exception import EventNotFoundException
from events_protocol.core.logging.mixins.loggable import LoggableMixin
from events_protocol.server.handler.event_handler import EventHandler, AsyncEventHandler


class EventDiscovery(LoggableMixin):
    _events: typing.Dict[
        typing.Tuple[str, int], typing.Union[EventHandler, AsyncEventHandler]
    ] = dict()
    _EVENT_NAME_STD: str = r"[a-z_]+[a-z]:[a-z_]+[a-z](:[a-z]+[a-z])*"

    @classmethod
    def add(cls, event_name: str, event_handler: EventHandler, version: int = 1) -> None:
        if not issubclass(event_handler, EventHandler):
            raise TypeError(f"event_handler must be of type EventHandler")
        res: re.Match = re.match(cls._EVENT_NAME_STD, event_name)
        if res is None or res.string != event_name:
            raise ValueError(
                f"Event name {event_name} does not meet the standard {cls._EVENT_NAME_STD}"
            )
        cls.logger.info(f"Registering event handler for {event_name} V{version}")
        cls._events[(event_name, version)] = event_handler

    @classmethod
    def get(cls, event_name: str, version: int = 1) -> EventHandler:
        event: typing.Union[EventHandler, None] = cls._events.get((event_name, version))
        if event is None:
            raise EventNotFoundException(
                f"Event Name {event_name} of version {version} was not found"
            )
        return event
