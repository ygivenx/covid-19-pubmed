"""
Handle database connections

"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class SQLAlchemyConnection:
    """
    A generic postgres connection class

    >> with SQLAlchemyConnection as conn:
    >>    conn.session.query(User.name).all()

    """
    def __init__(self, connection_string=os.environ["CONNECTION_STRING"]):
        """
        Initialize the connection

        """
        self.connection_string = connection_string
        self.engine = None
        self.connection = None
        self.session = None

    def __enter__(self):
        """
        Create connection on entry

        :return:
        """
        self.engine = create_engine(self.connection_string)
        self.connection = self.engine.connect()
        _session = sessionmaker(self.engine)
        self.session = _session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handle exit

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if exc_tb is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
        self.connection.close()


def db_connection(func):
    """
    Decorator to use db_connection

    >> @db_connection
    >> def list_users(conn):
    >>   conn.session.query(models.User.name).all()

    :param func:
    :return:
    """
    def with_connection_(*args, **kwargs):
        with SQLAlchemyConnection() as conn:
            res = func(conn, *args, **kwargs)

        return res

    return with_connection_

