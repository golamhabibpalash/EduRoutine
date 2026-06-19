"""People schema ORM models."""

from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

SCHEMA = "people"


class TeacherModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``people.teachers``."""

    __tablename__ = "teachers"
    __table_args__ = (
        UniqueConstraint("employee_id", name="uq_teachers_employee_id"),
        {"schema": SCHEMA},
    )

    employee_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    department: Mapped[str] = mapped_column(String(200), nullable=False)
    specialization: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, default=list)
    max_hours_per_week: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=30)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class StudentModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``people.students``."""

    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("student_id", name="uq_students_student_id"),
        {"schema": SCHEMA},
    )

    student_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("academic.batches.id", ondelete="RESTRICT"),
        nullable=False,
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("academic.sections.id", ondelete="RESTRICT"),
        nullable=False,
    )
    enrollment_year: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
