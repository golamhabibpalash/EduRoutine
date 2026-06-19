"""Users API router — profile, CRUD, role assignment, and claims (bare responses)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.common.dto.pagination import PageParams
from src.presentation.api.common.response_models import PaginatedResponse, paginate
from src.presentation.api.dependencies.auth import (
    CurrentUserId,
    Principal,
    require_permission,
)
from src.presentation.api.dependencies.services import UserServiceDep
from src.presentation.api.v1.roles.schemas import RoleData
from src.presentation.api.v1.users.schemas import (
    ChangePasswordRequest,
    ClaimData,
    CreateClaimRequest,
    CreateUserRequest,
    ReplaceUserRequest,
    SetUserRolesRequest,
    UpdateProfileRequest,
    UpdateUserRequest,
    UserData,
)

router = APIRouter(tags=["Users"])

PageQuery = Annotated[int, Query(ge=1)]
PageSizeQuery = Annotated[int, Query(ge=1, le=100)]


# --------------------------------------------------------------------- /users/me
@router.get("/users/me", response_model=UserData, operation_id="getCurrentUser")
async def get_me(user_id: CurrentUserId, service: UserServiceDep) -> UserData:
    return UserData.from_dto(await service.get_user(user_id))


@router.patch("/users/me", response_model=UserData, operation_id="updateCurrentUser")
async def update_me(
    body: UpdateProfileRequest, user_id: CurrentUserId, service: UserServiceDep
) -> UserData:
    dto = await service.update_user(
        user_id,
        display_name=body.display_name,
        phone=body.phone,
        phone_set="phone" in body.model_fields_set,
    )
    return UserData.from_dto(dto)


@router.put("/users/me/password", status_code=204, operation_id="changePassword")
async def change_password(
    body: ChangePasswordRequest, user_id: CurrentUserId, service: UserServiceDep
) -> None:
    await service.change_password(
        user_id, current_password=body.current_password, new_password=body.new_password
    )


# ------------------------------------------------------------------ collection
@router.get("/users", response_model=PaginatedResponse[UserData], operation_id="listUsers")
async def list_users(
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:read:*"))],
    page: PageQuery = 1,
    page_size: PageSizeQuery = 20,
    is_active: Annotated[bool | None, Query()] = None,
) -> PaginatedResponse[UserData]:
    result = await service.list_users(PageParams(page, page_size), is_active=is_active)
    return paginate(
        [UserData.from_dto(d) for d in result.items],
        page=result.page,
        page_size=result.page_size,
        total_items=result.total_items,
    )


@router.post("/users", response_model=UserData, status_code=201, operation_id="createUser")
async def create_user(
    body: CreateUserRequest,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:create:*"))],
) -> UserData:
    dto = await service.create_user(
        email=body.email,
        password=body.password,
        display_name=body.display_name,
        phone=body.phone,
        is_active=body.is_active,
        role_ids=tuple(body.role_ids),
    )
    return UserData.from_dto(dto)


# --------------------------------------------------------------------- /users/{id}
@router.get("/users/{user_id}", response_model=UserData, operation_id="getUser")
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:read:*"))],
) -> UserData:
    return UserData.from_dto(await service.get_user(user_id))


@router.put("/users/{user_id}", response_model=UserData, operation_id="replaceUser")
async def replace_user(
    user_id: UUID,
    body: ReplaceUserRequest,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:update:*"))],
) -> UserData:
    dto = await service.replace_user(
        user_id, display_name=body.display_name, phone=body.phone, is_active=body.is_active
    )
    return UserData.from_dto(dto)


@router.patch("/users/{user_id}", response_model=UserData, operation_id="patchUser")
async def patch_user(
    user_id: UUID,
    body: UpdateUserRequest,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:update:*"))],
) -> UserData:
    dto = await service.update_user(
        user_id,
        display_name=body.display_name,
        phone=body.phone,
        phone_set="phone" in body.model_fields_set,
        is_active=body.is_active,
    )
    return UserData.from_dto(dto)


@router.delete("/users/{user_id}", status_code=204, operation_id="deactivateUser")
async def deactivate_user(
    user_id: UUID,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:delete:*"))],
) -> None:
    await service.deactivate_user(user_id)


# ------------------------------------------------------------- /users/{id}/roles
@router.get("/users/{user_id}/roles", response_model=list[RoleData], operation_id="getUserRoles")
async def get_user_roles(
    user_id: UUID,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:read:*"))],
) -> list[RoleData]:
    return [RoleData.from_dto(r) for r in await service.get_user_roles(user_id)]


@router.put("/users/{user_id}/roles", response_model=list[RoleData], operation_id="setUserRoles")
async def set_user_roles(
    user_id: UUID,
    body: SetUserRolesRequest,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("role:assign:*"))],
) -> list[RoleData]:
    roles = await service.set_user_roles(user_id, tuple(body.role_ids))
    return [RoleData.from_dto(r) for r in roles]


# ------------------------------------------------------------ /users/{id}/claims
@router.get("/users/{user_id}/claims", response_model=list[ClaimData], operation_id="getUserClaims")
async def get_user_claims(
    user_id: UUID,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:read:*"))],
) -> list[ClaimData]:
    return [ClaimData.from_dto(c) for c in await service.list_claims(user_id)]


@router.post(
    "/users/{user_id}/claims",
    response_model=ClaimData,
    status_code=201,
    operation_id="addUserClaim",
)
async def add_user_claim(
    user_id: UUID,
    body: CreateClaimRequest,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:update:*"))],
) -> ClaimData:
    dto = await service.add_claim(user_id, claim_type=body.claim_type, claim_value=body.claim_value)
    return ClaimData.from_dto(dto)


@router.delete(
    "/users/{user_id}/claims/{claim_id}", status_code=204, operation_id="deleteUserClaim"
)
async def delete_user_claim(
    user_id: UUID,
    claim_id: UUID,
    service: UserServiceDep,
    _principal: Annotated[Principal, Depends(require_permission("user:update:*"))],
) -> None:
    await service.delete_claim(user_id, claim_id)
