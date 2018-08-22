# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean, Float, Numeric
from sqlalchemy.orm import relationship, sessionmaker, backref
# create a class that inherits all the features of sql alchemy
# it will be inherited from the classes
from actionmanagementapp.utilities.db_models import TimeStampMixin
from actionmanagementapp.utilities.database_init import Base


class ActionCategory(Base, TimeStampMixin):
    """
    class for storing the action categories
    """
    __tablename__ = 'action_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


class ActionGroup(Base, TimeStampMixin):
    """
    class for storing the action categories
    """
    __tablename__ = 'action_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


class Action(Base, TimeStampMixin):
    """
    class for storing actions data
    """
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    # service that is in charge of the specific action
    serviceInCharge = Column(Integer, ForeignKey('service.id', onupdate='cascade'))
    # service that will implement the action
    implementationService = Column(Integer, ForeignKey('service.id', onupdate='cascade'))
    actionCategory = Column(Integer, ForeignKey('action_category.id', onupdate='cascade'))
    # text field that show if the action is new or in progress (Νέα or Συνεχιζόμενη)
    newOrInProgress = Column(String(20), nullable=True)
    # action priority
    priority = Column(String(20), nullable=True)
    # the group that the action belongs to (Μέτρο)
    actionGroup = Column(Integer, ForeignKey('action_group.id', onupdate='cascade'))
    actionBudget = Column(Numeric(precision=(5, 4)), nullable=True)
