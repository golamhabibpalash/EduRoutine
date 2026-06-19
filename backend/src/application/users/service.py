"""User application service — CRUD, profile, role assignment, and claims."""

from __future__ import annotations

from uuid import UUID, uuid4

from src.application.common.dto.pagination import Page, PageParams
from src.application.common.exceptions import ConflictError, ValidationError
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.roles.dto import RoleDTO
from src.application.users.dto import ClaimDTO, UserDTO
from src.domain.identity.entities.claim import Claim
from src.domain.identity.entities.user import User
from src.domain.identity.exceptions import UserNotFoundError
from src.domain.identity.services import PasswordHasher
from src.domain.identity.value_objects.email import EmailAddress
from src.shared.utils.clock import utcnow


class UserService:
    """Use cases for the Users module."""

    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self._uow = uow
        self._hasher = password_hasher

    # ------------------------------------------------------------------ reads
    async def get_user(self, user_id: UUID) -> UserDTO:
        user = await self._uow.users.get(user_id)
        if user is None:
            raise UserNotFoundError(f"User '{user_id}' not found.")
        return await self._to_dto(user)

    async def list_users(self, page: PageParams, *, is_active: bool | None = None) -> Page[UserDTO]:
        users = await self._uow.users.list_page(
            limit=page.limit, offset=page.offset, is_active=is_active
        )
        total = await self._uow.users.count(is_active=is_active)
        items = [await self._to_dto(u) for u in users]
        return Page(items=items, page=page.page, page_size=page.page_size, total_items=total)

    # ----------------------------------------------------------------- writes
    async def create_user(
        self,
        *,
        email: str,
        password: str,
        display_name: str,
        phone: str | None = None,
        is_active: bool = True,
        role_ids: tuple[UUID, ...] = (),
    ) -> UserDTO:
        email_vo = EmailAddress(email)
        if await self._uow.users.exists_by_email(email_vo):
            raise ConflictError("A user with this email already exists.")
        await self._validate_roles_exist(role_ids)

        now = utcnow()
        user = User(
            id=uuid4(),
            email=email_vo,
            password_hash=self._hasher.hash(password),
            display_name=display_name,
            phone=phone,
            is_active=is_active,
            created_at=now,
            updated_at=now,
        )
        await self._uow.users.add(user)
        await self._uow.flush()  # parent row must exist before user_roles FK inserts
        if role_ids:
            await self._uow.users.set_role_ids(user.id, set(role_ids))
        await self._uow.commit()
        return await self._to_dto(user)

    async def update_user(
        self,
        user_id: UUID,
        *,
        display_name: str | None = None,
        phone: str | None = None,
        phone_set: bool = False,
        is_active: bool | None = None,
    ) -> UserDTO:
        user = await self._require(user_id)
        if display_name is not None:
            user.display_name = display_name
        if phone_set:
            user.phone = phone
        if is_active is not None:
            user.is_active = is_active
        user.updated_at = utcnow()
        await self._uow.users.update(user)
        await self._uow.commit()
        return await self._to_dto(user)

    async def replace_user(
        self, user_id: UUID, *, display_name: str, phone: str | None, is_active: bool
    ) -> UserDTO:
        user = await self._require(user_id)
        user.display_name = display_name
        user.phone = phone
        user.is_active = is_active
        user.updated_at = utcnow()
        await self._uow.users.update(user)
        await self._uow.commit()
        return await self._to_dto(user)

    async def deactivate_user(self, user_id: UUID) -> None:
        user = await self._require(user_id)
        user.deactivate()
        user.updated_at = utcnow()
        await self._uow.users.update(user)
        await self._uow.commit()

    async def change_password(
        self, user_id: UUID, *, current_password: str, new_password: str
    ) -> None:
        user = await self._require(user_id)
        if not self._hasher.verify(current_password, user.password_hash):
            raise ValidationError("Current password is incorrect.")
        user.password_hash = self._hasher.hash(new_password)
        user.updated_at = utcnow()
        await self._uow.users.update(user)
        await self._uow.commit()

    # ------------------------------------------------------------------ roles
    async def get_user_roles(self, user_id: UUID) -> list[RoleDTO]:
        await self._require(user_id)
        role_ids = await self._uow.users.get_role_ids(user_id)
        return await self._roles_to_dto(role_ids)

    async def set_user_roles(self, user_id: UUID, role_ids: tuple[UUID, ...]) -> list[RoleDTO]:
        await self._require(user_id)
        await self._validate_roles_exist(role_ids)
        await self._uow.users.set_role_ids(user_id, set(role_ids))
        await self._uow.commit()
        return await self._roles_to_dto(set(role_ids))

    # ----------------------------------------------------------------- claims
    async def list_claims(self, user_id: UUID) -> list[ClaimDTO]:
        await self._require(user_id)
        claims = await self._uow.claims.list_for_user(user_id)
        return [ClaimDTO(c.id, c.user_id, c.claim_type, c.claim_value) for c in claims]

    async def add_claim(self, user_id: UUID, *, claim_type: str, claim_value: str) -> ClaimDTO:
        await self._require(user_id)
        if await self._uow.claims.exists(user_id, claim_type, claim_value):
            raise ConflictError("This claim already exists for the user.")
        claim = Claim(id=uuid4(), user_id=user_id, claim_type=claim_type, claim_value=claim_value)
        await self._uow.claims.add(claim)
        await self._uow.commit()
        return ClaimDTO(claim.id, claim.user_id, claim.claim_type, claim.claim_value)

    async def delete_claim(self, user_id: UUID, claim_id: UUID) -> None:
        claim = await self._uow.claims.get(claim_id)
        if claim is None or claim.user_id != user_id:
            raise UserNotFoundError(f"Claim '{claim_id}' not found for user '{user_id}'.")
        await self._uow.claims.delete(claim)
        await self._uow.commit()

    # ----------------------------------------------------------------- helpers
    async def _require(self, user_id: UUID) -> User:
        user = await self._uow.users.get(user_id)
        if user is None:
            raise UserNotFoundError(f"User '{user_id}' not found.")
        return user

    async def _validate_roles_exist(self, role_ids: tuple[UUID, ...]) -> None:
        for role_id in role_ids:
            if await self._uow.roles.get(role_id) is None:
                raise ValidationError(f"Role '{role_id}' does not exist.")

    async def _to_dto(self, user: User) -> UserDTO:
        role_names = await self._uow.users.get_role_names(user.id)
        return UserDTO(
            id=user.id,
            email=user.email.value,
            email_verified=user.email_verified,
            display_name=user.display_name,
            phone=user.phone,
            is_active=user.is_active,
            roles=tuple(role_names),
            last_login_at=user.last_login_at,
            created_at=user.created_at or utcnow(),
            updated_at=user.updated_at or utcnow(),
        )

    async def _roles_to_dto(self, role_ids: set[UUID]) -> list[RoleDTO]:
        dtos: list[RoleDTO] = []
        for role_id in role_ids:
            role = await self._uow.roles.get(role_id)
            if role is None:
                continue
            count = await self._uow.roles.permission_count(role_id)
            dtos.append(
                RoleDTO(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    is_system_role=role.is_system_role,
                    permission_count=count,
                    created_at=role.created_at or utcnow(),
                )
            )
        return sorted(dtos, key=lambda r: r.name)
