"""Period request/response schemas (bare)."""

from __future__ import annotations

from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.timetable.dto import PeriodDTO


class PeriodData(BaseModel):
    id: UUID
    name: str
    period_number: int
    start_time: time
    end_time: time
    duration_minutes: int
    is_break: bool
    created_at: datetime

    @classmethod
    def from_dto(cls, p: PeriodDTO) -> PeriodData:
        return cls(
            id=p.id,
            name=p.name,
            period_number=p.period_number,
            start_time=p.start_time,
            end_time=p.end_time,
            duration_minutes=p.duration_minutes,
            is_break=p.is_break,
            created_at=p.created_at,
        )


class CreatePeriodRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    period_number: int = Field(ge=1, le=30)
    start_time: time
    end_time: time
    duration_minutes: int = Field(ge=1, le=480)
    is_break: bool = False


class UpdatePeriodRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    period_number: int = Field(ge=1, le=30)
    start_time: time
    end_time: time
    duration_minutes: int = Field(ge=1, le=480)
    is_break: bool = False
