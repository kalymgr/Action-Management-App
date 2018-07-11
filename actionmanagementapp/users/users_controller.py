# -*- coding: utf-8 -*-

"""
Blueprint related to user management
"""
import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import abort

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, g)
from werkzeug.utils import secure_filename

from actionmanagementapp.auth.auth_controller import login_required, user_permissions_restrictions
from actionmanagementapp.org.org_models import Service
from actionmanagementapp.users.users_models import User, UserCategory
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from actionmanagementapp.utilities.resource_strings import UsersResourceString, AuthResourceStrings

# create the blueprint
from actionmanagementapp.utilities.utility_classes import UploadHelper

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route('/')
@login_required
@user_permissions_restrictions
def userList():
    """
    User List page routing function
    :return:
    """
    # get the db session from the application settings

    # if the user is a simple user (cat id == 1) then redirect to his user details page
    # u = dbSession.query(User).filter(User.id == g.user.id).first()
    # if u.userCategoryId == 1:  # if he/she is a simple user
    #     return redirect(url_for('users.userDetails', user_id=g.user.id))

    # get the list of users
    dbSession = current_app.config['DBSESSION']  # get the db session
    users = dbSession.query(User).all()
    return render_template('usermanagement/users.html', users=users)


@bp.route('/<int:user_id>')
@bp.route('/<int:user_id>/view')
@login_required
@user_permissions_restrictions
def userDetails(user_id):
    """
    User details routing function
    :return:
    """
    # get the db session from the application settings
    dbSession = current_app.config['DBSESSION']  # get the db session
    user = dbSession.query(User).filter(User.id == user_id).first()
    if user is not None:  # if the user is found in the database
        katigoria = user.userCategory.name
    if user is None:
        abort(404, UsersResourceString.ERROR_NON_EXISTING_USER)

    return render_template('usermanagement/userdetails.html', user=user)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
@user_permissions_restrictions
def addUser():
    """
    Add user routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session
    # get the user categories and the services
    userCat = dbSession.query(UserCategory).all()
    services = dbSession.query(Service).order_by(Service.name.asc()).all()

    # create a new user object
    user = User()

    # save the user in the database
    error = UserHelperFunctions.saveUser(user, request, dbSession)

    # if everything was ok, go to the main users page
    if error == '':
        return redirect(url_for('users.userList'))

    return render_template('usermanagement/adduser.html',
                           user=None, userCategories=userCat, services=services)


@bp.route('/<int:user_id>/delete', methods=('GET', 'POST'))
@login_required
@user_permissions_restrictions
def deleteUser(user_id):
    """
    Delete user routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session
    if request.method == 'POST':
        # delete the user from the database
        u = dbSession.query(User).filter(User.id == user_id).first()
        dbSession.delete(u)
        dbSession.commit()

        # send a message that the specific user has been deleted
        flash(UsersResourceString.INFO_USER_DELETED % u.name)
        # redirect to the users list page
        return redirect(url_for('users.userList'))

    else:  # GET method
        # get the user by his/her user id

        u = dbSession.query(User).filter(User.id == user_id).first()
        # if the user does not exist, throw 404 error
        if u is None:
            abort(404)
        # if the user exists, show the delete page
        else:
            return render_template('usermanagement/deleteuser.html', user=u)


@bp.route('/<int:user_id>/edit', methods=('GET', 'POST'))
@login_required
@user_permissions_restrictions
def editUser(user_id):
    """
    Edit user routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session

    # get the user
    user = dbSession.query(User).filter(User.id == user_id).first()
    # get the categories and the services from the database
    uCategories = dbSession.query(UserCategory).all()
    services = dbSession.query(Service).order_by(Service.name.asc()).all()

    if user is None:
        abort(404)
    # save the user
    error = UserHelperFunctions.saveUser(user, request, dbSession)

    if error == '':
        return redirect(url_for('users.userList'))

    return render_template('usermanagement/edituser.html', user=user,
                           userCategories=uCategories, services=services)


@bp.route('/<int:user_id>/changepassword', methods=('GET', 'POST'))
@login_required
@user_permissions_restrictions
def changeUserPassword(user_id):
    """
    Change user password routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session
    u = dbSession.query(User).filter(User.id == user_id).first()  # get the user from the database
    if u is None:  # if the user does not exist in the database
        abort(404)
    if request.method == 'POST':
        oldPass = request.form.get('oldpassword', '')
        newPass1 = request.form.get('newpassword1', '')
        newPass2 = request.form.get('newpassword2', '')

        error = UserHelperFunctions.checkChangeUserPassword(u, oldPass, newPass1, newPass2)
        # if there is no error
        if error == '':
            # insert the new password in the database
            u.password = generate_password_hash(newPass1)
            dbSession.add(u)
            dbSession.commit()
            # go to the user details page
            flash(UsersResourceString.INFO_USER_PASSWORD_CHANGED % u.name)
            return redirect(url_for('users.userDetails', user_id=user_id))

        flash(error)

        # return redirect(url_for('users.userDetails', user_id=user_id))

    return render_template('usermanagement/changeuserpassword.html', user=u)


@bp.route('/categories')
@login_required
@user_permissions_restrictions
def userCategories():
    """
    User categories routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session
    categories = dbSession.query(UserCategory).all()
    return render_template('usermanagement/usercategories.html', userCategories=categories)


@bp.route('/categories/add', methods=('GET', 'POST'))
@login_required
@user_permissions_restrictions
def addUserCategory():
    """
    Add category routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session
    if request.method == 'POST':

        c = UserCategory()
        c.id = request.form.get('id', None)
        c.name = request.form.get('name', None)

        error = ''
        if c.id == '' or c.id is None:
            error += UsersResourceString.ERROR_USER_CATEGORY_ID_NOT_ENTERED
        if c.name == '' or c.id is None:
            error += UsersResourceString.ERROR_USER_CATEGORY_NAME_NOT_ENTERED

        if error == '':
            try:
                dbSession.add(c)
                dbSession.commit()  # add the new category in the database
                flash(UsersResourceString.INFO_USER_CATEGORY_ADDED)
                return redirect(url_for('users.userCategories'))
            except IntegrityError as e:
                flash(UsersResourceString.INFO_USER_CATEGORY_ID_EXISTS)
                dbSession.rollback()

        else:
            flash(error)

    return render_template('usermanagement/addusercategory.html')


@bp.route('/categories/<int:user_category_id>/edit', methods=('GET', 'POST'))
@login_required
@user_permissions_restrictions
def editUserCategory(user_category_id):
    """
    Edit category routing function
    :return:
    """
    # get the db session variable
    dbSession = current_app.config['DBSESSION']  # get the db session
    if request.method == 'POST':
        # get the POST fields
        catNameUpdated = request.form.get('name', None)

        c = dbSession.query(UserCategory).filter(UserCategory.id == user_category_id).first()

        # check for validation errors
        error = ''
        if catNameUpdated == '':
            error += UsersResourceString.ERROR_USER_CATEGORY_NAME_NOT_ENTERED

        if error != '':
            flash(error)
        else:
            # get the category from the database
            c.name = catNameUpdated
            dbSession.add(c)
            dbSession.commit()

            # show message for successful edit
            flash(UsersResourceString.INFO_USER_CATEGORY_UPDATED)
            # go to the main categories page
            return redirect(url_for('users.userCategories'))
    else:
        # get the category from the database
        c = dbSession.query(UserCategory).filter(UserCategory.id == user_category_id).first()
        if c is None:  # if the category with the specific id does not exist
            abort(404)  # respond with 404 error

    return render_template('usermanagement/editusercategory.html', userCategory=c)


@bp.route('/categories/<int:user_category_id>/delete', methods=('GET', 'POST'))
@login_required
@user_permissions_restrictions
def deleteUserCategory(user_category_id):
    """
    Delete category routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session
    c = dbSession.query(UserCategory).filter(UserCategory.id == user_category_id).first()  # get the category
    if request.method == 'POST':
        # get the id of the category to be deleted
        dbSession.delete(c)
        dbSession.commit()
        flash(UsersResourceString.INFO_USER_CATEGORY_DELETED)
        return redirect(url_for('users.userCategories'))
    else:
        if c is None:
            abort(404)

    return render_template('usermanagement/deleteusercategory.html', userCategory=c)


class UserHelperFunctions:
    """
    Class with helper functions related to user management
    """

    @staticmethod
    def checkChangeUserPassword(user, oldPass, newPass1, newPass2):
        """
        Method that checks whether a user password can be changed
        :param user: the user object
        :param oldPass: the old password
        :param newPass1: the new password
        :param newPass2: the new password
        :return: an error, if there is a problem, else ''
        """

        error = ''  # initialize an empty error message
        # check that the password given by the user is right
        if not check_password_hash(user.password, oldPass):
            error += AuthResourceStrings.ERROR_WRONG_PASSWORD
        # check that the new password is not blank
        if newPass1 == '':
            error += UsersResourceString.ERROR_USER_NEW_PASSWORD_BLANK
        # check that the two passwords match
        if newPass1 != newPass2:
            error += UsersResourceString.ERROR_USER_PASSWORDS_DO_NOT_MATCH

        return error

    @staticmethod
    def validateUser(user, request):
        """
        method for validating the user (insert and update operations)
        :param user: the user object
        :param form: the form with the user data
        :return: the object and an error, if there is a problem with validation
        """
        user.name = request.form.get('name', None)
        user.username = request.form.get('username', None)
        user.serviceId = request.form.get('service', None)
        user.userCategoryId = request.form.get('usercategory', None)
        user.phone = request.form.get('phone', None)
        user.mobile = request.form.get('mobile', None)
        user.email = request.form.get('email', None)
        # The checkbox field isn't returned if it is not checked.
        # So I tell the application that, if the form has no enabled field, return None value
        if request.form.get('enabled', None) == "on":
            user.enabled = True
        else:
            user.enabled = False

        # get the password in the case of a new user
        if user.id is None:
            user.password = request.form.get('password', None)
            password2 = request.form.get('password2', None)

        error = ''

        # Check for required fields that are empty
        if not user.name or user.name == '':
            error += UsersResourceString.ERROR_NAME_NOT_ENTERED
        if not user.username:
            error += UsersResourceString.ERROR_USERNAME_NOT_ENTERED
        if not user.userCategoryId:
            # error += UsersResourceString.ERROR_USER_CATEGORY_NOT_ENTERED
            userCatId = 1  # make him/her a simple user

        if not user.email:
            error += UsersResourceString.ERROR_EMAIL_ADDRESS_NOT_ENTERED

        # in the case of the insertion of a new user, check that the two passwords conform to the constraints
        if user.id is None:
            if not user.password:
                error += UsersResourceString.ERROR_EMPTY_USER_PASSWORD
            if user.password != password2:
                error += UsersResourceString.ERROR_PASSWORDS_DO_NOT_MATCH

        return user, error

    @staticmethod
    def saveUser(user, request, dbSession):
        """
        Method that saves a user in the database
        :param user:
        :param request:
        :param dbSession:
        :return: error, if one exists
        """
        if request.method == 'POST':
            user, error = UserHelperFunctions.validateUser(user, request)
            if error != '':
                flash(error)
            else:
                dbSession.add(user)
                dbSession.commit()

                # save the user avatar, if it exists
                try:
                    userAvatar = request.files.get('avatar', None)
                    # if everything is ok with the user avatar
                    if userAvatar and UploadHelper.allowed_image_file(userAvatar.filename):
                        # get the secure file name
                        avatarFileName = secure_filename(userAvatar.filename)
                        # set the name as it will be stored in the db and file system
                        dbAvatarFileName = 'usr_'+str(user.id)+'_'+avatarFileName
                        filePath = os.path.join(
                            current_app.config['UPLOAD_FOLDER'],
                            dbAvatarFileName
                        )
                        # save in the proper path
                        userAvatar.save(filePath)
                        user.avatar = dbAvatarFileName
                        dbSession.add(user)
                        dbSession.commit()

                except IOError, e:
                    flash(str(e))

                flash(UsersResourceString.INFO_USER_UPDATED % user.name)
            return error
