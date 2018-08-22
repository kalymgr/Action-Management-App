# -*- coding: utf-8 -*-
import os
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

from actionmanagementapp.actions import actions_controller, actions_models
from actionmanagementapp.org import org_controller
from actionmanagementapp.upload import upload_controller
from actionmanagementapp.utilities.database_init import initDb, dbSession
import auth
from actionmanagementapp.users import users_controller, users_models
from actionmanagementapp.auth import auth_controller
from actionmanagementapp.log import log_controller
from actionmanagementapp.utilities import custom_error_pages
from actionmanagementapp.log import logging_settings


def create_app(test_config=None):
    """
    This is the application factory function. It creates the application.
    Any configuration, registration, and other setup
    the application needs will happen inside the function,
    then the application will be returned.
    http://flask.pocoo.org/docs/1.0/tutorial/factory/
    :param test_config:
    :return:
    """

    # configure the logging settings before you create the app
    logging_settings.setLoggingSettings()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # the config attribute of the app is an object that holds the loaded
    # configuration values
    # http://flask.pocoo.org/docs/1.0/config/?highlight=instance_relative_config
    app.config.from_mapping(
        SECRET_KEY='dev',
        DBSESSION=dbSession,
        # the following key will be used from templates as: config['APPLICATION_NAME']
        APPLICATION_NAME=u'Εφαρμογή διαχείρισης δράσεων Δήμου',
        UPLOAD_FOLDER='uploads',  # name of the upload folder
        MAX_CONTENT_LENGTH=15 * 1024 * 1024  # max size of uploaded files - 15 Mb
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)  # this creates the instance folder ,if it does not exist
    except OSError:  # if the folder exists, an error is raised
        pass

    # the blueprints will be registered here, before the app is returned
    app.register_blueprint(auth_controller.bp)  # authorization blueprint
    app.register_blueprint(users_controller.bp)  # user management blueprint
    app.register_blueprint(log_controller.bp)  # logging blueprint
    app.register_blueprint(org_controller.bp)  # organizational chart blueprint
    app.register_blueprint(upload_controller.bp)  # upload blueprint
    app.register_blueprint(actions_controller.bp)  # actions blueprint

    # register error pages handlers
    app.register_error_handler(404, custom_error_pages.page_not_found)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """
        remove session after every request
        :param exception:
        :return:
        """
        dbSession.remove()

    return app


if __name__ == '__main__':
    initDb()  # initialize the database
    app = create_app()
    app.secret_key = 'super_secret_key'  # TODO: change the secret key before production
    app.debug = True

    app.env = 'development'  # this must be changed to production, before deployment

    app.run(host='127.0.0.1', port=5000)  # initially the address was 0.0.0.0
