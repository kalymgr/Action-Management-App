# create the blueprint
from flask import Blueprint, request, current_app

# define the blueprint
from actionmanagementapp.log.log_models import LoggingRecord

bp = Blueprint("log", __name__, url_prefix="/log")


@bp.route('/', methods=['POST'])
def addLog():
    dbSession = current_app.config['DBSESSION']
    if request.method == 'POST':
        logDescription = request.form.get('description', None)
        newLog = LoggingRecord(description=logDescription)
        dbSession.add(newLog)
        dbSession.commit()
        return ''  # just something returned