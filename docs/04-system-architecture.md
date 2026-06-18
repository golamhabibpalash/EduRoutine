# Phase 4: System Architecture

---

## 19. Clean Architecture Design

### Architecture Philosophy
EduRoutine follows **Clean Architecture** (Robert C. Martin) adapted for Python/FastAPI with DDD principles. The architecture enforces strict dependency inversion — inner layers define interfaces, outer layers implement them.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  FastAPI      │  │  GraphQL     │  │  Background Jobs │  │
│  │  Controllers  │  │  Resolvers   │  │  (Celery/ARQ)   │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                    │            │
│  ┌──────┴─────────────────┴────────────────────┴──────────┐ │
│  │                    API Gateway                          │ │
│  │  Rate Limiting │ Auth Middleware │ Validation │ Logging │ │
│  └────────────────────────┬───────────────────────────────┘ │
├───────────────────────────┼─────────────────────────────────┤
│              APPLICATION LAYER                               │
│  ┌────────────────────────┼───────────────────────────────┐ │
│  │  ┌──────────────────┐  │  ┌──────────────────┐        │ │
│  │  │   Commands       │  │  │    Queries       │        │ │
│  │  │  (CQRS Input)    │  │  │  (CQRS Output)   │        │ │
│  │  └──────────────────┘  │  └──────────────────┘        │ │
│  │  ┌──────────────────────────────────────────┐         │ │
│  │  │   Use Case / Application Services        │         │ │
│  │  │  Orchestrates domain objects, maps DTOs  │         │ │
│  │  └──────────────────────────────────────────┘         │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                     DOMAIN LAYER                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │  Entities    │  │ Value Objects│  │Aggregates  │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │  Repositories│  │Domain Events │  │  Domain    │ │  │
│  │  │  (Interfaces)│  │  & Handlers  │  │ Services   │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  │  ┌──────────────┐  ┌──────────────┐                  │  │
│  │  │  Specifications│  │  Exceptions │                  │  │
│  │  └──────────────┘  └──────────────┘                  │  │
│  └───────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE LAYER                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │  SQLAlchemy  │  │    Redis     │  │   Event    │ │  │
│  │  │  Repositories│  │   Cache/Queue│  │   Bus      │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │   Email      │  │  File Store  │  │  External  │ │  │
│  │  │   Service    │  │  (S3/Azure)  │  │   APIs     │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  │  ┌──────────────┐  ┌──────────────┐                  │  │
│  │  │   Auth      │  │   Logging    │                   │  │
│  │  │   Providers │  │   (OpenTelemetry)│                │  │
│  │  └──────────────┘  └──────────────┘                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 20. Folder Structure

```
eduroutine/
├── backend/
│   ├── src/
│   │   ├── api/                          # PRESENTATION LAYER
│   │   │   ├── __init__.py
│   │   │   ├── dependencies/             # FastAPI dependency injection
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py               # Current user, RBAC deps
│   │   │   │   ├── database.py           # DB session dependency
│   │   │   │   └── pagination.py         # Pagination deps
│   │   │   ├── middleware/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── correlation_id.py
│   │   │   │   ├── request_logging.py
│   │   │   │   └── rate_limiter.py
│   │   │   ├── v1/                       # API version 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── router.py
│   │   │   │   │   ├── schemas.py        # Request/Response DTOs
│   │   │   │   │   └── responses.py
│   │   │   │   ├── users/
│   │   │   │   ├── roles/
│   │   │   │   ├── sessions/
│   │   │   │   ├── batches/
│   │   │   │   ├── courses/
│   │   │   │   ├── students/
│   │   │   │   ├── teachers/
│   │   │   │   ├── rooms/
│   │   │   │   ├── routines/
│   │   │   │   ├── scheduling/
│   │   │   │   └── reports/
│   │   │   └── common/
│   │   │       ├── __init__.py
│   │   │       ├── error_handlers.py
│   │   │       ├── response_models.py
│   │   │       └── pagination.py
│   │   │
│   │   ├── application/                  # APPLICATION LAYER
│   │   │   ├── __init__.py
│   │   │   ├── common/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── interfaces/           # Ports
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── unit_of_work.py
│   │   │   │   │   ├── event_bus.py
│   │   │   │   │   └── cache_service.py
│   │   │   │   ├── dto/                  # Data Transfer Objects
│   │   │   │   ├── exceptions/
│   │   │   │   └── pagination.py
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── commands/             # CQRS Commands
│   │   │   │   ├── queries/              # CQRS Queries
│   │   │   │   └── services/
│   │   │   ├── users/
│   │   │   ├── academic/
│   │   │   ├── people/
│   │   │   ├── resources/
│   │   │   ├── timetable/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── commands/
│   │   │   │   ├── queries/
│   │   │   │   └── services/
│   │   │   ├── scheduling/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── commands/
│   │   │   │   ├── queries/
│   │   │   │   └── engine/
│   │   │   └── reports/
│   │   │
│   │   ├── domain/                       # DOMAIN LAYER
│   │   │   ├── __init__.py
│   │   │   ├── common/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_entity.py
│   │   │   │   ├── base_value_object.py
│   │   │   │   ├── domain_event.py
│   │   │   │   └── repository.py         # Generic repository interface
│   │   │   ├── identity/                 # Bounded Context
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities/
│   │   │   │   ├── value_objects/
│   │   │   │   ├── aggregates/
│   │   │   │   ├── events/
│   │   │   │   ├── repositories/
│   │   │   │   ├── services/
│   │   │   │   └── exceptions/
│   │   │   ├── academic/
│   │   │   ├── people/
│   │   │   ├── resources/
│   │   │   ├── timetable/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── entities/
│   │   │   │   ├── value_objects/
│   │   │   │   ├── aggregates/
│   │   │   │   ├── events/
│   │   │   │   ├── repositories/
│   │   │   │   ├── services/
│   │   │   │   └── exceptions/
│   │   │   └── scheduling/
│   │   │       ├── __init__.py
│   │   │       ├── entities/
│   │   │       ├── value_objects/
│   │   │       ├── services/
│   │   │       │   ├── conflict_detector.py
│   │   │       │   ├── constraint_engine.py
│   │   │       │   ├── resource_allocator.py
│   │   │       │   ├── graph_coloring.py
│   │   │       │   ├── backtracking.py
│   │   │       │   └── optimization_engine.py
│   │   │       └── exceptions/
│   │   │
│   │   ├── infrastructure/               # INFRASTRUCTURE LAYER
│   │   │   ├── __init__.py
│   │   │   ├── persistence/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/               # SQLAlchemy ORM models
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base.py
│   │   │   │   │   ├── user.py
│   │   │   │   │   ├── role.py
│   │   │   │   │   ├── academic.py
│   │   │   │   │   ├── people.py
│   │   │   │   │   ├── resource.py
│   │   │   │   │   ├── routine.py
│   │   │   │   │   └── audit.py
│   │   │   │   ├── repositories/         # SQLAlchemy implementations
│   │   │   │   ├── migrations/           # Alembic migrations
│   │   │   │   ├── unit_of_work.py
│   │   │   │   └── config.py
│   │   │   ├── cache/
│   │   │   │   ├── __init__.py
│   │   │   │   └── redis_cache.py
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── jwt_service.py
│   │   │   │   ├── oauth2_service.py
│   │   │   │   └── password_hasher.py
│   │   │   ├── messaging/
│   │   │   │   ├── __init__.py
│   │   │   │   └── event_bus.py
│   │   │   ├── logging/
│   │   │   │   ├── __init__.py
│   │   │   │   └── open_telemetry.py
│   │   │   └── external/
│   │   │       ├── __init__.py
│   │   │       ├── email_service.py
│   │   │       └── file_storage.py
│   │   │
│   │   ├── config/                       # Application configuration
│   │   │   ├── __init__.py
│   │   │   ├── settings.py               # Pydantic Settings
│   │   │   └── container.py              # DI container setup
│   │   │
│   │   └── main.py                       # FastAPI application entry
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── e2e/
│   │   └── conftest.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/                  # Next.js App Router
│   │   ├── components/           # ShadCN UI components
│   │   ├── lib/                  # Utilities, API client
│   │   ├── hooks/                # Custom React hooks
│   │   ├── stores/               # Zustand stores
│   │   ├── queries/              # TanStack Query definitions
│   │   ├── types/                # TypeScript types
│   │   └── middleware.ts         # Next.js middleware for auth
│   ├── Dockerfile
│   └── package.json
│
├── docker/
│   ├── dev/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── nginx.conf
│   └── prod/
│
├── scripts/
│   ├── seed_data.py
│   └── migration_helper.sh
│
├── docs/
│   └── ... (architecture documentation)
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── docker-compose.yml            # Root orchestrator
├── Makefile
├── pyproject.toml
└── README.md
```

---

## 21. Layer Responsibilities

### Presentation Layer (`api/`)
- HTTP request/response handling
- Input validation (Pydantic models)
- Authentication middleware (JWT validation)
- Authorization middleware (RBAC policy enforcement)
- Rate limiting, CORS, request logging
- OpenAPI schema generation (automatic via FastAPI)
- Versioned routers (`/api/v1/`)

### Application Layer (`application/`)
- **Commands**: Receive DTOs → validate → dispatch to domain → persist
- **Queries**: Receive filter/sort/paginate → assemble read model → return DTOs
- **Use Case Services**: Orchestrate domain objects, manage transactions
- **DTOs**: Data Transfer Objects — no behavior, no domain logic
- **Port Interfaces**: Define contracts for infrastructure (repositories, event bus, cache)

### Domain Layer (`domain/`)
- **Entities**: Rich domain objects with identity and behavior
- **Value Objects**: Immutable, self-validating data containers
- **Aggregates**: Transactional consistency boundaries
- **Domain Events**: Something meaningful that happened
- **Domain Services**: Stateless operations that don't fit on entities
- **Repository Interfaces**: Collection-like abstraction for persistence
- **Specifications**: Encapsulated query predicates

### Infrastructure Layer (`infrastructure/`)
- **Persistence**: SQLAlchemy ORM models, repository implementations, Alembic migrations
- **Cache**: Redis client implementation
- **Auth**: JWT creation/validation, OAuth2 provider integrations
- **Messaging**: Event bus (RabbitMQ / Redis Pub-Sub)
- **Logging**: OpenTelemetry collectors
- **External**: Email, file storage, SMS integrations

---

## 22. Dependency Flow

### The Dependency Rule
> Source code dependencies can only point inward. Nothing in an inner circle can know about something in an outer circle.

```
OUTER                                    INNER
[API] → [Application] → [Domain] ← [Infrastructure]
  │           │              │              │
  │           │              │              │
  └───────────┴──────┬──────┴──────────────┘
                     │
            Dependency Injection
            (FastAPI Depends / Container)
```

### Concrete Dependency Injection Flow
```
FastAPI Router
    ↓ Depends()
ApplicationService / CommandHandler
    ↓ Constructor Injection
Domain Repository Interface (port)
    ↑
SQLAlchemy Repository (adapter)   ← Infrastructure implements port
    ↓
Database Session
```

### Rules
1. **API layer** depends on **Application layer** (calls use cases) and **Domain layer** (uses DTOs)
2. **Application layer** depends on **Domain layer** (uses entities, interfaces) — NEVER on Infrastructure
3. **Domain layer** has ZERO dependencies on any other layer — pure Python with dataclasses
4. **Infrastructure layer** depends on **Domain layer** (implements interfaces) — NEVER on Application or API
5. All cross-layer communication uses **interfaces defined in the Domain layer** (Ports & Adapters)
