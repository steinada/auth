from fastapi import HTTPException
from starlette import status

from lib.app.utils.app_errors import AppError
from lib.auth.model.models import User, Clinic


class UserValidator:
    @staticmethod
    async def user_verify(current_user: User, work_user_id: int):
        if current_user.id != work_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=AppError.INCORRECT_USER,
            )

    # @staticmethod
    # async def user_access_check(current_user: User | Clinic):
    #     if current_user.role_id != 1:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail=AppError.ACCESS_DENIED,
    #         )
