from .settings import AMLAB_TELEGRAM_BOT_NAME, AMLAB_TELEGRAM_BOT_TOKEN
from ..client import TelegramClient, TelegramLog

AmlabTelegramClient = TelegramClient(
    name=AMLAB_TELEGRAM_BOT_NAME,
    token=AMLAB_TELEGRAM_BOT_TOKEN,
    log=TelegramLog("amlab_telegram")
)
