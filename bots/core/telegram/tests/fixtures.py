import pytest

from amlabcore.tests import MockResponse
from bots.models import Bot, TelegramUser, Token
from .objects import TestTelegramClient
from .settings import TEST_BOT_NAME, TEST_TELEGRAM_CHAT_ID, TEST_USERNAME
from .utils import get_telegram_hook_message
from ..client import TelegramClient
from ..message import Message

__all__ = (
    'telegram_client',
    'success_telegram_api_call',
    'json_message',
    'clean_json_message',
    'object_message',
    'default_telegram_bot',
    'auth_telegram_token',
    'auth_telegram_user',
)


@pytest.fixture
def telegram_client():
    return TestTelegramClient


@pytest.fixture
def success_telegram_api_call(monkeypatch):
    def call(*args, **kwargs):
        return MockResponse(200, dict(), '/', 'post')
    setattr(TelegramClient, 'call', call)


@pytest.fixture
def json_message(auth_telegram_token):
    return get_telegram_hook_message(text=f"/start {auth_telegram_token.key}")


@pytest.fixture
def clean_json_message(json_message):
    return json_message['message']


@pytest.fixture
def object_message(clean_json_message):
    return Message(clean_json_message)


@pytest.fixture
def default_telegram_bot():
    return Bot.objects.get_or_create(slug=TEST_BOT_NAME, name=TEST_BOT_NAME)[0]


@pytest.fixture
def auth_telegram_token(user, default_telegram_bot):
    return Token.objects.get_or_create(user=user, bot=default_telegram_bot)[0]


@pytest.fixture
def auth_telegram_user(user, default_telegram_bot):
    return TelegramUser.objects.get_or_create(
        user=user, chat_id=TEST_TELEGRAM_CHAT_ID, username=TEST_USERNAME, bot=default_telegram_bot
    )[0]
