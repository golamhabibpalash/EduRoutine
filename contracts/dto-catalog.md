# EduRoutine — DTO Catalog

> Field-level contract for every Request/Response DTO in `openapi.yaml`.
> Naming (Phase 5 §26): Requests `{Action}{Resource}Request`; Responses `{Resource}Response`;
> collections returned as `data: [ {Resource}Response ]` inside the standard envelope.
> All request DTOs are **closed** (`additionalProperties: false`) and **immutable** (frozen).
> Partial-update (PATCH) DTOs require `minProperties: 1`. Validation legend:
> R=required, O=optional, N=nullable.

**Cross-cutting response fields**: every `*Response` UUID `id` is server-assigned; `created_at`/
`updated_at` are RFC-3339 UTC and read-only. Passwords/hashes are **never** present in any response.

---

## 1. Envelope & Shared

### SuccessEnvelope
| Field | Type | Notes |
|---|---|---|
| status | const `success` | |
| data | object / array | resource or list |
| meta | Meta | request_id, timestamp, version, [pagination] |

### Meta / Pagination
`meta`: `request_id` (uuid), `timestamp` (date-time), `version` (str), `pagination` (on lists).
`pagination`: `page, page_size, total_items?, total_pages?, has_next, has_previous, next_cursor?`.

### ErrorEnvelope
`status=error`; `error{ code, message, details?, request_id, timestamp, documentation_url? }`.
See `error-response-catalog.md`.

### FieldError
`field` (JSON path), `code`, `message`, `rejected_value?`.

### Shared enums
| Enum | Values |
|---|---|
| DayOfWeek | int 0–6 (0=Mon … 6=Sun) |
| RoomType | lecture · lab · seminar · office |
| StudentStatus | active · inactive · graduated · suspended · withdrawn |
| RoutineStatus | draft · published · archived |
| ConstraintType | hard · soft |

---

## 2. Authentication DTOs

### RegisterRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| email | string(email) | R | ≤255, lowercased, unique |
| password | string(password) | R | 12–128, complexity + breach check (Phase 6) |
| display_name | string | R | 2–200, trimmed |
| phone | string | O,N | E.164, ≤30 |

### LoginRequest
`email` R, `password` R, `device_info` O,N (≤500).

### RefreshTokenRequest — `refresh_token` R (opaque).
### ForgotPasswordRequest — `email` R.
### ResetPasswordRequest — `token` R, `new_password` R (12–128, complexity).

### AuthTokens (response)
`access_token` (JWT), `refresh_token` (opaque), `token_type=Bearer`, `expires_in=900`.

---

## 3. Users DTOs

### CreateUserRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| email | string(email) | R | ≤255, unique |
| password | string(password) | R | 12–128, complexity |
| display_name | string | R | 2–200 |
| phone | string | O,N | ≤30, E.164 |
| is_active | boolean | O | default true |
| role_ids | array<uuid> | O | each must exist (`422 REFERENCE_NOT_FOUND`) |

### ReplaceUserRequest (PUT)
`display_name` R, `phone` O,N, `is_active` R. *(email/password not replaceable here.)*

### UpdateUserRequest (PATCH) — any of `display_name`, `phone`, `is_active`; ≥1.
### UpdateProfileRequest (self) — any of `display_name`, `phone`; ≥1.
### ChangePasswordRequest — `current_password` R, `new_password` R; new ≠ current; revokes other sessions.
### SetUserRolesRequest — `role_ids` array<uuid> R (unique; full replace).

### UserResponse
`id, email, email_verified, display_name, phone?, is_active, roles[], last_login_at?, created_at, updated_at`.

---

## 4. Roles & Permissions DTOs

### CreateRoleRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| name | string | R | 2–100, `^[a-z][a-z0-9_]*$`, unique |
| description | string | O,N | ≤500 |
| permission_ids | array<uuid> | O | must exist |

### UpdateRoleRequest (PATCH/PUT) — `name?`, `description?`; ≥1. System roles (`is_system_role=true`) reject rename ⇒ `422 BUSINESS_RULE_VIOLATION`.
### SetRolePermissionsRequest — `permission_ids` array<uuid> R (unique; full replace).

### RoleResponse — `id, name, description?, is_system_role, permission_count, created_at`.
### PermissionResponse — `id, code (module:action:scope), name, module, description?`.

---

## 5. Claims DTOs

### CreateClaimRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| claim_type | string | R | 1–200 |
| claim_value | string | R | 1–500 |
Unique per `(user_id, claim_type, claim_value)` ⇒ duplicate `409 DUPLICATE_RESOURCE`.

### ClaimResponse — `id, user_id, claim_type, claim_value`.

---

## 6. Sessions DTOs

### CreateSessionRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| name | string | R | 4–100 (e.g. `2025-2026`), unique |
| start_date | date | R | |
| end_date | date | R | **> start_date** (`422`) |
| is_current | boolean | O | default false; only one current at a time |

### UpdateSessionRequest (PATCH) — `name?`, `start_date?`, `end_date?`; ≥1; date order enforced.
### SessionResponse — `id, name, start_date, end_date, is_current, created_at`.

---

## 7. Batches DTOs

### CreateBatchRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| name | string | R | 2–100 |
| code | string | R | 2–50, **unique** |
| session_id | uuid | R | must exist |
| department_id | uuid | R | must exist |

### UpdateBatchRequest (PATCH) — `name?`, `code?`; ≥1.
### BatchResponse — `id, name, code, session_id, department_id, created_at`.

---

## 8. Semesters DTOs

### CreateSemesterRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| name | string | R | 2–100 |
| number | int | R | 1–12; **unique per (session_id, number)** |
| session_id | uuid | R | must exist |
| start_date | date | R | |
| end_date | date | R | > start_date |

### UpdateSemesterRequest (PATCH) — `name?`, `number?`, `start_date?`, `end_date?`; ≥1.
### SemesterResponse — `id, name, number, session_id, start_date, end_date, created_at`.

---

## 9. Sections DTOs

### CreateSectionRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| name | string | R | 1–50; **unique per (batch_id, name)** |
| batch_id | uuid | R | must exist |
| max_capacity | int | R | 1–500 |

### UpdateSectionRequest (PATCH) — `name?`, `max_capacity?`; ≥1. Reducing below current count ⇒ `422`.
### AssignStudentsRequest — `student_ids` array<uuid> R (unique); each must belong to the section's batch (`422`); over-capacity ⇒ `422 BUSINESS_RULE_VIOLATION`.
### SectionResponse — `id, name, batch_id, max_capacity, student_count, created_at`.

---

## 10. Courses DTOs

### CreateCourseRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| code | string | R | `^[A-Z]{2,4}-\d{3}$` (e.g. `CSE-101`), **unique** |
| title | string | R | 3–200 |
| credits | number | R | 0.5–6.0, multipleOf 0.5 |
| lecture_hours | int | R | 0–20 |
| lab_hours | int | O | 0–20, default 0 |
| department_id | uuid | R | must exist |
| prerequisite_ids | array<uuid> | O | each must exist; no self/cycle (`422`) |

### UpdateCourseRequest (PATCH) — `title?`, `credits?`, `lecture_hours?`, `lab_hours?`, `is_active?`; ≥1. `code`/`department_id` immutable post-create.
### AddPrerequisiteRequest — `prerequisite_id` uuid R; rejects self & cycles (`422 BUSINESS_RULE_VIOLATION`).
### CourseResponse — `id, code, title, credits, lecture_hours, lab_hours, department_id, is_active, created_at`. `expand=department,prerequisites`.

---

## 11. Students DTOs

### CreateStudentRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| user_id | uuid | R | must exist, **unique** (1:1) |
| roll_number | string | R | 1–50, **unique** |
| registration_number | string | O,N | ≤50, unique if present |
| batch_id | uuid | R | must exist |
| section_id | uuid | O,N | must belong to batch |
| enrollment_date | date | O | default today (CURRENT_DATE) |

### UpdateStudentRequest (PATCH) — `roll_number?`, `registration_number?`, `section_id?`, `status?`; ≥1.
### BulkStudentRequest — `items` array<CreateStudentRequest> R, 1–1000. Returns BulkResult (per-item).
### EnrollStudentRequest — `course_ids` array<uuid> R, ≥1, unique; prerequisite satisfaction enforced (`422`); duplicate enrollment skipped/`409`.
### StudentResponse — `id, user_id, roll_number, registration_number?, batch_id, section_id?, enrollment_date, status`. `expand=user,batch,section`.

---

## 12. Teachers DTOs

### CreateTeacherRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| user_id | uuid | R | must exist, **unique** (1:1) |
| employee_code | string | R | 1–50, **unique** |
| designation | string | R | 2–100 |
| department_id | uuid | R | must exist |
| max_hours_per_week | int | O | 1–60, default 30 |
| specialization | array<string> | O | each ≤100 |

### UpdateTeacherRequest (PATCH) — `designation?`, `max_hours_per_week?`, `specialization?`; ≥1.
### SetAvailabilityRequest — `slots[]` R: `{ day_of_week 0–6, time_slot_id uuid, available bool }`; each `time_slot_id` must exist; unique per `(day_of_week, time_slot_id)`.
### AddSpecializationRequest — `course_id` uuid R, `preference_level` int 0–10 (default 0).
### TeacherResponse — `id, user_id, employee_code, designation, department_id, max_hours_per_week, specialization[]`. `expand=user,department,specializations`.
### SpecializationResponse — `course_id, preference_level`.
### WorkloadResponse — `teacher_id, max_hours_per_week, assigned_hours_per_week, utilization_percent, courses_count`.

---

## 13. Rooms & Labs DTOs

### CreateRoomRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| name | string | R | 1–100 |
| code | string | R | 1–50, **unique** |
| building | string | R | 1–100 |
| floor | int | R | −5–200 |
| capacity | int | R | 1–1000 |
| room_type | RoomType | R | lecture/lab/seminar/office |
| has_projector | bool | O | default false |
| has_computers | bool | O | default false |
| has_ac | bool | O | default true |

### CreateLabRequest — same as CreateRoomRequest **minus `room_type`** (server forces `lab`); `has_computers` defaults true.
### UpdateRoomRequest (PATCH; also Labs) — `name?, building?, floor?, capacity?, has_projector?, has_computers?, has_ac?, is_active?`; ≥1. `code` and `room_type` immutable.
### RoomResponse — `id, name, code, building, floor, capacity, room_type, has_projector, has_computers, has_ac, is_active, created_at`.

---

## 14. Periods & TimeSlots DTOs

### CreatePeriodRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| name | string | R | 1–100 |
| period_number | int | R | 1–30 |
| session_id | uuid | O,N | must exist if present |

### PeriodResponse — `id, name, period_number, session_id?`.

### CreateTimeSlotRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| name | string | R | 1–100 |
| period_number | int | R | 1–30; **unique per (period_number, session_id)** |
| start_time | string | R | `HH:MM` 24h |
| end_time | string | R | `HH:MM`, **> start_time** (`422`) |
| duration_minutes | int | R | 5–480; should equal end−start (`422` if mismatch) |
| is_break | bool | O | default false |
| is_lab_slot | bool | O | default false |
| session_id | uuid | O,N | |

### UpdateTimeSlotRequest (PATCH) — `name?, start_time?, end_time?, duration_minutes?, is_break?, is_lab_slot?`; ≥1.
### TimeSlotResponse — `id, name, period_number, start_time, end_time, duration_minutes, is_break, is_lab_slot, session_id?`.

---

## 15. Routines DTOs

### CreateRoutineRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| title | string | R | 2–200 |
| description | string | O,N | ≤2000 |
| session_id | uuid | R | must exist |
| batch_id | uuid | R | must exist; belongs to session |
| semester_id | uuid | O,N | belongs to session |
| valid_from | date | R | |
| valid_to | date | R | > valid_from (`422`) |

Created in `draft` status.

### UpdateRoutineRequest (PATCH) — `title?, description?, semester_id?, valid_from?, valid_to?`; ≥1. Editing a `published` routine ⇒ `409 STATE_CONFLICT` (archive/clone instead).
### CloneRoutineRequest — `target_session_id` R; `target_semester_id?`, `target_batch_id?`, `new_title?`. Produces a new `draft`.
### RoutineResponse — `id, title, description?, session_id, batch_id, semester_id?, status, valid_from, valid_to, created_by?, details[]?, created_at, updated_at`. `details` only with `expand=details`.

---

## 16. RoutineDetails DTOs

### CreateRoutineDetailRequest
| Field | Type | Req | Rules |
|---|---|---|---|
| day_of_week | DayOfWeek | R | 0–6 |
| time_slot_id | uuid | R | must exist; not a break slot (`422`) |
| period_number | int | R | 1–30; must match time slot (`422`) |
| course_id | uuid | R | must exist |
| teacher_id | uuid | R | must exist; specialized for course (soft); within max load (soft) |
| room_id | uuid | R | must exist; capacity ≥ section size (soft); lab course ⇒ lab room (`422`) |
| section_id | uuid | O,N | belongs to routine batch |
| is_lab | bool | O | default false |
| group_name | string | O,N | ≤50 (combined classes) |

**Hard conflict constraints (`409 SCHEDULE_CONFLICT`)** — mirror DB unique constraints:
- Unique `(routine_id, day_of_week, period_number, room_id)` — room double-book.
- Unique `(routine_id, day_of_week, time_slot_id, teacher_id)` — teacher double-book.
- Section double-book on `(routine_id, day_of_week, period_number, section_id)`.

### UpdateRoutineDetailRequest (PATCH) — any subset of create fields; ≥1; same conflict checks.
### BulkRoutineDetailRequest — `items` array<CreateRoutineDetailRequest> R, 1–1000. `?atomic=true` ⇒ all-or-nothing; else per-item BulkResult.
### RoutineDetailResponse — full entry: `id, routine_id, day_of_week, time_slot_id, period_number, course_id, teacher_id, room_id, section_id?, is_lab, group_name?`.

---

## 17. Classes (projection) DTOs

### ClassResponse (read-only)
`id` (=routine_detail id), `routine_id`, `day_of_week`, `period_number`, `start_time`, `end_time`,
`course{ id, code, title }`, `teacher{ id, name }`, `room{ id, name }`, `section{ id, name }`, `is_lab`.
No request DTO — Classes is derived/read-only.

---

## 18. Shared Projection / Operation DTOs

| DTO | Shape |
|---|---|
| ScheduleResponse | `owner_type(student\|teacher), owner_id, session_id?, classes[ClassResponse]` |
| AvailabilityResponse | `resource_type(room\|teacher), resource_id, slots[{day_of_week, time_slot_id, available}]` |
| UtilizationResponse | `resource_id, total_slots, used_slots, utilization_percent` |
| ConflictReportResponse | `routine_id, conflict_count, conflicts[{conflict_type, day_of_week, period_number, detail_ids[]}]` |
| BulkResult | `total, succeeded, failed, results[BulkItemResult]` |
| BulkItemResult | `index, status(created\|updated\|skipped\|failed), id?, error?` |

---

## DTO Index (Request → Response)
| Module | Request DTOs | Response DTO(s) |
|---|---|---|
| Auth | Register, Login, RefreshToken, ForgotPassword, ResetPassword | AuthTokens |
| Users | CreateUser, ReplaceUser, UpdateUser, UpdateProfile, ChangePassword, SetUserRoles | UserResponse |
| Roles | CreateRole, UpdateRole, SetRolePermissions | RoleResponse, PermissionResponse |
| Claims | CreateClaim | ClaimResponse |
| Sessions | CreateSession, UpdateSession | SessionResponse |
| Batches | CreateBatch, UpdateBatch | BatchResponse |
| Semesters | CreateSemester, UpdateSemester | SemesterResponse |
| Sections | CreateSection, UpdateSection, AssignStudents | SectionResponse |
| Courses | CreateCourse, UpdateCourse, AddPrerequisite | CourseResponse |
| Students | CreateStudent, UpdateStudent, BulkStudent, EnrollStudent | StudentResponse, BulkResult |
| Teachers | CreateTeacher, UpdateTeacher, SetAvailability, AddSpecialization | TeacherResponse, Workload, Specialization, Availability |
| Rooms | CreateRoom, UpdateRoom | RoomResponse |
| Labs | CreateLab, (UpdateRoom) | RoomResponse |
| Periods | CreatePeriod | PeriodResponse |
| TimeSlots | CreateTimeSlot, UpdateTimeSlot | TimeSlotResponse |
| Routines | CreateRoutine, UpdateRoutine, CloneRoutine | RoutineResponse, ConflictReport |
| RoutineDetails | CreateRoutineDetail, UpdateRoutineDetail, BulkRoutineDetail | RoutineDetailResponse, BulkResult |
| Classes | — | ClassResponse, ScheduleResponse |
