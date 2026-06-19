"""Timetable schema ORM models."""

from __future__ import annotations

import uuid
from datetime import time

from sqlalchemy import Boolean, ForeignKey, SmallInteger, String, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
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


class RoutineModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``timetable.routines``."""

    __tablename__ = "routines"
    __table_args__ = (
        UniqueConstraint("name", name="uq_routines_name"),
        {"schema": SCHEMA},
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    session_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    batch_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    semester_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    department_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")


class RoutineDetailModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``timetable.routine_details``."""

    __tablename__ = "routine_details"
    __table_args__ = ({"schema": SCHEMA},)

    routine_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.routines.id", ondelete="CASCADE"),
        nullable=False,
    )
    course_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    teacher_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    room_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    section_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    day_of_week: Mapped[str] = mapped_column(String(10), nullable=False)
    start_time: Mapped[str] = mapped_column(String(5), nullable=False)
    end_time: Mapped[str] = mapped_column(String(5), nullable=False)
    is_lab: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
