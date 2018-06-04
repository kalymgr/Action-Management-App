"""
Contains setup functions called fixtures that each test will use
"""
import pytest
from actionmanagementapp import create_app
from actionmanagementapp.utilities.database_setup import getTestingDatabaseSession


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DBSESSION': getTestingDatabaseSession()
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()