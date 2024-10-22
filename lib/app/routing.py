from fastapi import APIRouter

from lib.auth.routes.routes import get_custom_auth_router
from lib.diary.routes.routes import get_diary_router
from lib.profile.routes.routes import get_profile_router


class AppRouting:
    def __init__(self, logger, current_user):
        self.logger = logger
        self.current_user = current_user

    def get_custom_auth_router(self) -> APIRouter:
        return get_custom_auth_router(current_user=self.current_user, logger=self.logger)

    def get_profile_router(self) -> APIRouter:
        return get_profile_router(current_user=self.current_user, logger=self.logger)

    def get_diary_router(self) -> APIRouter:
        return get_diary_router(current_user=self.current_user, logger=self.logger)

