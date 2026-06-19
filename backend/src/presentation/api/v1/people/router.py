"""Teachers & students API router (bare responses)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.common.dto.pagination import PageParams
from src.presentation.api.common.response_models import PaginatedResponse, paginate
from src.presentation.api.dependencies.auth import Principal, require_permission
from src.presentation.api.dependencies.services import StudentServiceDep, TeacherServiceDep
from src.presentation.api.v1.people.schemas import (
    CreateStudentRequest,
    CreateTeacherRequest,
    StudentData,
    TeacherData,
    UpdateStudentRequest,
    UpdateTeacherRequest,
)

router = APIRouter()

PageQ = Annotated[int, Query(ge=1)]
SizeQ = Annotated[int, Query(ge=1, le=100)]


# ============================================================ Teachers
@router.get("/teachers", response_model=PaginatedResponse[TeacherData], tags=["Teachers"])
async def list_teachers(
    service: TeacherServiceDep,
    _p: Annotated[Principal, Depends(require_permission("teacher:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
    is_active: Annotated[bool | None, Query()] = None,
) -> PaginatedResponse[TeacherData]:
    r = await service.list_teachers(PageParams(page, page_size), is_active=is_active)
    return paginate(
        [TeacherData.from_dto(t) for t in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/teachers", response_model=TeacherData, status_code=201, tags=["Teachers"])
async def create_teacher(
    body: CreateTeacherRequest,
    service: TeacherServiceDep,
    _p: Annotated[Principal, Depends(require_permission("teacher:create:*"))],
) -> TeacherData:
    dto = await service.create(
        employee_id=body.employee_id,
        name=body.name,
        email=body.email,
        department=body.department,
        phone=body.phone,
        specialization=body.specialization,
        max_hours_per_week=body.max_hours_per_week,
        is_active=body.is_active,
    )
    return TeacherData.from_dto(dto)


@router.get("/teachers/{teacher_id}", response_model=TeacherData, tags=["Teachers"])
async def get_teacher(
    teacher_id: UUID,
    service: TeacherServiceDep,
    _p: Annotated[Principal, Depends(require_permission("teacher:read:*"))],
) -> TeacherData:
    return TeacherData.from_dto(await service.get(teacher_id))


@router.put("/teachers/{teacher_id}", response_model=TeacherData, tags=["Teachers"])
async def update_teacher(
    teacher_id: UUID,
    body: UpdateTeacherRequest,
    service: TeacherServiceDep,
    _p: Annotated[Principal, Depends(require_permission("teacher:update:*"))],
) -> TeacherData:
    dto = await service.update(
        teacher_id,
        name=body.name,
        email=body.email,
        department=body.department,
        phone=body.phone,
        specialization=body.specialization,
        max_hours_per_week=body.max_hours_per_week,
        is_active=body.is_active,
    )
    return TeacherData.from_dto(dto)


@router.delete("/teachers/{teacher_id}", status_code=204, tags=["Teachers"])
async def delete_teacher(
    teacher_id: UUID,
    service: TeacherServiceDep,
    _p: Annotated[Principal, Depends(require_permission("teacher:delete:*"))],
) -> None:
    await service.delete(teacher_id)


# ============================================================ Students
@router.get("/students", response_model=PaginatedResponse[StudentData], tags=["Students"])
async def list_students(
    service: StudentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("student:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
    batch_id: Annotated[UUID | None, Query()] = None,
    section_id: Annotated[UUID | None, Query()] = None,
    is_active: Annotated[bool | None, Query()] = None,
) -> PaginatedResponse[StudentData]:
    r = await service.list_students(
        PageParams(page, page_size), batch_id=batch_id, section_id=section_id, is_active=is_active
    )
    return paginate(
        [StudentData.from_dto(s) for s in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/students", response_model=StudentData, status_code=201, tags=["Students"])
async def create_student(
    body: CreateStudentRequest,
    service: StudentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("student:create:*"))],
) -> StudentData:
    dto = await service.create(
        student_id=body.student_id,
        name=body.name,
        email=body.email,
        batch_id=body.batch_id,
        section_id=body.section_id,
        enrollment_year=body.enrollment_year,
        phone=body.phone,
        is_active=body.is_active,
    )
    return StudentData.from_dto(dto)


@router.get("/students/{student_pk}", response_model=StudentData, tags=["Students"])
async def get_student(
    student_pk: UUID,
    service: StudentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("student:read:*"))],
) -> StudentData:
    return StudentData.from_dto(await service.get(student_pk))


@router.put("/students/{student_pk}", response_model=StudentData, tags=["Students"])
async def update_student(
    student_pk: UUID,
    body: UpdateStudentRequest,
    service: StudentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("student:update:*"))],
) -> StudentData:
    dto = await service.update(
        student_pk,
        name=body.name,
        email=body.email,
        batch_id=body.batch_id,
        section_id=body.section_id,
        enrollment_year=body.enrollment_year,
        phone=body.phone,
        is_active=body.is_active,
    )
    return StudentData.from_dto(dto)


@router.delete("/students/{student_pk}", status_code=204, tags=["Students"])
async def delete_student(
    student_pk: UUID,
    service: StudentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("student:delete:*"))],
) -> None:
    await service.delete(student_pk)
