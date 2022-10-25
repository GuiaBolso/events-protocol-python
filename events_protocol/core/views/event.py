from http import HTTPStatus

from aiohttp.web import Response
from events_protocol.server.parser.event_processor import *

from .aiohttp import AIOHTTPView


class DataDogAsyncEventProcessor(AsyncEventProcessor):
    @classmethod
    async def process_event(cls, raw_event: str, request) -> str:
        event = None
        try:
            event: Event = cls.parse_event(raw_event)
            
            async with EventContextHolder.with_async_context(
                context_id=event.id, 
                context_flow_id=event.flow_id,
                event_name=event.name, 
                event_version=event.version,
                user_id=event.user_id,
                user_type=event.user_type,
            ) as _:
                request.dd_resource = "{}:v{}".format(event.name, event.version)
                request.tags = {"UserID": event.user_id, "UserType": event.user_type, "FlowID": event.flow_id, "EventID": event.id, "Origin": event.origin}
                event_handler: AsyncEventHandler = EventDiscovery.get(event.name, event.version)
                response: ResponseEvent = await event_handler.handle(event)
                return response.to_json()
        except EventException as exception:
            return EventBuilder.error_for(exception, event).to_json()

class EventView(AIOHTTPView):
    async def _post(self):
        response = await DataDogAsyncEventProcessor.process_event(self.body, self.request)
        return Response(body=response, status=HTTPStatus.OK, headers=self._base_header)
