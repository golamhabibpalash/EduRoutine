"""SQLAlchemy Unit of Work — implements the application :class:`UnitOfWork` port."""

from __future__ import annotations

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.academic.repositories import (
    BatchRepository,
    CourseRepository,
    DepartmentRepository,
    SectionRepository,
    SemesterRepository,
    SessionRepository,
)
from src.domain.identity.repositories import (
    ClaimRepository,
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.domain.people.repositories import StudentRepository, TeacherRepository
from src.domain.resources.repositories import RoomRepository
from src.domain.timetable.repositories import PeriodRepository
from src.infrastructure.persistence.database import get_sessionmaker
from src.infrastructure.persistence.repositories import (
    SqlAlchemyClaimRepository,
    SqlAlchemyPermissionRepository,
    SqlAlchemyRoleRepository,
    SqlAlchemyUserRepository,
)
from src.infrastructure.persistence.repositories.academic import (
    SqlAlchemyBatchRepository,
    SqlAlchemyCourseRepository,
    SqlAlchemyDepartmentRepository,
    SqlAlchemySectionRepository,
    SqlAlchemySemesterRepository,
    SqlAlchemySessionRepository,
)
from src.infrastructure.persistence.repositories.people import (
    SqlAlchemyStudentRepository,
    SqlAlchemyTeacherRepository,
)
from src.infrastructure.persistence.repositories.resources import SqlAlchemyRoomRepository
from src.infrastructure.persistence.repositories.timetable import SqlAlchemyPeriodRepository


class SqlAlchemyUnitOfWork:
    """Owns an :class:`AsyncSession` and exposes the identity repositories.

    Begins a session/transaction on ``__aenter__`` and rolls back any uncommitted work on exit.
    """

    # Typed to the domain ports so the class satisfies the ``UnitOfWork`` protocol;
    # concrete adapters are bound in ``__aenter__``.
    users: UserRepository
    roles: RoleRepository
    permissions: PermissionRepository
    claims: ClaimRepository
    departments: DepartmentRepository
    sessions: SessionRepository
    semesters: SemesterRepository
    batches: BatchRepository
    sections: SectionRepository
    courses: CourseRepository
    periods: PeriodRepository
    rooms: RoomRepository
    teachers: TeacherRepository
    students: StudentRepository

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] | None = None) -> None:
        self._session_factory = session_factory or get_sessionmaker()
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> SqlAlchemyUnitOfWork:
        self._session = self._session_factory()
        self.users = SqlAlchemyUserRepository(self._session)
        self.roles = SqlAlchemyRoleRepository(self._session)
        self.permissions = SqlAlchemyPermissionRepository(self._session)
        self.claims = SqlAlchemyClaimRepository(self._session)
        self.departments = SqlAlchemyDepartmentRepository(self._session)
        self.sessions = SqlAlchemySessionRepository(self._session)
        self.semesters = SqlAlchemySemesterRepository(self._session)
        self.batches = SqlAlchemyBatchRepository(self._session)
        self.sections = SqlAlchemySectionRepository(self._session)
        self.courses = SqlAlchemyCourseRepository(self._session)
        self.periods = SqlAlchemyPeriodRepository(self._session)
        self.rooms = SqlAlchemyRoomRepository(self._session)
        self.teachers = SqlAlchemyTeacherRepository(self._session)
        self.students = SqlAlchemyStudentRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            if self._session is not None:
                await self._session.close()
                self._session = None

    @property
    def session(self) -> AsyncSession:
        """Return the active session (raises if used outside the context)."""
        if self._session is None:
            raise RuntimeError("UnitOfWork used outside of an active context.")
        return self._session

    async def flush(self) -> None:
        await self.session.flush()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
