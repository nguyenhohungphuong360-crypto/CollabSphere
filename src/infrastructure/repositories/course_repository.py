from typing import List, Optional
from domain.models.icourse_repository import ICourseRepository
from domain.models.course import Course
from domain.exceptions import NotFoundException
from infrastructure.models.course_model import CourseModel
from infrastructure.databases.database import ScopedSession


class CourseRepository(ICourseRepository):
    """SQLAlchemy implementation of ICourseRepository."""

    def __init__(self, session=None):
        self._session = session or ScopedSession

    @property
    def session(self):
        return self._session

    @staticmethod
    def _to_domain(model: Optional[CourseModel]) -> Optional[Course]:
        if not model:
            return None
        return Course(
            id=model.id,
            course_name=model.course_name,
            description=model.description,
            status=model.status,
            start_date=model.start_date,
            end_date=model.end_date,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def add(self, course: Course) -> Course:
        model = CourseModel(
            course_name=course.course_name,
            description=course.description,
            status=course.status,
            start_date=course.start_date,
            end_date=course.end_date,
            created_at=course.created_at,
            updated_at=course.updated_at,
        )
        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return self._to_domain(model)
        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, course_id: int) -> Optional[Course]:
        model = self.session.query(CourseModel).filter(CourseModel.id == course_id).first()
        return self._to_domain(model)

    def list(self) -> List[Course]:
        models = self.session.query(CourseModel).order_by(CourseModel.id.desc()).all()
        return [self._to_domain(m) for m in models]

    def update(self, course: Course) -> Course:
        model = self.session.query(CourseModel).filter(CourseModel.id == course.id).first()
        if not model:
            raise NotFoundException(f"Course with id {course.id} not found")

        model.course_name = course.course_name
        model.description = course.description
        model.status = course.status
        if course.start_date is not None:
            model.start_date = course.start_date
        if course.end_date is not None:
            model.end_date = course.end_date
        if course.updated_at:
            model.updated_at = course.updated_at

        try:
            self.session.commit()
            self.session.refresh(model)
            return self._to_domain(model)
        except Exception:
            self.session.rollback()
            raise

    def delete(self, course_id: int) -> None:
        model = self.session.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not model:
            raise NotFoundException(f"Course with id {course_id} not found")

        try:
            self.session.delete(model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
