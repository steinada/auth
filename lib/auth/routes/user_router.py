from fastapi import APIRouter, Request, Body, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from fastapi_users import FastAPIUsers, models, exceptions
from fastapi_users.manager import UserManagerDependency, BaseUserManager
from pydantic import EmailStr
from starlette import status

from lib.app.utils.app_errors import AppError, AppException
from lib.auth.routes.routes import get_custom_auth_router


def get_reset_password_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/forgot-password",
        name="reset:forgot_password",
        dependencies=[Depends(RateLimiter(times=2, seconds=30))]
    )
    async def forgot_password(
        request: Request,
        email: EmailStr = Body(..., embed=True),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    ):
        """Забыл пароль, идет отправка на почту ссылки для сброса пароля"""

        try:
            user = await user_manager.get_by_email(email)
        except exceptions.UserNotExists:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=AppError.USER_NOT_FOUND,
                request=request.url.path,
                params=email)

        try:
            await user_manager.forgot_password(user, request)
        except exceptions.UserInactive:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppError.USER_IS_INACTIVE,
                request=request.url.path,
                params=email)

        return {"detail": "Письмо со ссылкой для сброса пароля выслано на почту"}

    return router


# def get_custom_auth_router(self) -> APIRouter:
#     return get_custom_auth_router(current_user=self.current_user, logger=self.logger)
#

class FastUsers(FastAPIUsers[models.UP, models.ID]):
    def get_reset_password_router(self) -> APIRouter:
        return get_reset_password_router(self.get_user_manager)

    def get_custom_auth_router(self, logger, current_user) -> APIRouter:
        return get_custom_auth_router(logger, current_user, self.get_user_manager)
