"""SQLAlchemy adapter for :class:`ClaimRepository` (Phase 1 skeleton)."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.claim import Claim


class SqlAlchemyClaimRepository:
    """Persists user :class:`Claim` rows via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, claim_id: UUID) -> Claim | None:
        raise NotImplementedError("SqlAlchemyClaimRepository.get is a Phase 1 skeleton stub.")

    async def list_for_user(self, user_id: UUID) -> list[Claim]:
        raise NotImplementedError(
            "SqlAlchemyClaimRepository.list_for_user is a Phase 1 skeleton stub."
        )

    async def add(self, claim: Claim) -> None:
        raise NotImplementedError("SqlAlchemyClaimRepository.add is a Phase 1 skeleton stub.")

    async def delete(self, claim: Claim) -> None:
        raise NotImplementedError("SqlAlchemyClaimRepository.delete is a Phase 1 skeleton stub.")
