import pytest

from bots.models import TelegramCommandLog, TelegramUser, Token
from bots.core.templates import DjangoTemplate
from bots.tests.fixtures import *
from .settings import TEST_TELEGRAM_CHAT_ID
from ..client import TelegramClient
from ..commands import Start, Help


@pytest.fixture
def command_start(object_message,
                  telegram_client,
                  default_telegram_bot,
                  success_telegram_api_call,
                  default_template_message):

    class TestStartCommand(Start):
        template_slug = default_template_message.slug

    command = TestStartCommand(object_message, client=telegram_client, bot=default_telegram_bot)
    return command


@pytest.fixture
def command_help(object_message,
                 telegram_client,
                 default_telegram_bot,
                 success_telegram_api_call,
                 default_template_message):

    class TestHelpCommand(Help):
        template_slug = default_template_message.slug

    command = TestHelpCommand(object_message, client=telegram_client, bot=default_telegram_bot)
    return command


class TestStart:
    def test_is_auth_created(self, user, command_start,
                             clean_json_message, auth_telegram_token, default_telegram_bot):
        command_start.run()
        telegram_user = TelegramUser.objects.get(user=user, bot=default_telegram_bot)
        chat = clean_json_message['chat']
        assert telegram_user.chat_id == chat['id'] and telegram_user.username == chat['username']

    def test_is_token_deleted(self, user, command_start, auth_telegram_token):
        command_start.run()
        is_token_deleted = not Token.objects.filter(id=auth_telegram_token.id).exists()
        assert is_token_deleted

    def test_is_log_created(self, user, command_start, auth_telegram_token, default_telegram_bot):
        command_start.run()
        is_log_created = TelegramCommandLog.objects.filter(
            user=user, command=Start.name, bot=default_telegram_bot
        ).exists()
        assert is_log_created

    def test_token_doesnt_exists(self, user, command_start, auth_telegram_token):
        auth_telegram_token.key = "unknown"
        auth_telegram_token.save()
        command_start.run()

    def test_run_without_token(self, user, command_start, auth_telegram_token):
        command_start.message.message['text'] = f"/{command_start.name}"
        command_start.run()

    def test_is_welcome_sent(self, mocker, command_start,
                             auth_telegram_token, default_template_message):
        welcome = mocker.patch.object(TelegramClient, 'send_message')
        command_start.run()
        prepared_message = DjangoTemplate().render_from_raw(default_template_message.text)
        welcome.assert_called_with(
            chat_id=TEST_TELEGRAM_CHAT_ID, prepared_message=prepared_message
        )


class TestHelp:
    def test_run(self, mocker, command_help, default_template_message):
        sent = mocker.patch.object(TelegramClient, 'send_message')
        command_help.run()
        prepared_message = DjangoTemplate().render_from_raw(default_template_message.text)
        sent.assert_called_with(
            chat_id=TEST_TELEGRAM_CHAT_ID, prepared_message=prepared_message
        )
