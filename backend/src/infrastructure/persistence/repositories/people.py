"""SQLAlchemy adapters for the people repository ports."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.people.entities.student import Student
from src.domain.people.entities.teacher import Teacher
from src.infrastructure.persistence.models.people import StudentModel, TeacherModel


class SqlAlchemyTeacherRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: TeacherModel) -> Teacher:
        return Teacher(
            id=m.id,
            employee_id=m.employee_id,
            name=m.name,
            email=m.email,
            phone=m.phone,
            department=m.department,
            specialization=list(m.specialization),
            max_hours_per_week=m.max_hours_per_week,
            is_active=m.is_active,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, teacher_id: UUID) -> Teacher | None:
        m = await self._session.get(TeacherModel, teacher_id)
        return self._to_domain(m) if m else None

    async def get_by_employee_id(self, employee_id: str) -> Teacher | None:
        r = await self._session.execute(
            select(TeacherModel).where(TeacherModel.employee_id == employee_id)
        )
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(
        self, *, limit: int, offset: int, is_active: bool | None = None
    ) -> list[Teacher]:
        stmt = select(TeacherModel).order_by(TeacherModel.employee_id)
        if is_active is not None:
            stmt = stmt.where(TeacherModel.is_active.is_(is_active))
        r = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_domain(m) for m in r.scalars()]

    async def count(self, *, is_active: bool | None = None) -> int:
        stmt = select(func.count()).select_from(TeacherModel)
        if is_active is not None:
            stmt = stmt.where(TeacherModel.is_active.is_(is_active))
        r = await self._session.execute(stmt)
        return int(r.scalar_one())

    async def add(self, teacher: Teacher) -> None:
        self._session.add(
            TeacherModel(
                id=teacher.id,
                employee_id=teacher.employee_id,
                name=teacher.name,
                email=teacher.email,
                phone=teacher.phone,
                department=teacher.department,
                specialization=list(teacher.specialization),
                max_hours_per_week=teacher.max_hours_per_week,
                is_active=teacher.is_active,
            )
        )

    async def update(self, teacher: Teacher) -> None:
        m = await self._session.get(TeacherModel, teacher.id)
        if m is None:
            return
        m.name = teacher.name
        m.email = teacher.email
        m.phone = teacher.phone
        m.department = teacher.department
        m.specialization = list(teacher.specialization)
        m.max_hours_per_week = teacher.max_hours_per_week
        m.is_active = teacher.is_active

    async def delete(self, teacher: Teacher) -> None:
        m = await self._session.get(TeacherModel, teacher.id)
        if m:
            await self._session.delete(m)


class SqlAlchemyStudentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: StudentModel) -> Student:
        return Student(
            id=m.id,
            student_id=m.student_id,
            name=m.name,
            email=m.email,
            phone=m.phone,
            batch_id=m.batch_id,
            section_id=m.section_id,
            enrollment_year=m.enrollment_year,
            is_active=m.is_active,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, student_id: UUID) -> Student | None:
        m = await self._session.get(StudentModel, student_id)
        return self._to_domain(m) if m else None

    async def get_by_student_id(self, student_id: str) -> Student | None:
        r = await self._session.execute(
            select(StudentModel).where(StudentModel.student_id == student_id)
        )
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(
        self,
        *,
        limit: int,
        offset: int,
        batch_id: UUID | None = None,
        section_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> list[Student]:
        stmt = select(StudentModel).order_by(StudentModel.student_id)
        if batch_id is not None:
            stmt = stmt.where(StudentModel.batch_id == batch_id)
        if section_id is not None:
            stmt = stmt.where(StudentModel.section_id == section_id)
        if is_active is not None:
            stmt = stmt.where(StudentModel.is_active.is_(is_active))
        r = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_domain(m) for m in r.scalars()]

    async def count(
        self,
        *,
        batch_id: UUID | None = None,
        section_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(StudentModel)
        if batch_id is not None:
            stmt = stmt.where(StudentModel.batch_id == batch_id)
        if section_id is not None:
            stmt = stmt.where(StudentModel.section_id == section_id)
        if is_active is not None:
            stmt = stmt.where(StudentModel.is_active.is_(is_active))
        r = await self._session.execute(stmt)
        return int(r.scalar_one())

    async def add(self, student: Student) -> None:
        self._session.add(
            StudentModel(
                id=student.id,
                student_id=student.student_id,
                name=student.name,
                email=student.email,
                phone=student.phone,
                batch_id=student.batch_id,
                section_id=student.section_id,
                enrollment_year=student.enrollment_year,
                is_active=student.is_active,
            )
        )

    async def update(self, student: Student) -> None:
        m = await self._session.get(StudentModel, student.id)
        if m is None:
            return
        m.name = student.name
        m.email = student.email
        m.phone = student.phone
        m.batch_id = student.batch_id
        m.section_id = student.section_id
        m.enrollment_year = student.enrollment_year
        m.is_active = student.is_active

    async def delete(self, student: Student) -> None:
        m = await self._session.get(StudentModel, student.id)
        if m:
            await self._session.delete(m)
