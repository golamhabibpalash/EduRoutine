# EduRoutine — API Contract: Standards

> **Phase 8 — API Contract**
> Derived from approved Phase 3 (Database Design), Phase 5 (API Design), Phase 6 (Authentication), Phase 7 (Authorization).
> Status: **Contract — no implementation code.**

This document defines the cross-cutting standards every endpoint in the OpenAPI specification
(`openapi.yaml`) must comply with. Companion deliverables:

| File | Purpose |
|---|---|
| `openapi.yaml` | OpenAPI 3.1 specification (machine-readable contract) |
| `api-endpoint-catalog.md` | Human-readable endpoint index (all modules) |
| `dto-catalog.md` | Request/Response DTO catalog with field-level validation |
| `error-response-catalog.md` | Canonical error codes and payloads |

---

## 0. Module → Data Source Mapping

Three requested modules are **logical projections/specializations** of approved tables, not new
tables. The contract honors them as first-class API resources while staying faithful to the schema.

| Module | Backing table(s) | Notes |
|---|---|---|
| Authentication | `identity.users`, `identity.refresh_tokens`, `identity.external_logins` | Token issuance/rotation |
| Users | `identity.users` | + `user_roles`, `user_claims` joins |
| Roles | `identity.roles`, `identity.role_permissions`, `identity.permissions` | RBAC |
| Claims | `identity.user_claims` | Claim-based auth |
| Students | `people.students` | |
| Teachers | `people.teachers`, `people.teacher_course_specializations` | |
| Courses | `academic.courses` | |
| Sessions | `academic.sessions` | Academic year/session |
| Batches | `academic.batches` | |
| Semesters | `academic.semesters` | |
| Sections | `academic.sections` | |
| **Classes** | *projection of* `timetable.routine_details` | Read-mostly: a single scheduled class meeting (course×teacher×room×timeslot×day) |
| Rooms | `resources.rooms` | All `room_type` values |
| **Labs** | *specialization of* `resources.rooms` | `room_type = 'lab'`; write ops force/validate `room_type=lab` |
| **Periods** | *projection of* `timetable.time_slots` | The `period_number`/`name` definition dimension (non-break) |
| TimeSlots | `timetable.time_slots` | Concrete time-bounded slots (full CRUD) |
| Routines | `timetable.routines` | |
| RoutineDetails | `timetable.routine_details` | Nested under routines |

---

## 1. REST API Standards

### 1.1 Design Philosophy
- **Resource-oriented**: URLs are nouns; behavior is expressed via HTTP method, not verbs in the path.
- **Action sub-resources** are permitted only for state transitions that are not naturally CRUD
  (e.g., `POST /routines/{id}/publish`, `PATCH /sessions/{id}/activate`).
- **Stateless**: each request carries full auth context (JWT). No server-side session affinity.
- **Consistent envelope**: every success and error response uses the standard envelope (§1.5).
- **Secure by default**: every endpoint requires authentication unless explicitly tagged `public`.

### 1.2 URI Conventions
```
https://api.eduroutine.com/api/v1/{collection}
https://api.eduroutine.com/api/v1/{collection}/{id}
https://api.eduroutine.com/api/v1/{collection}/{id}/{sub-collection}
https://api.eduroutine.com/api/v1/{collection}/{id}/{sub-collection}/{subId}
```
Rules:
- Collections are **plural, kebab-case** nouns: `time-slots`, `routine-details`, `audit-logs`.
- Path identifiers are **UUID v4** (except `me` alias and `audit-logs` which are filtered by query).
- No trailing slash. No file extensions. Content negotiation via `Accept` header.
- Maximum nesting depth: **2 levels** below the root collection. Deeper relations use query filters
  or `expand`.

### 1.3 HTTP Methods & Semantics
| Method | Operation | Safe | Idempotent | Success | Common errors |
|---|---|---|---|---|---|
| `GET` | Retrieve resource / collection | ✓ | ✓ | 200 | 401, 403, 404 |
| `POST` | Create / non-idempotent action | ✗ | ✗ | 201 (create), 200 (action), 202 (async) | 400, 401, 403, 409, 422 |
| `PUT` | Full replace | ✗ | ✓ | 200 | 400, 401, 403, 404, 409, 412 |
| `PATCH` | Partial update / transition | ✗ | ✗ | 200 | 400, 401, 403, 404, 409, 422 |
| `DELETE` | Remove / deactivate | ✗ | ✓ | 204 | 401, 403, 404, 409 |

- **Soft delete**: `students`, `teachers`, `courses`, `rooms`, `users` are deactivated (status flag),
  not physically removed. `DELETE` returns `204` and sets `is_active=false`/`status`.
- **Hard delete**: `roles`, `sessions`, `batches`, `semesters`, `sections`, `time-slots`, `routines`,
  `routine-details`, `claims` are removed; protected by `409 CONFLICT` when referenced (`RESTRICT` FKs).

### 1.4 Standard Headers
| Header | Direction | Required | Purpose |
|---|---|---|---|
| `Authorization: Bearer <jwt>` | Request | Authenticated routes | Access token |
| `X-Request-ID` | Request/Response | Recommended | Correlation/tracing UUID (server generates if absent) |
| `X-API-Key` | Request | M2M only | Public-API key auth |
| `Accept-Language` | Request | Optional | i18n locale (`en`, `bn`) |
| `If-Match: "<etag>"` | Request | Conditional `PUT`/`PATCH`/`DELETE` | Optimistic concurrency |
| `ETag` | Response | On single-resource GET | Concurrency token (resource `updated_at` hash) |
| `Idempotency-Key` | Request | Optional on `POST` create/bulk | De-dupe retries (24h window) |
| `X-RateLimit-Limit` / `X-RateLimit-Remaining` / `X-RateLimit-Reset` | Response | Always | Rate-limit budget |
| `Retry-After` | Response | On 429/503 | Back-off seconds |
| `Location` | Response | On 201 | URI of created resource |

### 1.5 Response Envelope
**Success (single & action):**
```json
{
  "status": "success",
  "data": { },
  "meta": {
    "request_id": "0f9c2a14-...",
    "timestamp": "2026-06-18T10:00:00Z",
    "version": "1.0"
  }
}
```
**Success (collection):** adds `pagination` to `meta` (see §8).
**Error:** see §7 and `error-response-catalog.md`.

`meta.version` is the **payload schema version** (`major.minor`), independent of the URL API version.

### 1.6 Status-Code Policy
- `200` reads & successful replaces/updates/actions returning a body.
- `201` resource creation (with `Location`).
- `202` accepted async job (scheduling generate, bulk import) — returns a job resource.
- `204` successful delete / action with no body.
- `3xx` only for OAuth redirect flows.
- Never return `200` with an error body. Errors always use 4xx/5xx + error envelope.

### 1.7 Idempotency
- `PUT`/`DELETE` are inherently idempotent.
- `POST` create and `POST .../bulk` accept `Idempotency-Key`. Replays within 24h return the original
  result (and `Idempotent-Replayed: true`).
- State-transition actions (`publish`, `archive`, `activate`) are **idempotent by effect**: re-issuing
  on an already-transitioned resource returns `200` (no-op) — never `409`.

---

## 2. Versioning Strategy

### 2.1 Scheme
- **URL-prefix major versioning**: `/api/v1`, `/api/v2`. Major version changes only for
  **breaking** changes.
- **Non-breaking, additive** changes (new optional fields, new endpoints, new enum values flagged
  `x-extensible-enum`) ship within the same major version and bump `meta.version` minor.

### 2.2 What constitutes breaking (requires new major)
- Removing/renaming a field, endpoint, or path parameter.
- Changing a field type, format, or making an optional field required.
- Removing an enum value or changing default behavior.
- Changing auth or error-code semantics.

### 2.3 Compatibility Rules
- Clients **must ignore unknown response fields** and tolerate new enum values (treat unknown as
  `unknown`).
- Servers **must not** require unknown request fields; unknown request fields are rejected with
  `422 UNPROCESSABLE_ENTITY` (`code=UNKNOWN_FIELD`) unless `?strict=false`.

### 2.4 Deprecation & Sunset
- Deprecated endpoints/fields return `Deprecation: true` and `Sunset: <RFC1123 date>` headers and are
  marked `deprecated: true` in OpenAPI.
- Minimum **6-month** deprecation window for a removed major version. Migration guide published per
  major bump.
- `GET /api/versions` (public) lists supported versions and their lifecycle state.

---

## 6. Validation Rules (general)

Per-field rules live in `dto-catalog.md`. General standards:

### 6.1 Layered Validation
1. **Syntactic** (schema): type, format, length, pattern, range, enum — `400 VALIDATION_ERROR`.
2. **Semantic** (cross-field/business): e.g. `end_date > start_date`, `lab_hours>0 ⇒ room_type=lab` —
   `422 UNPROCESSABLE_ENTITY`.
3. **Referential**: FK existence — `422` (`code=REFERENCE_NOT_FOUND`) for body refs; `404` for path id.
4. **Uniqueness/conflict**: `409 CONFLICT` (`code=DUPLICATE_*` / `*_OVERLAP`).

### 6.2 Common Formats & Constraints
| Type | Rule |
|---|---|
| UUID | RFC 4122 v4, lowercase canonical |
| Email | RFC 5322, ≤255, stored lowercase |
| Password | ≥12 chars, ≥1 upper, ≥1 lower, ≥1 digit, ≥1 symbol; checked vs breach list |
| Phone | E.164, ≤30 |
| Date | ISO 8601 `YYYY-MM-DD` |
| Time | 24h `HH:MM` (or `HH:MM:SS`) |
| Timestamp | RFC 3339 UTC (`Z`), e.g. `2026-06-18T10:00:00Z` |
| Money/credits | Decimal as string or number, scale fixed per field |
| Strings | Trimmed; reject control chars; NFC-normalized |
| `day_of_week` | int 0–6 (0=Mon … 6=Sun) |
| Enums | Closed set; case-sensitive lowercase tokens |

### 6.3 Request Hygiene
- Max body size **1 MB** (bulk endpoints **10 MB**). Exceed ⇒ `413`.
- Max collection items per bulk request: **1000**.
- Reject duplicate keys in JSON. Reject `NaN`/`Infinity`.
- All write requests must be `Content-Type: application/json` (bulk import may accept
  `text/csv` where noted) ⇒ else `415`.

### 6.4 Validation Error Shape
All field errors aggregate into `error.details.fields[]` (never fail-fast on first error) —
see §7.3.

---

## 7. Error Handling Standards

### 7.1 Error Envelope
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": { },
    "request_id": "0f9c2a14-...",
    "timestamp": "2026-06-18T10:00:00Z",
    "documentation_url": "https://docs.eduroutine.com/errors/VALIDATION_ERROR"
  }
}
```
- `code`: stable, machine-readable `SCREAMING_SNAKE_CASE`. Catalog in `error-response-catalog.md`.
- `message`: human-readable, **safe to display**, never leaks internals/stack/SQL.
- `details`: structured, code-specific (e.g. `fields`, `conflicting_resource`, `retry_after`).
- `request_id`: echoes `X-Request-ID` for support correlation.

### 7.2 HTTP ↔ Error-Code Baseline
| HTTP | Primary `code`(s) |
|---|---|
| 400 | `VALIDATION_ERROR`, `MALFORMED_REQUEST` |
| 401 | `UNAUTHORIZED`, `TOKEN_EXPIRED`, `TOKEN_INVALID` |
| 403 | `FORBIDDEN`, `INSUFFICIENT_PERMISSION` |
| 404 | `RESOURCE_NOT_FOUND` |
| 405 | `METHOD_NOT_ALLOWED` |
| 409 | `CONFLICT`, `DUPLICATE_RESOURCE`, `SCHEDULE_CONFLICT`, `STATE_CONFLICT` |
| 412 | `PRECONDITION_FAILED` (If-Match) |
| 413 | `PAYLOAD_TOO_LARGE` |
| 415 | `UNSUPPORTED_MEDIA_TYPE` |
| 422 | `UNPROCESSABLE_ENTITY`, `REFERENCE_NOT_FOUND`, `UNKNOWN_FIELD`, `BUSINESS_RULE_VIOLATION` |
| 429 | `RATE_LIMIT_EXCEEDED` |
| 500 | `INTERNAL_ERROR` |
| 503 | `SERVICE_UNAVAILABLE` |

### 7.3 Field-Validation Details
```json
"details": {
  "fields": [
    { "field": "credits", "code": "OUT_OF_RANGE", "message": "Must be between 0.5 and 6.0.", "rejected_value": 9 },
    { "field": "code", "code": "PATTERN_MISMATCH", "message": "Must match ^[A-Z]{2,4}-\\d{3}$." }
  ]
}
```
`field` uses dotted/bracket JSON paths (`prerequisite_ids[2]`, `address.city`).

### 7.4 Rules
- One error envelope per response. Aggregate multiple field errors; do not return partial success on
  single-item writes.
- Bulk endpoints return a **per-item result report** (§ bulk) instead of failing the whole batch,
  unless `atomic=true`.
- 5xx never echoes input or internal detail; logs carry `request_id` for correlation.
- All error responses include `WWW-Authenticate` (401) / `Retry-After` (429,503) where applicable.

---

## 8. Pagination Standards

### 8.1 Default: Offset/Page Pagination
Query parameters (all list endpoints):
| Param | Type | Default | Bounds |
|---|---|---|---|
| `page` | int | 1 | ≥1 |
| `page_size` | int | 20 | 1–100 |

Response `meta.pagination`:
```json
"pagination": {
  "page": 1,
  "page_size": 20,
  "total_items": 150,
  "total_pages": 8,
  "has_next": true,
  "has_previous": false
}
```
Collection payload:
```json
{ "status": "success", "data": [ ... ],
  "meta": { "request_id": "...", "timestamp": "...", "version": "1.0",
            "pagination": { ... } } }
```

### 8.2 Cursor Pagination (high-volume)
For `audit-logs`, `scheduling/.../logs`, and any feed > ~100k rows, **keyset/cursor** pagination is
offered:
| Param | Type | Notes |
|---|---|---|
| `cursor` | string (opaque) | From previous `meta.pagination.next_cursor` |
| `limit` | int | Default 50, max 200 |

`meta.pagination` for cursor mode: `{ "limit": 50, "next_cursor": "ey...", "has_next": true }`.
`page`/`cursor` are mutually exclusive ⇒ `400` if both supplied.

### 8.3 Rules
- `total_items`/`total_pages` may be omitted (returned as `null`) for cursor mode (count is expensive).
- Out-of-range `page` returns `200` with empty `data` (not 404).
- Pagination is always applied to collections; there is no "return all" mode.

---

## 9. Filtering Standards

### 9.1 Structured Field Filters (preferred)
Each listable field exposes typed query params; multiple params are AND-combined:
```
GET /api/v1/courses?department_id={uuid}&is_active=true&credits_gte=3&credits_lte=4
```
Operator suffixes:
| Suffix | Meaning | Applies to |
|---|---|---|
| *(none)* | equals | all |
| `_ne` | not equals | scalar |
| `_gt`,`_gte`,`_lt`,`_lte` | comparisons | number, date, time |
| `_in` | CSV membership | scalar/enum (`status_in=active,inactive`) |
| `_like` | case-insensitive contains | strings (`title_like=intro`) |
| `_from`,`_to` | inclusive range | date/timestamp (`created_at_from=2026-01-01`) |
| `_isnull` | `true`/`false` null check | nullable |

### 9.2 Full-Text Search
`q` performs server-defined full-text search across a resource's searchable fields:
```
GET /api/v1/students?q=rahman
```

### 9.3 Compact Filter Expression (compat with Phase 5)
`filter=key:value` shorthand is accepted and equals the structured equals form
(`filter=status:active` ≡ `status=active`). Multiple `filter` params AND-combine.

### 9.4 Rules
- Unknown filter field ⇒ `400 VALIDATION_ERROR` (`code=UNKNOWN_FILTER`).
- Type-mismatched value ⇒ `400`. Filtering only on documented filterable fields (see DTO catalog
  "Filterable" column).
- Each endpoint documents its allow-list of filterable fields in `openapi.yaml`.

---

## 10. Sorting Standards

```
GET /api/v1/courses?sort=-created_at,code
```
- `sort` is a CSV of fields; `-` prefix = descending, none/`+` = ascending.
- Default sort per resource is documented (commonly `-created_at`). Stable tiebreaker: `id`.
- Compat: Phase-5 `sort_by` + `sort_order` (`asc|desc`) accepted and mapped to a single-field `sort`.
- Sorting allowed only on documented sortable fields (DTO catalog "Sortable" column); else
  `400 VALIDATION_ERROR` (`code=UNKNOWN_SORT`).
- Max 3 sort keys.

### 10.1 Field Expansion (related-resource embedding)
`expand` embeds related objects to reduce round-trips:
```
GET /api/v1/courses/{id}?expand=department,prerequisites
GET /api/v1/routines/{id}?expand=details.course,details.teacher,details.room
```
- Comma-separated; dotted paths for nested expansion; max depth 2; allow-list per resource.
- Unknown expand target ⇒ `400` (`code=UNKNOWN_EXPAND`).
- Without `expand`, relations are returned as id references only.

---

## 11. Security Standards

### 11.1 Transport & Headers
- **TLS 1.3** mandatory; HSTS `max-age≥31536000; includeSubDomains; preload`.
- Security headers on all responses: `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: DENY`, `Content-Security-Policy` (API: `default-src 'none'`),
  `Referrer-Policy: no-referrer`, `Cache-Control: no-store` on auth/PII responses.
- CORS: explicit origin allow-list per environment; credentials allowed only for trusted origins;
  preflight cached 600s.

### 11.2 Authentication (see Phase 6)
- **Bearer JWT** access tokens, **RS256**, 15-min lifetime; verified via JWKS at
  `/.well-known/jwks.json` (public). `kid` header for rotation.
- **Opaque refresh tokens**, 7-day, SHA-256-hashed in Redis, **rotated on every use**; reuse of a
  revoked token ⇒ revoke all sessions (`code=TOKEN_REUSE_DETECTED`).
- OAuth2 Authorization-Code + **PKCE** for Google/Microsoft/Facebook; cryptographically random
  `state` (CSRF). Provider tokens never returned to client.
- `401` responses include `WWW-Authenticate: Bearer error="invalid_token"`.

### 11.3 Authorization (see Phase 7)
- Hybrid **RBAC + claim-based + resource-based**. Every protected operation declares the required
  permission in `{module}:{action}:{scope}` form (OpenAPI `x-required-permission`).
- Scopes: `*` (all) vs `own` (resource owner / department). Resource-based checks enforce ownership
  for `*:*:own` permissions (e.g., students read only their own schedule).
- Evaluation order: super_admin ⇒ role permission ⇒ claim ⇒ resource ⇒ DENY.
- Authorization failures: `403 FORBIDDEN` (authenticated but not allowed) — never reveal existence of
  resources the caller can't see beyond a generic `404` where enumeration is a risk.

### 11.4 Token & Permission Matrix (summary)
| Concern | Standard |
|---|---|
| Access token claims | `sub, email, roles[], permissions[], session_id, type, iat, exp, iss=eduroutine-api, aud=eduroutine-client` |
| Permission caching | role→perm 5 min; user→perm 15 min (Redis); invalidated on role/claim change |
| Logout | blacklist `jti` until `exp`; revoke refresh token |
| Password change | invalidate all user tokens |

### 11.5 Rate Limiting & Abuse Controls
| Bucket | Limit (default) |
|---|---|
| Unauthenticated (`/auth/login`, `/auth/forgot-password`) | 5 / 15 min / IP+account |
| Authenticated user (global) | 1000 / min |
| Bulk/scheduling-generate | 10 / hour / user |
| Reports/export | 60 / hour / user |
Exceeding ⇒ `429 RATE_LIMIT_EXCEEDED` + `Retry-After`. Failed-login lockout: 10 fails ⇒ 15-min lock.

### 11.6 Data Protection
- PII fields (`email`, `phone`, names) masked in logs; never in URLs/query strings.
- Passwords: Argon2id (per Phase 6); never returned in any DTO.
- Audit: all writes emit `audit.audit_logs` with `actor_id`, `actor_ip`, `correlation_id`.
- IDOR protection: all `own`-scoped access enforced server-side regardless of supplied ids.
- Input is validated/escaped; outputs are JSON-encoded; no HTML rendering in API.

### 11.7 OpenAPI Security Declaration
Two schemes are defined in `openapi.yaml`:
- `bearerAuth` (HTTP bearer, JWT) — default for all routes.
- `apiKeyAuth` (`X-API-Key`) — machine-to-machine public API only.
Public routes (`/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/forgot-password`,
`/auth/reset-password`, OAuth init/callback, `/health`, `/api/versions`, `/.well-known/jwks.json`)
declare `security: []`.
