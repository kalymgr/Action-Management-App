import os
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base

from utilities import DatabaseSetup
import auth
from actionmanagementapp.users import UsersController, UsersModels
from actionmanagementapp.auth import authController
from actionmanagementapp.utilities import CustomErrorPages
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
        DBSESSION=DatabaseSetup.getProductionDatabaseSession()
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
    app.register_blueprint(authController.bp)
    app.register_blueprint(UsersController.bp)
    # app.register_blueprint(log.bp)

    # register error pages handlers
    app.register_error_handler(404, CustomErrorPages.page_not_found)

    return app


if __name__ == '__main__':
    DatabaseSetup  # I put that here. Maybe I do it in a different way
    app = create_app()
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)