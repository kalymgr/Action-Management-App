"""
This module contains some utility classes, used for various purposes
"""
import os
import string


class UploadHelper():
    ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])  # allowed extensions for uploading images
    ORG_LOGO_FOLDER = 'org_logos'  # path for storing organization logos
    @staticmethod
    def allowed_image_file(filename):
        """
        method that checks if a filename corresponds to an allowed image file
        :param filename:
        :return: True if allowed image file, else False
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in UploadHelper.ALLOWED_IMAGE_EXTENSIONS

