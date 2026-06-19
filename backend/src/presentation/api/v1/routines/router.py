"""Routines API router."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.common.dto.pagination import PageParams
from src.presentation.api.common.response_models import PaginatedResponse, paginate
from src.presentation.api.dependencies.auth import Principal, require_permission
from src.presentation.api.dependencies.services import RoutineServiceDep
from src.presentation.api.v1.routines.schemas import (
    CreateRoutineDetailRequest,
    CreateRoutineRequest,
    RoutineData,
    RoutineDetailData,
    UpdateRoutineDetailRequest,
    UpdateRoutineRequest,
)

router = APIRouter(tags=["Routines"])

PageQ = Annotated[int, Query(ge=1)]
SizeQ = Annotated[int, Query(ge=1, le=100)]


# ---- Routine CRUD ----

@router.get("/routines", response_model=PaginatedResponse[RoutineData], operation_id="listRoutines")
async def list_routines(
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
) -> PaginatedResponse[RoutineData]:
    r = await service.list_routines(PageParams(page, page_size))
    return paginate(
        [RoutineData.from_dto(p) for p in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/routines", response_model=RoutineData, status_code=201, operation_id="createRoutine")
async def create_routine(
    body: CreateRoutineRequest,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:create:*"))],
) -> RoutineData:
    dto = await service.create(
        name=body.name,
        session_id=body.session_id,
        batch_id=body.batch_id,
        semester_id=body.semester_id,
        department_id=body.department_id,
    )
    return RoutineData.from_dto(dto)


@router.get("/routines/{routine_id}", response_model=RoutineData, operation_id="getRoutine")
async def get_routine(
    routine_id: UUID,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:read:*"))],
) -> RoutineData:
    return RoutineData.from_dto(await service.get(routine_id))


@router.put("/routines/{routine_id}", response_model=RoutineData, operation_id="updateRoutine")
async def update_routine(
    routine_id: UUID,
    body: UpdateRoutineRequest,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:update:*"))],
) -> RoutineData:
    dto = await service.update(
        routine_id,
        name=body.name,
        session_id=body.session_id,
        batch_id=body.batch_id,
        semester_id=body.semester_id,
        department_id=body.department_id,
    )
    return RoutineData.from_dto(dto)


@router.delete("/routines/{routine_id}", status_code=204, operation_id="deleteRoutine")
async def delete_routine(
    routine_id: UUID,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:delete:*"))],
) -> None:
    await service.delete(routine_id)


# ---- Routine actions ----

@router.post("/routines/{routine_id}/publish", response_model=RoutineData, operation_id="publishRoutine")
async def publish_routine(
    routine_id: UUID,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:update:*"))],
) -> RoutineData:
    return RoutineData.from_dto(await service.publish(routine_id))


@router.post("/routines/{routine_id}/archive", response_model=RoutineData, operation_id="archiveRoutine")
async def archive_routine(
    routine_id: UUID,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:update:*"))],
) -> RoutineData:
    return RoutineData.from_dto(await service.archive(routine_id))


@router.post("/routines/{routine_id}/clone", response_model=RoutineData, operation_id="cloneRoutine")
async def clone_routine(
    routine_id: UUID,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:create:*"))],
) -> RoutineData:
    return RoutineData.from_dto(await service.clone(routine_id))


# ---- Routine Details ----

@router.get(
    "/routines/{routine_id}/details",
    response_model=list[RoutineDetailData],
    operation_id="listRoutineDetails",
)
async def list_routine_details(
    routine_id: UUID,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:read:*"))],
) -> list[RoutineDetailData]:
    details = await service.get_details(routine_id)
    return [RoutineDetailData.from_dto(d) for d in details]


@router.post(
    "/routine-details",
    response_model=RoutineDetailData,
    status_code=201,
    operation_id="createRoutineDetail",
)
async def create_routine_detail(
    body: CreateRoutineDetailRequest,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:create:*"))],
) -> RoutineDetailData:
    dto = await service.create_detail(
        routine_id=body.routine_id,
        course_id=body.course_id,
        teacher_id=body.teacher_id,
        room_id=body.room_id,
        section_id=body.section_id,
        day_of_week=body.day_of_week,
        start_time=body.start_time,
        end_time=body.end_time,
        is_lab=body.is_lab,
    )
    return RoutineDetailData.from_dto(dto)


@router.put(
    "/routine-details/{detail_id}",
    response_model=RoutineDetailData,
    operation_id="updateRoutineDetail",
)
async def update_routine_detail(
    detail_id: UUID,
    body: UpdateRoutineDetailRequest,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:update:*"))],
) -> RoutineDetailData:
    dto = await service.update_detail(
        detail_id,
        course_id=body.course_id,
        teacher_id=body.teacher_id,
        room_id=body.room_id,
        section_id=body.section_id,
        day_of_week=body.day_of_week,
        start_time=body.start_time,
        end_time=body.end_time,
        is_lab=body.is_lab,
    )
    return RoutineDetailData.from_dto(dto)


@router.delete("/routine-details/{detail_id}", status_code=204, operation_id="deleteRoutineDetail")
async def delete_routine_detail(
    detail_id: UUID,
    service: RoutineServiceDep,
    _p: Annotated[Principal, Depends(require_permission("routine:delete:*"))],
) -> None:
    await service.delete_detail(detail_id)
