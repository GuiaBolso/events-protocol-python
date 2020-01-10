from unittest import TestCase

from events_protocol.core.model.event import RawEvent
from events_protocol.core.validation.strict_event_validator import StrictEventValidator
from events_protocol.core.exception.event_exception import EventValidationException


class StrictEventValidatorForResponseTest(TestCase):
    def setUp(self):
        self.validator = StrictEventValidator()
    
    def test_response_validation(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        response = self.validator.validate_as_response_event(raw_event)

        self.assertEqual('event:name', response.name)
        self.assertEqual(1, response.version)
        self.assertEqual('eventId', response.id)
        self.assertEqual('flowId', response.flow_id)
        self.assertEqual({'value': 42}, response.payload)
        self.assertEqual({}, response.auth)
        self.assertEqual({}, response.identity)
        self.assertEqual({}, response.metadata)
    
    def test_response_validation_without_name(self):
        raw_event = RawEvent(
            name=None,
            version=1,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_response_event(raw_event)
    
    def test_response_validation_without_version(self):
        raw_event = RawEvent(
            name='event:name',
            version=None,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_response_event(raw_event)
    
    def test_response_validation_without_id(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id=None,
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_response_event(raw_event)
    
    def test_response_validation_without_flow_id(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id=None,
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_response_event(raw_event)
    
    def test_response_validation_without_payload(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id='flowId',
            payload=None,
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_response_event(raw_event)
    
    def test_response_validation_without_auth(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth=None,
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_response_event(raw_event)
    
    def test_response_validation_without_identity(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity=None,
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_response_event(raw_event)
    
    def test_response_validation_without_metadata(self):
        raw_event = RawEvent(
            name='event:name',
            version=None,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata=None
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_response_event(raw_event)


class StrictEventValidatorForRequestTest(TestCase):
    def setUp(self):
        self.validator = StrictEventValidator()
    
    def test_request_validation(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        request = self.validator.validate_as_request_event(raw_event)

        self.assertEqual('event:name', request.name)
        self.assertEqual(1, request.version)
        self.assertEqual('eventId', request.id)
        self.assertEqual('flowId', request.flow_id)
        self.assertEqual({'value': 42}, request.payload)
        self.assertEqual({}, request.auth)
        self.assertEqual({}, request.identity)
        self.assertEqual({}, request.metadata)
    
    def test_request_validation_without_name(self):
        raw_event = RawEvent(
            name=None,
            version=1,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_request_event(raw_event)
    
    def test_request_validation_without_version(self):
        raw_event = RawEvent(
            name='event:name',
            version=None,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_request_event(raw_event)
    
    def test_request_validation_without_id(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id=None,
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_request_event(raw_event)
    
    def test_request_validation_without_flow_id(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id=None,
            payload={'value': 42},
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_request_event(raw_event)
    
    def test_request_validation_without_payload(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id='flowId',
            payload=None,
            auth={},
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_request_event(raw_event)
    
    def test_request_validation_without_auth(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth=None,
            identity={},
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_request_event(raw_event)
    
    def test_request_validation_without_identity(self):
        raw_event = RawEvent(
            name='event:name',
            version=1,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity=None,
            metadata={}
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_request_event(raw_event)
    
    def test_request_validation_without_metadata(self):
        raw_event = RawEvent(
            name='event:name',
            version=None,
            id='eventId',
            flow_id='flowId',
            payload={'value': 42},
            auth={},
            identity={},
            metadata=None
        )

        with self.assertRaises(EventValidationException):
            self.validator.validate_as_request_event(raw_event)
