from datetime import date

from fastapi import status

from lib.app.utils.app_errors import AppException, AppError
from lib.app.utils.validator.input_validator import InputValidator
from lib.app.utils.validator.user_validator import UserValidator
from lib.auth.model.models import User
from lib.diary.db.db import SQLAlchemyRecommendedProcedureDatabase, SQLAlchemyVisitDatabase, \
    SQLAlchemyFactProcedureDatabase
from lib.diary.model.schemas import FactProcedureCreate, VisitCreate, RecommendedProcedureCreate, FactProcedureUpdate


class DiaryManager:
    def __init__(self, logger):
        self.logger = logger

    async def add_procedure(self, user: User,
                            procedure: FactProcedureCreate | RecommendedProcedureCreate | VisitCreate,
                            procedure_db: SQLAlchemyRecommendedProcedureDatabase | SQLAlchemyVisitDatabase | SQLAlchemyFactProcedureDatabase):

        # await UserValidator.user_access_check(current_user=user)
        await UserValidator.user_verify(current_user=user, work_user_id=procedure.user_id)

        result = await procedure_db.add(procedure.model_dump(exclude_unset=True))

        self.logger.info(f"User {user.id} added procedure {procedure.model_dump()}")
        return result

    async def get_fact_procedures(self, procedure_db: SQLAlchemyFactProcedureDatabase, user: User,
                                  date_from: date, date_to: date):
        # await UserValidator.user_access_check(current_user=user)

        procedures = await procedure_db.get_many(user_id=user.id, date_from=date_from, date_to=date_to)
        return procedures

    async def get_one_fact_procedure(self, procedure_db: SQLAlchemyFactProcedureDatabase, user: User, procedure_id: int):
        # await UserValidator.user_access_check(current_user=user)

        procedure = await procedure_db.get_one(user_id=user.id, procedure_id=procedure_id)
        if not procedure:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND,
                               detail=AppError.PROCEDURE_NOT_FOUND,
                               params=f"user {user.id} procedure {procedure_id}")
        return procedure

    async def update_fact_procedure(self, procedure_id: int, procedure_db: SQLAlchemyFactProcedureDatabase,
                                    user: User, procedure: FactProcedureUpdate):
        await UserValidator.user_verify(user.id, procedure.user_id)
        # await UserValidator.user_access_check(current_user=user)

        procedure_dict = procedure.model_dump(exclude_unset=True)
        user_id = procedure_dict.pop("user_id")
        await InputValidator.empty_form_check(procedure_dict)

        update = await procedure_db.update(user_id=user.id, procedure_id=procedure_id, procedure_dict=procedure_dict)

        self.logger.info(f"User {user_id} updated procedure with params {procedure_dict}")
        return update




