from flask import render_template


def page_not_found(error):
    """
    Custom 404 error page
    :param error:
    :return:
    """
    return render_template('page_not_found.html'), 404
