"""Academic schema ORM models — departments, sessions, semesters, batches, sections, courses.

Faithful to docs/03 + docs/12 (academic.*), minus multi-tenancy (deferred).
"""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Numeric,
    SmallInteger,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

SCHEMA = "academic"


class DepartmentModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``academic.departments``."""

    __tablename__ = "departments"
    __table_args__ = (
        UniqueConstraint("code", name="uq_departments_code"),
        {"schema": SCHEMA},
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)


class SessionModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``academic.sessions``."""

    __tablename__ = "sessions"
    __table_args__ = {"schema": SCHEMA}

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class SemesterModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``academic.semesters``."""

    __tablename__ = "semesters"
    __table_args__ = (
        UniqueConstraint("session_id", "number", name="uq_semesters_session_id_number"),
        {"schema": SCHEMA},
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.sessions.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)


class BatchModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``academic.batches``."""

    __tablename__ = "batches"
    __table_args__ = (
        UniqueConstraint("code", name="uq_batches_code"),
        {"schema": SCHEMA},
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.sessions.id", ondelete="RESTRICT"),
        nullable=False,
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.departments.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)


class SectionModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``academic.sections``."""

    __tablename__ = "sections"
    __table_args__ = (
        UniqueConstraint("batch_id", "name", name="uq_sections_batch_id_name"),
        {"schema": SCHEMA},
    )

    batch_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.batches.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    max_capacity: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class CourseModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``academic.courses``."""

    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint("code", name="uq_courses_code"),
        {"schema": SCHEMA},
    )

    department_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.departments.id", ondelete="RESTRICT"),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    credits: Mapped[Decimal] = mapped_column(Numeric(3, 1), nullable=False)
    lecture_hours: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    lab_hours: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class CoursePrerequisiteModel(Base):
    """``academic.course_prerequisites`` — course↔prerequisite association."""

    __tablename__ = "course_prerequisites"
    __table_args__ = {"schema": SCHEMA}

    course_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.courses.id", ondelete="CASCADE"),
        primary_key=True,
    )
    prerequisite_course_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.courses.id", ondelete="CASCADE"),
        primary_key=True,
    )
