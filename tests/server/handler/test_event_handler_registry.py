from unittest import TestCase

from events_protocol.server.handler.event_handler import EventHandler
from events_protocol.server.handler.event_handler_discovery import EventDiscovery
from events_protocol.server.handler.event_handler_registry import EventRegister


class _TestEventHandler(EventHandler):
    async def handle():
        pass


class TestEventRegister(TestCase):
    def test_event_instantiation(self):
        class EventTester(EventRegister):
            event_name = "event:top:zera"
            event_version = 1
            event_handler = _TestEventHandler

        EventTester.register_event()
        event = EventDiscovery.get(EventTester.event_name, EventTester.event_version)
        self.assertEqual(event, _TestEventHandler)
