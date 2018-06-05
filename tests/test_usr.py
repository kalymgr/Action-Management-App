import pytest
from flask import g

@pytest.mark.parametrize('path', (
    '/users/',
    '/users/add',
    '/users/1',
    '/users/1/view',
    '/users/1/edit',
    '/users/1/delete',
    '/users/1/changepassword',
    '/users/categories',
    '/users/categories/add',
    '/users/categories/1/edit',
    '/users/categories/1/delete',
))
def test_user_loggedin(client, path):
    """
    Test function that checks that if a user is not logged in,
    he will be redirected to the login page (auth/login)
    :param client:
    :param path:
    :return:
    """
    responseHeaders = client.get(path).headers
    for h in responseHeaders:
        if h[0] == 'Location':
            assert b"/auth/login" in h[1]


def test_userList(client, auth):

    # case the user is not logged in
    response = client.get('/users/')
    assert b"Redirecting" in response.data

    # case the user logs in
    auth.login()  # login as test user

    # case we get a normal result
    response = client.get('/users/')
    assert response.status_code == 200  # the response is ok
    assert b"test user" in response.data  # test user exists in page
    with client:
        client.get('/users/')  # necessary to get the g.user variable
        assert g.user.username == 'test'


