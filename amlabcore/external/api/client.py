import copy
import json
import logging

import requests
from contracts import contract
from django.utils.functional import cached_property

from amlab.logs.settings import EXTERNAL
from .auth import AuthBase

__all__ = (
    'AbstractAPILog',
    'DefaultAPILog',
    'DefaultAPIClient',
)


class AbstractAPILog:
    def write(self, response):
        raise NotImplementedError()


class DefaultAPILog(AbstractAPILog):
    logger_name = EXTERNAL

    def __init__(self, api_name):
        self.api_name = api_name

    def is_success_request(self, response):
        return response.ok

    def get_digital_log_level(self, response):
        return logging.INFO if self.is_success_request(response) else logging.ERROR

    def get_default_log_params(self, response):
        return {
            'api': self.api_name,
            'status': response.status_code,
        }

    @classmethod
    def get_request_log_params(cls, response):
        body = response.body
        return {
            'url': response.url,
            'method': response.method,
            'body': body.decode('UTF-8') if hasattr(body, 'decode') else dict()
        }

    @classmethod
    def get_response_log_params(cls, response):
        """
        Some times server return not json decoded response, for example:
        Google Ecommerce can return file as pixel."""
        try:
            return response.json()
        except json.JSONDecodeError:
            return dict({
                'error': 'response is not json decoded.'
            })

    def get_log_message(self, response):
        params = self.get_default_log_params(response)
        params['request'] = self.get_request_log_params(response.request)
        params['response'] = self.get_response_log_params(response)
        return params

    def check_logger(self):
        """
        Check logger no in __new__ or __init__ methods because
        custom logger from django settings can be not loaded.
        """
        available_loggers = logging.root.manager.loggerDict.keys()
        if self.logger_name not in available_loggers:
            raise ValueError(
                f"logger `{self.logger_name}` is not registered, available `{available_loggers}`."
            )

    @cached_property
    def logger(self):
        self.check_logger()
        return logging.getLogger(self.logger_name)

    def write(self, response, digital_level=None):
        level = logging.getLevelName(digital_level or self.get_digital_log_level(response))
        message = self.get_log_message(response)
        getattr(self.logger, level.lower())(message)


class DefaultAPIClient:
    @contract
    def __init__(self,
                 auth: AuthBase,
                 api_url: str,
                 log: AbstractAPILog = None,
                 headers=None,
                 is_default_logging=True):
        self.auth = auth
        self.url = api_url
        self.headers = headers or dict()
        self.log = log or DefaultAPILog('default')
        self.is_default_logging = is_default_logging

    def call(self, method, endpoint, write_log=False, **kwargs):
        write_log = write_log or self.is_default_logging
        headers = copy.deepcopy(self.headers)
        headers.update(kwargs.pop('headers', dict()))
        response = requests.request(
            method,
            f"{self.url}{endpoint}",
            auth=self.auth,
            headers=headers,
            **kwargs
        )
        setattr(self, '_last_request', response)
        write_log and self.write_log(response)
        return response

    @property
    def last_request(self):
        return getattr(self, '_last_request', None)

    @staticmethod
    def is_success_request(response):
        return response.ok

    def write_log(self, response):
        self.log.write(response)
