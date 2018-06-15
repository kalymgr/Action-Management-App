# -*- coding: utf-8 -*-

import logging
import logging.handlers


class HttpLoggerSetup:
    """
    Class that manages the http logging. Sends logs to a POST url,
    which stores them in the database
    """
    def __init__(self):
        self.logger = logging.getLogger('synchronous logging')
        self.logger.setLevel('INFO')
        httpHandler = logging.handlers.HTTPHandler(
            'localhost:5000',
            '/log/addlog',
            method='POST'
        )
        self.logger.addHandler(httpHandler)

    def getLogger(self):
        return self.logger