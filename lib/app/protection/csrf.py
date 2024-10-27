from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

from config import SECRET_CSRF


class CsrfSettings(BaseModel):
    secret_key: str = SECRET_CSRF


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()



