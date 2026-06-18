# EduRoutine — API Endpoint Catalog

> Human-readable index of every endpoint in `openapi.yaml` (API v1, base `/api/v1`).
> **Auth**: `Bearer` = JWT required; `Public` = no auth. **Perm** = required `{module}:{action}:{scope}`
> permission (Phase 7). Standards in `00-api-standards.md`.

**Totals:** 70 paths · 18 modules · 2 security schemes.
Legend — *Idmp* = idempotent · *List* = paginated/filterable/sortable collection.

---

## 1. Authentication  `/auth/*`  (Public unless noted)
| Method | Path | Operation | Auth | Success | Notes |
|---|---|---|---|---|---|
| POST | `/auth/register` | registerUser | Public | 201 | Issues tokens |
| POST | `/auth/login` | login | Public | 200 | Rate-limited 5/15min |
| POST | `/auth/refresh` | refreshToken | Public | 200 | Rotates refresh token |
| POST | `/auth/logout` | logout | Bearer | 204 | Revokes refresh + blacklists access |
| POST | `/auth/forgot-password` | forgotPassword | Public | 202 | Always 202 (no user enumeration) |
| POST | `/auth/reset-password` | resetPassword | Public | 204 | Invalidates all sessions |
| GET | `/auth/oauth/{provider}` | oauthInitiate | Public | 302 | PKCE; provider ∈ google/microsoft/facebook |
| GET | `/auth/oauth/{provider}/callback` | oauthCallback | Public | 302 | Code exchange (server-side) |
| GET | `/health` | health | Public | 200 | Liveness/readiness |

## 2. Users  `/users/*`
| Method | Path | Operation | Perm | Success | Notes |
|---|---|---|---|---|---|
| GET | `/users` | listUsers | `user:read:*` | 200 | List |
| POST | `/users` | createUser | `user:create:*` | 201 | Idempotency-Key |
| GET | `/users/me` | getCurrentUser | `user:read:own` | 200 | Self |
| PATCH | `/users/me` | updateCurrentUser | `user:update:own` | 200 | Self profile |
| PUT | `/users/me/password` | changePassword | `user:update:own` | 204 | Invalidates other sessions |
| GET | `/users/{id}` | getUser | `user:read:*` | 200 | ETag |
| PUT | `/users/{id}` | replaceUser | `user:update:*` | 200 | If-Match · Idmp |
| PATCH | `/users/{id}` | patchUser | `user:update:*` | 200 | |
| DELETE | `/users/{id}` | deactivateUser | `user:delete:*` | 204 | Soft delete · Idmp |
| GET | `/users/{id}/roles` | getUserRoles | `user:read:*` | 200 | |
| PUT | `/users/{id}/roles` | setUserRoles | `role:assign:*` | 200 | Replace · Idmp |
| GET | `/users/{id}/claims` | getUserClaims | `user:read:*` | 200 | |
| POST | `/users/{id}/claims` | addUserClaim | `user:update:*` | 201 | |
| DELETE | `/users/{id}/claims/{claimId}` | deleteUserClaim | `user:update:*` | 204 | Idmp |

## 3. Roles & Permissions  `/roles/*`, `/permissions`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/roles` | listRoles | `role:read:*` | 200 |
| POST | `/roles` | createRole | `role:create:*` | 201 |
| GET | `/roles/{id}` | getRole | `role:read:*` | 200 |
| PUT | `/roles/{id}` | updateRole | `role:update:*` | 200 |
| DELETE | `/roles/{id}` | deleteRole | `role:delete:*` | 204 |
| GET | `/roles/{id}/permissions` | getRolePermissions | `role:read:*` | 200 |
| PUT | `/roles/{id}/permissions` | setRolePermissions | `role:update:*` | 200 |
| GET | `/permissions` | listPermissions | `role:read:*` | 200 |

## 4. Claims  (nested under Users — see §2)
Claim management is exposed via `/users/{id}/claims` and `/users/{id}/claims/{claimId}`.

## 5. Sessions  `/sessions/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/sessions` | listSessions | `session:read:*` | 200 |
| POST | `/sessions` | createSession | `session:create:*` | 201 |
| GET | `/sessions/{id}` | getSession | `session:read:*` | 200 |
| PUT | `/sessions/{id}` | updateSession | `session:update:*` | 200 |
| DELETE | `/sessions/{id}` | deleteSession | `session:delete:*` | 204 |
| PATCH | `/sessions/{id}/activate` | activateSession | `session:update:*` | 200 |

## 6. Batches  `/batches/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/batches` | listBatches | `batch:read:*` | 200 |
| POST | `/batches` | createBatch | `batch:create:*` | 201 |
| GET | `/batches/{id}` | getBatch | `batch:read:*` | 200 |
| PUT | `/batches/{id}` | updateBatch | `batch:update:*` | 200 |
| DELETE | `/batches/{id}` | deleteBatch | `batch:delete:*` | 204 |
| GET | `/batches/{id}/sections` | listBatchSections | `section:read:*` | 200 |
| GET | `/batches/{id}/routines` | listBatchRoutines | `routine:read:*` | 200 |

## 7. Semesters  `/semesters/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/semesters` | listSemesters | `semester:read:*` | 200 |
| POST | `/semesters` | createSemester | `semester:create:*` | 201 |
| GET | `/semesters/{id}` | getSemester | `semester:read:*` | 200 |
| PUT | `/semesters/{id}` | updateSemester | `semester:update:*` | 200 |
| DELETE | `/semesters/{id}` | deleteSemester | `semester:delete:*` | 204 |

## 8. Sections  `/sections/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/sections` | listSections | `section:read:*` | 200 |
| POST | `/sections` | createSection | `section:create:*` | 201 |
| GET | `/sections/{id}` | getSection | `section:read:*` | 200 |
| PUT | `/sections/{id}` | updateSection | `section:update:*` | 200 |
| DELETE | `/sections/{id}` | deleteSection | `section:delete:*` | 204 |
| GET | `/sections/{id}/students` | listSectionStudents | `student:read:*` | 200 |
| PUT | `/sections/{id}/students` | assignSectionStudents | `student:update:*` | 200 |

## 9. Courses  `/courses/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/courses` | listCourses | `course:read:*` | 200 |
| POST | `/courses` | createCourse | `course:create:*` | 201 |
| GET | `/courses/{id}` | getCourse | `course:read:*` | 200 |
| PUT | `/courses/{id}` | updateCourse | `course:update:*` | 200 |
| DELETE | `/courses/{id}` | deactivateCourse | `course:delete:*` | 204 (soft) |
| GET | `/courses/{id}/prerequisites` | listCoursePrerequisites | `course:read:*` | 200 |
| POST | `/courses/{id}/prerequisites` | addCoursePrerequisite | `course:update:*` | 201 |
| DELETE | `/courses/{id}/prerequisites/{prereqId}` | deleteCoursePrerequisite | `course:update:*` | 204 |

## 10. Students  `/students/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/students` | listStudents | `student:read:*` | 200 |
| POST | `/students` | createStudent | `student:create:*` | 201 |
| POST | `/students/bulk` | bulkImportStudents | `student:create:*` | 202 |
| GET | `/students/{id}` | getStudent | `student:read:*` | 200 |
| PUT | `/students/{id}` | updateStudent | `student:update:*` | 200 |
| DELETE | `/students/{id}` | deleteStudent | `student:delete:*` | 204 (soft) |
| GET | `/students/{id}/schedule` | getStudentSchedule | `routine:read:own` | 200 |
| GET | `/students/{id}/courses` | getStudentCourses | `student:read:*` | 200 |
| POST | `/students/{id}/enroll` | enrollStudent | `student:update:*` | 200 |
| DELETE | `/students/{id}/enroll/{courseId}` | unenrollStudent | `student:update:*` | 204 |

## 11. Teachers  `/teachers/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/teachers` | listTeachers | `teacher:read:*` | 200 |
| POST | `/teachers` | createTeacher | `teacher:create:*` | 201 |
| GET | `/teachers/{id}` | getTeacher | `teacher:read:*` | 200 |
| PUT | `/teachers/{id}` | updateTeacher | `teacher:update:*` | 200 |
| DELETE | `/teachers/{id}` | deleteTeacher | `teacher:delete:*` | 204 (soft) |
| GET | `/teachers/{id}/schedule` | getTeacherSchedule | `routine:read:own` | 200 |
| GET | `/teachers/{id}/workload` | getTeacherWorkload | `teacher:read:*` | 200 |
| PUT | `/teachers/{id}/availability` | setTeacherAvailability | `teacher:update:own` | 200 |
| GET | `/teachers/{id}/specializations` | getTeacherSpecializations | `teacher:read:*` | 200 |
| POST | `/teachers/{id}/specializations` | addTeacherSpecialization | `teacher:update:*` | 201 |

## 12. Rooms  `/rooms/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/rooms` | listRooms | `room:read:*` | 200 |
| POST | `/rooms` | createRoom | `room:create:*` | 201 |
| GET | `/rooms/{id}` | getRoom | `room:read:*` | 200 |
| PUT | `/rooms/{id}` | updateRoom | `room:update:*` | 200 |
| DELETE | `/rooms/{id}` | deactivateRoom | `room:delete:*` | 204 (soft) |
| GET | `/rooms/{id}/availability` | getRoomAvailability | `room:read:*` | 200 |
| GET | `/rooms/{id}/utilization` | getRoomUtilization | `report:read:*` | 200 |

## 13. Labs  `/labs/*`  *(specialization of Rooms, room_type=lab)*
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/labs` | listLabs | `room:read:*` | 200 |
| POST | `/labs` | createLab | `room:create:*` | 201 |
| GET | `/labs/{id}` | getLab | `room:read:*` | 200 |
| PUT | `/labs/{id}` | updateLab | `room:update:*` | 200 |

## 14. Periods  `/periods/*`  *(projection over time slots)*
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/periods` | listPeriods | `room:read:*` | 200 |
| POST | `/periods` | createPeriod | `room:create:*` | 201 |
| GET | `/periods/{id}` | getPeriod | `room:read:*` | 200 |
| DELETE | `/periods/{id}` | deletePeriod | `room:delete:*` | 204 |

## 15. TimeSlots  `/time-slots/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/time-slots` | listTimeSlots | `room:read:*` | 200 |
| POST | `/time-slots` | createTimeSlot | `room:create:*` | 201 |
| GET | `/time-slots/{id}` | getTimeSlot | `room:read:*` | 200 |
| PUT | `/time-slots/{id}` | updateTimeSlot | `room:update:*` | 200 |
| DELETE | `/time-slots/{id}` | deleteTimeSlot | `room:delete:*` | 204 |

## 16. Routines  `/routines/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/routines` | listRoutines | `routine:read:*` | 200 |
| POST | `/routines` | createRoutine | `routine:create:*` | 201 |
| GET | `/routines/{id}` | getRoutine | `routine:read:*` | 200 (ETag) |
| PUT | `/routines/{id}` | updateRoutine | `routine:update:*` | 200 (If-Match) |
| DELETE | `/routines/{id}` | deleteRoutine | `routine:delete:*` | 204 |
| POST | `/routines/{id}/publish` | publishRoutine | `routine:publish:*` | 200 (Idmp) |
| POST | `/routines/{id}/archive` | archiveRoutine | `routine:update:*` | 200 (Idmp) |
| POST | `/routines/{id}/clone` | cloneRoutine | `routine:clone:*` | 201 |
| GET | `/routines/{id}/conflicts` | getRoutineConflicts | `routine:read:*` | 200 |

## 17. RoutineDetails  `/routines/{routineId}/details/*`
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/routines/{routineId}/details` | listRoutineDetails | `routine:read:*` | 200 |
| POST | `/routines/{routineId}/details` | addRoutineDetail | `routine:update:*` | 201 |
| POST | `/routines/{routineId}/details/bulk` | bulkAddRoutineDetails | `routine:update:*` | 200 |
| PUT | `/routines/{routineId}/details/{id}` | updateRoutineDetail | `routine:update:*` | 200 |
| DELETE | `/routines/{routineId}/details/{id}` | deleteRoutineDetail | `routine:update:*` | 204 |

## 18. Classes  `/classes/*`  *(read-only projection over routine details)*
| Method | Path | Operation | Perm | Success |
|---|---|---|---|---|
| GET | `/classes` | listClasses | `routine:read:own` | 200 |
| GET | `/classes/{id}` | getClass | `routine:read:own` | 200 |

---

## Query Parameter Quick Reference
All `List` endpoints accept: `page`, `page_size`, `sort`, plus resource-specific filters and (where
applicable) `q` (search) and `expand`. See `00-api-standards.md` §§8–10 and per-endpoint
parameters in `openapi.yaml`.

| Resource | Filterable | Sortable (default) | Expandable | Searchable (`q`) |
|---|---|---|---|---|
| users | is_active, role | created_at⤓, display_name, email | roles | name, email |
| roles | name | name, created_at⤓ | — | name |
| sessions | is_current | start_date⤓, name | — | — |
| batches | session_id, department_id | created_at⤓, code | session, department | — |
| semesters | session_id | number, start_date | — | — |
| sections | batch_id | name | batch | — |
| courses | department_id, is_active, credits | code, created_at⤓, credits | department, prerequisites | code, title |
| students | batch_id, section_id, status | roll_number, enrollment_date⤓ | user, batch, section | roll_number, name |
| teachers | department_id | employee_code | user, department, specializations | name, employee_code |
| rooms | room_type, building, capacity, is_active | code, capacity | — | name, code |
| labs | has_computers, capacity | code, capacity | — | — |
| time-slots | session_id, is_break, is_lab_slot | period_number | — | — |
| periods | session_id | period_number | — | — |
| routines | session_id, batch_id, semester_id, status | created_at⤓, title | details, batch, semester | title |
| routine-details | day_of_week, teacher_id, room_id, section_id | day_of_week, period_number | course, teacher, room, section | — |
| classes | session_id, batch_id, section_id, teacher_id, room_id, course_id, day_of_week | day_of_week, period_number | course, teacher, room, section | — |
| audit-logs (admin) | entity_type, entity_id, actor_id, action, timestamp | timestamp⤓ (cursor) | — | — |
