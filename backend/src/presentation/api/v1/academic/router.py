"""Academic Structure API router (bare responses)."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.common.dto.pagination import PageParams
from src.presentation.api.common.response_models import PaginatedResponse, paginate
from src.presentation.api.dependencies.auth import Principal, require_permission
from src.presentation.api.dependencies.services import (
    BatchServiceDep,
    CourseServiceDep,
    DepartmentServiceDep,
    SectionServiceDep,
    SemesterServiceDep,
    SessionServiceDep,
)
from src.presentation.api.v1.academic.schemas import (
    AddPrerequisiteRequest,
    BatchData,
    CourseData,
    CreateBatchRequest,
    CreateCourseRequest,
    CreateDepartmentRequest,
    CreateSectionRequest,
    CreateSemesterRequest,
    CreateSessionRequest,
    DepartmentData,
    SectionData,
    SemesterData,
    SessionData,
    UpdateBatchRequest,
    UpdateCourseRequest,
    UpdateDepartmentRequest,
    UpdateSectionRequest,
    UpdateSemesterRequest,
    UpdateSessionRequest,
)

router = APIRouter()

PageQ = Annotated[int, Query(ge=1)]
SizeQ = Annotated[int, Query(ge=1, le=100)]


# ============================================================ Departments
@router.get("/departments", response_model=PaginatedResponse[DepartmentData], tags=["Departments"])
async def list_departments(
    service: DepartmentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("department:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
) -> PaginatedResponse[DepartmentData]:
    r = await service.list_departments(PageParams(page, page_size))
    return paginate(
        [DepartmentData.from_dto(d) for d in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/departments", response_model=DepartmentData, status_code=201, tags=["Departments"])
async def create_department(
    body: CreateDepartmentRequest,
    service: DepartmentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("department:create:*"))],
) -> DepartmentData:
    return DepartmentData.from_dto(await service.create(name=body.name, code=body.code))


@router.get("/departments/{department_id}", response_model=DepartmentData, tags=["Departments"])
async def get_department(
    department_id: UUID,
    service: DepartmentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("department:read:*"))],
) -> DepartmentData:
    return DepartmentData.from_dto(await service.get(department_id))


@router.put("/departments/{department_id}", response_model=DepartmentData, tags=["Departments"])
async def update_department(
    department_id: UUID,
    body: UpdateDepartmentRequest,
    service: DepartmentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("department:update:*"))],
) -> DepartmentData:
    return DepartmentData.from_dto(
        await service.update(department_id, name=body.name, code=body.code)
    )


@router.delete("/departments/{department_id}", status_code=204, tags=["Departments"])
async def delete_department(
    department_id: UUID,
    service: DepartmentServiceDep,
    _p: Annotated[Principal, Depends(require_permission("department:delete:*"))],
) -> None:
    await service.delete(department_id)


# ============================================================ Sessions
@router.get("/sessions", response_model=PaginatedResponse[SessionData], tags=["Sessions"])
async def list_sessions(
    service: SessionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("session:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
    is_current: Annotated[bool | None, Query()] = None,
) -> PaginatedResponse[SessionData]:
    r = await service.list_sessions(PageParams(page, page_size), is_current=is_current)
    return paginate(
        [SessionData.from_dto(s) for s in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/sessions", response_model=SessionData, status_code=201, tags=["Sessions"])
async def create_session(
    body: CreateSessionRequest,
    service: SessionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("session:create:*"))],
) -> SessionData:
    dto = await service.create(
        name=body.name,
        start_date=body.start_date,
        end_date=body.end_date,
        is_current=body.is_current,
    )
    return SessionData.from_dto(dto)


@router.get("/sessions/{session_id}", response_model=SessionData, tags=["Sessions"])
async def get_session(
    session_id: UUID,
    service: SessionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("session:read:*"))],
) -> SessionData:
    return SessionData.from_dto(await service.get(session_id))


@router.put("/sessions/{session_id}", response_model=SessionData, tags=["Sessions"])
async def update_session(
    session_id: UUID,
    body: UpdateSessionRequest,
    service: SessionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("session:update:*"))],
) -> SessionData:
    dto = await service.update(
        session_id, name=body.name, start_date=body.start_date, end_date=body.end_date
    )
    return SessionData.from_dto(dto)


@router.patch("/sessions/{session_id}/activate", response_model=SessionData, tags=["Sessions"])
async def activate_session(
    session_id: UUID,
    service: SessionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("session:update:*"))],
) -> SessionData:
    return SessionData.from_dto(await service.activate(session_id))


@router.delete("/sessions/{session_id}", status_code=204, tags=["Sessions"])
async def delete_session(
    session_id: UUID,
    service: SessionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("session:delete:*"))],
) -> None:
    await service.delete(session_id)


# ============================================================ Semesters
@router.get("/semesters", response_model=PaginatedResponse[SemesterData], tags=["Semesters"])
async def list_semesters(
    service: SemesterServiceDep,
    _p: Annotated[Principal, Depends(require_permission("semester:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
    session_id: Annotated[UUID | None, Query()] = None,
) -> PaginatedResponse[SemesterData]:
    r = await service.list_semesters(PageParams(page, page_size), session_id=session_id)
    return paginate(
        [SemesterData.from_dto(s) for s in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/semesters", response_model=SemesterData, status_code=201, tags=["Semesters"])
async def create_semester(
    body: CreateSemesterRequest,
    service: SemesterServiceDep,
    _p: Annotated[Principal, Depends(require_permission("semester:create:*"))],
) -> SemesterData:
    dto = await service.create(
        session_id=body.session_id,
        name=body.name,
        number=body.number,
        start_date=body.start_date,
        end_date=body.end_date,
    )
    return SemesterData.from_dto(dto)


@router.get("/semesters/{semester_id}", response_model=SemesterData, tags=["Semesters"])
async def get_semester(
    semester_id: UUID,
    service: SemesterServiceDep,
    _p: Annotated[Principal, Depends(require_permission("semester:read:*"))],
) -> SemesterData:
    return SemesterData.from_dto(await service.get(semester_id))


@router.put("/semesters/{semester_id}", response_model=SemesterData, tags=["Semesters"])
async def update_semester(
    semester_id: UUID,
    body: UpdateSemesterRequest,
    service: SemesterServiceDep,
    _p: Annotated[Principal, Depends(require_permission("semester:update:*"))],
) -> SemesterData:
    dto = await service.update(
        semester_id,
        name=body.name,
        number=body.number,
        start_date=body.start_date,
        end_date=body.end_date,
    )
    return SemesterData.from_dto(dto)


@router.delete("/semesters/{semester_id}", status_code=204, tags=["Semesters"])
async def delete_semester(
    semester_id: UUID,
    service: SemesterServiceDep,
    _p: Annotated[Principal, Depends(require_permission("semester:delete:*"))],
) -> None:
    await service.delete(semester_id)


# ============================================================ Batches
@router.get("/batches", response_model=PaginatedResponse[BatchData], tags=["Batches"])
async def list_batches(
    service: BatchServiceDep,
    _p: Annotated[Principal, Depends(require_permission("batch:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
    session_id: Annotated[UUID | None, Query()] = None,
    department_id: Annotated[UUID | None, Query()] = None,
) -> PaginatedResponse[BatchData]:
    r = await service.list_batches(
        PageParams(page, page_size), session_id=session_id, department_id=department_id
    )
    return paginate(
        [BatchData.from_dto(b) for b in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/batches", response_model=BatchData, status_code=201, tags=["Batches"])
async def create_batch(
    body: CreateBatchRequest,
    service: BatchServiceDep,
    _p: Annotated[Principal, Depends(require_permission("batch:create:*"))],
) -> BatchData:
    dto = await service.create(
        session_id=body.session_id,
        department_id=body.department_id,
        name=body.name,
        code=body.code,
    )
    return BatchData.from_dto(dto)


@router.get("/batches/{batch_id}", response_model=BatchData, tags=["Batches"])
async def get_batch(
    batch_id: UUID,
    service: BatchServiceDep,
    _p: Annotated[Principal, Depends(require_permission("batch:read:*"))],
) -> BatchData:
    return BatchData.from_dto(await service.get(batch_id))


@router.put("/batches/{batch_id}", response_model=BatchData, tags=["Batches"])
async def update_batch(
    batch_id: UUID,
    body: UpdateBatchRequest,
    service: BatchServiceDep,
    _p: Annotated[Principal, Depends(require_permission("batch:update:*"))],
) -> BatchData:
    return BatchData.from_dto(await service.update(batch_id, name=body.name, code=body.code))


@router.delete("/batches/{batch_id}", status_code=204, tags=["Batches"])
async def delete_batch(
    batch_id: UUID,
    service: BatchServiceDep,
    _p: Annotated[Principal, Depends(require_permission("batch:delete:*"))],
) -> None:
    await service.delete(batch_id)


@router.get("/batches/{batch_id}/sections", response_model=list[SectionData], tags=["Batches"])
async def list_batch_sections(
    batch_id: UUID,
    service: BatchServiceDep,
    _p: Annotated[Principal, Depends(require_permission("section:read:*"))],
) -> list[SectionData]:
    return [SectionData.from_dto(s) for s in await service.list_sections(batch_id)]


# ============================================================ Sections
@router.get("/sections", response_model=PaginatedResponse[SectionData], tags=["Sections"])
async def list_sections(
    service: SectionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("section:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
    batch_id: Annotated[UUID | None, Query()] = None,
) -> PaginatedResponse[SectionData]:
    r = await service.list_sections(PageParams(page, page_size), batch_id=batch_id)
    return paginate(
        [SectionData.from_dto(s) for s in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/sections", response_model=SectionData, status_code=201, tags=["Sections"])
async def create_section(
    body: CreateSectionRequest,
    service: SectionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("section:create:*"))],
) -> SectionData:
    dto = await service.create(
        batch_id=body.batch_id, name=body.name, max_capacity=body.max_capacity
    )
    return SectionData.from_dto(dto)


@router.get("/sections/{section_id}", response_model=SectionData, tags=["Sections"])
async def get_section(
    section_id: UUID,
    service: SectionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("section:read:*"))],
) -> SectionData:
    return SectionData.from_dto(await service.get(section_id))


@router.put("/sections/{section_id}", response_model=SectionData, tags=["Sections"])
async def update_section(
    section_id: UUID,
    body: UpdateSectionRequest,
    service: SectionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("section:update:*"))],
) -> SectionData:
    dto = await service.update(section_id, name=body.name, max_capacity=body.max_capacity)
    return SectionData.from_dto(dto)


@router.delete("/sections/{section_id}", status_code=204, tags=["Sections"])
async def delete_section(
    section_id: UUID,
    service: SectionServiceDep,
    _p: Annotated[Principal, Depends(require_permission("section:delete:*"))],
) -> None:
    await service.delete(section_id)


# ============================================================ Courses
@router.get("/courses", response_model=PaginatedResponse[CourseData], tags=["Courses"])
async def list_courses(
    service: CourseServiceDep,
    _p: Annotated[Principal, Depends(require_permission("course:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
    department_id: Annotated[UUID | None, Query()] = None,
    is_active: Annotated[bool | None, Query()] = None,
) -> PaginatedResponse[CourseData]:
    r = await service.list_courses(
        PageParams(page, page_size), department_id=department_id, is_active=is_active
    )
    return paginate(
        [CourseData.from_dto(c) for c in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/courses", response_model=CourseData, status_code=201, tags=["Courses"])
async def create_course(
    body: CreateCourseRequest,
    service: CourseServiceDep,
    _p: Annotated[Principal, Depends(require_permission("course:create:*"))],
) -> CourseData:
    dto = await service.create(
        department_id=body.department_id,
        code=body.code,
        title=body.title,
        credits=Decimal(body.credits),
        lecture_hours=body.lecture_hours,
        lab_hours=body.lab_hours,
        prerequisite_ids=tuple(body.prerequisite_ids),
    )
    return CourseData.from_dto(dto)


@router.get("/courses/{course_id}", response_model=CourseData, tags=["Courses"])
async def get_course(
    course_id: UUID,
    service: CourseServiceDep,
    _p: Annotated[Principal, Depends(require_permission("course:read:*"))],
) -> CourseData:
    return CourseData.from_dto(await service.get(course_id))


@router.put("/courses/{course_id}", response_model=CourseData, tags=["Courses"])
async def update_course(
    course_id: UUID,
    body: UpdateCourseRequest,
    service: CourseServiceDep,
    _p: Annotated[Principal, Depends(require_permission("course:update:*"))],
) -> CourseData:
    dto = await service.update(
        course_id,
        title=body.title,
        credits=Decimal(body.credits),
        lecture_hours=body.lecture_hours,
        lab_hours=body.lab_hours,
        is_active=body.is_active,
    )
    return CourseData.from_dto(dto)


@router.delete("/courses/{course_id}", status_code=204, tags=["Courses"])
async def deactivate_course(
    course_id: UUID,
    service: CourseServiceDep,
    _p: Annotated[Principal, Depends(require_permission("course:delete:*"))],
) -> None:
    await service.deactivate(course_id)


@router.get("/courses/{course_id}/prerequisites", response_model=list[CourseData], tags=["Courses"])
async def list_course_prerequisites(
    course_id: UUID,
    service: CourseServiceDep,
    _p: Annotated[Principal, Depends(require_permission("course:read:*"))],
) -> list[CourseData]:
    return [CourseData.from_dto(c) for c in await service.list_prerequisites(course_id)]


@router.post("/courses/{course_id}/prerequisites", status_code=201, tags=["Courses"])
async def add_course_prerequisite(
    course_id: UUID,
    body: AddPrerequisiteRequest,
    service: CourseServiceDep,
    _p: Annotated[Principal, Depends(require_permission("course:update:*"))],
) -> dict[str, str]:
    await service.add_prerequisite(course_id, body.prerequisite_id)
    return {"status": "added"}


@router.delete(
    "/courses/{course_id}/prerequisites/{prerequisite_id}", status_code=204, tags=["Courses"]
)
async def remove_course_prerequisite(
    course_id: UUID,
    prerequisite_id: UUID,
    service: CourseServiceDep,
    _p: Annotated[Principal, Depends(require_permission("course:update:*"))],
) -> None:
    await service.remove_prerequisite(course_id, prerequisite_id)
