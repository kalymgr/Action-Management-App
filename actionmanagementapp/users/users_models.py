# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship, sessionmaker, backref
# create a class that inherits all the features of sql alchemy
# it will be inherited from the classes
from werkzeug.security import generate_password_hash

from actionmanagementapp.utilities.db_models import TimeStampMixin
from actionmanagementapp.utilities import sql_alchemy_utils

# Base = sql_alchemy_utils.Base
from actionmanagementapp.utilities.database_init import Base


# -- Database tables
class UserCategory(Base, TimeStampMixin):
    """
    Class for storing the user categories data
    """
    __tablename__ = 'usercategory'

    # mapper code that creates columns
    id = Column(Integer, primary_key=True,  autoincrement=False)
    name = Column(String(200), nullable=False, unique=True)
    # users = relationship('User', backref=backref("userCategory", cascade="save-update"))


class User(Base, TimeStampMixin):
    """
    Class for storing the user data
    """
    __tablename__ = 'user'

    # mapper code that creates columns
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    serviceId = Column(Integer, ForeignKey('service.id', onupdate='cascade'), nullable=False)
    service = relationship('Service', backref=backref('employees'))
    phone = Column(String(15))
    mobile = Column(String(15))
    email = Column(String(50), unique=True, nullable=False)
    enabled = Column(Boolean)
    userCategoryId = Column(Integer, ForeignKey('usercategory.id', onupdate='cascade'), nullable=False)
    userCategory = relationship('UserCategory', backref=backref('users'))


def insertDefaultUserData(DBSession):
    """
    Function tha inserts default user data in the database

    :param dbSession:
    :return:
    """
    dbSession = DBSession()
    # -- insert default user category data
    if dbSession.query(UserCategory).count() == 0:  # if the user categories table is empty
        # insert some default values in the database
        defaultUserCategories = [
            (1, u'Χρήστης'),
            (2, u'Διαχειριστής'),
            (3, u'Υπερδιαχειριστής'),
        ]
        for uc in defaultUserCategories:
            dbSession.add(UserCategory(id=uc[0], name=uc[1]))


    # -- insert default user data
    if dbSession.query(User).count() == 0:  # case the default user does not exist
        # create the user
        defaultUser = User(
            id=1,
            name=u'Μιχάλης Τσουγκράνης',
            username='kalymgr',
            email='mtsougranis@gmail.com',
            password=generate_password_hash('kalymgr'),
            userCategoryId=3,
            enabled=True
        )
        # insert the user in the database
        dbSession.add(defaultUser)
    dbSession.commit()
