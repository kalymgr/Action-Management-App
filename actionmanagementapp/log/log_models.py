# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from actionmanagementapp.utilities.db_models import TimeStampMixin

from actionmanagementapp.utilities import sql_alchemy_utils

# Base = sql_alchemy_utils.Base
from actionmanagementapp.utilities.database_init import Base


class LoggingRecord(Base, TimeStampMixin):
    """
    table in the database for storing the log records
    """
    __tablename__ = 'logrecords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(300))

