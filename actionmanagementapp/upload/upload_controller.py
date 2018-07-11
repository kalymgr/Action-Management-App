from flask import Blueprint, request, current_app, send_from_directory

bp = Blueprint("uploads", __name__, url_prefix="/uploads")

@bp.route('/<filename>')
def getUploadedFile(filename):
    """
    routing function for getting the uploaded file
    :param filename:
    :return:
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)

