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
from users.model import User, UserCategory
from werkzeug.security import generate_password_hash, check_password_hash
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
    if user is not None:  # if the user is found in the database
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
        """
        name = request.form['name']
        username = request.form['username']
        department = request.form['department']
        userCatId = request.form['usercategory']
        phone = request.form['phone']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        """
        name = request.form.get('name', None)
        username = request.form.get('username', None)
        department = request.form.get('department', None)
        userCatId = request.form.get('usercategory', None)
        phone = request.form.get('phone', None)
        mobile = request.form.get('mobile', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        password2 = request.form.get('password2', None)
        # The checkbox field isn't returned if it is not checked.
        # So I tell the application that, if the form has no enabled field, return None value
        if request.form.get('enabled', None) == "True":
            enabled = True
        else:
            enabled = False

        error = ''

        # Check for required fields that are empty
        if not name or name == '':
            error += u'Δε δόθηκε το όνομα.'
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

            # show message
            flash("The user %s has been added" % newUser.name)
            # go to the main users page
            return redirect(url_for('users.userList'))
    return render_template('usermanagement/adduser.html', userCategories=dummyData.userCategories)


@bp.route('/<int:user_id>/delete', methods=('GET', 'POST'))
@login_required
def deleteUser(user_id):
    """
    Delete user routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']
    if request.method == 'POST':
        # delete the user from the database
        u = dbSession.query(User).filter(User.id == user_id).first()
        dbSession.delete(u)
        dbSession.commit()

        # send a message that the specific user has been deleted
        flash("The user %s has been deleted"%u.name)
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
def editUser(user_id):
    """
    Edit user routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # initialize db session variable
    if request.method == 'POST':
        # get the form data and save them in the database
        u = dbSession.query(User).filter(User.id == user_id).first()

        u.name = request.form.get('name', None)
        u.username = request.form.get('username', None)
        u.enabled = bool(request.form.get('enabled', None))
        u.email = request.form.get('email', None)
        u.phone = request.form.get('phone', None)
        u.mobile = request.form.get('mobile', None)
        u.userCategoryId = request.form.get('usercategory', None)
        u.department = request.form.get('department', None)

        dbSession.add(u)  # update the user in the database
        dbSession.commit()

        # flash message that the user has been updated
        flash(u"The user %s has been updated"%u.name)
        # return redirect
        return redirect(url_for('users.userList'))

    else:
        # get the user from the database
        u = dbSession.query(User).filter(User.id == user_id).first()
        # get the categories from the database
        uCategories = dbSession.query(UserCategory).all()
        # if the user does not exist, send 404 response
        if u is None:
            abort(404)
        return render_template('usermanagement/edituser.html', user=u,
                           userCategories=uCategories)


@bp.route('/<int:user_id>/changepassword', methods=('GET', 'POST'))
@login_required
def changeUserPassword(user_id):
    """
    Change user password routing function
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # initialize db session variable
    u = dbSession.query(User).filter(User.id == user_id).first()  # get the user from the database
    if u is None:  # if the user does not exist in the database
        abort(404)
    if request.method == 'POST':
        oldPass = request.form.get('oldpassword', '')
        newPass1 = request.form.get('newpassword1', '')
        newPass2 = request.form.get('newpassword2', '')

        error = ''  # initialize an empty error message
        # check that the password given by the user is right
        if not check_password_hash(u.password, oldPass):
            error += u'Λάθος κωδικός χρήστη'
        # check that the new password is not blank
        if newPass1 == '':
            error += u'Ο καινούριος κωδικός δε μπορεί να είναι κενός'
        # check that the two passwords match
        if newPass1 != newPass2:
            error += u'Οι δύο κωδικοί δεν ταιριάζουν'
        # if there is no error
        if error == '':
            # insert the new password in the database
            u.password = generate_password_hash(newPass1)
            dbSession.add(u)
            dbSession.commit()
            # go to the user details page
            flash(u'Ο Κωδικός για το χρήστη %s έχει αλλάξει'%u.name)
            return redirect(url_for('users.userDetails', user_id=user_id))

        flash(error)

        # return redirect(url_for('users.userDetails', user_id=user_id))

    return render_template('usermanagement/changeuserpassword.html', user=u)


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
