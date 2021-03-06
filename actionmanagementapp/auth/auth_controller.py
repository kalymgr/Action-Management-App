"""
Blueprint for authentication
"""
import os

from werkzeug.exceptions import abort

from actionmanagementapp.utilities.resource_strings import AuthResourceStrings, UsersResourceString, \
    GeneralResourceStrings, OrganizationResourceStrings, MenuResourceStrings, ActionResourceStrings, DropdownLists

from actionmanagementapp.log.http_log_handling import HttpLoggerSetup
from actionmanagementapp.users.users_models import User, UserCategory
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app,
    app)
from werkzeug.security import check_password_hash, generate_password_hash


# a blueprint named auth is created.Like the application object,
# the blueprint needs to know where it's defined, so __name__ is passed as the second argument
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Function for routing the login page requests
    :return:
    """
    # get the db session from the application settings
    # dbSession = current_app.config['DBSESSION']()

    applicationLogger = current_app.logger  # get the application logger
    dbSession = current_app.config['DBSESSION']  # get the db session
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # get the user with the specific username. If not user is found,
        # first() will return None
        user = dbSession.query(User).filter(User.username == username).first()

        # setup a logger that stores login attempts in the database
        dbLoginLoggerSetup = HttpLoggerSetup()
        dbLoginLogger = dbLoginLoggerSetup.getLogger()

        # check if the user can login
        error = LoginHelperFunctions.checkLogin(user, password, dbLoginLogger)

        if error is '':
            dbLoginLogger.info((AuthResourceStrings.INFO_SUCCESSSFUL_LOGIN % username).encode('utf-8'))
            session.clear()
            session['user_id'] = user.id
            # return redirect(url_for('index'))
            return redirect(url_for('users.userList'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_resource_strings():
    """
    This function will always run before the view function, no matter what URL is requested.
    It loads the resource strings used in the templates.
    It also loads the absolute file location of the font file needed for properly creating
    pdf documents.
    :return:
    """
    # resource strings
    g.userResourceStrings = UsersResourceString
    g.authResourceStrings = AuthResourceStrings
    g.generalResourceStrings = GeneralResourceStrings
    g.organizationResourceStrings = OrganizationResourceStrings
    g.actionResourceStrings = ActionResourceStrings
    g.menuResourceStrings = MenuResourceStrings
    g.dropDownLists = DropdownLists

    # absolute file location for font file for pdf documents. It will be used in CSS rules.
    g.pdfFontFileAbsolutePath = os.path.abspath('./static/fonts/GFSDidot-Regular.ttf')

    # absolute folder location for uploaded images
    g.imageFolderAbsolutePath = os.path.abspath('./uploads/')

@bp.before_app_request
def load_logged_in_user():
    """
    This function will always run before the view function, no matter what URL is requested.
    It gets the user data from the database so as to use them when needed
    :return:
    """
    # get the db session from the application settings
    # dbSession = current_app.config['DBSESSION']()
    user_id = session.get('user_id')
    dbSession = current_app.config['DBSESSION']  # get the db session
    if user_id is None:
        g.user = None
    else:
        g.user = dbSession.query(User).filter(User.id == user_id).first()

    # g.userResourceStrings = UsersResourceString
    # g.authResourceStrings = AuthResourceStrings


@bp.route('/logout')
def logout():
    """
    Used when a user decides to logout. It clears the http session (deletes the user id)
    :return:
    """
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    """
    decorator function. It requires from the user to be loggedin, for each view it's applied to, t
    :param view:
    :return:
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def user_permissions_restrictions(view):
    """
    sets restrictions on user permissions
    :param view:
    :return:
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # get the user id from the url
        userIdFromUrl = kwargs.get('user_id', None)
        dbSession = current_app.config['DBSESSION']  # get the db session
        if g.user.userCategoryId == 1:  # if he is a simple user - Level 1

            if userIdFromUrl is None:
                return redirect(url_for('users.userDetails', user_id=g.user.id))
            else:
                # if he tries to access any url that isn't related to him
                if g.user.id != userIdFromUrl:
                    # redirect the user to his user page
                    abort(403)  # access denied
        elif g.user.userCategoryId == 2:  # if he is an administrator - Level 2
            if userIdFromUrl is not None:
                # get the user category
                u = dbSession.query(User).filter(User.id == userIdFromUrl).first()
                uCategory = u.userCategoryId

                # if the page is not related to simple users and not related to the logged in user
                if uCategory != 1 and userIdFromUrl != g.user.id:
                    abort(403)  # access denied
                # check for the urls related to user categories

        return view(**kwargs)

    return wrapped_view


class LoginHelperFunctions:
    """
    class that contains helper functions for logging in
    """

    @staticmethod
    def checkLogin(user, password, dbLoginLogger):
        """
        Static Method that decides whether the user will log in or not.
        :param: the user object
        :param: the user password typed by the user
        :return: error message (if there is one), else ''
        """

        error = ''  # initialize the error variable

        if user is None:
            error = AuthResourceStrings.ERROR_WRONG_USERNAME
            # log the attempt
            dbLoginLogger.info(AuthResourceStrings.ERROR_WRONG_USERNAME_2.encode('utf-8'))

        elif not check_password_hash(user.password, password):
            error = AuthResourceStrings.ERROR_WRONG_PASSWORD
            dbLoginLogger.info(AuthResourceStrings.ERROR_WRONG_PASSWORD_2.encode('utf-8'))
        elif user.enabled is False:  # the user is not activated/enabled
            error = AuthResourceStrings.ERROR_USER_NOT_ACTIVATED
            dbLoginLogger.info(AuthResourceStrings.ERROR_USER_NOT_ACTIVATED_2.encode('utf-8'))

        return error
