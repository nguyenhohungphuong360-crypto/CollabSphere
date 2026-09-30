"""Dependency Injection Container
Provides decoupled factory and singleton providers for repositories and domain services.
"""

from infrastructure.databases.database import ScopedSession
from infrastructure.repositories.todo_repository import TodoRepository
from infrastructure.repositories.course_repository import CourseRepository
from infrastructure.repositories.user_repository import UserRepository
from services.todo_service import TodoService
from services.course_service import CourseService
from services.user_service import UserService
from services.auth_service import AuthService


class Container:
    """Service and Repository Dependency Container."""

    def __init__(self, session=None):
        self._session = session or ScopedSession
        # Repositories
        self.todo_repository = TodoRepository(self._session)
        self.course_repository = CourseRepository(self._session)
        self.user_repository = UserRepository(self._session)

        # Services
        self.todo_service = TodoService(self.todo_repository)
        self.course_service = CourseService(self.course_repository)
        self.user_service = UserService(self.user_repository)
        self.auth_service = AuthService(self.user_repository)


# Global default container instance
container = Container()