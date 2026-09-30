from typing import List, Optional
from domain.models.user import User
from domain.models.iuser_repository import IUserRepository
from domain.exceptions import NotFoundException, ValidationException
from werkzeug.security import generate_password_hash


class UserService:
    """Service layer encapsulating business logic for User profile operations."""

    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return user

    def get_by_username(self, username: str) -> User:
        user = self.repository.get_by_username(username)
        if not user:
            raise NotFoundException(f"User with username '{username}' not found")
        return user

    def list_users(self) -> List[User]:
        return self.repository.list()

    def update_user(
        self,
        user_id: int,
        user_name: Optional[str] = None,
        password: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[bool] = None
    ) -> User:
        user = self.get_user(user_id)
        if user_name is not None:
            if not user_name.strip():
                raise ValidationException("Username cannot be empty")
            user.user_name = user_name.strip()
        if password is not None:
            if len(password) < 6:
                raise ValidationException("Password must be at least 6 characters")
            user.password = generate_password_hash(password)
        if description is not None:
            user.description = description
        if status is not None:
            user.status = status

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        self.get_user(user_id)  # verifies existence
        self.repository.delete(user_id)
