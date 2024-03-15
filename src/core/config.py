from dotenv import load_dotenv
from pathlib import Path
import os

from pydantic import BaseSettings
from sqlalchemy.sql.functions import user

dir_path = (Path(__file__) / ".." / ".." / "..").resolve()
env_path = dir_path / "dev.env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    App_title: str = os.getenv("APP_TITLE")
    APP_Version: str = os.getenv("APP_VERSION")
    OTEL_SERVICE_NAME: str = os.getenv("OTEL_SERVICE_NAME")
    HONEYCOMB_API_KEY: str = os.getenv("HONEYCOMB_API_KEY")
    user: str = os.getenv("user")
    password: str = os.getenv("password")
    server: str = os.getenv("server")
    data: str = os.getenv("data")
    host: str = os.getenv("host")
    port: int = os.getenv("port")
    pool_size :int = os.getenv("POOL_SIZE")
    max_overflow:int = os.getenv("MAX_OVERFLOW")
    pool_pre_ping:bool= os.getenv("POOL_PRE_PING")


s = Settings()
def db_url():
    return f"postgresql://{s.user}:{s.password}@{s.server}/{s.data}"
