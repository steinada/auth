from fastapi import HTTPException
from starlette import status

from lib.app.utils.app_errors import AppError
from lib.auth.model.models import User


class Validator:
    @staticmethod
    async def user_verify(current_user: User, work_user_id: int):
        if current_user.id != work_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=AppError.INCORRECT_USER,
            )

    @staticmethod
    async def empty_form_check(form: dict):
        if not form:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppError.EMPTY_FORM,
            )

    @staticmethod
    async def file_format_check(filename: str):
        _, file_format = filename.split('.')
        legal_formats = ['jpeg', 'jpg', 'png']
        if file_format not in legal_formats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppError.ILLIGAL_FILE_FORMAT + ', '.join(legal_formats),
            )

    @staticmethod
    async def file_size_check(filesize: int):
        filesize_in_mb = filesize / 1_000_000
        max_legal_size = 5  # MB
        if filesize_in_mb > max_legal_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppError.FILE_IS_TOO_BIG + str(max_legal_size) + "MB",
            )

    @staticmethod
    async def pagination_params_check(page: int, limit: int):
        start_page = 0
        min_limit = 5

        if page < start_page:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppError.ILLIGAL_PAGE_NUMER + str(start_page),
            )

        if limit < min_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppError.ILLIGAL_PAGE_SIZE + str(min_limit),
            )
