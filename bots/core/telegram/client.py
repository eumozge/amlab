from amlabcore.external import DefaultAPIClient, Anonymous, DefaultAPILog
from bots.models import Bot
from .settings import DEFAULT_PARSE_MODE


class TelegramClient(DefaultAPIClient):
    def __init__(self, name, token, log):
        super().__init__(auth=Anonymous(), api_url="https://api.telegram.org/", log=log)
        self.name = name
        self.token = token

    def get_bot(self):
        return Bot.objects.get(slug__iexact=self.name)

    @staticmethod
    def get_endpoint(source_endpoint, bot_auth_token):
        return f"bot{bot_auth_token}/{source_endpoint}"

    def call(self, method, endpoint, write_log=False, **kwargs):
        endpoint = self.get_endpoint(endpoint, self.token)
        return super().call(method, endpoint, write_log=False, **kwargs)

    def send_message(self, chat_id, prepared_message, parse_mode=DEFAULT_PARSE_MODE):
        data = {
            'chat_id': chat_id,
            'text': prepared_message,
            'parse_mode': parse_mode
        }
        return self.call('post', 'sendMessage', data=data)


class TelegramLog(DefaultAPILog):
    pass
