"""
Blueprint for authentication
"""
from actionmanagementapp.log.http_log_handling import HttpLoggerSetup
from actionmanagementapp.users.users_models import User, UserCategory
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
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
    dbSession = current_app.config['DBSESSION']

    applicationLogger = current_app.logger  # get the application logger

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        # get the user with the specific username. If not user is found,
        # first() will return None
        user = dbSession.query(User).filter(User.username == username).first()

        # setup a logger that stores login attempts in the database
        dbLoginLoggerSetup = HttpLoggerSetup()
        dbLoginLogger = dbLoginLoggerSetup.getLogger()

        if user is None:
            error = 'Incorrect username.'
            # log the attempt
            dbLoginLogger.info('Login attempt. Incorrect username')
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
            dbLoginLogger.info('Login attempt: Incorrect password')
        if error is None:
            dbLoginLogger.info('Login attempt: Successful login for user '+username)
            session.clear()
            session['user_id'] = user.id
            # return redirect(url_for('index'))
            return redirect(url_for('users.userList'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    This function will always run before the view function, no matter what URL is requested.
    It gets the user data from the database so as to use them when needed
    :return:
    """
    # get the db session from the application settings
    dbSession = current_app.config['DBSESSION']
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = dbSession.query(User).filter(User.id == user_id).first()


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
