# Phase 8: Scheduling Engine Design

---

## 36. Scheduling Engine Design

### Engine Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEDULING ENGINE                              │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    INPUT PREPROCESSOR                    │   │
│  │  - Load course requirements                              │   │
│  │  - Load teacher availability & specializations           │   │
│  │  - Load room inventory & capacity                        │   │
│  │  - Load time slots                                       │   │
│  │  - Load hard/soft constraints                            │   │
│  │  - Build conflict graph                                  │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              CONSTRAINT VALIDATOR                        │   │
│  │  - Validates all hard constraints before scheduling      │   │
│  │  - Identifies impossible schedules early                 │   │
│  │  - Returns conflict report if infeasible                 │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    SCHEDULING STRATEGY                   │   │
│  │                                                         │   │
│  │  ┌──────────────────┐  ┌──────────────────┐            │   │
│  │  │  Graph Coloring  │  │   Backtracking   │            │   │
│  │  │  (Phase 1: Fast) │  │  (Phase 2: Refine)│            │   │
│  │  └──────────────────┘  └──────────────────┘            │   │
│  │                                                         │   │
│  │  ┌──────────────────┐  ┌──────────────────┐            │   │
│  │  │  Local Search    │  │  Optimization    │            │   │
│  │  │  (Hill Climbing) │  │  (Iterative)     │            │   │
│  │  └──────────────────┘  └──────────────────┘            │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               CONFLICT DETECTOR & RESOLVER              │   │
│  │  - Detects all conflicts (room, teacher, time)          │   │
│  │  - Classifies conflicts (hard vs soft)                  │   │
│  │  - Suggests resolutions                                 │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              QUALITY SCORER                              │   │
│  │  - Computes schedule quality metrics                    │   │
│  │  - Room utilization %, gap analysis, balance score      │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    OUTPUT FORMATTER                      │   │
│  │  - Convert to Routine + RoutineDetail entities          │   │
│  │  - Attach conflict reports                              │   │
│  │  - Attach quality metrics                               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Scheduling Process Flow

```
1. Initialize
   ├─ Load all courses requiring scheduling
   ├─ Load all available teachers with specializations
   ├─ Load all rooms with capacities and types
   ├─ Load all time slots
   └─ Load constraint definitions

2. Validate Input
   ├─ Check: every course has a qualified teacher
   ├─ Check: every course has a compatible room type
   ├─ Check: total available slots ≥ total required slots
   └─ Return early if infeasible

3. Assign Courses to Sections
   ├─ Group courses by batch/section
   ├─ Determine weekly meeting patterns
   └─ Create scheduling units (course + section + hours)

4. Phase 1: Graph Coloring (Fast)
   ├─ Build constraint graph:
   │   Vertices = scheduling units (course+section+hours)
   │   Edges = conflicts (same teacher, same room, same student)
   ├─ Assign colors (time slots) using DSATUR heuristic
   └─ Minimize number of colors used

5. Phase 2: Backtracking (Refine)
   ├─ For unassigned or conflicting units:
   │   ├─ Select most constrained unit
   │   ├─ Try each valid time slot
   │   └─ Recurse with forward checking
   └─ Return first complete valid schedule

6. Phase 3: Local Search (Optimize)
   ├─ Evaluate current schedule quality
   ├─ Apply hill-climbing moves:
   │   ├─ Swap two time slots
   │   ├─ Move a course to different time slot
   │   ├─ Exchange rooms between courses
   └─ Accept if quality improves

7. Validate Final Schedule
   ├─ Check all hard constraints
   ├─ Score all soft constraints
   ├─ Generate conflict report (if any)
   └─ Generate quality metrics

8. Persist Results
   └─ Save RoutineDetails, conflicts, generation log
```

---

## 37. Graph Coloring Design

### Problem Formulation
Schedule generation is modeled as a **graph coloring problem** where:
- **Vertices**: Each `(course, section, hours_per_week)` combination that needs a time slot
- **Colors**: Available time slots across the week
- **Edges**: Conflicts between vertices (cannot share same time slot)

### Conflict Graph Construction
An edge exists between two vertices if:
- Same **teacher** assigned to both courses
- Same **room** needed at the same time
- Same **section** (students) must attend both courses
- Same **course** meeting at different times (within same day constraint)

### DSATUR Algorithm (Saturation Degree)
```
1. Calculate degree of each vertex in conflict graph
2. Calculate saturation degree for each vertex
   (number of different colors already used by neighbors)
3. Select vertex with highest saturation degree (tie-breaker: highest degree)
4. Assign the lowest-numbered valid color to this vertex
5. Update saturation degrees
6. Repeat until all vertices colored
```

### Application to Timetabling
```python
# Pseudo-code: Graph coloring phase
def graph_coloring_schedule(courses, time_slots, teachers, rooms):
    # Build conflict graph
    graph = ConflictGraph()
    for course_a in courses:
        for course_b in courses:
            if share_teacher(course_a, course_b, teachers) or \
               share_section(course_a, course_b) or \
               share_room(course_a, course_b, rooms):
                graph.add_edge(course_a, course_b)

    # Apply DSATUR
    colors = {}  # vertex → time_slot_id
    uncolored = set(courses)

    while uncolored:
        # Find highest saturation degree vertex
        vertex = max(uncolored, key=lambda v: (saturation_degree(v, colors), degree(v)))
        # Find available time slots
        available = find_valid_slots(vertex, colors, time_slots, rooms, teachers)
        if available:
            # Assign first available (can be optimized)
            colors[vertex] = available[0]
            uncolored.remove(vertex)
        else:
            # Fall through to backtracking phase
            return partial_assignment(colors)

    return complete_schedule(colors)
```

---

## 38. Backtracking Design

### Forward-Checking Backtracking
Used when graph coloring fails to assign all vertices or when conflicts remain.

```python
# Pseudo-code: Backtracking with forward checking
def backtrack(courses, time_slots, rooms, teachers, assignment, index):
    if index == len(courses):
        return assignment  # Complete schedule found

    course = courses[index]
    # Order domains by least-constraining value heuristic
    available_slots = order_by_least_constraining(
        get_valid_slots(course, assignment, rooms, teachers)
    )

    for slot in available_slots:
        if is_consistent(course, slot, assignment, rooms, teachers):
            # Forward checking: prune future domains
            saved_domains = prune_future_domains(courses[index+1:], course, slot, assignment)
            assignment[course.id] = slot

            result = backtrack(courses, time_slots, rooms, teachers, assignment, index + 1)
            if result is not None:
                return result

            # Restore pruned domains (backtrack)
            restore_domains(saved_domains)
            del assignment[course.id]

    return None  # No valid assignment found
```

### Heuristics
| Heuristic | Type | Description |
|---|---|---|
| **MRV** (Minimum Remaining Values) | Variable ordering | Schedule most constrained course first |
| **LCV** (Least Constraining Value) | Value ordering | Try least-restrictive time slot first |
| **FC** (Forward Checking) | Constraint propagation | Eliminate incompatible future values |

---

## 39. Resource Allocation Design

### Room Allocation Strategy
```
For each scheduled (course, time_slot):
    1. Filter rooms by:
       - Compatible type (lecture/lab)
       - Sufficient capacity (>= enrollment)
       - Available at this time slot
       - Working condition (no maintenance)

    2. Score available rooms:
       - Best-fit capacity (minimize excess capacity wasted)
       - Same building as section (minimize student travel)
       - Equipment match (projector, computers, AC)

    3. Assign highest-scoring room
```

### Teacher Allocation Strategy
```
For each scheduled (course, time_slot):
    1. Filter teachers by:
       - Qualified for this course (specialization match)
       - Available at this time slot
       - Current workload + this course <= max hours
       - Not already assigned to another course at this time

    2. Score available teachers:
       - Preference for this time slot (soft constraint)
       - Preference for this course
       - Workload balance (prefer underloaded teachers)

    3. Assign highest-scoring teacher
```

### Resource Allocation Constraints Matrix
| Constraint | Hard/Soft | Description |
|---|---|---|
| Room capacity ≥ enrollment | Hard | Physical limit |
| Room type matches course | Hard | Lab courses in lab rooms |
| No double-booking | Hard | One room per time slot |
| Teacher qualification | Hard | Must be specialized |
| Teacher availability | Hard | Within available hours |
| Teacher workload ≤ max | Hard | Weekly limit |
| Teacher preference | Soft | Preferred time slots |
| Room proximity | Soft | Near section classrooms |
| Capacity efficiency | Soft | Minimize wasted seats |
| Load distribution | Soft | Even teacher workload |
| Gap minimization | Soft | Minimize free periods |

---

## 40. Conflict Detection Design

### Conflict Types
| Type | Code | Description | Severity |
|---|---|---|---|
| Teacher Time Clash | TC-001 | Same teacher at same time across sections | Critical |
| Room Double-Book | RC-001 | Same room at same time for different courses | Critical |
| Section Overlap | SC-001 | Same section (students) at same time | Critical |
| Teacher Capacity | TC-002 | Teacher assigned > max hours/week | High |
| Room Capacity | RC-002 | Course enrollment > room capacity | High |
| Room Type Mismatch | RC-003 | Lab course in non-lab room | High |
| Teacher Unqualified | TC-003 | Teacher not specialized for course | High |
| Consecutive Overload | SC-002 | Section has >3 consecutive classes | Medium |
| Travel Gap | SC-003 | Building change with <10min gap | Medium |
| Uneven Distribution | SC-004 | Courses concentrated on few days | Low |

### Conflict Detection Algorithm
```
For each routine (during validation or real-time):
    for each detail_a in routine.details:
        for each detail_b in routine.details:
            if detail_a.id == detail_b.id:
                continue

            # Same time check
            if detail_a.day == detail_b.day AND
               detail_a.time_slot == detail_b.time_slot:

                # Teacher conflict
                if detail_a.teacher_id == detail_b.teacher_id:
                    register(TC-001, detail_a, detail_b)

                # Room conflict
                if detail_a.room_id == detail_b.room_id:
                    register(RC-001, detail_a, detail_b)

                # Section conflict
                if detail_a.section_id == detail_b.section_id:
                    register(SC-001, detail_a, detail_b)

            # Cross-day checks (capacity, load)
            if detail_a.teacher_id == detail_b.teacher_id:
                check_weekly_workload(detail_a, detail_b)
```

### Real-Time Conflict Detection
- On every RoutineDetail add/update/delete
- Only re-check affected time slots (incremental)
- Return conflicts immediately to the API caller
- Visual indicators on the frontend (red = hard conflict, yellow = soft conflict)

### Conflict Report Format
```json
{
  "total_conflicts": 5,
  "critical": 2,
  "high": 1,
  "medium": 1,
  "low": 1,
  "conflicts": [
    {
      "type": "TC-001",
      "severity": "critical",
      "description": "Teacher 'Dr. Smith' assigned to two courses at Monday 10:00-10:50",
      "entries": ["detail-uuid-1", "detail-uuid-2"],
      "suggestion": "Move 'CS201' to Monday 11:00-11:50 or assign different teacher"
    }
  ],
  "quality_score": 72.5
}
```

### Generation Quality Metrics
| Metric | Formula | Target |
|---|---|---|
| Hard Conflict Free | 100 × (1 - conflicts/total_entries) | 100% |
| Room Utilization | 100 × (avg_occupancy / capacity) | 75-85% |
| Teacher Load Balance | Relative standard deviation of weekly hours | < 0.2 |
| Gap Ratio | Classes with gaps / total classes | < 0.3 |
| Preference Satisfaction | % soft constraints satisfied | > 80% |
| Overall Score | Weighted composite of above metrics | > 85% |
