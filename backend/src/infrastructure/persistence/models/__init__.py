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
from src.infrastructure.persistence.models.people import StudentModel, TeacherModel
from src.infrastructure.persistence.models.resources import RoomModel
from src.infrastructure.persistence.models.timetable import PeriodModel

__all__ = [
    "Base",
    "BatchModel",
    "CourseModel",
    "CoursePrerequisiteModel",
    "DepartmentModel",
    "PeriodModel",
    "PermissionModel",
    "RefreshTokenModel",
    "RoleModel",
    "RolePermissionModel",
    "RoomModel",
    "SectionModel",
    "SemesterModel",
    "SessionModel",
    "StudentModel",
    "TeacherModel",
    "UserClaimModel",
    "UserModel",
    "UserRoleModel",
]
