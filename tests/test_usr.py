import pytest
from flask import g, current_app, url_for

from actionmanagementapp.users.model import User
from tests import helperFunctions

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
    assert b"/auth/login" in helperFunctions.getHeaderContent(responseHeaders, 'Location')
    """
    responseHeaders = client.get(path).headers
    for h in responseHeaders:
        if h[0] == 'Location':
            assert b"/auth/login" in h[1]
"""


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

    # test POST method and successful storing of user data in the database

    # get the user from the database
    with client:
        userData = {
            'name': 'Michalis',
            'username': 'kalymgr',
            'department': 'IT Department',
            'usercategory': 1,
            'phone': '22433XXXXX',
            'mobile': '6945XXXXX',
            'email': 'mtsougranis@gmail.com',
            'enabled': True,
            'password': 'kalymgr',
            'password2': 'kalymgr',
        }
        auth.login()
        response = client.post('/users/add', data=userData)
        dbSession = current_app.config['DBSESSION']
        # check if the user has been added to the database
        newUser = dbSession.query(User).filter(User.username == 'kalymgr').first()
        assert userData['name'] == newUser.name
        # delete the user
        dbSession.delete(newUser)
        dbSession.commit()


def test_DeleteUser(client, auth):

    with client:
        # login
        auth.login()

        # create a user to be deleted
        userToBeDeleted = User(name='User to be deleted',
                               username='del', password='del')
        dbSession = current_app.config['DBSESSION']
        dbSession.add(userToBeDeleted)
        dbSession.commit()

        # get the response from GET method
        response = client.get(url_for('users.deleteUser', user_id=userToBeDeleted.id))

        # check that the user is logged in and that the global user is test user
        assert g.user.id == 1

        # check that the GET response for the existing is ok
        assert response.status_code == 200

        # check that the GET response for a non existing user is 404
        response = client.get(url_for('users.deleteUser', user_id=546789785))
        assert response.status_code == 404

        # check that the user is properly deleted when POST method is used
        response = client.post(url_for('users.deleteUser', user_id=userToBeDeleted.id))
        u = dbSession.query(User).filter(User.id == userToBeDeleted.id).first()
        assert u is None  # the user no more exists in the database

        # check that there has been a redirection to the users list page
        locationHeaderResponse = helperFunctions.getHeaderContent(response.headers,'Location')
        assert locationHeaderResponse.endswith(url_for('users.userList'))


def test_editUser(client, auth):

    with client:

        auth.login()
        dbSession = current_app.config['DBSESSION']
        # test that the user is logged in as test user
        response = client.get(url_for('users.editUser', user_id=1))
        assert g.user.id == 1

        # test that the response is 404 for a non existing user
        response404 = client.get(url_for('users.editUser', user_id=6890076))
        assert response404.status_code == 404

        # test that the response is 200 for an existing user
        assert response.status_code == 200

        # test that the form properly loaded the user's data in the form fields

        # test that the user's data was properly updated (POST method)
        userToUpdate = User()  # first insert a new user in the database
        userToUpdate.name = 'User to update'
        userToUpdate.username = 'utu'
        userToUpdate.password = 'utu'
        userToUpdate.enabled = False
        userToUpdate.email = 'email'
        userToUpdate.phone = 'phone'
        userToUpdate.mobile = 'mobile',
        userToUpdate.department = 'dep'

        dbSession.add(userToUpdate)
        dbSession.commit()

        userUpdated = User()  # user with updated data
        userUpdated.name = 'User to update'
        userUpdated.username = 'utu updated'
        userUpdated.enabled = True
        userUpdated.email = 'email updated'
        userUpdated.phone = 'phoneUp'
        userUpdated.mobile = 'mobileUp',
        userUpdated.userCategoryId = 1
        userUpdated.department = 'depUp'

        # set the data that will be sent via POST method
        userData = {
            'name': userUpdated.name,
            'username': userUpdated.username,
            'enabled': userUpdated.enabled,
            'email': userUpdated.email,
            'phone': userUpdated.phone,
            'mobile': userUpdated.mobile,
            'usercategory': userUpdated.userCategoryId,
            'department': userUpdated.department
        }

        # send the POST request
        response = client.post(url_for('users.editUser', user_id = userToUpdate.id),
                               data = userData)


