# -*- coding: utf8 -*-
# The encoding has been set to UTF8 to support Greek
from flaskr.users.model import UserCategory, User
from flaskr.utilities.database_setup import databaseSession
from tests.users import dummyData

# insert some dummy data in the database, in case it is empty
dummyData.insertDummyDataToMYSQL(databaseSession)

# update the user category id
def updateCategoryId(session, oldId, newId):
    """
    Function that updates a user Category Id
    :param session:
    :param oldId:
    :param newId:
    :return:
    """
    cat = session.query(UserCategory).filter(UserCategory.id == oldId).one()
    cat.id = newId
    session.add(cat)
    session.commit()


# updateCategoryId(session, 3, 23)  # execute the function

newUser = User(name=u"Ελληνάρας", username="ellinaras", userCategoryId=1)
databaseSession.add(newUser)
databaseSession.commit()


