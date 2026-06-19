"""SQLAlchemy adapter for :class:`ClaimRepository`."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.claim import Claim
from src.infrastructure.persistence.models.identity import UserClaimModel


def _model_to_domain(model: UserClaimModel) -> Claim:
    return Claim(
        id=model.id,
        user_id=model.user_id,
        claim_type=model.claim_type,
        claim_value=model.claim_value,
    )


class SqlAlchemyClaimRepository:
    """Persists user :class:`Claim` rows via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, claim_id: UUID) -> Claim | None:
        model = await self._session.get(UserClaimModel, claim_id)
        return _model_to_domain(model) if model else None

    async def list_for_user(self, user_id: UUID) -> list[Claim]:
        result = await self._session.execute(
            select(UserClaimModel)
            .where(UserClaimModel.user_id == user_id)
            .order_by(UserClaimModel.claim_type)
        )
        return [_model_to_domain(row) for row in result.scalars()]

    async def exists(self, user_id: UUID, claim_type: str, claim_value: str) -> bool:
        result = await self._session.execute(
            select(UserClaimModel.id).where(
                UserClaimModel.user_id == user_id,
                UserClaimModel.claim_type == claim_type,
                UserClaimModel.claim_value == claim_value,
            )
        )
        return result.scalar() is not None

    async def add(self, claim: Claim) -> None:
        self._session.add(
            UserClaimModel(
                id=claim.id,
                user_id=claim.user_id,
                claim_type=claim.claim_type,
                claim_value=claim.claim_value,
            )
        )

    async def delete(self, claim: Claim) -> None:
        model = await self._session.get(UserClaimModel, claim.id)
        if model:
            await self._session.delete(model)
