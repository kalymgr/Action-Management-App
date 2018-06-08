# -*- coding: utf-8 -*-
import pytest
from flask import g, current_app, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from actionmanagementapp.users.model import User, UserCategory
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


@pytest.mark.parametrize(('name', 'username', 'userCategory', 'password', 'password2', 'message'),
                         (
                                ('', 'aoua', '1', '1', '1', u'Δε δόθηκε το όνομα'),  # empty name
                                ('aaaa', '', '1', '1', '1', u'Δε δόθηκε όνομα χρήστη'),  # empty user name
                                ('aaaa', 'aaa', '', '1', '1', u'Δε δόθηκε κατηγορία χρήστη'),  # empty category
                                ('aaaa', 'aa', '1', '', '', u'Κενός κωδικός χρήστη'),  # empty password
                                ('aaaa', '', '1', '123', '321', u'Δεν ταιριάζουν οι κωδικοί')  # passwords do not match
                         ))
def test_addUser_validInput(client, auth, name, username, userCategory, password, password2, message):
    with client:
        auth.login()  # login
        response = client.post(url_for('users.addUser'),
                               data={
                                   'name': name,
                                   'username': username,
                                   'usercategory': userCategory,
                                   'password': password,
                                   'password2': password2
                               })
        assert message in response.data.decode('utf-8')

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
        locationHeaderResponse = helperFunctions.getHeaderContent(response.headers, 'Location')
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
        userToUpdate.mobile = 'mobilep'
        userToUpdate.department = 'dep'

        dbSession.add(userToUpdate)
        dbSession.commit()

        userUpdated = User()  # user with updated data
        userUpdated.name = 'User to update'
        userUpdated.username = 'utu updated'
        userUpdated.enabled = True
        userUpdated.email = 'email updated'
        userUpdated.phone = 'phoneUp'
        userUpdated.mobile = 'mobileUpdated'
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
        response = client.post(url_for('users.editUser', user_id=userToUpdate.id),
                               data=userData)

        # check if the data was properly updated
        userFromDb = dbSession.query(User).filter(User.username == userUpdated.username).first()
        assert userFromDb is not None

        dbSession.delete(userFromDb)  # delete the updated user (not needed)
        dbSession.commit()

        # check that after the successful updating of user, the browser redirects to users list page
        locationHeaderResponse = helperFunctions.getHeaderContent(response.headers, 'Location')
        assert locationHeaderResponse.endswith(url_for('users.userList'))


def test_changeUserPassword(client, auth):
    with client:
        auth.login()  # the user is logged in
        dbSession = current_app.config['DBSESSION']  # get the database session

        # create a new user for testing
        u = User(name='testchangepwduser',
                 username='pwdusername',
                 password=generate_password_hash('1234'))
        dbSession.add(u)
        dbSession.commit()

        # test that the user properly gets the page (answer 200)
        response = client.get(url_for('users.changeUserPassword', user_id=u.id))
        assert response.status_code == 200

        # test that the global user exists
        assert g.user.id == 1  # the id of the default test user

        # test that the user get the page for changing his/her password (not someone else)
        # the response data had to be decoded with UTF-8 because of Greek
        assert u.name in response.data.decode('utf-8')

        # test that for a non existing user, a 404 error is returned
        response404 = client.get(url_for('users.changeUserPassword', user_id=11846292))
        assert response404.status_code == 404

        userData = {  # user data with wrong old password
            'oldpassword': u'1',
            'newpassword1': u'1',
            'newpassword2': u'1'
        }

        # send the POST request
        responsePost = client.post(url_for('users.changeUserPassword', user_id=u.id),
                                   data=userData)
        assert u'Λάθος κωδικός' in responsePost.data.decode('utf-8')

        # test that the new password is not blank
        userDataBlankNewPassword = {  # user data with empty new password
            'oldpassword': u'1234',
            'newpassword1': u'',
            'newpassword2': u''
        }
        responsePost = client.post(url_for('users.changeUserPassword', user_id=u.id),
                                   data=userDataBlankNewPassword)
        assert u'Ο καινούριος κωδικός δε μπορεί να είναι κενός' in responsePost.data.decode('utf-8')

        # test that the two new passwords match
        userDataNewPasswordsDontMatch= {  # new passwords don't match
            'oldpassword': u'1234',
            'newpassword1': u'9999',
            'newpassword2': u'8888'
        }
        responsePost = client.post(url_for('users.changeUserPassword', user_id=u.id),
                                   data=userDataNewPasswordsDontMatch)

        assert u'Οι δύο κωδικοί δεν ταιριάζουν' in responsePost.data.decode('utf-8')

        # test that the new password has been properly inserted in the database
        userDataOK = {  # user data which is OK
            'oldpassword': u'1234',
            'newpassword1': u'9999',
            'newpassword2': u'9999'
        }
        # change the password of the user
        responsePost = client.post(url_for('users.changeUserPassword', user_id=u.id),
                                   data=userDataOK)
        # get the user from the database
        userWithChangedPassword = dbSession.query(User).filter(User.id == u.id).first()
        # check if the new password is the one inserted
        assert check_password_hash(userWithChangedPassword.password, userDataOK['newpassword1'])


        # delete user
        dbSession.delete(u)
        dbSession.commit()

def test_userCategories(client, auth):
    with client:
        auth.login()  # login
        dbSession = current_app.config['DBSESSION']  # get the database session

        # test that the response for a get request is 200
        response = client.get(url_for('users.userCategories'))
        assert response.status_code == 200

        # test that the categories are shown on the page
        categories = dbSession.query(UserCategory).all()  # get the categories from the database
        for category in categories:
            assert category.name in response.data.decode('utf-8')  # all category names should appear on page


@pytest.mark.parametrize(('catId', 'name', 'message'),(
        ('', 'empty id category', u'Δε συμπληρώθηκε κωδικός κατηγορίας'),
        ('28391782', '', u'Δε συμπληρώθηκε όνομα κατηγορίας')
))
def test_addUserCategory_validateInput(client, auth, catId, name, message):
    with client:
        auth.login()
        response = client.post(url_for('users.addUserCategory'), data={'id': catId, 'name': name})
        assert message in response.data.decode('utf-8')


def test_addUserCategory(client, auth):
    with client:
        auth.login()  # login
        dbSession = current_app.config['DBSESSION']  # get the database session

        # test that the get method returns a 200 status
        response = client.get(url_for('users.addUserCategory'))
        assert response.status_code == 200

        # test that the post method properly saves the data in the database
        categoryData = {'id': 5827, 'name': 'testing add new category'}
        responsePost = client.post(url_for('users.addUserCategory'), data=categoryData)

        catAdded = dbSession.query(UserCategory).filter(UserCategory.id == categoryData['id']).first()
        assert catAdded is not None

        # remove the category from the database (cleaning)
        dbSession.delete(catAdded)
        dbSession.commit()

        # test that the user cannot create a new category with an existing id (integrity error)
        cat = dbSession.query(UserCategory).first()  # get an existing category
        newCat = UserCategory()
        newCat.id = cat.id
        newCat.name = cat.name
        responseDuplicateKey = client.post(url_for('users.addUserCategory'),
                                           data={
                                               'id': newCat.id,
                                               'name': newCat.name
                                           })
        assert u'Ο κωδικός κατηγορίας υπάρχει ήδη' in responseDuplicateKey.data.decode('utf-8')
