"""Periods API router (bare responses)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.common.dto.pagination import PageParams
from src.presentation.api.common.response_models import PaginatedResponse, paginate
from src.presentation.api.dependencies.auth import Principal, require_permission
from src.presentation.api.dependencies.services import PeriodServiceDep
from src.presentation.api.v1.periods.schemas import (
    CreatePeriodRequest,
    PeriodData,
    UpdatePeriodRequest,
)

router = APIRouter(tags=["Periods"])

PageQ = Annotated[int, Query(ge=1)]
SizeQ = Annotated[int, Query(ge=1, le=100)]


@router.get("/periods", response_model=PaginatedResponse[PeriodData], operation_id="listPeriods")
async def list_periods(
    service: PeriodServiceDep,
    _p: Annotated[Principal, Depends(require_permission("period:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
) -> PaginatedResponse[PeriodData]:
    r = await service.list_periods(PageParams(page, page_size))
    return paginate(
        [PeriodData.from_dto(p) for p in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/periods", response_model=PeriodData, status_code=201, operation_id="createPeriod")
async def create_period(
    body: CreatePeriodRequest,
    service: PeriodServiceDep,
    _p: Annotated[Principal, Depends(require_permission("period:create:*"))],
) -> PeriodData:
    dto = await service.create(
        name=body.name,
        period_number=body.period_number,
        start_time=body.start_time,
        end_time=body.end_time,
        duration_minutes=body.duration_minutes,
        is_break=body.is_break,
    )
    return PeriodData.from_dto(dto)


@router.get("/periods/{period_id}", response_model=PeriodData, operation_id="getPeriod")
async def get_period(
    period_id: UUID,
    service: PeriodServiceDep,
    _p: Annotated[Principal, Depends(require_permission("period:read:*"))],
) -> PeriodData:
    return PeriodData.from_dto(await service.get(period_id))


@router.put("/periods/{period_id}", response_model=PeriodData, operation_id="updatePeriod")
async def update_period(
    period_id: UUID,
    body: UpdatePeriodRequest,
    service: PeriodServiceDep,
    _p: Annotated[Principal, Depends(require_permission("period:update:*"))],
) -> PeriodData:
    dto = await service.update(
        period_id,
        name=body.name,
        period_number=body.period_number,
        start_time=body.start_time,
        end_time=body.end_time,
        duration_minutes=body.duration_minutes,
        is_break=body.is_break,
    )
    return PeriodData.from_dto(dto)


@router.delete("/periods/{period_id}", status_code=204, operation_id="deletePeriod")
async def delete_period(
    period_id: UUID,
    service: PeriodServiceDep,
    _p: Annotated[Principal, Depends(require_permission("period:delete:*"))],
) -> None:
    await service.delete(period_id)
