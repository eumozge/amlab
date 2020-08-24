from requests.auth import AuthBase, HTTPBasicAuth

__all__ = (
    'HTTPBasicAuth',
    'BearerToken',
    'Anonymous',
    'AuthBase'
)


class BearerToken(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer ' + self.token
        return request


class Anonymous(AuthBase):
    def __call__(self, request):
        return request
