"""resources schema — rooms (module #2)

Revision ID: 0004_resources_rooms
Revises: 0003_timetable_periods
Create Date: 2026-06-19

Standalone room records matching the frontend contract (``type`` field with five values,
equipment flags). Deviates from the DB design's room_type set to match the built frontend.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0004_resources_rooms"
down_revision: str | None = "0003_timetable_periods"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "resources"
_UUID = postgresql.UUID(as_uuid=True)
_PK = sa.text("gen_random_uuid()")
_NOW = sa.text("now()")

ROOM_TYPES = ("classroom", "lab", "lecture_hall", "seminar_room", "conference_room")


def upgrade() -> None:
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
    op.create_table(
        "rooms",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("type", sa.String(30), nullable=False),
        sa.Column("capacity", sa.SmallInteger(), nullable=False),
        sa.Column("building", sa.String(100), nullable=False),
        sa.Column("floor", sa.SmallInteger(), nullable=False),
        sa.Column("has_projector", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_computers", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_ac", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.UniqueConstraint("code", name="uq_rooms_code"),
        sa.CheckConstraint(
            "type IN ('classroom','lab','lecture_hall','seminar_room','conference_room')",
            name="ck_rooms_type",
        ),
        sa.CheckConstraint("capacity > 0", name="ck_rooms_capacity"),
        schema=SCHEMA,
    )
    op.create_index("idx_rooms_type", "rooms", ["type"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_table("rooms", schema=SCHEMA)
    op.execute(f"DROP SCHEMA IF EXISTS {SCHEMA}")
