"""identity.password_reset_tokens — forgot/reset password flow

Revision ID: 0006_password_reset_tokens
Revises: 0005_people
Create Date: 2026-06-19
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006_password_reset_tokens"
down_revision: str | None = "0005_people"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "identity"
_UUID = postgresql.UUID(as_uuid=True)
_PK = sa.text("gen_random_uuid()")
_NOW = sa.text("now()")


def upgrade() -> None:
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", _UUID, primary_key=True, server_default=_PK),
        sa.Column("user_id", _UUID, nullable=False),
        sa.Column("token_hash", sa.String(512), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.ForeignKeyConstraint(
            ["user_id"], [f"{SCHEMA}.users.id"], name="fk_password_reset_tokens_user_id",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("token_hash", name="uq_password_reset_tokens_token_hash"),
        schema=SCHEMA,
    )
    op.create_index(
        "idx_password_reset_tokens_user_id", "password_reset_tokens", ["user_id"], schema=SCHEMA
    )


def downgrade() -> None:
    op.drop_table("password_reset_tokens", schema=SCHEMA)
