from contextlib import suppress

from django.utils.functional import cached_property

from bots.models import TelegramUser
from .client import TelegramClient
from .commands import Command
from .message import MessageParser


class TelegramHandler:
    client = None
    message_class = None
    template_class = None
    command_classes = None

    def __new__(cls, *args, **kwargs):
        assert isinstance(cls.client, TelegramClient), f"got {cls.client}."
        return super().__new__(cls)

    def __init__(self):
        self.message = None

    def parse_message(self, json_message):
        self.message = self.message_class(json_message)
        assert isinstance(self.message, MessageParser), \
            f"message parsing return not a {MessageParser.__class__.__name__} object. " \
            f"Try to use default {MessageParser.__class__.__name__} or inheritance from it."

    def get_start_link(self, token_key):
        return f"https://t.me/{self.client.name}?start={token_key}"

    @staticmethod
    def get_telegram_user(user):
        """TODO At the moment there is only one bot."""
        with suppress(TelegramUser.DoesNotExist):
            return TelegramUser.objects.get(user=user)

    @cached_property
    def bot(self):
        return self.client.get_bot()

    def _validate_commands(self):
        for name, cls in self.commands.items():
            if not isinstance(cls, Command):
                raise ValueError(f"{cls} must be a command instance, got {cls.__name__}.")

    @cached_property
    def commands(self):
        return {
            c.name: c for c in self.command_classes
        }

    @staticmethod
    def check_permission(command):
        permissions = command.get_permissions()
        for perm in permissions:
            if not perm.has_permission():
                message = perm.get_message()
                raise perm.raise_exception(message)

    def run(self, check_permission=True):
        assert self.message is not None, "message isn't parsed, use `parse_message`."
        text = self.message['text']
        if text.is_command:
            command_name = text.clean_command
            if command_name in self.commands:
                command = self.commands[command_name](self.message, self.client, self.bot)
                check_permission and self.check_permission(command)
                return command.run()
        return False

    def send_message(self, chat_id, prepared_message):
        return self.client.send_message(chat_id, prepared_message)
