from django.utils.translation import gettext_lazy as _

from amlabcore.db.models import Name, Slug


class Bot(Name, Slug):
    class Meta:
        verbose_name = _('bot')
        verbose_name_plural = _('bots')
        db_table = 'bots_bot'

    def __repr__(self):
        return f"<{self.__class__.__name__} (slug={self.slug})>"

    def __str__(self):
        return self.slug
