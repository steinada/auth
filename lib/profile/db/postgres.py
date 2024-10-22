from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_AUTH_DB_NAME
from lib.profile.db.db import SQLAlchemyProfileDatabase, SQLAlchemyPictureDatabase
from lib.profile.model.models import Profile, Picture

DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_AUTH_DB_NAME}"


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session_depends() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def get_async_session_context():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close_all()


async def get_profile_db(session: AsyncSession = Depends(get_async_session_depends)):
    yield SQLAlchemyProfileDatabase(session, Profile)


async def get_picture_db(session: AsyncSession = Depends(get_async_session_depends)):
    yield SQLAlchemyPictureDatabase(session, Picture)
