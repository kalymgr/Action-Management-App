"""
Contains setup functions called fixtures that each test will use
"""
import pytest
from actionmanagementapp import create_app
from actionmanagementapp.utilities.DatabaseSetup import getTestingDatabaseSession


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,  # set TESTING to True
        'DBSESSION': getTestingDatabaseSession()  # use the test database
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    """
    Class for logging in (will be used in views)
    """
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)