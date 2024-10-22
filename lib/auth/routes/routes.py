import logging

import aioredis
from fastapi import Depends, APIRouter, Response
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr
from starlette.requests import Request

from lib.auth.model.models import User
from lib.auth.db.redis import get_redis_generator
from lib.auth.manager import UserManager, get_user_manager
from lib.auth.model.schemas import ChangePassword


def get_custom_auth_router(current_user, logger) -> APIRouter:
    router = APIRouter()

    @router.get("/reset-password-token/{token}")
    async def reset_password_link(response: Response, token: str):
        response.set_cookie('token', token, expires=300)
        logger.info(f"Set cookies for reset password: {token}")
        return 'ok'

    @router.post("/send-email-verify-code/",
                 dependencies=[Depends(RateLimiter(times=1, seconds=30))])
    async def send_email_verify_code(email: EmailStr, redis: aioredis.Redis = Depends(get_redis_generator)):
        await UserManager.send_email_verify_code(email, redis, logger)
        return {"result": "Письмо отправлено, проверьте почту"}

    @router.post("/change-password")
    async def change_password(request: Request,
                              change_password_schema: ChangePassword,
                              user_manager: UserManager = Depends(get_user_manager),
                              user: User = Depends(current_user)):
        await user_manager.change_password(change_password_schema=change_password_schema, user=user, request=request)
        return 'ok'

    return router

