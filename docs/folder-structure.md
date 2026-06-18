# Project Folder Structure

**Generated:** 2026-06-18

```
EduRoutine/
│
├── backend/
│   ├── src/
│   │   ├── domain/              # Domain layer — entities, value objects, aggregates, events, repository interfaces
│   │   │   ├── identity/        # User, Role, Permission, Auth
│   │   │   ├── academic/        # Session, Batch, Semester, Course, Section
│   │   │   ├── people/          # Student, Teacher, Enrollment
│   │   │   ├── resources/       # Room, Lab, Equipment
│   │   │   ├── timetable/       # Routine, RoutineDetail, TimeSlot
│   │   │   ├── scheduling/      # Constraint, Conflict, GenerationJob
│   │   │   └── common/          # Base classes, domain events
│   │   ├── application/         # Application layer — CQRS commands/queries, DTOs, use-case services
│   │   │   ├── auth/            # Login, register, OAuth, token refresh
│   │   │   ├── users/           # User CRUD
│   │   │   ├── academic/        # Session, batch, semester, course management
│   │   │   ├── people/          # Student, teacher management
│   │   │   ├── resources/       # Room, lab management
│   │   │   ├── timetable/       # Routine CRUD, publishing
│   │   │   ├── scheduling/      # Auto-generation, validation
│   │   │   ├── reports/         # Schedule views, utilization
│   │   │   └── common/          # Shared DTOs, interfaces, exceptions
│   │   ├── infrastructure/      # Infrastructure layer — adapters for persistence, cache, auth, messaging
│   │   │   ├── persistence/     # SQLAlchemy models, repositories, Alembic migrations
│   │   │   ├── cache/           # Redis implementation
│   │   │   ├── auth/            # JWT, OAuth2 providers, password hashing
│   │   │   ├── messaging/       # Event bus, outbox publisher
│   │   │   ├── logging/         # OpenTelemetry, structured logging
│   │   │   └── external/        # Email, file storage, SMS
│   │   ├── presentation/        # Presentation layer — FastAPI routes, middleware, dependencies
│   │   │   └── api/
│   │   │       ├── v1/          # Versioned API endpoints (13 resource modules)
│   │   │       ├── dependencies/# FastAPI dependency injection (auth, db, pagination)
│   │   │       ├── middleware/   # Correlation ID, request logging, rate limiting
│   │   │       └── common/      # Error handlers, response models
│   │   └── shared/              # Cross-cutting — config, utilities
│   ├── tests/                   # Test suite
│   │   ├── unit/                # Unit tests (domain + application)
│   │   ├── integration/         # Integration tests (DB, cache, API)
│   │   ├── e2e/                 # End-to-end tests
│   │   └── fixtures/            # Test data factories
│   ├── alembic/versions/        # Database migrations
│   ├── requirements/            # Dependency files (dev, prod, test)
│   ├── .env.example
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   ├── features/            # Feature modules (auth, routines, courses, etc.)
│   │   ├── components/          # Shared components
│   │   │   ├── ui/              # ShadCN UI primitives (button, card, dialog, etc.)
│   │   │   ├── layout/          # App shell, sidebar, navbar
│   │   │   └── shared/          # Cross-feature components
│   │   ├── services/            # API client, TanStack Query configuration
│   │   ├── hooks/               # Custom React hooks
│   │   ├── store/               # Zustand state management
│   │   ├── types/               # TypeScript interfaces and types
│   │   └── lib/                 # Utilities, constants, helpers
│   ├── public/                  # Static assets
│   ├── .env.example
│   ├── Dockerfile
│   └── package.json
│
├── docker/                      # Docker infrastructure
│   ├── postgres/                # Custom PostgreSQL config
│   ├── redis/                   # Redis config
│   ├── pgadmin/                 # pgAdmin config
│   └── nginx/                   # Nginx reverse proxy config
│
├── contracts/                   # API contracts
│   ├── openapi/                 # OpenAPI specification
│   ├── dto/                     # Shared DTO definitions
│   └── events/                  # CloudEvent schemas
│
├── docs/                        # Architecture documentation
│   ├── architecture/            # System architecture documents
│   ├── database/                # Database design documents
│   ├── api/                     # API design documents
│   ├── security/                # Security design documents
│   └── scheduling/              # Scheduling engine design
│
├── scripts/                     # Operational scripts
│   ├── setup/                   # Environment setup scripts
│   ├── backup/                  # Database backup scripts
│   └── deployment/              # Deployment automation scripts
│
├── .gitignore
├── AGENTS.md                    # AI collaboration rules
├── README.md
└── docker-compose.yml           # Multi-service orchestrator
```
