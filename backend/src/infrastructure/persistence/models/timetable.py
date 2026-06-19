"""Timetable schema ORM models."""

from __future__ import annotations

from datetime import time

from sqlalchemy import Boolean, SmallInteger, String, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

SCHEMA = "timetable"


class PeriodModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``timetable.periods``."""

    __tablename__ = "periods"
    __table_args__ = (
        UniqueConstraint("period_number", name="uq_periods_period_number"),
        {"schema": SCHEMA},
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    period_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    is_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
