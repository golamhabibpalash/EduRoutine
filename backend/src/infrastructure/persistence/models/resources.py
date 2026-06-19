"""Resources schema ORM models."""

from __future__ import annotations

from sqlalchemy import Boolean, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

SCHEMA = "resources"


class RoomModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``resources.rooms``."""

    __tablename__ = "rooms"
    __table_args__ = (
        UniqueConstraint("code", name="uq_rooms_code"),
        {"schema": SCHEMA},
    )

    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    capacity: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    building: Mapped[str] = mapped_column(String(100), nullable=False)
    floor: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    has_projector: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_computers: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_ac: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
