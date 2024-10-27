from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from lib.app.database import DATABASE_URL
from lib.diary.db.db import SQLAlchemyFactProcedureDatabase, SQLAlchemyVisitDatabase, \
    SQLAlchemyRecommendedProcedureDatabase

from lib.diary.model.models import FactProcedure, RecommendedProcedure, Visit

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


async def get_fact_procedures_db(session: AsyncSession = Depends(get_async_session_depends)):
    yield SQLAlchemyFactProcedureDatabase(session, FactProcedure)


async def get_visit_db(session: AsyncSession = Depends(get_async_session_depends)):
    yield SQLAlchemyVisitDatabase(session, RecommendedProcedure)


async def get_recommended_procedures_db(session: AsyncSession = Depends(get_async_session_depends)):
    yield SQLAlchemyRecommendedProcedureDatabase(session, Visit)

