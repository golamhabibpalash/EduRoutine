"""Roles & permissions API router (bare responses)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.common.dto.pagination import PageParams
from src.presentation.api.common.response_models import PaginatedResponse, paginate
from src.presentation.api.dependencies.auth import Principal, require_permission
from src.presentation.api.dependencies.services import RoleServiceDep
from src.presentation.api.v1.roles.schemas import (
    CreateRoleRequest,
    PermissionData,
    RoleData,
    SetRolePermissionsRequest,
    UpdateRoleRequest,
)

router = APIRouter(tags=["Roles"])

PageQuery = Annotated[int, Query(ge=1)]
PageSizeQuery = Annotated[int, Query(ge=1, le=100)]


@router.get("/roles", response_model=PaginatedResponse[RoleData], operation_id="listRoles")
async def list_roles(
    service: RoleServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:read:*"))],
    page: PageQuery = 1,
    page_size: PageSizeQuery = 20,
) -> PaginatedResponse[RoleData]:
    result = await service.list_roles(PageParams(page, page_size))
    return paginate(
        [RoleData.from_dto(d) for d in result.items],
        page=result.page,
        page_size=result.page_size,
        total_items=result.total_items,
    )


@router.post("/roles", response_model=RoleData, status_code=201, operation_id="createRole")
async def create_role(
    body: CreateRoleRequest,
    service: RoleServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:create:*"))],
) -> RoleData:
    dto = await service.create_role(
        name=body.name, description=body.description, permission_ids=tuple(body.permission_ids)
    )
    return RoleData.from_dto(dto)


@router.get("/roles/{role_id}", response_model=RoleData, operation_id="getRole")
async def get_role(
    role_id: UUID,
    service: RoleServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:read:*"))],
) -> RoleData:
    return RoleData.from_dto(await service.get_role(role_id))


@router.put("/roles/{role_id}", response_model=RoleData, operation_id="updateRole")
async def update_role(
    role_id: UUID,
    body: UpdateRoleRequest,
    service: RoleServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:update:*"))],
) -> RoleData:
    dto = await service.update_role(
        role_id,
        name=body.name,
        description=body.description,
        description_set="description" in body.model_fields_set,
    )
    return RoleData.from_dto(dto)


@router.delete("/roles/{role_id}", status_code=204, operation_id="deleteRole")
async def delete_role(
    role_id: UUID,
    service: RoleServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:delete:*"))],
) -> None:
    await service.delete_role(role_id)


@router.get(
    "/roles/{role_id}/permissions",
    response_model=list[PermissionData],
    operation_id="getRolePermissions",
)
async def get_role_permissions(
    role_id: UUID,
    service: RoleServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:read:*"))],
) -> list[PermissionData]:
    return [PermissionData.from_dto(p) for p in await service.get_role_permissions(role_id)]


@router.put(
    "/roles/{role_id}/permissions",
    response_model=list[PermissionData],
    operation_id="setRolePermissions",
)
async def set_role_permissions(
    role_id: UUID,
    body: SetRolePermissionsRequest,
    service: RoleServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:update:*"))],
) -> list[PermissionData]:
    permissions = await service.set_role_permissions(role_id, tuple(body.permission_ids))
    return [PermissionData.from_dto(p) for p in permissions]


@router.get(
    "/permissions",
    response_model=PaginatedResponse[PermissionData],
    tags=["Roles"],
    operation_id="listPermissions",
)
async def list_permissions(
    service: RoleServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:read:*"))],
    page: PageQuery = 1,
    page_size: PageSizeQuery = 20,
    module: Annotated[str | None, Query()] = None,
) -> PaginatedResponse[PermissionData]:
    result = await service.list_permissions(PageParams(page, page_size), module=module)
    return paginate(
        [PermissionData.from_dto(d) for d in result.items],
        page=result.page,
        page_size=result.page_size,
        total_items=result.total_items,
    )
