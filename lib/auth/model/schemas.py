from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    email: Optional[EmailStr]
    phone: str
    registered_at: datetime
    role_id: Optional[int]
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    phone: str
    registered_at: datetime = datetime.utcnow
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    # email_verify_code: str


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    registered_at: Optional[datetime] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

    # email_verify_code: Optional[str] = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class ClinicCreate(schemas.BaseUserCreate):
    email: EmailStr
    phone: str
    password: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    inn: int
    organisation_name: str


class ClinicUpdate(schemas.BaseUserUpdate):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    inn: Optional[int] = None
    organisation_name: Optional[str] = None


class ClinicRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    phone: str
    role_id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool
    inn: int
    organisation_name: str
