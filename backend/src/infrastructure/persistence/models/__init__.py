"""SQLAlchemy ORM models. Importing this package registers all tables on ``Base.metadata``."""

from src.infrastructure.persistence.models.academic import (
    BatchModel,
    CourseModel,
    CoursePrerequisiteModel,
    DepartmentModel,
    SectionModel,
    SemesterModel,
    SessionModel,
)
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
    "BatchModel",
    "CourseModel",
    "CoursePrerequisiteModel",
    "DepartmentModel",
    "PermissionModel",
    "RefreshTokenModel",
    "RoleModel",
    "RolePermissionModel",
    "SectionModel",
    "SemesterModel",
    "SessionModel",
    "UserClaimModel",
    "UserModel",
    "UserRoleModel",
]
