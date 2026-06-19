"""Identity schema ORM models — users, roles, permissions, claims, and join tables.

Faithful to docs/03-database-design.md (identity.*) and the OpenAPI contract
(``is_active`` boolean; multi-tenancy/MFA from docs/12 deferred to a later phase).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

SCHEMA = "identity"


class UserModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """``identity.users``."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        {"schema": SCHEMA},
    )

    email: Mapped[str] = mapped_column(String(255), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class RoleModel(UUIDPrimaryKeyMixin, Base):
    """``identity.roles``."""

    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint("name", name="uq_roles_name"),
        {"schema": SCHEMA},
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_system_role: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class PermissionModel(UUIDPrimaryKeyMixin, Base):
    """``identity.permissions``."""

    __tablename__ = "permissions"
    __table_args__ = (
        UniqueConstraint("code", name="uq_permissions_code"),
        {"schema": SCHEMA},
    )

    code: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    module: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)


class UserRoleModel(Base):
    """``identity.user_roles`` — user↔role association."""

    __tablename__ = "user_roles"
    __table_args__ = {"schema": SCHEMA}

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.roles.id", ondelete="CASCADE"),
        primary_key=True,
    )


class RolePermissionModel(Base):
    """``identity.role_permissions`` — role↔permission association."""

    __tablename__ = "role_permissions"
    __table_args__ = {"schema": SCHEMA}

    role_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )


class UserClaimModel(UUIDPrimaryKeyMixin, Base):
    """``identity.user_claims``."""

    __tablename__ = "user_claims"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "claim_type", "claim_value", name="uq_user_claims_user_type_value"
        ),
        {"schema": SCHEMA},
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    claim_type: Mapped[str] = mapped_column(String(200), nullable=False)
    claim_value: Mapped[str] = mapped_column(String(500), nullable=False)


class RefreshTokenModel(UUIDPrimaryKeyMixin, Base):
    """``identity.refresh_tokens`` (opaque token store; SHA-256 hashed)."""

    __tablename__ = "refresh_tokens"
    __table_args__ = (
        UniqueConstraint("token_hash", name="uq_refresh_tokens_token_hash"),
        {"schema": SCHEMA},
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    device_info: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class PasswordResetTokenModel(UUIDPrimaryKeyMixin, Base):
    """``identity.password_reset_tokens`` (opaque, SHA-256 hashed, single-use)."""

    __tablename__ = "password_reset_tokens"
    __table_args__ = (
        UniqueConstraint("token_hash", name="uq_password_reset_tokens_token_hash"),
        {"schema": SCHEMA},
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
