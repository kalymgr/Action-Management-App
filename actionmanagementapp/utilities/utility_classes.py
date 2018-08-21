"""
This module contains some utility classes, used for various purposes
"""
import os
import string
from cStringIO import StringIO

from xhtml2pdf import pisa
# https://xhtml2pdf.readthedocs.io/en/latest/usage.html

import logging
pisa.showLogging()  # debug

class UploadHelper():
    """
    Class with helper methods related to uploads
    """
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


class Pdfs():
    """
    Class with helper methods concerning the creation of pdf
    """

    @staticmethod
    def createPdf(pdfData):
        """
        method that creates a pdf from a string
        :param pdfData: string pdf data
        :return: the pdf file
        """
        # create an empty StringIO object
        pdf = StringIO()
        pisa.CreatePDF(StringIO(pdfData.encode('utf-8')), pdf)
        return pdf
