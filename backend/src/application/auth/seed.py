"""Seed baseline identity data on first startup (development mode).

Creates the permission catalog, the built-in roles, and the default admin user (granted the
``super_admin`` role). Idempotent: existing rows are left untouched.
"""

from __future__ import annotations

from uuid import UUID, uuid4

from src.domain.identity.entities.permission import Permission
from src.domain.identity.entities.role import Role
from src.domain.identity.entities.user import User
from src.domain.identity.value_objects.email import EmailAddress
from src.infrastructure.auth.password_hasher import Argon2PasswordHasher
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.shared.utils.clock import utcnow

ADMIN_EMAIL = "admin@eduroutine.com"
ADMIN_PASSWORD = "Admin123!"  # noqa: S105 — dev seed default; not a production secret
ADMIN_DISPLAY_NAME = "System Administrator"

SUPER_ADMIN_ROLE = "super_admin"

# (code, name, module) — focused identity catalog for Phase 2.
PERMISSION_CATALOG: tuple[tuple[str, str, str], ...] = (
    ("user:create:*", "Create users", "user"),
    ("user:read:*", "Read users", "user"),
    ("user:update:*", "Update users", "user"),
    ("user:delete:*", "Deactivate users", "user"),
    ("role:create:*", "Create roles", "role"),
    ("role:read:*", "Read roles", "role"),
    ("role:update:*", "Update roles", "role"),
    ("role:delete:*", "Delete roles", "role"),
    ("role:assign:*", "Assign roles to users", "role"),
    # academic structure
    ("department:create:*", "Create departments", "department"),
    ("department:read:*", "Read departments", "department"),
    ("department:update:*", "Update departments", "department"),
    ("department:delete:*", "Delete departments", "department"),
    ("session:create:*", "Create sessions", "session"),
    ("session:read:*", "Read sessions", "session"),
    ("session:update:*", "Update sessions", "session"),
    ("session:delete:*", "Delete sessions", "session"),
    ("semester:create:*", "Create semesters", "semester"),
    ("semester:read:*", "Read semesters", "semester"),
    ("semester:update:*", "Update semesters", "semester"),
    ("semester:delete:*", "Delete semesters", "semester"),
    ("batch:create:*", "Create batches", "batch"),
    ("batch:read:*", "Read batches", "batch"),
    ("batch:update:*", "Update batches", "batch"),
    ("batch:delete:*", "Delete batches", "batch"),
    ("section:create:*", "Create sections", "section"),
    ("section:read:*", "Read sections", "section"),
    ("section:update:*", "Update sections", "section"),
    ("section:delete:*", "Delete sections", "section"),
    ("course:create:*", "Create courses", "course"),
    ("course:read:*", "Read courses", "course"),
    ("course:update:*", "Update courses", "course"),
    ("course:delete:*", "Deactivate courses", "course"),
    # timetable
    ("period:create:*", "Create periods", "period"),
    ("period:read:*", "Read periods", "period"),
    ("period:update:*", "Update periods", "period"),
    ("period:delete:*", "Delete periods", "period"),
    # resources
    ("room:create:*", "Create rooms", "room"),
    ("room:read:*", "Read rooms", "room"),
    ("room:update:*", "Update rooms", "room"),
    ("room:delete:*", "Delete rooms", "room"),
    # people
    ("teacher:create:*", "Create teachers", "teacher"),
    ("teacher:read:*", "Read teachers", "teacher"),
    ("teacher:update:*", "Update teachers", "teacher"),
    ("teacher:delete:*", "Delete teachers", "teacher"),
    ("student:create:*", "Create students", "student"),
    ("student:read:*", "Read students", "student"),
    ("student:update:*", "Update students", "student"),
    ("student:delete:*", "Delete students", "student"),
)

# role name -> description
ROLE_CATALOG: dict[str, str] = {
    "super_admin": "Full system access.",
    "admin": "Institution-wide administration.",
    "faculty": "Teaching staff.",
    "student": "Enrolled student.",
}


async def seed_identity() -> None:
    """Seed permissions, roles, and the default admin user (idempotent)."""
    async with SqlAlchemyUnitOfWork() as uow:
        # --- permissions ---
        all_permission_ids: set[UUID] = set()
        for code, name, module in PERMISSION_CATALOG:
            existing = await uow.permissions.get_by_code(code)
            if existing is not None:
                all_permission_ids.add(existing.id)
            else:
                permission = Permission(id=uuid4(), code=code, name=name, module=module)
                await uow.permissions.add(permission)
                all_permission_ids.add(permission.id)

        # --- roles ---
        admin_tier_role_ids: list[UUID] = []
        super_admin_id: UUID | None = None
        for name, description in ROLE_CATALOG.items():
            existing_role = await uow.roles.get_by_name(name)
            if existing_role is not None:
                role_id = existing_role.id
            else:
                role = Role(id=uuid4(), name=name, description=description, is_system_role=True)
                await uow.roles.add(role)
                role_id = role.id
            if name == SUPER_ADMIN_ROLE:
                super_admin_id = role_id
            if name in (SUPER_ADMIN_ROLE, "admin"):
                admin_tier_role_ids.append(role_id)
        await uow.commit()

        # --- (re)grant the full catalog to admin-tier roles (idempotent) ---
        for role_id in admin_tier_role_ids:
            await uow.roles.set_permission_ids(role_id, all_permission_ids)
        await uow.commit()

        # --- default admin user ---
        email = EmailAddress(ADMIN_EMAIL)
        admin = await uow.users.get_by_email(email)
        if admin is None:
            now = utcnow()
            admin = User(
                id=uuid4(),
                email=email,
                password_hash=Argon2PasswordHasher().hash(ADMIN_PASSWORD),
                display_name=ADMIN_DISPLAY_NAME,
                email_verified=True,
                created_at=now,
                updated_at=now,
            )
            await uow.users.add(admin)
            await uow.commit()

        # Idempotently ensure the admin holds the super_admin role.
        if super_admin_id is not None:
            current_role_ids = await uow.users.get_role_ids(admin.id)
            if super_admin_id not in current_role_ids:
                await uow.users.set_role_ids(admin.id, current_role_ids | {super_admin_id})
                await uow.commit()
