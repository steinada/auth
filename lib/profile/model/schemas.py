from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from lib.profile.model.enums import Sex


# Profile
class ProfileCreate(BaseModel):
    user_id: int


class ProfileUpdate(ProfileCreate):
    name: Optional[str] = Field(min_length=2, max_length=50, default=None)
    surname: Optional[str] = Field(min_length=2, max_length=50, default=None)
    sex: Optional[Sex] = None
    date_of_birth: Optional[date] = None
    city: Optional[str] = None


class ProfileRead(ProfileUpdate):
    name: Optional[str] = None
    surname: Optional[str] = None


# Picture
class PictureCreate(BaseModel):
    user_id: int
    picture_url: int
    master: bool = False
    file_name: str


class PictureRead(PictureCreate):
    id: int
    upload_date: date
