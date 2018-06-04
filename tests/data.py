"""
Module for inserting dummy data in the database
"""

from actionmanagementapp.users.model import UserCategory, User


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
            User(name='Michalis Tsougranis', username='kalymgr', userCategoryId=3, password=''),
            User(name='Dimitris Roditis', username='dimitri', userCategoryId=3, password=''),
            User(name='Thanasis Reveras', username='trevelas', userCategoryId=2, password=''),
            User(name='Michalis Bairamis', username='bairam', userCategoryId=1, password=''),
        ]
        session.add_all(users)
        session.commit()