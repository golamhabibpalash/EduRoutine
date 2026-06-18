# AI Collaboration Rules

## Project Identity
- **Project**: EduRoutine — Educational Institution Timetable Management System
- **Stack**: Python 3.13+ / FastAPI / SQLAlchemy 2.x / PostgreSQL / Redis / Next.js 15+ / TypeScript
- **Architecture**: Clean Architecture (Domain → Application → Infrastructure → Presentation)
- **Patterns**: DDD, CQRS, Event-Driven, Repository, Unit of Work

## Code Generation Rules

### General
- All code must include type hints (Python) or TypeScript types (frontend)
- Follow existing naming conventions from `docs/11-coding-standards.md`
- Never commit secrets, API keys, or credentials
- Use dependency injection — no service locator or global singletons

### Backend (Python)
- **Domain layer**: Pure Python, zero framework dependencies. Dataclasses or Pydantic for entities/value objects. Repository interfaces only (no implementations).
- **Application layer**: Pydantic DTOs for all inputs/outputs. Handlers receive commands/queries, orchestrate domain objects, call repository interfaces.
- **Infrastructure layer**: SQLAlchemy models inherit from a declarative base. Repository implementations implement domain interfaces. Alembic for migrations.
- **Presentation layer**: FastAPI routers are thin — no business logic. Request validation via Pydantic. Response serialization via DTOs.

### Frontend (TypeScript)
- Components in `features/` — one folder per domain capability
- Shared UI primitives in `components/ui/` (ShadCN)
- Data fetching via TanStack Query in `services/`
- State via Zustand in `store/`
- All API types in `types/`

### Database
- All DDL changes via Alembic migrations (never raw SQL in production)
- UUID primary keys, snake_case naming, explicit FK constraints
- See `docs/12-postgresql-architecture.md` for full schema

### Testing
- Unit tests for domain and application layers
- Integration tests for database and API
- Factories in `tests/fixtures/` for test data

## Documentation
- Architecture docs in `docs/` — update when significant changes are made
- API contracts in `contracts/` — keep OpenAPI spec in sync
- This file must be read at the start of every session
