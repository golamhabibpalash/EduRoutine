"""timetable schema — periods (Phase 4 / module #1)

Revision ID: 0003_timetable_periods
Revises: 0002_academic_schema
Create Date: 2026-06-19

Creates the ``timetable`` schema and the ``periods`` table (the daily-grid period definition;
fulfils the DB design's time-slot role under the project's "periods" naming).
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003_timetable_periods"
down_revision: str | None = "0002_academic_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "timetable"
_UUID = postgresql.UUID(as_uuid=True)
_PK = sa.text("gen_random_uuid()")
_NOW = sa.text("now()")


def upgrade() -> None:
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

    op.create_table(
        "periods",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("period_number", sa.SmallInteger(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("duration_minutes", sa.SmallInteger(), nullable=False),
        sa.Column("is_break", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.UniqueConstraint("period_number", name="uq_periods_period_number"),
        sa.CheckConstraint("end_time > start_time", name="ck_periods_time_order"),
        sa.CheckConstraint("duration_minutes > 0", name="ck_periods_duration"),
        schema=SCHEMA,
    )


def downgrade() -> None:
    op.drop_table("periods", schema=SCHEMA)
    op.execute(f"DROP SCHEMA IF EXISTS {SCHEMA}")
