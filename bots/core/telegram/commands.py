from contextlib import suppress

from contracts import contract
from django.db import transaction

from bots.core.templates import DjangoTemplate
from bots.models import Bot, TelegramCommandLog, TelegramUser, Token
from .client import TelegramClient
from .message import MessageParser


class Command:
    name = None
    template_slug = None
    template_class = DjangoTemplate
    permission_classes = None

    def __new__(cls, *args, **kwargs):
        """
        At the moment there aren't command without template,
        any command must return to user some message.
        Every command makes template request to database and
        it is not a good way for mass notification but now it is not a problem.
        """
        assert cls.name, f"{cls.__name__} provide a command name as 'start' or 'help'."
        assert cls.template_slug,  f"{cls.__name__} provide a slug as doc string says."
        return super().__new__(cls)

    @contract
    def __init__(self, message: MessageParser, client: TelegramClient, bot: Bot):
        self.message = message
        self.client = client
        self.bot = bot
        self.template_handler = self.template_class()
        self.permission_classes = self.permission_classes or list()
        self.user = None

    def get_permissions(self):
        return [
            cls(self.bot, self.message['chat'].chat_id, self.message['text'].command)
            for cls in self.permission_classes
        ]

    def has_permissions(self):
        return all([perm.has_permissions() for perm in self.get_permissions()])

    def render_template(self, template_slug, context_dict=None):
        return self.template_handler.render_from_template(template_slug, context_dict)

    @property
    def chat_id(self):
        return self.message['chat'].chat_id

    def set_user(self):
        """Sometimes there isn't user or user can be provided only after a command is run."""
        try:
            self.user = TelegramUser.objects.get(chat_id=self.chat_id).user
        except TelegramUser.DoesNotExist:
            pass

    def _command_processing(self):
        raise NotImplementedError(f"{self.__class__.__name__} command")

    def run(self, write_log=True):
        """
        Logging needs for user commands and analyzing user behavior
        but for mass newsletters no needs it.
        TODO Add the separating log type for automatic notification.
        """
        with transaction.atomic():
            result = self._command_processing()
            self.set_user()
            if write_log:
                TelegramCommandLog.objects.create(
                    user=self.user, command=self.name, bot=self.bot
                )
            return result


class Start(Command):
    name = "start"
    template_slug = None

    @staticmethod
    def get_token(source_text):
        """A start command looks like `/start token`"""
        with suppress(Token.DoesNotExist, IndexError):
            return Token.objects.get(key=source_text.split(" ")[1])

    def _create_objects(self, token):
        TelegramUser.objects.get_or_create(
            user=token.user,
            chat_id=self.chat_id,
            username=self.message['chat'].username,
            bot=token.bot,
        )
        token.delete()
        return True

    def _send_welcome_message(self, chat_id):
        message = self.render_template(self.template_slug)
        return self.client.send_message(chat_id=chat_id, prepared_message=message)

    def _command_processing(self):
        token = self.get_token(self.message['text'].command)
        created = self._create_objects(token) if token else False
        created and self._send_welcome_message(self.chat_id)
        return created


class Help(Command):
    name = 'help'
    template_slug = None

    def _command_processing(self):
        message = self.render_template(self.template_slug)
        return self.client.send_message(chat_id=self.chat_id, prepared_message=message)
