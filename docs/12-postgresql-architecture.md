# PostgreSQL Database Architecture

**Document ID:** EDU-DB-001
**Version:** 1.0
**Date:** 2026-06-18
**Author:** Principal Database Architect

---

## Table of Contents

1. [Naming Conventions & Standards](#1-naming-conventions--standards)
2. [Database Standards](#2-database-standards)
3. [Schema Design](#3-schema-design)
4. [Custom Types & Domains](#4-custom-types--domains)
5. [Complete ERD (Mermaid)](#5-complete-erd-mermaid)
6. [dbdiagram.io Format](#6-dbdiagramio-format)
7. [Table Definitions (DDL)](#7-table-definitions-ddl)
8. [Relationships & Constraints](#8-relationships--constraints)
9. [Index Strategy](#9-index-strategy)
10. [Performance Strategy](#10-performance-strategy)
11. [Partition Strategy](#11-partition-strategy)
12. [Audit Tables](#12-audit-tables)
13. [Multi-Tenant Strategy](#13-multi-tenant-strategy)
14. [Event Sourcing Tables](#14-event-sourcing-tables)
15. [Migration Strategy](#15-migration-strategy)
16. [Appendix: Complete DDL Script](#16-appendix-complete-ddl-script)

---

## 1. Naming Conventions & Standards

### 1.1 General Rules

| Element | Convention | Example |
|---|---|---|
| Database | `snake_case` | `eduroutine` |
| Schema | `snake_case` | `identity`, `timetable` |
| Table | `snake_case`, plural | `routine_details`, `time_slots` |
| Column | `snake_case` | `day_of_week`, `period_number` |
| Primary Key | `id` (UUID) | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` |
| Foreign Key | `{singular_referenced_table}_id` | `routine_id`, `course_id` |
| Unique Constraint | `uq_{table}_{columns}` | `uq_routine_detail_slot` |
| Foreign Key Constraint | `fk_{child}_{parent}` | `fk_routine_details_routine` |
| Check Constraint | `ck_{table}_{column}` | `ck_day_of_week_range` |
| Index | `idx_{table}_{columns}` | `idx_routine_details_teacher` |
| Partial Index | `idx_{table}_{columns}_partial` | `idx_users_active_partial` |
| Unique Index | `uq_{table}_{columns}` | `uq_courses_code` |
| Enum Type | `PascalCase` | `RoutineStatus`, `RoomType` |
| Domain | `snake_case` | `email_address`, `phone_number` |
| Function | `snake_case` | `update_updated_at_column()` |
| Trigger | `trg_{table}_{action}` | `trg_users_updated_at` |
| Sequence | `seq_{table}_{column}` | `seq_audit_logs_id` |

### 1.2 Reserved Words Policy

- All SQL reserved words (e.g., `user`, `role`, `type`) used as identifiers **must** be quoted or schema-qualified
- EduRoutine always uses schema-qualified identifiers: `identity.users`, `identity.roles`
- Avoid reserved words as column names

---

## 2. Database Standards

### 2.1 PostgreSQL Configuration

```sql
-- Database creation
CREATE DATABASE eduroutine
    WITH ENCODING 'UTF8'
    LC_COLLATE 'en_US.UTF-8'
    LC_CTYPE 'en_US.UTF-8'
    TEMPLATE template0;

-- Required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pgcrypto";        -- cryptographic functions
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements"; -- query performance
CREATE EXTENSION IF NOT EXISTS "btree_gin";       -- GIN + b-tree indexes
CREATE EXTENSION IF NOT EXISTS "pg_partman";      -- partition management (future)
CREATE EXTENSION IF NOT EXISTS "pg_trgm";         -- trigram fuzzy search
```

### 2.2 Column Standards

| Rule | Standard |
|---|---|
| Primary Keys | `UUID` with `DEFAULT gen_random_uuid()` |
| Timestamps | `TIMESTAMPTZ` (never `TIMESTAMP` or `TIMESTAMP WITHOUT TIME ZONE`) |
| Date-only | `DATE` (never `TIMESTAMPTZ` for dates) |
| Time-only | `TIME` (never `TIMESTAMPTZ` for times) |
| Monetary | `NUMERIC(12,2)` |
| Percentages | `NUMERIC(5,2)` with CHECK constraint |
| Flags | `BOOLEAN` with `DEFAULT` (never `SMALLINT` or `CHAR(1)`) |
| Audit columns | All tables have `created_at` and `updated_at` |
| Soft delete | `deleted_at TIMESTAMPTZ` (nullable), indexed partial |
| Status columns | `VARCHAR` with CHECK constraint referencing an ENUM |
| JSON data | `JSONB` (never `JSON`) |
| Text search | `TSVECTOR` generated column |

### 2.3 Audit Column Rules

```
Every table MUST include:
    created_at  TIMESTAMPTZ  NOT NULL  DEFAULT NOW()
    updated_at  TIMESTAMPTZ  NOT NULL  DEFAULT NOW()

Tables with soft delete MAY include:
    deleted_at  TIMESTAMPTZ  DEFAULT NULL
```

### 2.4 Trigger for updated_at

```sql
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Applied to every table with updated_at
CREATE TRIGGER trg_{table}_updated_at
    BEFORE UPDATE ON {schema}.{table}
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();
```

---

## 3. Schema Design

### 3.1 Schema Catalog

| Schema | Ownership | Purpose | Access Pattern |
|---|---|---|---|
| `identity` | DBA | Users, roles, permissions, auth tokens | High-read, medium-write |
| `academic` | DBA | Sessions, batches, courses, departments | Low-write, high-read |
| `people` | DBA | Students, teachers, profiles | Medium-read, medium-write |
| `resources` | DBA | Rooms, labs, equipment inventory | Low-write, high-read |
| `timetable` | DBA | Routines, details, time slots | High-read, high-write (scheduling periods) |
| `scheduling` | DBA | Engine constraints, generation logs | Low-read, high-write (during generation) |
| `event_store` | DBA | Domain events, subscriptions | Append-only, high-write |
| `audit` | DBA | Audit logs, entity changes | Append-only, medium-read |
| `reporting` | DBA | Materialized views, aggregations | Read-only (refreshed) |

### 3.2 Schema DDL

```sql
CREATE SCHEMA IF NOT EXISTS identity AUTHORIZATION dba;
CREATE SCHEMA IF NOT EXISTS academic AUTHORIZATION dba;
CREATE SCHEMA IF NOT EXISTS people AUTHORIZATION dba;
CREATE SCHEMA IF NOT EXISTS resources AUTHORIZATION dba;
CREATE SCHEMA IF NOT EXISTS timetable AUTHORIZATION dba;
CREATE SCHEMA IF NOT EXISTS scheduling AUTHORIZATION dba;
CREATE SCHEMA IF NOT EXISTS event_store AUTHORIZATION dba;
CREATE SCHEMA IF NOT EXISTS audit AUTHORIZATION dba;
CREATE SCHEMA IF NOT EXISTS reporting AUTHORIZATION dba;
```

---

## 4. Custom Types & Domains

### 4.1 ENUM Types

```sql
-- ============================================================
-- identity schema enums
-- ============================================================
CREATE TYPE UserStatus AS ENUM ('active', 'inactive', 'locked', 'suspended');
CREATE TYPE MFAMethod AS ENUM ('none', 'totp', 'sms', 'email');

-- ============================================================
-- academic schema enums
-- ============================================================
CREATE TYPE SemesterNumber AS ENUM ('1','2','3','4','5','6','7','8','9','10','11','12');

-- ============================================================
-- people schema enums
-- ============================================================
CREATE TYPE StudentStatus AS ENUM ('active', 'graduated', 'withdrawn', 'suspended');
CREATE TYPE TeacherDesignation AS ENUM (
    'professor', 'associate_professor', 'assistant_professor',
    'lecturer', 'senior_lecturer', 'instructor', 'lab_assistant'
);

-- ============================================================
-- resources schema enums
-- ============================================================
CREATE TYPE RoomType AS ENUM ('lecture_hall', 'classroom', 'lab', 'seminar_room', 'conference_room', 'office');

-- ============================================================
-- timetable schema enums
-- ============================================================
CREATE TYPE DayOfWeek AS ENUM ('monday','tuesday','wednesday','thursday','friday','saturday','sunday');
CREATE TYPE RoutineStatus AS ENUM ('draft', 'published', 'archived');

-- ============================================================
-- scheduling schema enums
-- ============================================================
CREATE TYPE ConstraintType AS ENUM ('hard', 'soft');
CREATE TYPE ConstraintCategory AS ENUM ('time', 'room', 'teacher', 'load', 'section', 'custom');
CREATE TYPE GenerationStatus AS ENUM ('queued', 'running', 'completed', 'failed');
CREATE TYPE ConflictSeverity AS ENUM ('critical', 'high', 'medium', 'low');
CREATE TYPE ConflictCode AS ENUM (
    'TC-001', 'RC-001', 'SC-001', 'TC-002', 'RC-002',
    'RC-003', 'TC-003', 'SC-002', 'SC-003', 'SC-004'
);

-- ============================================================
-- audit & event_store schema enums
-- ============================================================
CREATE TYPE AuditAction AS ENUM ('CREATE', 'UPDATE', 'DELETE', 'PUBLISH', 'ARCHIVE', 'LOGIN', 'LOGOUT', 'IMPORT', 'EXPORT');
CREATE TYPE EventStatus AS ENUM ('pending', 'published', 'failed', 'skipped');
```

### 4.2 DOMAIN Types

```sql
CREATE DOMAIN email_address AS VARCHAR(255)
    CHECK (VALUE ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');

CREATE DOMAIN phone_number AS VARCHAR(30)
    CHECK (VALUE ~ '^\+?[1-9]\d{1,14}$');

CREATE DOMAIN uuid_v4 AS UUID
    CHECK (VALUE IS NOT NULL);

CREATE DOMAIN positive_int AS INTEGER
    CHECK (VALUE > 0);

CREATE DOMAIN non_negative_int AS INTEGER
    CHECK (VALUE >= 0);

CREATE DOMAIN percentage AS NUMERIC(5,2)
    CHECK (VALUE >= 0 AND VALUE <= 100);

CREATE DOMAIN credit_hours AS NUMERIC(3,1)
    CHECK (VALUE >= 0.5 AND VALUE <= 6.0);
```

---

## 5. Complete ERD (Mermaid)

```mermaid
erDiagram

    %% ========================
    %% IDENTITY SCHEMA
    %% ========================
    identity.tenants {
        uuid id PK
        varchar name
        varchar slug UK
        varchar domain
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    identity.users {
        uuid id PK
        uuid tenant_id FK
        email_address email UK
        boolean email_verified
        varchar password_hash
        varchar display_name
        phone_number phone
        user_status status
        mfa_method mfa_method
        varchar mfa_secret
        timestamptz last_login_at
        timestamptz deleted_at
        timestamptz created_at
        timestamptz updated_at
    }

    identity.roles {
        uuid id PK
        uuid tenant_id FK
        varchar name UK
        varchar description
        boolean is_system_role
        timestamptz created_at
    }

    identity.permissions {
        uuid id PK
        varchar code UK
        varchar name
        varchar module
        varchar description
    }

    identity.user_roles {
        uuid user_id FK
        uuid role_id FK
    }

    identity.role_permissions {
        uuid role_id FK
        uuid permission_id FK
    }

    identity.user_claims {
        uuid id PK
        uuid user_id FK
        varchar claim_type
        varchar claim_value
    }

    identity.refresh_tokens {
        uuid id PK
        uuid user_id FK
        varchar token_hash UK
        timestamptz expires_at
        varchar device_info
        inet ip_address
        boolean is_revoked
        timestamptz created_at
    }

    identity.external_logins {
        uuid id PK
        uuid user_id FK
        varchar provider
        varchar provider_subject_id
        varchar provider_email
        jsonb raw_user_info
        timestamptz linked_at
        timestamptz last_login_at
    }

    identity.login_attempts {
        bigint id PK
        uuid user_id FK
        inet ip_address
        varchar user_agent
        boolean success
        varchar failure_reason
        timestamptz attempted_at
    }

    identity.password_reset_tokens {
        uuid id PK
        uuid user_id FK
        varchar token_hash UK
        timestamptz expires_at
        boolean is_used
        timestamptz created_at
    }

    %% ========================
    %% ACADEMIC SCHEMA
    %% ========================
    academic.departments {
        uuid id PK
        uuid tenant_id FK
        varchar name
        varchar code UK
        timestamptz created_at
        timestamptz updated_at
    }

    academic.sessions {
        uuid id PK
        uuid tenant_id FK
        varchar name
        date start_date
        date end_date
        boolean is_current
        timestamptz created_at
        timestamptz updated_at
    }

    academic.batches {
        uuid id PK
        uuid tenant_id FK
        uuid session_id FK
        uuid department_id FK
        varchar name
        varchar code UK
        timestamptz created_at
        timestamptz updated_at
    }

    academic.semesters {
        uuid id PK
        uuid tenant_id FK
        uuid session_id FK
        varchar name
        semester_number number
        date start_date
        date end_date
        timestamptz created_at
        timestamptz updated_at
    }

    academic.courses {
        uuid id PK
        uuid tenant_id FK
        uuid department_id FK
        varchar code UK
        varchar title
        credit_hours credits
        smallint lecture_hours
        smallint lab_hours
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    academic.course_prerequisites {
        uuid course_id FK
        uuid prerequisite_course_id FK
    }

    academic.sections {
        uuid id PK
        uuid tenant_id FK
        uuid batch_id FK
        varchar name
        positive_int max_capacity
        timestamptz created_at
        timestamptz updated_at
    }

    %% ========================
    %% PEOPLE SCHEMA
    %% ========================
    people.students {
        uuid id PK
        uuid tenant_id FK
        uuid user_id FK UK
        varchar roll_number UK
        varchar registration_number UK
        uuid batch_id FK
        uuid section_id FK
        date enrollment_date
        student_status status
        timestamptz created_at
        timestamptz updated_at
    }

    people.student_enrollments {
        uuid id PK
        uuid student_id FK
        uuid course_id FK
        uuid semester_id FK
        date enrolled_at
        date dropped_at
    }

    people.teachers {
        uuid id PK
        uuid tenant_id FK
        uuid user_id FK UK
        varchar employee_code UK
        varchar first_name
        varchar last_name
        teacher_designation designation
        uuid department_id FK
        positive_int max_hours_per_week
        text[] specialization
        timestamptz created_at
        timestamptz updated_at
    }

    people.teacher_course_specializations {
        uuid teacher_id FK
        uuid course_id FK
        smallint preference_level
    }

    people.teacher_availabilities {
        uuid id PK
        uuid tenant_id FK
        uuid teacher_id FK
        day_of_week day_of_week
        time start_time
        time end_time
        boolean is_preferred
        timestamptz created_at
        timestamptz updated_at
    }

    %% ========================
    %% RESOURCES SCHEMA
    %% ========================
    resources.rooms {
        uuid id PK
        uuid tenant_id FK
        varchar name
        varchar code UK
        varchar building
        smallint floor
        positive_int capacity
        room_type room_type
        boolean has_projector
        boolean has_computers
        boolean has_ac
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    resources.room_maintenance_slots {
        uuid id PK
        uuid room_id FK
        date maintenance_date
        time start_time
        time end_time
        varchar reason
        timestamptz created_at
    }

    %% ========================
    %% TIMETABLE SCHEMA
    %% ========================
    timetable.time_slots {
        uuid id PK
        uuid tenant_id FK
        uuid session_id FK
        varchar name
        smallint period_number
        time start_time
        time end_time
        positive_int duration_minutes
        boolean is_break
        boolean is_lab_slot
        timestamptz created_at
        timestamptz updated_at
    }

    timetable.routines {
        uuid id PK
        uuid tenant_id FK
        uuid session_id FK
        uuid batch_id FK
        uuid semester_id FK
        varchar title
        text description
        routine_status status
        integer version
        uuid created_by FK
        timestamptz created_at
        timestamptz updated_at
    }

    timetable.routine_details {
        uuid id PK
        uuid tenant_id FK
        uuid routine_id FK
        day_of_week day_of_week
        uuid time_slot_id FK
        smallint period_number
        uuid course_id FK
        uuid teacher_id FK
        uuid room_id FK
        uuid section_id FK
        boolean is_lab
        varchar group_name
        timestamptz created_at
        timestamptz updated_at
    }

    timetable.teacher_workload {
        uuid id PK
        uuid tenant_id FK
        uuid teacher_id FK
        uuid routine_id FK
        uuid semester_id FK
        positive_int total_hours_per_week
        timestamptz created_at
    }

    %% ========================
    %% SCHEDULING SCHEMA
    %% ========================
    scheduling.constraints {
        uuid id PK
        uuid tenant_id FK
        varchar name
        constraint_type type
        constraint_category category
        jsonb expression
        smallint priority
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    scheduling.generation_jobs {
        uuid id PK
        uuid tenant_id FK
        uuid routine_id FK
        generation_status status
        varchar strategy
        smallint max_iterations
        integer conflicts_found
        integer conflicts_resolved
        integer execution_time_ms
        percentage quality_score
        text error_message
        timestamptz started_at
        timestamptz completed_at
        timestamptz created_at
    }

    scheduling.conflicts {
        uuid id PK
        uuid tenant_id FK
        uuid routine_id FK
        uuid generation_job_id FK
        conflict_code conflict_code
        conflict_severity severity
        text description
        jsonb conflicting_entries
        varchar suggestion
        timestamptz created_at
    }

    scheduling.teacher_preferences {
        uuid id PK
        uuid tenant_id FK
        uuid teacher_id FK
        uuid time_slot_id FK
        day_of_week day_of_week
        smallint preference_weight
        timestamptz created_at
        timestamptz updated_at
    }

    %% ========================
    %% EVENT STORE SCHEMA
    %% ========================
    event_store.events {
        bigint id PK
        uuid event_id UK
        varchar aggregate_type
        uuid aggregate_id
        varchar event_type
        jsonb event_data
        integer version
        jsonb metadata
        event_status status
        timestamptz created_at
    }

    event_store.subscriptions {
        uuid id PK
        varchar subscriber_name
        varchar event_type_pattern
        boolean is_active
        timestamptz last_processed_at
        timestamptz created_at
    }

    event_store.outbox_messages {
        uuid id PK
        varchar message_type
        jsonb message_body
        varchar destination
        event_status status
        integer retry_count
        text error_message
        timestamptz created_at
        timestamptz processed_at
    }

    %% ========================
    %% AUDIT SCHEMA
    %% ========================
    audit.audit_logs {
        bigint id PK
        uuid event_id UK
        varchar entity_type
        uuid entity_id
        audit_action action
        jsonb old_values
        jsonb new_values
        uuid actor_id
        inet actor_ip
        varchar user_agent
        uuid correlation_id
        timestamptz timestamp
    }

    audit.entity_changes {
        bigint id PK
        uuid audit_log_id FK
        varchar field_name
        text old_value
        text new_value
        timestamptz timestamp
    }

    %% ==========================================
    %% RELATIONSHIPS
    %% ==========================================

    %% identity.tenants relationships
    identity.tenants ||--o{ identity.users : "has"
    identity.tenants ||--o{ identity.roles : "has"

    %% identity.users relationships
    identity.users ||--o{ identity.user_roles : "has"
    identity.users ||--o{ identity.user_claims : "has"
    identity.users ||--o{ identity.refresh_tokens : "has"
    identity.users ||--o{ identity.external_logins : "has"
    identity.users ||--o{ identity.login_attempts : "records"
    identity.users ||--o{ identity.password_reset_tokens : "has"

    %% identity.roles relationships
    identity.roles ||--o{ identity.user_roles : "assigned-to"
    identity.roles ||--o{ identity.role_permissions : "grants"

    %% identity.permissions relationships
    identity.permissions ||--o{ identity.role_permissions : "assigned-to"

    %% academic relationships
    academic.departments ||--o{ academic.batches : "offers"
    academic.departments ||--o{ academic.courses : "offers"

    academic.sessions ||--o{ academic.batches : "contains"
    academic.sessions ||--o{ academic.semesters : "contains"

    academic.batches ||--o{ academic.sections : "has"
    academic.batches ||--o{ timetable.routines : "has"

    academic.courses ||--o{ academic.course_prerequisites : "requires"
    academic.courses ||--o{ people.student_enrollments : "enrolled-in"
    academic.courses ||--o{ people.teacher_course_specializations : "taught-by"

    %% people relationships
    people.students ||--o{ people.student_enrollments : "enrolls-in"
    people.teachers ||--o{ people.teacher_course_specializations : "specializes-in"
    people.teachers ||--o{ people.teacher_availabilities : "has"

    %% resources relationships
    resources.rooms ||--o{ resources.room_maintenance_slots : "scheduled-for"

    %% timetable relationships
    timetable.routines ||--o{ timetable.routine_details : "contains"
    timetable.routines ||--o{ scheduling.generation_jobs : "has"

    timetable.routine_details }o--|| academic.courses : "references"
    timetable.routine_details }o--|| people.teachers : "references"
    timetable.routine_details }o--|| resources.rooms : "references"
    timetable.routine_details }o--|| academic.sections : "references"
    timetable.routine_details }o--|| timetable.time_slots : "references"

    %% scheduling relationships
    scheduling.generation_jobs ||--o{ scheduling.conflicts : "detected"
```

---

## 6. dbdiagram.io Format

```dbml
// ============================================================
// EduRoutine Database Design
// dbdiagram.io DSL Format
// ============================================================

Project EduRoutine {
  database_type: 'PostgreSQL'
  Note: 'EduRoutine - Educational Institution Timetable Management System'
}

// ============================================================
// ENUM Definitions
// ============================================================

Table UserStatus {
  value varchar [note: 'active, inactive, locked, suspended']
}

Table MFAMethod {
  value varchar [note: 'none, totp, sms, email']
}

Table StudentStatus {
  value varchar [note: 'active, graduated, withdrawn, suspended']
}

Table TeacherDesignation {
  value varchar [note: 'professor, associate_professor, assistant_professor, lecturer, senior_lecturer, instructor, lab_assistant']
}

Table RoomType {
  value varchar [note: 'lecture_hall, classroom, lab, seminar_room, conference_room, office']
}

Table DayOfWeek {
  value varchar [note: 'monday, tuesday, wednesday, thursday, friday, saturday, sunday']
}

Table RoutineStatus {
  value varchar [note: 'draft, published, archived']
}

Table ConstraintType {
  value varchar [note: 'hard, soft']
}

Table ConstraintCategory {
  value varchar [note: 'time, room, teacher, load, section, custom']
}

Table GenerationStatus {
  value varchar [note: 'queued, running, completed, failed']
}

Table ConflictSeverity {
  value varchar [note: 'critical, high, medium, low']
}

Table ConflictCode {
  value varchar [note: 'TC-001, RC-001, SC-001, TC-002, RC-002, RC-003, TC-003, SC-002, SC-003, SC-004']
}

Table AuditAction {
  value varchar [note: 'CREATE, UPDATE, DELETE, PUBLISH, ARCHIVE, LOGIN, LOGOUT, IMPORT, EXPORT']
}

Table EventStatus {
  value varchar [note: 'pending, published, failed, skipped']
}

// ============================================================
// IDENTITY SCHEMA
// ============================================================

Table identity.tenants {
  id UUID [pk, default: `gen_random_uuid()`]
  name VARCHAR(200) [not null]
  slug VARCHAR(100) [unique, not null]
  domain VARCHAR(255)
  is_active BOOLEAN [default: true]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table identity.users {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  email VARCHAR(255) [unique, not null]
  email_verified BOOLEAN [default: false]
  password_hash VARCHAR(512) [not null]
  display_name VARCHAR(200) [not null]
  phone VARCHAR(30)
  status UserStatus [not null, default: 'active']
  mfa_method MFAMethod [not null, default: 'none']
  mfa_secret VARCHAR(255)
  last_login_at TIMESTAMPTZ
  deleted_at TIMESTAMPTZ
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table identity.roles {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  name VARCHAR(100) [unique, not null]
  description VARCHAR(500)
  is_system_role BOOLEAN [default: false]
  created_at TIMESTAMPTZ [not null, default: `now()`]
}

Table identity.permissions {
  id UUID [pk, default: `gen_random_uuid()`]
  code VARCHAR(100) [unique, not null]
  name VARCHAR(200) [not null]
  module VARCHAR(100) [not null]
  description VARCHAR(500)
}

Table identity.user_roles {
  user_id UUID [pk, ref: > identity.users.id]
  role_id UUID [pk, ref: > identity.roles.id]
}

Table identity.role_permissions {
  role_id UUID [pk, ref: > identity.roles.id]
  permission_id UUID [pk, ref: > identity.permissions.id]
}

Table identity.user_claims {
  id UUID [pk, default: `gen_random_uuid()`]
  user_id UUID [not null, ref: > identity.users.id]
  claim_type VARCHAR(200) [not null]
  claim_value VARCHAR(500) [not null]
  unique: (user_id, claim_type, claim_value)
}

Table identity.refresh_tokens {
  id UUID [pk, default: `gen_random_uuid()`]
  user_id UUID [not null, ref: > identity.users.id]
  token_hash VARCHAR(512) [unique, not null]
  expires_at TIMESTAMPTZ [not null]
  device_info VARCHAR(500)
  ip_address INET
  is_revoked BOOLEAN [default: false]
  created_at TIMESTAMPTZ [not null, default: `now()`]
}

Table identity.external_logins {
  id UUID [pk, default: `gen_random_uuid()`]
  user_id UUID [not null, ref: > identity.users.id]
  provider VARCHAR(50) [not null]
  provider_subject_id VARCHAR(255) [not null]
  provider_email VARCHAR(255)
  raw_user_info JSONB
  linked_at TIMESTAMPTZ [not null, default: `now()`]
  last_login_at TIMESTAMPTZ
  unique: (provider, provider_subject_id)
}

Table identity.login_attempts {
  id BIGSERIAL [pk]
  user_id UUID [ref: > identity.users.id]
  ip_address INET [not null]
  user_agent VARCHAR(500)
  success BOOLEAN [not null]
  failure_reason VARCHAR(100)
  attempted_at TIMESTAMPTZ [not null, default: `now()`]
}

Table identity.password_reset_tokens {
  id UUID [pk, default: `gen_random_uuid()`]
  user_id UUID [not null, ref: > identity.users.id]
  token_hash VARCHAR(512) [unique, not null]
  expires_at TIMESTAMPTZ [not null]
  is_used BOOLEAN [default: false]
  created_at TIMESTAMPTZ [not null, default: `now()`]
}

// ============================================================
// ACADEMIC SCHEMA
// ============================================================

Table academic.departments {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  name VARCHAR(200) [not null]
  code VARCHAR(20) [unique, not null]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table academic.sessions {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  name VARCHAR(100) [not null]
  start_date DATE [not null]
  end_date DATE [not null]
  is_current BOOLEAN [default: false]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table academic.batches {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  session_id UUID [not null, ref: > academic.sessions.id]
  department_id UUID [not null, ref: > academic.departments.id]
  name VARCHAR(100) [not null]
  code VARCHAR(50) [unique, not null]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table academic.semesters {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  session_id UUID [not null, ref: > academic.sessions.id]
  name VARCHAR(100) [not null]
  number SMALLINT [not null]
  start_date DATE [not null]
  end_date DATE [not null]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
  unique: (session_id, number)
}

Table academic.courses {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  department_id UUID [not null, ref: > academic.departments.id]
  code VARCHAR(20) [unique, not null]
  title VARCHAR(200) [not null]
  credits NUMERIC(3,1) [not null]
  lecture_hours SMALLINT [not null, default: 0]
  lab_hours SMALLINT [not null, default: 0]
  is_active BOOLEAN [default: true]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table academic.course_prerequisites {
  course_id UUID [pk, ref: > academic.courses.id]
  prerequisite_course_id UUID [pk, ref: > academic.courses.id]
}

Table academic.sections {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  batch_id UUID [not null, ref: > academic.batches.id]
  name VARCHAR(50) [not null]
  max_capacity SMALLINT [not null]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
  unique: (batch_id, name)
}

// ============================================================
// PEOPLE SCHEMA
// ============================================================

Table people.students {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  user_id UUID [unique, not null, ref: > identity.users.id]
  roll_number VARCHAR(50) [unique, not null]
  registration_number VARCHAR(50) [unique]
  batch_id UUID [not null, ref: > academic.batches.id]
  section_id UUID [ref: > academic.sections.id]
  enrollment_date DATE [not null, default: `current_date`]
  status StudentStatus [not null, default: 'active']
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table people.student_enrollments {
  id UUID [pk, default: `gen_random_uuid()`]
  student_id UUID [not null, ref: > people.students.id]
  course_id UUID [not null, ref: > academic.courses.id]
  semester_id UUID [not null, ref: > academic.semesters.id]
  enrolled_at DATE [not null, default: `current_date`]
  dropped_at DATE
  unique: (student_id, course_id, semester_id)
}

Table people.teachers {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  user_id UUID [unique, not null, ref: > identity.users.id]
  employee_code VARCHAR(50) [unique, not null]
  first_name VARCHAR(100) [not null]
  last_name VARCHAR(100) [not null]
  designation TeacherDesignation [not null]
  department_id UUID [not null, ref: > academic.departments.id]
  max_hours_per_week SMALLINT [not null, default: 30]
  specialization TEXT[]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table people.teacher_course_specializations {
  teacher_id UUID [pk, ref: > people.teachers.id]
  course_id UUID [pk, ref: > academic.courses.id]
  preference_level SMALLINT [default: 0]
}

Table people.teacher_availabilities {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  teacher_id UUID [not null, ref: > people.teachers.id]
  day_of_week DayOfWeek [not null]
  start_time TIME [not null]
  end_time TIME [not null]
  is_preferred BOOLEAN [default: true]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

// ============================================================
// RESOURCES SCHEMA
// ============================================================

Table resources.rooms {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  name VARCHAR(100) [not null]
  code VARCHAR(50) [unique, not null]
  building VARCHAR(100) [not null]
  floor SMALLINT [not null]
  capacity SMALLINT [not null]
  room_type RoomType [not null]
  has_projector BOOLEAN [default: false]
  has_computers BOOLEAN [default: false]
  has_ac BOOLEAN [default: true]
  is_active BOOLEAN [default: true]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table resources.room_maintenance_slots {
  id UUID [pk, default: `gen_random_uuid()`]
  room_id UUID [not null, ref: > resources.rooms.id]
  maintenance_date DATE [not null]
  start_time TIME [not null]
  end_time TIME [not null]
  reason VARCHAR(500)
  created_at TIMESTAMPTZ [not null, default: `now()`]
}

// ============================================================
// TIMETABLE SCHEMA
// ============================================================

Table timetable.time_slots {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  session_id UUID [not null, ref: > academic.sessions.id]
  name VARCHAR(100) [not null]
  period_number SMALLINT [not null]
  start_time TIME [not null]
  end_time TIME [not null]
  duration_minutes SMALLINT [not null]
  is_break BOOLEAN [default: false]
  is_lab_slot BOOLEAN [default: false]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
  unique: (session_id, period_number)
}

Table timetable.routines {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  session_id UUID [not null, ref: > academic.sessions.id]
  batch_id UUID [not null, ref: > academic.batches.id]
  semester_id UUID [ref: > academic.semesters.id]
  title VARCHAR(200) [not null]
  description TEXT
  status RoutineStatus [not null, default: 'draft']
  version INTEGER [not null, default: 1]
  created_by UUID [not null, ref: > identity.users.id]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table timetable.routine_details {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  routine_id UUID [not null, ref: > timetable.routines.id]
  day_of_week DayOfWeek [not null]
  time_slot_id UUID [not null, ref: > timetable.time_slots.id]
  period_number SMALLINT [not null]
  course_id UUID [not null, ref: > academic.courses.id]
  teacher_id UUID [not null, ref: > people.teachers.id]
  room_id UUID [not null, ref: > resources.rooms.id]
  section_id UUID [ref: > academic.sections.id]
  is_lab BOOLEAN [default: false]
  group_name VARCHAR(50)
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
  unique: (routine_id, day_of_week, period_number, room_id)
  unique: (routine_id, day_of_week, time_slot_id, teacher_id)
}

Table timetable.teacher_workload {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  teacher_id UUID [not null, ref: > people.teachers.id]
  routine_id UUID [not null, ref: > timetable.routines.id]
  semester_id UUID [not null, ref: > academic.semesters.id]
  total_hours_per_week SMALLINT [not null]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  unique: (teacher_id, routine_id, semester_id)
}

// ============================================================
// SCHEDULING SCHEMA
// ============================================================

Table scheduling.constraints {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  name VARCHAR(200) [not null]
  type ConstraintType [not null]
  category ConstraintCategory [not null]
  expression JSONB [not null]
  priority SMALLINT [not null, default: 0]
  is_active BOOLEAN [default: true]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
}

Table scheduling.generation_jobs {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  routine_id UUID [not null, ref: > timetable.routines.id]
  status GenerationStatus [not null, default: 'queued']
  strategy VARCHAR(50) [not null]
  max_iterations SMALLINT [default: 1000]
  conflicts_found INTEGER [default: 0]
  conflicts_resolved INTEGER [default: 0]
  execution_time_ms INTEGER
  quality_score NUMERIC(5,2)
  error_message TEXT
  started_at TIMESTAMPTZ
  completed_at TIMESTAMPTZ
  created_at TIMESTAMPTZ [not null, default: `now()`]
}

Table scheduling.conflicts {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  routine_id UUID [not null, ref: > timetable.routines.id]
  generation_job_id UUID [ref: > scheduling.generation_jobs.id]
  conflict_code ConflictCode [not null]
  severity ConflictSeverity [not null]
  description TEXT [not null]
  conflicting_entries JSONB [not null]
  suggestion TEXT
  created_at TIMESTAMPTZ [not null, default: `now()`]
}

Table scheduling.teacher_preferences {
  id UUID [pk, default: `gen_random_uuid()`]
  tenant_id UUID [not null, ref: > identity.tenants.id]
  teacher_id UUID [not null, ref: > people.teachers.id]
  time_slot_id UUID [not null, ref: > timetable.time_slots.id]
  day_of_week DayOfWeek [not null]
  preference_weight SMALLINT [not null, default: 0]
  created_at TIMESTAMPTZ [not null, default: `now()`]
  updated_at TIMESTAMPTZ [not null, default: `now()`]
  unique: (teacher_id, day_of_week, time_slot_id)
}

// ============================================================
// EVENT STORE SCHEMA
// ============================================================

Table event_store.events {
  id BIGSERIAL [pk]
  event_id UUID [unique, not null]
  aggregate_type VARCHAR(100) [not null]
  aggregate_id UUID [not null]
  event_type VARCHAR(200) [not null]
  event_data JSONB [not null]
  version INTEGER [not null]
  metadata JSONB
  status EventStatus [not null, default: 'pending']
  created_at TIMESTAMPTZ [not null, default: `now()`]
}

Table event_store.subscriptions {
  id UUID [pk, default: `gen_random_uuid()`]
  subscriber_name VARCHAR(200) [not null]
  event_type_pattern VARCHAR(200) [not null]
  is_active BOOLEAN [default: true]
  last_processed_at TIMESTAMPTZ
  created_at TIMESTAMPTZ [not null, default: `now()`]
}

Table event_store.outbox_messages {
  id UUID [pk, default: `gen_random_uuid()`]
  message_type VARCHAR(200) [not null]
  message_body JSONB [not null]
  destination VARCHAR(200)
  status EventStatus [not null, default: 'pending']
  retry_count INTEGER [default: 0]
  error_message TEXT
  created_at TIMESTAMPTZ [not null, default: `now()`]
  processed_at TIMESTAMPTZ
}

// ============================================================
// AUDIT SCHEMA
// ============================================================

Table audit.audit_logs {
  id BIGSERIAL [pk]
  event_id UUID [unique, not null]
  entity_type VARCHAR(100) [not null]
  entity_id UUID [not null]
  action AuditAction [not null]
  old_values JSONB
  new_values JSONB
  actor_id UUID
  actor_ip INET
  user_agent VARCHAR(500)
  correlation_id UUID
  timestamp TIMESTAMPTZ [not null, default: `now()`]
}

Table audit.entity_changes {
  id BIGSERIAL [pk]
  audit_log_id BIGINT [not null, ref: > audit.audit_logs.id]
  field_name VARCHAR(200) [not null]
  old_value TEXT
  new_value TEXT
  timestamp TIMESTAMPTZ [not null, default: `now()`]
}
```

---

## 7. Table Definitions (DDL)

### 7.1 Complete PostgreSQL DDL

The complete DDL script is provided in the appendix. This section covers the design rationale for key tables.

### 7.2 identity.users

```sql
CREATE TABLE identity.users (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES identity.tenants(id) ON DELETE RESTRICT,
    email           VARCHAR(255) NOT NULL,
    email_verified  BOOLEAN     NOT NULL DEFAULT FALSE,
    password_hash   VARCHAR(512) NOT NULL,
    display_name    VARCHAR(200) NOT NULL,
    phone           VARCHAR(30),
    status          UserStatus  NOT NULL DEFAULT 'active',
    mfa_method      MFAMethod   NOT NULL DEFAULT 'none',
    mfa_secret      VARCHAR(255),       -- encrypted at application layer
    last_login_at   TIMESTAMPTZ,
    deleted_at      TIMESTAMPTZ,        -- soft delete
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_users_email_tenant UNIQUE (email, tenant_id),
    CONSTRAINT uq_users_email_active UNIQUE (email) WHERE deleted_at IS NULL,
    CONSTRAINT ck_users_email_format CHECK (email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
);
```

**Design Rationale:**
- `tenant_id` is the first column after PK for clustering
- Soft delete via `deleted_at` (partial unique index on active emails)
- `mfa_secret` encrypted at application layer, not database
- Composite unique on (email, tenant_id) for multi-tenant support

### 7.3 timetable.routine_details (Core Table)

```sql
CREATE TABLE timetable.routine_details (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID        NOT NULL REFERENCES identity.tenants(id) ON DELETE RESTRICT,
    routine_id      UUID        NOT NULL REFERENCES timetable.routines(id) ON DELETE CASCADE,
    day_of_week     DayOfWeek   NOT NULL,
    time_slot_id    UUID        NOT NULL REFERENCES timetable.time_slots(id) ON DELETE RESTRICT,
    period_number   SMALLINT    NOT NULL,
    course_id       UUID        NOT NULL REFERENCES academic.courses(id) ON DELETE RESTRICT,
    teacher_id      UUID        NOT NULL REFERENCES people.teachers(id) ON DELETE RESTRICT,
    room_id         UUID        NOT NULL REFERENCES resources.rooms(id) ON DELETE RESTRICT,
    section_id      UUID        REFERENCES academic.sections(id) ON DELETE RESTRICT,
    is_lab          BOOLEAN     NOT NULL DEFAULT FALSE,
    group_name      VARCHAR(50),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Prevent room double-booking
    CONSTRAINT uq_rd_room_slot UNIQUE (routine_id, day_of_week, period_number, room_id),
    -- Prevent teacher double-booking
    CONSTRAINT uq_rd_teacher_slot UNIQUE (routine_id, day_of_week, time_slot_id, teacher_id),
    -- Prevent section double-booking
    CONSTRAINT uq_rd_section_slot UNIQUE (routine_id, day_of_week, time_slot_id, section_id)
);
```

**Design Rationale:**
- Three unique constraints enforce the core scheduling invariants at the database level
- `ON DELETE CASCADE` on routine_id ensures cleanup when routine is deleted
- `ON DELETE RESTRICT` on course/teacher/room prevents accidental deletion of referenced entities

---

## 8. Relationships & Constraints

### 8.1 Foreign Key Matrix

```sql
-- ============================================================
-- IDENTITY SCHEMA FKs
-- ============================================================
ALTER TABLE identity.users
    ADD CONSTRAINT fk_users_tenant
    FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE RESTRICT;

ALTER TABLE identity.roles
    ADD CONSTRAINT fk_roles_tenant
    FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE;

ALTER TABLE identity.user_roles
    ADD CONSTRAINT fk_user_roles_user
    FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_user_roles_role
    FOREIGN KEY (role_id) REFERENCES identity.roles(id) ON DELETE CASCADE;

ALTER TABLE identity.role_permissions
    ADD CONSTRAINT fk_role_permissions_role
    FOREIGN KEY (role_id) REFERENCES identity.roles(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_role_permissions_perm
    FOREIGN KEY (permission_id) REFERENCES identity.permissions(id) ON DELETE CASCADE;

ALTER TABLE identity.user_claims
    ADD CONSTRAINT fk_user_claims_user
    FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE;

ALTER TABLE identity.refresh_tokens
    ADD CONSTRAINT fk_refresh_tokens_user
    FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE;

ALTER TABLE identity.external_logins
    ADD CONSTRAINT fk_external_logins_user
    FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE;

ALTER TABLE identity.login_attempts
    ADD CONSTRAINT fk_login_attempts_user
    FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE SET NULL;

ALTER TABLE identity.password_reset_tokens
    ADD CONSTRAINT fk_password_reset_tokens_user
    FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE;

-- ============================================================
-- ACADEMIC SCHEMA FKs
-- ============================================================
ALTER TABLE academic.departments
    ADD CONSTRAINT fk_departments_tenant
    FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE;

ALTER TABLE academic.sessions
    ADD CONSTRAINT fk_sessions_tenant
    FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE;

ALTER TABLE academic.batches
    ADD CONSTRAINT fk_batches_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_batches_session FOREIGN KEY (session_id) REFERENCES academic.sessions(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_batches_department FOREIGN KEY (department_id) REFERENCES academic.departments(id) ON DELETE RESTRICT;

ALTER TABLE academic.semesters
    ADD CONSTRAINT fk_semesters_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_semesters_session FOREIGN KEY (session_id) REFERENCES academic.sessions(id) ON DELETE CASCADE;

ALTER TABLE academic.courses
    ADD CONSTRAINT fk_courses_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_courses_department FOREIGN KEY (department_id) REFERENCES academic.departments(id) ON DELETE RESTRICT;

ALTER TABLE academic.course_prerequisites
    ADD CONSTRAINT fk_cp_course FOREIGN KEY (course_id) REFERENCES academic.courses(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_cp_prerequisite FOREIGN KEY (prerequisite_course_id) REFERENCES academic.courses(id) ON DELETE CASCADE;

ALTER TABLE academic.sections
    ADD CONSTRAINT fk_sections_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_sections_batch FOREIGN KEY (batch_id) REFERENCES academic.batches(id) ON DELETE CASCADE;

-- ============================================================
-- PEOPLE SCHEMA FKs
-- ============================================================
ALTER TABLE people.students
    ADD CONSTRAINT fk_students_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_students_user FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_students_batch FOREIGN KEY (batch_id) REFERENCES academic.batches(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_students_section FOREIGN KEY (section_id) REFERENCES academic.sections(id) ON DELETE SET NULL;

ALTER TABLE people.student_enrollments
    ADD CONSTRAINT fk_se_student FOREIGN KEY (student_id) REFERENCES people.students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_se_course FOREIGN KEY (course_id) REFERENCES academic.courses(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_se_semester FOREIGN KEY (semester_id) REFERENCES academic.semesters(id) ON DELETE RESTRICT;

ALTER TABLE people.teachers
    ADD CONSTRAINT fk_teachers_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_teachers_user FOREIGN KEY (user_id) REFERENCES identity.users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_teachers_department FOREIGN KEY (department_id) REFERENCES academic.departments(id) ON DELETE RESTRICT;

ALTER TABLE people.teacher_course_specializations
    ADD CONSTRAINT fk_tcs_teacher FOREIGN KEY (teacher_id) REFERENCES people.teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tcs_course FOREIGN KEY (course_id) REFERENCES academic.courses(id) ON DELETE CASCADE;

ALTER TABLE people.teacher_availabilities
    ADD CONSTRAINT fk_ta_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_ta_teacher FOREIGN KEY (teacher_id) REFERENCES people.teachers(id) ON DELETE CASCADE;

-- ============================================================
-- RESOURCES SCHEMA FKs
-- ============================================================
ALTER TABLE resources.rooms
    ADD CONSTRAINT fk_rooms_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE;

ALTER TABLE resources.room_maintenance_slots
    ADD CONSTRAINT fk_rms_room FOREIGN KEY (room_id) REFERENCES resources.rooms(id) ON DELETE CASCADE;

-- ============================================================
-- TIMETABLE SCHEMA FKs
-- ============================================================
ALTER TABLE timetable.time_slots
    ADD CONSTRAINT fk_ts_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_ts_session FOREIGN KEY (session_id) REFERENCES academic.sessions(id) ON DELETE CASCADE;

ALTER TABLE timetable.routines
    ADD CONSTRAINT fk_routines_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_routines_session FOREIGN KEY (session_id) REFERENCES academic.sessions(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_routines_batch FOREIGN KEY (batch_id) REFERENCES academic.batches(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_routines_semester FOREIGN KEY (semester_id) REFERENCES academic.semesters(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_routines_created_by FOREIGN KEY (created_by) REFERENCES identity.users(id) ON DELETE RESTRICT;

ALTER TABLE timetable.routine_details
    ADD CONSTRAINT fk_rd_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_rd_routine FOREIGN KEY (routine_id) REFERENCES timetable.routines(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_rd_timeslot FOREIGN KEY (time_slot_id) REFERENCES timetable.time_slots(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_rd_course FOREIGN KEY (course_id) REFERENCES academic.courses(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_rd_teacher FOREIGN KEY (teacher_id) REFERENCES people.teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_rd_room FOREIGN KEY (room_id) REFERENCES resources.rooms(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_rd_section FOREIGN KEY (section_id) REFERENCES academic.sections(id) ON DELETE RESTRICT;

ALTER TABLE timetable.teacher_workload
    ADD CONSTRAINT fk_tw_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tw_teacher FOREIGN KEY (teacher_id) REFERENCES people.teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tw_routine FOREIGN KEY (routine_id) REFERENCES timetable.routines(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tw_semester FOREIGN KEY (semester_id) REFERENCES academic.semesters(id) ON DELETE RESTRICT;

-- ============================================================
-- SCHEDULING SCHEMA FKs
-- ============================================================
ALTER TABLE scheduling.constraints
    ADD CONSTRAINT fk_constraints_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE;

ALTER TABLE scheduling.generation_jobs
    ADD CONSTRAINT fk_gj_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_gj_routine FOREIGN KEY (routine_id) REFERENCES timetable.routines(id) ON DELETE CASCADE;

ALTER TABLE scheduling.conflicts
    ADD CONSTRAINT fk_conflicts_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_conflicts_routine FOREIGN KEY (routine_id) REFERENCES timetable.routines(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_conflicts_job FOREIGN KEY (generation_job_id) REFERENCES scheduling.generation_jobs(id) ON DELETE SET NULL;

ALTER TABLE scheduling.teacher_preferences
    ADD CONSTRAINT fk_tp_tenant FOREIGN KEY (tenant_id) REFERENCES identity.tenants(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tp_teacher FOREIGN KEY (teacher_id) REFERENCES people.teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tp_timeslot FOREIGN KEY (time_slot_id) REFERENCES timetable.time_slots(id) ON DELETE CASCADE;

-- ============================================================
-- AUDIT SCHEMA FKs
-- ============================================================
ALTER TABLE audit.entity_changes
    ADD CONSTRAINT fk_ec_audit_log FOREIGN KEY (audit_log_id) REFERENCES audit.audit_logs(id) ON DELETE CASCADE;
```

### 8.2 CHECK Constraints

```sql
-- Domain-level CHECK constraints

ALTER TABLE academic.sessions
    ADD CONSTRAINT ck_session_date_range CHECK (end_date >= start_date);

ALTER TABLE academic.semesters
    ADD CONSTRAINT ck_semester_date_range CHECK (end_date >= start_date),
    ADD CONSTRAINT ck_semester_number CHECK (number BETWEEN 1 AND 12);

ALTER TABLE academic.courses
    ADD CONSTRAINT ck_course_credits CHECK (credits >= 0.5 AND credits <= 6.0),
    ADD CONSTRAINT ck_course_hours CHECK (lecture_hours >= 0 AND lab_hours >= 0);

ALTER TABLE academic.sections
    ADD CONSTRAINT ck_section_capacity CHECK (max_capacity > 0 AND max_capacity <= 500);

ALTER TABLE people.teachers
    ADD CONSTRAINT ck_teacher_max_hours CHECK (max_hours_per_week > 0 AND max_hours_per_week <= 60);

ALTER TABLE people.teacher_course_specializations
    ADD CONSTRAINT ck_tcs_preference CHECK (preference_level BETWEEN 0 AND 10);

ALTER TABLE resources.rooms
    ADD CONSTRAINT ck_room_capacity CHECK (capacity > 0 AND capacity <= 1000),
    ADD CONSTRAINT ck_room_floor CHECK (floor >= -5 AND floor <= 100);

ALTER TABLE timetable.time_slots
    ADD CONSTRAINT ck_ts_time_range CHECK (end_time > start_time),
    ADD CONSTRAINT ck_ts_duration CHECK (duration_minutes > 0 AND duration_minutes <= 240),
    ADD CONSTRAINT ck_ts_period CHECK (period_number BETWEEN 1 AND 20);

ALTER TABLE timetable.routine_details
    ADD CONSTRAINT ck_rd_period CHECK (period_number BETWEEN 1 AND 20);

ALTER TABLE scheduling.constraints
    ADD CONSTRAINT ck_constraint_priority CHECK (priority BETWEEN 0 AND 100);

ALTER TABLE scheduling.generation_jobs
    ADD CONSTRAINT ck_gj_iterations CHECK (max_iterations > 0 AND max_iterations <= 10000),
    ADD CONSTRAINT ck_gj_score CHECK (quality_score IS NULL OR (quality_score >= 0 AND quality_score <= 100));

ALTER TABLE scheduling.conflicts
    ADD CONSTRAINT ck_conflict_code_severity CHECK (
        (conflict_code IN ('TC-001','RC-001','SC-001') AND severity = 'critical') OR
        (conflict_code IN ('TC-002','RC-002','RC-003','TC-003') AND severity = 'high') OR
        (conflict_code IN ('SC-002','SC-003') AND severity = 'medium') OR
        (severity = 'low')
    );
```

### 8.3 Exclusion Constraints (Scheduling Overlap Prevention)

```sql
-- Prevent time overlap in teacher availabilities
ALTER TABLE people.teacher_availabilities
    ADD CONSTRAINT excl_ta_no_overlap
    EXCLUDE USING gist (
        teacher_id WITH =,
        day_of_week WITH =,
        tstzrange(
            (now()::date + start_time)::timestamptz,
            (now()::date + end_time)::timestamptz,
            '[)'
        ) WITH &&
    );

-- Prevent room maintenance slot overlap
ALTER TABLE resources.room_maintenance_slots
    ADD CONSTRAINT excl_rms_no_overlap
    EXCLUDE USING gist (
        room_id WITH =,
        tstzrange(
            (maintenance_date + start_time)::timestamptz,
            (maintenance_date + end_time)::timestamptz,
            '[)'
        ) WITH &&
    );
```

---

## 9. Index Strategy

### 9.1 B-Tree Indexes (Default)

```sql
-- ============================================================
-- IDENTITY SCHEMA INDEXES
-- ============================================================
CREATE INDEX idx_users_tenant         ON identity.users(tenant_id);
CREATE INDEX idx_users_email          ON identity.users(email);
CREATE INDEX idx_users_status         ON identity.users(status);
CREATE INDEX idx_users_deleted_at     ON identity.users(deleted_at) WHERE deleted_at IS NOT NULL;
CREATE INDEX idx_roles_tenant         ON identity.roles(tenant_id);
CREATE INDEX idx_roles_name           ON identity.roles(name);
CREATE INDEX idx_permissions_module   ON identity.permissions(module);
CREATE INDEX idx_permissions_code     ON identity.permissions(code);
CREATE INDEX idx_user_roles_user      ON identity.user_roles(user_id);
CREATE INDEX idx_user_roles_role      ON identity.user_roles(role_id);
CREATE INDEX idx_role_permissions_role ON identity.role_permissions(role_id);
CREATE INDEX idx_role_permissions_perm ON identity.role_permissions(permission_id);
CREATE INDEX idx_user_claims_user     ON identity.user_claims(user_id);
CREATE INDEX idx_refresh_tokens_user  ON identity.refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires ON identity.refresh_tokens(expires_at) WHERE is_revoked = FALSE;
CREATE INDEX idx_external_logins_provider ON identity.external_logins(provider, provider_subject_id);
CREATE INDEX idx_login_attempts_user  ON identity.login_attempts(user_id);
CREATE INDEX idx_login_attempts_ip    ON identity.login_attempts(ip_address);
CREATE INDEX idx_login_attempts_time  ON identity.login_attempts(attempted_at);
CREATE INDEX idx_password_reset_user  ON identity.password_reset_tokens(user_id);

-- ============================================================
-- ACADEMIC SCHEMA INDEXES
-- ============================================================
CREATE INDEX idx_departments_tenant   ON academic.departments(tenant_id);
CREATE INDEX idx_sessions_tenant      ON academic.sessions(tenant_id);
CREATE INDEX idx_batches_tenant       ON academic.batches(tenant_id);
CREATE INDEX idx_batches_session      ON academic.batches(session_id);
CREATE INDEX idx_batches_department   ON academic.batches(department_id);
CREATE INDEX idx_semesters_tenant     ON academic.semesters(tenant_id);
CREATE INDEX idx_semesters_session    ON academic.semesters(session_id);
CREATE INDEX idx_courses_tenant       ON academic.courses(tenant_id);
CREATE INDEX idx_courses_department   ON academic.courses(department_id);
CREATE INDEX idx_courses_code         ON academic.courses(code);
CREATE INDEX idx_sections_tenant      ON academic.sections(tenant_id);
CREATE INDEX idx_sections_batch       ON academic.sections(batch_id);

-- ============================================================
-- PEOPLE SCHEMA INDEXES
-- ============================================================
CREATE INDEX idx_students_tenant      ON people.students(tenant_id);
CREATE INDEX idx_students_batch       ON people.students(batch_id);
CREATE INDEX idx_students_section     ON people.students(section_id);
CREATE INDEX idx_students_roll        ON people.students(roll_number);
CREATE INDEX idx_students_status      ON people.students(status);
CREATE INDEX idx_student_enrollments_student ON people.student_enrollments(student_id);
CREATE INDEX idx_student_enrollments_course  ON people.student_enrollments(course_id);
CREATE INDEX idx_teachers_tenant      ON people.teachers(tenant_id);
CREATE INDEX idx_teachers_department  ON people.teachers(department_id);
CREATE INDEX idx_teachers_employee    ON people.teachers(employee_code);
CREATE INDEX idx_ta_teacher           ON people.teacher_availabilities(teacher_id);
CREATE INDEX idx_ta_day               ON people.teacher_availabilities(teacher_id, day_of_week);

-- ============================================================
-- RESOURCES SCHEMA INDEXES
-- ============================================================
CREATE INDEX idx_rooms_tenant         ON resources.rooms(tenant_id);
CREATE INDEX idx_rooms_building       ON resources.rooms(building);
CREATE INDEX idx_rooms_type           ON resources.rooms(room_type);
CREATE INDEX idx_rooms_active         ON resources.rooms(id) WHERE is_active = TRUE;
CREATE INDEX idx_rms_room             ON resources.room_maintenance_slots(room_id);
CREATE INDEX idx_rms_date             ON resources.room_maintenance_slots(maintenance_date);

-- ============================================================
-- TIMETABLE SCHEMA INDEXES
-- ============================================================
CREATE INDEX idx_time_slots_tenant    ON timetable.time_slots(tenant_id);
CREATE INDEX idx_time_slots_session   ON timetable.time_slots(session_id);
CREATE INDEX idx_routines_tenant      ON timetable.routines(tenant_id);
CREATE INDEX idx_routines_batch_sem   ON timetable.routines(batch_id, semester_id);
CREATE INDEX idx_routines_status      ON timetable.routines(status);
CREATE INDEX idx_routines_created_by  ON timetable.routines(created_by);
CREATE INDEX idx_rd_tenant            ON timetable.routine_details(tenant_id);
CREATE INDEX idx_rd_routine           ON timetable.routine_details(routine_id);
CREATE INDEX idx_rd_teacher           ON timetable.routine_details(teacher_id);
CREATE INDEX idx_rd_room              ON timetable.routine_details(room_id);
CREATE INDEX idx_rd_section           ON timetable.routine_details(section_id);
CREATE INDEX idx_rd_course            ON timetable.routine_details(course_id);
CREATE INDEX idx_tw_teacher           ON timetable.teacher_workload(teacher_id);
CREATE INDEX idx_tw_routine           ON timetable.teacher_workload(routine_id);

-- ============================================================
-- SCHEDULING SCHEMA INDEXES
-- ============================================================
CREATE INDEX idx_constraints_tenant   ON scheduling.constraints(tenant_id);
CREATE INDEX idx_constraints_active   ON scheduling.constraints(id) WHERE is_active = TRUE;
CREATE INDEX idx_gj_tenant            ON scheduling.generation_jobs(tenant_id);
CREATE INDEX idx_gj_routine           ON scheduling.generation_jobs(routine_id);
CREATE INDEX idx_gj_status            ON scheduling.generation_jobs(status);
CREATE INDEX idx_conflicts_tenant     ON scheduling.conflicts(tenant_id);
CREATE INDEX idx_conflicts_routine    ON scheduling.conflicts(routine_id);
CREATE INDEX idx_conflicts_severity   ON scheduling.conflicts(severity);
CREATE INDEX idx_tp_teacher           ON scheduling.teacher_preferences(teacher_id);
```

### 9.2 Composite Indexes (Multi-Column)

```sql
-- Primary query patterns
CREATE INDEX idx_rd_teacher_day       ON timetable.routine_details(teacher_id, day_of_week);
CREATE INDEX idx_rd_room_day          ON timetable.routine_details(room_id, day_of_week);
CREATE INDEX idx_rd_section_day       ON timetable.routine_details(section_id, day_of_week);
CREATE INDEX idx_rd_routine_day_period ON timetable.routine_details(routine_id, day_of_week, period_number);

-- Routine lookup
CREATE INDEX idx_routines_session_batch ON timetable.routines(session_id, batch_id);
CREATE INDEX idx_routines_sem_batch_status ON timetable.routines(semester_id, batch_id, status);

-- Conflict detection hot path
CREATE INDEX idx_rd_conflict_teacher ON timetable.routine_details(routine_id, day_of_week, time_slot_id, teacher_id);
CREATE INDEX idx_rd_conflict_room    ON timetable.routine_details(routine_id, day_of_week, time_slot_id, room_id);
CREATE INDEX idx_rd_conflict_section ON timetable.routine_details(routine_id, day_of_week, time_slot_id, section_id);
```

### 9.3 Partial Indexes

```sql
-- Active sessions only
CREATE INDEX idx_sessions_current ON academic.sessions(id) WHERE is_current = TRUE;

-- Active routines only
CREATE INDEX idx_routines_published ON timetable.routines(id) WHERE status = 'published';

-- Non-expired, non-revoked refresh tokens
CREATE INDEX idx_refresh_tokens_valid ON identity.refresh_tokens(user_id)
    WHERE is_revoked = FALSE AND expires_at > NOW();

-- Failed login attempts (last 24 hours)
CREATE INDEX idx_login_attempts_failed_recent ON identity.login_attempts(user_id, attempted_at)
    WHERE success = FALSE AND attempted_at > NOW() - INTERVAL '24 hours';

-- Unprocessed events
CREATE INDEX idx_events_pending ON event_store.events(id) WHERE status = 'pending';
CREATE INDEX idx_outbox_pending ON event_store.outbox_messages(id) WHERE status = 'pending';
```

### 9.4 Covering Indexes (INCLUDE)

```sql
-- Cover routine detail read patterns without table access
CREATE INDEX idx_rd_list_covering ON timetable.routine_details(routine_id, day_of_week, period_number)
    INCLUDE (course_id, teacher_id, room_id, section_id, time_slot_id, is_lab);

-- Cover user lookup without accessing table for auth
CREATE INDEX idx_users_auth_covering ON identity.users(email)
    INCLUDE (id, tenant_id, password_hash, status, mfa_method);
```

### 9.5 GIN Indexes (JSONB & Full-Text)

```sql
-- JSONB query support
CREATE INDEX idx_constraints_expression ON scheduling.constraints USING gin(expression);
CREATE INDEX idx_conflicts_entries ON scheduling.conflicts USING gin(conflicting_entries);
CREATE INDEX idx_external_logins_info ON identity.external_logins USING gin(raw_user_info);
CREATE INDEX idx_events_data ON event_store.events USING gin(event_data);

-- Full-text search on course titles
ALTER TABLE academic.courses ADD COLUMN search_vector TSVECTOR
    GENERATED ALWAYS AS (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(code, ''))) STORED;

CREATE INDEX idx_courses_fts ON academic.courses USING gin(search_vector);
```

### 9.6 BRIN Indexes (Large Append-Only Tables)

```sql
-- Audit logs: time-based queries benefit from BRIN on timestamp
CREATE INDEX idx_audit_logs_brin ON audit.audit_logs USING brin(timestamp)
    WITH (pages_per_range = 32);

-- Event store: naturally ordered by created_at
CREATE INDEX idx_events_brin ON event_store.events USING brin(created_at)
    WITH (pages_per_range = 32);

-- Login attempts: time-ordered data
CREATE INDEX idx_login_attempts_brin ON identity.login_attempts USING brin(attempted_at)
    WITH (pages_per_range = 32);
```

---

## 10. Performance Strategy

### 10.1 Connection Pooling

```sql
-- PgBouncer configuration (recommended)
-- pgbouncer.ini
[databases]
eduroutine = host=localhost port=5432 dbname=eduroutine

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
pool_mode = transaction      -- Best for FastAPI request lifecycle
default_pool_size = 25       -- Per connection pool
max_client_conn = 200        -- Max client connections to pgbouncer
max_db_connections = 50      -- Max connections to PostgreSQL
query_wait_timeout = 10      -- Seconds before timing out
server_idle_timeout = 300    -- Seconds before closing idle connections
```

### 10.2 PostgreSQL Configuration

```ini
# postgresql.conf — Production settings
# Memory
shared_buffers = '2GB'           # 25% of RAM
effective_cache_size = '6GB'     # 75% of RAM
work_mem = '64MB'                # Per-operation memory
maintenance_work_mem = '512MB'   # VACUUM, CREATE INDEX

# Write-Ahead Log
wal_level = 'replica'
max_wal_size = '4GB'
min_wal_size = '1GB'
wal_buffers = '16MB'

# Query Tuning
random_page_cost = 1.1           # SSD optimization
effective_io_concurrency = 200   # SSD optimization
default_statistics_target = 500  # Better query plans

# Connections
max_connections = 50             # PgBouncer handles client connections
superuser_reserved_connections = 5

# Autovacuum
autovacuum_max_workers = 4
autovacuum_naptime = '30s'
autovacuum_vacuum_threshold = 1000
autovacuum_vacuum_scale_factor = 0.05
autovacuum_analyze_threshold = 500
autovacuum_analyze_scale_factor = 0.02

# Parallel query
max_parallel_workers_per_gather = 2
max_parallel_workers = 4
parallel_tuple_cost = 0.01
parallel_setup_cost = 100
```

### 10.3 Query Optimization Patterns

```sql
-- Pattern 1: Use CTEs for complex schedule queries
WITH teacher_schedule AS (
    SELECT
        rd.day_of_week,
        rd.period_number,
        ts.start_time,
        ts.end_time,
        c.code AS course_code,
        c.title AS course_title,
        r.code AS room_code,
        sec.name AS section_name
    FROM timetable.routine_details rd
    JOIN timetable.time_slots ts ON rd.time_slot_id = ts.id
    JOIN academic.courses c ON rd.course_id = c.id
    JOIN resources.rooms r ON rd.room_id = r.id
    LEFT JOIN academic.sections sec ON rd.section_id = sec.id
    WHERE rd.teacher_id = $1
      AND rd.routine_id = $2
    ORDER BY rd.day_of_week, rd.period_number
)
SELECT * FROM teacher_schedule;

-- Pattern 2: Window functions for workload analytics
SELECT
    teacher_id,
    COUNT(*) AS total_slots,
    COUNT(DISTINCT day_of_week) AS days_active,
    ROUND(AVG(period_number), 1) AS avg_period,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS workload_rank
FROM timetable.routine_details
WHERE routine_id = $1
GROUP BY teacher_id
ORDER BY workload_rank;

-- Pattern 3: LATERAL join for conflict detection
SELECT
    a.day_of_week,
    a.period_number,
    a.teacher_id,
    b.id AS conflicting_detail_id,
    b.room_id AS conflicting_room
FROM timetable.routine_details a
CROSS JOIN LATERAL (
    SELECT id, room_id
    FROM timetable.routine_details
    WHERE routine_id = a.routine_id
      AND id <> a.id
      AND day_of_week = a.day_of_week
      AND time_slot_id = a.time_slot_id
      AND room_id = a.room_id
    LIMIT 1
) b
WHERE a.routine_id = $1;
```

### 10.4 Read Replica Strategy

```sql
-- Reporting queries directed to read replica
-- Connection string: postgresql://user:pass@replica:5432/eduroutine

-- Read-only transactions for reporting
BEGIN;
SET TRANSACTION READ ONLY;
SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;

SELECT ... FROM reporting.mv_*;  -- Materialized views on replica

COMMIT;
```

### 10.5 Materialized Views for Reporting

```sql
-- Teacher schedule materialized view
CREATE MATERIALIZED VIEW reporting.teacher_schedule_mv AS
SELECT
    t.id AS teacher_id,
    t.first_name || ' ' || t.last_name AS teacher_name,
    d.name AS department,
    r.title AS routine_title,
    rd.day_of_week,
    ts.start_time,
    ts.end_time,
    c.code AS course_code,
    c.title AS course_title,
    rm.code AS room_code,
    sec.name AS section_name
FROM people.teachers t
JOIN timetable.routine_details rd ON t.id = rd.teacher_id
JOIN timetable.routines r ON rd.routine_id = r.id
JOIN timetable.time_slots ts ON rd.time_slot_id = ts.id
JOIN academic.courses c ON rd.course_id = c.id
JOIN resources.rooms rm ON rd.room_id = rm.id
LEFT JOIN academic.sections sec ON rd.section_id = sec.id
LEFT JOIN academic.departments d ON t.department_id = d.id
WHERE r.status = 'published'
ORDER BY t.id, rd.day_of_week, rd.period_number;

CREATE UNIQUE INDEX idx_mv_teacher_schedule
    ON reporting.teacher_schedule_mv(teacher_id, day_of_week, start_time);

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY reporting.teacher_schedule_mv;
```

### 10.6 ANALYZE & Vacuum Strategy

```sql
-- Daily maintenance job (cron)
-- 03:00 AM daily
VACUUM ANALYZE identity.users;
VACUUM ANALYZE identity.login_attempts;
VACUUM ANALYZE timetable.routine_details;
VACUUM ANALYZE scheduling.generation_jobs;
VACUUM ANALYZE audit.audit_logs;

-- Weekly
REINDEX TABLE identity.refresh_tokens;
REINDEX TABLE audit.audit_logs;

-- Monitor for bloat
SELECT
    schemaname,
    tablename,
    n_live_tup,
    n_dead_tup,
    ROUND(100 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_pct DESC;
```

---

## 11. Partition Strategy

### 11.1 Audit Logs — Range Partitioning by Month

```sql
CREATE TABLE audit.audit_logs (
    id              BIGSERIAL,
    event_id        UUID            NOT NULL,
    entity_type     VARCHAR(100)    NOT NULL,
    entity_id       UUID            NOT NULL,
    action          AuditAction     NOT NULL,
    old_values      JSONB,
    new_values      JSONB,
    actor_id        UUID,
    actor_ip        INET,
    user_agent      VARCHAR(500),
    correlation_id  UUID,
    timestamp       TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    PRIMARY KEY (id, timestamp)     -- Partition key must be part of PK
) PARTITION BY RANGE (timestamp);

-- Monthly partitions (auto-generated via cron/pg_partman)
CREATE TABLE audit.audit_logs_2026_01 PARTITION OF audit.audit_logs
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE audit.audit_logs_2026_02 PARTITION OF audit.audit_logs
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE audit.audit_logs_2026_03 PARTITION OF audit.audit_logs
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

CREATE TABLE audit.audit_logs_2026_04 PARTITION OF audit.audit_logs
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');

CREATE TABLE audit.audit_logs_2026_05 PARTITION OF audit.audit_logs
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

CREATE TABLE audit.audit_logs_2026_06 PARTITION OF audit.audit_logs
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

-- Default partition for unexpected dates
CREATE TABLE audit.audit_logs_default PARTITION OF audit.audit_logs DEFAULT;

-- Indexes on each partition (applied via template or manually)
CREATE INDEX idx_audit_logs_2026_01_entity ON audit.audit_logs_2026_01(entity_type, entity_id);
CREATE INDEX idx_audit_logs_2026_01_actor  ON audit.audit_logs_2026_01(actor_id);

-- BRIN index on each partition for timestamp-range queries
CREATE INDEX idx_audit_logs_2026_01_brin ON audit.audit_logs_2026_01 USING brin(timestamp)
    WITH (pages_per_range = 32);
```

### 11.2 Login Attempts — Range Partitioning by Month

```sql
CREATE TABLE identity.login_attempts (
    id              BIGSERIAL,
    user_id         UUID,
    ip_address      INET            NOT NULL,
    user_agent      VARCHAR(500),
    success         BOOLEAN         NOT NULL,
    failure_reason  VARCHAR(100),
    attempted_at    TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    PRIMARY KEY (id, attempted_at)
) PARTITION BY RANGE (attempted_at);

-- Keep last 3 months hot
CREATE TABLE identity.login_attempts_2026_04 PARTITION OF identity.login_attempts
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE identity.login_attempts_2026_05 PARTITION OF identity.login_attempts
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE identity.login_attempts_2026_06 PARTITION OF identity.login_attempts
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
```

### 11.3 Event Store Events — Range Partitioning by Month

```sql
CREATE TABLE event_store.events (
    id              BIGSERIAL,
    event_id        UUID            NOT NULL,
    aggregate_type  VARCHAR(100)    NOT NULL,
    aggregate_id    UUID            NOT NULL,
    event_type      VARCHAR(200)    NOT NULL,
    event_data      JSONB           NOT NULL,
    version         INTEGER         NOT NULL,
    metadata        JSONB,
    status          EventStatus     NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
```

### 11.4 Partition Management Automation

```sql
-- pg_partman extension setup
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman WITH SCHEMA partman;

-- Auto-manage audit_logs partitions
SELECT partman.create_parent(
    p_parent_table := 'audit.audit_logs',
    p_control := 'timestamp',
    p_type := 'native',
    p_interval := '1 month',
    p_premake := 3,
    p_start_partition := '2026-06-01'
);

-- Schedule partition maintenance (daily cron)
UPDATE partman.part_config
SET infinite_time_partitions = true,
    retention = '24 months',
    retention_keep_table = false
WHERE parent_table = 'audit.audit_logs';

-- Maintenance call (run daily via pg_cron or OS cron)
SELECT partman.run_maintenance();

-- Archive old partitions (older than 24 months)
-- 1. Detach partition
ALTER TABLE audit.audit_logs DETACH PARTITION audit.audit_logs_2024_01;
-- 2. Dump to compressed file
-- 3. Drop from database
DROP TABLE IF EXISTS audit.audit_logs_2024_01;
```

### 11.5 Future Partitioning Candidates

| Table | Method | Trigger | Action |
|---|---|---|---|
| `scheduling.generation_jobs` | Range by `created_at` | Monthly | > 500K rows |
| `scheduling.conflicts` | Range by `created_at` | Monthly | > 500K rows |
| `event_store.outbox_messages` | Range by `created_at` | Weekly | > 100K rows |
| `timetable.routine_details` | List by `routine_id` | When cross-session queries slow | Archive old sessions |

---

## 12. Audit Tables

### 12.1 Audit Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     AUDIT STRATEGY                              │
│                                                                │
│  Application Layer                                             │
│  ┌────────────────────────────────────────────┐                │
│  │  Domain Event → Audit Log Decorator        │                │
│  │  Captures: entity_type, entity_id,         │                │
│  │            action, old_values, new_values,  │                │
│  │            actor_id, correlation_id         │                │
│  └──────────────────┬─────────────────────────┘                │
│                     │                                          │
│                     ▼                                          │
│  Database Layer                                                │
│  ┌────────────────────────────────────────────┐                │
│  │  audit.audit_logs (Partitioned by month)   │                │
│  │  audit.entity_changes (Normalized changes) │                │
│  └────────────────────────────────────────────┘                │
│                     │                                          │
│                     ▼                                          │
│  Retention Policy                                              │
│  ┌────────────────────────────────────────────┐                │
│  │  Hot: Current month (fast queries)         │                │
│  │  Warm: 1-24 months (compressed, queryable) │                │
│  │  Cold: > 24 months (archived to S3)       │                │
│  └────────────────────────────────────────────┘                │
└────────────────────────────────────────────────────────────────┘
```

### 12.2 Audit Log Table

```sql
CREATE TABLE audit.audit_logs (
    id              BIGSERIAL,
    event_id        UUID            NOT NULL,
    entity_type     VARCHAR(100)    NOT NULL,
    entity_id       UUID            NOT NULL,
    action          AuditAction     NOT NULL,
    old_values      JSONB,
    new_values      JSONB,
    actor_id        UUID,
    actor_ip        INET,
    user_agent      VARCHAR(500),
    correlation_id  UUID,
    timestamp       TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    PRIMARY KEY (id, timestamp),

    CONSTRAINT uq_audit_event_id UNIQUE (event_id)
) PARTITION BY RANGE (timestamp);

-- Audit log indexes
CREATE INDEX idx_audit_entity ON audit.audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_actor  ON audit.audit_logs(actor_id);
CREATE INDEX idx_audit_action ON audit.audit_logs(action);
CREATE INDEX idx_audit_correlation ON audit.audit_logs(correlation_id);
```

### 12.3 Entity Changes (Denormalized for Field-Level Queries)

```sql
CREATE TABLE audit.entity_changes (
    id              BIGSERIAL       PRIMARY KEY,
    audit_log_id    BIGINT          NOT NULL REFERENCES audit.audit_logs(id) ON DELETE CASCADE,
    field_name      VARCHAR(200)    NOT NULL,
    old_value       TEXT,
    new_value       TEXT,
    timestamp       TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_entity_changes_audit_log ON audit.entity_changes(audit_log_id);
CREATE INDEX idx_entity_changes_field    ON audit.entity_changes(field_name);
CREATE INDEX idx_entity_changes_new_val  ON audit.entity_changes(new_value)
    WHERE new_value IS NOT NULL;
```

### 12.4 Audit Trigger Function (Application-Managed)

```sql
-- NOTE: Primary audit capture is at application layer via decorators.
-- This trigger provides database-level safety net for direct SQL operations.

CREATE OR REPLACE FUNCTION audit.audit_trigger_func()
RETURNS TRIGGER AS $$
DECLARE
    v_old_json JSONB;
    v_new_json JSONB;
    v_diff     JSONB;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_old_json = to_jsonb(OLD);
        INSERT INTO audit.audit_logs (
            event_id, entity_type, entity_id, action,
            old_values, correlation_id, timestamp
        ) VALUES (
            gen_random_uuid(),
            TG_TABLE_NAME,
            OLD.id,
            'DELETE',
            v_old_json,
            current_setting('request.correlation_id', true),
            NOW()
        );
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        v_old_json = to_jsonb(OLD);
        v_new_json = to_jsonb(NEW);
        INSERT INTO audit.audit_logs (
            event_id, entity_type, entity_id, action,
            old_values, new_values, correlation_id, timestamp
        ) VALUES (
            gen_random_uuid(),
            TG_TABLE_NAME,
            NEW.id,
            'UPDATE',
            v_old_json,
            v_new_json,
            current_setting('request.correlation_id', true),
            NOW()
        );
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        v_new_json = to_jsonb(NEW);
        INSERT INTO audit.audit_logs (
            event_id, entity_type, entity_id, action,
            new_values, correlation_id, timestamp
        ) VALUES (
            gen_random_uuid(),
            TG_TABLE_NAME,
            NEW.id,
            'CREATE',
            v_new_json,
            current_setting('request.correlation_id', true),
            NOW()
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 12.5 Audit Query Patterns

```sql
-- Get full audit history for an entity
SELECT
    al.timestamp,
    al.action,
    al.actor_id,
    u.display_name AS actor_name,
    al.old_values,
    al.new_values
FROM audit.audit_logs al
LEFT JOIN identity.users u ON al.actor_id = u.id
WHERE al.entity_type = 'Routine'
  AND al.entity_id = $1
ORDER BY al.timestamp DESC;

-- Get changes to a specific field
SELECT
    ec.timestamp,
    ec.old_value,
    ec.new_value,
    al.actor_id
FROM audit.entity_changes ec
JOIN audit.audit_logs al ON ec.audit_log_id = al.id
WHERE al.entity_type = 'Routine'
  AND al.entity_id = $1
  AND ec.field_name = 'status'
ORDER BY ec.timestamp DESC;

-- Get user action timeline
SELECT
    al.timestamp,
    al.action,
    al.entity_type,
    al.entity_id
FROM audit.audit_logs al
WHERE al.actor_id = $1
  AND al.timestamp >= NOW() - INTERVAL '30 days'
ORDER BY al.timestamp DESC;
```

---

## 13. Multi-Tenant Strategy

### 13.1 Architecture: Shared Schema with Row-Level Security

```
┌────────────────────────────────────────────────────────────────┐
│                    MULTI-TENANT ARCHITECTURE                    │
│                                                                │
│  Strategy: Shared Schema, Row-Level Security                   │
│  Isolation: Row-level + app-layer validation                   │
│  Performance: Partition + tenant_id on all queries             │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Database: eduroutine                                   │   │
│  │                                                         │   │
│  │  Schema: identity                                       │   │
│  │  ├── tenants        (tenant registry)                   │   │
│  │  ├── users          (tenant_id → RLS)                   │   │
│  │  ├── roles          (tenant_id → RLS)                   │   │
│  │  └── ...                                                │   │
│  │                                                         │   │
│  │  Schema: academic                                       │   │
│  │  ├── departments    (tenant_id → RLS)                   │   │
│  │  ├── courses        (tenant_id → RLS)                   │   │
│  │  └── ...                                                │   │
│  │                                                         │   │
│  │  Schema: timetable                                      │   │
│  │  ├── routines       (tenant_id → RLS)                   │   │
│  │  ├── routine_details (tenant_id → RLS)                  │   │
│  │  └── ...                                                │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

### 13.2 Tenant Table

```sql
CREATE TABLE identity.tenants (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(200)    NOT NULL,
    slug            VARCHAR(100)    NOT NULL,
    domain          VARCHAR(255),
    settings        JSONB           DEFAULT '{}',
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    subscription_tier VARCHAR(50)   DEFAULT 'standard',
    max_users       INTEGER         DEFAULT 1000,
    max_routines    INTEGER         DEFAULT 100,
    storage_limit_mb INTEGER        DEFAULT 1024,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_tenants_slug UNIQUE (slug),
    CONSTRAINT uq_tenants_domain UNIQUE (domain)
);

CREATE INDEX idx_tenants_active ON identity.tenants(id) WHERE is_active = TRUE;
```

### 13.3 Row-Level Security Implementation

```sql
-- Step 1: Enable RLS on all tenant-scoped tables
ALTER TABLE identity.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE academic.departments ENABLE ROW LEVEL SECURITY;
ALTER TABLE academic.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE academic.batches ENABLE ROW LEVEL SECURITY;
ALTER TABLE academic.semesters ENABLE ROW LEVEL SECURITY;
ALTER TABLE academic.courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE academic.sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE people.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE people.teachers ENABLE ROW LEVEL SECURITY;
ALTER TABLE people.teacher_availabilities ENABLE ROW LEVEL SECURITY;
ALTER TABLE resources.rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE timetable.time_slots ENABLE ROW LEVEL SECURITY;
ALTER TABLE timetable.routines ENABLE ROW LEVEL SECURITY;
ALTER TABLE timetable.routine_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE timetable.teacher_workload ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduling.constraints ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduling.generation_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduling.conflicts ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduling.teacher_preferences ENABLE ROW LEVEL SECURITY;

-- Step 2: Create tenant isolation policy (applied to all tenant-scoped tables)
CREATE POLICY p_tenant_isolation ON identity.users
    USING (tenant_id = current_setting('app.tenant_id')::UUID);

CREATE POLICY p_tenant_isolation ON academic.departments
    USING (tenant_id = current_setting('app.tenant_id')::UUID);

CREATE POLICY p_tenant_isolation ON academic.courses
    USING (tenant_id = current_setting('app.tenant_id')::UUID);

-- ... apply to all tenant-scoped tables ...

-- Step 3: Application sets tenant context at connection start
-- (FastAPI middleware)
-- SET SESSION app.tenant_id = 'tenant-uuid';
```

### 13.4 Application-Layer Tenant Resolution

```sql
-- Function to validate tenant access
CREATE OR REPLACE FUNCTION validate_tenant_access(
    p_user_id UUID,
    p_tenant_id UUID
) RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM identity.users
        WHERE id = p_user_id
          AND tenant_id = p_tenant_id
          AND status = 'active'
    );
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- Function to get user's tenant
CREATE OR REPLACE FUNCTION get_user_tenant(p_user_id UUID)
RETURNS UUID AS $$
BEGIN
    RETURN (
        SELECT tenant_id FROM identity.users
        WHERE id = p_user_id AND deleted_at IS NULL
    );
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;
```

### 13.5 Tenant-Aware Indexes

```sql
-- All tenant-scoped indexes include tenant_id as leading column
CREATE INDEX idx_users_tenant_email      ON identity.users(tenant_id, email);
CREATE INDEX idx_departments_tenant_code ON academic.departments(tenant_id, code);
CREATE INDEX idx_courses_tenant_code     ON academic.courses(tenant_id, code);
CREATE INDEX idx_routines_tenant_batch   ON timetable.routines(tenant_id, batch_id, semester_id);
CREATE INDEX idx_rd_tenant_routine       ON timetable.routine_details(tenant_id, routine_id, day_of_week);
```

---

## 14. Event Sourcing Tables

### 14.1 Event Store Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVENT STORE PATTERN                           │
│                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌─────────────────────┐   │
│  │  Aggregate  │───→│  Domain    │───→│  event_store.events │   │
│  │  (Entity)   │    │  Event     │    │  (Append-only log) │   │
│  └────────────┘    └────────────┘    └──────────┬──────────┘   │
│                                                  │              │
│                                                  │              │
│                          ┌───────────────────────┼──────────┐   │
│                          │                       │          │   │
│                          ▼                       ▼          │   │
│              ┌────────────────────┐    ┌──────────────────┐ │   │
│              │   Projection       │    │   Outbox Pattern  │ │   │
│              │   (Current State)  │    │   (Integration)   │ │   │
│              └────────────────────┘    └──────────────────┘ │   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  event_store.subscriptions — Event handler registry     │   │
│  │  event_store.outbox_messages — Reliable publishing      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 14.2 Event Store Table

```sql
CREATE TABLE event_store.events (
    id              BIGSERIAL,
    event_id        UUID            NOT NULL,
    aggregate_type  VARCHAR(100)    NOT NULL,
    aggregate_id    UUID            NOT NULL,
    event_type      VARCHAR(200)    NOT NULL,
    event_data      JSONB           NOT NULL,
    version         INTEGER         NOT NULL,
    metadata        JSONB,
    status          EventStatus     NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    PRIMARY KEY (id, created_at),
    CONSTRAINT uq_events_event_id UNIQUE (event_id),
    CONSTRAINT uq_events_aggregate_version UNIQUE (aggregate_type, aggregate_id, version)
) PARTITION BY RANGE (created_at);

-- Indexes
CREATE INDEX idx_events_aggregate     ON event_store.events(aggregate_type, aggregate_id);
CREATE INDEX idx_events_type          ON event_store.events(event_type);
CREATE INDEX idx_events_pending       ON event_store.events(id) WHERE status = 'pending';
CREATE INDEX idx_events_created       ON event_store.events USING brin(created_at)
    WITH (pages_per_range = 32);

-- Helper function: append event
CREATE OR REPLACE FUNCTION event_store.append_event(
    p_aggregate_type    VARCHAR(100),
    p_aggregate_id      UUID,
    p_event_type        VARCHAR(200),
    p_event_data        JSONB,
    p_metadata          JSONB DEFAULT NULL,
    p_expected_version  INTEGER DEFAULT NULL
) RETURNS BIGINT AS $$
DECLARE
    v_next_version  INTEGER;
    v_event_id      UUID := gen_random_uuid();
    v_new_id        BIGINT;
BEGIN
    -- Optimistic concurrency check
    IF p_expected_version IS NOT NULL THEN
        SELECT COALESCE(MAX(version), 0) + 1 INTO v_next_version
        FROM event_store.events
        WHERE aggregate_type = p_aggregate_type
          AND aggregate_id = p_aggregate_id;

        IF p_expected_version + 1 != v_next_version THEN
            RAISE EXCEPTION 'Optimistic concurrency failure for % %: expected version %, actual version %',
                p_aggregate_type, p_aggregate_id, p_expected_version, v_next_version - 1
            USING ERRCODE = 'TXXX01';
        END IF;
    ELSE
        SELECT COALESCE(MAX(version), 0) + 1 INTO v_next_version
        FROM event_store.events
        WHERE aggregate_type = p_aggregate_type
          AND aggregate_id = p_aggregate_id;
    END IF;

    INSERT INTO event_store.events (event_id, aggregate_type, aggregate_id, event_type, event_data, version, metadata)
    VALUES (v_event_id, p_aggregate_type, p_aggregate_id, p_event_type, p_event_data, v_next_version, p_metadata)
    RETURNING id INTO v_new_id;

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;
```

### 14.3 Outbox Messages Table

```sql
CREATE TABLE event_store.outbox_messages (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    message_type    VARCHAR(200)    NOT NULL,
    message_body    JSONB           NOT NULL,
    destination     VARCHAR(200),
    status          EventStatus     NOT NULL DEFAULT 'pending',
    retry_count     INTEGER         NOT NULL DEFAULT 0,
    max_retries     INTEGER         NOT NULL DEFAULT 3,
    error_message   TEXT,
    scheduled_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    processed_at    TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ
);

CREATE INDEX idx_outbox_pending    ON event_store.outbox_messages(id)
    WHERE status = 'pending' AND (scheduled_at IS NULL OR scheduled_at <= NOW())
    ORDER BY created_at ASC;
CREATE INDEX idx_outbox_status     ON event_store.outbox_messages(status);
CREATE INDEX idx_outbox_type       ON event_store.outbox_messages(message_type);
```

### 14.4 Event Subscriptions Table

```sql
CREATE TABLE event_store.subscriptions (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    subscriber_name     VARCHAR(200)    NOT NULL,
    event_type_pattern  VARCHAR(200)    NOT NULL,  -- e.g., "com.eduroutine.*" or "com.eduroutine.routine.*"
    handler_class       VARCHAR(500)    NOT NULL,  -- Python class path
    is_active           BOOLEAN         NOT NULL DEFAULT TRUE,
    last_processed_at   TIMESTAMPTZ,
    last_error_message  TEXT,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_subscriptions_name UNIQUE (subscriber_name)
);

-- Fetch pending events for subscription
CREATE OR REPLACE FUNCTION event_store.get_pending_events(
    p_subscriber_name   VARCHAR(200),
    p_batch_size        INTEGER DEFAULT 100
) RETURNS SETOF event_store.events AS $$
BEGIN
    RETURN QUERY
    SELECT e.*
    FROM event_store.events e
    WHERE e.status = 'pending'
    ORDER BY e.id ASC
    LIMIT p_batch_size
    FOR UPDATE SKIP LOCKED;
END;
$$ LANGUAGE plpgsql;
```

---

## 15. Migration Strategy

### 15.1 Alembic Configuration

```ini
# alembic.ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://user:pass@localhost:5432/eduroutine

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### 15.2 Migration Standards

| Rule | Standard |
|---|---|
| **Naming** | `{YYYYMMDD_HHMM}_{description}.py` |
| **Reversible** | Every migration must implement `upgrade()` and `downgrade()` |
| **Atomic** | One logical change per migration |
| **Data migrations** | Separate file from schema migrations |
| **Review required** | Every migration reviewed in PR |
| **No direct prod SQL** | Never modify production database directly |
| **Test before deploy** | Migrations tested in CI against fresh database |
| **Backward compatible** | Migrations must not break running application |

### 15.3 Migration Example

```python
"""add teacher_availabilities table

Revision ID: abc123def456
Revises: 789ghi012jkl
Create Date: 2026-06-18 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'abc123def456'
down_revision = '789ghi012jkl'

def upgrade():
    op.create_table(
        'teacher_availabilities',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(), nullable=False),
        sa.Column('teacher_id', postgresql.UUID(), nullable=False),
        sa.Column('day_of_week', sa.Enum('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', name='dayofweek'), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('is_preferred', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['tenant_id'], ['identity.tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['teacher_id'], ['people.teachers.id'], ondelete='CASCADE'),
        schema='people'
    )
    op.create_index('idx_ta_teacher', 'teacher_availabilities', ['teacher_id'], schema='people')
    op.create_index('idx_ta_tenant', 'teacher_availabilities', ['tenant_id'], schema='people')

def downgrade():
    op.drop_table('teacher_availabilities', schema='people')
    op.execute('DROP TYPE IF EXISTS dayofweek')
```

### 15.4 Migration Workflow

```
Development:
  alembic revision --autogenerate -m "description"
  alembic upgrade head
  # Verify changes
  alembic downgrade -1
  # Commit migration

CI Pipeline:
  alembic upgrade head          # Create fresh test DB
  pytest tests/                  # Run tests
  alembic check                  # Verify model-sync

Production:
  alembic upgrade head          # Apply pending migrations
  # Monitor for errors
  alembic current               # Verify version
```

### 15.5 Seed Data Strategy

```python
"""seed initial data

Revision ID: seed_001
Revises: abc123def456
"""

from alembic import op
from sqlalchemy import text

def upgrade():
    # Ensure schemas exist
    op.execute("CREATE SCHEMA IF NOT EXISTS identity")
    op.execute("CREATE SCHEMA IF NOT EXISTS academic")
    op.execute("CREATE SCHEMA IF NOT EXISTS people")
    op.execute("CREATE SCHEMA IF NOT EXISTS resources")
    op.execute("CREATE SCHEMA IF NOT EXISTS timetable")
    op.execute("CREATE SCHEMA IF NOT EXISTS scheduling")
    op.execute("CREATE SCHEMA IF NOT EXISTS event_store")
    op.execute("CREATE SCHEMA IF NOT EXISTS audit")
    op.execute("CREATE SCHEMA IF NOT EXISTS reporting")

    # Seed default permissions
    permissions = [
        ('user:create', 'Create User', 'user'),
        ('user:read', 'Read User', 'user'),
        ('user:update', 'Update User', 'user'),
        ('user:delete', 'Delete User', 'user'),
        ('role:create', 'Create Role', 'role'),
        ('role:read', 'Read Role', 'role'),
        ('role:update', 'Update Role', 'role'),
        ('role:delete', 'Delete Role', 'role'),
        ('course:create', 'Create Course', 'course'),
        ('course:read', 'Read Course', 'course'),
        ('course:update', 'Update Course', 'course'),
        ('course:delete', 'Delete Course', 'course'),
        ('routine:create', 'Create Routine', 'routine'),
        ('routine:read', 'Read Routine', 'routine'),
        ('routine:update', 'Update Routine', 'routine'),
        ('routine:delete', 'Delete Routine', 'routine'),
        ('routine:publish', 'Publish Routine', 'routine'),
        ('scheduling:generate', 'Generate Schedule', 'scheduling'),
        ('scheduling:validate', 'Validate Schedule', 'scheduling'),
        ('report:read', 'Read Reports', 'report'),
        ('report:export', 'Export Reports', 'report'),
        ('audit:read', 'Read Audit Logs', 'audit'),
        ('audit:export', 'Export Audit Logs', 'audit'),
    ]

    for code, name, module in permissions:
        op.execute(
            text("""
                INSERT INTO identity.permissions (code, name, module)
                VALUES (:code, :name, :module)
                ON CONFLICT (code) DO NOTHING
            """),
            {"code": code, "name": name, "module": module}
        )

def downgrade():
    op.execute("DELETE FROM identity.permissions")
```

---

## 16. Appendix: Complete DDL Script

A single executable DDL script consolidating all the above definitions is available in the companion file:
- [`eduroutine-ddl.sql`](eduroutine-ddl.sql)

This script is organized in dependency order:
1. Extensions
2. ENUM types
3. DOMAIN types
4. Schemas
5. Tables (dependency order)
6. Indexes
7. Foreign keys (separated for dependency resolution)
8. Check constraints
9. Exclusion constraints
10. Row-level security policies
11. Functions and triggers
12. Materialized views
13. Seed data

### DDL Execution Order

```bash
# Step 1: Create database (superuser)
psql -U postgres -c "CREATE DATABASE eduroutine WITH ENCODING 'UTF8' LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8' TEMPLATE template0;"

# Step 2: Install extensions (superuser)
psql -U postgres -d eduroutine -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
psql -U postgres -d eduroutine -c "CREATE EXTENSION IF NOT EXISTS \"pgcrypto\";"
psql -U postgres -d eduroutine -c "CREATE EXTENSION IF NOT EXISTS \"btree_gin\";"
psql -U postgres -d eduroutine -c "CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";"

# Step 3: Create schemas
psql -U postgres -d eduroutine -f 01_schemas.sql

# Step 4: Create types
psql -U postgres -d eduroutine -f 02_types.sql

# Step 5: Create tables
psql -U postgres -d eduroutine -f 03_tables.sql

# Step 6: Create indexes
psql -U postgres -d eduroutine -f 04_indexes.sql

# Step 7: Create constraints
psql -U postgres -d eduroutine -f 05_constraints.sql

# Step 8: Apply RLS
psql -U postgres -d eduroutine -f 06_rls.sql

# Step 9: Create functions and triggers
psql -U postgres -d eduroutine -f 07_functions.sql

# Step 10: Create materialized views
psql -U postgres -d eduroutine -f 08_views.sql

# Step 11: Seed data
psql -U postgres -d eduroutine -f 09_seed.sql
```

### Rollback Strategy

```bash
# Full database reset (development only)
psql -U postgres -d eduroutine -c "DROP SCHEMA IF EXISTS identity, academic, people, resources, timetable, scheduling, event_store, audit, reporting CASCADE;"

# Drop all tables in dependency order
psql -U postgres -d eduroutine -f rollback.sql
```

---

**End of PostgreSQL Database Architecture Document**
