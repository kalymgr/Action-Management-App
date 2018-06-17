# -*- coding: utf-8 -*-

"""
Blueprint related to organizational chart management
"""

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, g)
from actionmanagementapp.auth.auth_controller import login_required, user_permissions_restrictions
from actionmanagementapp.org.org_models import Organization
from actionmanagementapp.users.users_models import User, UserCategory
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from actionmanagementapp.utilities.resource_strings import UsersResourceString, AuthResourceStrings

# create the blueprint
bp = Blueprint("org", __name__, url_prefix="/org")


@bp.route('/')
@login_required
def orgList():
    """
    Routing function that shows list of the organizations
    :return:
    """

    # get the db session from the application settings
    dbSession = current_app.config['DBSESSION']

    # get the organization list
    orgList = dbSession.query(Organization).all()

    # get the proper template
    return render_template('org/organization_list.html', orgList=orgList)