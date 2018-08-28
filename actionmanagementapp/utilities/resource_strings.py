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

    # -- ERROR elements
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
    FRM_USER_ID = u'Κωδ. χρήστη'
    FRM_FULL_NAME = u'Όνοματεπώνυμο'
    FRM_USERNAME = u'Όνομα χρήστη'
    FRM_DEPARTMENT = u'Υπηρεσία'
    FRM_USER_CATEGORY = u'Κατηγορία'
    FRM_PHONE = u'Τηλ'
    FRM_MOBILE = u'Κινητό'
    FRM_EMAIL = u'Email'
    FRM_ENABLED = u'Ενεργός'
    FRM_OLD_PASSWORD = u'Παλιός κωδικός'
    FRM_NEW_PASSWORD = u'Νέος Κωδικός'
    FRM_CONFIRM_NEW_PASSWORD = u'Επιβεβαίωση νέου κωδικού'
    FRM_USER_CATEGORY_ID = u'Κωδ.'
    FRM_USER_CATEGORY_NAME = u'Όνομα'
    FRM_CHANGE_PASSWORD = u'Αλλαγή κωδικού'
    FRM_ADD_CATEGORY = u'Προσθήκη κατηγορίας'
    FRM_ADD_USER = u'Προσθήκη χρήστη'
    FRM_USER_CATEGORIES = u'Κατηγορίες χρηστών'
    FRM_USER_AVATAR = u'Εικονίδιο χρήστη'
    FRM_PRINT_USERS = u'Εκτύπωση λίστας χρηστών'

    # -- text elements
    TXT_ADD_USER = u'Προσθήκη χρήστη'
    TXT_BACK_TO_USER_LIST = u'Επιστροφή στη λίστα χρηστών'
    TXT_ADD_USER_CATEGORY = u'Προσθήκη κατηγορίας χρήστη'
    TXT_CHANGE_USER_PASSWORD_TITLE = u'Αλλαγή κωδικού χρήστη'
    TXT_CHANGE_USER_PASSWORD = u'Αλλαγή κωδικού για το χρήστη'
    TXT_DELETE_USER = u'Διαγραφή χρήστη'
    TXT_CONFIRM_USER_DELETE = u'Είστε σίγουρος/η ότι θέλετε να διαγράψετε το/τη χρήστη %s ;'
    TXT_DELETE_USER_CATEGORY = u'Διαγραφή κατηγορίας χρήστη'
    TXT_CONFIRM_USER_CATEGORY_DELETE = u'Είστε σίγουρος/η ότι θέλετε να διαγράψετε την κατηγορία %s;'
    TXT_BACK_TO_CATEGORY_LIST = u'Πίσω στη Λίστα κατηγοριών'
    TXT_EDIT_USER = u'Επεξεργασία χρήστη'
    TXT_EDIT_USER_CATEGORY = u'Επεξεργασία κατηγορίας χρήστη'
    TXT_USER_CATEGORIES = u'Κατηγορίες χρηστών'
    TXT_USER_INFO = u'Πληροφορίες χρήστη'
    TXT_USER_LIST = u'Λίστα χρηστών'
    TXT_FULL_NAME = u'Όνοματεπώνυμο'
    TXT_USERNAME = u'Όνομα χρήστη'
    TXT_EMAIL = u'Email'
    TXT_USER_CATEGORY = u'Κατηγορία'
    TXT_USER_CATEGORY_NAME = u'Όνομα'


class ActionResourceStrings:
    """
    Strings related to managing actions
    """
    # -- ERROR elements
    # -- FORM elements
    FRM_ADD_ACTION = u'Προσθήκη δράσης'
    FRM_PRINT_ACTIONS = u'Εκτύπωση λίστας δράσεων'
    FRM_ACTION_ID = u'Κωδ.'
    FRM_ACTION_BUDGET_CODE = u'Κωδ Προϋπολ'
    FRM_ACTION_NAME = u'Τίτλος δράσης'
    FRM_ACTION_CATEGORY = u'Κατηγορία'
    FRM_ACTION_NEW_OR_IN_PROGRESS = u'Νέα ή Συνεχιζόμενη'
    FRM_ACTION_SERVICE_IN_CHARGE = u'Αρμόδια υπηρεσία'
    FRM_ACTION_IMPLEMENTATION_SERVICE = u'Υπηρεσία υλοποίησης'
    FRM_ACTION_PRIORITY = u'Προτεραιότητα'
    FRM_ACTION_GROUP = u'Μέτρο'
    FRM_ACTION_STATUS = u'Κατάσταση'
    FRM_ACTION_START_DATE = u'Ημνία Έναρξης'
    FRM_ACTION_END_DATE = u'Ημνία Λήξης'

    # -- TEXT elements
    TXT_ACTION_LIST_TITLE = u'Λίστα δράσεων'
    TXT_NO_ACTIONS = u'Δεν υπάρχουν καταχωρημένες δράσεις'
    TXT_ACTION_TITLE = u'Τίτλος Δράσης'
    TXT_ACTION_SERVICE_INCHARGE = u'Υπεύθυνη Υπηρεσία'
    TXT_ACTION_BUDGET = u'Προϋπολογισμός'
    TXT_ADD_ACTION_TITLE = u'Προσθήκη νέας δράσης'
    TXT_EDIT_ACTION_TITLE = u'Επεξεργασία δράσης'
    TXT_BACK_TO_ACTION_LIST = u'Πίσω στη λίστα με τις δράσεις'

class OrganizationResourceStrings:
    """
    Strings related to the management of the organization
    """
    # -- ERROR elements
    ERR_ORGANIZATION_EMPTY_NAME = u'Δε δόθηκε όνομα οργανισμού.'
    ERR_ORGANIZATION_EMPTY_CEO = u' Δε δόθηκαν στοιχεία της διοίκησης.'
    ERR_SERVICE_EMPTY_NAME = u' Δε δόθηκε όνομα υπηρεσίας. '
    ERR_SERVICE_EMPTY_TYPE = u' Δε δόθηκε τύπος υπηρεσίας. '
    ERR_CHILDREN_ORGANIZATIONS = u' Σε αυτό το νομικό πρόσωπο υπάγονται άλλα νομικά πρόσωπα. Δε μπορεί να διαγραφεί. '
    ERR_CHILDREN_SERVICES = u' Σε αυτή την υπηρεσία υπάγονται άλλες υπηρεσίες. Δε μπορεί να διαγραφεί. '
    ERR_SERVICE_EMPLOYEES = u' Υπάρχουν υπάλληλοι καταχωρημένοι σε αυτή την υπηρεσία. Δε μπορεί να διαγραφεί. '
    ERR_ORGANIZATION_SERVICES = u' Υπάρχουν υπηρεσίες σε αυτό το νομικό πρόσωπο. Δε μπορεί να διαγραφεί. '

    # -- FORM elements
    FRM_ORGANIZATION_NAME = u'Όνομα'
    FRM_ORGANIZATION_TYPE = u'Τύπος'
    FRM_ORGANIZATION_CEO = u'Νόμιμος εκπρόσωπος'
    FRM_PARENT_ORGANIZATION = u'Υπάγεται σε'
    FRM_ORGANIZATION_ADDRESS = u'Διεύθυνση'
    FRM_ORGANIZATION_PHONE = u'Τηλέφωνο'
    FRM_ORGANIZATION_EMAIL = u'Διεύθυνση Email'
    FRM_ORGANIZATION_LOGO = u'Λογότυπο'
    FRM_ORGANIZATION_IRSNO = u'ΑΦΜ'
    FRM_ADD_ORGANIZATION = u'Προσθήκη νομικού προσώπου'
    FRM_ADD_SERVICE = u'Προσθήκη υπηρεσίας'
    FRM_SERVICE_ID = u'Κωδ. Υπηρεσίας'
    FRM_SERVICE_NAME = u'Όνομα'
    FRM_SERVICE_ADDRESS = u'Διεύθυνση'
    FRM_SERVICE_CHIEF = u'Προϊστάμενος'
    FRM_SERVICE_PHONE = u'Τηλέφωνο'
    FRM_SERVICE_EMAIL = u'Email'
    FRM_PARENT_SERVICE = u'Ανήκει σε'
    FRM_NO_SERVICE = u'Καμία υπηρεσία '
    FRM_ORGANIZATION = u'Νομικό πρόσωπο'
    FRM_SERVICE_TYPE = u'Τύπος'
    FRM_PRINT_ORGANIZATIONS = u'Εκτύπωση λίστας νομικών προσώπων'
    FRM_PRINT_SERVICES = u'Εκτύπωση λίστας υπηρεσιών'

    # -- TEXT elements
    TXT_NO_ORGANIZATIONS = u' Δεν υπάρχουν καταχωρημένα νομικά πρόσωπα. '
    TXT_ORGANIZATION_LIST_TITLE = u'Λίστα νομικών προσώπων'
    TXT_ORGANIZATION_SAVED = u' Το νομικό πρόσωπο έχει αποθηκευτεί. '
    TXT_ADD_ORGANIZATION_TITLE = u'Προσθήκη νέου νομικού προσώπου'
    TXT_EDIT_ORGANIZATION_TITLE = u'Επεξεργασία νομικού προσώπου'
    TXT_BACK_TO_ORGANIZATION_LIST = u'Πίσω στη λίστα με τα νομικά πρόσωπα'
    TXT_ORGANIZATION_DELETED = u'Το νομικό πρόσωπο έχει διαγραφεί.'
    TXT_DELETE_ORGANIZATION_TITLE = u'Επεξεργασία νέου νομικού προσώπου'
    TXT_CONFIRM_DELETE_ORGANIZATION = u'Είστε σίγουροι ότι θέλετε να διαγράψετε το νομικό πρόσωπο %s;'
    TXT_ORGANIZATION_NAME = u'Όνομα Νομικού Προσώπου'
    TXT_ORGANIZATION_ADDRESS = u'Διεύθυνση'
    TXT_ORGANIZATION_CEO = u'Νόμιμος Εκπρόσωπος'
    TXT_SERVICES_TITLE = u'Λίστα υπηρεσιών νομικών προσώπων'
    TXT_NO_SERVICES = u'Δεν υπάρχουν καταχωρημένες υπηρεσίες'
    TXT_SERVICE_NAME = u'Όνομα Υπηρεσίας'
    TXT_EDIT_SERVICE_TITLE = u'Επεξεργασία υπηρεσίας'
    TXT_BACK_TO_SERVICE_LIST = u'Πίσω στη λίστα με τις υπηρεσίες'
    TXT_SERVICE_SAVED = u'Η υπηρεσία έχει αποθηκευτεί.'
    TXT_ADD_SERVICE_TITLE = u'Προσθήκη υπηρεσίας'
    TXT_SERVICE_DELETED = u'Η υπηρεσία έχει διαγραφεί.'
    TXT_DELETE_SERVICE_TITLE = u'Διαγραφή υπηρεσίας'
    TXT_CONFIRM_DELETE_SERVICE = u'Είστε σίγουροι ότι θέλετε να διαγράψετε την υπηρεσία %s;'



class GeneralResourceStrings:
    """
    class with resource strings for generic use
    """
    # -- Form elements
    FRM_SAVE = u'OK'
    FRM_EDIT = u'Επεξεργασία'
    FRM_DELETE = u'Διαγραφή'
    FRM_VIEW = u'Προβολή'

    # -- TEXT elements
    TXT_OPERATIONS = u'Λειτουργίες'


    # -- Error elements
    ERR_PROBLEM_UPLOAD_FILE = u'Πρόβλημα με τη μεταφόρτωση του αρχείου'

class MenuResourceStrings:
    """
    class with resource strings used by the menus
    """

    # -- TXT elements
    TXT_MENU_USERS = u'Χρήστες'
    TXT_MENU_ORGANIZATIONS = u'Νομικά πρόσωπα'
    TXT_MENU_SERVICES = u'Υπηρεσίες'
    TXT_MENU_ACTIONS = u'Δράσεις'


class DropdownLists:
    """
    class with values used in dropdown lists. This method is used to avoid
    creating unnecessary tables in the database
    """
    newOrInProgress = [u'Νέα', u'Συνεχιζόμενη']
    priority = [u'(1) Υψηλή', u'(2) Μεσαία', u'(3) Χαμηλή']

