from contracts import contract

from . import mixins
from .fields import DictField, Field, ListField, MessageField


class TextField(mixins.TitleDictFieldMixin,
                DictField):

    def __init__(self, value: str):
        super().__init__()
        self.set_value('value', value)

    def _get_default_params(self):
        return {
            'title': "",
            'value': "",
            'short': True
        }

    def set_short(self, value=True):
        return self.set_value('short', value)


class AttachmentField(mixins.TitleDictFieldMixin,
                      mixins.ColorDictFieldMixin,
                      mixins.TextDictFieldMixin,
                      mixins.AuthorDictFieldMixin,
                      DictField):

    @property
    def fields(self):
        return self.params.setdefault("fields", ListField())

    def append(self, field: Field):
        self.fields.append(field)
        return self


class Message(mixins.TitleDictFieldMixin,
              mixins.ColorDictFieldMixin,
              mixins.TextDictFieldMixin,
              MessageField):

    @property
    def attachments(self):
        return self.params.setdefault("attachments", ListField())

    @contract(field=Field)
    def add_attachment(self, field):
        self.attachments.append(field)
        return self
