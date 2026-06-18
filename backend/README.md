# EduRoutine — Backend

FastAPI backend following Clean Architecture (Domain → Application → Infrastructure → Presentation),
DDD, and CQRS. See `../docs/04-system-architecture.md` and `../docs/11-coding-standards.md`.

> **Status: Phase 1 skeleton.** Only `GET /api/v1/health` is exposed. Identity layers
> (User / Role / Permission / Claim) are scaffolded (entities, repositories, DTOs, CQRS handlers as
> stubs) but no business endpoints are wired. No routine system, scheduling engine, or social login.

## Layout (`src/`)
| Layer | Package | Responsibility |
|---|---|---|
| Presentation | `presentation/` | FastAPI routers, middleware, DI, response/error envelopes |
| Application | `application/` | CQRS commands/queries, DTOs, ports (UoW), services |
| Domain | `domain/` | Pure entities, value objects, repository interfaces, events |
| Infrastructure | `infrastructure/` | SQLAlchemy models + repos, UoW, auth (hasher/JWT), persistence |
| Shared | `shared/` | Settings, cross-cutting utils |

## Quick start (local)
```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env

# Run the API (health check only in Phase 1)
uvicorn src.main:app --reload
# -> http://localhost:8000/api/v1/health
# -> http://localhost:8000/docs

# Migrations (requires a running PostgreSQL from .env DATABASE_URL)
alembic upgrade head

# Tests / quality gates
pytest
ruff check . && mypy src
```

## Notes / decisions (for Phase 1 review)
- API paths referenced in the task brief (`/contracts/openapi/openapi.yaml`,
  `/docs/database/schema.sql`, `/docs/architecture/`) are empty placeholders. The implemented
  contract source is `../contracts/openapi.yaml`; DB design source is `../docs/03-database-design.md`.
- Identity models follow `docs/03` + the OpenAPI contract (`is_active` boolean, no `tenant_id`).
  The multi-tenant / `status`-enum / MFA variant in `docs/12-postgresql-architecture.md` is deferred
  (roadmap Phase 4) to keep the API contract unchanged.
