# EduRoutine — Error Response Catalog

> Canonical, stable error codes for API v1. Every non-2xx response uses the error envelope
> (`00-api-standards.md` §7). `code` values are part of the API contract and are **immutable** within
> a major version. `documentation_url` resolves to `https://docs.eduroutine.com/errors/{code}`.

## Envelope
```json
{
  "status": "error",
  "error": {
    "code": "SCHEDULE_CONFLICT",
    "message": "Teacher is already booked for this time slot.",
    "details": { },
    "request_id": "0f9c2a14-3b6e-4c2a-9f3a-1a2b3c4d5e6f",
    "timestamp": "2026-06-18T10:00:00Z",
    "documentation_url": "https://docs.eduroutine.com/errors/SCHEDULE_CONFLICT"
  }
}
```

---

## 1. Master Error Code Table

| HTTP | `code` | Meaning | `details` keys | Retryable |
|---|---|---|---|---|
| 400 | `VALIDATION_ERROR` | Syntactic request validation failed | `fields[]` | No |
| 400 | `MALFORMED_REQUEST` | Body is not valid JSON / wrong shape | `hint` | No |
| 400 | `UNKNOWN_FILTER` | Filter on non-filterable field | `field` | No |
| 400 | `UNKNOWN_SORT` | Sort on non-sortable field | `field` | No |
| 400 | `UNKNOWN_EXPAND` | Unsupported `expand` target | `target` | No |
| 400 | `INVALID_PAGINATION` | `page`/`cursor` mutually exclusive or out of bounds | `param` | No |
| 401 | `UNAUTHORIZED` | No/invalid credentials | — | No |
| 401 | `TOKEN_EXPIRED` | Access token `exp` passed | `expired_at` | Yes (refresh) |
| 401 | `TOKEN_INVALID` | Signature/issuer/audience invalid | — | No |
| 401 | `TOKEN_REVOKED` | Token blacklisted (logout/password change) | — | No |
| 401 | `TOKEN_REUSE_DETECTED` | Revoked refresh token reused → all sessions revoked | — | No |
| 403 | `FORBIDDEN` | Authenticated but not allowed | `required_permission` | No |
| 403 | `INSUFFICIENT_PERMISSION` | Missing specific permission | `required_permission` | No |
| 403 | `ACCOUNT_DISABLED` | User deactivated/locked | — | No |
| 404 | `RESOURCE_NOT_FOUND` | Path resource does not exist | `resource`, `id` | No |
| 405 | `METHOD_NOT_ALLOWED` | Verb not supported on path | `allowed[]` | No |
| 406 | `NOT_ACCEPTABLE` | `Accept` not satisfiable | — | No |
| 409 | `CONFLICT` | Generic conflict | — | No |
| 409 | `DUPLICATE_RESOURCE` | Unique constraint violated | `field`, `value` | No |
| 409 | `RESOURCE_IN_USE` | RESTRICT FK prevents delete | `referenced_by` | No |
| 409 | `STATE_CONFLICT` | Invalid state transition | `current_state`, `attempted` | No |
| 409 | `SCHEDULE_CONFLICT` | Timetable clash | `conflict_type`, `conflicting_detail_id`, `day_of_week`, `period_number` | No |
| 412 | `PRECONDITION_FAILED` | `If-Match` ETag mismatch | `current_etag` | Yes (re-GET) |
| 413 | `PAYLOAD_TOO_LARGE` | Body exceeds limit | `max_bytes` | No |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Bad `Content-Type` | `expected` | No |
| 422 | `UNPROCESSABLE_ENTITY` | Semantic validation failed | `fields[]` / `reason` | No |
| 422 | `REFERENCE_NOT_FOUND` | FK in body does not exist | `field`, `value` | No |
| 422 | `UNKNOWN_FIELD` | Unknown property in strict mode | `field` | No |
| 422 | `BUSINESS_RULE_VIOLATION` | Domain rule failed | `rule`, `message` | No |
| 429 | `RATE_LIMIT_EXCEEDED` | Throttled | `retry_after`, `limit`, `scope` | Yes |
| 500 | `INTERNAL_ERROR` | Unexpected server error | — | Yes |
| 502 | `UPSTREAM_ERROR` | Dependent service failed (OAuth provider) | `service` | Yes |
| 503 | `SERVICE_UNAVAILABLE` | Maintenance/overload | `retry_after` | Yes |
| 504 | `UPSTREAM_TIMEOUT` | Dependency timed out | `service` | Yes |

---

## 2. Canonical Payload Examples

### 2.1 `VALIDATION_ERROR` (400) — aggregated field errors
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": {
      "fields": [
        { "field": "code", "code": "PATTERN_MISMATCH", "message": "Must match ^[A-Z]{2,4}-\\d{3}$.", "rejected_value": "cs101" },
        { "field": "credits", "code": "OUT_OF_RANGE", "message": "Must be between 0.5 and 6.0.", "rejected_value": 9 }
      ]
    },
    "request_id": "0f9c2a14-...",
    "timestamp": "2026-06-18T10:00:00Z"
  }
}
```

**Field-level `code` vocabulary** (inside `details.fields[].code`):
`REQUIRED` · `TYPE_MISMATCH` · `PATTERN_MISMATCH` · `OUT_OF_RANGE` · `TOO_SHORT` · `TOO_LONG` ·
`INVALID_ENUM` · `INVALID_FORMAT` · `NOT_UNIQUE_IN_LIST` · `UNKNOWN_FIELD`.

### 2.2 `UNAUTHORIZED` (401)
```json
{ "status": "error", "error": {
  "code": "TOKEN_EXPIRED", "message": "Access token has expired.",
  "details": { "expired_at": "2026-06-18T09:45:00Z" },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```
Header: `WWW-Authenticate: Bearer error="invalid_token", error_description="The access token expired"`.

### 2.3 `FORBIDDEN` (403)
```json
{ "status": "error", "error": {
  "code": "INSUFFICIENT_PERMISSION", "message": "You do not have permission to publish routines.",
  "details": { "required_permission": "routine:publish:*" },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```

### 2.4 `RESOURCE_NOT_FOUND` (404)
```json
{ "status": "error", "error": {
  "code": "RESOURCE_NOT_FOUND", "message": "Course 'a1b2…' not found.",
  "details": { "resource": "course", "id": "a1b2c3d4-…" },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```

### 2.5 `DUPLICATE_RESOURCE` (409)
```json
{ "status": "error", "error": {
  "code": "DUPLICATE_RESOURCE", "message": "A course with code 'CSE-101' already exists.",
  "details": { "field": "code", "value": "CSE-101" },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```

### 2.6 `RESOURCE_IN_USE` (409) — RESTRICT delete
```json
{ "status": "error", "error": {
  "code": "RESOURCE_IN_USE", "message": "Session cannot be deleted while batches reference it.",
  "details": { "referenced_by": [ { "resource": "batch", "count": 4 } ] },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```

### 2.7 `SCHEDULE_CONFLICT` (409) — timetable clash
```json
{ "status": "error", "error": {
  "code": "SCHEDULE_CONFLICT",
  "message": "Room R-204 is already booked for Monday period 3.",
  "details": {
    "conflict_type": "room",
    "conflicting_detail_id": "8b1c…",
    "day_of_week": 0,
    "period_number": 3,
    "room_id": "…"
  },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```
`conflict_type` ∈ `teacher` · `room` · `section`.

### 2.8 `STATE_CONFLICT` (409) — illegal transition
```json
{ "status": "error", "error": {
  "code": "STATE_CONFLICT", "message": "A published routine cannot be edited. Archive or clone it first.",
  "details": { "current_state": "published", "attempted": "update" },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```

### 2.9 `UNPROCESSABLE_ENTITY` / `BUSINESS_RULE_VIOLATION` (422)
```json
{ "status": "error", "error": {
  "code": "BUSINESS_RULE_VIOLATION",
  "message": "end_date must be after start_date.",
  "details": { "rule": "session.date_order", "fields": [ { "field": "end_date", "code": "OUT_OF_RANGE" } ] },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```

### 2.10 `REFERENCE_NOT_FOUND` (422) — body FK missing
```json
{ "status": "error", "error": {
  "code": "REFERENCE_NOT_FOUND", "message": "department_id does not reference an existing department.",
  "details": { "field": "department_id", "value": "00000000-…" },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```

### 2.11 `PRECONDITION_FAILED` (412) — ETag mismatch
```json
{ "status": "error", "error": {
  "code": "PRECONDITION_FAILED", "message": "The resource was modified by someone else. Re-fetch and retry.",
  "details": { "current_etag": "\"a1b2c3\"" },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```

### 2.12 `RATE_LIMIT_EXCEEDED` (429)
```json
{ "status": "error", "error": {
  "code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Retry in 42 seconds.",
  "details": { "retry_after": 42, "limit": 1000, "scope": "user" },
  "request_id": "…", "timestamp": "2026-06-18T10:00:00Z" } }
```
Headers: `Retry-After: 42`, `X-RateLimit-Limit: 1000`, `X-RateLimit-Remaining: 0`, `X-RateLimit-Reset: <epoch>`.

### 2.13 `INTERNAL_ERROR` (500) — no internal detail leaked
```json
{ "status": "error", "error": {
  "code": "INTERNAL_ERROR", "message": "An unexpected error occurred. Quote the request_id when contacting support.",
  "details": {},
  "request_id": "0f9c2a14-…", "timestamp": "2026-06-18T10:00:00Z" } }
```

---

## 3. Bulk Endpoint Error Semantics
Bulk endpoints (`/students/bulk`, `/routines/{id}/details/bulk`) return **200** with a per-item
`BulkResult` instead of a single error — unless `?atomic=true`, in which case the **first** failure
rolls back the batch and returns the corresponding 4xx error.
```json
{
  "status": "success",
  "data": {
    "total": 3, "succeeded": 2, "failed": 1,
    "results": [
      { "index": 0, "status": "created", "id": "…" },
      { "index": 1, "status": "failed", "id": null,
        "error": { "field": "roll_number", "code": "NOT_UNIQUE_IN_LIST", "message": "Duplicate roll_number '2025-001'." } },
      { "index": 2, "status": "created", "id": "…" }
    ]
  },
  "meta": { "request_id": "…", "timestamp": "2026-06-18T10:00:00Z", "version": "1.0" }
}
```

---

## 4. Endpoint → Possible Errors Matrix
| Endpoint class | 400 | 401 | 403 | 404 | 409 | 412 | 422 | 429 |
|---|---|---|---|---|---|---|---|---|
| Auth (login/register) | ✓ | ✓ | | | ✓ (register dup) | | ✓ | ✓ |
| List (GET collection) | ✓ | ✓ | ✓ | | | | | ✓ |
| Get (GET /{id}) | | ✓ | ✓ | ✓ | | | | ✓ |
| Create (POST) | ✓ | ✓ | ✓ | | ✓ | | ✓ | ✓ |
| Replace (PUT) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Update (PATCH) | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ |
| Delete (DELETE) | | ✓ | ✓ | ✓ | ✓ (RESTRICT) | | | ✓ |
| Routine detail write | ✓ | ✓ | ✓ | ✓ | ✓ (SCHEDULE) | | ✓ | ✓ |
| State action (publish/activate) | | ✓ | ✓ | ✓ | ✓ (STATE) | | ✓ | ✓ |

> All endpoints may additionally return `500`, `503`, `502`, `504` for server/dependency faults.

---

## 5. Client Handling Guidance
- **Always** branch on `error.code`, not `message` (message is localized/displayable, may change).
- `401 TOKEN_EXPIRED` → call `/auth/refresh` once, then retry; any other 401 → re-authenticate.
- `409 *` and `422 *` are non-retryable as-is — fix input/state.
- `412` → re-GET to obtain a fresh ETag, reapply changes, retry.
- `429`/`503` → honor `Retry-After` with exponential backoff + jitter.
- Surface `request_id` to end users for support correlation.
