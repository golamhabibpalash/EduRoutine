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
    PasswordResetTokenModel,
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
from src.infrastructure.persistence.models.timetable import (
    PeriodModel,
    RoutineDetailModel,
    RoutineModel,
)

__all__ = [
    "Base",
    "BatchModel",
    "CourseModel",
    "CoursePrerequisiteModel",
    "DepartmentModel",
    "PasswordResetTokenModel",
    "PeriodModel",
    "PermissionModel",
    "RefreshTokenModel",
    "RoleModel",
    "RolePermissionModel",
    "RoomModel",
    "RoutineDetailModel",
    "RoutineModel",
    "SectionModel",
    "SemesterModel",
    "SessionModel",
    "StudentModel",
    "TeacherModel",
    "UserClaimModel",
    "UserModel",
    "UserRoleModel",
]
