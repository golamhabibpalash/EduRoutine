# Phase 3: Database Design

---

## 12. Complete ERD

### Notation
- `PK` — Primary Key
- `FK` — Foreign Key
- `UQ` — Unique Constraint
- `IX` — Index
- `NN` — Not Null
- `DF` — Default Value

### Entity Relationship Summary

```
User 1──* UserRole *──1 Role 1──* RolePermission *──1 Permission
  │
  ├──1 Student
  └──1 Teacher

Session 1──* Batch 1──* Section
Session 1──* Semester

Department 1──* Course
Department 1──* Teacher
Department 1──* Batch

Batch 1──* Section 1──* Student
Batch 1──* Routine

Routine 1──* RoutineDetail *──1 Course
RoutineDetail *──1 Teacher
RoutineDetail *──1 Room
RoutineDetail *──1 TimeSlot
RoutineDetail *──1 Section
```

---

## 13. Database Schema Overview

| Schema | Purpose |
|---|---|
| `identity` | Users, roles, permissions, authentication |
| `academic` | Sessions, batches, semesters, courses, sections |
| `people` | Students, teachers, profiles |
| `resources` | Rooms, labs, equipment |
| `timetable` | Routines, routine details, time slots |
| `scheduling` | Constraints, allocation results, optimization logs |
| `audit` | Audit logs, event store |

---

## 14. Table Definitions

### identity.users
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK, DF: gen_random_uuid() |
| email | VARCHAR(255) | NN, UQ |
| email_verified | BOOLEAN | NN, DF: FALSE |
| password_hash | VARCHAR(512) | NN |
| display_name | VARCHAR(200) | NN |
| phone | VARCHAR(30) | NULL |
| is_active | BOOLEAN | NN, DF: TRUE |
| last_login_at | TIMESTAMPTZ | NULL |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |
| updated_at | TIMESTAMPTZ | NN, DF: NOW() |

### identity.roles
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(100) | NN, UQ |
| description | VARCHAR(500) | NULL |
| is_system_role | BOOLEAN | NN, DF: FALSE |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |

### identity.permissions
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| code | VARCHAR(100) | NN, UQ (e.g., "routine:create") |
| name | VARCHAR(200) | NN |
| module | VARCHAR(100) | NN (e.g., "routine", "user") |
| description | VARCHAR(500) | NULL |

### identity.user_roles
| Column | Type | Constraints |
|---|---|---|
| user_id | UUID | PK, FK → users.id |
| role_id | UUID | PK, FK → roles.id |

### identity.role_permissions
| Column | Type | Constraints |
|---|---|---|
| role_id | UUID | PK, FK → roles.id |
| permission_id | UUID | PK, FK → permissions.id |

### identity.user_claims
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | NN, FK → users.id |
| claim_type | VARCHAR(200) | NN |
| claim_value | VARCHAR(500) | NN |
| UQ: (user_id, claim_type, claim_value) |

### identity.refresh_tokens
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | NN, FK → users.id |
| token_hash | VARCHAR(512) | NN, UQ |
| expires_at | TIMESTAMPTZ | NN |
| is_revoked | BOOLEAN | NN, DF: FALSE |
| device_info | VARCHAR(500) | NULL |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |

### academic.sessions
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(100) | NN (e.g., "2025-2026") |
| start_date | DATE | NN |
| end_date | DATE | NN |
| is_current | BOOLEAN | NN, DF: FALSE |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |

### academic.batches
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(100) | NN (e.g., "CSE-2025") |
| code | VARCHAR(50) | NN, UQ |
| session_id | UUID | NN, FK → sessions.id |
| department_id | UUID | NN, FK → departments.id |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |

### academic.semesters
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(100) | NN (e.g., "Fall 2025") |
| number | SMALLINT | NN (1-12) |
| session_id | UUID | NN, FK → sessions.id |
| start_date | DATE | NN |
| end_date | DATE | NN |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |
| UQ: (session_id, number) |

### academic.departments
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(200) | NN |
| code | VARCHAR(20) | NN, UQ |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |

### academic.courses
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| code | VARCHAR(20) | NN, UQ (e.g., "CSE-101") |
| title | VARCHAR(200) | NN |
| credits | DECIMAL(3,1) | NN |
| lecture_hours | SMALLINT | NN, DF: 0 |
| lab_hours | SMALLINT | NN, DF: 0 |
| department_id | UUID | NN, FK → departments.id |
| is_active | BOOLEAN | NN, DF: TRUE |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |

### academic.sections
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(50) | NN (e.g., "A", "B") |
| batch_id | UUID | NN, FK → batches.id |
| max_capacity | SMALLINT | NN |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |
| UQ: (batch_id, name) |

### people.students
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | NN, UQ, FK → users.id |
| roll_number | VARCHAR(50) | NN, UQ |
| registration_number | VARCHAR(50) | NULL, UQ |
| batch_id | UUID | NN, FK → batches.id |
| section_id | UUID | NULL, FK → sections.id |
| enrollment_date | DATE | NN, DF: CURRENT_DATE |
| status | VARCHAR(20) | NN, DF: 'active' |

### people.teachers
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | NN, UQ, FK → users.id |
| employee_code | VARCHAR(50) | NN, UQ |
| designation | VARCHAR(100) | NN |
| department_id | UUID | NN, FK → departments.id |
| max_hours_per_week | SMALLINT | NN, DF: 30 |
| specialization | TEXT[] | NULL |

### people.teacher_course_specializations
| Column | Type | Constraints |
|---|---|---|
| teacher_id | UUID | PK, FK → teachers.id |
| course_id | UUID | PK, FK → courses.id |
| preference_level | SMALLINT | NN, DF: 0 |

### resources.rooms
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(100) | NN |
| code | VARCHAR(50) | NN, UQ |
| building | VARCHAR(100) | NN |
| floor | SMALLINT | NN |
| capacity | SMALLINT | NN |
| room_type | VARCHAR(30) | NN (lecture/lab/seminar/office) |
| has_projector | BOOLEAN | DF: FALSE |
| has_computers | BOOLEAN | DF: FALSE |
| has_ac | BOOLEAN | DF: TRUE |
| is_active | BOOLEAN | DF: TRUE |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |

### timetable.time_slots
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(100) | NN (e.g., "1st Period") |
| period_number | SMALLINT | NN |
| start_time | TIME | NN |
| end_time | TIME | NN |
| duration_minutes | SMALLINT | NN |
| is_break | BOOLEAN | DF: FALSE |
| is_lab_slot | BOOLEAN | DF: FALSE |
| session_id | UUID | FK → sessions.id |
| UQ: (period_number, session_id) |

### timetable.routines
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| title | VARCHAR(200) | NN |
| description | TEXT | NULL |
| session_id | UUID | NN, FK → sessions.id |
| batch_id | UUID | NN, FK → batches.id |
| semester_id | UUID | NULL, FK → semesters.id |
| status | VARCHAR(20) | NN, DF: 'draft' |
| valid_from | DATE | NN |
| valid_to | DATE | NN |
| created_by | UUID | FK → users.id |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |
| updated_at | TIMESTAMPTZ | NN, DF: NOW() |

### timetable.routine_details
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| routine_id | UUID | NN, FK → routines.id |
| day_of_week | SMALLINT | NN (0=Mon, 6=Sun) |
| time_slot_id | UUID | NN, FK → time_slots.id |
| period_number | SMALLINT | NN |
| course_id | UUID | NN, FK → courses.id |
| teacher_id | UUID | NN, FK → teachers.id |
| room_id | UUID | NN, FK → rooms.id |
| section_id | UUID | NULL, FK → sections.id |
| is_lab | BOOLEAN | DF: FALSE |
| group_name | VARCHAR(50) | NULL (for combined classes) |
| UQ: (routine_id, day_of_week, period_number, room_id) |
| UQ: (routine_id, day_of_week, time_slot_id, teacher_id) |

### scheduling.constraints
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(200) | NN |
| type | VARCHAR(20) | NN (hard/soft) |
| category | VARCHAR(50) | NN (time/room/teacher/load) |
| expression | JSONB | NN |
| priority | SMALLINT | NN, DF: 0 |
| is_active | BOOLEAN | DF: TRUE |
| created_at | TIMESTAMPTZ | NN, DF: NOW() |

### scheduling.generation_logs
| Column | Type | Constraints |
|---|---|---|
| id | UUID | PK |
| routine_id | UUID | NN, FK → routines.id |
| status | VARCHAR(20) | NN (running/success/failed) |
| strategy | VARCHAR(50) | NN (graph_coloring/backtracking/hybrid) |
| conflicts_found | INTEGER | DF: 0 |
| conflicts_resolved | INTEGER | DF: 0 |
| execution_time_ms | INTEGER | NULL |
| score | DECIMAL(5,2) | NULL |
| error_message | TEXT | NULL |
| started_at | TIMESTAMPTZ | NN |
| completed_at | TIMESTAMPTZ | NULL |

### audit.audit_logs
| Column | Type | Constraints |
|---|---|---|
| id | BIGSERIAL | PK |
| event_id | UUID | NN, UQ |
| entity_type | VARCHAR(100) | NN |
| entity_id | UUID | NN |
| action | VARCHAR(20) | NN (create/update/delete) |
| old_values | JSONB | NULL |
| new_values | JSONB | NULL |
| actor_id | UUID | NULL |
| actor_ip | INET | NULL |
| user_agent | VARCHAR(500) | NULL |
| correlation_id | UUID | NULL |
| timestamp | TIMESTAMPTZ | NN, DF: NOW() |

---

## 15. Primary Keys

- All primary keys use **UUID v4** (generated via `gen_random_uuid()`)
- Rationale: distributed-friendly, no sequential guessing, supports sharding
- Exception: `audit.audit_logs.id` uses `BIGSERIAL` for append-only sequential performance

---

## 16. Foreign Keys

| FK Name | From | To | On Delete |
|---|---|---|---|
| fk_user_roles_user | user_roles.user_id | users.id | CASCADE |
| fk_user_roles_role | user_roles.role_id | roles.id | CASCADE |
| fk_role_permissions_role | role_permissions.role_id | roles.id | CASCADE |
| fk_role_permissions_perm | role_permissions.permission_id | permissions.id | CASCADE |
| fk_user_claims_user | user_claims.user_id | users.id | CASCADE |
| fk_refresh_tokens_user | refresh_tokens.user_id | users.id | CASCADE |
| fk_batches_session | batches.session_id | sessions.id | RESTRICT |
| fk_batches_dept | batches.department_id | departments.id | RESTRICT |
| fk_semesters_session | semesters.session_id | sessions.id | RESTRICT |
| fk_courses_dept | courses.department_id | departments.id | RESTRICT |
| fk_students_user | students.user_id | users.id | CASCADE |
| fk_students_batch | students.batch_id | batches.id | RESTRICT |
| fk_teachers_user | teachers.user_id | users.id | CASCADE |
| fk_teachers_dept | teachers.department_id | departments.id | RESTRICT |
| fk_routines_session | routines.session_id | sessions.id | RESTRICT |
| fk_routines_batch | routines.batch_id | batches.id | RESTRICT |
| fk_routine_details_routine | routine_details.routine_id | routines.id | CASCADE |
| fk_routine_details_course | routine_details.course_id | courses.id | RESTRICT |
| fk_routine_details_teacher | routine_details.teacher_id | teachers.id | RESTRICT |
| fk_routine_details_room | routine_details.room_id | rooms.id | RESTRICT |
| fk_routine_details_timeslot | routine_details.time_slot_id | time_slots.id | RESTRICT |

---

## 17. Indexing Strategy

### B-Tree Indexes (Default)
| Table | Index Columns | Rationale |
|---|---|---|
| users | (email) | Login lookups |
| users | (is_active) | Filtered queries |
| batches | (session_id) | Routines by session |
| batches | (department_id) | Department filtering |
| courses | (department_id) | Department course listing |
| courses | (code) | Code lookups |
| students | (batch_id) | Batch enrollment |
| students | (roll_number) | Unique student lookups |
| teachers | (department_id) | Department teachers |
| routines | (batch_id, semester_id) | Primary query pattern |
| routine_details | (routine_id) | Detail eager loading |
| routine_details | (teacher_id) | Teacher schedule queries |
| routine_details | (room_id) | Room utilization queries |
| audit_logs | (entity_type, entity_id) | Entity audit trail |
| audit_logs | (actor_id) | User action history |
| audit_logs | (timestamp) | Time-range queries |

### Composite Indexes
| Table | Index Columns | Rationale |
|---|---|---|
| routine_details | (routine_id, day_of_week, period_number) | Conflict detection |
| routine_details | (routine_id, teacher_id, day_of_week) | Teacher clash detection |
| routine_details | (routine_id, room_id, day_of_week) | Room clash detection |
| user_roles | (user_id, role_id) | AuthZ lookups |

### Partial Indexes
```sql
CREATE INDEX idx_active_sessions ON academic.sessions (id) WHERE is_current = TRUE;
CREATE INDEX idx_active_routines ON timetable.routines (id) WHERE status = 'published';
```

### Covering Indexes (PostgreSQL INCLUDE)
```sql
CREATE INDEX idx_routine_details_covering ON timetable.routine_details (routine_id)
INCLUDE (day_of_week, period_number, course_id, teacher_id, room_id);
```

---

## 18. Partitioning Strategy

### Audit Logs — Time-Based Partitioning
- Table: `audit.audit_logs`
- Method: **Range partitioning** by `timestamp`
- Partition interval: **Monthly**
- Naming: `audit_logs_2025_01`, `audit_logs_2025_02`, ...

```sql
CREATE TABLE audit.audit_logs (
    id BIGSERIAL,
    event_id UUID NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ...
) PARTITION BY RANGE (timestamp);
```

### Future Partitioning Candidates
| Table | Method | Trigger |
|---|---|---|
| scheduling.generation_logs | Range by month | When > 1M rows |
| timetable.routine_details | List by session | When cross-session data grows |
| identity.refresh_tokens | Range by expires_at | Cleanup efficiency |

### Partitioning Rules
- Partition keys are immutable
- Each partition has its own indexes
- Auto-creation of future partitions via pg_partman or cron job
- Archive partitions > 2 years old to cold storage
