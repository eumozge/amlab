from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from amlabcore.db.models import CreatedAt

User = get_user_model()


class TelegramUser(CreatedAt):
    bot = models.ForeignKey(
        'bots.Bot', on_delete=models.PROTECT, verbose_name=_('bot'),
        blank=True, null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('user'),
    )
    chat_id = models.PositiveIntegerField(verbose_name=_('chat id'))
    username = models.CharField(max_length=128, verbose_name=_('username'), blank=True)

    class Meta:
        verbose_name = _('telegram user')
        verbose_name_plural = _('telegram users')
        db_table = 'bots_telegram_user'


class TelegramCommandLog(CreatedAt):
    bot = models.ForeignKey(
        'bots.Bot', on_delete=models.PROTECT, verbose_name=_('bot'),
        blank=True, null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('user'),
        blank=True, null=True
    )
    command = models.CharField(max_length=256, verbose_name=_('command'))

    class Meta:
        verbose_name = _('command log')
        verbose_name_plural = _('command logs')
        db_table = 'bots_telegram_command_logs'

    def __repr__(self):
        user = {self.user.email if self.user else 'anonymous'}
        return f"<{self.__class__.__name__} (command={self.command}, user={user})>"

    def __str__(self):
        return repr(self)
