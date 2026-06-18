# Alembic migrations

Async Alembic environment for EduRoutine. The database URL is injected from application settings
(`src/shared/config/settings.py`) at runtime; `alembic.ini` leaves `sqlalchemy.url` blank.

```bash
cd backend
alembic upgrade head                       # apply migrations
alembic revision --autogenerate -m "msg"   # generate a new migration (review before commit)
alembic downgrade -1                        # roll back one revision
```

`0001_identity_schema` creates the `identity` schema and the User / Role / Permission / Claim
tables (+ join tables and refresh tokens) for Phase 1.
