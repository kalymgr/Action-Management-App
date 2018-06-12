from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from actionmanagementapp.utilities.db_models import TimeStampMixin

from actionmanagementapp.utilities import sql_alchemy_utils

Base = sql_alchemy_utils.Base


class LoggingRecord(Base, TimeStampMixin):
    """
    table in the database for storing the log records
    """
    __tablename__ = 'logrecords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(300))

