"""
Module with helper functions for testing
"""


def getHeaderContent(responseHeaders, headerName):
    """
    helper function that gets the content of a specific http response header
    :param responseHeaders:
    :param headerName:
    :return:
    """

    for h in responseHeaders:
        if h[0] == 'Location':
            return h[1]

