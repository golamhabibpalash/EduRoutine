# Phase 7: Authorization Design

---

## 32. Authorization Design

### Authorization Architecture
```
                    ┌─────────────────────────────┐
                    │      Authorization Flow      │
                    └─────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │           JWT Token            │
                    │     (contains roles + claims)  │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │    Authorization Middleware     │
                    │  Decodes JWT → Extracts Claims │
                    └───────────────┬───────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
    ┌──────────────┐      ┌────────────────┐      ┌──────────────┐
    │  Role-Based   │      │  Claim-Based   │      │  Resource-   │
    │   Auth (RBAC) │      │  Auth (CBA)    │      │  Based Auth  │
    └──────────────┘      └────────────────┘      └──────────────┘
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────────────────────────────────────────────────┐
    │                    Policy Evaluator                        │
    │  Combines role checks + claim checks + resource policies   │
    └───────────────────────────────────────────────────────────┘
            │
            ▼
    ┌──────────────────┐
    │  Allow / Deny    │
    └──────────────────┘
```

### Authorization Models
| Model | Granularity | Use Case |
|---|---|---|
| RBAC | Coarse | Module-level access (e.g., "Can access routines module") |
| Claim-Based | Fine | Specific permissions (e.g., "Can publish routine") |
| Resource-Based | Instance | Ownership checks (e.g., "Can edit own schedule") |

---

## 33. RBAC Design

### Role Hierarchy
```
┌─────────────────────────────────────────────────────────────┐
│  super_admin                                                 │
│  ├── admin                                                   │
│  │   ├── academic_admin                                       │
│  │   ├── scheduling_admin                                     │
│  │   └── reporting_admin                                      │
│  ├── faculty_head                                             │
│  │   └── faculty                                               │
│  └── student_representative                                   │
│      └── student                                              │
└─────────────────────────────────────────────────────────────┘
```

### Built-in Roles
| Role | Level | Description |
|---|---|---|
| `super_admin` | 100 | Full system access, tenant configuration |
| `admin` | 90 | Institution-wide administration |
| `academic_admin` | 80 | Academic structure management |
| `scheduling_admin` | 80 | Timetable creation and publishing |
| `faculty_head` | 70 | Department faculty management |
| `faculty` | 50 | Personal schedule view, availability |
| `student` | 30 | Personal schedule view only |

### RBAC Evaluation
```
1. Extract roles from JWT
2. For each role, compute effective permissions (role hierarchy)
3. Check if any role grants the required permission
4. If no role grants → DENY
```

---

## 34. Claim-Based Authorization

### Permission Schema
```yaml
# Format: {module}:{action}:{scope}
# Scopes: * = all, own = own resources only

# User Management
user:create:*          # Create any user
user:read:*            # View any user
user:read:own          # View own profile
user:update:*          # Update any user
user:update:own        # Update own profile
user:delete:*          # Delete/deactivate any user

# Role Management
role:create:*          # Create roles
role:read:*            # View roles
role:update:*          # Update roles
role:delete:*          # Delete roles
role:assign:*          # Assign roles to users

# Academic Structure
session:create:*       # Create sessions
session:read:*         # View sessions
session:update:*       # Update sessions
session:delete:*       # Delete sessions

course:create:*        # Create courses
course:read:*          # View courses
course:update:*        # Update courses
course:delete:*        # Delete/deactivate courses

# People Management
student:create:*       # Create/import students
student:read:*         # View student details
student:update:*       # Update student records
student:delete:*       # Deactivate students

teacher:create:*       # Create teacher records
teacher:read:*         # View teacher details
teacher:update:*       # Update teacher records
teacher:delete:*       # Deactivate teachers

# Resource Management
room:create:*          # Add rooms
room:read:*            # View rooms
room:update:*          # Update room details
room:delete:*          # Deactivate rooms

# Timetable / Routine
routine:create:*       # Create routines
routine:read:*         # View any routine
routine:read:own       # View own schedule (student/faculty)
routine:update:*       # Update routines
routine:delete:*       # Delete routines
routine:publish:*      # Publish routines
routine:clone:*        # Clone routines

# Scheduling Engine
scheduling:generate:*  # Run auto-generation
scheduling:validate:*  # Run validation
scheduling:constraint:*   # Manage constraints

# Reports
report:read:*          # View any report
report:export:*        # Export reports to PDF/Excel

# Audit
audit:read:*           # View audit logs
audit:export:*         # Export audit logs
```

### Default Role-Permission Mapping
| Role | Core Permissions |
|---|---|
| super_admin | All permissions (`*:*:*`) |
| admin | All except `super_admin` escalation |
| academic_admin | `session:*`, `course:*`, `batch:*`, `semester:*`, `section:*`, `user:read:*` |
| scheduling_admin | `routine:*`, `scheduling:*`, `room:*`, `time-slot:*`, `report:read:*`, `report:export:*` |
| faculty_head | `teacher:read:*`, `routine:read:*`, `report:read:*`, `routine:read:own` |
| faculty | `routine:read:own`, `teacher:read:own`, `teacher:update:own` (availability) |
| student | `routine:read:own` |

---

## 35. Permission Matrix

### Module × Role Permissions

| Module / Action | super_admin | admin | academic_admin | scheduling_admin | faculty_head | faculty | student |
|---|---|---|---|---|---|---|---|
| **User** | | | | | | | |
| user:create | ✓ | ✓ | | | | | |
| user:read | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | ✓ (own) | ✓ (own) |
| user:update | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | ✓ (own) | ✓ (own) |
| user:delete | ✓ | ✓ | | | | | |
| **Role** | | | | | | | |
| role:create | ✓ | ✓ | | | | | |
| role:read | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| role:assign | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | | |
| **Academic** | | | | | | | |
| session:* | ✓ | ✓ | ✓ | ✓ | | | |
| course:* | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | | |
| batch:* | ✓ | ✓ | ✓ | | | | |
| semester:* | ✓ | ✓ | ✓ | | | | |
| section:* | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | | |
| **People** | | | | | | | |
| student:create | ✓ | ✓ | ✓ | | | | |
| student:read | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | | |
| student:update | ✓ | ✓ | ✓ | | ✓ (dept) | | |
| teacher:create | ✓ | ✓ | ✓ | | | | |
| teacher:read | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | ✓ (dept) | |
| teacher:update | ✓ | ✓ | ✓ | | ✓ (dept) | ✓ (own) | |
| **Resources** | | | | | | | |
| room:create | ✓ | ✓ | | ✓ | | | |
| room:read | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| room:update | ✓ | ✓ | | ✓ | | | |
| room:delete | ✓ | ✓ | | ✓ | | | |
| **Routine** | | | | | | | |
| routine:create | ✓ | ✓ | | ✓ | ✓ (dept) | | |
| routine:read | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | ✓ (own) | ✓ (own) |
| routine:update | ✓ | ✓ | | ✓ | ✓ (dept) | | |
| routine:delete | ✓ | ✓ | | ✓ | | | |
| routine:publish | ✓ | ✓ | | ✓ | | | |
| routine:clone | ✓ | ✓ | | ✓ | ✓ (dept) | | |
| **Scheduling** | | | | | | | |
| scheduling:generate | ✓ | ✓ | | ✓ | | | |
| scheduling:validate | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| scheduling:constraint | ✓ | ✓ | | ✓ | ✓ (dept) | | |
| **Reports** | | | | | | | |
| report:read | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | ✓ (own) | ✓ (own) |
| report:export | ✓ | ✓ | ✓ | ✓ | ✓ (dept) | | |
| **Audit** | | | | | | | |
| audit:read | ✓ | ✓ | | | | | |
| audit:export | ✓ | ✓ | | | | | |

### Permission Evaluation Order
```
1. If user is super_admin → ALLOW (skip further checks)
2. If user has explicit permission via role → ALLOW
3. If user has claim-based permission → ALLOW
4. If resource-based check passes → ALLOW (e.g., own resource)
5. Otherwise → DENY
```

### Implementation: Permission Decorator
```python
# Pseudo-code for authorization check
@require_permission("routine:publish")
async def publish_routine(routine_id: UUID, current_user: User):
    # Proceed with publishing
    ...
```

### Dynamic Permission Checks
Used for resource-level authorization:
- **Faculty can edit only their own availability**
- **Students can view only their own schedule**
- **Faculty heads can manage their department's data**
- **Users can update their own profile**

### Permission Caching
- Role-permission mappings cached in Redis (TTL: 5 minutes)
- User-permission mappings cached in Redis (TTL: 15 minutes, or until token refresh)
- Cache invalidated on role/permission assignment changes
