from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from lib.diary.db.protocols import FPP


class SQLAlchemyFactProcedureDatabase:

    def __init__(
        self,
        session: AsyncSession,
        procedure_table,
    ):
        self.session = session
        self.procedure_table = procedure_table

    async def add(self, create_dict):
        procedure = self.procedure_table(**create_dict)
        self.session.add(procedure)
        await self.session.commit()
        await self.session.refresh(procedure)
        return procedure


class SQLAlchemyVisitDatabase:

    def __init__(
        self,
        session: AsyncSession,
        visit_table,
    ):
        self.session = session
        self.visit_table = visit_table

    async def add(self, create_dict):
        visit = self.visit_table(**create_dict)
        self.session.add(visit)
        await self.session.commit()
        await self.session.refresh(visit)
        return visit


class SQLAlchemyRecommendedProcedureDatabase:

    def __init__(
        self,
        session: AsyncSession,
        recommended_procedure_table,
    ):
        self.session = session
        self.recommended_procedure_table = recommended_procedure_table

    async def add(self, create_dict):
        recommended_procedure = self.recommended_procedure_table(**create_dict)
        self.session.add(recommended_procedure)
        await self.session.commit()
        await self.session.refresh(recommended_procedure)
        return recommended_procedure
