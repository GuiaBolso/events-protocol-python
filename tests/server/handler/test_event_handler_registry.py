from dataclasses import dataclass
from unittest import TestCase

from events_protocol.server.handler.event_handler import EventHandler
from events_protocol.server.handler.event_handler_discovery import \
    EventDiscovery


@dataclass
class _TestEventHandler(EventHandler):
    async def handle():
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
        self.assertIsInstance(event_response, EventHandler)
        self.assertEqual(event_response.event_name, self.event_name)
        self.assertEqual(event_response.event_version, self.event_version)
