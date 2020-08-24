import pytest
from rest_framework import status

from bots.core.telegram import factory
from bots.models import TelegramUser
from bots.tests.fixtures import *
from .objects import TestAuthCommand, TestTelegramHandler
from .settings import TEST_BOT_TOKEN
from ..client import TelegramClient


@pytest.fixture
def handler_mock(mocker, success_telegram_api_call):
    mocker.patch.object(
        factory, 'get_handler_by_token',
        return_value=TestTelegramHandler()
    )


@pytest.fixture
def exception_template(default_template_message):
    default_template_message.text = "exception"
    default_template_message.save()
    return default_template_message


class TestAPIHookProcessing:
    def test_start(self, api_client, user, handler_mock, json_message,
                   success_telegram_api_call, default_template_message, default_telegram_bot):
        response = api_client.post(
            f"/api/v1/bots/telegram/hook/{TEST_BOT_TOKEN}/", data=json_message
        )
        assert response.status_code == status.HTTP_200_OK
        assert TelegramUser.objects.filter(user=user).exists()

    def test_auth_permission(self, mocker, api_client, user, handler_mock,
                             json_message, exception_template, default_telegram_bot):
        send_error = mocker.patch.object(TelegramClient, 'send_message', return_value=True)
        json_message['message']['text'] = f"/{TestAuthCommand.name}"
        response = api_client.post(
            f"/api/v1/bots/telegram/hook/{TEST_BOT_TOKEN}/", data=json_message
        )
        assert response.status_code == status.HTTP_200_OK
        send_error.assert_called_with(
            chat_id=json_message['message']['chat']['id'], prepared_message=exception_template.text
        )
