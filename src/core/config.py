import json
import logging
import os
from typing import Any, Dict, List

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseSettings

from src.core.custom_logging import CustomizeLogger
from pathlib import Path

from service_version import version

LOGGER = logging.getLogger(__name__)
config_path=Path(__file__).with_name("logconfig.json")


class Settings(BaseSettings):
    """
    get env variables
    """

    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    docs_url: str = "/docs"
    title: str = "Dataset Service Dashboard"
    version: str = version["tool"]["poetry"]["version"]

    api_prefix: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    database: str
    db_secret: str

    dataset_honeycomb_dataset_write_key: str = None
    dataset_honeycomb_dataset_name: str = None

    debug: bool = False
    max_overflow: int
    pool_size: int
    pool_pre_ping: bool

    service: str

    @property
    def backend_cors_origins(self) -> List[str]:
        return [x.strip() for x in self.backend_cors_origins_str.split(",") if x]

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.api_prefix + self.docs_url,
            "openapi_url": self.api_prefix + self.openapi_url,
            "redoc_url": self.api_prefix + self.redoc_url,
            "title": self.title,
            "version": self.version,
        }


    def db_url(self) -> str :
        SQLALCHEMY_DATABASE_URL = (
            "postgresql://"
            + self.db_user
            + ":"
            + self.db_pass
            + "@"
            + self.db_host
            + ":"
            + self.db_port
            + "/"
            + self.database
        )
        return SQLALCHEMY_DATABASE_URL


    def configure_logging(self) -> None:  # noqa
        CustomizeLogger.make_logger(config_path)

    class Config:
        validate_assignment = True
        env_file = "dev.env"
        env_file_encoding = "utf-8"


def get_secret_value(secret_name):
    aws_secrets = boto3.client("secretsmanager", os.environ.get("REGION_NAME"))
    try:
        res = aws_secrets.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        LOGGER.exception(f"Error occurs during fetching DB secrets --> {str(e)}")
    else:
        secret_dict = json.loads(res["SecretString"])
        return secret_dict
    return None


def settings():
    app_settings = Settings()
    db_cred = get_secret_value(app_settings.db_secret)
    if db_cred:
        app_settings.db_user = db_cred.get("username")
        app_settings.db_pass = db_cred.get("password")
        app_settings.db_host = db_cred.get("host")
        app_settings.db_port = db_cred.get("port")
        app_settings.database = db_cred.get("dbname")
    return app_settings
