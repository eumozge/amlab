import pytest

from .settings import TEST_CHANNEL, TEST_VALUE, TEST_VALUE_2, TEST_VALUE_3
from .utils import get_text_field_reference
from ..message import AttachmentField, DictField, ListField, Message, TextField, get_dict_message


@pytest.fixture
def field_dict():
    return DictField()


@pytest.fixture
def field_list():
    return ListField()


@pytest.fixture
def field_attachment():
    return AttachmentField()


@pytest.fixture
def field_text():
    return TextField(TEST_VALUE)


@pytest.fixture
def message():
    return Message(TEST_CHANNEL)


class TestDictField:
    def test_set_additional_params(self, field_dict):
        field_dict.set_value('key', 'value')
        assert field_dict.params['key'] == 'value'

    def test_set_value(self, field_dict, field_list):
        field_dict.set_value('key', field_list)
        assert field_dict.params.get('key') == field_list

    def test_to_representative(self, field_dict, field_list):
        field_dict.set_value('key', field_list)
        assert field_dict.to_representative() == {'key': []}


class TestListField:
    def test_append(self, field_dict, field_list):
        field_list.append(field_dict)
        assert (len(field_list), field_list.params[0]) == (1, field_dict)

    def test_to_representative(self, field_dict, field_list):
        field_list.append(field_dict)
        assert field_list.to_representative() == [dict()]


class TestTextField:
    def test_build(self, field_text):
        reference = get_text_field_reference(title=TEST_VALUE, short=False, key='value')
        field_text\
            .set_title(TEST_VALUE)\
            .set_short(False)\
            .set_value('key', 'value')
        assert field_text.to_representative() == reference


class TestAttachmentField:
    def test_append(self, field_attachment, field_text):
        field_attachment.append(field_text)
        assert field_attachment.params['fields'][0] == field_text

    def test_build(self, field_attachment, field_text):
        reference = {
            'key': 'value',
            'fields': [
                get_text_field_reference()
            ]
        }
        field_attachment.set_value('key', 'value')
        field_attachment.append(field_text)
        assert field_attachment.to_representative() == reference


class TestMessage:
    def test_init(self, message):
        assert message.channel == TEST_CHANNEL

    @pytest.mark.parametrize('channel', [
        "AAA", "000", "?00", "0",
    ])
    def test_channel_invalid(self, channel):
        with pytest.raises(ValueError):
            Message(channel)

    @pytest.mark.parametrize('channel', [
        "@00", "#00",
    ])
    def test_channel_valid(self, channel):
        Message(channel)

    def test_attachments(self, message, field_dict):
        message.add_attachment(field_dict)
        assert message.attachments[0] == field_dict

    def test_build(self, message):
        field_attachment_1 = AttachmentField()\
            .set_title(TEST_VALUE)\
            .set_color_warning()\
            .append(TextField(TEST_VALUE_2).set_short(False))\
            .append(TextField(TEST_VALUE_3).set_short(True))

        field_attachment_2 = AttachmentField()\
            .set_text(TEST_VALUE)\
            .set_pretext(TEST_VALUE_2)

        message\
            .add_attachment(field_attachment_1)\
            .add_attachment(field_attachment_2)

        reference = {
            'channel': TEST_CHANNEL,
            'attachments': [
                field_attachment_1.to_representative(),
                field_attachment_2.to_representative()
            ]
        }
        assert message.to_representative() == reference


class TestUtils:
    def test_get_text_message_from_dict(self):
        source = {
            'key1': TEST_VALUE,
            'key2': TEST_VALUE_2
        }
        message = get_dict_message(TEST_CHANNEL, source)
        assert len(message.attachments[0]['fields']) == 2
        assert isinstance(message.attachments[0]['fields'][0], TextField)
