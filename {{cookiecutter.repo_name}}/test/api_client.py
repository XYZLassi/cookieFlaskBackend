from __future__ import annotations

__all__ = ['ApiClient', 'login', 'login_by_data', 'assert_success']

import json
from typing import TypeVar

from flask import Response
from flask.testing import FlaskClient

T = TypeVar('T')


class ApiClient:
    class ErrorStatusCode(Exception):
        def __init__(self, status, error):
            self.status = status
            self.error = error

    def __init__(self, client: FlaskClient, token: str = None, user=None):

        self.token = token
        self.client = client

        self.user = user

        self.app = None

    def init_app(self, app):
        self.app = app

    def post(self, url, data=None, content_type='application/json') -> dict:
        data = data or dict()
        headers = dict()

        if self.token:
            headers['X-API-Key'] = self.token

        request_data = data
        if hasattr(data, 'to_dict'):
            request_data = data.to_dict()

        kwargs = {
            'headers': headers,
            'content_type': content_type,
        }

        if content_type == 'application/json':
            kwargs['json'] = request_data
        else:
            kwargs['data'] = request_data

        # noinspection PyTypeChecker
        response: Response = self.client.post(url, **kwargs)

        data = json.loads(response.data)

        if response.status_code != 200:
            error = data['error']
            raise ApiClient.ErrorStatusCode(response.status_code, error)

        return data

    def patch(self, url, data) -> dict:
        headers = dict()

        if self.token:
            headers['X-API-Key'] = self.token

        request_data = data
        if hasattr(data, 'to_dict'):
            request_data = data.to_dict()

        # noinspection PyTypeChecker
        response: Response = self.client.patch(url, headers=headers, json=request_data)

        data = json.loads(response.data)

        if response.status_code != 200:
            error = data['error']
            raise ApiClient.ErrorStatusCode(response.status_code, error)

        return data

    def delete(self, url, data=None, ):
        data = data or dict()
        headers = dict()

        if self.token:
            headers['X-API-Key'] = self.token

        request_data = data
        if hasattr(data, 'to_dict'):
            request_data = data.to_dict()

        # noinspection PyTypeChecker
        response: Response = self.client.delete(url, headers=headers, json=request_data)

        if response.status_code != 200:
            data = json.loads(response.data)
            error = data['error']
            raise ApiClient.ErrorStatusCode(response.status_code, error)

        if response.data:
            return json.loads(response.data)

    def get(self, url, params: dict = None) -> dict:
        headers = dict()

        if self.token:
            headers['X-API-Key'] = self.token

        # if params:
        #    url += '?' + '&'.join([f'{k}={v}' for k, v in params.items()])

        # noinspection PyTypeChecker
        response: Response = self.client.get(url, headers=headers, query_string=params)

        data = json.loads(response.data)

        if response.status_code != 200:
            error = data['error']
            raise ApiClient.ErrorStatusCode(response.status_code, error)

        return data

    @staticmethod
    def login(client: FlaskClient, username: str, password: str) -> ApiClient:
        login_response: dict = login(client, username, password)
        return ApiClient(client, login_response['token'], user=login_response['user'])

    @staticmethod
    def login_by_data(client: FlaskClient, data: dict) -> ApiClient:
        return ApiClient.login(client, data['username'], data['password'])


def assert_success(response):
    assert response.success, response.error
    assert not response.error


def login(client: FlaskClient, username: str, password: str) -> dict:
    request = {'username': username, 'password': password}
    response: Response = client.post('/api/v2/login', json=request)

    assert response.content_type == 'application/json'

    data = json.loads(response.data)

    return data


def login_by_data(client: FlaskClient, data: dict) -> dict:
    return login(client, data['username'], data['password'])
