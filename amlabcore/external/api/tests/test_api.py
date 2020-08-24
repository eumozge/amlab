import copy

import pytest
import requests

from amlabcore.tests.mock import MockResponse
from .settings import *
from ..auth import Anonymous, BearerToken
from ..client import DefaultAPIClient, DefaultAPILog
from ..headers import HEADERS_CONTENT_TYPE_JSON


@pytest.fixture
def auth():
    return BearerToken(TEST_TOKEN)


@pytest.fixture
def log(response):
    return DefaultAPILog(TEST_API_NAME)


@pytest.fixture
def client(auth, log):
    return DefaultAPIClient(
        auth=auth,
        api_url=TEST_API_URL,
        log=log,
        headers=HEADERS_CONTENT_TYPE_JSON
    )


@pytest.fixture
def response():
    return MockResponse(
        status_code=200,
        url="", method="",
        request_data=dict(), response_json_data=dict()
    )


class TestAuth:
    def test_bearer(self):
        request = requests.Request()
        BearerToken(TEST_TOKEN)(request)
        assert request.headers == {'Authorization': f"Bearer {TEST_TOKEN}"}

    def test_anonymous(self):
        request = requests.Request()
        Anonymous()(request)
        assert request.headers == dict()


class TestClient:
    def test_call(self, mocker, auth, client, response):
        request = mocker.patch.object(requests, 'request', return_value=response)
        headers = {'foo': 'bar'}
        client.call(
            method="GET",
            endpoint=TEST_API_ENDPOINT,
            headers=headers
        )
        reference_headers = copy.copy(HEADERS_CONTENT_TYPE_JSON)
        reference_headers.update(headers)
        request.assert_called_with(
            "GET",
            f"{TEST_API_URL}{TEST_API_ENDPOINT}",
            auth=auth,
            headers=reference_headers
        )
        assert client.last_request == response

    def test_write_log(self, mocker, auth, client, response):
        mocker.patch.object(requests, 'request', return_value=response)
        write = mocker.patch.object(DefaultAPILog, 'write')
        client.call(method="GET", endpoint=TEST_API_ENDPOINT)
        write.assert_called_with(response)


class TestLog:
    @pytest.mark.parametrize('status_code,digital_level', [
        (200, 20), (300, 40), (500, 40)
    ])
    def test_get_digital_log_level(self, log, response, status_code, digital_level):
        response.status_code = status_code
        level = log.get_digital_log_level(response)
        assert level == digital_level

    def test_get_log_message(self, log, response):
        message = log.get_log_message(response)
        reference = {
            'api': log.api,
            'request': {
                'url': response.request.url,
                'method': response.request.method,
                'body': response.request.body
            },
            'response': response.json(),
            'status': response.status_code
        }
        assert message == reference
