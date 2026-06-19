"""academic schema — departments, sessions, semesters, batches, sections, courses (Phase 3)

Revision ID: 0002_academic_schema
Revises: 0001_identity_schema
Create Date: 2026-06-18

Faithful to docs/03-database-design.md and docs/12 (academic.*), minus multi-tenancy
(``tenant_id`` deferred, consistent with the identity schema and the OpenAPI contract).
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_academic_schema"
down_revision: str | None = "0001_identity_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "academic"
_UUID = postgresql.UUID(as_uuid=True)
_PK = sa.text("gen_random_uuid()")
_NOW = sa.text("now()")


def _ts() -> tuple[sa.Column, sa.Column]:
    return (
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
    )


def upgrade() -> None:
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

    op.create_table(
        "departments",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("code", sa.String(20), nullable=False),
        *_ts(),
        sa.UniqueConstraint("code", name="uq_departments_code"),
        schema=SCHEMA,
    )

    op.create_table(
        "sessions",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_ts(),
        sa.CheckConstraint("end_date > start_date", name="ck_sessions_date_order"),
        schema=SCHEMA,
    )

    op.create_table(
        "semesters",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("session_id", _UUID, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("number", sa.SmallInteger(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        *_ts(),
        sa.ForeignKeyConstraint(
            ["session_id"], [f"{SCHEMA}.sessions.id"], name="fk_semesters_session_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("session_id", "number", name="uq_semesters_session_id_number"),
        sa.CheckConstraint("number BETWEEN 1 AND 12", name="ck_semesters_number"),
        sa.CheckConstraint("end_date > start_date", name="ck_semesters_date_order"),
        schema=SCHEMA,
    )

    op.create_table(
        "batches",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("session_id", _UUID, nullable=False),
        sa.Column("department_id", _UUID, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        *_ts(),
        sa.ForeignKeyConstraint(
            ["session_id"], [f"{SCHEMA}.sessions.id"], name="fk_batches_session_id",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["department_id"], [f"{SCHEMA}.departments.id"], name="fk_batches_department_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("code", name="uq_batches_code"),
        schema=SCHEMA,
    )

    op.create_table(
        "sections",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("batch_id", _UUID, nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("max_capacity", sa.SmallInteger(), nullable=False),
        *_ts(),
        sa.ForeignKeyConstraint(
            ["batch_id"], [f"{SCHEMA}.batches.id"], name="fk_sections_batch_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("batch_id", "name", name="uq_sections_batch_id_name"),
        sa.CheckConstraint("max_capacity > 0", name="ck_sections_capacity"),
        schema=SCHEMA,
    )

    op.create_table(
        "courses",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("department_id", _UUID, nullable=False),
        sa.Column("code", sa.String(20), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("credits", sa.Numeric(3, 1), nullable=False),
        sa.Column("lecture_hours", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("lab_hours", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_ts(),
        sa.ForeignKeyConstraint(
            ["department_id"], [f"{SCHEMA}.departments.id"], name="fk_courses_department_id",
            ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("code", name="uq_courses_code"),
        schema=SCHEMA,
    )

    op.create_table(
        "course_prerequisites",
        sa.Column("course_id", _UUID, nullable=False),
        sa.Column("prerequisite_course_id", _UUID, nullable=False),
        sa.PrimaryKeyConstraint(
            "course_id", "prerequisite_course_id", name="pk_course_prerequisites"
        ),
        sa.ForeignKeyConstraint(
            ["course_id"], [f"{SCHEMA}.courses.id"], name="fk_course_prerequisites_course_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["prerequisite_course_id"], [f"{SCHEMA}.courses.id"],
            name="fk_course_prerequisites_prerequisite_course_id", ondelete="CASCADE",
        ),
        sa.CheckConstraint(
            "course_id <> prerequisite_course_id", name="ck_course_prerequisites_no_self"
        ),
        schema=SCHEMA,
    )

    op.create_index("idx_batches_session_id", "batches", ["session_id"], schema=SCHEMA)
    op.create_index("idx_batches_department_id", "batches", ["department_id"], schema=SCHEMA)
    op.create_index("idx_semesters_session_id", "semesters", ["session_id"], schema=SCHEMA)
    op.create_index("idx_sections_batch_id", "sections", ["batch_id"], schema=SCHEMA)
    op.create_index("idx_courses_department_id", "courses", ["department_id"], schema=SCHEMA)
    op.create_index(
        "idx_active_sessions", "sessions", ["id"], schema=SCHEMA,
        postgresql_where=sa.text("is_current = true"),
    )


def downgrade() -> None:
    op.drop_table("course_prerequisites", schema=SCHEMA)
    op.drop_table("courses", schema=SCHEMA)
    op.drop_table("sections", schema=SCHEMA)
    op.drop_table("batches", schema=SCHEMA)
    op.drop_table("semesters", schema=SCHEMA)
    op.drop_table("sessions", schema=SCHEMA)
    op.drop_table("departments", schema=SCHEMA)
    op.execute(f"DROP SCHEMA IF EXISTS {SCHEMA}")
