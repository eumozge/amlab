import pytest

from bots.tests.fixtures import *
from .settings import TEST_MESSAGE_UNKNOWN_FIELD
from ..exceptions import UnknownField
from ..message import Chat, Text


class TestChat:
    @pytest.mark.parametrize('attr_name,reference_key', [
        ('chat_id', 'id'),
        ('username', 'username'),
    ], ids=['id', 'username'])
    def test_parse(self, clean_json_message, attr_name, reference_key):
        chat = Chat(clean_json_message['chat'])
        assert getattr(chat, attr_name) == clean_json_message['chat'][reference_key]


class TestText:
    def test_parse(self, clean_json_message):
        text = Text(clean_json_message['text'])
        assert text.is_command and text.command == clean_json_message['text'][1:]


class TestParser:
    @pytest.mark.parametrize('field_key,reference_class', [
        ('chat', Chat),
        ('text', Text),
    ])
    def test_fields(self, clean_json_message, object_message, field_key, reference_class):
        field = object_message.get_field(field_key)
        assert field_key in object_message
        assert field.__class__ == object_message[field_key].__class__ == reference_class

    def test_unknown_fields(self, clean_json_message, object_message):
        with pytest.raises(UnknownField):
            object_message.get_field(TEST_MESSAGE_UNKNOWN_FIELD)
