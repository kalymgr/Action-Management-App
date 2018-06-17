# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship, sessionmaker, backref
# create a class that inherits all the features of sql alchemy
# it will be inherited from the classes
from actionmanagementapp.utilities.db_models import TimeStampMixin
from actionmanagementapp.utilities import sql_alchemy_utils

Base = sql_alchemy_utils.Base

class Organization(Base, TimeStampMixin):
    """
    class for storing the organization basic info eg Municipality
    """
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(150), nullable=False)
    type = Column(Integer)
    address = Column(String(150))
    ceo = Column(String(50), nullable=False)
    phone = Column(String(50))
    email = Column(String(50))
    parentOrganizationId = Column(Integer, ForeignKey('organization.id', onupdate='cascade'))
    children = relationship("Organization",
                            backref=backref('parent', remote_side=[id]))


class Service (Base, TimeStampMixin):
    """
    class for storing the organization services eg Accounting, Tourism Office
    """
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    address = Column(String(150))
    chief = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    organizationTypeId = Column(Integer, ForeignKey('organizationtype.id', onupdate='cascade'))
    # relationship with other services
    parentServiceId = Column(Integer, ForeignKey('service.id', onupdate='cascade'))
    children = relationship("Service",
                            backref=backref('parent', remote_side=[id]))
    # relationship with organization
    organizationId = Column(Integer, ForeignKey('organization.id', onupdate='cascade'), nullable=False)
    organization = relationship('Organization', backref=backref('services'))
    test = Column(Integer)


class OrganizationType(Base, TimeStampMixin):
    """
    class for storing the type of the organization e.g. OTA A bathmou, OTA b bathmou
    """
    __tablename__ = 'organizationtype'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


def insertDefaultOrgData(dbSession):
    """
    Function that inserts default organization data in the application
    :param dbSession:
    :return:
    """
    # insert default organization types
    if dbSession.query(OrganizationType).count() == 0:  # if the organizationtype table is empty
        # create the list with organization types
        defaultOrganizationTypes = [
            (1, u'ΟΤΑ Α Βαθμού'),
            (2, u'ΟΤΑ Β Βαθμού'),
            (3, u'ΝΠΔΔ'),
            (4, u'ΝΠΙΔ'),
            (5, u'Δημοτική Επιχείρηση'),
            (6, u'Ανώνυμη Εταιρεία')
        ]
        # insert them in the database
        for orgType in defaultOrganizationTypes:
            dbSession.add(OrganizationType(id=orgType[0], name=orgType[1]))
        dbSession.commit()