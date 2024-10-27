from datetime import date
from typing import List
from fastapi import APIRouter, Depends

from lib.auth.model.models import User
from lib.diary.db.db import SQLAlchemyFactProcedureDatabase
from lib.diary.db.postgres import get_fact_procedures_db
from lib.diary.controller import DiaryManager
from lib.diary.model.schemas import FactProcedureCreate, FactProcedureUpdate, VisitCreate, VisitUpdate, \
    RecommendedProcedureCreate, RecommendedProcedureUpdate, RecommendedProcedureRead, VisitRead, FactProcedureRead


def get_diary_router(current_user, logger):
    router = APIRouter()
    diary_manager = DiaryManager(logger)

    @router.post('/fact-procedure', response_model=FactProcedureRead)
    async def add_procedure(procedure: FactProcedureCreate,
                            user: User = Depends(current_user),
                            procedure_db: SQLAlchemyFactProcedureDatabase = Depends(get_fact_procedures_db)):
        procedure = await diary_manager.add_procedure(procedure=procedure, procedure_db=procedure_db, user=user)
        return procedure

    @router.get('/fact-procedures', response_model=List[FactProcedureRead])
    async def get_procedures(date_from: date, date_to: date, user: User = Depends(current_user),
                             procedure_db: SQLAlchemyFactProcedureDatabase = Depends(get_fact_procedures_db)):
        procedures = await diary_manager.get_fact_procedures(procedure_db=procedure_db, user=user,
                                                        date_from=date_from, date_to=date_to)
        return procedures

    @router.get('/fact-procedure', response_model=FactProcedureRead)
    async def get_procedure(procedure_id: int, user: User = Depends(current_user),
                            procedure_db: SQLAlchemyFactProcedureDatabase = Depends(get_fact_procedures_db)):
        procedure = await diary_manager.get_one_fact_procedure(procedure_db=procedure_db,
                                                                user=user, procedure_id=procedure_id)
        return procedure

    @router.put('/fact-procedure', response_model=FactProcedureRead)
    async def update_procedure(procedure: FactProcedureUpdate, procedure_id: int,
                               user: User = Depends(current_user),
                               procedure_db: SQLAlchemyFactProcedureDatabase = Depends(get_fact_procedures_db)):
        procedure = await diary_manager.update_fact_procedure(procedure_db=procedure_db, procedure_id=procedure_id,
                                                               user=user, procedure=procedure)
        return procedure

    @router.delete('/fact-procedure')
    async def delete_procedure(procedure_id: int, user: User = Depends(current_user)):
        pass

    @router.post('/visit', response_model=VisitRead)
    async def add_visit(visit: VisitCreate,
                        user: User = Depends(current_user)):
        pass

    @router.get('/visit', response_model=List[VisitRead])
    async def get_visit(user: User = Depends(current_user)):
        pass

    @router.get('/visit', response_model=VisitRead)
    async def get_visit(visit_id: int, user: User = Depends(current_user)):
        pass

    @router.put('/visit', response_model=VisitRead)
    async def update_visit(visit: VisitUpdate,
                           visit_id: int,
                           user: User = Depends(current_user)):
        pass

    @router.delete('/visit')
    async def delete_visit(visit_id: int, user: User = Depends(current_user)):
        pass

    @router.post('/recommended-procedure', response_model=RecommendedProcedureRead)
    async def add_recommended_procedure(procedure: RecommendedProcedureCreate,
                                        user: User = Depends(current_user)):
        pass

    @router.get('/recommended-procedure', response_model=List[RecommendedProcedureRead])
    async def get_recommended_procedure(user: User = Depends(current_user)):
        pass

    @router.get('/recommended-procedure', response_model=RecommendedProcedureRead)
    async def get_recommended_procedure(procedure_id: int, user: User = Depends(current_user)):
        pass

    @router.put('/recommended-procedure')
    async def update_recommended_procedure(procedure: RecommendedProcedureUpdate,
                                           procedure_id: int,
                                           user: User = Depends(current_user)):
        pass

    @router.delete('/recommended-procedure')
    async def delete_recommended_procedure(procedure_id: int, user: User = Depends(current_user)):
        pass

    return router
