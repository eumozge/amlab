from bots.core.templates import DjangoTemplate
from .client import AmlabTelegramClient
from .commands import AmlabHelp, AmlabStart
from ..handlers import TelegramHandler
from ..message import Message


class AmlabTelegramHandler(TelegramHandler):
    client = AmlabTelegramClient
    message_class = Message
    template_class = DjangoTemplate
    command_classes = (AmlabStart, AmlabHelp)
