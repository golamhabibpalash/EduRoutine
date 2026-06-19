"""Unit of Work port — transactional boundary exposing repositories."""

from __future__ import annotations

from types import TracebackType
from typing import Protocol, runtime_checkable

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


@runtime_checkable
class UnitOfWork(Protocol):
    """Atomic transaction boundary that aggregates the domain repositories.

    Command handlers/services depend on this port; the infrastructure layer provides the
    SQLAlchemy implementation. Use as an async context manager:

        async with uow:
            await uow.users.add(user)
            await uow.commit()
    """

    # identity
    users: UserRepository
    roles: RoleRepository
    permissions: PermissionRepository
    claims: ClaimRepository
    # academic
    departments: DepartmentRepository
    sessions: SessionRepository
    semesters: SemesterRepository
    batches: BatchRepository
    sections: SectionRepository
    courses: CourseRepository
    # timetable
    periods: PeriodRepository
    # resources / people
    rooms: RoomRepository
    teachers: TeacherRepository
    students: StudentRepository

    async def __aenter__(self) -> UnitOfWork:
        """Begin a transaction."""
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Roll back on error; release resources."""
        ...

    async def flush(self) -> None:
        """Emit staged INSERT/UPDATEs to the DB without committing the transaction.

        Used to satisfy foreign keys when a parent row and its association rows are created
        in the same transaction (the parent must exist before the child INSERT).
        """
        ...

    async def commit(self) -> None:
        """Persist all staged changes."""
        ...

    async def rollback(self) -> None:
        """Discard all staged changes."""
        ...
