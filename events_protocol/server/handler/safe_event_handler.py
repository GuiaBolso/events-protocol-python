import typing

from events_protocol.server.handler.event_handler import Event, ResponseEvent
from events_protocol.server.handler.event_handler import AsyncEventHandler
from events_protocol.core.exception import EventException

class SafeEventHandler(AsyncEventHandler):
    """
    Defines a safe event handler

    Parameters
    ----------
    event_name : str
        Event endpoint. It should contain only letters and respect the following format:
            - {{name}}:{{name}}
    event_version : int
        Event version

    How to use the template
    -----------------------
    Change the __safe_event_handler to contain the calls to the desired service
    The run method will be override to create a new handler

    See also
    --------
    SafeHandler
    """
    event_name: str
    event_version: typing.Union[None, int]

    def __init__(self):
        super().__init__(self.event_name, self.event_version)
       

    @classmethod
    async def handle(cls, event: Event) -> ResponseEvent:
        """
        Method that will safely handle the current event in the events_protocol library

        Parameters
        ----------
        event: Event
            Event sent by the user

        Returns
        -------
        ResponseEvent
            Response event containing the result of the service
        """
        return await cls.__safe_event_handler(event)

    @classmethod
    async def run(cls, event: Event) -> typing.Dict:
        pass

    @classmethod
    async def __safe_event_handler(cls, event: Event) -> ResponseEvent:
        """
        Implements the integrity verification of the payload and runs the service

        Parameters
        ----------
        event: Event
            Event sent by the user

        Returns
        -------
        ResponseEvent
            Response event containing the result of the service
        """
        try:
            response_event = ResponseEvent.from_event(event)
            response_event.payload = await cls.run(event)
            return response_event
        except EventException as ex:
            exception_event = ResponseEvent.from_event(
                event=event,
                event_type=ex._TYPE,
            )
            exception_event.payload = {
                "message" : ex.parameters["message"],
                "code" : ex._CODE,
            }
            return exception_event