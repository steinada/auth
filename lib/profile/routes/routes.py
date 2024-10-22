from fastapi import APIRouter, Depends, UploadFile, Request
from fastapi.responses import JSONResponse

from lib.auth.model.models import User
from lib.profile.db.db import SQLAlchemyProfileDatabase, SQLAlchemyPictureDatabase
from lib.profile.db.postgres import get_profile_db, get_picture_db
from lib.profile.manager import ProfileManager
from lib.profile.model.schemas import ProfileUpdate, ProfileRead


def get_profile_router(current_user, logger) -> APIRouter:
    router = APIRouter()
    profile_manager = ProfileManager(logger)

    @router.post("/update", response_class=JSONResponse)
    async def update_profile(profile_schema: ProfileUpdate,
                        user: User = Depends(current_user),
                        profile_db: SQLAlchemyProfileDatabase = Depends(get_profile_db)):

        result = await profile_manager.update_profile(profile_schema=profile_schema,
                                                      profile_db=profile_db, user=user)
        return result

    @router.get("")
    async def get_profile(user: User = Depends(current_user),
                          profile_db: SQLAlchemyProfileDatabase = Depends(get_profile_db)):

        profile = await profile_manager.get_profile(profile_db=profile_db, user=user)
        return profile

    @router.post("/photo")
    async def add_photo(master: bool, file: UploadFile, user: User = Depends(current_user),
                        picture_db: SQLAlchemyPictureDatabase = Depends(get_picture_db)):
        result = await profile_manager.add_photo_to_profile(user=user, master=master, picture_db=picture_db, file=file)
        return {"picture_url": result}

    @router.get("/photos")
    async def get_photos(limit: int, page: int, user: User = Depends(current_user),
                         picture_db: SQLAlchemyPictureDatabase = Depends(get_picture_db)):
        result = await profile_manager.get_profile_photos(user=user, limit=limit, page=page, picture_db=picture_db)
        return result

    @router.get("/photo")
    async def get_photos(user: User = Depends(current_user),
                         picture_db: SQLAlchemyPictureDatabase = Depends(get_picture_db)):
        result = await profile_manager.get_main_profile_photo(user=user, picture_db=picture_db)
        return result

    @router.delete("/photo")
    async def get_photos(file_id: int, request: Request,
                         user: User = Depends(current_user),
                         picture_db: SQLAlchemyPictureDatabase = Depends(get_picture_db)):
        result = await profile_manager.delete_profile_photo(user=user, picture_db=picture_db,
                                                            file_id=file_id, request=request)
        return result

    @router.post("/set-master-picture")
    async def set_master_to_photo(picture_id: int, request: Request,
                                  user: User = Depends(current_user),
                                  picture_db: SQLAlchemyPictureDatabase = Depends(get_picture_db)):
        result = await profile_manager.set_master_to_photo(picture_db=picture_db, picture_id=picture_id,
                                                           request=request, user=user)
        return result

    return router




