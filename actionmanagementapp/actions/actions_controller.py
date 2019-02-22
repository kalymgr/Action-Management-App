# -*- coding: utf-8 -*-

"""
Blueprint related to actions
"""


from flask import Blueprint, current_app, render_template, jsonify

# create the blueprint
from werkzeug.exceptions import abort

from actionmanagementapp.actions.actions_models import Action, ActionCategory, ActionGroup, FinancingSource, \
    ActionFinancingSource
from actionmanagementapp.auth.auth_controller import login_required
from actionmanagementapp.org.org_models import Service

bp = Blueprint("actions", __name__, url_prefix="/actions")


@bp.route('/')
@login_required
def actions():
    """
    Routing function for showing an action list
    :return:
    """
    # get the list of actions
    dbSession = current_app.config['DBSESSION']  # get the db session
    actionList = dbSession.query(Action).all()
    return render_template('actions/actions.html', actions=actionList)


@bp.route('/<int:action_id>/edit', methods=('GET', 'POST'))
@login_required
def editAction(action_id):
    """
    routing function for editing a function data
    :param action_id:
    :return:
    """

    # get the action and other useful data from the database
    dbSession = current_app.config['DBSESSION']
    action = dbSession.query(Action).filter(Action.id == action_id).first()
    services = dbSession.query(Service).all()
    actionCategories = dbSession.query(ActionCategory).all()
    actionGroups = dbSession.query(ActionGroup).all()
    financingSources = dbSession.query(FinancingSource).all()

    if action is None:
        abort(404)

    # save the action - to be implemented

    # return the rendered template
    return render_template('actions/edit_action.html', action=action,
                           services=services,
                           actionCategories=actionCategories,
                           actionGroups=actionGroups,
                           financingSources=financingSources)


@bp.route('/financingsources_json', methods=('GET',))
@login_required
def financingSourcesJson():
    """
    Function that returns the financing sources data as json
    :return:
    """
    # get the financing sources data
    dbSession = current_app.config['DBSESSION']
    financingSources = dbSession.query(FinancingSource).all()

    # create the data that will be jsonified
    d = {}  # dictionary containing the financing sources
    for financingSource in financingSources:
        d[financingSource.id] = financingSource.name

    return jsonify(d)


@bp.route('/<int:action_id>/financingsources_json', methods=('GET',))
@login_required
def actionFinancingSourcesJson(action_id):
    """
    Function that returns the financing sources of a specific action
    :param action_id: the id of the action
    :return: the financing sources of the action
    """
    # get the financing sources of the specific action, from the database
    dbSession = current_app.config['DBSESSION']
    actionFinancingSources = \
        dbSession.query(ActionFinancingSource)\
        .filter(ActionFinancingSource.actionId == action_id).all()

    # create the data that will be jsonified

    l = []  # list of the action financing sources
    for actionFinancingSource in actionFinancingSources:
        l.append(
            {
                'actionId': actionFinancingSource.actionId,
                'financingSourceId': actionFinancingSource.financingSourceId,
                'budgetCode': actionFinancingSource.budgetCode,
                'amount': actionFinancingSource.amount
            }
        )
    return jsonify(l)


@bp.route('/<int:action_id>/json', methods=('GET',))
@login_required
def actionJson(action_id):
    """
    Function that returns the action data as json
    :param action_id: the id of the action
    :return: the action data in json format
    """
    dbSession = current_app.config['DBSESSION']

    # get the action data from the database
    action = dbSession.query(Action).filter(Action.id == action_id).first()
    actionDict = {
        'id': action.id,
        'name': action.name,
        'serviceInChargeId': action.serviceInChargeId,
        'implementationServiceId': action.implementationServiceId,
        'categoryId': action.categoryId,
        'newOrInProgress': action.newOrInProgress,
        'priority': action.priority,
        'groupId': action.groupId,
        'budget': action.budget,
        'budgetCode': action.budgetCode,
        'startDate': action.startDate,
        'endDate': action.endDate,
        'status': action.status,
        'details': action.details
    }

    return jsonify(actionDict)

@bp.route('/action_categories/json', methods=('GET',))
@login_required
def actionCategoriesJson():
    """
    Function for returning the action categories as json
    :return:
    """

    # get the action categories from the database
    dbSession = current_app.config['DBSESSION']
    actionCategories = dbSession.query(ActionCategory).all()

    # create the list that will be returned as json
    actionCategoriesList = []
    for actionCategory in actionCategories:
        actionCategoriesList.append(
            {
                'id': actionCategory.id,
                'name': actionCategory.name
            }
        )

    return jsonify(actionCategoriesList)


@bp.route('/action_groups/json', methods=('GET',))
@login_required
def actionGroupsJson():
    """
       Function for returning the action groups as json
       :return:
       """

    # get the action categories from the database
    dbSession = current_app.config['DBSESSION']
    actionGroups = dbSession.query(ActionGroup).all()

    # create the list that will be returned as json
    actionGroupsList = []
    for actionGroup in actionGroups:
        actionGroupsList.append(
            {
                'id': actionGroup.id,
                'name': actionGroup.name
            }
        )

    return jsonify(actionGroupsList)