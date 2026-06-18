"""Seed the database with a default admin user.

Usage:
    python -m scripts.seed
"""

from __future__ import annotations

import asyncio

from src.application.auth.seed import ADMIN_EMAIL, ADMIN_PASSWORD, seed_admin_user


async def seed() -> None:
    await seed_admin_user()
    print(f"Admin user ready: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed())
