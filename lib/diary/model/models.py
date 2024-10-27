from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import mapped_column, Mapped

from lib.auth.model.models import Base
from lib.auth.model.models import User
from lib.clinic_manager.model.models import Preparation, Device, Clinic


class FactProcedure(Base):
    __tablename__ = 'fact_procedure'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    preparation_id: Mapped[int] = mapped_column(Integer, ForeignKey(Preparation.id), nullable=True)
    device_id: Mapped[int] = mapped_column(Integer, ForeignKey(Device.id), nullable=True)
    clinic_id: Mapped[int] = mapped_column(Integer, ForeignKey(Clinic.id), nullable=True)
    date: Mapped[datetime.date] = mapped_column(TIMESTAMP, nullable=False)
    preparation_photo_urls: Mapped[dict] = mapped_column(JSON, nullable=True)


class Visit(Base):
    __tablename__ = 'visit'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    preparation_id: Mapped[int] = mapped_column(Integer, ForeignKey(Preparation.id), nullable=True)
    clinic_id: Mapped[int] = mapped_column(Integer, ForeignKey(Clinic.id), nullable=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    length_in_minutes: Mapped[int] = mapped_column(Integer, nullable=True)


class RecommendedProcedure(Base):
    __tablename__ = 'recommended_procedure'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    preparation_id: Mapped[int] = mapped_column(Integer, ForeignKey(Preparation.id), nullable=False)
    date: Mapped[dict] = mapped_column(JSON, nullable=False)
