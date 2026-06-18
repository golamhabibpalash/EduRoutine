# Phase 11: Coding & Standards

---

## 50. Coding Standards

### Python Coding Standards

#### General Guidelines
- **Python Version**: 3.13+ (use latest stable features)
- **Style**: PEP 8 enforced via `ruff`
- **Formatting**: `ruff format` (line length = 100)
- **Type Hints**: Required for all function signatures (enforced via `mypy --strict`)
- **Docstrings**: Google-style for all public modules, classes, and functions
- **Imports**: Organized by `ruff` (standard lib → third-party → internal)

#### Code Quality Tools
| Tool | Purpose | Configuration |
|---|---|---|
| `ruff` | Linting + formatting | `pyproject.toml` |
| `mypy` | Static type checking | `--strict` mode |
| `pytest` | Testing framework | `tests/` directory |
| `coverage` | Code coverage | Target: > 85% |
| `bandit` | Security scanning | All severities |
| `safety` | Dependency vulnerabilities | CI check |
| `pre-commit` | Pre-commit hooks | ruff, mypy, bandit |

### TypeScript Coding Standards

#### General Guidelines
- **TypeScript Version**: 5.x (strict mode)
- **Style**: ESLint + Prettier (line length = 100)
- **Formatting**: Prettier enforced in CI
- **Strictness**: `strict: true` in `tsconfig.json`
- **No `any`**: Use `unknown` if type is truly uncertain
- **No `@ts-ignore`**: Use `@ts-expect-error` with justification

#### Code Quality Tools
| Tool | Purpose |
|---|---|
| `ESLint` | Linting |
| `Prettier` | Formatting |
| `TypeScript` | Type checking |
| `Vitest` | Unit testing |
| `Playwright` | E2E testing |

---

## 51. Naming Standards

### Python Naming
| Element | Convention | Example |
|---|---|---|
| Packages | snake_case | `scheduling_engine` |
| Modules | snake_case | `conflict_detector.py` |
| Classes | PascalCase | `ConflictDetector`, `CreateRoutineCommand` |
| Functions/Methods | snake_case | `detect_conflicts()` |
| Variables | snake_case | `routine_details` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private | _prefix | `_validate_constraints()` |
| Protected | single _ | `_internal_method()` |
| Magic | __dunder__ | `__init__`, `__repr__` |
| Type Variables | PascalCase | `T`, `RoutineT` |
| Interfaces (Protocols) | PascalCase + Protocol | `RoutineRepositoryProtocol` |

### TypeScript Naming
| Element | Convention | Example |
|---|---|---|
| Components | PascalCase | `RoutineCalendar` |
| Hooks | camelCase + use | `useRoutineQuery` |
| Functions | camelCase | `fetchRoutineById` |
| Variables | camelCase | `routineDetails` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| Types/Interfaces | PascalCase | `RoutineResponse` |
| Enums | PascalCase | `RoutineStatus` |
| Enum Members | PascalCase | `RoutineStatus.Published` |
| Files (components) | PascalCase | `RoutineCalendar.tsx` |
| Files (utilities) | camelCase | `dateUtils.ts` |
| CSS Classes | kebab-case | `routine-calendar__header` |

### Database Naming
| Element | Convention | Example |
|---|---|---|
| Schemas | snake_case | `timetable`, `identity` |
| Tables | snake_case, plural | `routine_details`, `time_slots` |
| Columns | snake_case | `day_of_week`, `period_number` |
| Primary Keys | `id` | `id` |
| Foreign Keys | `{table}_id` | `routine_id`, `course_id` |
| Indexes | `idx_{table}_{column}` | `idx_routines_batch_id` |
| Unique Constraints | `uq_{table}_{columns}` | `uq_routine_detail_slot` |
| Foreign Keys | `fk_{child}_{parent}` | `fk_routine_details_routine` |

---

## 52. API Standards

### URL Standards
| Convention | Example |
|---|---|
| Lowercase | `/api/v1/users` |
| Plural nouns | `/api/v1/courses` |
| Hyphens for multi-word | `/api/v1/time-slots` |
| No file extensions | `/api/v1/routines`, NOT `/api/v1/routines.json` |
| Query params for filtering | `?status=active&department_id=uuid` |
| No verbs in URL | `/api/v1/routines/{id}/publish` (approves) |

### Request/Response Standards
- **Content-Type**: `application/json` (default)
- **Accept header**: Used for version negotiation (future)
- **Idempotency key**: Optional `Idempotency-Key` header for POST/PUT
- **Pagination**: Page-based (`page`, `page_size`) or cursor-based
- **Sorting**: `sort_by=field_name&sort_order=asc|desc`
- **Filtering**: `filter=field:operator:value` (e.g., `status:eq:active`)

### Error Response Standards
```json
{
  "status": "error",
  "error": {
    "code": "STRING_CODE",
    "message": "Human-readable summary",
    "details": [
      {"field": "email", "message": "Email already registered", "code": "DUPLICATE"}
    ],
    "request_id": "uuid"
  }
}
```

---

## 53. Database Standards

### Schema Design Standards
- Every table has a UUID primary key (`id`)
- Every table has `created_at` and `updated_at` timestamps
- Soft delete via `deleted_at` TIMESTAMPTZ (nullable) where applicable
- All foreign keys are indexed
- All foreign keys have explicit names
- Use `TIMESTAMPTZ` (not `TIMESTAMP`) for all time values
- Use `UUID` (not auto-increment) for public-facing IDs
- Use `BIGSERIAL` only for internal, append-only tables (audit logs)

### Naming Standards
```sql
-- Table: routine_details
-- Schema: timetable
CREATE TABLE timetable.routine_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    routine_id UUID NOT NULL,
    day_of_week SMALLINT NOT NULL,
    period_number SMALLINT NOT NULL,
    course_id UUID NOT NULL,
    teacher_id UUID NOT NULL,
    room_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_routine_details_routine
        FOREIGN KEY (routine_id) REFERENCES timetable.routines(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_routine_details_course
        FOREIGN KEY (course_id) REFERENCES academic.courses(id),
    CONSTRAINT fk_routine_details_teacher
        FOREIGN KEY (teacher_id) REFERENCES people.teachers(id),
    CONSTRAINT fk_routine_details_room
        FOREIGN KEY (room_id) REFERENCES resources.rooms(id),

    CONSTRAINT uq_routine_detail_slot
        UNIQUE (routine_id, day_of_week, period_number, room_id),

    CONSTRAINT ck_day_of_week CHECK (day_of_week BETWEEN 0 AND 6),
    CONSTRAINT ck_period_number CHECK (period_number > 0)
);

CREATE INDEX idx_routine_details_routine ON timetable.routine_details(routine_id);
CREATE INDEX idx_routine_details_teacher ON timetable.routine_details(teacher_id);
CREATE INDEX idx_routine_details_room ON timetable.routine_details(room_id);
```

### Migration Standards
- Every migration is reversible (`upgrade()` + `downgrade()`)
- Migrations are numbered sequentially (Alembic auto-generates)
- Data migrations are separate from schema migrations
- No direct SQL modifications in production — always via Alembic
- Migration review required in PR

### Query Standards
- Use parameterized queries (SQLAlchemy ORM or `text()` with bind params)
- Avoid N+1 queries — use eager loading (`selectinload`, `joinedload`)
- Use `EXPLAIN ANALYZE` to review complex queries
- Paginate all list endpoints (default: 20, max: 100)
- Read replicas for reporting queries

---

## 54. Security Standards

### Authentication Standards
- Passwords: Minimum 8 characters, hashed with bcrypt (cost factor 12)
- JWT: RS256 signed, 15-minute access token expiry
- Refresh Tokens: 7-day expiry, rotation on use, stored as SHA-256 hash
- Failed login: Lockout after 5 attempts (15-minute cooldown)
- MFA: TOTP (RFC 6238) optional, enforced for admin roles
- Session: Server-side session tracking, revocable

### Authorization Standards
- All endpoints require authentication unless explicitly public (login, register)
- RBAC enforced at middleware level
- Claim-based authorization for granular operations
- Resource-based checks for data ownership
- Default-deny: if no rule explicitly allows, deny

### Data Protection Standards
- **At Rest**: AES-256 encryption for sensitive fields (MFA secrets, OAuth tokens)
- **In Transit**: TLS 1.3 minimum
- **Secrets**: Environment variables or secret manager, never in code
- **PII**: Minimize collection, mask in logs, encrypt in database
- **Backup**: Encrypted backups with separate key management

### API Security Standards
| Standard | Implementation |
|---|---|
| Rate Limiting | 100 req/min per user, 1000 req/min per IP |
| CORS | Whitelist specific origins per environment |
| CSP | Content-Security-Policy header |
| HSTS | Strict-Transport-Security header (max-age=31536000) |
| XSS Protection | X-Content-Type-Options: nosniff |
| CSRF | Anti-forgery tokens for cookie-based auth |
| SQL Injection | Parameterized queries (ORM prevents) |
| Request Size | Max 10MB request body |
| Timeout | 30-second request timeout |

### Dependency Security Standards
- Lock files committed (`requirements.lock`, `package-lock.json`)
- Regular `npm audit` / `safety check` in CI
- Dependabot/Renovate for automated dependency updates
- Monthly full dependency review
- No deprecated or unmaintained packages

### Incident Response Standards
| Severity | Response Time | Escalation |
|---|---|---|
| Critical (data breach, auth bypass) | 15 minutes | CTO, Security Lead |
| High (service degradation) | 30 minutes | Engineering Lead |
| Medium (non-critical feature down) | 2 hours | Team Lead |
| Low (cosmetic issue) | Next business day | Dev team |

### Security Review Checklist (Pre-Deployment)
- [ ] Authentication tested with invalid/malformed tokens
- [ ] Authorization tested for all roles (including anonymous)
- [ ] Rate limiting verified on auth endpoints
- [ ] SQL injection attempt on all input fields
- [ ] XSS attempt on all string inputs
- [ ] CORS configuration verified per environment
- [ ] Secrets confirmed absent from code and logs
- [ ] Dependency vulnerabilities checked
- [ ] All default credentials changed
- [ ] TLS verified on all endpoints
