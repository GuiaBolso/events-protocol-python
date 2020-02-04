from unittest import TestCase

from events_protocol.core.exception import EventNotFoundException
from events_protocol.core.logging.supressor import supress_log
from events_protocol.server.handler.event_handler import EventHandler
from events_protocol.server.handler.event_handler_discovery import EventDiscovery


class TestEventDiscovery(TestCase):
    @supress_log
    def test_add_event_handler_getting_correct_one(self):
        class FakeEventHandler(EventHandler):
            pass

        event_name = "put:test:here"
        event_version = 2
        expected_event_handler = FakeEventHandler
        EventDiscovery.add(event_name, expected_event_handler, version=event_version)
        event_handler = EventDiscovery.get(event_name, event_version)
        self.assertEqual(expected_event_handler, event_handler)

    @supress_log
    def test_add_event_handler_wrongly_raising_type_error(self):
        event_name = "put:test:here"
        event_version = 2
        event_handler = "A string is not a event, dude"

        with self.assertRaises(TypeError):
            EventDiscovery.add(event_name, event_handler, version=event_version)

    def test_add_event_handler_getting_raising_event_not_found_exception(self):
        class FakeEventHandler(EventHandler):
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
        class FakeEventHandler(EventHandler):
            pass

        event_name = "wrong/mame:test:here"
        event_version = 2
        expected_event_handler = FakeEventHandler

        with self.assertRaises(ValueError):
            EventDiscovery.add(event_name, expected_event_handler, version=event_version)
