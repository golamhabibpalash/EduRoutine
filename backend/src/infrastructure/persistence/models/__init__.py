"""SQLAlchemy ORM models. Importing this package registers all tables on ``Base.metadata``."""

from src.infrastructure.persistence.models.base import Base
from src.infrastructure.persistence.models.identity import (
    PermissionModel,
    RefreshTokenModel,
    RoleModel,
    RolePermissionModel,
    UserClaimModel,
    UserModel,
    UserRoleModel,
)

__all__ = [
    "Base",
    "PermissionModel",
    "RefreshTokenModel",
    "RoleModel",
    "RolePermissionModel",
    "UserClaimModel",
    "UserModel",
    "UserRoleModel",
]
