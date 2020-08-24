import os
import warnings

from ..tests.settings import TEST_BOT_TOKEN

AMLAB_TELEGRAM_BOT_NAME = "AmlabBot"
AMLAB_TELEGRAM_BOT_TOKEN = os.getenv('AMLAB_TELEGRAM_BOT_TOKEN', TEST_BOT_TOKEN)
AMLAB_WELCOME_MESSAGE_SLUG = "amlab-welcome"
AMLAB_HELP_MESSAGE_SLUG = "amlab-help"
AMLAB_CHALLENGE_MESSAGE_SLUG = "amlab-challenge"


if AMLAB_TELEGRAM_BOT_TOKEN == TEST_BOT_TOKEN:
    warnings.warn(
        "The AMLAB_TELEGRAM_BOT_TOKEN is not provided. AmlabBot functionality doesnt work."
        "Define a token via environment variable 'AMLAB_TELEGRAM_BOT_TOKEN'."
    )
