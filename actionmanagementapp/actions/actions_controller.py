# -*- coding: utf-8 -*-

"""
Blueprint related to actions
"""


from flask import Blueprint, current_app, render_template

# create the blueprint
from actionmanagementapp.actions.actions_models import Action
from actionmanagementapp.auth.auth_controller import login_required

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
