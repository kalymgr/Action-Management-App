from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


class TimeStampMixin(object):
    """
    Mixin class with timestamp columns that should be added to every table
    """
    created_at = Column(DateTime, default=func.now())  # column that stores the time when a row was created
    mysql_engine = 'InnoDB',
    mysql_charset = 'utf8'