from fastapi import HTTPException, status

from lib.app.utils.app_errors import AppError


class FileValidator:
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
