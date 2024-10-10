from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app import config


class Base(DeclarativeBase):
    pass


engine = create_async_engine(config.database.dsn.raw_dsn, echo=True)
ASYNC_SESSION_MAKER = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
