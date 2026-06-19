"""Timetable application services."""

from __future__ import annotations

from datetime import time
from uuid import UUID, uuid4

from src.application.common.dto.pagination import Page, PageParams
from src.application.common.exceptions import ConflictError, ValidationError
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.timetable.dto import PeriodDTO, RoutineDTO, RoutineDetailDTO
from src.domain.timetable.entities.period import Period
from src.domain.timetable.entities.routine import Routine, RoutineDetail
from src.domain.timetable.exceptions import PeriodNotFoundError, RoutineNotFoundError
from src.shared.utils.clock import utcnow

# ---------------------------------------------------------------------------
# Period service
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Routine service
# ---------------------------------------------------------------------------


class RoutineService:
    """Use cases for routines and their details."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    # ---- helpers ----

    @staticmethod
    def _dto(r: Routine) -> RoutineDTO:
        return RoutineDTO(
            id=r.id,
            name=r.name,
            session_id=r.session_id,
            batch_id=r.batch_id,
            semester_id=r.semester_id,
            department_id=r.department_id,
            status=r.status,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )

    @staticmethod
    def _detail_dto(d: RoutineDetail) -> RoutineDetailDTO:
        return RoutineDetailDTO(
            id=d.id,
            routine_id=d.routine_id,
            course_id=d.course_id,
            teacher_id=d.teacher_id,
            room_id=d.room_id,
            section_id=d.section_id,
            day_of_week=d.day_of_week,
            start_time=d.start_time,
            end_time=d.end_time,
            is_lab=d.is_lab,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )

    async def _require(self, routine_id: UUID) -> Routine:
        r = await self._uow.routines.get(routine_id)
        if r is None:
            raise RoutineNotFoundError(f"Routine '{routine_id}' not found.")
        return r

    # ---- routine CRUD ----

    async def get(self, routine_id: UUID) -> RoutineDTO:
        return self._dto(await self._require(routine_id))

    async def list_routines(self, page: PageParams) -> Page[RoutineDTO]:
        items = await self._uow.routines.list_page(limit=page.limit, offset=page.offset)
        total = await self._uow.routines.count()
        return Page([self._dto(r) for r in items], page.page, page.page_size, total)

    async def create(
        self,
        *,
        name: str,
        session_id: UUID,
        batch_id: UUID,
        semester_id: UUID,
        department_id: UUID,
    ) -> RoutineDTO:
        routine = Routine(
            id=uuid4(),
            name=name,
            session_id=session_id,
            batch_id=batch_id,
            semester_id=semester_id,
            department_id=department_id,
            status="draft",
        )
        await self._uow.routines.add(routine)
        await self._uow.commit()
        return self._dto(routine)

    async def update(
        self,
        routine_id: UUID,
        *,
        name: str,
        session_id: UUID,
        batch_id: UUID,
        semester_id: UUID,
        department_id: UUID,
    ) -> RoutineDTO:
        routine = await self._require(routine_id)
        routine.name = name
        routine.session_id = session_id
        routine.batch_id = batch_id
        routine.semester_id = semester_id
        routine.department_id = department_id
        await self._uow.routines.update(routine)
        await self._uow.commit()
        return self._dto(routine)

    async def delete(self, routine_id: UUID) -> None:
        routine = await self._require(routine_id)
        await self._uow.details.delete_by_routine(routine_id)
        await self._uow.routines.delete(routine)
        await self._uow.commit()

    async def publish(self, routine_id: UUID) -> RoutineDTO:
        routine = await self._require(routine_id)
        routine.status = "published"
        await self._uow.routines.update(routine)
        await self._uow.commit()
        return self._dto(routine)

    async def archive(self, routine_id: UUID) -> RoutineDTO:
        routine = await self._require(routine_id)
        routine.status = "archived"
        await self._uow.routines.update(routine)
        await self._uow.commit()
        return self._dto(routine)

    async def clone(self, routine_id: UUID) -> RoutineDTO:
        original = await self._require(routine_id)
        clone = Routine(
            id=uuid4(),
            name=f"{original.name} (Copy)",
            session_id=original.session_id,
            batch_id=original.batch_id,
            semester_id=original.semester_id,
            department_id=original.department_id,
            status="draft",
        )
        await self._uow.routines.add(clone)
        details = await self._uow.details.list_by_routine(routine_id)
        for d in details:
            cloned_detail = RoutineDetail(
                id=uuid4(),
                routine_id=clone.id,
                course_id=d.course_id,
                teacher_id=d.teacher_id,
                room_id=d.room_id,
                section_id=d.section_id,
                day_of_week=d.day_of_week,
                start_time=d.start_time,
                end_time=d.end_time,
                is_lab=d.is_lab,
            )
            await self._uow.details.add(cloned_detail)
        await self._uow.commit()
        return self._dto(clone)

    # ---- detail CRUD ----

    async def get_details(self, routine_id: UUID) -> list[RoutineDetailDTO]:
        details = await self._uow.details.list_by_routine(routine_id)
        return [self._detail_dto(d) for d in details]

    async def create_detail(
        self,
        *,
        routine_id: UUID,
        course_id: UUID,
        teacher_id: UUID,
        room_id: UUID,
        section_id: UUID,
        day_of_week: str,
        start_time: str,
        end_time: str,
        is_lab: bool = False,
    ) -> RoutineDetailDTO:
        detail = RoutineDetail(
            id=uuid4(),
            routine_id=routine_id,
            course_id=course_id,
            teacher_id=teacher_id,
            room_id=room_id,
            section_id=section_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            is_lab=is_lab,
        )
        await self._uow.details.add(detail)
        await self._uow.commit()
        return self._detail_dto(detail)

    async def update_detail(
        self,
        detail_id: UUID,
        *,
        course_id: UUID,
        teacher_id: UUID,
        room_id: UUID,
        section_id: UUID,
        day_of_week: str,
        start_time: str,
        end_time: str,
        is_lab: bool,
    ) -> RoutineDetailDTO:
        detail = await self._uow.details.get(detail_id)
        if detail is None:
            raise RoutineNotFoundError(f"Routine detail '{detail_id}' not found.")
        detail.course_id = course_id
        detail.teacher_id = teacher_id
        detail.room_id = room_id
        detail.section_id = section_id
        detail.day_of_week = day_of_week
        detail.start_time = start_time
        detail.end_time = end_time
        detail.is_lab = is_lab
        await self._uow.details.update(detail)
        await self._uow.commit()
        return self._detail_dto(detail)

    async def delete_detail(self, detail_id: UUID) -> None:
        detail = await self._uow.details.get(detail_id)
        if detail is None:
            raise RoutineNotFoundError(f"Routine detail '{detail_id}' not found.")
        await self._uow.details.delete(detail)
        await self._uow.commit()
