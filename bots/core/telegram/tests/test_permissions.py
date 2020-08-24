from bots.tests.fixtures import *
from .settings import TEST_TELEGRAM_CHAT_ID
from ..permissions import IsAuthenticated


class TestIsAuthenticated:
    def test_has_no_permission(self, user, default_telegram_bot):
        has = IsAuthenticated(default_telegram_bot, TEST_TELEGRAM_CHAT_ID).has_permission()
        assert not has

    def test_get_has_permission(self, user, default_telegram_bot, auth_telegram_user):
        has = IsAuthenticated(default_telegram_bot, TEST_TELEGRAM_CHAT_ID).has_permission()
        assert has
