import binascii
import os

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from amlabcore.db.models import CreatedAt

User = get_user_model()


class Token(CreatedAt):
    bot = models.ForeignKey(
        'bots.Bot', on_delete=models.CASCADE, verbose_name=_('bot'),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('user'),
    )
    key = models.CharField(max_length=32, verbose_name=_('key'))

    class Meta:
        verbose_name = _('token')
        verbose_name_plural = _('tokens')
        db_table = 'bots_token'

    def __repr__(self):
        return f"<{self.__class__.__name__} (user={self.user}, bot={self.bot}, key={self.key})>"

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(16)).decode()
