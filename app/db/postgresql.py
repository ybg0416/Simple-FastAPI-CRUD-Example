from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI.unicode_string(), echo=settings.POSTGRES_ECHO
)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=settings.EXPIRE_ON_COMMIT
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncSession:
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
