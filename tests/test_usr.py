import pytest
from flask import g, current_app

from actionmanagementapp.users.model import User


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


def test_userDetails(client, auth):
    auth.login()  # test user logs in

    # test that the user is valid and the view page is fetched with the user's info
    userId = 1
    response = client.get('/users/%s/view'%userId)
    assert response.status_code == 200
    assert "test user" in response.data

    # test that if the user id in the URL is not valid, the response will be 404
    response2 = client.get('/users/1928336/view')
    assert response2.status_code == 404

    # test that the global g.user object (logged in user) exists
    with client:
        response = client.get('/users/%s/view' % userId)
        assert g.user.id == 1  # the logged in user is test user (with user id equal to 1)


def test_addUser(client, auth):
    # test that the add user page opens properly
    # test that the logged in user has id 1 (g.user)
    with client:
        auth.login()
        response = client.get('/users/add')
        assert response.status_code == 200
        assert g.user.id == 1

    #test POST method and successful storing of user data in the database


    # get the user from the database
    with client:
        userData = {
            'name': 'Michalis',
            'username': 'kalymgr',
            'password': 'kalymgr',
            'password2': 'kalymgr',
            'department': 'IT Department',
            'phone': '22433XXXXX',
            'mobile': '6945XXXXX',
            'email': 'mtsougranis@gmail.com',
            'enabled': True,
            'usercategory': 1
        }
        auth.login()
        response = client.post('/users/add', userData)
        dbSession = current_app.config['DBSESSION']
        newUser = dbSession.query(User).filter(User.username == 'kalymgr').first()
        assert userData['name'] == newUser.name


