from typing import Optional

from pydantic import BaseModel


#Preparation
class PreparationCreate(BaseModel):
    name: str


class PreparationRead(PreparationCreate):
    id: int


class PreparationUpdate(PreparationRead):
    id: Optional[int] = None
    name: Optional[str] = None


#Device
class DeviceCreate(BaseModel):
    name: str


class DeviceRead(DeviceCreate):
    id: int


class DeviceUpdate(DeviceRead):
    id: Optional[int] = None
    name: Optional[str] = None


#Clinic
class ClinicCreate(BaseModel):
    name: str
    city: str
    address: str


class ClinicRead(ClinicCreate):
    id: int


class ClinicUpdate(ClinicRead):
    id: Optional[int] = None
    name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
