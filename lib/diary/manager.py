from lib.app.utils.validator import Validator
from lib.auth.model.models import User
from lib.diary.db.db import SQLAlchemyRecommendedProcedureDatabase, SQLAlchemyVisitDatabase, \
    SQLAlchemyFactProcedureDatabase
from lib.diary.model.schemas import FactProcedureCreate, VisitCreate, RecommendedProcedureCreate


class DiaryManager:
    def __init__(self, logger):
        self.logger = logger

    async def add_procedure(self, user: User,
                            procedure: FactProcedureCreate | RecommendedProcedureCreate | VisitCreate,
                            procedure_db: SQLAlchemyRecommendedProcedureDatabase | SQLAlchemyVisitDatabase | SQLAlchemyFactProcedureDatabase):

        await Validator.user_verify(current_user=user, work_user_id=procedure.user_id)

        result = await procedure_db.add(procedure.model_dump(exclude_unset=True))

        self.logger.info(f"User {user.id} added procedure {procedure.model_dump()}")
        return result
