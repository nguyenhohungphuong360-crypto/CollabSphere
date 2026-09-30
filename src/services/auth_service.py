from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from domain.models.user import User
from domain.models.iuser_repository import IUserRepository
from domain.exceptions import ValidationException, UnauthorizedException, ConflictException
from config import Config


class AuthService:
    """Service handling User Authentication and JWT Token Lifecycle."""

    def __init__(self, repository: IUserRepository):
        self.repository = repository
        self.secret_key = Config.JWT_SECRET_KEY
        self.expiration_seconds = Config.JWT_EXPIRATION_SECONDS

    def register(
        self,
        user_name: str,
        password: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        if not user_name or len(user_name.strip()) < 3:
            raise ValidationException("Username must be at least 3 characters long")
        if not password or len(password) < 6:
            raise ValidationException("Password must be at least 6 characters long")

        clean_username = user_name.strip()
        existing = self.repository.get_by_username(clean_username)
        if existing:
            raise ConflictException(f"Username '{clean_username}' is already taken")

        hashed_password = generate_password_hash(password)
        now = datetime.now(timezone.utc)
        user = User(
            id=None,
            user_name=clean_username,
            password=hashed_password,
            description=description,
            status=True,
            created_at=now,
            updated_at=now,
        )
        saved_user = self.repository.add(user)
        token = self.generate_token(saved_user)
        return {
            "token": token,
            "user": saved_user.to_dict()
        }

    def login(self, user_name: str, password: str) -> Dict[str, Any]:
        if not user_name or not password:
            raise ValidationException("Both username and password are required")

        user = self.repository.get_by_username(user_name.strip())
        if not user or not check_password_hash(user.password, password):
            raise UnauthorizedException("Invalid username or password")

        if not user.status:
            raise UnauthorizedException("User account is inactive")

        token = self.generate_token(user)
        return {
            "token": token,
            "user": user.to_dict()
        }

    def generate_token(self, user: User) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "user_name": user.user_name,
            "iat": now,
            "exp": now + timedelta(seconds=self.expiration_seconds),
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("Token has expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("Invalid authentication token")
