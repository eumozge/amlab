import pytest

from .. import amlab, get_handler_by_token, get_handler_by_bot


class TestFactory:
    @pytest.mark.parametrize('token,reference_class', [
        (amlab.AMLAB_TELEGRAM_BOT_TOKEN, amlab.AmlabTelegramHandler),
    ], ids=['amlab-telegram'])
    def test_get_handler_by_token(self, token, reference_class):
        handler = get_handler_by_token(token)
        assert handler.__class__ == reference_class

    @pytest.mark.parametrize('name,reference_class', [
        (amlab.AMLAB_TELEGRAM_BOT_NAME, amlab.AmlabTelegramHandler),
    ], ids=['amlab-telegram'])
    def test_get_handler_by_name(self, name, reference_class):
        handler = get_handler_by_bot(name)
        assert handler.__class__ == reference_class
