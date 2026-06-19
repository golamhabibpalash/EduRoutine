"""People repository ports."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from src.domain.people.entities.student import Student
from src.domain.people.entities.teacher import Teacher


class TeacherRepository(Protocol):
    """Persistence contract for :class:`Teacher`."""

    async def get(self, teacher_id: UUID) -> Teacher | None: ...
    async def get_by_employee_id(self, employee_id: str) -> Teacher | None: ...
    async def list_page(
        self, *, limit: int, offset: int, is_active: bool | None = None
    ) -> list[Teacher]: ...
    async def count(self, *, is_active: bool | None = None) -> int: ...
    async def add(self, teacher: Teacher) -> None: ...
    async def update(self, teacher: Teacher) -> None: ...
    async def delete(self, teacher: Teacher) -> None: ...


class StudentRepository(Protocol):
    """Persistence contract for :class:`Student`."""

    async def get(self, student_id: UUID) -> Student | None: ...
    async def get_by_student_id(self, student_id: str) -> Student | None: ...
    async def list_page(
        self,
        *,
        limit: int,
        offset: int,
        batch_id: UUID | None = None,
        section_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> list[Student]: ...
    async def count(
        self,
        *,
        batch_id: UUID | None = None,
        section_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> int: ...
    async def add(self, student: Student) -> None: ...
    async def update(self, student: Student) -> None: ...
    async def delete(self, student: Student) -> None: ...


__all__ = ["StudentRepository", "TeacherRepository"]
