from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Iterator

from backend.settings import TimescaleSettings


def get_dsn():
    settings = TimescaleSettings()
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


SessionFactory = sessionmaker(
    bind=create_engine(get_dsn(), connect_args={"options": "-c timezone=utc"}),
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
