"""Seed-data endpoint — populates demo data on demand (development only)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.shared.config.settings import get_settings

router = APIRouter(tags=["Seed"])


@router.post(
    "/seed",
    summary="Seed demo data",
    description="Insert sample departments, sessions, semesters, batches, sections, courses, periods, rooms, teachers, and students. Idempotent — skips existing records. Only available in development mode.",
)
async def seed_demo_data() -> dict[str, str]:
    """Seed all entity types with demo data."""
    settings = get_settings()
    if settings.app_env != "development":
        raise HTTPException(status_code=403, detail="Seeding is only allowed in development mode.")
    from src.application.auth.seed import seed_identity
    from src.application.data.seed import seed_data

    try:
        await seed_identity()
    except Exception:
        pass

    await seed_data()
    return {"status": "success", "message": "Demo data seeded successfully."}
