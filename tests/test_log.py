import pytest
from flask import url_for, current_app

from actionmanagementapp.log.log_models import LoggingRecord


def test_addLog(client, auth):

    with client:
        auth.login()  # just used to pass the application context
        dbSession = current_app.config['DBSESSION']  # get the db session

        # test that get method is not allowed
        response405 = client.get(url_for('log.addLog'))
        assert response405.status_code == 405

        # create a log and test that it is inserted int the database
        newLog = {'description': 'testing logging records'}
        responsePOST = client.post(url_for('log.addLog'), data=newLog)

        # check if the log is in the database
        newLogFromDatabase = dbSession.query(LoggingRecord)\
            .filter(LoggingRecord.description=='testing logging records').first()
        assert newLogFromDatabase is not None

        # delete the log from the database
        if newLogFromDatabase is not None:
            dbSession.delete(newLogFromDatabase)
            dbSession.commit()




