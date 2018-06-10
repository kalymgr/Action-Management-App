"""
File that is used for configuring logging settings
"""
from logging import Filter
from logging.config import dictConfig

from flask import url_for


class LoginAttemptFilter(Filter):
    """
    Class that filters the login items and returns only those that are related to login attempts
    """
    def filter(self, record):

        loginText = 'Login attempt:'
        if loginText in record.msg:
            return True  # keep this record
        else:
            return False  # do not keep this record


def setLoggingSettings():
    """
    Function that sets the logging preferences for the application. Must be called before the app is created
    :return:
    """
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},

        'filters': {  # custom filters used by some handlers
            'loginAttempt': {  # filter that creates a log when there is an attempt to login
                '()': LoginAttemptFilter,
            }
        },
        'handlers':
            {
                'smtp':  # handler that sends email to infoerawebdesign@gmail.com when an ERROR (or worse) happens
                {
                    'class': 'logging.handlers.SMTPHandler',
                    'formatter': 'default',
                    'mailhost': 'smtp.gmail.com',
                    'secure': (),  # needed because of tls/ssl smtp server
                    'credentials': ('mtsougranis2@gmail.com', 'k@lymn0s'),
                    'fromaddr': 'mtsougranis2@gmail.com',
                    'toaddrs': 'infoerawebdesign@gmail.com',
                    'subject': 'Actions Management App Log Event',
                    # 'filters': ['loginAttempt']
                    # 'level': 'ERROR',  # filter logging level per handler
                },
                'debugconsole':  # handler that sends all messages to the console - should be activated only during dev
                {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    # 'level': 'DEBUG',

                },
                'dblog': {  # handler that stores logs in the database
                    'class': 'logging.handlers.HTTPHandler',
                    'host': 'localhost',
                    'url': url_for('log.addLog'),
                    'method': 'POST'
                }

             },
        'root': {
            'handlers': ['smtp', 'debugconsole']
        }
    })