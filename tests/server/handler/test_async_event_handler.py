from unittest import TestCase

from events_protocol.core.exception import EventNotFoundException
from events_protocol.core.logging.supressor import supress_log
from events_protocol.server.handler.event_handler import AsyncEventHandler, EventHandler
from events_protocol.server.handler.event_handler_discovery import EventDiscovery

from dataclasses import dataclass


class TestAsyncEventHandler(TestCase):
    @supress_log
    def test_add_event_handler_getting_correct_one(self):
        class FakeEventHandler(AsyncEventHandler):
            pass

        event_name = "put:test:here"
        event_version = 2
        expected_event_handler = FakeEventHandler
        EventDiscovery.add(event_name, expected_event_handler, version=event_version)
        event_handler = EventDiscovery.get(event_name, event_version)
        self.assertEqual(expected_event_handler, event_handler)

    def test_add_event_handler_getting_raising_event_not_found_exception(self):
        class FakeEventHandler(AsyncEventHandler):
            pass

        event_name = "put:test:here"
        event_version = 2
        wrong_event_version = 3
        expected_event_handler = FakeEventHandler
        EventDiscovery.add(event_name, expected_event_handler, version=event_version)
        with self.assertRaises(EventNotFoundException):
            EventDiscovery.get(event_name, wrong_event_version)

    @supress_log
    def test_add_event_handler_with_wrong_name_raising_value_error(self):
        class FakeEventHandler(AsyncEventHandler):
            pass

        event_name = "wrong/mame:test:here"
        event_version = 2
        expected_event_handler = FakeEventHandler

        with self.assertRaises(ValueError):
            EventDiscovery.add(event_name, expected_event_handler, version=event_version)

@dataclass
class _TestEventHandler(AsyncEventHandler):

    @classmethod
    async def handle(cls):
        pass


class TestEventRegister(TestCase):
    event_name = "test:event"
    event_version = 1

    def test_event_instantiation(self):
        event_tester = _TestEventHandler(
            event_name=self.event_name, event_version=self.event_version,
        )
        event_response = EventDiscovery.get(
            event_name=event_tester.event_name, event_version=event_tester.event_version,
        )
        self.assertIsInstance(event_response, AsyncEventHandler)
        self.assertEqual(event_response.event_name, self.event_name)
        self.assertEqual(event_response.event_version, self.event_version)