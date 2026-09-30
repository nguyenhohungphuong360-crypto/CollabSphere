from typing import List, Optional
from domain.models.itodo_repository import ITodoRepository
from domain.models.todo import Todo
from domain.exceptions import NotFoundException
from infrastructure.models.todo_model import TodoModel
from infrastructure.databases.database import ScopedSession


class TodoRepository(ITodoRepository):
    """SQLAlchemy implementation of ITodoRepository."""

    def __init__(self, session=None):
        self._session = session or ScopedSession

    @property
    def session(self):
        return self._session

    @staticmethod
    def _to_domain(model: Optional[TodoModel]) -> Optional[Todo]:
        if not model:
            return None
        return Todo(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def add(self, todo: Todo) -> Todo:
        model = TodoModel(
            title=todo.title,
            description=todo.description,
            status=todo.status,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )
        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return self._to_domain(model)
        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        model = self.session.query(TodoModel).filter(TodoModel.id == todo_id).first()
        return self._to_domain(model)

    def list(self) -> List[Todo]:
        models = self.session.query(TodoModel).order_by(TodoModel.id.desc()).all()
        return [self._to_domain(m) for m in models]

    def update(self, todo: Todo) -> Todo:
        model = self.session.query(TodoModel).filter(TodoModel.id == todo.id).first()
        if not model:
            raise NotFoundException(f"Todo with id {todo.id} not found")

        model.title = todo.title
        model.description = todo.description
        model.status = todo.status
        if todo.updated_at:
            model.updated_at = todo.updated_at

        try:
            self.session.commit()
            self.session.refresh(model)
            return self._to_domain(model)
        except Exception:
            self.session.rollback()
            raise

    def delete(self, todo_id: int) -> None:
        model = self.session.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not model:
            raise NotFoundException(f"Todo with id {todo_id} not found")

        try:
            self.session.delete(model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
