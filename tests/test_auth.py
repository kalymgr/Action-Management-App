import pytest
from flask import g, session, current_app
from actionmanagementapp.users.model import User
from actionmanagementapp.utilities import database_setup


def test_register(client, app):
    # assert that you can get the registration page
    pass

    assert client.get('/auth/register').status_code == 200

    # get a response using the POST method on registration page

    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a', 'name': 'aName'},
    )

    assert True


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required.'),
        ('a', '', b'Password is required.'),
        ('test', 'test', b'The user already exists'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, 'name': ''}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login
    assert response.headers['Location'] == 'http://localhost/users'

