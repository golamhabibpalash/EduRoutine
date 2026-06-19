"""SQLAlchemy adapters for the timetable repository ports."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.timetable.entities.period import Period
from src.domain.timetable.entities.routine import Routine, RoutineDetail
from src.infrastructure.persistence.models.timetable import (
    PeriodModel,
    RoutineDetailModel,
    RoutineModel,
)


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


class SqlAlchemyRoutineRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: RoutineModel) -> Routine:
        return Routine(
            id=m.id,
            name=m.name,
            session_id=m.session_id,
            batch_id=m.batch_id,
            semester_id=m.semester_id,
            department_id=m.department_id,
            status=m.status,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, routine_id: UUID) -> Routine | None:
        m = await self._session.get(RoutineModel, routine_id)
        return self._to_domain(m) if m else None

    async def list_page(self, *, limit: int, offset: int) -> list[Routine]:
        r = await self._session.execute(
            select(RoutineModel).order_by(RoutineModel.created_at.desc()).limit(limit).offset(offset)
        )
        return [self._to_domain(m) for m in r.scalars()]

    async def count(self) -> int:
        r = await self._session.execute(select(func.count()).select_from(RoutineModel))
        return int(r.scalar_one())

    async def add(self, routine: Routine) -> None:
        self._session.add(
            RoutineModel(
                id=routine.id,
                name=routine.name,
                session_id=routine.session_id,
                batch_id=routine.batch_id,
                semester_id=routine.semester_id,
                department_id=routine.department_id,
                status=routine.status,
            )
        )

    async def update(self, routine: Routine) -> None:
        m = await self._session.get(RoutineModel, routine.id)
        if m is None:
            return
        m.name = routine.name
        m.session_id = routine.session_id
        m.batch_id = routine.batch_id
        m.semester_id = routine.semester_id
        m.department_id = routine.department_id
        m.status = routine.status

    async def delete(self, routine: Routine) -> None:
        m = await self._session.get(RoutineModel, routine.id)
        if m:
            await self._session.delete(m)


class SqlAlchemyRoutineDetailRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: RoutineDetailModel) -> RoutineDetail:
        return RoutineDetail(
            id=m.id,
            routine_id=m.routine_id,
            course_id=m.course_id,
            teacher_id=m.teacher_id,
            room_id=m.room_id,
            section_id=m.section_id,
            day_of_week=m.day_of_week,
            start_time=m.start_time,
            end_time=m.end_time,
            is_lab=m.is_lab,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, detail_id: UUID) -> RoutineDetail | None:
        m = await self._session.get(RoutineDetailModel, detail_id)
        return self._to_domain(m) if m else None

    async def list_by_routine(self, routine_id: UUID) -> list[RoutineDetail]:
        r = await self._session.execute(
            select(RoutineDetailModel)
            .where(RoutineDetailModel.routine_id == routine_id)
            .order_by(RoutineDetailModel.start_time, RoutineDetailModel.day_of_week)
        )
        return [self._to_domain(m) for m in r.scalars()]

    async def add(self, detail: RoutineDetail) -> None:
        self._session.add(
            RoutineDetailModel(
                id=detail.id,
                routine_id=detail.routine_id,
                course_id=detail.course_id,
                teacher_id=detail.teacher_id,
                room_id=detail.room_id,
                section_id=detail.section_id,
                day_of_week=detail.day_of_week,
                start_time=detail.start_time,
                end_time=detail.end_time,
                is_lab=detail.is_lab,
            )
        )

    async def update(self, detail: RoutineDetail) -> None:
        m = await self._session.get(RoutineDetailModel, detail.id)
        if m is None:
            return
        m.course_id = detail.course_id
        m.teacher_id = detail.teacher_id
        m.room_id = detail.room_id
        m.section_id = detail.section_id
        m.day_of_week = detail.day_of_week
        m.start_time = detail.start_time
        m.end_time = detail.end_time
        m.is_lab = detail.is_lab

    async def delete(self, detail: RoutineDetail) -> None:
        m = await self._session.get(RoutineDetailModel, detail.id)
        if m:
            await self._session.delete(m)

    async def delete_by_routine(self, routine_id: UUID) -> None:
        await self._session.execute(
            select(RoutineDetailModel).where(RoutineDetailModel.routine_id == routine_id)
        )
        await self._session.execute(
            RoutineDetailModel.__table__.delete().where(
                RoutineDetailModel.routine_id == routine_id
            )
        )
