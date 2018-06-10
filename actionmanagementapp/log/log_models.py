from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from actionmanagementapp.utilities.DbModels import TimeStampMixin

from actionmanagementapp.utilities import SQLALchemyUtils

Base = SQLALchemyUtils.Base


class LoggingRecord(Base, TimeStampMixin):
    """
    table in the database for storing the log records
    """
    __tablename__ = 'logrecords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(300))

