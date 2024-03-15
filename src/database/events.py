import logging

from fastapi import FastAPI

from src.core.config import Settings
from src.database.connection import DBConnection


async def connect_to_db(app: FastAPI, settings: Settings):
    # Initialize db connection class
    DBConnection.get_connection()


def close_db_connection(app: FastAPI):
    """
    Disconnect to the database when server stops running.
    """
    logger = logging.getLogger(__name__)
    try:
        DBConnection.get_connection().dispose()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")



