"""
Blueprint for authentication
"""

from users.model import User, UserCategory
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash


# a blueprint named auth is created.Like the application object,
# the blueprint needs to know where it's defined, so __name__ is passed as the second argument
bp = Blueprint('auth', __name__, url_prefix='/auth')


# Here, the routing functions are associated with URLS and functionality is implemented
"""
@bp.route('/register', methods=('GET', 'POST'))
def register():
    
    # get the db session from the application settings
    dbSession = current_app.config['DBSESSION']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form.get('email', None)
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            # check if the user is in the database
            noOfExistingUser =\
                dbSession.query(User).filter(User.username == username).count()
            if noOfExistingUser !=0:  # the user already exists
                error = "The user already exists"

        if error is None:
            # insert new user in the database
            newUser = User(name=name, username=username,
                           password=generate_password_hash(password, salt_length=8))
            dbSession.add(newUser)
            dbSession.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
"""


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

        if user is None:
            error = 'Incorrect username.'
            # log the attempt
            applicationLogger.info("Login attempt: Incorrect username")
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
            applicationLogger.info("Login attempt: Incorrect password")
        if error is None:
            applicationLogger.info("Login attempt: Successful login")
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
