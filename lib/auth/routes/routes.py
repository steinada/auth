import logging

import aioredis
from fastapi import Depends, APIRouter, Response
from fastapi_csrf_protect import CsrfProtect
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import SECRET_CSRF
from lib.auth.model.models import User
from lib.auth.db.redis import get_redis_generator
from lib.auth.controller import UserManager, get_user_manager
from lib.auth.model.schemas import ChangePassword


def get_custom_auth_router(current_user, logger, get_some_user_manager) -> APIRouter:
    router = APIRouter()
    get_some_user_manager = get_some_user_manager

    # @router.get("/csrftoken/")
    # async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    #     token = csrf_protect.generate_csrf_tokens(SECRET_CSRF)
    #     response = JSONResponse(status_code=200, content={'csrf_token': 'cookie'})
    #     csrf_protect.set_csrf_cookie(token, response)
    #     return response

    @router.get("/reset-password-token/{token}")
    async def reset_password_link(response: Response, token: str):
        """По этой ссылке переходит пользователь для сброса пароля, токен сетится в куки,
        далее его надо отпарвить в запросе /auth/reset-password в token"""

        response.set_cookie('token', token, expires=300)
        logger.info(f"Set cookies for reset password: {token}")
        return 'ok'

    # @router.post("/send-email-verify-code/",
    #              dependencies=[Depends(RateLimiter(times=1, seconds=30))])
    # async def send_email_verify_code(email: EmailStr, redis: aioredis.Redis = Depends(get_redis_generator)):
    #     await UserManager.send_email_verify_code(email, redis, logger)
    #     return {"result": "Письмо отправлено, проверьте почту"}

    @router.post("/change-password")
    async def change_password(request: Request,
                              change_password_schema: ChangePassword,
                              user_manager: UserManager = Depends(get_some_user_manager),
                              user: User = Depends(current_user)):
        """Изменение пароля через личный кабинет путем ввода текущего и нового"""

        await user_manager.change_password(change_password_schema=change_password_schema, user=user, request=request)
        return 'ok'

    return router

