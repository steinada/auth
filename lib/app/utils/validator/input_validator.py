from fastapi import HTTPException, status

from lib.app.utils.app_errors import AppError


class InputValidator:
    @staticmethod
    async def empty_form_check(form: dict):
        if not form:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AppError.EMPTY_FORM,
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
