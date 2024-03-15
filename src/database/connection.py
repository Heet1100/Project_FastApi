import logging

from functools import wraps
from fastapi import Request
from sqlalchemy.exc import (
    OperationalError
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from src.exception.exception import DBTransactionError
from src.core.config import Settings




Base = declarative_base()
LOGGER = logging.getLogger(__name__)


class DBConnector:
    def __init__(self, config):
       self.config = config

    def get_rds_instance(self):
        rds_engine = create_engine(
            self.config.db_url(),
            pool_size=int(self.config.pool_size),
            max_overflow=int(self.config.max_overflow),
            pool_pre_ping=self.config.pool_pre_ping)
        return rds_engine


class DBConnection:
    connection = None

    @classmethod
    def get_connection(cls, new=False):
        """Creates return new Singleton database connection"""
        if new or not cls.connection:
            settings = Settings()
            cls.connection = DBConnector(settings).get_rds_instance()
        return cls.connection

    @classmethod
    def session_maker(cls):
        """Create sessionmaker instance"""
        SessionLocal = sessionmaker(cls.connection, autocommit=False, autoflush=False)
        return SessionLocal()

    @classmethod
    def raw_conn(cls):
        """Create raw fb connection"""
        raw_conn = cls.connection.connect()
        return raw_conn

    @classmethod
    def dispose_conn(cls):
        """Dispose rds engine instance"""
        cls.connection.dispose()


# Dependency
def db_conn_intializer():
    try:
        LOGGER.info("Re-initializing DB connection...")
        DBConnection.get_connection(new=True)
        LOGGER.info("DB connection re-initialized")
    except Exception as ex:
        LOGGER.error(f"Failed to reinitialized db connection got an error --> {str(ex)}")


def get_db():
    """provide db session to path operation functions"""
    db = DBConnection.session_maker()
    try:
        yield db
    finally:
        db.close()


def get_raw_db_conn():
    """provide engine connection to path operation to execute raw query"""
    connection = DBConnection.raw_conn()
    try:
        yield connection
    finally:
        connection.close()


def get_db_connection_for_worker():
    db = DBConnection.session_maker()
    return db


def transaction(func):
    """
    This function is a decorator that wraps the function it's applied to.
    It attempts to commit changes, and if there are any errors, it rolls back those changes.
    This helps avoid leaving behind partially-committed transactions when things go wrong.

    :param func: Pass the function that is being wrapped
    :return: The response of the function it decorates
    """
    @wraps(func)
    def inner(conn, *args, **kwargs):
        try:
            response = func(conn, *args, **kwargs)
            conn.commit()
            return response
        except OperationalError as ex:
            db_conn_intializer()
            LOGGER.exception(
                f"Something has gone wrong in DB! Got exception -->> {str(ex)}"
            )
            raise DBTransactionError()
    return inner