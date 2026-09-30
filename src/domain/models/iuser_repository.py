from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.user import User


class IUserRepository(ABC):
    """Interface for User Repository defining contract for data access."""

    @abstractmethod
    def add(self, user: User) -> User:
        """Add a new user entity."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their primary key id."""
        pass

    @abstractmethod
    def get_by_username(self, user_name: str) -> Optional[User]:
        """Retrieve a user by their unique username."""
        pass

    @abstractmethod
    def list(self) -> List[User]:
        """Retrieve all users."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user entity."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        """Delete a user entity by id."""
        pass
