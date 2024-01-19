import os
from typing import Optional

from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    NAME: str
    VERSION: str
    PORT: int
    SUMMARY: Optional[str] = None
    DESCRIPTION: Optional[str] = None

    class Config:
        env_file = os.path.join("config", ".api.env")


class PostgresSettings(BaseSettings):
    POSTGRES_NAME: Optional[str] = "smart-home-postgres"
    POSTGRES_HOST: Optional[str] = "host.docker.internal"
    POSTGRES_USER: Optional[str] = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: Optional[str] = "postgres"
    POSTGRES_PORT: Optional[int] = 5432

    class Config:
        env_file = os.path.join("config", ".postgres.env")


class TimescaleSettings(BaseSettings):
    POSTGRES_NAME: Optional[str] = "smart-home-timescaledb"
    POSTGRES_HOST: Optional[str] = "host.docker.internal"
    POSTGRES_USER: Optional[str] = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: Optional[str] = "postgres"
    POSTGRES_PORT: Optional[int] = 5431

    class Config:
        env_file = os.path.join("config", ".timescaledb.env")
