"""Academic entities and aggregate roots."""

from src.domain.academic.entities.batch import Batch
from src.domain.academic.entities.course import Course
from src.domain.academic.entities.department import Department
from src.domain.academic.entities.section import Section
from src.domain.academic.entities.semester import Semester
from src.domain.academic.entities.session import Session

__all__ = ["Batch", "Course", "Department", "Section", "Semester", "Session"]
