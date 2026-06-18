# Phase 5: API Design

---

## 23. API Design Standards

### Design Philosophy
- **Resource-Oriented**: Every URL represents a resource (noun), not an action
- **Consistent Conventions**: Predictable patterns across all endpoints
- **Versioned**: URL prefix versioning (`/api/v1/`)
- **Stateless**: Each request contains all necessary context
- **Self-Descriptive**: HATEOAS-inspired links where practical
- **Secure by Default**: Authentication required unless explicitly public

### Base URL Convention
```
https://api.eduroutine.com/api/v1/{resource}
https://api.eduroutine.com/api/v1/{resource}/{id}
https://api.eduroutine.com/api/v1/{resource}/{id}/{sub-resource}
```

### HTTP Methods & Semantics
| Method | Operation | Idempotent | Safe | Status Codes |
|---|---|---|---|---|
| GET | Retrieve resource(s) | Yes | Yes | 200, 404 |
| POST | Create resource | No | No | 201, 400, 409 |
| PUT | Full replace resource | Yes | No | 200, 400, 404, 409 |
| PATCH | Partial update | No | No | 200, 400, 404 |
| DELETE | Remove resource | Yes | No | 204, 404 |

### Standard Headers
| Header | When | Purpose |
|---|---|---|
| `Authorization: Bearer <token>` | All authenticated requests | JWT access token |
| `X-Request-ID` | All requests | Correlation ID for tracing |
| `X-API-Key` | Machine-to-machine | API key auth for public API |
| `Accept-Language` | Optional | Locale for i18n |
| `If-Match` | Conditional updates | ETag-based concurrency |
| `X-RateLimit-Remaining` | Response | Rate limit info |

### Response Envelope
```json
{
  "status": "success",
  "data": {},
  "meta": {
    "request_id": "uuid",
    "timestamp": "2026-06-18T10:00:00Z",
    "version": "1.0"
  }
}
```

### Error Response Format
```json
{
  "status": "error",
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Course with id 'abc-123' not found",
    "details": {},
    "request_id": "uuid"
  }
}
```

### Error Codes
| HTTP | Error Code | Description |
|---|---|---|
| 400 | VALIDATION_ERROR | Request validation failed |
| 401 | UNAUTHORIZED | Missing or invalid token |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | RESOURCE_NOT_FOUND | Resource does not exist |
| 409 | CONFLICT | Resource conflict (duplicate, overlap) |
| 422 | UNPROCESSABLE_ENTITY | Semantic validation failure |
| 429 | RATE_LIMIT_EXCEEDED | Too many requests |
| 500 | INTERNAL_ERROR | Unexpected server error |
| 503 | SERVICE_UNAVAILABLE | Temporary outage |

---

## 24. REST Endpoint Design

### Authentication Endpoints
```
POST   /api/v1/auth/register          # Register new user
POST   /api/v1/auth/login             # Email/password login
POST   /api/v1/auth/refresh           # Refresh access token
POST   /api/v1/auth/logout            # Revoke refresh token
POST   /api/v1/auth/forgot-password   # Send reset email
POST   /api/v1/auth/reset-password    # Reset password with token
POST   /api/v1/auth/oauth/{provider}  # Initiate OAuth2 flow
GET    /api/v1/auth/oauth/{provider}/callback  # OAuth2 callback
```

### User Management
```
GET    /api/v1/users                  # List users (admin)
POST   /api/v1/users                  # Create user (admin)
GET    /api/v1/users/{id}             # Get user details
PUT    /api/v1/users/{id}             # Update user
PATCH  /api/v1/users/{id}             # Partial update
DELETE /api/v1/users/{id}             # Deactivate user
GET    /api/v1/users/{id}/roles       # Get user roles
PUT    /api/v1/users/{id}/roles       # Set user roles
GET    /api/v1/users/{id}/claims      # Get user claims
POST   /api/v1/users/{id}/claims      # Add user claim
DELETE /api/v1/users/{id}/claims/{claimId}
GET    /api/v1/users/me               # Current user profile
PATCH  /api/v1/users/me               # Update own profile
PUT    /api/v1/users/me/password      # Change password
```

### Role Management
```
GET    /api/v1/roles                  # List roles
POST   /api/v1/roles                  # Create role
GET    /api/v1/roles/{id}             # Get role details
PUT    /api/v1/roles/{id}             # Update role
DELETE /api/v1/roles/{id}             # Delete role
GET    /api/v1/roles/{id}/permissions # Get role permissions
PUT    /api/v1/roles/{id}/permissions # Set role permissions
```

### Academic Sessions
```
GET    /api/v1/sessions               # List sessions
POST   /api/v1/sessions               # Create session
GET    /api/v1/sessions/{id}          # Get session
PUT    /api/v1/sessions/{id}          # Update session
DELETE /api/v1/sessions/{id}          # Delete session
PATCH  /api/v1/sessions/{id}/activate # Set as current session
```

### Batches
```
GET    /api/v1/batches                # List batches
POST   /api/v1/batches                # Create batch
GET    /api/v1/batches/{id}           # Get batch
PUT    /api/v1/batches/{id}           # Update batch
DELETE /api/v1/batches/{id}           # Delete batch
GET    /api/v1/batches/{id}/sections  # List sections in batch
GET    /api/v1/batches/{id}/routines  # List routines for batch
```

### Semesters
```
GET    /api/v1/semesters              # List semesters
POST   /api/v1/semesters              # Create semester
GET    /api/v1/semesters/{id}         # Get semester
PUT    /api/v1/semesters/{id}         # Update semester
DELETE /api/v1/semesters/{id}         # Delete semester
```

### Courses
```
GET    /api/v1/courses                # List courses (filterable)
POST   /api/v1/courses                # Create course
GET    /api/v1/courses/{id}           # Get course
PUT    /api/v1/courses/{id}           # Update course
DELETE /api/v1/courses/{id}           # Deactivate course
GET    /api/v1/courses/{id}/prerequisites      # List prerequisites
POST   /api/v1/courses/{id}/prerequisites      # Add prerequisite
DELETE /api/v1/courses/{id}/prerequisites/{prereqId}
```

### Sections
```
GET    /api/v1/sections               # List sections
POST   /api/v1/sections               # Create section
GET    /api/v1/sections/{id}          # Get section
PUT    /api/v1/sections/{id}          # Update section
DELETE /api/v1/sections/{id}          # Delete section
GET    /api/v1/sections/{id}/students # Students in section
PUT    /api/v1/sections/{id}/students # Assign students to section
```

### Students
```
GET    /api/v1/students               # List students
POST   /api/v1/students               # Create student record
GET    /api/v1/students/{id}          # Get student details
PUT    /api/v1/students/{id}          # Update student
DELETE /api/v1/students/{id}          # Soft-delete
POST   /api/v1/students/bulk         # Bulk import
GET    /api/v1/students/{id}/schedule # Get student timetable
GET    /api/v1/students/{id}/courses  # Get enrolled courses
POST   /api/v1/students/{id}/enroll   # Enroll in courses
DELETE /api/v1/students/{id}/enroll/{courseId}
```

### Teachers
```
GET    /api/v1/teachers               # List teachers
POST   /api/v1/teachers               # Create teacher record
GET    /api/v1/teachers/{id}          # Get teacher details
PUT    /api/v1/teachers/{id}          # Update teacher
DELETE /api/v1/teachers/{id}          # Soft-delete
GET    /api/v1/teachers/{id}/schedule # Get teacher timetable
GET    /api/v1/teachers/{id}/workload # Get workload summary
PUT    /api/v1/teachers/{id}/availability  # Set availability
GET    /api/v1/teachers/{id}/specializations   # Get specializations
POST   /api/v1/teachers/{id}/specializations   # Add specialization
```

### Rooms
```
GET    /api/v1/rooms                  # List rooms
POST   /api/v1/rooms                  # Create room
GET    /api/v1/rooms/{id}             # Get room details
PUT    /api/v1/rooms/{id}             # Update room
DELETE /api/v1/rooms/{id}             # Deactivate room
GET    /api/v1/rooms/{id}/availability  # Get availability
GET    /api/v1/rooms/{id}/utilization   # Get utilization stats
```

### Time Slots
```
GET    /api/v1/time-slots             # List time slots
POST   /api/v1/time-slots             # Create time slot
PUT    /api/v1/time-slots/{id}        # Update time slot
DELETE /api/v1/time-slots/{id}        # Delete time slot
```

### Routines
```
GET    /api/v1/routines               # List routines
POST   /api/v1/routines               # Create empty routine
GET    /api/v1/routines/{id}          # Get routine with details
PUT    /api/v1/routines/{id}          # Update routine metadata
DELETE /api/v1/routines/{id}          # Delete routine
POST   /api/v1/routines/{id}/publish  # Publish routine
POST   /api/v1/routines/{id}/archive  # Archive routine
POST   /api/v1/routines/{id}/clone    # Clone to new session
GET    /api/v1/routines/{id}/details  # List routine details
```

### Routine Details
```
POST   /api/v1/routines/{routineId}/details       # Add schedule entry
PUT    /api/v1/routines/{routineId}/details/{id}   # Update entry
DELETE /api/v1/routines/{routineId}/details/{id}   # Remove entry
POST   /api/v1/routines/{routineId}/details/bulk   # Bulk add entries
GET    /api/v1/routines/{routineId}/conflicts      # Check conflicts
```

### Scheduling Engine
```
POST   /api/v1/scheduling/generate            # Auto-generate routine
GET    /api/v1/scheduling/generate/{jobId}    # Check generation status
POST   /api/v1/scheduling/validate            # Validate routine
GET    /api/v1/scheduling/constraints         # List all constraints
POST   /api/v1/scheduling/constraints         # Create constraint
DELETE /api/v1/scheduling/constraints/{id}    # Delete constraint
PUT    /api/v1/scheduling/constraints/{id}    # Update constraint
```

### Reports
```
GET    /api/v1/reports/students/{id}/schedule    # PDF/JSON schedule
GET    /api/v1/reports/teachers/{id}/schedule    # Teacher timetable
GET    /api/v1/reports/rooms/{id}/utilization    # Room usage
GET    /api/v1/reports/routines/{id}/conflicts   # Conflict report
GET    /api/v1/reports/routines/{id}/summary     # Schedule summary
GET    /api/v1/reports/dashboard                 # Admin dashboard
```

### Audit Logs (Admin)
```
GET    /api/v1/audit-logs               # Query audit logs
GET    /api/v1/audit-logs/{id}          # Get audit entry detail
```

---

## 25. OpenAPI Specification Strategy

### Approach
- **Auto-generated** from FastAPI route decorators and Pydantic models
- **Documented at** `/docs` (Swagger UI) and `/redoc` (ReDoc)
- **Versioned** alongside API versions
- **Published** as a downloadable `openapi.json` for client generation

### Documentation Requirements
- Every endpoint must have `summary` and `description`
- Every parameter must have `description`
- Every request/response model must have field `description`
- Every enum must document all values
- Examples provided for complex request bodies
- Response schemas include all possible HTTP status codes

### OpenAPI Tags Organization
| Tag | Endpoints |
|---|---|
| Authentication | `/auth/*` |
| Users | `/users/*` |
| Roles & Permissions | `/roles/*`, `/permissions/*` |
| Academic | `/sessions/*`, `/batches/*`, `/semesters/*` |
| Courses | `/courses/*` |
| People | `/students/*`, `/teachers/*` |
| Resources | `/rooms/*`, `/time-slots/*` |
| Routine | `/routines/*` |
| Scheduling | `/scheduling/*` |
| Reports | `/reports/*` |
| Audit | `/audit-logs/*` |

---

## 26. DTO Standards

### Naming Convention
- **Request DTOs**: `{Action}{Resource}Request` (e.g., `CreateCourseRequest`)
- **Response DTOs**: `{Resource}Response` (e.g., `CourseResponse`)
- **List Response**: `{Resource}ListResponse` (e.g., `CourseListResponse`)
- **Pagination**: `PaginatedResponse<{Resource}Response>`

### DTO Design Principles
1. **Explicit**: One DTO per operation — never reuse request DTOs across different operations
2. **Flat**: Avoid deep nesting where possible; use `expand=...` query parameter for nested data
3. **Immutable**: All DTOs are Pydantic models with `frozen=True`
4. **Validated**: Use Pydantic validators for domain-level validation
5. **Versioned**: DTOs namespaced by API version

### Request DTO Example Structure
```python
# CreateCourseRequest
{
  "code": "CSE-101",           # str, required, pattern: ^[A-Z]{3,4}-\d{3}$
  "title": "Introduction to CS", # str, required, max_length: 200
  "credits": 3.0,              # Decimal, required, min: 0.5, max: 6.0
  "lecture_hours": 3,          # int, required, min: 0
  "lab_hours": 0,              # int, optional, default: 0
  "department_id": "uuid",     # UUID, required
  "prerequisite_ids": []       # List[UUID], optional
}
```

### Response DTO Example Structure
```python
# CourseResponse
{
  "id": "uuid",
  "code": "CSE-101",
  "title": "Introduction to Computer Science",
  "credits": 3.0,
  "lecture_hours": 3,
  "lab_hours": 0,
  "department": {              # Nested if ?expand=department
    "id": "uuid",
    "name": "Computer Science",
    "code": "CSE"
  },
  "prerequisites": [],         # List of CourseResponse if ?expand=prerequisites
  "is_active": true,
  "created_at": "2026-01-15T10:00:00Z"
}
```

### Pagination Format
```python
# Request query params
page: int = 1
page_size: int = 20            # max: 100
sort_by: str = "created_at"
sort_order: str = "desc"       # asc | desc
filter: str = "status:active"  # Simple key:value filter

# Response
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 150,
    "total_pages": 8,
    "has_next": true,
    "has_previous": false
  }
}
```
