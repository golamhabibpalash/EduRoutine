"""people schema — teachers, students (modules #3, #4)

Revision ID: 0005_people
Revises: 0004_resources_rooms
Create Date: 2026-06-19

Standalone teacher/student records matching the frontend contract (name/email/phone carried
directly; department as a string; enrollment_year). Deviates from the DB design's user-linked
people model to match the built frontend.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0005_people"
down_revision: str | None = "0004_resources_rooms"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "people"
_UUID = postgresql.UUID(as_uuid=True)
_PK = sa.text("gen_random_uuid()")
_NOW = sa.text("now()")


def upgrade() -> None:
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

    op.create_table(
        "teachers",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("employee_id", sa.String(50), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("department", sa.String(200), nullable=False),
        sa.Column(
            "specialization",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::text[]"),
        ),
        sa.Column("max_hours_per_week", sa.SmallInteger(), nullable=False, server_default=sa.text("30")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.UniqueConstraint("employee_id", name="uq_teachers_employee_id"),
        schema=SCHEMA,
    )

    op.create_table(
        "students",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("student_id", sa.String(50), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("batch_id", _UUID, nullable=False),
        sa.Column("section_id", _UUID, nullable=False),
        sa.Column("enrollment_year", sa.SmallInteger(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.UniqueConstraint("student_id", name="uq_students_student_id"),
        sa.ForeignKeyConstraint(
            ["batch_id"], ["academic.batches.id"], name="fk_students_batch_id", ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["section_id"], ["academic.sections.id"], name="fk_students_section_id",
            ondelete="RESTRICT",
        ),
        schema=SCHEMA,
    )
    op.create_index("idx_students_batch_id", "students", ["batch_id"], schema=SCHEMA)
    op.create_index("idx_students_section_id", "students", ["section_id"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_table("students", schema=SCHEMA)
    op.drop_table("teachers", schema=SCHEMA)
    op.execute(f"DROP SCHEMA IF EXISTS {SCHEMA}")
