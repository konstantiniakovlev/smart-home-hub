from pydantic_settings import BaseSettings
from typing import Optional


class TimescaleSettings(BaseSettings):
    """BaseSettings match existing environmental variable values
    with declared constants in this class.
    If environmental variables are not exported, they can be read from
    an .env file by adding the following lines:
    class Config:
        env_file = ".env"
    """
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: Optional[str] = "smart-home-timescaledb"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: int = 5432

    # class Config:
    #     env_file = ".env"


class ApiSettings(BaseSettings):
    VERSION: str = "0.0.3"
