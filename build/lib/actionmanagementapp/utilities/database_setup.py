"""
Python module that sets up the database for the application
"""
# TODO: change passive_updates to True and setup referential integrity in the database (recommended by SQLAlchemy)
# https://docs.sqlalchemy.org/en/latest/orm/cascades.html#unitofwork-cascades
# TODO: read the webpage about relationships
# https://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from actionmanagementapp.users.UsersModels import Base, UserCategory
from actionmanagementapp.users.UsersModels import User
from werkzeug.security import generate_password_hash


def createEngine(db_UserName, db_Password, database_Name, db_Server, connection_Charset):
    """
    Function that creates and returns the db engine
    :param db_UserName:
    :param db_Password:
    :param database_Name:
    :param db_Server:
    :param connection_Charset:
    :return:
    """
    # configuration code that creates a new MYSQL database
    dbUserName = db_UserName
    dbPassword = db_Password
    databaseName = database_Name
    dbServer = db_Server
    connectionCharset = connection_Charset  # client character set for the connection
    engine = create_engine('mysql+pymysql://'+dbUserName+':'
                           +dbPassword+'@'+dbServer
                           +'/'+databaseName+"?charset="+connectionCharset,
                           pool_recycle=3600)
    return engine


def getSession(base, engine):
    """
    Function that returns the databaseSession
    :param base:
    :param engine:
    :return:
    """
    base.metadata.create_all(engine)
    base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    databaseSession = DBSession()
    return databaseSession


engine = createEngine('root', '', 'actionapplicationdb', 'localhost', 'utf8')
# go into the database and add the classes as new tables

def getProductionDatabaseSession():
    """
    Function that gets the database session
    :return:db session for the production database
    """
    engine = createEngine('root', '', 'actionapplicationdb', 'localhost', 'utf8')
    # go into the database and add the classes as new tables
    return getSession(Base, engine)


def getTestingDatabaseSession():
    """
    Function that gets the database session for test database
    :return: db session for the testing database
    """
    engine = createEngine('root', '', 'test_actionapplicationdb', 'localhost', 'utf8')
    # go into the database and add the classes as new tables
    dbSession = getSession(Base, engine)

    # create a dummy test category
    testCategory = dbSession.query(UserCategory)\
        .filter(UserCategory.id == 1).first()
    if testCategory is None:
        testCategory = UserCategory(id=1, name="test category")
        dbSession.add(testCategory)

    # create a dummy user called test (automated usage in some tests)
    testUser = dbSession.query(User).filter(User.username == 'test').first()
    if testUser is None:
        testUser = User(name="test user",
                        username="test",
                        password=generate_password_hash("test"),
                        userCategoryId=1)
        dbSession.add(testUser)

    dbSession.commit()  # save changes to the database
    return dbSession


