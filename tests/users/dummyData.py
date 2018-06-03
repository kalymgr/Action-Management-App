# -*- coding: utf-8 -*-
# encoding has been set as utf-8 for greek characters to appear properly
from flaskr.users.model import UserCategory, User

userCategory = {
    'id': 1,
    'name': u'Χρήστης'
}

userCategories = [
    {
        'id': 1,
        'name': u'Χρήστης'
    },
    {
        'id': 2,
        'name': u'Διαχειριστής'
    },
    {
        'id': 3,
        'name': u'Υπερδιαχειριστής'
    }
]

user = {
    'id': 1,
    'name': u'Μιχάλης Τσουγκράνης',
    'username': 'kalymgr',
    'department': u'Ειδικός Συνεργάτης',
    'categoryId': 3,
    'phone': '2243360158',
    'mobile': '6945xxxxxx',
    'email': 'mtsougranis@kalymnos.gr',
    'password': '1234',
    'enabled': True
}

users = [
    {
        'id': 1,
        'name': u'Μιχάλης Τσουγκράνης',
        'username': 'kalymgr',
        'department': u'Ειδικός Συνεργάτης',
        'categoryId': 3,
        'phone': '2243360158',
        'mobile': '6945xxxxxx',
        'email': 'mtsougranis@kalymnos.gr',
        'password': '1234',
        'enabled': True
    },
    {
        'id': 2,
        'name': u'Δημήτρης Ροδίτης',
        'username': 'dimitri',
        'department': u'Γραφείο Μηχανοργάνωσης',
        'categoryId': 3,
        'phone': '2243360158',
        'mobile': '6975xxxxxx',
        'email': 'dimitri@kalymnos.gr',
        'password': '4321',
        'enabled': True
    },
    {
        'id': 3,
        'name': u'Θανάσης Ρέβελας',
        'username': 'trevelas',
        'department': u'Τμήμα Προμηθειών',
        'categoryId': 2,
        'phone': '2243360150',
        'mobile': '6975xxxxxx',
        'email': 'revelas@kalymnos.gr',
        'password': '2222',
        'enabled': False
    },
]


def getCategoryNameById(categoryId):
    """
    Helper function that gets the category name by it's id
    :param categoryList:
    :param categoryId:
    :return:
    """
    for category in userCategories:
        if category['id'] == categoryId:
            return category['name']


def getUserWithCategoryDescription():
    """
    Function that get the used object, with the category description
    :return:
    """
    user['categoryDescr'] = getCategoryNameById(user['categoryId'])
    return user


def getUsersWithCategoryDescription():
    """
    Gets the user list, having added the category descriptions
    :param users:
    :param categories:
    :return:
    """
    for user in users:
        # set the category description
        user['categoryDescr'] = getCategoryNameById(user['categoryId'])
    return users


def insertDummyDataToMYSQL(session):
    """
    function that inserts dummy data to MySQL database
    :param session:
    :return:
    """

    # add some user categories, if there are none
    if session.query(UserCategory).count() == 0:
        userCategories = [
            UserCategory(id=1, name='User'),
            UserCategory(id=2, name='Administrator'),
            UserCategory(id=3, name='Super Administrator')
        ]
        session.add_all(userCategories)
        session.commit()

    # add some users, if there are none
    if session.query(User).count() == 0:
        users = [
            User(name='Michalis Tsougranis', username='kalymgr', userCategoryId=3),
            User(name='Dimitris Roditis', username='dimitri', userCategoryId=3),
            User(name='Thanasis Reveras', username='trevelas', userCategoryId=2),
            User(name='Michalis Bairamis', username='bairam', userCategoryId=1),
        ]
        session.add_all(users)
        session.commit()