"""Seed demo data for all entity types (idempotent)."""

from __future__ import annotations

from datetime import date, time
from decimal import Decimal
from uuid import UUID, uuid4

from src.domain.academic.entities.batch import Batch
from src.domain.academic.entities.course import Course
from src.domain.academic.entities.department import Department
from src.domain.academic.entities.section import Section
from src.domain.academic.entities.semester import Semester
from src.domain.academic.entities.session import Session
from src.domain.people.entities.student import Student
from src.domain.people.entities.teacher import Teacher
from src.domain.resources.entities.room import Room
from src.domain.timetable.entities.period import Period
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.shared.utils.clock import utcnow

SEED_DEPARTMENTS: tuple[tuple[str, str], ...] = (
    ("Computer Science & Engineering", "CSE"),
    ("Electrical & Electronic Engineering", "EEE"),
    ("Business Administration", "BBA"),
    ("English", "ENG"),
    ("Law", "LAW"),
)

SEED_SESSIONS: tuple[tuple[str, int, int], ...] = (
    ("2024-2025", 2024, 2025),
    ("2025-2026", 2025, 2026),
)

SEED_PERIODS: tuple[tuple[str, int, int, int, int, bool], ...] = (
    ("1st Period", 1, 8, 0, 55, False),
    ("2nd Period", 2, 9, 0, 55, False),
    ("3rd Period", 3, 10, 0, 55, False),
    ("4th Period", 4, 11, 0, 55, False),
    ("Midday Break", 5, 12, 0, 40, True),
    ("5th Period", 6, 12, 45, 55, False),
    ("6th Period", 7, 13, 45, 55, False),
    ("7th Period", 8, 14, 45, 55, False),
    ("8th Period", 9, 15, 45, 55, False),
)

SEED_ROOMS: tuple[tuple[str, str, str, int, str, int, bool, bool], ...] = (
    ("CSE-101", "Lecture Hall 101", "lecture_hall", 60, "Main Building", 1, True, False),
    ("CSE-102", "Lecture Hall 102", "lecture_hall", 50, "Main Building", 1, True, False),
    ("CSE-201", "Lecture Hall 201", "lecture_hall", 45, "Main Building", 2, True, False),
    ("CSE-202", "Lecture Hall 202", "lecture_hall", 40, "Main Building", 2, True, False),
    ("LAB-01", "Computer Lab 1", "lab", 30, "Science Block", 1, True, True),
    ("LAB-02", "Computer Lab 2", "lab", 25, "Science Block", 1, True, True),
    ("EEE-101", "EEE Lecture Hall", "lecture_hall", 55, "Engineering Block", 1, True, False),
    ("EEE-LAB", "EEE Lab", "lab", 20, "Engineering Block", 1, True, True),
    ("BBA-101", "BBA Lecture Hall", "lecture_hall", 50, "Business Block", 1, True, False),
    ("ENG-101", "English Seminar Room", "seminar_room", 35, "Arts Block", 1, True, False),
    ("LAW-101", "Moot Court Hall", "seminar_room", 40, "Law Block", 1, True, False),
    ("AUDI", "Auditorium", "lecture_hall", 200, "Main Building", 1, True, False),
)

SEED_COURSES: tuple[tuple[str, str, str, float, int, int], ...] = (
    ("CSE-101", "Introduction to Programming", 3.0, 3, 0),
    ("CSE-102", "Data Structures", 3.0, 3, 0),
    ("CSE-201", "Algorithms", 3.0, 3, 0),
    ("CSE-202", "Database Systems", 3.0, 3, 0),
    ("CSE-203", "Object Oriented Programming", 3.0, 3, 0),
    ("CSE-204", "Computer Networks", 3.0, 3, 0),
    ("CSE-205", "Operating Systems", 3.0, 3, 0),
    ("CSE-301", "Software Engineering", 3.0, 3, 0),
    ("CSE-302", "Artificial Intelligence", 3.0, 3, 0),
    ("CSE-303", "Machine Learning", 3.0, 3, 0),
    ("CSE-304", "Web Development Lab", 1.5, 0, 3),
    ("CSE-305", "Database Lab", 1.5, 0, 3),
    ("EEE-101", "Basic Electrical Engineering", 3.0, 3, 0),
    ("EEE-102", "Electronic Circuits", 3.0, 3, 0),
    ("EEE-103", "Digital Logic Design", 3.0, 3, 0),
    ("EEE-104", "Electrical Machines", 3.0, 3, 0),
    ("EEE-105", "Power Systems", 3.0, 3, 0),
    ("BBA-101", "Principles of Management", 3.0, 3, 0),
    ("BBA-102", "Financial Accounting", 3.0, 3, 0),
    ("BBA-103", "Marketing Management", 3.0, 3, 0),
    ("BBA-104", "Organizational Behavior", 3.0, 3, 0),
    ("ENG-101", "English Literature", 3.0, 3, 0),
    ("ENG-102", "English Language Teaching", 3.0, 3, 0),
    ("ENG-103", "American Literature", 3.0, 3, 0),
    ("ENG-104", "Linguistics", 3.0, 3, 0),
    ("LAW-101", "Constitutional Law", 3.0, 3, 0),
    ("LAW-102", "Criminal Law", 3.0, 3, 0),
    ("LAW-103", "Contract Law", 3.0, 3, 0),
    ("LAW-104", "Jurisprudence", 3.0, 3, 0),
)

SEED_TEACHERS: tuple[tuple[str, str, str, str, str, int], ...] = (
    ("T-001", "Prof. Dr. Rahman", "rahman@eduroutine.com", "CSE", "+8801711111111", 24),
    ("T-002", "Dr. Fatima Begum", "fatima@eduroutine.com", "CSE", "+8801711111112", 20),
    ("T-003", "Prof. Dr. Hasan", "hasan@eduroutine.com", "EEE", "+8801711111113", 22),
    ("T-004", "Dr. Nusrat Jahan", "nusrat@eduroutine.com", "EEE", "+8801711111114", 18),
    ("T-005", "Prof. Kamal Hossain", "kamal@eduroutine.com", "BBA", "+8801711111115", 20),
    ("T-006", "Dr. Sharmin Akter", "sharmin@eduroutine.com", "ENG", "+8801711111116", 16),
    ("T-007", "Prof. Mahmudul Islam", "mahmudul@eduroutine.com", "LAW", "+8801711111117", 18),
    ("T-008", "Ms. Tanjina Alam", "tanjina@eduroutine.com", "CSE", "+8801711111118", 20),
)

SEED_STUDENTS: tuple[tuple[str, str, str, int], ...] = (
    ("S-2024-001", "Abdul Karim", "abdul.karim@eduroutine.com", 2024),
    ("S-2024-002", "Farzana Akhter", "farzana@eduroutine.com", 2024),
    ("S-2024-003", "Mehedi Hasan", "mehedi@eduroutine.com", 2024),
    ("S-2024-004", "Shamima Sultana", "shamima@eduroutine.com", 2024),
    ("S-2024-005", "Rafiqul Islam", "rafiqul@eduroutine.com", 2024),
    ("S-2024-006", "Nadia Rahman", "nadia@eduroutine.com", 2024),
    ("S-2024-007", "Tanvir Ahmed", "tanvir@eduroutine.com", 2024),
    ("S-2024-008", "Sadia Afrin", "sadia@eduroutine.com", 2024),
    ("S-2024-009", "Jubayer Ali", "jubayer@eduroutine.com", 2024),
    ("S-2024-010", "Taslima Begum", "taslima@eduroutine.com", 2024),
    ("S-2025-001", "Arafat Hossain", "arafat@eduroutine.com", 2025),
    ("S-2025-002", "Mim Akhter", "mim@eduroutine.com", 2025),
    ("S-2025-003", "Shakil Ahmed", "shakil@eduroutine.com", 2025),
    ("S-2025-004", "Rima Sultana", "rima@eduroutine.com", 2025),
    ("S-2025-005", "Fahim Hasan", "fahim@eduroutine.com", 2025),
    ("S-2025-006", "Jannatul Ferdous", "jannatul@eduroutine.com", 2025),
    ("S-2025-007", "Imran Hossain", "imran@eduroutine.com", 2025),
    ("S-2025-008", "Shaila Parvin", "shaila@eduroutine.com", 2025),
    ("S-2025-009", "Rashed Khan", "rashed@eduroutine.com", 2025),
    ("S-2025-010", "Maliha Tabassum", "maliha@eduroutine.com", 2025),
)

DEPARTMENT_COURSE_MAP: dict[str, list[str]] = {
    "CSE": [
        "CSE-101", "CSE-102", "CSE-201", "CSE-202", "CSE-203",
        "CSE-204", "CSE-205", "CSE-301", "CSE-302", "CSE-303",
        "CSE-304", "CSE-305",
    ],
    "EEE": ["EEE-101", "EEE-102", "EEE-103", "EEE-104", "EEE-105"],
    "BBA": ["BBA-101", "BBA-102", "BBA-103", "BBA-104"],
    "ENG": ["ENG-101", "ENG-102", "ENG-103", "ENG-104"],
    "LAW": ["LAW-101", "LAW-102", "LAW-103", "LAW-104"],
}

TEACHER_SPECIALIZATIONS: dict[str, list[str]] = {
    "T-001": ["Data Structures", "Algorithms", "Software Engineering"],
    "T-002": ["Database Systems", "Web Development", "Programming"],
    "T-003": ["Power Systems", "Electrical Machines"],
    "T-004": ["Digital Logic", "Electronic Circuits"],
    "T-005": ["Management", "Marketing"],
    "T-006": ["English Literature", "Linguistics"],
    "T-007": ["Constitutional Law", "Criminal Law"],
    "T-008": ["Computer Networks", "Operating Systems", "Programming"],
}


async def seed_data() -> None:
    """Seed demo data for all entity types (idempotent)."""
    async with SqlAlchemyUnitOfWork() as uow:
        now = utcnow()

        # ── departments ──────────────────────────────────────────────
        dept_map: dict[str, UUID] = {}
        for name, code in SEED_DEPARTMENTS:
            existing = await uow.departments.get_by_code(code)
            if existing is not None:
                dept_map[code] = existing.id
            else:
                dept = Department(id=uuid4(), name=name, code=code, created_at=now)
                await uow.departments.add(dept)
                dept_map[code] = dept.id
        await uow.commit()

        # ── sessions ─────────────────────────────────────────────────
        session_map: dict[str, UUID] = {}
        for name, start_year, end_year in SEED_SESSIONS:
            existing = await uow.sessions.list_page(limit=1, offset=0)
            if existing:
                for s in existing:
                    if s.name == name:
                        session_map[name] = s.id
                        break
            if name not in session_map:
                sess = Session(
                    id=uuid4(),
                    name=name,
                    start_date=date(start_year, 7, 1),
                    end_date=date(end_year, 6, 30),
                    is_current=(name == "2025-2026"),
                    created_at=now,
                )
                await uow.sessions.add(sess)
                session_map[name] = sess.id
        await uow.commit()

        # ── semesters ────────────────────────────────────────────────
        semesters_created = 0
        for sess_name, sess_id in session_map.items():
            sem_data = [
                (1, "Spring", date(int(sess_name[:4]), 1, 10), date(int(sess_name[:4]), 6, 20)),
                (2, "Fall", date(int(sess_name[:4]), 7, 10), date(int(sess_name[5:9]), 1, 20)),
            ]
            for num, sem_name, s_date, e_date in sem_data:
                existing_sem = await uow.semesters.get_by_session_and_number(sess_id, num)
                if existing_sem is None:
                    sem = Semester(
                        id=uuid4(),
                        session_id=sess_id,
                        name=f"{sem_name} {sess_name[:4]}",
                        number=num,
                        start_date=s_date,
                        end_date=e_date,
                        created_at=now,
                    )
                    await uow.semesters.add(sem)
                    semesters_created += 1
        await uow.commit()

        # ── batches ──────────────────────────────────────────────────
        batch_map: dict[str, UUID] = {}
        sess_2024 = session_map.get("2024-2025")
        sess_2025 = session_map.get("2025-2026")
        # Map session short names to codes
        sess_short: dict[UUID, str] = {}
        for name, sid in session_map.items():
            sess_short[sid] = name[:4]
        batch_defs = [
            (sess_2024, "CSE"), (sess_2024, "EEE"), (sess_2024, "BBA"),
            (sess_2025, "CSE"), (sess_2025, "EEE"),
        ]
        for sess_id, dept_code in batch_defs:
            if not sess_id:
                continue
            dept_id = dept_map.get(dept_code)
            if not dept_id:
                continue
            year_label = sess_short.get(sess_id, "0000")
            code = f"{dept_code}-{year_label}"
            existing = await uow.batches.get_by_code(code)
            if existing is not None:
                batch_map[f"{dept_code}_{sess_id}"] = existing.id
            else:
                batch = Batch(
                    id=uuid4(),
                    session_id=sess_id,
                    department_id=dept_id,
                    name=f"Batch {dept_code} {year_label}",
                    code=code,
                    created_at=now,
                )
                await uow.batches.add(batch)
                batch_map[f"{dept_code}_{sess_id}"] = batch.id
        await uow.commit()

        # fallback — re-fetch existing batches if map is empty
        if not batch_map:
            for sess_id in session_map.values():
                for dept_code in ("CSE", "EEE", "BBA"):
                    dept_id = dept_map.get(dept_code)
                    if not dept_id:
                        continue
                    existing = await uow.batches.list_page(limit=1, offset=0,
                                                           session_id=sess_id,
                                                           department_id=dept_id)
                    if existing:
                        batch_map[f"{dept_code}_{sess_id}"] = existing[0].id

        # ── sections ─────────────────────────────────────────────────
        for key, batch_id in batch_map.items():
            for sec_name in ("A", "B"):
                existing_sec = await uow.sections.get_by_batch_and_name(batch_id, sec_name)
                if existing_sec is None:
                    sec = Section(
                        id=uuid4(),
                        batch_id=batch_id,
                        name=sec_name,
                        max_capacity=30,
                        created_at=now,
                    )
                    await uow.sections.add(sec)
        await uow.commit()

        # ── periods ──────────────────────────────────────────────────
        for name, num, hour, minute, duration, is_break in SEED_PERIODS:
            existing = await uow.periods.get_by_number(num)
            if existing is None:
                period = Period(
                    id=uuid4(),
                    name=name,
                    period_number=num,
                    start_time=time(hour, minute),
                    end_time=time(hour + (minute + duration) // 60, (minute + duration) % 60),
                    duration_minutes=duration,
                    is_break=is_break,
                    created_at=now,
                )
                await uow.periods.add(period)
        await uow.commit()

        # ── courses ──────────────────────────────────────────────────
        course_id_map: dict[str, UUID] = {}
        for code, title, credits, lec_hours, lab_hours in SEED_COURSES:
            existing = await uow.courses.get_by_code(code)
            if existing is not None:
                course_id_map[code] = existing.id
            else:
                # determine department
                dept_code = code.split("-")[0]
                dept_id = dept_map.get(dept_code)
                if not dept_id:
                    continue
                course = Course(
                    id=uuid4(),
                    department_id=dept_id,
                    code=code,
                    title=title,
                    credits=Decimal(str(credits)),
                    lecture_hours=lec_hours,
                    lab_hours=lab_hours,
                    is_active=True,
                    created_at=now,
                )
                await uow.courses.add(course)
                course_id_map[code] = course.id
        await uow.commit()

        # ── rooms ────────────────────────────────────────────────────
        for code, name, room_type, capacity, building, floor, has_projector, has_computers in SEED_ROOMS:
            existing = await uow.rooms.get_by_code(code)
            if existing is None:
                room = Room(
                    id=uuid4(),
                    code=code,
                    name=name,
                    type=room_type,
                    capacity=capacity,
                    building=building,
                    floor=floor,
                    has_projector=has_projector,
                    has_computers=has_computers,
                    is_active=True,
                    created_at=now,
                )
                await uow.rooms.add(room)
        await uow.commit()

        # ── teachers ─────────────────────────────────────────────────
        teacher_map: dict[str, UUID] = {}
        for emp_id, name, email, dept, phone, max_hours in SEED_TEACHERS:
            existing = await uow.teachers.get_by_employee_id(emp_id)
            if existing is not None:
                teacher_map[emp_id] = existing.id
            else:
                teacher = Teacher(
                    id=uuid4(),
                    employee_id=emp_id,
                    name=name,
                    email=email,
                    department=dept,
                    phone=phone,
                    specialization=TEACHER_SPECIALIZATIONS.get(emp_id, []),
                    max_hours_per_week=max_hours,
                    is_active=True,
                    created_at=now,
                )
                await uow.teachers.add(teacher)
                teacher_map[emp_id] = teacher.id
        await uow.commit()

        # ── students ─────────────────────────────────────────────────
        # Find the first available batch with sections
        batch_id_for_students: UUID | None = None
        section_ids: list[UUID] = []
        for batch_key, bid in batch_map.items():
            sections = await uow.sections.list_for_batch(bid)
            if sections:
                batch_id_for_students = bid
                section_ids = [s.id for s in sections]
                break

        for i, (sid, name, email, year) in enumerate(SEED_STUDENTS):
            existing = await uow.students.get_by_student_id(sid)
            if existing is None and batch_id_for_students and section_ids:
                student = Student(
                    id=uuid4(),
                    student_id=sid,
                    name=name,
                    email=email,
                    batch_id=batch_id_for_students,
                    section_id=section_ids[i % len(section_ids)],
                    enrollment_year=year,
                    is_active=True,
                    created_at=now,
                )
                await uow.students.add(student)
        await uow.commit()
