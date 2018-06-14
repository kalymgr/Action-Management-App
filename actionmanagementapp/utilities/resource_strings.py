# -*- coding: utf-8 -*-
"""
Contains the resource strings that are used in the application.
A prefix will be used; ERR for error, NOT for notice, INFO for informational.
If the resource strings are used in templates, TXT will be used for text and FRM for form content
"""


class AuthResourceStrings:
    """
    This class contains the constant strings used in the auth blueprint of the application
    """
    # -- controller/routing functions text
    # INFO elements
    INFO_LOGIN_ATTEMPT = u' Προσπάθεια σύνδεσης. '
    INFO_SUCCESSSFUL_LOGIN = INFO_LOGIN_ATTEMPT+u' Επιτυχής σύνδεση για τον/την χρήστη %s.'

    # ERROR elements
    ERROR_WRONG_USERNAME = u' Λάθος όνομα χρήστη. '
    ERROR_WRONG_USERNAME_2 = INFO_LOGIN_ATTEMPT+ERROR_WRONG_USERNAME
    ERROR_WRONG_PASSWORD = u' Λάθος κωδικός χρήστη. '
    ERROR_WRONG_PASSWORD_2 = INFO_LOGIN_ATTEMPT+ERROR_WRONG_PASSWORD
    ERROR_USER_NOT_ACTIVATED = u' Ο χρήστης δεν έχει ενεργοποιηθεί. '
    ERROR_USER_NOT_ACTIVATED_2 = INFO_LOGIN_ATTEMPT+ERROR_USER_NOT_ACTIVATED

    # -- form elements
    FRM_USERNAME = u'Όνομα χρήστη'
    FRM_PASSWORD = u'Κωδικός'
    FRM_LOGIN  = u'Σύνδεση'

    # -- text elements
    TXT_LOGIN = u'Σύνδεση'
    TXT_LOGOUT = u'Αποσύνδεση'


class UsersResourceString:
    """
    This class contains the constant strings used in the users blueprint of the application
    """
    # -- controller/routing functions text
    # INFO elements
    INFO_USER_ADDED = u' Ο χρήστης %s έχει προστεθεί. '
    INFO_USER_DELETED = u' Ο χρήστης %s έχει διαγραφεί. '
    INFO_USER_UPDATED = u' Τα στοιχεία για τον χρήστη %s έχουν ενημερωθεί. '
    INFO_USER_PASSWORD_CHANGED = u' Ο κωδικός για το χρήστη %s έχει αλλάξει. '
    INFO_USER_CATEGORY_ADDED = u' Η νέα κατηγορία έχει προστεθεί. '
    INFO_USER_CATEGORY_ID_EXISTS = u' Ο κωδικός κατηγορίας υπάρχει ήδη. '
    INFO_USER_CATEGORY_UPDATED = u' Τα στοιχεία της κατηγορίας έχουν ενημερωθεί. '
    INFO_USER_CATEGORY_DELETED = u' Η κατηγορία έχει διαγραφεί. '

    # ERROR elements
    ERROR_NON_EXISTING_USER = u' Ο χρήστης δεν υπάρχει. '
    ERROR_NAME_NOT_ENTERED = u' Δε δόθηκε το όνομα. '
    ERROR_USERNAME_NOT_ENTERED = u' Δε δόθηκε το όνομα χρήστη. '
    ERROR_USER_CATEGORY_NOT_ENTERED = u' Δε δόθηκε κατηγορία χρήστη. '
    ERROR_EMPTY_USER_PASSWORD = u' Κενός κωδικός χρήστη.'
    ERROR_PASSWORDS_DO_NOT_MATCH = u' Δεν ταιριάζουν οι κωδικοί. '
    ERROR_EMAIL_ADDRESS_NOT_ENTERED = u' Δε δόθηκε διεύθυνση email. '
    ERROR_USER_CATEGORY_ID_NOT_ENTERED = u' Δε συμπληρώθηκε κωδικός κατηγορίας. '
    ERROR_USER_CATEGORY_NAME_NOT_ENTERED = u' Δε συμπληρώθηκε όνομα κατηγορίας. '
    ERROR_USER_NEW_PASSWORD_BLANK = u' Ο καινούριος κωδικός δε μπορεί να είναι κενός. '
    ERROR_USER_PASSWORDS_DO_NOT_MATCH = u' Οι δύο κωδικοί δεν ταιριάζουν. '

    # -- form elements

    # -- text elements

class GeneralResourceStrings:
    pass