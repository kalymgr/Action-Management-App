"""
Module that handles the CRUD operations related to user management
"""
from flaskr.utilities.database_setup import databaseSession
from flaskr.users.model import User


class UserController():
    """
    Controller Class for managing users and their categories
    """

    @staticmethod
    def getAllUsers(session):
        """
        Method that returns all users
        :return:
        """

        users = session.query(User).all()
        return users

