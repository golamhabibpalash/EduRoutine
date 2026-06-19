"""People Management application services."""

from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID, uuid4

from src.application.common.dto.pagination import Page, PageParams
from src.application.common.exceptions import ConflictError, ValidationError
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.people.dto import StudentDTO, TeacherDTO
from src.domain.people.entities.student import Student
from src.domain.people.entities.teacher import Teacher
from src.domain.people.exceptions import StudentNotFoundError, TeacherNotFoundError
from src.shared.utils.clock import utcnow


class TeacherService:
    """Use cases for the Teachers module."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @staticmethod
    def _dto(t: Teacher) -> TeacherDTO:
        return TeacherDTO(
            id=t.id,
            employee_id=t.employee_id,
            name=t.name,
            email=t.email,
            phone=t.phone,
            department=t.department,
            specialization=tuple(t.specialization),
            max_hours_per_week=t.max_hours_per_week,
            is_active=t.is_active,
            created_at=t.created_at or utcnow(),
            updated_at=t.updated_at or utcnow(),
        )

    async def get(self, teacher_id: UUID) -> TeacherDTO:
        return self._dto(await self._require(teacher_id))

    async def list_teachers(
        self, page: PageParams, *, is_active: bool | None = None
    ) -> Page[TeacherDTO]:
        items = await self._uow.teachers.list_page(
            limit=page.limit, offset=page.offset, is_active=is_active
        )
        total = await self._uow.teachers.count(is_active=is_active)
        return Page([self._dto(t) for t in items], page.page, page.page_size, total)

    async def create(
        self,
        *,
        employee_id: str,
        name: str,
        email: str,
        department: str,
        phone: str | None = None,
        specialization: Sequence[str] = (),
        max_hours_per_week: int = 30,
        is_active: bool = True,
    ) -> TeacherDTO:
        if await self._uow.teachers.get_by_employee_id(employee_id) is not None:
            raise ConflictError(f"A teacher with employee id '{employee_id}' already exists.")
        teacher = Teacher(
            id=uuid4(),
            employee_id=employee_id,
            name=name,
            email=email,
            department=department,
            phone=phone,
            specialization=list(specialization),
            max_hours_per_week=max_hours_per_week,
            is_active=is_active,
        )
        await self._uow.teachers.add(teacher)
        await self._uow.commit()
        return self._dto(teacher)

    async def update(
        self,
        teacher_id: UUID,
        *,
        name: str,
        email: str,
        department: str,
        phone: str | None,
        specialization: Sequence[str],
        max_hours_per_week: int,
        is_active: bool,
    ) -> TeacherDTO:
        teacher = await self._require(teacher_id)
        teacher.name = name
        teacher.email = email
        teacher.department = department
        teacher.phone = phone
        teacher.specialization = list(specialization)
        teacher.max_hours_per_week = max_hours_per_week
        teacher.is_active = is_active
        await self._uow.teachers.update(teacher)
        await self._uow.commit()
        return self._dto(teacher)

    async def delete(self, teacher_id: UUID) -> None:
        teacher = await self._require(teacher_id)
        await self._uow.teachers.delete(teacher)
        await self._uow.commit()

    async def _require(self, teacher_id: UUID) -> Teacher:
        teacher = await self._uow.teachers.get(teacher_id)
        if teacher is None:
            raise TeacherNotFoundError(f"Teacher '{teacher_id}' not found.")
        return teacher


class StudentService:
    """Use cases for the Students module."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def _dto(self, s: Student) -> StudentDTO:
        batch = await self._uow.batches.get(s.batch_id)
        section = await self._uow.sections.get(s.section_id)
        return StudentDTO(
            id=s.id,
            student_id=s.student_id,
            name=s.name,
            email=s.email,
            phone=s.phone,
            batch_id=s.batch_id,
            batch_name=batch.name if batch else None,
            section_id=s.section_id,
            section_name=section.name if section else None,
            enrollment_year=s.enrollment_year,
            is_active=s.is_active,
            created_at=s.created_at or utcnow(),
            updated_at=s.updated_at or utcnow(),
        )

    async def get(self, student_pk: UUID) -> StudentDTO:
        return await self._dto(await self._require(student_pk))

    async def list_students(
        self,
        page: PageParams,
        *,
        batch_id: UUID | None = None,
        section_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> Page[StudentDTO]:
        items = await self._uow.students.list_page(
            limit=page.limit,
            offset=page.offset,
            batch_id=batch_id,
            section_id=section_id,
            is_active=is_active,
        )
        total = await self._uow.students.count(
            batch_id=batch_id, section_id=section_id, is_active=is_active
        )
        return Page([await self._dto(s) for s in items], page.page, page.page_size, total)

    async def create(
        self,
        *,
        student_id: str,
        name: str,
        email: str,
        batch_id: UUID,
        section_id: UUID,
        enrollment_year: int,
        phone: str | None = None,
        is_active: bool = True,
    ) -> StudentDTO:
        if await self._uow.students.get_by_student_id(student_id) is not None:
            raise ConflictError(f"A student with id '{student_id}' already exists.")
        await self._validate_batch_section(batch_id, section_id)
        student = Student(
            id=uuid4(),
            student_id=student_id,
            name=name,
            email=email,
            batch_id=batch_id,
            section_id=section_id,
            enrollment_year=enrollment_year,
            phone=phone,
            is_active=is_active,
        )
        await self._uow.students.add(student)
        await self._uow.commit()
        return await self._dto(student)

    async def update(
        self,
        student_pk: UUID,
        *,
        name: str,
        email: str,
        batch_id: UUID,
        section_id: UUID,
        enrollment_year: int,
        phone: str | None,
        is_active: bool,
    ) -> StudentDTO:
        student = await self._require(student_pk)
        await self._validate_batch_section(batch_id, section_id)
        student.name = name
        student.email = email
        student.batch_id = batch_id
        student.section_id = section_id
        student.enrollment_year = enrollment_year
        student.phone = phone
        student.is_active = is_active
        await self._uow.students.update(student)
        await self._uow.commit()
        return await self._dto(student)

    async def delete(self, student_pk: UUID) -> None:
        student = await self._require(student_pk)
        await self._uow.students.delete(student)
        await self._uow.commit()

    async def _validate_batch_section(self, batch_id: UUID, section_id: UUID) -> None:
        if await self._uow.batches.get(batch_id) is None:
            raise ValidationError(f"Batch '{batch_id}' does not exist.")
        section = await self._uow.sections.get(section_id)
        if section is None:
            raise ValidationError(f"Section '{section_id}' does not exist.")
        if section.batch_id != batch_id:
            raise ValidationError("Section does not belong to the given batch.")

    async def _require(self, student_pk: UUID) -> Student:
        student = await self._uow.students.get(student_pk)
        if student is None:
            raise StudentNotFoundError(f"Student '{student_pk}' not found.")
        return student
