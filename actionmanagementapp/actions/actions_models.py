# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean, Float, Numeric, Text
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


class PartialBudget(Base, TimeStampMixin):
    """
    class that stores the partial budgets for each action
    """
    __tablename__ = 'partial_budget'
    id = Column(Integer, primary_key=True)
    actionId = Column(Integer, ForeignKey('action.id', onupdate='cascade'))
    # year of the partial budget
    year = Column(Integer, nullable=True)
    # amount of the partial budget
    amount = Column(Numeric(precision=15, scale=5), nullable=True)
    action = relationship('Action', backref=backref('partialBudgets'))


class ServiceAction(Base, TimeStampMixin):
    """
    Services involved in an action (many to many relationship)
    it has a composite primary key
    """
    __tablename__ = 'service_action'
    serviceId = Column(Integer, ForeignKey('service.id'), primary_key=True)
    actionId = Column(Integer, ForeignKey('action.id'), primary_key=True)


class FinancingSource(Base, TimeStampMixin):
    """
    stores the sources of financing
    """
    __tablename__ = 'financing_source'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    details = Column(Text, nullable=True)


class ActionFinancingSource(Base, TimeStampMixin):
    """
    stores the financing source per action. Many to many relationship.
    """
    __tablename__ = 'action_financingsource'
    actionId = Column(Integer, ForeignKey('action.id'), primary_key=True)
    financingSourceId = Column(Integer, ForeignKey('financing_source.id'), primary_key=True)
    # the code of the budget
    budgetCode = Column(String(50), nullable=True)
    # the amount for financing the action from the specific financing source
    amount = Column(Numeric(precision=15, scale=5), nullable=True)
    actionFinanced = relationship('Action', backref=backref('actionFinancingSources'),
                                         foreign_keys=[actionId])
    sourceOfFinance = relationship('FinancingSource', backref=backref('actionFinancingSources'),
                                   foreign_keys=[financingSourceId])


class Action(Base, TimeStampMixin):
    """
    class for storing actions data
    """
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    # service that is in charge of the specific action
    serviceInChargeId = Column(Integer, ForeignKey('service.id', onupdate='cascade'))
    serviceInCharge = relationship('Service', backref=backref('actionsInChargeOf'),
                                   foreign_keys=[serviceInChargeId])
    # service that will implement the action
    implementationServiceId = Column(Integer, ForeignKey('service.id', onupdate='cascade'))
    implementationService = relationship('Service', backref=backref('actionsImplemented'),
                                   foreign_keys=[implementationServiceId])
    # action category
    categoryId = Column(Integer, ForeignKey('action_category.id', onupdate='cascade'))
    # text field that show if the action is new or in progress (Νέα or Συνεχιζόμενη)
    newOrInProgress = Column(String(20), nullable=True)
    # action priority
    priority = Column(String(20), nullable=True)
    # the group that the action belongs to (Μέτρο)
    groupId = Column(Integer, ForeignKey('action_group.id', onupdate='cascade'))
    # the total budget of the action
    budget = Column(Numeric(precision=15, scale=5), nullable=True)
    # the total budget code of the action
    budgetCode = Column(String(50), nullable=True)
    # date that the action starts
    startDate = Column(DateTime)
    # date that the action ends
    endDate = Column(DateTime)
    # shows the status of the action eg in progress, cancelled, completed
    status = Column(String(50), nullable=True)
    # some details about the action
    details = Column(Text, nullable=True)
