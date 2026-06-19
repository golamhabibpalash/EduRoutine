"""Role & permission application service."""

from __future__ import annotations

from uuid import UUID, uuid4

from src.application.common.dto.pagination import Page, PageParams
from src.application.common.exceptions import ConflictError, ValidationError
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.roles.dto import PermissionDTO, RoleDTO
from src.domain.identity.entities.permission import Permission
from src.domain.identity.entities.role import Role
from src.domain.identity.exceptions import RoleNotFoundError
from src.shared.utils.clock import utcnow


class RoleService:
    """Use cases for the Roles & Permissions modules."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    # ------------------------------------------------------------------ roles
    async def get_role(self, role_id: UUID) -> RoleDTO:
        role = await self._require(role_id)
        return await self._to_dto(role)

    async def list_roles(self, page: PageParams) -> Page[RoleDTO]:
        roles = await self._uow.roles.list_page(limit=page.limit, offset=page.offset)
        total = await self._uow.roles.count()
        items = [await self._to_dto(r) for r in roles]
        return Page(items=items, page=page.page, page_size=page.page_size, total_items=total)

    async def create_role(
        self, *, name: str, description: str | None, permission_ids: tuple[UUID, ...]
    ) -> RoleDTO:
        if await self._uow.roles.get_by_name(name) is not None:
            raise ConflictError(f"A role named '{name}' already exists.")
        await self._validate_permissions_exist(permission_ids)
        role = Role(id=uuid4(), name=name, description=description)
        await self._uow.roles.add(role)
        await self._uow.flush()  # parent row must exist before role_permissions FK inserts
        if permission_ids:
            await self._uow.roles.set_permission_ids(role.id, set(permission_ids))
        await self._uow.commit()
        return await self._to_dto(role)

    async def update_role(
        self,
        role_id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
        description_set: bool = False,
    ) -> RoleDTO:
        role = await self._require(role_id)
        if role.is_system_role and name is not None and name != role.name:
            raise ValidationError("System roles cannot be renamed.")
        if name is not None:
            existing = await self._uow.roles.get_by_name(name)
            if existing is not None and existing.id != role_id:
                raise ConflictError(f"A role named '{name}' already exists.")
            role.name = name
        if description_set:
            role.description = description
        await self._uow.roles.update(role)
        await self._uow.commit()
        return await self._to_dto(role)

    async def delete_role(self, role_id: UUID) -> None:
        role = await self._require(role_id)
        if role.is_system_role:
            raise ConflictError("System roles cannot be deleted.")
        await self._uow.roles.delete(role)
        await self._uow.commit()

    # ------------------------------------------------------------- permissions
    async def get_role_permissions(self, role_id: UUID) -> list[PermissionDTO]:
        await self._require(role_id)
        ids = await self._uow.roles.get_permission_ids(role_id)
        permissions = await self._uow.permissions.list_by_ids(ids)
        return [self._perm_to_dto(p) for p in permissions]

    async def set_role_permissions(
        self, role_id: UUID, permission_ids: tuple[UUID, ...]
    ) -> list[PermissionDTO]:
        await self._require(role_id)
        await self._validate_permissions_exist(permission_ids)
        await self._uow.roles.set_permission_ids(role_id, set(permission_ids))
        await self._uow.commit()
        permissions = await self._uow.permissions.list_by_ids(set(permission_ids))
        return [self._perm_to_dto(p) for p in permissions]

    async def list_permissions(
        self, page: PageParams, *, module: str | None = None
    ) -> Page[PermissionDTO]:
        permissions = await self._uow.permissions.list_page(
            module=module, limit=page.limit, offset=page.offset
        )
        total = await self._uow.permissions.count(module=module)
        items = [self._perm_to_dto(p) for p in permissions]
        return Page(items=items, page=page.page, page_size=page.page_size, total_items=total)

    # ----------------------------------------------------------------- helpers
    async def _require(self, role_id: UUID) -> Role:
        role = await self._uow.roles.get(role_id)
        if role is None:
            raise RoleNotFoundError(f"Role '{role_id}' not found.")
        return role

    async def _validate_permissions_exist(self, permission_ids: tuple[UUID, ...]) -> None:
        for permission_id in permission_ids:
            if await self._uow.permissions.get(permission_id) is None:
                raise ValidationError(f"Permission '{permission_id}' does not exist.")

    async def _to_dto(self, role: Role) -> RoleDTO:
        count = await self._uow.roles.permission_count(role.id)
        return RoleDTO(
            id=role.id,
            name=role.name,
            description=role.description,
            is_system_role=role.is_system_role,
            permission_count=count,
            created_at=role.created_at or utcnow(),
        )

    @staticmethod
    def _perm_to_dto(permission: Permission) -> PermissionDTO:
        return PermissionDTO(
            id=permission.id,
            code=permission.code,
            name=permission.name,
            module=permission.module,
            description=permission.description,
        )
