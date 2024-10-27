import sqlalchemy
from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette import status

from lib.app import app
from lib.app.utils.app_errors import AppError
from lib.logger.logger import get_logger


logger = get_logger()


@app.exception_handler(sqlalchemy.exc.IntegrityError)
async def sqlalchemy_error_handler(request: Request, exc: sqlalchemy.exc.IntegrityError):
    logger.error(f"{request.method} {request.url.path} {exc.orig}\nParams: {exc.params}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": AppError.INCORRECT_DATA_FOR_DB},
    )


@app.exception_handler(Exception)
async def server_error_handler(request: Request, exc: Exception):
    logger.error(f"{request.method} {request.url.path} {type(exc)} {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": AppError.UNKNOWN_ERROR_HAPPENED},
    )

