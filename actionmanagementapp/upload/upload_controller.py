from flask import Blueprint, request, current_app, send_from_directory

bp = Blueprint("uploads", __name__, url_prefix="/uploads")

@bp.route('/organization_logos/<filename>')
def orgLogos(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)
