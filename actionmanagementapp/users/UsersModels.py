from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean

from sqlalchemy.orm import relationship, sessionmaker, backref


# create a class that inherits all the features of sql alchemy
# it will be inherited from the classes
from actionmanagementapp.utilities.DbModels import TimeStampMixin
from actionmanagementapp.utilities import SQLALchemyUtils

Base = SQLALchemyUtils.Base


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
    department = Column(String(200))
    phone = Column(String(15))
    mobile = Column(String(15))
    email = Column(String(50), unique=True, nullable=False)
    enabled = Column(Boolean)
    userCategoryId = Column(Integer, ForeignKey('usercategory.id', onupdate='cascade'), nullable=False)
    userCategory = relationship('UserCategory', backref=backref('users'))
