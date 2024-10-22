from datetime import date
from typing import Protocol, TypeVar

ID = TypeVar("ID")


class FactProcedureProtocol(Protocol[ID]):

    id: ID
    user_id: int
    name: str
    preparation_id: int
    device_id: int
    clinic_id: int
    date: date
    preparation_photo_urls: dict


FPP = TypeVar("FPP", bound=FactProcedureProtocol)
