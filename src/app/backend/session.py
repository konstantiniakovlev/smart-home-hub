from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.config import PostgresSettings


def get_dsn(settings):
    host = settings.POSTGRES_HOST
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    db = settings.POSTGRES_DB
    port = settings.POSTGRES_PORT

    dns = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return dns


def create_session() -> Iterator[Session]:
    session = SessionFactory()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


settings = PostgresSettings()

SessionFactory = sessionmaker(
    bind=create_engine(get_dsn(settings)),
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
