import os
import tempfile

import pytest
from flask import Flask
from flask.testing import FlaskClient

from {{cookiecutter.package_name}} import create_app
from {{cookiecutter.package_name}}.ext import db
from {{cookiecutter.package_name}}.users.cli import create_user
from . import ADMIN_DATA, USER_DATA


@pytest.fixture
def app() -> Flask:
    temp_dir = tempfile.TemporaryDirectory()
    tmp_dirname = temp_dir.name

    os.chdir(tmp_dirname)

    app = create_app('testing')
    with app.app_context():
        db.create_all()

        create_user(USER_DATA['username'],
                    USER_DATA['email'],
                    USER_DATA['password'], is_admin=False)
        create_user(ADMIN_DATA['username'],
                    ADMIN_DATA['email'],
                    ADMIN_DATA['password'], is_admin=True)

        yield app
    temp_dir.cleanup()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    client = app.test_client(use_cookies=True)
    yield client


@pytest.fixture
def client_no_cookie(app: Flask) -> FlaskClient:
    client = app.test_client(use_cookies=False)
    return client


@pytest.fixture
def api_client(client: FlaskClient):
    from .api_client import ApiClient

    api_client = ApiClient.login_by_data(client, USER_DATA)

    app: Flask = api_client.client.application

    api_client.init_app(app)
    yield api_client


@pytest.fixture
def socket_client(api_client):
    from {{cookiecutter.package_name}}.ext import socket

    app: Flask = api_client.client.application

    test_client = socket.test_client(app, auth={'X-API-Key': api_client.token})

    return test_client


@pytest.fixture
def api_anonymous_client(client: FlaskClient):
    from .api_client import ApiClient

    api_client = ApiClient(client)

    app: Flask = api_client.client.application
    with app.app_context():
        yield api_client


@pytest.fixture
def api_admin_client(client: FlaskClient):
    from .api_client import ApiClient

    api_client = ApiClient.login_by_data(client, ADMIN_DATA)

    app: Flask = api_client.client.application
    with app.app_context():
        yield api_client

