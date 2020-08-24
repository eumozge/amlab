from bots.core.templates.tests.settings import TEST_TEMPLATE_SLUG
from .settings import TEST_BOT_NAME, TEST_BOT_TOKEN
from ..client import TelegramClient, TelegramLog
from ..commands import Command, Help, Start
from ..handlers import TelegramHandler
from ..message import Message
from ..permissions import IsAuthenticated

TestTelegramClient = TelegramClient(
    name=TEST_BOT_NAME,
    token=TEST_BOT_TOKEN,
    log=TelegramLog("telegram")
)


class TestIsAuthenticated(IsAuthenticated):
    template_slug = TEST_TEMPLATE_SLUG


class TestStartCommand(Start):
    template_slug = TEST_TEMPLATE_SLUG


class TestHelpCommand(Help):
    template_slug = TEST_TEMPLATE_SLUG


class TestAuthCommand(Command):
    name = "auth-is-necessary"
    template_slug = TEST_TEMPLATE_SLUG
    permission_classes = (TestIsAuthenticated,)

    def _command_processing(self):
        pass


class TestTelegramHandler(TelegramHandler):
    client = TestTelegramClient
    message_class = Message
    command_classes = (TestStartCommand, TestHelpCommand, TestAuthCommand)
