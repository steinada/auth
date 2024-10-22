from enum import Enum

from fastapi import HTTPException

from lib.logger.logger import get_logger


class AppError(str, Enum):
    CODE_WASNT_SEND = "Сначала запросите код на почту"
    INCORRECT_CODE_INPUTED = "Неверный код подтверждения, повторите запрос и введите код снова"
    USER_NOT_FOUND = "Пользователь не найден"
    USER_IS_INACTIVE = "Пользователь неактивен"
    USER_ALREADY_EXISTS = "Пользователь уже существует"
    INCORRECT_USER = "Неверный пользователь"
    INCORRECT_PASSWORD = "Неверный пароль"

    INCORRECT_DATA_FOR_DB = "Запрос содержит некорректные данные"
    UNKNOWN_ERROR_HAPPENED = "Произошла неизвестная ошибка, нам очень жаль"
    EMPTY_FORM = "Не введены данные для обновления"

    ILLIGAL_FILE_FORMAT = "Неверный формат файла, допустимы: "
    FILE_IS_TOO_BIG = "Размер файла больше допустимого "
    FILE_DOES_NOT_EXIST = "Файл не существует"

    ILLIGAL_PAGE_SIZE = "Неверный лимит объектов на странице, значение не должно быть меньше "
    ILLIGAL_PAGE_NUMER = "Неверный номер страницы, значение не должно быть меньше "


class AppException(HTTPException):
    def __init__(self, status_code, detail, params=None, request=None):
        super().__init__(status_code, detail)

        self.logger = get_logger()
        self.logger.error(f"{detail} {request if request else str(request)} {params if params else str(params)}")


