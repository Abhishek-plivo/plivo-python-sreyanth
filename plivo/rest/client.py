# -*- coding: utf-8 -*-
"""
Core client, used for all API requests.
"""

import os
import platform
from collections import namedtuple

import requests

from plivo.base import ResponseObject
from plivo.exceptions import (AuthenticationError, InvalidRequestError,
                              PlivoRestError, PlivoServerError,
                              ResourceNotFoundError, ValidationError)
from plivo.resources import (Accounts, Applications, Calls, Conferences,
                             Endpoints, Messages, Numbers, Pricings,
                             Recordings, Subaccounts)
from plivo.resources.live_calls import LiveCalls
from plivo.utils import is_valid_mainaccount, is_valid_subaccount
from plivo.version import __version__

AuthenticationCredentials = namedtuple('AuthenticationCredentials',
                                       'auth_id auth_token')

PLIVO_API = 'https://api.plivo.com'
PLIVO_API_BASE_URI = '/'.join([PLIVO_API, 'v1/Account'])


def get_user_agent():
    return 'plivo-python/%s (Python: %s)' % (__version__,
                                             platform.python_version())


def fetch_credentials(auth_id, auth_token):
    """Fetches the right credentials either from params or from environment"""

    if not (auth_id and auth_token):
        try:
            auth_id = os.environ['PLIVO_AUTH_ID']
            auth_token = os.environ['PLIVO_AUTH_TOKEN']
        except KeyError:
            raise AuthenticationError('The Plivo Python SDK '
                                      'could not find your auth credentials.')

    if not (is_valid_mainaccount(auth_id) or is_valid_subaccount(auth_id)):
        raise AuthenticationError('Invalid auth_id supplied: %s' % auth_id)

    return AuthenticationCredentials(auth_id=auth_id, auth_token=auth_token)


class Client(object):
    def __init__(self, auth_id=None, auth_token=None):
        """
        The Plivo API client.

        Deals with all the API requests to be made. To configure a proxy,
        set it on the Requests session. To configure a timeout, you can mount a
        custom transport adapter (see
        https://github.com/requests/requests/issues/2011#issuecomment-64440818)
        """

        self.base_uri = PLIVO_API_BASE_URI
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': get_user_agent(),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })

        self.session.auth = fetch_credentials(auth_id, auth_token)

        self.account = Accounts(self)
        self.subaccounts = Subaccounts(self)
        self.applications = Applications(self)
        self.calls = Calls(self)
        self.live_calls = LiveCalls(self)
        self.conferences = Conferences(self)
        self.endpoints = Endpoints(self)
        self.messages = Messages(self)
        self.numbers = Numbers(self)
        self.pricing = Pricings(self)
        self.recordings = Recordings(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def process_response(self,
                         method,
                         response,
                         response_type=None,
                         objects_type=None):
        """Processes the API response based on the status codes and method used
        to access the API
        """
        try:
            response_json = response.json(
                object_hook=
                lambda x: ResponseObject(x) if isinstance(x, dict) else x)
            if response_type:
                r = response_type(self, response_json.__dict__)
                response_json = r

            if 'objects' in response_json and objects_type:
                response_json.objects = [
                    objects_type(self, obj.__dict__)
                    for obj in response_json.objects
                ]
        except ValueError:
            response_json = None

        if response.status_code == 400:
            if response_json and 'error' in response_json:
                raise ValidationError(response_json.error)
            raise ValidationError(
                'A parameter is missing or is invalid while accessing resource '
                'at: {url}'.format(url=response.url))

        if response.status_code == 401:
            if response_json and 'error' in response_json:
                raise AuthenticationError(response_json.error)
            raise AuthenticationError(
                'Failed to authenticate while accessing resource at: '
                '{url}'.format(url=response.url))

        if response.status_code == 404:
            if response_json and 'error' in response_json:
                raise ResourceNotFoundError(response_json.error)
            raise ResourceNotFoundError(
                'Resource not found at: {url}'.format(url=response.url))

        if response.status_code == 405:
            if response_json and 'error' in response_json:
                raise InvalidRequestError(response_json.error)
            raise InvalidRequestError(
                'HTTP method "{method}" not allowed to access resource at: '
                '{url}'.format(method=method, url=response.url))

        if response.status_code == 500:
            if response_json and 'error' in response_json:
                raise PlivoServerError(response_json.error)
            raise PlivoServerError(
                'A server error occurred while accessing resource at: '
                '{url}'.format(url=response.url))

        if method == 'DELETE':
            if response.status_code != 204:
                raise PlivoRestError('Resource at {url} could not be '
                                     'deleted'.format(url=response.url))

        elif response.status_code not in [200, 201, 202]:
            raise PlivoRestError(
                'Received status code {status_code} for the HTTP method '
                '"{method}"'.format(
                    status_code=response.status_code, method=method))

        return response_json

    def create_request(self, method, path=None, data=None):
        path = path or []
        req = requests.Request(
            method, '/'.join([self.base_uri, self.session.auth[0]] + list(
                [str(p) for p in path])) + '/', **({
                    'params': data
                } if method == 'GET' else {
                    'json': data
                }))
        return self.session.prepare_request(req)

    def send_request(self, request, **kwargs):
        return self.session.send(request, **kwargs)

    def request(self,
                method,
                path=None,
                data=None,
                response_type=None,
                objects_type=None,
                **kwargs):
        req = self.create_request(method, path, data)
        res = self.send_request(req, **kwargs)
        return self.process_response(method, res, response_type, objects_type)
