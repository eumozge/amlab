from .settings import TEST_VALUE

__all__ = (
    'get_text_field_reference'
)


def get_text_field_reference(value=TEST_VALUE, short=True, title=None, **kwargs):
    params = {
        'value': value,
        'short': short,
        'title': title or "",
    }
    params.update(kwargs)
    return params
