# create the blueprint
from flask import Blueprint, request, current_app
import json
# define the blueprint
from actionmanagementapp.log.log_models import LoggingRecord

bp = Blueprint("log", __name__, url_prefix="/log")

# I had to define a path (not the root path of the bp, for the routing function to work)
@bp.route('/addlog', methods=['POST'])
def addLog():
    dbSession = current_app.config['DBSESSION']
    if request.method == 'POST':
        # logDescription = request.form.get('description', None)
        logDescription = request.form.get('msg', None)
        newLog = LoggingRecord(description=logDescription)
        dbSession.add(newLog)
        dbSession.commit()
        return ''  # just something returned