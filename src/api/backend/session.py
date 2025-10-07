from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from typing import Iterator, AsyncIterator

from src.api.backend.settings import TimescaleSettings


def get_dsn(use_async=False):
    settings = TimescaleSettings()

    host = settings.POSTGRES_HOST
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    db = settings.POSTGRES_DB
    port = settings.POSTGRES_PORT

    async_driver = "" if not use_async else "+asyncpg"
    dns = f"postgresql{async_driver}://{user}:{password}@{host}:{port}/{db}"
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

async def create_async_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

SessionFactory = sessionmaker(
    bind=create_engine(get_dsn()),
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

AsyncSessionFactory = async_sessionmaker(
    bind=create_async_engine(get_dsn(use_async=True)),
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)