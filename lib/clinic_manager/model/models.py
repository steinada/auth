from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from lib.auth.model.models import Base


class Preparation(Base):
    __tablename__ = "preparation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)


class Device(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)


class Clinic(Base):
    __tablename__ = "clinic"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    city: Mapped[str] = mapped_column(String(length=100), nullable=False)
    address: Mapped[str] = mapped_column(String(length=250), nullable=True)
