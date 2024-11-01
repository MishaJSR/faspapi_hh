from typing import AsyncGenerator

from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from base_settings import base_settings

Base = declarative_base()

metadata = MetaData()

DATABASE_URL = base_settings.get_database_url()

engine = create_async_engine(DATABASE_URL,
                             poolclass=NullPool,
                             query_cache_size=1200,
                             future=True,
                             echo=False,
                             )
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

