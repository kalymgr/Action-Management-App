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
    d = {}  # dictionary of the action financing sources
    for actionFinancingSource in actionFinancingSources:
        d[actionFinancingSource.financingSourceId] = \
        {
            'budgetCode': actionFinancingSource.budgetCode,
            'amount': actionFinancingSource.amount
        }

    return jsonify(d)

