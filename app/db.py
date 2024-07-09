from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings

DATABASE_URL = settings.get_database_url()

if settings.MODE == "DEV":
    DATABASE_PARAMS = {}
else:
    DATABASE_PARAMS = {"poolclass": NullPool}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """
    class for alembic migrations
    """
    pass
