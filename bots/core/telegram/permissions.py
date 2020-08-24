from typing import Union

from contracts import contract

from bots.core.templates import DjangoTemplate
from bots.models import Bot, TelegramUser
from .exceptions import PermissionException


class Permission:
    template_slug = None
    template_class = DjangoTemplate

    @contract
    def __init__(self, bot: Bot, chat_id, command=None):
        self.bot = bot
        self.chat_id = chat_id
        self.command = command

    def has_permission(self):
        raise NotImplementedError(f"{self.__class__.__name__}")

    def get_message(self):
        assert self.template_slug, f"{self.__class__.__name__} define a `template_slug` " \
                                   f"for using default error templates."
        return DjangoTemplate().render_from_template(self.template_slug)

    def raise_exception(self, message):
        raise PermissionException(message)


class IsAuthenticated(Permission):
    def has_permission(self):
        return TelegramUser.objects.filter(bot=self.bot, chat_id=self.chat_id).exists()
