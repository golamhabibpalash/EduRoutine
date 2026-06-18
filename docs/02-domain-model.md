# Phase 2: Domain Model & DDD Design

---

## 6. Complete Domain Model

### Core Domain Overview
The EduRoutine domain is organized around five primary business capabilities: **Identity & Access**, **Academic Structure**, **People Management**, **Resource Management**, and **Timetable Scheduling**.

```
┌─────────────────────────────────────────────────────────┐
│                    EduRoutine Domain                      │
├─────────────────────────────────────────────────────────┤
│  Identity       Academic       People      Resources    │
│  ┌──────────┐  ┌──────────┐  ┌──────┐  ┌────────────┐ │
│  │  User    │  │ Session  │  │Student│  │   Room     │ │
│  │  Role    │  │  Batch   │  │Teacher│  │   Lab      │ │
│  │  Claim   │  │ Semester │  │      │  │ Equipment  │ │
│  │Permission│  │ Course   │  │      │  │            │ │
│  └──────────┘  │ Section  │  └──────┘  └────────────┘ │
│                 └──────────┘                            │
│                      ↕                                  │
│              ┌────────────────┐                         │
│              │   Routine      │                         │
│              │  Scheduling    │  ← Core Subdomain       │
│              │   Engine       │                         │
│              └────────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

---

## 7. Bounded Contexts

| Bounded Context | Core/Supporting/Generic | Description |
|---|---|---|
| **Identity & Access** | Generic | User authentication, authorization, role management. Supports standard IAM patterns. |
| **Academic Structure** | Supporting | Defines the organizational hierarchy — sessions, batches, semesters, courses. |
| **People Management** | Supporting | Manages student and teacher profiles, assignments, specializations. |
| **Resource Management** | Supporting | Room, lab, and equipment inventory. Availability tracking and allocation. |
| **Timetable Scheduling** | **Core** | The heart of the system. Constraint-based timetable generation, conflict detection, optimization. |
| **Reporting** | Supporting | Schedule views, utilization stats, conflict reports. |
| **Audit** | Supporting | Immutable event log for all state-changing operations. |

### Context Map
```
Identity & Access ──→ Timetable Scheduling ──→ Reporting
       │                      │                      │
       │                      │                      │
       ↓                      ↓                      ↓
  Academic Structure ←── People Management ──→ Resource Management
                                                      │
                                                      ↓
                                                  Audit
```

---

## 8. DDD Design — Ubiquitous Language

| Term | Definition |
|---|---|
| **Routine** | A complete timetable for a given academic session/semester |
| **TimeSlot** | A defined time interval (e.g., 10:00–10:50) within a day |
| **Period** | An ordered position in the daily schedule (1st period, 2nd period, etc.) |
| **RoutineDetail** | A single entry mapping a course, teacher, room, and time slot |
| **Conflict** | Any overlap in resource (room, teacher) or time across RoutineDetails |
| **Session** | An academic year (e.g., 2025–2026) |
| **Batch** | A cohort of students admitted in the same session |
| **Section** | A subdivision of a batch for scheduling purposes |
| **Constraint** | A rule that governs the validity of a schedule (hard or soft) |
| **Allocation** | The assignment of a resource (teacher, room) to a time slot |

---

## 9. Aggregate Roots

| Aggregate Root | Bounded Context | Primary Identifier |
|---|---|---|
| **User** | Identity & Access | UserID (UUID) |
| **Role** | Identity & Access | RoleID (UUID) |
| **Session** | Academic Structure | SessionID (UUID) |
| **Batch** | Academic Structure | BatchID (UUID) |
| **Course** | Academic Structure | CourseID (UUID) |
| **Student** | People Management | StudentID (UUID) |
| **Teacher** | People Management | TeacherID (UUID) |
| **Room** | Resource Management | RoomID (UUID) |
| **Routine** | Timetable Scheduling | RoutineID (UUID) |
| **RoutineDetail** | Timetable Scheduling | RoutineDetailID (UUID) |

### Aggregate Design Rules
1. All aggregates are accessed via their repository interface
2. Cross-aggregate references use foreign identities (UUID), not object references
3. Aggregates enforce their own invariants
4. Changes to an aggregate are transactional and atomic
5. Eventual consistency is used for cross-aggregate operations via domain events

---

## 10. Entities

### User (Identity & Access)
- UserID (UUID), Email, PasswordHash, DisplayName, IsActive
- CreatedAt, UpdatedAt, LastLoginAt
- Collection of UserRoles
- Collection of UserClaims

### Role (Identity & Access)
- RoleID (UUID), Name, Description, IsSystemRole
- Collection of RolePermissions

### Session (Academic Structure)
- SessionID (UUID), Name (e.g., "2025-2026"), StartDate, EndDate
- IsCurrent (boolean)

### Batch (Academic Structure)
- BatchID (UUID), Name (e.g., "CSE-2025"), Code
- SessionID (FK), DepartmentID (FK)

### Semester (Academic Structure)
- SemesterID (UUID), Name (e.g., "Fall 2025"), Number (1-8)
- StartDate, EndDate
- SessionID (FK)

### Section (Academic Structure)
- SectionID (UUID), Name (e.g., "A", "B")
- BatchID (FK)
- MaxCapacity

### Course (Academic Structure)
- CourseID (UUID), Code (e.g., "CSE-101"), Title, Credits, LectureHours, LabHours
- DepartmentID (FK)
- Collection of prerequisite courses

### Student (People Management)
- StudentID (UUID), UserID (FK), RollNumber, RegistrationNumber
- BatchID (FK), SectionID (FK)
- EnrollmentDate

### Teacher (People Management)
- TeacherID (UUID), UserID (FK), EmployeeCode, Designation, MaxHoursPerWeek
- DepartmentID (FK)
- Collection of TeacherCourseSpecializations

### Room (Resource Management)
- RoomID (UUID), Name, Code, Building, Floor, Capacity, RoomType (Lecture/Lab/Seminar)
- Available equipment flags

### Routine (Timetable Scheduling)
- RoutineID (UUID), Title, Description
- SessionID (FK), BatchID (FK), SemesterID (FK)
- Status (Draft/Published/Archived)
- ValidFrom, ValidTo
- Collection of RoutineDetails

### RoutineDetail (Timetable Scheduling)
- RoutineDetailID (UUID), RoutineID (FK)
- DayOfWeek (Monday–Friday/Saturday)
- TimeSlotID (FK), PeriodNumber
- CourseID (FK), TeacherID (FK), RoomID (FK)
- SectionID (FK)
- IsLab, GroupName (for combined classes)

### TimeSlot (Timetable Scheduling)
- TimeSlotID (UUID), Name (e.g., "1st Period"), StartTime, EndTime, DurationMinutes
- IsBreak, IsLabSlot

### AuditLog (Audit)
- AuditLogID (UUID), EntityType, EntityID, Action (Create/Update/Delete)
- OldValues (JSON), NewValues (JSON)
- ActorUserID, ActorIP, Timestamp

---

## 11. Value Objects

| Value Object | Properties | Used By |
|---|---|---|
| **EmailAddress** | Value (string, validated) | User |
| **PasswordHash** | Hash, Salt, Algorithm | User |
| **PhoneNumber** | CountryCode, Number | User, Student, Teacher |
| **Address** | Street, City, State, Country, PostalCode | Institution |
| **DayOfWeek** | Value (enum: Mon–Sun) | RoutineDetail, TimeSlot |
| **TimeRange** | StartTime, EndTime | TimeSlot |
| **Duration** | Hours, Minutes | Course, TimeSlot |
| **Capacity** | TotalSeats, AvailableSeats | Room |
| **CreditHours** | Lecture, Lab, Total | Course |
| **Constraint** | Type, Priority, Expression | Scheduling Engine |
| **AllocationResult** | Success, Conflicts[], Score | Scheduling Engine |
| **AuditMetadata** | CreatedBy, CreatedAt, UpdatedBy, UpdatedAt | All Entities |

### Value Object Characteristics
- Immutable — once created, cannot be modified
- No identity — compared by structural equality
- Self-validating — validate on construction
- Expressed as dataclasses (Python) or frozen data structures
