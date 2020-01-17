from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from events_protocol.core.model.event import RequestEvent, ResponseEvent
from events_protocol.core.model.event_error_type import EventErrorType
from events_protocol.client.event_client import EventClient
from events_protocol.client.exception.request_exception import BadProtocolException


class EventClientTest(TestCase):
    def setUp(self):
        self.client = EventClient()
    
    @patch('events_protocol.client.event_client.HttpClient.post')
    def test_success_response(self, post_method):
        event = RequestEvent(
            name='event:name',
            version=1,
            id=uuid4(),
            flow_id=uuid4(),
            payload={'test': 'test'},
            identity={},
            auth={},
            metadata={},
        )
        response_event = ResponseEvent(
            name="event:name:response",
            version=1,
            id=uuid4(),
            flow_id=uuid4(),
            payload={'test': 'test'},
            identity={},
            auth={},
            metadata={},
        )

        post_method.return_value = response_event.to_json()
        response = self.client.send_event('url', event)

        self.assertTrue(response.is_success)
        self.assertEqual(response, response_event)
    
    @patch('events_protocol.client.event_client.HttpClient.post')
    def test_error_response(self, post_method):
        event = RequestEvent(
            name='event:name',
            version=1,
            id=uuid4(),
            flow_id=uuid4(),
            payload={'test': 'test'},
            identity={},
            auth={},
            metadata={},
        )
        response_event = ResponseEvent(
            name="event:name:error",
            version=1,
            id=uuid4(),
            flow_id=uuid4(),
            payload={'test': 'test'},
            identity={},
            auth={},
            metadata={},
        )

        post_method.return_value = response_event.to_json()
        response = self.client.send_event('url', event)
        
        self.assertTrue(response.is_error)
        self.assertEqual(EventErrorType.GENERIC, response.error_type)
        self.assertEqual(response, response_event)
    
    @patch('events_protocol.client.event_client.HttpClient.post')
    def test_invalid_response(self, post_method):
        event = RequestEvent(
            name='event:name',
            version=1,
            id=uuid4(),
            flow_id=uuid4(),
            payload={'test': 'test'},
            identity={},
            auth={},
            metadata={},
        )

        post_method.return_value = '{}'
        
        with self.assertRaises(BadProtocolException):
            response = self.client.send_event('url', event)
