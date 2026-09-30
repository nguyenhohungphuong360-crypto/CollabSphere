
from typing import List, Optional
from datetime import datetime, date, timezone
from typing import List, Optional, Union
from domain.models.course import Course
from domain.models.icourse_repository import ICourseRepository
from domain.exceptions import NotFoundException, ValidationException


class CourseService:
    """Service layer encapsulating business logic for Courses."""

    def __init__(self, repository: ICourseRepository):
        self.repository = repository
    def create_course(self, course_name: str, description: str, status: str, start_date, end_date, created_at, updated_at) -> Course:
        course = Course(id=None, course_name=course_name, description=description, status=status, start_date=start_date, end_date=end_date, created_at=created_at, updated_at=updated_at)

    def create_course(
        self,
        course_name: str,
        description: Optional[str] = None,
        status: str = "active",
        start_date: Optional[Union[date, datetime]] = None,
        end_date: Optional[Union[date, datetime]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> Course:
        if not course_name or not course_name.strip():
            raise ValidationException("Course name is required and cannot be empty")

        now = datetime.now(timezone.utc)
        course = Course(
            id=None,
            course_name=course_name.strip(),
            description=description,
            status=status,
            start_date=start_date,
            end_date=end_date,
            created_at=created_at or now,
            updated_at=updated_at or now,
        )
        return self.repository.add(course)
    def get_course(self, course_id: int) -> Optional[Course]:
        return self.repository.get_by_id(course_id)

    def get_course(self, course_id: int) -> Course:
        course = self.repository.get_by_id(course_id)
        if not course:
            raise NotFoundException(f"Course with id {course_id} not found")
        return course

    def list_courses(self) -> List[Course]:
        return self.repository.list()

    def update_course(self, course_id: int, course_name: str, description: str, status: str, start_date, end_date, created_at, updated_at) -> Course:
        course = Course(id=course_id, course_name=course_name, description=description, status=status, start_date=start_date, end_date=end_date, created_at=created_at, updated_at=updated_at)
    def update_course(
        self,
        course_id: int,
        course_name: str,
        description: Optional[str] = None,
        status: str = "active",
        start_date: Optional[Union[date, datetime]] = None,
        end_date: Optional[Union[date, datetime]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> Course:
        if not course_name or not course_name.strip():
            raise ValidationException("Course name is required and cannot be empty")

        existing = self.repository.get_by_id(course_id)
        if not existing:
            raise NotFoundException(f"Course with id {course_id} not found")

        course = Course(
            id=course_id,
            course_name=course_name.strip(),
            description=description,
            status=status,
            start_date=start_date if start_date is not None else existing.start_date,
            end_date=end_date if end_date is not None else existing.end_date,
            created_at=existing.created_at,
            updated_at=updated_at or datetime.now(timezone.utc),
        )
        return self.repository.update(course)

    def delete_course(self, course_id: int) -> None:
        existing = self.repository.get_by_id(course_id)
        if not existing:
            raise NotFoundException(f"Course with id {course_id} not found")
        self.repository.delete(course_id)

    