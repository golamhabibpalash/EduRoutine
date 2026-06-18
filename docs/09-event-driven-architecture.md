# Phase 9: Event-Driven Architecture

---

## 41. Event-Driven Architecture

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    EVENT-DRIVEN ARCHITECTURE                     │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    EVENT BUS                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │           Message Broker (Redis Pub/Sub → RabbitMQ) │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│            ▲                    ▲                      ▲        │
│            │                    │                      │        │
│  ┌─────────┴──┐      ┌─────────┴──┐       ┌──────────┴───┐    │
│  │  Publisher  │      │  Publisher  │       │  Publisher   │    │
│  │  (Identity) │      │ (Scheduler) │       │  (People)    │    │
│  └─────────────┘      └────────────┘       └──────────────┘    │
│            │                    │                      │        │
│            ▼                    ▼                      ▼        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    EVENT HANDLERS                          │  │
│  │                                                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │   Audit      │  │  Reporting   │  │ Notification │    │  │
│  │  │   Handler    │  │  Handler     │  │  Handler     │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │  Integration │  │   Cache      │  │   Analytics  │    │  │
│  │  │  Handler     │  │  Invalidation│  │   Handler    │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Event Categories
| Category | Routing | Delivery Guarantee | Example |
|---|---|---|---|
| Domain Events | In-process bus + Outbox | At-least-once | `RoutinePublished` |
| Integration Events | Message broker | At-least-once | `ScheduleGenerated` |
| Audit Events | Direct persistence | Exactly-once | `EntityUpdated` |
| Notification Events | Message broker | Best-effort | `ScheduleChanged` |

### Event Bus Implementation Strategy
- **Phase 1**: In-process event bus with outbox pattern (simpler, no external broker dependency)
- **Phase 2**: Redis Pub/Sub for lightweight cross-process events
- **Phase 3**: RabbitMQ / Apache Kafka for high-throughput, durable messaging (microservice migration)

### Event Schema (CloudEvents Standard)
```json
{
  "specversion": "1.0",
  "id": "uuid-event-id",
  "source": "/eduroutine/identity",
  "type": "com.eduroutine.identity.user.registered",
  "subject": "user-uuid",
  "datacontenttype": "application/json",
  "time": "2026-06-18T10:00:00Z",
  "data": {
    "user_id": "uuid",
    "email": "user@institution.edu",
    "display_name": "John Doe",
    "roles": ["student"]
  }
}
```

---

## 42. CQRS Design

### Command-Query Separation

```
                    ┌──────────────────────────────┐
                    │         CLIENT                │
                    └──────────┬───────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
    ┌───────────────────┐         ┌───────────────────┐
    │     COMMAND       │         │       QUERY        │
    │      SIDE         │         │       SIDE         │
    │                   │         │                   │
    │  ┌─────────────┐  │         │  ┌─────────────┐  │
    │  │  Command    │  │         │  │   Query     │  │
    │  │  Handler    │  │         │  │   Handler   │  │
    │  └──────┬──────┘  │         │  └──────┬──────┘  │
    │         │         │         │         │         │
    │         ▼         │         │         ▼         │
    │  ┌─────────────┐  │         │  ┌─────────────┐  │
    │  │  Validate   │  │         │  │  Read       │  │
    │  │  (Business) │  │         │  │  Model      │  │
    │  └──────┬──────┘  │         │  └──────┬──────┘  │
    │         │         │         │         │         │
    │         ▼         │         │         ▼         │
    │  ┌─────────────┐  │         │  ┌─────────────┐  │
    │  │  Domain     │  │         │  │  Optimized  │  │
    │  │  Logic      │  │         │  │  Query (DB) │  │
    │  └──────┬──────┘  │         │  └─────────────┘  │
    │         │         │         │                   │
    │         ▼         │         │                   │
    │  ┌─────────────┐  │         │                   │
    │  │  Persist    │  │         │                   │
    │  │  (Domain DB)│  │         │                   │
    │  └─────────────┘  │         │                   │
    └───────────────────┘         └───────────────────┘
```

### CQRS Rules
| Aspect | Command Side | Query Side |
|---|---|---|
| **Purpose** | Write operations (create, update, delete) | Read operations (list, get, search) |
| **Returns** | Entity ID or status | Data (DTOs) |
| **Validation** | Business rules, invariants | Schema validation only |
| **Model** | Domain entities (rich) | Read models (flat, denormalized) |
| **Transaction** | Required (ACID) | Not required (read-only) |
| **Cache** | Invalidate on write | Cache aggressively |
| **Naming** | `CreateRoutineCommand` | `GetRoutineQuery` |
| **Handler** | `CreateRoutineHandler` | `GetRoutineHandler` |

### Command Handler Pattern
```python
# Structure of a command handler
class CreateRoutineHandler(BaseHandler):
    def __init__(
        self,
        routine_repo: RoutineRepository,
        unit_of_work: UnitOfWork,
        event_bus: EventBus,
    ):
        ...

    async def handle(self, command: CreateRoutineCommand) -> RoutineId:
        # 1. Validate business rules
        # 2. Create domain entity / aggregate
        # 3. Apply domain events
        # 4. Persist via Unit of Work
        # 5. Publish events
        # 6. Return new ID
```

### Query Handler Pattern
```python
# Structure of a query handler
class GetRoutineQueryHandler(BaseHandler):
    def __init__(
        self,
        read_model_repo: RoutineReadRepository,
        cache_service: CacheService,
    ):
        ...

    async def handle(self, query: GetRoutineQuery) -> RoutineResponse:
        # 1. Check cache
        # 2. Execute optimized query
        # 3. Map to DTO
        # 4. Return result
```

---

## 43. Event Sourcing Design

### Event Sourcing Architecture (Future Phase)
```
                    ┌────────────────────────────┐
                    │       EVENT STORE            │
                    │  ┌────────────────────────┐ │
                    │  │  Event 1 (UserCreated) │ │
                    │  │  Event 2 (UserLoggedIn)│ │
                    │  │  Event 3 (RoleAssigned)│ │
                    │  │  Event 4 (...)         │ │
                    │  │  Event N (Current)     │ │
                    │  └────────────────────────┘ │
                    │                              │
                    │  • Append-only               │
                    │  • Immutable                 │
                    │  • Ordered by timestamp      │
                    └──────────────────────────────┘
                               │
                               │ Replay
                               ▼
                    ┌────────────────────────────┐
                    │       PROJECTIONS            │
                    │                              │
                    │  ┌──────────────────────┐   │
                    │  │  Current State DB    │   │
                    │  │  (Optimized for read)│   │
                    │  └──────────────────────┘   │
                    │  ┌──────────────────────┐   │
                    │  │  Report DB           │   │
                    │  │  (Analytics data)    │   │
                    │  └──────────────────────┘   │
                    │  ┌──────────────────────┐   │
                    │  │  Search Index        │   │
                    │  │  (Elasticsearch)     │   │
                    │  └──────────────────────┘   │
                    └──────────────────────────────┘
```

### When to Use Event Sourcing
| Use Case | Applicability |
|---|---|
| Routine scheduling history | High — audit, rollback, what-if |
| User identity changes | Medium — audit trail |
| Academic structure changes | Medium — version history |
| Real-time scheduling engine | Low — performance critical |

### Event Store Table (Future)
```sql
CREATE TABLE event_store.events (
    id BIGSERIAL,
    event_id UUID NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(200) NOT NULL,
    event_data JSONB NOT NULL,
    version INTEGER NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (aggregate_type, aggregate_id, version),
    UNIQUE (event_id)
);
```

---

## 44. Audit Trail Design

### Audit Philosophy
- **Every state change is recorded** — immutable, append-only
- **Who did what, when, and what changed**
- **Non-repudiation** — actors cannot deny their actions
- **Compliance-ready** — GDPR, SOX, institutional policies

### Audit Data Model
```yaml
AuditEntry:
  id: UUID (or BIGSERIAL)
  event_id: UUID  # Correlates related changes
  timestamp: TIMESTAMPTZ  # When the change occurred
  actor_id: UUID  # Who performed the action
  actor_type: str  # "user", "system", "api_key"
  actor_ip: str
  user_agent: str
  action: str  # "CREATE", "UPDATE", "DELETE", "PUBLISH", "LOGIN"
  entity_type: str  # "Routine", "Course", "User", etc.
  entity_id: UUID  # The affected entity
  changes: List[ChangeRecord]  # Before and after values
  correlation_id: UUID  # Links to request/event chain
  context: dict  # Additional metadata
```

### Change Record Format
```json
{
  "field": "status",
  "old_value": "draft",
  "new_value": "published"
}
```

### Audit Logging Implementation
```python
# Pseudo-code: Audit decorator for domain event handlers
class AuditLogger:
    async def log(
        self,
        action: str,
        entity_type: str,
        entity_id: UUID,
        old_values: dict | None,
        new_values: dict | None,
        actor_id: UUID,
        correlation_id: UUID,
    ):
        entry = AuditEntry(
            event_id=uuid4(),
            timestamp=now(),
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )
        await self.repository.save(entry)
```

### Audit Events vs Domain Events
| Aspect | Domain Event | Audit Event |
|---|---|---|
| Purpose | Business logic trigger | Compliance record |
| Destination | Event bus, handlers | Audit log database |
| Retention | Processed then discarded | Retained indefinitely |
| Schema | Business semantics | Generic change record |
| Immutability | Not guaranteed | Immutable |
| Partial Updates | Possible | Full state snapshots |

### Audit Retention Policy
| Environment | Retention | Action After Retention |
|---|---|---|
| Production | 7 years | Archive to cold storage |
| Staging | 90 days | Auto-delete |
| Development | 30 days | Auto-delete |

### Correlation ID Flow
```
Client Request (X-Request-ID: abc-123)
  → API Gateway
    → Command Handler (correlation_id = abc-123)
      → Domain Event (correlation_id = abc-123)
        → Audit Log (correlation_id = abc-123)
        → Event Bus (correlation_id = abc-123)
```

This enables full traceability from HTTP request through domain logic to audit trail.
