from random import randrange
from typing import Optional

import aioredis
from starlette import status

from lib.app.utils.app_errors import AppError, AppException
from lib.app.utils.validator.user_validator import UserValidator
from lib.auth.db.postgres import get_user_db, get_clinic_db
from lib.auth.model.schemas import ChangePassword, UserUpdate
from lib.auth.repository.redis_repo import add_email_verify_code, get_email_verify_code
from lib.logger.logger import get_logger
from lib.mail_service.constructor import MailConstructor
from lib.auth.db.redis import redis_cli

from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from fastapi_users.jwt import generate_jwt

from lib.auth.model.models import User, Clinic

from config import USER_AUTH_SECRET
from lib.mail_service.mail_sendler import MailSendler
from lib.profile.controller import ProfileManager


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = USER_AUTH_SECRET
    verification_token_secret = USER_AUTH_SECRET

    def __init__(self, *args, **kwargs):
        self.logger = get_logger()
        super().__init__(*args, **kwargs)

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise AppException(status_code=status.HTTP_409_CONFLICT,
                               detail=AppError.USER_ALREADY_EXISTS,
                               params=user_create.email,
                               request=request.url.path)

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        # email_verify_code = user_dict.pop("email_verify_code")
        # await self.check_email_verify_code(user_dict["email"], email_verify_code)

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["is_superuser"], user_dict["is_verified"] = False, False

        self.logger.info(f"Start to create user with params {user_dict}")
        created_user = await self.user_db.create(user_dict)

        if created_user.role_id == 1:
            await self.on_after_user_register(created_user, request)
        elif created_user.role_id == 2:
            await self.on_after_clinic_register(created_user, request)

        return created_user

    async def on_after_user_register(self, user: User, request: Optional[Request] = None):
        profile_manager = ProfileManager(logger=self.logger)
        await profile_manager.create_profile(user.id)
        self.logger.info(f"User created with params {vars(user)}")

    async def on_after_clinic_register(self, clinic: Clinic, request: Optional[Request] = None):
        self.logger.info(f"Clinic created with params {vars(clinic)}")

    async def on_after_forgot_password(
        self, user: User, token: int, request: Optional[Request] = None
    ):
        self.logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        self.logger.info(f"Verification requested for user {user.id}. Verification token: {token}")

    async def forgot_password(
            self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        if not user.is_active:
            raise AppException(status_code=status.HTTP_409_CONFLICT,
                               detail=AppError.USER_IS_INACTIVE,
                               params=user.id,
                               request=request.url.path)

        token_data = {
            "sub": str(user.id),
            "password_fgpt": self.password_helper.hash(user.hashed_password),
            "aud": self.reset_password_token_audience}

        token = generate_jwt(
            token_data,
            self.reset_password_token_secret,
            self.reset_password_token_lifetime_seconds)

        await self.on_after_forgot_password(user, token, request)

        user_email = user.email
        reset_password_link = await MailConstructor.reset_password_link_mail(user_email, token)

        with MailSendler() as mail_sendler:
            mail_sendler.send_mail(user_email, reset_password_link)
        self.logger.info(f"Send reset token {token} to email {user_email}")

    @staticmethod
    async def send_email_verify_code(email: str, redis: aioredis.Redis, logger):
        code = str(randrange(100000, 999999))
        logger.info(f"User {email} requested email verify code {code}")

        await add_email_verify_code(email, code, redis)
        verify_mail_code = await MailConstructor.verify_mail_code(code, email)

        with MailSendler() as mail_sendler:
            mail_sendler.send_mail(email, verify_mail_code)
        logger.info(f"Send registration verify code {verify_mail_code} to email {email}")

    @staticmethod
    async def check_email_verify_code(email, verify_code):
        redis = await redis_cli
        code_in_redis = await get_email_verify_code(email, redis)
        if not code_in_redis:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail=AppError.CODE_WASNT_SEND,
                               params=verify_code,
                               request=email)

        if code_in_redis != verify_code:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail=AppError.INCORRECT_CODE_INPUTED,
                               params=verify_code,
                               request=email)

    async def change_password(self, request: Request, user: User,
                              change_password_schema: ChangePassword):
        # await UserValidator.user_access_check(current_user=user)

        existing_user = await self.user_db.get(user.id)
        user_update = UserUpdate(password=change_password_schema.new_password)

        verified, updated_password_hash = self.password_helper.verify_and_update(
            change_password_schema.old_password, user.hashed_password)

        if not verified:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail=AppError.INCORRECT_PASSWORD,
                               params=request.url.path,
                               request=user.id)

        await self.update(user_update, user, safe=True, request=request)
        self.logger.info(f"User {user.id} changed password")

        return existing_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


async def get_clinic_manager(clinic_db=Depends(get_clinic_db)):
    yield UserManager(clinic_db)
