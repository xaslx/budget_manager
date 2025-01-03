from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import PostgresConfig


def new_session_maker(psql_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    database_uri: str = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
        user=psql_config.user,
        password=psql_config.password,
        host=psql_config.host,
        port=psql_config.port,
        database=psql_config.database,
    )

    engine: AsyncEngine = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)