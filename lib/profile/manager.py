from datetime import datetime

from fastapi import UploadFile, Request, status

from lib.app.utils.app_errors import AppError, AppException
from lib.app.utils.validator import Validator
from lib.auth.model.models import User
from lib.media_service.manager import MinioManager
from lib.profile.db.db import SQLAlchemyProfileDatabase, SQLAlchemyPictureDatabase
from lib.profile.db.postgres import get_profile_db, get_async_session_context
from lib.profile.model.schemas import ProfileCreate, ProfileUpdate


class ProfileManager:
    def __init__(self, logger):
        self.logger = logger

    async def create_profile(self, user_id: int):
        profile_schema = ProfileCreate(user_id=user_id)
        profile_dict = profile_schema.model_dump()
        async with get_async_session_context() as session:
            profile_db = await anext(get_profile_db(session))
            await profile_db.create(**profile_dict)

        self.logger.info(f"Created empty profile for user {user_id}")

    async def update_profile(self,
                             profile_db: SQLAlchemyProfileDatabase,
                             profile_schema: ProfileUpdate,
                             user: User):
        await Validator.user_verify(current_user=user, work_user_id=profile_schema.user_id)

        profile_dict = profile_schema.model_dump(exclude_unset=True)
        user_id = profile_dict.pop("user_id")
        await Validator.empty_form_check(profile_dict)

        result = await profile_db.update(user_id, **profile_dict)

        self.logger.info(f"User {user_id} updated profile with params {profile_dict}")
        return result

    async def get_profile(self, profile_db: SQLAlchemyProfileDatabase, user: User):
        user_id = user.id
        return await profile_db.get_one(user_id=user_id)

    async def add_photo_to_profile(self, user: User, file: UploadFile, master: bool,
                                   picture_db: SQLAlchemyPictureDatabase):

        await Validator.file_format_check(file.filename)
        await Validator.file_size_check(file.size)

        if master:
            await picture_db.unset_master(user_id=user.id)

        minio_manager = MinioManager(self.logger)

        file_bytes = await file.read()
        file_name = f"{datetime.timestamp(datetime.now())}_{file.filename}"
        picture_url = await minio_manager.put_object(file_name=file_name,
                                                     file_bytes=file_bytes,
                                                     bytes_len=file.size)
        await picture_db.add(user_id=user.id, master=master, picture_url=picture_url, file_name=file_name)

        self.logger.info(f"User {user.id} added {picture_url} into profile")
        return picture_url

    async def get_profile_photos(self, user: User, limit: int, page: int, picture_db: SQLAlchemyPictureDatabase):
        await Validator.pagination_params_check(limit=limit, page=page)

        photos = await picture_db.get_many(user_id=user.id, page=page, limit=limit)
        response = {"content": photos,
                    "page": page,
                    "size": len(photos)}
        return response

    async def get_main_profile_photo(self, user: User, picture_db: SQLAlchemyPictureDatabase):
        photos = await picture_db.get_main(user_id=user.id)
        return photos

    async def delete_profile_photo(self, user: User, picture_db: SQLAlchemyPictureDatabase,
                                   file_id: int, request: Request):
        file_name = await picture_db.delete(user_id=user.id, file_id=file_id)
        self.logger.info(f"Photo {file_id} of user {user.id} deleted from pg")

        if not file_name:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppError.FILE_DOES_NOT_EXIST,
                params=file_id,
                request=request.url.path)

        minio_manager = MinioManager(self.logger)
        result = await minio_manager.delete(file_name=file_name)

        self.logger.info(f"Photo {file_id} of user {user.id} deleted from minio")
        return result

    async def set_master_to_photo(self, request: Request, picture_db: SQLAlchemyPictureDatabase, picture_id: int, user: User):
        result = await picture_db.set_master(picture_id=picture_id, user_id=user.id)

        if not result:
            raise AppException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                               detail=AppError.INCORRECT_USER,
                               params=f"User {user.id} picture_id {picture_id}",
                               request=request.url.path)

        self.logger.info(f"User {user.id} set photo {picture_id} as master")
        return result

