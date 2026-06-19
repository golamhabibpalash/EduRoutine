"""Timetable application services."""

from __future__ import annotations

from datetime import time
from uuid import UUID, uuid4

from src.application.common.dto.pagination import Page, PageParams
from src.application.common.exceptions import ConflictError, ValidationError
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.timetable.dto import PeriodDTO
from src.domain.timetable.entities.period import Period
from src.domain.timetable.exceptions import PeriodNotFoundError
from src.shared.utils.clock import utcnow


class PeriodService:
    """Use cases for the Periods module."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @staticmethod
    def _dto(p: Period) -> PeriodDTO:
        return PeriodDTO(
            id=p.id,
            name=p.name,
            period_number=p.period_number,
            start_time=p.start_time,
            end_time=p.end_time,
            duration_minutes=p.duration_minutes,
            is_break=p.is_break,
            created_at=p.created_at or utcnow(),
        )

    async def get(self, period_id: UUID) -> PeriodDTO:
        return self._dto(await self._require(period_id))

    async def list_periods(self, page: PageParams) -> Page[PeriodDTO]:
        items = await self._uow.periods.list_page(limit=page.limit, offset=page.offset)
        total = await self._uow.periods.count()
        return Page([self._dto(p) for p in items], page.page, page.page_size, total)

    async def create(
        self,
        *,
        name: str,
        period_number: int,
        start_time: time,
        end_time: time,
        duration_minutes: int,
        is_break: bool = False,
    ) -> PeriodDTO:
        _validate_times(start_time, end_time)
        if await self._uow.periods.get_by_number(period_number) is not None:
            raise ConflictError(f"Period number {period_number} already exists.")
        period = Period(
            id=uuid4(),
            name=name,
            period_number=period_number,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration_minutes,
            is_break=is_break,
        )
        await self._uow.periods.add(period)
        await self._uow.commit()
        return self._dto(period)

    async def update(
        self,
        period_id: UUID,
        *,
        name: str,
        period_number: int,
        start_time: time,
        end_time: time,
        duration_minutes: int,
        is_break: bool,
    ) -> PeriodDTO:
        period = await self._require(period_id)
        _validate_times(start_time, end_time)
        other = await self._uow.periods.get_by_number(period_number)
        if other is not None and other.id != period_id:
            raise ConflictError(f"Period number {period_number} already exists.")
        period.name = name
        period.period_number = period_number
        period.start_time = start_time
        period.end_time = end_time
        period.duration_minutes = duration_minutes
        period.is_break = is_break
        await self._uow.periods.update(period)
        await self._uow.commit()
        return self._dto(period)

    async def delete(self, period_id: UUID) -> None:
        period = await self._require(period_id)
        await self._uow.periods.delete(period)
        await self._uow.commit()

    async def _require(self, period_id: UUID) -> Period:
        period = await self._uow.periods.get(period_id)
        if period is None:
            raise PeriodNotFoundError(f"Period '{period_id}' not found.")
        return period


def _validate_times(start_time: time, end_time: time) -> None:
    if end_time <= start_time:
        raise ValidationError("end_time must be after start_time.")
