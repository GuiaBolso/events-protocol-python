import json
from unittest import TestCase
from uuid import uuid4

from events_protocol.core.exception import EventParsingException
from events_protocol.core.logging.supressor import supress_log
from events_protocol.core.model.event import Event, CamelPydanticMixin, ResponseEvent
from events_protocol.core.model.event_type import EventErrorType
from tests.utils.sync import make_sync
from events_protocol.server.handler.event_handler import EventHandler
from events_protocol.server.handler.event_handler_registry import EventRegister
from events_protocol.server.parser.event_processor import AsyncEventProcessor, EventProcessor


class FakeSchema(CamelPydanticMixin):
    field: str


class FakeHandler(EventHandler):
    _SCHEMA = FakeSchema

    @classmethod
    async def handle(cls, event: Event):
        return event


class FakeRegister(EventRegister):
    event_version = 2
    event_name = "awesome:test:here"
    event_handler = FakeHandler


class TestAsyncEventProcessor(TestCase):
    @supress_log
    def test_parse_event_with_event_validation_error(self):
        test_json = json.dumps({"awesome": "test"})
        event_processor = AsyncEventProcessor()
        with self.assertRaises(EventParsingException):
            event_processor.parse_event(test_json)

    @supress_log
    def test_parse_event_with_event_parsing_error(self):
        test_json = r"{{wrong_json}"
        event_processor = AsyncEventProcessor()
        with self.assertRaises(EventParsingException):
            event_processor.parse_event(test_json)

    @supress_log
    def test_parse_event_with_valid_event(self):
        test_event = Event(name="event:test", version="2", id=str(uuid4()), flow_id=str(uuid4()))
        test_json = test_event.to_json()
        event_processor = AsyncEventProcessor()
        event = event_processor.parse_event(test_json)
        self.assertEqual(event, test_event)

    @supress_log
    @make_sync
    async def test_process_event_founding_none_event(self):
        test_event = Event(name="event:test", version="2", id=str(uuid4()), flow_id=str(uuid4()))
        test_json = test_event.to_json()
        event_processor = AsyncEventProcessor()
        event = await event_processor.process_event(test_json)
        response: ResponseEvent = ResponseEvent.from_json(event)
        self.assertTrue(response.is_error)
        self.assertEqual(response.event_type, EventErrorType.NOT_FOUND)

    @supress_log
    @make_sync
    async def test_process_event_founding_fake_event(self):
        FakeRegister.register_event()
        test_event = Event(
            name=FakeRegister.event_name,
            version=FakeRegister.event_version,
            id=str(uuid4()),
            flow_id=str(uuid4()),
            payload={},
        )
        test_json = test_event.to_json()
        event_processor = AsyncEventProcessor()
        response = await event_processor.process_event(test_json)
        self.assertEqual(test_json, response)

    @supress_log
    @make_sync
    def test_process_event_(self):
        test_event = Event(name="event:test", version="1", id=str(uuid4()), flow_id=str(uuid4()))
        test_json = test_event.to_json()
        event_processor = EventProcessor()
        event = event_processor.process_event(test_json)
        response: ResponseEvent = ResponseEvent.from_json(event)
        self.assertTrue(response.is_error)
        self.assertEqual(response.event_type, EventErrorType.NOT_FOUND)
