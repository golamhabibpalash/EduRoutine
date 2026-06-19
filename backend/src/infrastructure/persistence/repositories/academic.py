"""SQLAlchemy adapters for the academic repository ports."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.academic.entities.batch import Batch
from src.domain.academic.entities.course import Course
from src.domain.academic.entities.department import Department
from src.domain.academic.entities.section import Section
from src.domain.academic.entities.semester import Semester
from src.domain.academic.entities.session import Session
from src.infrastructure.persistence.models.academic import (
    BatchModel,
    CourseModel,
    CoursePrerequisiteModel,
    DepartmentModel,
    SectionModel,
    SemesterModel,
    SessionModel,
)


class SqlAlchemyDepartmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: DepartmentModel) -> Department:
        return Department(
            id=m.id, name=m.name, code=m.code, created_at=m.created_at, updated_at=m.updated_at
        )

    async def get(self, department_id: UUID) -> Department | None:
        m = await self._session.get(DepartmentModel, department_id)
        return self._to_domain(m) if m else None

    async def get_by_code(self, code: str) -> Department | None:
        r = await self._session.execute(select(DepartmentModel).where(DepartmentModel.code == code))
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(self, *, limit: int, offset: int) -> list[Department]:
        r = await self._session.execute(
            select(DepartmentModel).order_by(DepartmentModel.code).limit(limit).offset(offset)
        )
        return [self._to_domain(m) for m in r.scalars()]

    async def count(self) -> int:
        r = await self._session.execute(select(func.count()).select_from(DepartmentModel))
        return int(r.scalar_one())

    async def add(self, department: Department) -> None:
        self._session.add(
            DepartmentModel(id=department.id, name=department.name, code=department.code)
        )

    async def update(self, department: Department) -> None:
        m = await self._session.get(DepartmentModel, department.id)
        if m is None:
            return
        m.name = department.name
        m.code = department.code

    async def delete(self, department: Department) -> None:
        m = await self._session.get(DepartmentModel, department.id)
        if m:
            await self._session.delete(m)


class SqlAlchemySessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: SessionModel) -> Session:
        return Session(
            id=m.id,
            name=m.name,
            start_date=m.start_date,
            end_date=m.end_date,
            is_current=m.is_current,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, session_id: UUID) -> Session | None:
        m = await self._session.get(SessionModel, session_id)
        return self._to_domain(m) if m else None

    async def list_page(
        self, *, limit: int, offset: int, is_current: bool | None = None
    ) -> list[Session]:
        stmt = select(SessionModel).order_by(SessionModel.start_date.desc())
        if is_current is not None:
            stmt = stmt.where(SessionModel.is_current.is_(is_current))
        r = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_domain(m) for m in r.scalars()]

    async def count(self, *, is_current: bool | None = None) -> int:
        stmt = select(func.count()).select_from(SessionModel)
        if is_current is not None:
            stmt = stmt.where(SessionModel.is_current.is_(is_current))
        r = await self._session.execute(stmt)
        return int(r.scalar_one())

    async def add(self, session: Session) -> None:
        self._session.add(
            SessionModel(
                id=session.id,
                name=session.name,
                start_date=session.start_date,
                end_date=session.end_date,
                is_current=session.is_current,
            )
        )

    async def update(self, session: Session) -> None:
        m = await self._session.get(SessionModel, session.id)
        if m is None:
            return
        m.name = session.name
        m.start_date = session.start_date
        m.end_date = session.end_date
        m.is_current = session.is_current

    async def delete(self, session: Session) -> None:
        m = await self._session.get(SessionModel, session.id)
        if m:
            await self._session.delete(m)

    async def set_current(self, session_id: UUID) -> None:
        await self._session.execute(update(SessionModel).values(is_current=False))
        await self._session.execute(
            update(SessionModel).where(SessionModel.id == session_id).values(is_current=True)
        )


class SqlAlchemySemesterRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: SemesterModel) -> Semester:
        return Semester(
            id=m.id,
            session_id=m.session_id,
            name=m.name,
            number=m.number,
            start_date=m.start_date,
            end_date=m.end_date,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, semester_id: UUID) -> Semester | None:
        m = await self._session.get(SemesterModel, semester_id)
        return self._to_domain(m) if m else None

    async def get_by_session_and_number(self, session_id: UUID, number: int) -> Semester | None:
        r = await self._session.execute(
            select(SemesterModel).where(
                SemesterModel.session_id == session_id, SemesterModel.number == number
            )
        )
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(
        self, *, limit: int, offset: int, session_id: UUID | None = None
    ) -> list[Semester]:
        stmt = select(SemesterModel).order_by(SemesterModel.number)
        if session_id is not None:
            stmt = stmt.where(SemesterModel.session_id == session_id)
        r = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_domain(m) for m in r.scalars()]

    async def count(self, *, session_id: UUID | None = None) -> int:
        stmt = select(func.count()).select_from(SemesterModel)
        if session_id is not None:
            stmt = stmt.where(SemesterModel.session_id == session_id)
        r = await self._session.execute(stmt)
        return int(r.scalar_one())

    async def add(self, semester: Semester) -> None:
        self._session.add(
            SemesterModel(
                id=semester.id,
                session_id=semester.session_id,
                name=semester.name,
                number=semester.number,
                start_date=semester.start_date,
                end_date=semester.end_date,
            )
        )

    async def update(self, semester: Semester) -> None:
        m = await self._session.get(SemesterModel, semester.id)
        if m is None:
            return
        m.name = semester.name
        m.number = semester.number
        m.start_date = semester.start_date
        m.end_date = semester.end_date

    async def delete(self, semester: Semester) -> None:
        m = await self._session.get(SemesterModel, semester.id)
        if m:
            await self._session.delete(m)


class SqlAlchemyBatchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: BatchModel) -> Batch:
        return Batch(
            id=m.id,
            session_id=m.session_id,
            department_id=m.department_id,
            name=m.name,
            code=m.code,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, batch_id: UUID) -> Batch | None:
        m = await self._session.get(BatchModel, batch_id)
        return self._to_domain(m) if m else None

    async def get_by_code(self, code: str) -> Batch | None:
        r = await self._session.execute(select(BatchModel).where(BatchModel.code == code))
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(
        self,
        *,
        limit: int,
        offset: int,
        session_id: UUID | None = None,
        department_id: UUID | None = None,
    ) -> list[Batch]:
        stmt = select(BatchModel).order_by(BatchModel.code)
        if session_id is not None:
            stmt = stmt.where(BatchModel.session_id == session_id)
        if department_id is not None:
            stmt = stmt.where(BatchModel.department_id == department_id)
        r = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_domain(m) for m in r.scalars()]

    async def count(
        self, *, session_id: UUID | None = None, department_id: UUID | None = None
    ) -> int:
        stmt = select(func.count()).select_from(BatchModel)
        if session_id is not None:
            stmt = stmt.where(BatchModel.session_id == session_id)
        if department_id is not None:
            stmt = stmt.where(BatchModel.department_id == department_id)
        r = await self._session.execute(stmt)
        return int(r.scalar_one())

    async def add(self, batch: Batch) -> None:
        self._session.add(
            BatchModel(
                id=batch.id,
                session_id=batch.session_id,
                department_id=batch.department_id,
                name=batch.name,
                code=batch.code,
            )
        )

    async def update(self, batch: Batch) -> None:
        m = await self._session.get(BatchModel, batch.id)
        if m is None:
            return
        m.name = batch.name
        m.code = batch.code

    async def delete(self, batch: Batch) -> None:
        m = await self._session.get(BatchModel, batch.id)
        if m:
            await self._session.delete(m)


class SqlAlchemySectionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: SectionModel) -> Section:
        return Section(
            id=m.id,
            batch_id=m.batch_id,
            name=m.name,
            max_capacity=m.max_capacity,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, section_id: UUID) -> Section | None:
        m = await self._session.get(SectionModel, section_id)
        return self._to_domain(m) if m else None

    async def get_by_batch_and_name(self, batch_id: UUID, name: str) -> Section | None:
        r = await self._session.execute(
            select(SectionModel).where(SectionModel.batch_id == batch_id, SectionModel.name == name)
        )
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(
        self, *, limit: int, offset: int, batch_id: UUID | None = None
    ) -> list[Section]:
        stmt = select(SectionModel).order_by(SectionModel.name)
        if batch_id is not None:
            stmt = stmt.where(SectionModel.batch_id == batch_id)
        r = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_domain(m) for m in r.scalars()]

    async def count(self, *, batch_id: UUID | None = None) -> int:
        stmt = select(func.count()).select_from(SectionModel)
        if batch_id is not None:
            stmt = stmt.where(SectionModel.batch_id == batch_id)
        r = await self._session.execute(stmt)
        return int(r.scalar_one())

    async def list_for_batch(self, batch_id: UUID) -> list[Section]:
        r = await self._session.execute(
            select(SectionModel)
            .where(SectionModel.batch_id == batch_id)
            .order_by(SectionModel.name)
        )
        return [self._to_domain(m) for m in r.scalars()]

    async def add(self, section: Section) -> None:
        self._session.add(
            SectionModel(
                id=section.id,
                batch_id=section.batch_id,
                name=section.name,
                max_capacity=section.max_capacity,
            )
        )

    async def update(self, section: Section) -> None:
        m = await self._session.get(SectionModel, section.id)
        if m is None:
            return
        m.name = section.name
        m.max_capacity = section.max_capacity

    async def delete(self, section: Section) -> None:
        m = await self._session.get(SectionModel, section.id)
        if m:
            await self._session.delete(m)


class SqlAlchemyCourseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: CourseModel) -> Course:
        return Course(
            id=m.id,
            department_id=m.department_id,
            code=m.code,
            title=m.title,
            credits=m.credits,
            lecture_hours=m.lecture_hours,
            lab_hours=m.lab_hours,
            is_active=m.is_active,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, course_id: UUID) -> Course | None:
        m = await self._session.get(CourseModel, course_id)
        return self._to_domain(m) if m else None

    async def get_by_code(self, code: str) -> Course | None:
        r = await self._session.execute(select(CourseModel).where(CourseModel.code == code))
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(
        self,
        *,
        limit: int,
        offset: int,
        department_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> list[Course]:
        stmt = select(CourseModel).order_by(CourseModel.code)
        if department_id is not None:
            stmt = stmt.where(CourseModel.department_id == department_id)
        if is_active is not None:
            stmt = stmt.where(CourseModel.is_active.is_(is_active))
        r = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_domain(m) for m in r.scalars()]

    async def count(
        self, *, department_id: UUID | None = None, is_active: bool | None = None
    ) -> int:
        stmt = select(func.count()).select_from(CourseModel)
        if department_id is not None:
            stmt = stmt.where(CourseModel.department_id == department_id)
        if is_active is not None:
            stmt = stmt.where(CourseModel.is_active.is_(is_active))
        r = await self._session.execute(stmt)
        return int(r.scalar_one())

    async def add(self, course: Course) -> None:
        self._session.add(
            CourseModel(
                id=course.id,
                department_id=course.department_id,
                code=course.code,
                title=course.title,
                credits=course.credits,
                lecture_hours=course.lecture_hours,
                lab_hours=course.lab_hours,
                is_active=course.is_active,
            )
        )

    async def update(self, course: Course) -> None:
        m = await self._session.get(CourseModel, course.id)
        if m is None:
            return
        m.title = course.title
        m.credits = course.credits
        m.lecture_hours = course.lecture_hours
        m.lab_hours = course.lab_hours
        m.is_active = course.is_active

    async def delete(self, course: Course) -> None:
        m = await self._session.get(CourseModel, course.id)
        if m:
            await self._session.delete(m)

    async def get_prerequisite_ids(self, course_id: UUID) -> set[UUID]:
        r = await self._session.execute(
            select(CoursePrerequisiteModel.prerequisite_course_id).where(
                CoursePrerequisiteModel.course_id == course_id
            )
        )
        return set(r.scalars())

    async def add_prerequisite(self, course_id: UUID, prerequisite_id: UUID) -> None:
        self._session.add(
            CoursePrerequisiteModel(course_id=course_id, prerequisite_course_id=prerequisite_id)
        )

    async def remove_prerequisite(self, course_id: UUID, prerequisite_id: UUID) -> None:
        await self._session.execute(
            delete(CoursePrerequisiteModel).where(
                CoursePrerequisiteModel.course_id == course_id,
                CoursePrerequisiteModel.prerequisite_course_id == prerequisite_id,
            )
        )

    async def prerequisite_exists(self, course_id: UUID, prerequisite_id: UUID) -> bool:
        r = await self._session.execute(
            select(CoursePrerequisiteModel.course_id).where(
                CoursePrerequisiteModel.course_id == course_id,
                CoursePrerequisiteModel.prerequisite_course_id == prerequisite_id,
            )
        )
        return r.scalar() is not None

    async def list_prerequisites(self, course_id: UUID) -> list[Course]:
        r = await self._session.execute(
            select(CourseModel)
            .join(
                CoursePrerequisiteModel,
                CoursePrerequisiteModel.prerequisite_course_id == CourseModel.id,
            )
            .where(CoursePrerequisiteModel.course_id == course_id)
            .order_by(CourseModel.code)
        )
        return [self._to_domain(m) for m in r.scalars()]
