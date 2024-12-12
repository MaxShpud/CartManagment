from typing import Any

from pydantic import PostgresDsn, BaseModel
from pydantic_settings import BaseSettings

from app.LOGGING import LoggingConfig


class DBConfig(BaseModel):
    app_name: str = "template-app"
    dsn: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5434/postgres"
    #schema_name: str = "content"
    pool_size: int = 10
    timezone: str = "utc"
    max_overflow: int = 10
    pool_pre_ping: bool = True
    connection_timeout: int = 30
    command_timeout: int = 5
    server_settings: dict[str, Any] = {}
    connect_args: dict[str, Any] = {}
    debug: bool = False


class Config(BaseSettings):
    class Config:
        env_file = "../../.env.default"
        env_nested_delimiter = "__"

    DB: DBConfig = DBConfig()
    LOGGING: LoggingConfig = LoggingConfig()
