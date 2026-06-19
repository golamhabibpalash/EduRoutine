"""SQLAlchemy adapters for the timetable repository ports."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.timetable.entities.period import Period
from src.infrastructure.persistence.models.timetable import PeriodModel


class SqlAlchemyPeriodRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: PeriodModel) -> Period:
        return Period(
            id=m.id,
            name=m.name,
            period_number=m.period_number,
            start_time=m.start_time,
            end_time=m.end_time,
            duration_minutes=m.duration_minutes,
            is_break=m.is_break,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, period_id: UUID) -> Period | None:
        m = await self._session.get(PeriodModel, period_id)
        return self._to_domain(m) if m else None

    async def get_by_number(self, period_number: int) -> Period | None:
        r = await self._session.execute(
            select(PeriodModel).where(PeriodModel.period_number == period_number)
        )
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(self, *, limit: int, offset: int) -> list[Period]:
        r = await self._session.execute(
            select(PeriodModel).order_by(PeriodModel.period_number).limit(limit).offset(offset)
        )
        return [self._to_domain(m) for m in r.scalars()]

    async def count(self) -> int:
        r = await self._session.execute(select(func.count()).select_from(PeriodModel))
        return int(r.scalar_one())

    async def add(self, period: Period) -> None:
        self._session.add(
            PeriodModel(
                id=period.id,
                name=period.name,
                period_number=period.period_number,
                start_time=period.start_time,
                end_time=period.end_time,
                duration_minutes=period.duration_minutes,
                is_break=period.is_break,
            )
        )

    async def update(self, period: Period) -> None:
        m = await self._session.get(PeriodModel, period.id)
        if m is None:
            return
        m.name = period.name
        m.period_number = period.period_number
        m.start_time = period.start_time
        m.end_time = period.end_time
        m.duration_minutes = period.duration_minutes
        m.is_break = period.is_break

    async def delete(self, period: Period) -> None:
        m = await self._session.get(PeriodModel, period.id)
        if m:
            await self._session.delete(m)
