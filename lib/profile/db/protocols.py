from datetime import date
from typing import Protocol, TypeVar

ID = TypeVar("ID")


class ProfileProtocol(Protocol[ID]):

    id: ID
    user_id: int
    sex: int
    name: str
    surname: str
    date_of_birth: date
    city: str


PrP = TypeVar("PrP", bound=ProfileProtocol)


class PictureProtocol(Protocol[ID]):

    id: ID
    user_id: int
    picture_url: str
    upload_date: date
    master: bool
    file_name: str


PiP = TypeVar("PiP", bound=PictureProtocol)
