# -*- coding: utf-8 -*-

"""
Blueprint related to organizational chart management
"""

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, g)
from werkzeug.exceptions import abort

from actionmanagementapp.auth.auth_controller import login_required, user_permissions_restrictions
from actionmanagementapp.org.org_models import Organization, OrganizationType, Service, ServiceType
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
    return render_template('org/organizations.html', organizationList=organizationList)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def addOrg():
    """
    routing function for adding a new organization
    :return:
    """
    dbSession = current_app.config['DBSESSION']  # get the db session
    orgTypes = dbSession.query(OrganizationType).all()  # get the organization types
    organizations = dbSession.query(Organization).all()
    org = Organization()

    # save the organization
    error = OrganizationHelperFunctions.saveOrganization(org, request, dbSession)

    if error == '':
        return redirect(url_for('org.orgList'))

    return render_template('org/edit_organization.html', organization=None,
                           orgTypes=orgTypes, organizations=organizations)


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

    # save the organization
    error = OrganizationHelperFunctions.saveOrganization(org, request, dbSession)

    if error == '':
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


@bp.route('/services/')
@login_required
def services():
    """
    Function that returns a page with a list of the services
    :return:
    """
    dbSession = current_app.config['DBSESSION']

    # get the list of services from the db
    serv = dbSession.query(Service).all()
    return render_template('org/services.html', services=serv)


@bp.route('/services/<int:service_id>/edit', methods=('GET', 'POST'))
@login_required
def editService(service_id):
    """
    Function for editing a service
    :param service_id:
    :return:
    """
    dbSession = current_app.config['DBSESSION']
    serv = dbSession.query(Service).filter(Service.id == service_id).first()
    services = dbSession.query(Service).all()
    organizations = dbSession.query(Organization).all()
    serviceTypes = dbSession.query(ServiceType).all()

    if serv is None:
        abort(404)

    # call the method that saves the service in the database
    error = OrganizationHelperFunctions.saveService(serv, request, dbSession)

    if error == '':
        return redirect(url_for('org.services'))

    return render_template('org/edit_service.html',
                           service=serv,
                           services=services,
                           organizations=organizations,
                           serviceTypes=serviceTypes)


@bp.route('/services/add', methods=('GET', 'POST'))
@login_required
def addService():
    dbSession = current_app.config['DBSESSION']
    services = dbSession.query(Service).all()
    organizations = dbSession.query(Organization).all()
    serviceTypes = dbSession.query(ServiceType).all()
    serv = Service()

    # call the method that saves the service in the database
    error = OrganizationHelperFunctions.saveService(serv, request, dbSession)

    if error == '':
        return redirect(url_for('org.services'))

    return render_template('org/edit_service.html',
                           service=None,
                           services=services,
                           organizations=organizations,
                           serviceTypes=serviceTypes)


class OrganizationHelperFunctions:
    """
    class with various methods related to organization blueprint
    """

    @staticmethod
    def validateOrganization(organization, form):
        """
        method for validating (insert or update) an organization.
        This method performs the validation and stores the data of the form in the object
        :param: the organization sqlalchemy object, the http post request form
        :return: the object and an error, if there is a problem with validation
        """
        if organization.id is None:  # if it is not none, it's an update operation
            organization.id = form.get('id', None)
        organization.name = form.get('name', None)
        organization.address = form.get('address', None)
        organization.ceo = form.get('ceo', None)
        organization.type = form.get('type', None)
        organization.email = form.get('email', None)
        organization.phone = form.get('phone', None)
        organization.parentOrganizationId = form.get('parentOrganizationId', None)

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

    @staticmethod
    def saveOrganization(org, request, dbSession):
        """
        Method that saves the organization data (insert or update)
        :param org: the organization object
        :param request: the http request object
        :param dbSession: the db session object
        :return: the error
        """
        if request.method == 'POST':
            org, error = OrganizationHelperFunctions.validateOrganization(org, request.form)

            # save the new organization in the database
            if error != '':  # if there was an error
                flash(error)
            else:
                dbSession.add(org)
                dbSession.commit()
                flash(OrganizationResourceStrings.TXT_ORGANIZATION_SAVED)

            return error


    @staticmethod
    def validateService(service, form):
        """
        method for validating a service. It performs validation and stores the data in the object
        :param service: the service object.
        :param form: the html form that contains the data
        :return: the object and an error
        """

        error = ""

        # put the form field data in the object
        service.name = form.get('name', None)
        service.address = form.get('address', None)
        service.chief = form.get('chief', None)
        service.phone = form.get('phone', None)
        service.email = form.get('email', None)
        service.parentServiceId = form.get('parentServiceId', None)
        service.organizationId = form.get('organizationId', None)
        service.type = form.get('type', None)

        # if needed, set parent service id to None, to avoid integrity errors
        if service.parentServiceId == '':
            service.parentServiceId = None

        # check for validation errors
        if service.name is None or service.name == '':
            error += OrganizationResourceStrings.ERR_SERVICE_EMPTY_NAME
        if service.type is None:
            error += OrganizationResourceStrings.ERR_SERVICE_EMPTY_TYPE

        # return object and error
        return service, error

    @staticmethod
    def saveService(serv, request, dbSession):
        """
        Method for saving the service in the database, in case there is no error
        :param serv: the service object
        :param request: the http request object
        :param dbSession: the dbSession request object
        :return: the error
        """

        if request.method == 'POST':
            serv, error = OrganizationHelperFunctions.validateService(serv, request.form)

            if error != '':
                flash(error)
            else:
                dbSession.add(serv)
                dbSession.commit()
                flash(OrganizationResourceStrings.TXT_SERVICE_SAVED)
            return error
