from datetime import datetime, timezone
from typing import List, Optional
from domain.models.todo import Todo
from domain.models.itodo_repository import ITodoRepository
from domain.exceptions import NotFoundException, ValidationException


class TodoService:
    """Service layer encapsulating business logic for Todos."""

    def __init__(self, repository: ITodoRepository):
        self.repository = repository

    def create_todo(
        self,
        title: str,
        description: Optional[str] = None,
        status: str = "pending",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> Todo:
        if not title or not title.strip():
            raise ValidationException("Title is required and cannot be empty")

        now = datetime.now(timezone.utc)
        todo = Todo(
            id=None,
            title=title.strip(),
            description=description,
            status=status,
            created_at=created_at or now,
            updated_at=updated_at or now,
        )
        return self.repository.add(todo)

    def get_todo(self, todo_id: int) -> Todo:
        todo = self.repository.get_by_id(todo_id)
        if not todo:
            raise NotFoundException(f"Todo with id {todo_id} not found")
        return todo

    def list_todos(self) -> List[Todo]:
        return self.repository.list()

    def update_todo(
        self,
        todo_id: int,
        title: str,
        description: Optional[str] = None,
        status: str = "pending",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> Todo:
        if not title or not title.strip():
            raise ValidationException("Title is required and cannot be empty")

        # Check existence
        existing = self.repository.get_by_id(todo_id)
        if not existing:
            raise NotFoundException(f"Todo with id {todo_id} not found")

        todo = Todo(
            id=todo_id,
            title=title.strip(),
            description=description,
            status=status,
            created_at=existing.created_at,
            updated_at=updated_at or datetime.now(timezone.utc),
        )
        return self.repository.update(todo)

    def delete_todo(self, todo_id: int) -> None:
        existing = self.repository.get_by_id(todo_id)
        if not existing:
            raise NotFoundException(f"Todo with id {todo_id} not found")
        self.repository.delete(todo_id)