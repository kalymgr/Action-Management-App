"""
Contains setup functions called fixtures that each test will use
"""
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from actionmanagementapp import create_app
from actionmanagementapp.utilities.database_init import createEngine, Base


def getTestDbSession():
    """
    Used only for testing purposes
    :return: a test db session
    """
    engine = createEngine('root', '', 'test_actionapplicationdb', 'localhost', 'utf8')
    dbSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    import actionmanagementapp.users.users_models
    import actionmanagementapp.org.org_models
    import actionmanagementapp.log.log_models
    Base.metadata.create_all(bind=engine)

    # insert default organizational data
    actionmanagementapp.org.org_models.insertDefaultOrgData(dbSession)
    # insert default user data
    actionmanagementapp.users.users_models.insertDefaultUserData(dbSession)

    return dbSession


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,  # set TESTING to True
        'DBSESSION': getTestDbSession()  # use the test database
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

    def login(self, username='kalymgr', password='kalymgr'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)