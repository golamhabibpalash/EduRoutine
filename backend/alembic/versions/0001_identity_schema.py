"""identity schema — users, roles, permissions, claims (Phase 1)

Revision ID: 0001_identity_schema
Revises:
Create Date: 2026-06-18

Creates the ``identity`` schema and the Phase 1 identity tables, faithful to
docs/03-database-design.md and src/infrastructure/persistence/models/identity.py.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_identity_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "identity"

_UUID = postgresql.UUID(as_uuid=True)
_UUID_PK = sa.text("gen_random_uuid()")
_NOW = sa.text("now()")


def upgrade() -> None:
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

    op.create_table(
        "users",
        sa.Column("id", _UUID, primary_key=True, server_default=_UUID_PK),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("password_hash", sa.String(512), nullable=False),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.UniqueConstraint("email", name="uq_users_email"),
        schema=SCHEMA,
    )

    op.create_table(
        "roles",
        sa.Column("id", _UUID, primary_key=True, server_default=_UUID_PK),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("is_system_role", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.UniqueConstraint("name", name="uq_roles_name"),
        schema=SCHEMA,
    )

    op.create_table(
        "permissions",
        sa.Column("id", _UUID, primary_key=True, server_default=_UUID_PK),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("module", sa.String(100), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.UniqueConstraint("code", name="uq_permissions_code"),
        schema=SCHEMA,
    )

    op.create_table(
        "user_roles",
        sa.Column("user_id", _UUID, nullable=False),
        sa.Column("role_id", _UUID, nullable=False),
        sa.PrimaryKeyConstraint("user_id", "role_id", name="pk_user_roles"),
        sa.ForeignKeyConstraint(
            ["user_id"], [f"{SCHEMA}.users.id"], name="fk_user_roles_user_id", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["role_id"], [f"{SCHEMA}.roles.id"], name="fk_user_roles_role_id", ondelete="CASCADE"
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "role_permissions",
        sa.Column("role_id", _UUID, nullable=False),
        sa.Column("permission_id", _UUID, nullable=False),
        sa.PrimaryKeyConstraint("role_id", "permission_id", name="pk_role_permissions"),
        sa.ForeignKeyConstraint(
            ["role_id"],
            [f"{SCHEMA}.roles.id"],
            name="fk_role_permissions_role_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            [f"{SCHEMA}.permissions.id"],
            name="fk_role_permissions_permission_id",
            ondelete="CASCADE",
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "user_claims",
        sa.Column("id", _UUID, primary_key=True, server_default=_UUID_PK),
        sa.Column("user_id", _UUID, nullable=False),
        sa.Column("claim_type", sa.String(200), nullable=False),
        sa.Column("claim_value", sa.String(500), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], [f"{SCHEMA}.users.id"], name="fk_user_claims_user_id", ondelete="CASCADE"
        ),
        sa.UniqueConstraint(
            "user_id", "claim_type", "claim_value", name="uq_user_claims_user_type_value"
        ),
        schema=SCHEMA,
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", _UUID, primary_key=True, server_default=_UUID_PK),
        sa.Column("user_id", _UUID, nullable=False),
        sa.Column("token_hash", sa.String(512), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("device_info", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=_NOW),
        sa.ForeignKeyConstraint(
            ["user_id"],
            [f"{SCHEMA}.users.id"],
            name="fk_refresh_tokens_user_id",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("token_hash", name="uq_refresh_tokens_token_hash"),
        schema=SCHEMA,
    )

    op.create_index("idx_user_claims_user_id", "user_claims", ["user_id"], schema=SCHEMA)
    op.create_index("idx_refresh_tokens_user_id", "refresh_tokens", ["user_id"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_table("refresh_tokens", schema=SCHEMA)
    op.drop_table("user_claims", schema=SCHEMA)
    op.drop_table("role_permissions", schema=SCHEMA)
    op.drop_table("user_roles", schema=SCHEMA)
    op.drop_table("permissions", schema=SCHEMA)
    op.drop_table("roles", schema=SCHEMA)
    op.drop_table("users", schema=SCHEMA)
    op.execute(f"DROP SCHEMA IF EXISTS {SCHEMA}")
