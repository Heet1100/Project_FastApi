import logging
import typing

from fastapi import FastAPI

from src.core.config import Settings
from src.database.events import close_db_connection, connect_to_db


def create_start_app_handler(app: FastAPI, settings: Settings) -> typing.Callable:
    """
    Handle the database connection when the server started.
    """

    async def start_app() -> None:
        await connect_to_db()

    logger = logging.getLogger(__name__)
    logger.info("Starting app")
    return start_app


def create_stop_app_handler(app: FastAPI) -> typing.Callable:
    """
    Handle the database connection  when the server stopped.
    """

    def stop_app() -> None:
        close_db_connection()

    logger = logging.getLogger(__name__)
    logger.info("Database Shut down")
    return stop_app