# -*- coding: utf-8 -*-
import os
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

from actionmanagementapp.org import org_controller
from utilities import database_setup
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
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        DBSESSION=database_setup.getProductionDatabaseSession(),
        # the following key will be used from templates as: config['APPLICATION_NAME']
        APPLICATION_NAME=u'Εφαρμογή διαχείρισης δράσεων Δήμου'

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

    # register error pages handlers
    app.register_error_handler(404, custom_error_pages.page_not_found)

    return app


if __name__ == '__main__':
    database_setup  # I put that here. Maybe I do it in a different way
    app = create_app()
    app.secret_key = 'super_secret_key'  # TODO: change the secret key before production
    app.debug = True
    app.run(host='0.0.0.0', port=5000)