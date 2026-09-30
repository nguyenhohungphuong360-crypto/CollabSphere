from typing import List, Optional
from domain.models.iuser_repository import IUserRepository
from domain.models.user import User
from domain.exceptions import NotFoundException, ConflictException
from infrastructure.models.user_model import UserModel
from infrastructure.databases.database import ScopedSession
from sqlalchemy.exc import IntegrityError


class UserRepository(IUserRepository):
    """SQLAlchemy implementation of IUserRepository."""

    def __init__(self, session=None):
        self._session = session or ScopedSession

    @property
    def session(self):
        return self._session

    @staticmethod
    def _to_domain(model: Optional[UserModel]) -> Optional[User]:
        if not model:
            return None
        return User(
            id=model.id,
            user_name=model.user_name,
            password=model.password,
            description=model.description,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def add(self, user: User) -> User:
        model = UserModel(
            user_name=user.user_name,
            password=user.password,
            description=user.description,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return self._to_domain(model)
        except IntegrityError:
            self.session.rollback()
            raise ConflictException(f"Username '{user.user_name}' already exists")
        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, user_id: int) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(model)

    def get_by_username(self, user_name: str) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.user_name == user_name).first()
        return self._to_domain(model)

    def list(self) -> List[User]:
        models = self.session.query(UserModel).order_by(UserModel.id.asc()).all()
        return [self._to_domain(m) for m in models]

    def update(self, user: User) -> User:
        model = self.session.query(UserModel).filter(UserModel.id == user.id).first()
        if not model:
            raise NotFoundException(f"User with id {user.id} not found")

        model.user_name = user.user_name
        if user.password:
            model.password = user.password
        model.description = user.description
        model.status = user.status
        if user.updated_at:
            model.updated_at = user.updated_at

        try:
            self.session.commit()
            self.session.refresh(model)
            return self._to_domain(model)
        except IntegrityError:
            self.session.rollback()
            raise ConflictException(f"Username '{user.user_name}' already exists")
        except Exception:
            self.session.rollback()
            raise

    def delete(self, user_id: int) -> None:
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not model:
            raise NotFoundException(f"User with id {user_id} not found")

        try:
            self.session.delete(model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise