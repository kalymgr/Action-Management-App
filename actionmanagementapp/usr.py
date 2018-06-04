# -*- coding: utf-8 -*-

"""
Blueprint related to user management
"""
from werkzeug.exceptions import abort

from tests.users import dummyData
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for)
from auth import login_required
# create the blueprint
bp = Blueprint("users", __name__, url_prefix="/users")
from users.model import User
from werkzeug.security import generate_password_hash
from flask import current_app


@bp.route('/')
@login_required
def userList():
    """
    User List page routing function
    :return:
    """
    # create the user list that will be rendered (get the category name for each user)
    # usersData = dummyData.getUsersWithCategoryDescription()
    # return the rendered template

    # get the db session from the application settings
    dbSession = current_app.config['DBSESSION']
    # get the list of users
    users = dbSession.query(User).all()
    return render_template('usermanagement/users.html', users=users)


@bp.route('/<int:user_id>')
@bp.route('/<int:user_id>/view')
@login_required
def userDetails(user_id):
    """
    User details routing function
    :return:
    """
    # get the db session from the application settings
    dbSession = current_app.config['DBSESSION']
    user = dbSession.query(User).filter(User.id == user_id).first()
    katigoria = user.userCategory.name
    if user is None:
        abort(404, u"Ο Χρήστης δεν υπάρχει. The user does not exist!")

    """ 
    if user_id != g.user.id:
        abort(403, u"Δεν έχετε δικαιώματα να δείτε το χρήστη. No rights to view this user")
    """

    return render_template('usermanagement/userdetails.html', user=user)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def addUser():
    """
    Add user routing function
    :return:
    """
    if request.method == 'POST':
        error = None  # set an error variable

        forma = request.form
        name = request.form['name']
        username = request.form['username']
        department = request.form['department']
        userCatId = request.form['usercategory']
        phone = request.form['phone']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        # The checkbox field isn't returned if it is not checked.
        # So I tell the application that, if the form has no enabled field, return None value
        enabled = request.form.get('enabled', None)

        error = ''

        # Check for required fields that are empty
        if not name:
            error += u' Δε δόθηκε το όνομα.'
        if not username:
            error += u' Δε δόθηκε όνομα χρήστη.'
        if not userCatId:
            error += u' Δε δόθηκε κατηγορία χρήστη.'
        if not password:
            error += u' Κενός κωδικός χρήστη.'
        if password != password2:
            error += u' Δεν ταιριάζουν οι κωδικοί.'
        """
        """
        if error is not '':  # if there was an error
            flash(error)
        else:
            # save the user data in the database
            newUser = User(name=name,
                           username=username,
                           department=department,
                           userCategoryId=userCatId,
                           phone=phone,
                           mobile=mobile,
                           email=email,
                           password=generate_password_hash(password),
                           enabled=enabled)
            # get the db session from the application settings
            dbSession = current_app.config['DBSESSION']
            dbSession.add(newUser)
            dbSession.commit()

            # go to the main users page
            return redirect(url_for('users.userList'))
    return render_template('usermanagement/adduser.html', userCategories=dummyData.userCategories)


@bp.route('/<int:user_id>/delete')
@login_required
def deleteUser(user_id):
    """
    Delete user routing function
    :return:
    """
    return render_template('usermanagement/deleteuser.html', user=dummyData.user)


@bp.route('/<int:user_id>/edit')
@login_required
def editUser(user_id):
    """
    Edit user routing function
    :return:
    """

    return render_template('usermanagement/edituser.html', user=dummyData.getUserWithCategoryDescription(),
                           userCategories=dummyData.userCategories)


@bp.route('/<int:user_id>/changepassword')
@login_required
def changeUserPassword(user_id):
    """
    Change user password routing function
    :return:
    """
    return render_template('usermanagement/changeuserpassword.html', user=dummyData.user)


@bp.route('/categories')
@login_required
def userCategories():
    """
    User categories routing function
    :return:
    """
    return render_template('usermanagement/usercategories.html', userCategories=dummyData.userCategories)


@bp.route('/categories/add')
@login_required
def addUserCategory():
    """
    Add category routing function
    :return:
    """
    return render_template('usermanagement/addusercategory.html')


@bp.route('/categories/<int:user_category_id>/edit')
@login_required
def editUserCategory(user_category_id):
    """
    Edit category routing function
    :return:
    """
    return render_template('usermanagement/editusercategory.html', userCategory=dummyData.userCategory)


@bp.route('/categories/<int:user_category_id>/delete')
@login_required
def deleteUserCategory(user_category_id):
    """
    Delete category routing function
    :return:
    """
    return render_template('usermanagement/deleteusercategory.html', userCategory=dummyData.userCategory)
