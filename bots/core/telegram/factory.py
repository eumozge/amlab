from .amlab.handlers import AmlabTelegramHandler
from .exceptions import UnknownHandler

HANDLERS = (AmlabTelegramHandler,)


def get_handler_by_token(key):
    for cls in HANDLERS:
        if cls.client.token == key:
            return cls()
    raise UnknownHandler(f"undefined token: ...{key[-8:]}")


def get_handler_by_bot(name):
    name = name.lower()
    for cls in HANDLERS:
        if cls.client.name.lower() == name:
            return cls()
    raise UnknownHandler(f"undefined name: {name}")
