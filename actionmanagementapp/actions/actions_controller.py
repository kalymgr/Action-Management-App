# -*- coding: utf-8 -*-

"""
Blueprint related to actions
"""


from flask import Blueprint, current_app, render_template

# create the blueprint
from werkzeug.exceptions import abort

from actionmanagementapp.actions.actions_models import Action, ActionCategory, ActionGroup, FinancingSource
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
