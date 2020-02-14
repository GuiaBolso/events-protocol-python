from unittest import TestCase
from unittest.mock import patch

from events_protocol.client.event_client import EventClient
from events_protocol.client.exception.request_exception import BadProtocolException
from events_protocol.core.context import EventContext, EventContextHolder
from events_protocol.core.model.event import ResponseEvent
from events_protocol.core.model.event_type import EventErrorType


class EventClientTest(TestCase):
    def setUp(self):
        self.client = EventClient("http://test.com/events/")

    @patch("events_protocol.client.event_client.HttpClient.post")
    def test_success_response(self, post_method):
        event = {
            "name": "event:name",
            "version": 1,
            "payload": {"test": "test"},
        }
        response_event = ResponseEvent(
            name="event:name:response", version=1, payload={"test": "test"},
        )

        post_method.return_value = response_event.to_json()
        response = self.client.send_event(**event)

        self.assertTrue(response.is_success)
        self.assertEqual(response, response_event)

    @patch("events_protocol.client.event_client.HttpClient.post")
    def test_error_response(self, post_method):
        event = {
            "name": "event:name",
            "version": 1,
            "payload": {"test": "test"},
        }
        response_event = ResponseEvent(
            name="event:name:error", version=1, payload={"test": "test"},
        )

        post_method.return_value = response_event.to_json()
        response = self.client.send_event(**event)
        self.assertTrue(response.is_error)
        self.assertEqual(EventErrorType.GENERIC, response.error_type)
        self.assertEqual(response, response_event)

    @patch("events_protocol.client.event_client.HttpClient.post")
    def test_invalid_response(self, post_method):
        event = {
            "name": "event:name",
            "version": 1,
            "payload": {"test": "test"},
        }

        post_method.return_value = "{}"

        with self.assertRaises(BadProtocolException):
            self.client.send_event(**event)


class BuildEventTest(TestCase):
    def setUp(self):
        self.client = EventClient("http://test.com/events/")

    def test_build_event_with_context(self):
        context = EventContext(id="my-id", flow_id="my-flow-id", name="test")
        EventContextHolder.set(context)

        event = {
            "name": "event:name",
            "version": 1,
            "payload": {"test": "test"},
            "id": "id-test",
            "flow_id": "flow-id-test",
        }
        builded_event = self.client.build_request_event(**event)

        self.assertEqual(context.id, builded_event.id)
        self.assertEqual(context.flow_id, builded_event.flow_id)

        EventContextHolder.clean()

    def test_build_event_without_context(self):
        event = {
            "name": "event:name",
            "version": 1,
            "payload": {"test": "test"},
            "id": "test-id",
            "flow_id": "test-flow-id",
        }
        builded_event = self.client.build_request_event(**event)

        self.assertEqual(event["id"], builded_event.id)
        self.assertEqual(event["flow_id"], builded_event.flow_id)

    def test_build_event_without_pass_id_and_flow_id(self):
        event = {"name": "event:name", "version": 1, "payload": {"test": "test"}}
        builded_event = self.client.build_request_event(**event)

        self.assertIsNotNone(builded_event.id)
        self.assertIsNotNone(builded_event.flow_id)
