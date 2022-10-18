from unittest import TestCase
from unittest.mock import patch, MagicMock

from requests.exceptions import Timeout, ReadTimeout, ConnectTimeout

from events_protocol.client.http import HttpClient
from events_protocol.client.exception.request_exception import (
    TimeoutException,
    FailedDependencyException,
)


class HttpClientTest(TestCase):
    def setUp(self):
        self.http_client = HttpClient()

    @patch("events_protocol.client.http.requests")
    def test_success_response(self, requests):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = "THIS IS A TEST"

        requests.post.return_value = response_mock

        returned_value = self.http_client.post(
            url="http://test.com/", headers=None, payload=None, timeout=1000
        )

        self.assertEqual(response_mock.text, returned_value)

    @patch("events_protocol.client.http.requests")
    def test_timeout_exception(self, requests):
        requests.post.side_effect = Timeout()

        with self.assertRaises(TimeoutException):
            self.http_client.post(url="http://test.com/", headers=None, payload=None, timeout=1000)

    @patch("events_protocol.client.http.requests")
    def test_read_timeout_exception(self, requests):
        requests.post.side_effect = ReadTimeout()

        with self.assertRaises(TimeoutException):
            self.http_client.post(url="http://test.com/", headers=None, payload=None, timeout=1000)

    @patch("events_protocol.client.http.requests")
    def test_connect_timeout_exception(self, requests):
        requests.post.side_effect = ConnectTimeout()

        with self.assertRaises(TimeoutException):
            self.http_client.post(url="http://test.com/", headers=None, payload=None, timeout=1000)

    @patch("events_protocol.client.http.requests")
    def test_not_ok_response(self, requests):
        response_mock = MagicMock()
        response_mock.ok = False

        requests.post.return_value = response_mock

        with self.assertRaises(FailedDependencyException):
            self.http_client.post(
                url="http://test.com/", headers=None, payload=None, timeout=1000,
            )
