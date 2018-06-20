# -*- coding: utf-8 -*-

"""
Blueprint related to organizational chart management
"""

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, g)
from actionmanagementapp.auth.auth_controller import login_required, user_permissions_restrictions
from actionmanagementapp.org.org_models import Organization, OrganizationType
from actionmanagementapp.users.users_models import User, UserCategory
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from actionmanagementapp.utilities.resource_strings import UsersResourceString, AuthResourceStrings, \
    OrganizationResourceStrings

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
    organizationList = dbSession.query(Organization).all()

    # get the proper template
    return render_template('org/organization_list.html', organizationList=organizationList)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def addOrg():
    """
    routing function for adding a new organization
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session

    if request.method == 'POST':
        # create a new organization and get the form fields
        newOrg = Organization()
        newOrg.id = request.form.get('id', None)
        newOrg.name = request.form.get('name', None)
        newOrg.address = request.form.get('address', None)
        newOrg.phone = request.form.get('phone', None)
        newOrg.ceo = request.form.get('ceo', None)
        newOrg.type = request.form.get('type', None)
        newOrg.email = request.form.get('email', None)
        newOrg.parentOrganizationId = request.form.get('parentOrganizationId', None)

        # if needed set, parent organization to None, to avoid sql integrity constraints error
        if newOrg.parentOrganizationId == '':
            newOrg.parentOrganizationId = None

        # check for constraints
        error = ''
        if newOrg.name is None or newOrg.name == '':
            error += OrganizationResourceStrings.ERR_ORGANIZATION_EMPTY_NAME
        if newOrg.ceo is None or newOrg.ceo == '':
            error += OrganizationResourceStrings.ERR_ORGANIZATION_EMPTY_CEO

        # save the new organization in the database
        if error != '':  # if there was an error
            flash(error)
        else:
            dbSession.add(newOrg)
            dbSession.commit()
            flash(OrganizationResourceStrings.TXT_ORGANIZATION_SAVED)
            return redirect(url_for('org.orgList'))
    orgTypes = dbSession.query(OrganizationType).all()  # get the organization types
    organizations = dbSession.query(Organization).all()
    return render_template('org/addorganization.html', orgTypes=orgTypes, organizations=organizations)