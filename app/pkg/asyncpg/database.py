from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.internal.config import DATABASE_URL
from contextlib import asynccontextmanager


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession
)

Base = declarative_base()


@asynccontextmanager
async def async_session():
    async with SessionLocal() as sess:
        yield sess
