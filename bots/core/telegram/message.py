import copy

from .exceptions import UnknownField


class MessageObject:
    """
    Telegram requests has a good structure for parsing. Every objects has a name as key.
    Use it for connecting parameters from Telegram request with MessageObject.
    """
    key = None

    def __new__(cls, *args, **kwargs):
        assert cls.key, f"{cls.__name__} provide key for define a command."
        return super().__new__(cls)

    def __init__(self, json_data):
        self._data = copy.deepcopy(json_data)

    def __hash__(self):
        return self.key

    @property
    def data(self):
        return self._data


class Chat(MessageObject):
    key = 'chat'

    @property
    def chat_id(self):
        return self.data['id']

    @property
    def username(self):
        """Some times Telegram API does not provide username. Maybe its personal settings."""
        return self.data['username'] if 'username' in self.data else ""


class Text(MessageObject):
    key = 'text'

    @property
    def is_command(self):
        return self.data.startswith("/")

    @property
    def command(self):
        return self.data[1:]

    @property
    def clean_command(self):
        return self.data.split()[0][1:]


class MessageParser:
    object_classes = None

    def __new__(cls, *args, **kwargs):
        assert cls.object_classes, f"{cls.__name__} does not have object classes."
        return super().__new__(cls)

    def __init__(self, json_message: dict):
        self.message = json_message
        self._available_fields = {
            f.key: f for f in self.object_classes
        }

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.message.keys()}>"

    def __getitem__(self, item):
        return self.get_field(item)

    def __contains__(self, item):
        return self.is_field(item)

    @property
    def available(self):
        return self._available_fields

    def is_field(self, key):
        return key in self.message

    def get_field(self, key):
        if key not in self:
            raise ValueError(
                f"the message does not have a object `{key}`, keys: {self.message.keys()}"
            )

        if key not in self.available:
            raise UnknownField(
                f"{self.__class__.__name__} does not have a object `{key}`. "
                f"Available fields: {self.available.keys()}."
            )
        field_data = self.message[key]
        return self.available[key](field_data)


class Message(MessageParser):
    object_classes = (Chat, Text)
