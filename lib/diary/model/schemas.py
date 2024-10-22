from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


#FactProcedure
class FactProcedureCreate(BaseModel):
    user_id: int
    name: Optional[str] = None
    preparation_id: Optional[int] = None
    device_id: Optional[int] = None
    clinic_id: Optional[int] = None
    date: date
    preparation_photo_urls: Optional[dict] = None


class FactProcedureRead(FactProcedureCreate):
    id: int


class FactProcedureUpdate(FactProcedureRead):
    id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[date] = None


#Visit
class VisitCreate(BaseModel):
    user_id: int
    preparation_id: Optional[int] = None
    clinic_id: Optional[int] = None
    date: datetime
    length_in_minutes: Optional[int] = None


class VisitRead(VisitCreate):
    id: int


class VisitUpdate(VisitRead):
    id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[datetime] = None


#RecommendedProcedure
class RecommendedProcedureCreate(BaseModel):
    user_id: int
    preparation_id: int
    date: dict


class RecommendedProcedureRead(RecommendedProcedureCreate):
    id: int


class RecommendedProcedureUpdate(RecommendedProcedureRead):
    id: Optional[int] = None
    user_id: Optional[int] = None
    preparation_id: Optional[int] = None
    date: Optional[dict] = None

