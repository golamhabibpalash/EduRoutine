"""Teacher & student request/response schemas (bare, matching the frontend)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.people.dto import StudentDTO, TeacherDTO


class TeacherData(BaseModel):
    id: UUID
    employee_id: str
    name: str
    email: str
    phone: str | None
    department: str
    specialization: list[str]
    max_hours_per_week: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, t: TeacherDTO) -> TeacherData:
        return cls(
            id=t.id,
            employee_id=t.employee_id,
            name=t.name,
            email=t.email,
            phone=t.phone,
            department=t.department,
            specialization=list(t.specialization),
            max_hours_per_week=t.max_hours_per_week,
            is_active=t.is_active,
            created_at=t.created_at,
            updated_at=t.updated_at,
        )


class StudentData(BaseModel):
    id: UUID
    student_id: str
    name: str
    email: str
    phone: str | None
    batch_id: UUID
    batch_name: str | None
    section_id: UUID
    section_name: str | None
    enrollment_year: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, s: StudentDTO) -> StudentData:
        return cls(
            id=s.id,
            student_id=s.student_id,
            name=s.name,
            email=s.email,
            phone=s.phone,
            batch_id=s.batch_id,
            batch_name=s.batch_name,
            section_id=s.section_id,
            section_name=s.section_name,
            enrollment_year=s.enrollment_year,
            is_active=s.is_active,
            created_at=s.created_at,
            updated_at=s.updated_at,
        )


class CreateTeacherRequest(BaseModel):
    employee_id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    department: str = Field(min_length=1, max_length=200)
    specialization: list[str] = Field(default_factory=list)
    max_hours_per_week: int = Field(default=30, ge=1, le=60)
    is_active: bool = True


class UpdateTeacherRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    department: str = Field(min_length=1, max_length=200)
    specialization: list[str] = Field(default_factory=list)
    max_hours_per_week: int = Field(default=30, ge=1, le=60)
    is_active: bool = True


class CreateStudentRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    batch_id: UUID
    section_id: UUID
    enrollment_year: int = Field(ge=1900, le=2100)
    is_active: bool = True


class UpdateStudentRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    batch_id: UUID
    section_id: UUID
    enrollment_year: int = Field(ge=1900, le=2100)
    is_active: bool = True
