# -*- coding: utf-8 -*-
"""
File that is used for configuring logging settings.
The LoginAttemptFilter class and the filters section are not used because
the http handler that saves login attempts in the database could not be implemented via flask.logger.
So, the standard logging libraries were used (Check HttpLoggerSetup class in http_log_handling.py)
"""
from logging import Filter
from logging.config import dictConfig

from flask import url_for

"""
class LoginAttemptFilter(Filter):
    # Class that filters the login items and returns only those that are related to login attempts
    
    def filter(self, record):

        loginText = 'Login attempt:'
        if loginText in record.msg:
            return True  # keep this record
        else:
            return False  # do not keep this record

This section was in the dictConfig, to enable filters
'filters': {  # custom filters used by some handlers
    'loginAttempt': {  # filter that creates a log when there is an attempt to login
        '()': LoginAttemptFilter,
    }
},
"""

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
                    'level': 'ERROR',  # filter logging level per handler
                },

                'debugconsole':  # handler that sends all messages to the console - should be activated only during dev
                {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    # 'level': 'NOTSET',  # this is the lowest log level
                },

             },
        'root': {
            'handlers': ['smtp', 'debugconsole']
        }
    })