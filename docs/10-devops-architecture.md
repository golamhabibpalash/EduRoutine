# Phase 10: DevOps & Deployment Architecture

---

## 45. Docker Architecture

### Container Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                      DOCKER COMPOSE                              │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │  Traefik  │  │  FastAPI │  │  Next.js │  │   PostgreSQL   │  │
│  │  (Proxy)  │  │  Backend │  │  Frontend│  │   (Primary)    │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
│       │              │              │               │           │
│       │              │              │               │           │
│       │         ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│       │         │  Redis   │  │  Celery  │  │  PostgreSQL    │  │
│       │         │  Cache   │  │  Worker  │  │  (Replica)     │  │
│       │         └──────────┘  └──────────┘  └────────────────┘  │
│       │                         │                                │
│       │                    ┌──────────┐                          │
│       │                    │  Flower  │                          │
│       │                    │  (Monitor)│                          │
│       │                    └──────────┘                          │
│       │                                                         │
│  ┌────┴────┐  ┌─────────────────────────────────────────────┐   │
│  │  MinIO  │  │  Prometheus + Grafana + Loki + Tempo       │   │
│  │ (S3)    │  │  (Observability Stack)                     │   │
│  └─────────┘  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Dockerfile Strategy

#### Backend Dockerfile (Multi-stage)
```
Stage 1: Builder
  - Base: python:3.13-slim
  - Install build dependencies
  - Copy requirements.txt
  - pip install packages
  - Copy source code
  - Run tests

Stage 2: Production
  - Base: python:3.13-slim
  - Copy installed packages from builder
  - Copy application code
  - Copy alembic migrations
  - USER: non-root (appuser)
  - HEALTHCHECK: /health endpoint
  - CMD: uvicorn with gunicorn workers
```

#### Frontend Dockerfile
```
Stage 1: Builder
  - Base: node:20-alpine
  - npm ci (exact dependency resolution)
  - npm run build

Stage 2: Production
  - Base: nginx:alpine
  - Copy built static files
  - Custom nginx.conf with compression, caching headers, HSTS
  - HEALTHCHECK
```

### Docker Compose Profiles
| Profile | Services | Purpose |
|---|---|---|
| `dev` | Backend, Frontend, PostgreSQL, Redis | Development |
| `test` | Backend, PostgreSQL (temp), Redis (temp) | CI testing |
| `staging` | All services | Pre-production validation |
| `prod` | All services + replicas | Production deployment |
| `observability` | Prometheus, Grafana, Loki, Tempo | Monitoring |

---

## 46. Deployment Architecture

### Environment Strategy
```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│ Development│────→│  Staging   │────→│Production 1 │     │Production 2 │
│            │     │            │     │ (Active)   │────→│ (Standby)   │
│ • Local    │     │ • Dev      │     │ • Live     │     │ • DR        │
│ • Docker   │     │ • Pre-prod │     │ • 99.9%    │     │ • 0% traffic│
│ • Auto-deploy│   │ • UAT      │     │            │     │             │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
```

### Deployment Topology (Production)
```
                      ┌─────────────────┐
                      │   Cloudflare    │
                      │  (DNS + DDoS)   │
                      └────────┬────────┘
                               │
                      ┌────────┴────────┐
                      │   AWS ALB /     │
                      │   Load Balancer │
                      └────────┬────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
   │  ECS Service  │    │  ECS Service  │    │  ECS Service  │
   │  FastAPI v1   │    │  FastAPI v1   │    │  FastAPI v1   │
   │  (3 replicas) │    │  (3 replicas) │    │  (3 replicas) │
   └───────┬───────┘    └───────┬───────┘    └───────┬───────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │      Redis Cluster     │
                    │   (Cache + Sessions)   │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │    PostgreSQL RDS      │
                    │  (Primary + Read Replica)│
                    └───────────────────────┘
```

### Infrastructure as Code
- **Terraform** for cloud resource provisioning (AWS/Azure/GCP)
- **Ansible** for configuration management
- **Helm charts** for Kubernetes deployment (future)
- **Secrets**: AWS Secrets Manager / HashiCorp Vault

---

## 47. CI/CD Design

### CI Pipeline (GitHub Actions)

```
┌─────────────────────────────────────────────────────────────────┐
│                      CI PIPELINE                                 │
│                                                                  │
│  Trigger: Push to feature/*, develop, main                      │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐ │
│  │  Lint    │  │  Type    │  │  Unit    │  │  Security      │ │
│  │  (ruff)  │  │  Check   │  │  Tests   │  │  Scan (Bandit) │ │
│  └──────────┘  │  (mypy)  │  └──────────┘  └────────────────┘ │
│                └──────────┘                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐ │
│  │  Build   │  │  Integration│  │  E2E    │  │  Docker Build │ │
│  │  (Backend)│  │  Tests    │  │  Tests  │  │  & Push       │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘ │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Artifacts: Docker images → ECR / Docker Hub             │   │
│  │  Reports: Coverage, lint, security scan → PR comments    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### CD Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                      CD PIPELINE                                 │
│                                                                  │
│  Trigger: Merge to main (or manual approval)                    │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │  Deploy    │  │  Smoke     │  │  Integration│  │  Health  │ │
│  │  to Staging│  │  Tests     │  │  Tests      │  │  Check   │ │
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘ │
│         │              │              │              │          │
│         └──────────────┴──────┬───────┴──────┬───────┘          │
│                               │              │                  │
│                               ▼              ▼                  │
│                    ┌────────────────┐  ┌──────────────────┐     │
│                    │  Manual Gate   │  │  Deploy to Prod  │     │
│                    │  (Approval)    │──→  (Blue/Green)    │     │
│                    └────────────────┘  └──────────────────┘     │
│                                               │                  │
│                                               ▼                  │
│                                    ┌──────────────────────┐     │
│                                    │  Production Health   │     │
│                                    │  Monitor (15 min)    │     │
│                                    └──────────────────────┘     │
│                                               │                  │
│                                    ┌──────────┴──────────┐      │
│                                    │  Rollback if failed │      │
│                                    └─────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### CI/CD Configuration
| Stage | Tools | Timing |
|---|---|---|
| Code Linting | Ruff | On push |
| Type Checking | mypy | On push |
| Unit Tests | pytest + coverage | On push |
| Security Scan | Bandit, Safety | On push |
| Integration Tests | pytest + Docker | On PR |
| E2E Tests | Playwright | On merge to main |
| Build & Push | Docker Buildx | On merge to main |
| Deploy Staging | AWS ECS / k8s | On merge to main |
| Deploy Production | Blue/Green via AWS ECS | Manual approval |

---

## 48. Monitoring Design

### Monitoring Stack
```
┌─────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY STACK                           │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │   Prometheus    │  │    Loki        │  │    Tempo          │  │
│  │   (Metrics)     │  │    (Logs)      │  │    (Traces)       │  │
│  └───────┬────────┘  └───────┬────────┘  └────────┬─────────┘  │
│          │                   │                     │             │
│          └───────────────────┼─────────────────────┘             │
│                              │                                   │
│                      ┌───────┴────────┐                          │
│                      │    Grafana      │                          │
│                      │   (Dashboards)  │                          │
│                      └────────────────┘                          │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │   Alertmanager  │  │    Sentry      │  │   PagerDuty      │  │
│  │   (Alerts)      │  │    (Errors)    │  │   (On-call)      │  │
│  └────────────────┘  └────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Metrics (Prometheus)

#### API Metrics
| Metric | Type | Labels | Description |
|---|---|---|---|
| `http_requests_total` | Counter | method, endpoint, status | Total request count |
| `http_request_duration_seconds` | Histogram | method, endpoint | Request latency |
| `http_requests_in_flight` | Gauge | method | Current concurrent requests |

#### Business Metrics
| Metric | Type | Description |
|---|---|---|
| `routines_total` | Gauge | Total routines in system |
| `routine_generations_total` | Counter | Number of auto-generations |
| `scheduling_conflicts_total` | Counter | Conflicts detected |
| `active_users_total` | Gauge | Currently active users |
| `scheduling_generation_duration_seconds` | Histogram | Generation time |

#### System Metrics
| Metric | Description |
|---|---|
| `cpu_usage_percent` | CPU utilization per container |
| `memory_usage_bytes` | Memory utilization |
| `db_connection_pool_usage` | Database connection pool |
| `redis_hit_ratio` | Cache hit ratio |
| `celery_queue_depth` | Background task queue depth |

### Alerts (Alertmanager Rules)
| Alert Name | Condition | Severity | Response Time |
|---|---|---|---|
| HighErrorRate | Error rate > 5% for 5 min | Critical | 5 min |
| HighLatency | p99 latency > 1s for 5 min | Warning | 15 min |
| LowCacheHitRatio | Cache hit < 80% for 10 min | Warning | 30 min |
| HighCPUUsage | CPU > 85% for 10 min | Warning | 15 min |
| DiskSpace | Disk usage > 85% | Critical | 10 min |
| DBCXHAUSTED | DB connections > 80% pool | Critical | 5 min |
| OAuthFailure | OAuth login failure spike | Warning | 15 min |

### Health Check Endpoints
| Endpoint | Purpose | Expected Response |
|---|---|---|
| `/health` | Liveness check | `{"status": "healthy"}` |
| `/health/ready` | Readiness check | `{"status": "ready", "db": "ok", "redis": "ok"}` |
| `/health/db` | Database check | `{"status": "ok", "latency_ms": 2}` |
| `/health/cache` | Redis check | `{"status": "ok", "latency_ms": 1}` |
| `/metrics` | Prometheus metrics | Prometheus text format |

---

## 49. Logging Design

### Logging Strategy
- **Structured logging**: JSON-formatted logs
- **Centralized**: All logs shipped to Loki / Elasticsearch
- **Correlation**: Every log entry includes `request_id` and `correlation_id`
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Log Format
```json
{
  "timestamp": "2026-06-18T10:00:00.123Z",
  "level": "INFO",
  "logger": "eduroutine.api.v1.routines",
  "message": "Routine published successfully",
  "request_id": "req-abc-123",
  "correlation_id": "corr-xyz-789",
  "user_id": "user-uuid",
  "resource_type": "Routine",
  "resource_id": "routine-uuid",
  "duration_ms": 245,
  "extra": {
    "status": "published",
    "version": 3
  }
}
```

### Log Categories
| Category | Level | Contents | Retention |
|---|---|---|---|
| `api.access` | INFO | All HTTP requests | 30 days |
| `api.error` | ERROR | 5xx responses | 90 days |
| `auth.login` | INFO | Login attempts (success/failure) | 1 year |
| `auth.security` | WARN | Suspicious auth activity | 1 year |
| `domain.event` | INFO | Domain event dispatches | 30 days |
| `scheduling.engine` | INFO | Generation progress | 30 days |
| `db.query` | DEBUG (dev) / INFO (prod) | Slow queries (>100ms) | 7 days |
| `background.task` | INFO | Celery task lifecycle | 30 days |

### Logging Best Practices
1. **No PII in logs**: Mask emails, phone numbers, IP addresses
2. **No secrets**: Never log passwords, tokens, API keys
3. **Structured context**: Use log context objects, not string interpolation
4. **Sampling**: High-volume debug logs sampled (1:100)
5. **Error aggregation**: Sentry for exception tracking with full stack traces
6. **Audit logs**: Separate persistent storage (not shipped to Loki)

### OpenTelemetry Integration
```python
# Instrumentation approach
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

# Auto-instrument all supported libraries
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument()
RedisInstrumentor().instrument()
```

### Logging Architecture
```
Application → Console (JSON) → Filebeat / Fluentd → Loki → Grafana
                                      │
                                      ↓
                                 S3 Archive (30+ days retention)
```
