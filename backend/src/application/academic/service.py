"""Academic Structure application services."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from src.application.academic.dto import (
    BatchDTO,
    CourseDTO,
    DepartmentDTO,
    SectionDTO,
    SemesterDTO,
    SessionDTO,
)
from src.application.common.dto.pagination import Page, PageParams
from src.application.common.exceptions import ConflictError, ValidationError
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.domain.academic.entities.batch import Batch
from src.domain.academic.entities.course import Course
from src.domain.academic.entities.department import Department
from src.domain.academic.entities.section import Section
from src.domain.academic.entities.semester import Semester
from src.domain.academic.entities.session import Session
from src.domain.academic.exceptions import (
    BatchNotFoundError,
    CourseNotFoundError,
    DepartmentNotFoundError,
    SectionNotFoundError,
    SemesterNotFoundError,
    SessionNotFoundError,
)
from src.shared.utils.clock import utcnow


# ============================================================ Departments
class DepartmentService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @staticmethod
    def _dto(d: Department) -> DepartmentDTO:
        return DepartmentDTO(id=d.id, name=d.name, code=d.code, created_at=d.created_at or utcnow())

    async def get(self, department_id: UUID) -> DepartmentDTO:
        d = await self._uow.departments.get(department_id)
        if d is None:
            raise DepartmentNotFoundError(f"Department '{department_id}' not found.")
        return self._dto(d)

    async def list_departments(self, page: PageParams) -> Page[DepartmentDTO]:
        items = await self._uow.departments.list_page(limit=page.limit, offset=page.offset)
        total = await self._uow.departments.count()
        return Page([self._dto(d) for d in items], page.page, page.page_size, total)

    async def create(self, *, name: str, code: str) -> DepartmentDTO:
        if await self._uow.departments.get_by_code(code) is not None:
            raise ConflictError(f"A department with code '{code}' already exists.")
        d = Department(id=uuid4(), name=name, code=code)
        await self._uow.departments.add(d)
        await self._uow.commit()
        return self._dto(d)

    async def update(self, department_id: UUID, *, name: str, code: str) -> DepartmentDTO:
        d = await self._uow.departments.get(department_id)
        if d is None:
            raise DepartmentNotFoundError(f"Department '{department_id}' not found.")
        existing = await self._uow.departments.get_by_code(code)
        if existing is not None and existing.id != department_id:
            raise ConflictError(f"A department with code '{code}' already exists.")
        d.name, d.code = name, code
        await self._uow.departments.update(d)
        await self._uow.commit()
        return self._dto(d)

    async def delete(self, department_id: UUID) -> None:
        d = await self._uow.departments.get(department_id)
        if d is None:
            raise DepartmentNotFoundError(f"Department '{department_id}' not found.")
        await self._uow.departments.delete(d)
        await self._uow.commit()


# ============================================================ Sessions
class SessionService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @staticmethod
    def _dto(s: Session) -> SessionDTO:
        return SessionDTO(
            id=s.id,
            name=s.name,
            start_date=s.start_date,
            end_date=s.end_date,
            is_current=s.is_current,
            created_at=s.created_at or utcnow(),
        )

    async def get(self, session_id: UUID) -> SessionDTO:
        s = await self._require(session_id)
        return self._dto(s)

    async def list_sessions(
        self, page: PageParams, *, is_current: bool | None = None
    ) -> Page[SessionDTO]:
        items = await self._uow.sessions.list_page(
            limit=page.limit, offset=page.offset, is_current=is_current
        )
        total = await self._uow.sessions.count(is_current=is_current)
        return Page([self._dto(s) for s in items], page.page, page.page_size, total)

    async def create(
        self, *, name: str, start_date: date, end_date: date, is_current: bool = False
    ) -> SessionDTO:
        _validate_dates(start_date, end_date)
        s = Session(
            id=uuid4(), name=name, start_date=start_date, end_date=end_date, is_current=False
        )
        await self._uow.sessions.add(s)
        await self._uow.flush()
        if is_current:
            await self._uow.sessions.set_current(s.id)
            s.is_current = True
        await self._uow.commit()
        return self._dto(s)

    async def update(
        self, session_id: UUID, *, name: str, start_date: date, end_date: date
    ) -> SessionDTO:
        s = await self._require(session_id)
        _validate_dates(start_date, end_date)
        s.name, s.start_date, s.end_date = name, start_date, end_date
        await self._uow.sessions.update(s)
        await self._uow.commit()
        return self._dto(s)

    async def activate(self, session_id: UUID) -> SessionDTO:
        await self._require(session_id)
        await self._uow.sessions.set_current(session_id)
        await self._uow.commit()
        return await self.get(session_id)

    async def delete(self, session_id: UUID) -> None:
        s = await self._require(session_id)
        await self._uow.sessions.delete(s)
        await self._uow.commit()

    async def _require(self, session_id: UUID) -> Session:
        s = await self._uow.sessions.get(session_id)
        if s is None:
            raise SessionNotFoundError(f"Session '{session_id}' not found.")
        return s


# ============================================================ Semesters
class SemesterService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @staticmethod
    def _dto(s: Semester) -> SemesterDTO:
        return SemesterDTO(
            id=s.id,
            session_id=s.session_id,
            name=s.name,
            number=s.number,
            start_date=s.start_date,
            end_date=s.end_date,
            created_at=s.created_at or utcnow(),
        )

    async def get(self, semester_id: UUID) -> SemesterDTO:
        s = await self._require(semester_id)
        return self._dto(s)

    async def list_semesters(
        self, page: PageParams, *, session_id: UUID | None = None
    ) -> Page[SemesterDTO]:
        items = await self._uow.semesters.list_page(
            limit=page.limit, offset=page.offset, session_id=session_id
        )
        total = await self._uow.semesters.count(session_id=session_id)
        return Page([self._dto(s) for s in items], page.page, page.page_size, total)

    async def create(
        self, *, session_id: UUID, name: str, number: int, start_date: date, end_date: date
    ) -> SemesterDTO:
        if await self._uow.sessions.get(session_id) is None:
            raise ValidationError(f"Session '{session_id}' does not exist.")
        _validate_dates(start_date, end_date)
        if await self._uow.semesters.get_by_session_and_number(session_id, number) is not None:
            raise ConflictError(f"Semester number {number} already exists in this session.")
        s = Semester(
            id=uuid4(),
            session_id=session_id,
            name=name,
            number=number,
            start_date=start_date,
            end_date=end_date,
        )
        await self._uow.semesters.add(s)
        await self._uow.commit()
        return self._dto(s)

    async def update(
        self, semester_id: UUID, *, name: str, number: int, start_date: date, end_date: date
    ) -> SemesterDTO:
        s = await self._require(semester_id)
        _validate_dates(start_date, end_date)
        other = await self._uow.semesters.get_by_session_and_number(s.session_id, number)
        if other is not None and other.id != semester_id:
            raise ConflictError(f"Semester number {number} already exists in this session.")
        s.name, s.number, s.start_date, s.end_date = name, number, start_date, end_date
        await self._uow.semesters.update(s)
        await self._uow.commit()
        return self._dto(s)

    async def delete(self, semester_id: UUID) -> None:
        s = await self._require(semester_id)
        await self._uow.semesters.delete(s)
        await self._uow.commit()

    async def _require(self, semester_id: UUID) -> Semester:
        s = await self._uow.semesters.get(semester_id)
        if s is None:
            raise SemesterNotFoundError(f"Semester '{semester_id}' not found.")
        return s


# ============================================================ Batches
class BatchService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @staticmethod
    def _dto(b: Batch) -> BatchDTO:
        return BatchDTO(
            id=b.id,
            session_id=b.session_id,
            department_id=b.department_id,
            name=b.name,
            code=b.code,
            created_at=b.created_at or utcnow(),
        )

    async def get(self, batch_id: UUID) -> BatchDTO:
        b = await self._require(batch_id)
        return self._dto(b)

    async def list_batches(
        self,
        page: PageParams,
        *,
        session_id: UUID | None = None,
        department_id: UUID | None = None,
    ) -> Page[BatchDTO]:
        items = await self._uow.batches.list_page(
            limit=page.limit, offset=page.offset, session_id=session_id, department_id=department_id
        )
        total = await self._uow.batches.count(session_id=session_id, department_id=department_id)
        return Page([self._dto(b) for b in items], page.page, page.page_size, total)

    async def create(
        self, *, session_id: UUID, department_id: UUID, name: str, code: str
    ) -> BatchDTO:
        if await self._uow.sessions.get(session_id) is None:
            raise ValidationError(f"Session '{session_id}' does not exist.")
        if await self._uow.departments.get(department_id) is None:
            raise ValidationError(f"Department '{department_id}' does not exist.")
        if await self._uow.batches.get_by_code(code) is not None:
            raise ConflictError(f"A batch with code '{code}' already exists.")
        b = Batch(
            id=uuid4(), session_id=session_id, department_id=department_id, name=name, code=code
        )
        await self._uow.batches.add(b)
        await self._uow.commit()
        return self._dto(b)

    async def update(self, batch_id: UUID, *, name: str, code: str) -> BatchDTO:
        b = await self._require(batch_id)
        existing = await self._uow.batches.get_by_code(code)
        if existing is not None and existing.id != batch_id:
            raise ConflictError(f"A batch with code '{code}' already exists.")
        b.name, b.code = name, code
        await self._uow.batches.update(b)
        await self._uow.commit()
        return self._dto(b)

    async def delete(self, batch_id: UUID) -> None:
        b = await self._require(batch_id)
        await self._uow.batches.delete(b)
        await self._uow.commit()

    async def list_sections(self, batch_id: UUID) -> list[SectionDTO]:
        await self._require(batch_id)
        sections = await self._uow.sections.list_for_batch(batch_id)
        return [
            SectionDTO(
                id=s.id,
                batch_id=s.batch_id,
                name=s.name,
                max_capacity=s.max_capacity,
                created_at=s.created_at or utcnow(),
            )
            for s in sections
        ]

    async def _require(self, batch_id: UUID) -> Batch:
        b = await self._uow.batches.get(batch_id)
        if b is None:
            raise BatchNotFoundError(f"Batch '{batch_id}' not found.")
        return b


# ============================================================ Sections
class SectionService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @staticmethod
    def _dto(s: Section) -> SectionDTO:
        return SectionDTO(
            id=s.id,
            batch_id=s.batch_id,
            name=s.name,
            max_capacity=s.max_capacity,
            created_at=s.created_at or utcnow(),
        )

    async def get(self, section_id: UUID) -> SectionDTO:
        s = await self._require(section_id)
        return self._dto(s)

    async def list_sections(
        self, page: PageParams, *, batch_id: UUID | None = None
    ) -> Page[SectionDTO]:
        items = await self._uow.sections.list_page(
            limit=page.limit, offset=page.offset, batch_id=batch_id
        )
        total = await self._uow.sections.count(batch_id=batch_id)
        return Page([self._dto(s) for s in items], page.page, page.page_size, total)

    async def create(self, *, batch_id: UUID, name: str, max_capacity: int) -> SectionDTO:
        if await self._uow.batches.get(batch_id) is None:
            raise ValidationError(f"Batch '{batch_id}' does not exist.")
        if await self._uow.sections.get_by_batch_and_name(batch_id, name) is not None:
            raise ConflictError(f"Section '{name}' already exists in this batch.")
        s = Section(id=uuid4(), batch_id=batch_id, name=name, max_capacity=max_capacity)
        await self._uow.sections.add(s)
        await self._uow.commit()
        return self._dto(s)

    async def update(self, section_id: UUID, *, name: str, max_capacity: int) -> SectionDTO:
        s = await self._require(section_id)
        other = await self._uow.sections.get_by_batch_and_name(s.batch_id, name)
        if other is not None and other.id != section_id:
            raise ConflictError(f"Section '{name}' already exists in this batch.")
        s.name, s.max_capacity = name, max_capacity
        await self._uow.sections.update(s)
        await self._uow.commit()
        return self._dto(s)

    async def delete(self, section_id: UUID) -> None:
        s = await self._require(section_id)
        await self._uow.sections.delete(s)
        await self._uow.commit()

    async def _require(self, section_id: UUID) -> Section:
        s = await self._uow.sections.get(section_id)
        if s is None:
            raise SectionNotFoundError(f"Section '{section_id}' not found.")
        return s


# ============================================================ Courses
class CourseService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def _dto(self, c: Course) -> CourseDTO:
        dept = await self._uow.departments.get(c.department_id)
        return CourseDTO(
            id=c.id,
            department_id=c.department_id,
            department_name=dept.name if dept else "",
            code=c.code,
            title=c.title,
            credits=c.credits,
            lecture_hours=c.lecture_hours,
            lab_hours=c.lab_hours,
            is_active=c.is_active,
            created_at=c.created_at or utcnow(),
        )

    async def get(self, course_id: UUID) -> CourseDTO:
        c = await self._require(course_id)
        return await self._dto(c)

    async def list_courses(
        self,
        page: PageParams,
        *,
        department_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> Page[CourseDTO]:
        items = await self._uow.courses.list_page(
            limit=page.limit, offset=page.offset, department_id=department_id, is_active=is_active
        )
        total = await self._uow.courses.count(department_id=department_id, is_active=is_active)
        return Page([await self._dto(c) for c in items], page.page, page.page_size, total)

    async def create(
        self,
        *,
        department_id: UUID,
        code: str,
        title: str,
        credits: Decimal,
        lecture_hours: int,
        lab_hours: int,
        prerequisite_ids: tuple[UUID, ...] = (),
    ) -> CourseDTO:
        if await self._uow.departments.get(department_id) is None:
            raise ValidationError(f"Department '{department_id}' does not exist.")
        if await self._uow.courses.get_by_code(code) is not None:
            raise ConflictError(f"A course with code '{code}' already exists.")
        for pid in prerequisite_ids:
            if await self._uow.courses.get(pid) is None:
                raise ValidationError(f"Prerequisite course '{pid}' does not exist.")
        c = Course(
            id=uuid4(),
            department_id=department_id,
            code=code,
            title=title,
            credits=credits,
            lecture_hours=lecture_hours,
            lab_hours=lab_hours,
        )
        await self._uow.courses.add(c)
        await self._uow.flush()
        for pid in set(prerequisite_ids):
            await self._uow.courses.add_prerequisite(c.id, pid)
        await self._uow.commit()
        return await self._dto(c)

    async def update(
        self,
        course_id: UUID,
        *,
        title: str,
        credits: Decimal,
        lecture_hours: int,
        lab_hours: int,
        is_active: bool,
    ) -> CourseDTO:
        c = await self._require(course_id)
        c.title, c.credits = title, credits
        c.lecture_hours, c.lab_hours, c.is_active = lecture_hours, lab_hours, is_active
        await self._uow.courses.update(c)
        await self._uow.commit()
        return await self._dto(c)

    async def deactivate(self, course_id: UUID) -> None:
        c = await self._require(course_id)
        c.deactivate()
        await self._uow.courses.update(c)
        await self._uow.commit()

    async def list_prerequisites(self, course_id: UUID) -> list[CourseDTO]:
        await self._require(course_id)
        return [await self._dto(c) for c in await self._uow.courses.list_prerequisites(course_id)]

    async def add_prerequisite(self, course_id: UUID, prerequisite_id: UUID) -> None:
        await self._require(course_id)
        if prerequisite_id == course_id:
            raise ValidationError("A course cannot be its own prerequisite.")
        if await self._uow.courses.get(prerequisite_id) is None:
            raise ValidationError(f"Prerequisite course '{prerequisite_id}' does not exist.")
        if await self._uow.courses.prerequisite_exists(course_id, prerequisite_id):
            raise ConflictError("This prerequisite is already set.")
        await self._uow.courses.add_prerequisite(course_id, prerequisite_id)
        await self._uow.commit()

    async def remove_prerequisite(self, course_id: UUID, prerequisite_id: UUID) -> None:
        await self._require(course_id)
        await self._uow.courses.remove_prerequisite(course_id, prerequisite_id)
        await self._uow.commit()

    async def _require(self, course_id: UUID) -> Course:
        c = await self._uow.courses.get(course_id)
        if c is None:
            raise CourseNotFoundError(f"Course '{course_id}' not found.")
        return c


def _validate_dates(start_date: date, end_date: date) -> None:
    if end_date <= start_date:
        raise ValidationError("end_date must be after start_date.")
