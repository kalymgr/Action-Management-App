"""
Module for initializing the database.
It is based on the information given on http://flask.pocoo.org/docs/1.0/patterns/sqlalchemy/
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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


engine = createEngine('root', '', 'actionapplicationdb', 'localhost', 'utf8')
dbSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = dbSession.query_property()


def initDb():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()

    import actionmanagementapp.users.users_models
    import actionmanagementapp.org.org_models
    import actionmanagementapp.log.log_models
    import actionmanagementapp.actions.actions_models
    Base.metadata.create_all(bind=engine)

    # insert default organizational data
    actionmanagementapp.org.org_models.insertDefaultOrgData(dbSession)
    # insert default user data
    actionmanagementapp.users.users_models.insertDefaultUserData(dbSession)



