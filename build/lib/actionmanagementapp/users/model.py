from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref

# create a class that inherits all the features of sql alchemy
# it will be inherited from the classes
Base = declarative_base()


class TimeStampMixin(object):
    """
    Mixin class with timestamp columns that should be added to every table
    """
    created_at = Column(DateTime, default=func.now())  # column that stores the time when a row was created
    mysql_engine = 'InnoDB',
    mysql_charset = 'utf8'


class UserCategory(Base, TimeStampMixin):
    """
    Class for storing the user categories data
    """
    __tablename__ = 'usercategory'

    # mapper code that creates columns
    id = Column(Integer, primary_key=True,  autoincrement=False)
    name = Column(String(200), nullable=False)
    # users = relationship('User', backref=backref("userCategory", cascade="save-update"))


class User(Base, TimeStampMixin):
    """
    Class for storing the user data
    """
    __tablename__ = 'user'

    # mapper code that creates columns
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    department = Column(String(200))
    phone = Column(String(15))
    mobile = Column(String(15))
    email = Column(String(50))
    enabled = Column(Boolean)
    userCategoryId = Column(Integer, ForeignKey('usercategory.id', onupdate='cascade'))
    userCategory = relationship('UserCategory', backref=backref('users'))
