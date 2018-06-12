import pytest
from flask import g, session, current_app
from actionmanagementapp.users.users_models import User
from actionmanagementapp.utilities import database_setup


def test_register(client, app):
    # assert that you can get the registration page
    pass

    assert client.get('/auth/register').status_code == 200

    # get a response using the POST method on registration page

    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a', 'name': 'aName'},
    )


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
    response = auth.login()

    with client:
        client.get('/users')
        assert session['user_id'] == 1
        assert g.user.username == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('onoma_xristi', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session