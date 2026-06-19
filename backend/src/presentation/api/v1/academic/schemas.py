"""Academic request/response schemas."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.academic.dto import (
    BatchDTO,
    CourseDTO,
    DepartmentDTO,
    SectionDTO,
    SemesterDTO,
    SessionDTO,
)


# --------------------------------------------------------------- response data
class DepartmentData(BaseModel):
    id: UUID
    name: str
    code: str
    created_at: datetime

    @classmethod
    def from_dto(cls, d: DepartmentDTO) -> DepartmentData:
        return cls(id=d.id, name=d.name, code=d.code, created_at=d.created_at)


class SessionData(BaseModel):
    id: UUID
    name: str
    start_date: date
    end_date: date
    is_current: bool
    created_at: datetime

    @classmethod
    def from_dto(cls, s: SessionDTO) -> SessionData:
        return cls(
            id=s.id,
            name=s.name,
            start_date=s.start_date,
            end_date=s.end_date,
            is_current=s.is_current,
            created_at=s.created_at,
        )


class SemesterData(BaseModel):
    id: UUID
    session_id: UUID
    name: str
    number: int
    start_date: date
    end_date: date
    created_at: datetime

    @classmethod
    def from_dto(cls, s: SemesterDTO) -> SemesterData:
        return cls(
            id=s.id,
            session_id=s.session_id,
            name=s.name,
            number=s.number,
            start_date=s.start_date,
            end_date=s.end_date,
            created_at=s.created_at,
        )


class BatchData(BaseModel):
    id: UUID
    session_id: UUID
    department_id: UUID
    name: str
    code: str
    created_at: datetime

    @classmethod
    def from_dto(cls, b: BatchDTO) -> BatchData:
        return cls(
            id=b.id,
            session_id=b.session_id,
            department_id=b.department_id,
            name=b.name,
            code=b.code,
            created_at=b.created_at,
        )


class SectionData(BaseModel):
    id: UUID
    batch_id: UUID
    name: str
    max_capacity: int
    created_at: datetime

    @classmethod
    def from_dto(cls, s: SectionDTO) -> SectionData:
        return cls(
            id=s.id,
            batch_id=s.batch_id,
            name=s.name,
            max_capacity=s.max_capacity,
            created_at=s.created_at,
        )


class CourseData(BaseModel):
    id: UUID
    department_id: UUID
    code: str
    title: str
    credits: float
    lecture_hours: int
    lab_hours: int
    is_active: bool
    created_at: datetime

    @classmethod
    def from_dto(cls, c: CourseDTO) -> CourseData:
        return cls(
            id=c.id,
            department_id=c.department_id,
            code=c.code,
            title=c.title,
            credits=float(c.credits),
            lecture_hours=c.lecture_hours,
            lab_hours=c.lab_hours,
            is_active=c.is_active,
            created_at=c.created_at,
        )


# ------------------------------------------------------------------- requests
class CreateDepartmentRequest(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    code: str = Field(min_length=1, max_length=20)


class UpdateDepartmentRequest(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    code: str = Field(min_length=1, max_length=20)


class CreateSessionRequest(BaseModel):
    name: str = Field(min_length=4, max_length=100)
    start_date: date
    end_date: date
    is_current: bool = False


class UpdateSessionRequest(BaseModel):
    name: str = Field(min_length=4, max_length=100)
    start_date: date
    end_date: date


class CreateSemesterRequest(BaseModel):
    session_id: UUID
    name: str = Field(min_length=2, max_length=100)
    number: int = Field(ge=1, le=12)
    start_date: date
    end_date: date


class UpdateSemesterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    number: int = Field(ge=1, le=12)
    start_date: date
    end_date: date


class CreateBatchRequest(BaseModel):
    session_id: UUID
    department_id: UUID
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=50)


class UpdateBatchRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=50)


class CreateSectionRequest(BaseModel):
    batch_id: UUID
    name: str = Field(min_length=1, max_length=50)
    max_capacity: int = Field(ge=1, le=500)


class UpdateSectionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    max_capacity: int = Field(ge=1, le=500)


class CreateCourseRequest(BaseModel):
    department_id: UUID
    code: str = Field(pattern=r"^[A-Z]{2,4}-\d{3}$")
    title: str = Field(min_length=3, max_length=200)
    credits: Decimal = Field(ge=0.5, le=6.0, multiple_of=0.5)
    lecture_hours: int = Field(ge=0, le=20)
    lab_hours: int = Field(default=0, ge=0, le=20)
    prerequisite_ids: list[UUID] = Field(default_factory=list)


class UpdateCourseRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    credits: Decimal = Field(ge=0.5, le=6.0, multiple_of=0.5)
    lecture_hours: int = Field(ge=0, le=20)
    lab_hours: int = Field(ge=0, le=20)
    is_active: bool = True


class AddPrerequisiteRequest(BaseModel):
    prerequisite_id: UUID
