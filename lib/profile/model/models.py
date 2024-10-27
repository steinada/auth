from datetime import date
from typing import get_args

import sqlalchemy
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Boolean, Enum
from sqlalchemy.orm import mapped_column, Mapped

from lib.auth.model.models import Base
from lib.auth.model.models import User


class Profile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    sex: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[date] = mapped_column(TIMESTAMP, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)


class Picture(Base):
    __tablename__ = 'profile_picture'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    picture_url: Mapped[str] = mapped_column(String)
    upload_date: Mapped[date] = mapped_column(TIMESTAMP)
    master: Mapped[bool] = mapped_column(Boolean, default=False)
    file_name: Mapped[str] = mapped_column(String, nullable=True)
