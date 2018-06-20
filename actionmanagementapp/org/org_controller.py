# -*- coding: utf-8 -*-

"""
Blueprint related to organizational chart management
"""

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, g)
from werkzeug.exceptions import abort

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
        newOrg, error = OrganizationHelperFunctions.saveOrganization(newOrg, request.form)

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


@bp.route('/<int:org_id>/edit', methods=('GET', 'POST'))
@login_required
def editOrg(org_id):
    """routing function for editing an organization data"""

    dbSession = current_app.config['DBSESSION']
    # get the organization from the database
    org = dbSession.query(Organization).filter(Organization.id == org_id).first()
    orgTypes = dbSession.query(OrganizationType).all()
    organizations = dbSession.query(Organization).all()
    if org is None:
        abort(404)

    if request.method == 'POST':
        org, error = OrganizationHelperFunctions.saveOrganization(org, request.form)

        # save the new organization in the database
        if error != '':  # if there was an error
            flash(error)
        else:
            dbSession.add(org)
            dbSession.commit()
            flash(OrganizationResourceStrings.TXT_ORGANIZATION_SAVED)
            return redirect(url_for('org.orgList'))

    return render_template('org/edit_organization.html',
                           organization=org,
                           orgTypes=orgTypes,
                           organizations=organizations)


@bp.route('/<int:org_id>/delete', methods=('GET', 'POST'))
@login_required
def deleteOrg(org_id):
    """
    Routing function for deleting an organization
    :param org_id:
    :return:
    """
    dbSession=current_app.config['DBSESSION']
    org = dbSession.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        abort(404)

    if request.method == 'POST':
        dbSession.delete(org)
        dbSession.commit()
        flash(OrganizationResourceStrings.TXT_ORGANIZATION_DELETED)
        return redirect(url_for('org.orgList'))

    return render_template('org/delete_organization.html', org=org)


class OrganizationHelperFunctions:
    """
    class with various methods related to organization blueprint
    """

    @staticmethod
    def saveOrganization(organization, form):
        """
        method for saving (insert or update) an organization.
        This method performs the validation and stores the data of the form in the object
        :param: the organization sqlalchemy object, the http post request form
        :return: the object and an error, if there is a problem with validation
        """
        if organization.id is None:  # if it is not none, it's an update operation
            organization.id = request.form.get('id', None)
        organization.name = request.form.get('name', None)
        organization.address = request.form.get('address', None)
        organization.ceo = request.form.get('ceo', None)
        organization.type = request.form.get('type', None)
        organization.email = request.form.get('email', None)
        organization.phone = request.form.get('phone', None)
        organization.parentOrganizationId = request.form.get('parentOrganizationId', None)

        # if needed set, parent organization to None, to avoid sql integrity constraints error
        if organization.parentOrganizationId == '':
            organization.parentOrganizationId = None

        # check for constraints
        error = ''
        if organization.name is None or organization.name == '':
            error += OrganizationResourceStrings.ERR_ORGANIZATION_EMPTY_NAME
        if organization.ceo is None or organization.ceo == '':
            error += OrganizationResourceStrings.ERR_ORGANIZATION_EMPTY_CEO

        return organization, error