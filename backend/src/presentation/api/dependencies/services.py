"""Application-service dependency providers (each enters a request-scoped UnitOfWork)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends

from src.application.academic.service import (
    BatchService,
    CourseService,
    DepartmentService,
    SectionService,
    SemesterService,
    SessionService,
)
from src.application.roles.service import RoleService
from src.application.users.service import UserService
from src.infrastructure.auth.password_hasher import Argon2PasswordHasher
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork


async def get_user_service() -> AsyncIterator[UserService]:
    """Yield a :class:`UserService` bound to a request-scoped UnitOfWork."""
    async with SqlAlchemyUnitOfWork() as uow:
        yield UserService(uow, Argon2PasswordHasher())


async def get_role_service() -> AsyncIterator[RoleService]:
    """Yield a :class:`RoleService` bound to a request-scoped UnitOfWork."""
    async with SqlAlchemyUnitOfWork() as uow:
        yield RoleService(uow)


async def get_department_service() -> AsyncIterator[DepartmentService]:
    async with SqlAlchemyUnitOfWork() as uow:
        yield DepartmentService(uow)


async def get_session_service() -> AsyncIterator[SessionService]:
    async with SqlAlchemyUnitOfWork() as uow:
        yield SessionService(uow)


async def get_semester_service() -> AsyncIterator[SemesterService]:
    async with SqlAlchemyUnitOfWork() as uow:
        yield SemesterService(uow)


async def get_batch_service() -> AsyncIterator[BatchService]:
    async with SqlAlchemyUnitOfWork() as uow:
        yield BatchService(uow)


async def get_section_service() -> AsyncIterator[SectionService]:
    async with SqlAlchemyUnitOfWork() as uow:
        yield SectionService(uow)


async def get_course_service() -> AsyncIterator[CourseService]:
    async with SqlAlchemyUnitOfWork() as uow:
        yield CourseService(uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
DepartmentServiceDep = Annotated[DepartmentService, Depends(get_department_service)]
SessionServiceDep = Annotated[SessionService, Depends(get_session_service)]
SemesterServiceDep = Annotated[SemesterService, Depends(get_semester_service)]
BatchServiceDep = Annotated[BatchService, Depends(get_batch_service)]
SectionServiceDep = Annotated[SectionService, Depends(get_section_service)]
CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]
