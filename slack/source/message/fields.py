from contracts import contract


class Field:
    """The idea is saving field attrs in the same format as format for requests to Slack API."""

    def __init__(self):
        self._params = self._get_default_params()
        self.check_params(self._params)

    def __len__(self):
        return len(self.params)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.params}>"

    def __str__(self):
        return repr(self)

    def __getitem__(self, item):
        return self.params[item]

    def __contains__(self, item: str):
        return item in self._params

    @classmethod
    def check_params(cls, params):
        assert type(params) in (dict, list), (
            "field structure can look just as dict or list, not {type(params)}."
            "At the moment that types cover all Slack messages."
        )

    @property
    def params(self):
        return self._params

    def _get_default_params(self):
        raise NotImplementedError()

    def _parse_data(self, item):
        """As a field can includes the other fields it can be unpacked with recursion."""
        if hasattr(item, 'to_representative'):
            return self._parse_data(item.to_representative())
        if isinstance(item, list):
            return [
                self._parse_data(i) for i in item
            ]
        if isinstance(item, dict):
            return {
                k: self._parse_data(i) for k, i in item.items()
            }
        return item

    def to_representative(self):
        return self._parse_data(self._params)


class DictField(Field):
    def __setitem__(self, key, value):
        self.params[key] = value

    def _get_default_params(self):
        return dict()

    @contract
    def set_value(self, key: str, value):
        self[key] = value
        return self


class ListField(Field):
    def _get_default_params(self):
        return list()

    @contract
    def append(self, field: Field):
        self.params.append(field)
        return self


class MessageField(DictField):
    """The one required arguments for any `main` message is `channel`."""
    channel_prefixes = ('@', "#")

    @contract
    def __init__(self, channel: str):
        super().__init__()
        self.check_channel(channel)
        self.set_value('channel', channel)

    @classmethod
    def check_channel(cls, channel):
        """
        TODO At the moment there are not a cases with channel as ID and not a simple name.
        TODO But maybe add supporting it and use only ID? No cases, but maybe somebody rename it?
        """
        if not len(channel) > 1:
            raise ValueError("unreal channel `{channel}`.")
        if not sum([channel.startswith(p) for p in cls.channel_prefixes]) == 1:
            raise ValueError(
                f"channel name must start with `{cls.channel_prefixes}`, `{channel}`."
            )

    @property
    def channel(self):
        return self.params['channel']
