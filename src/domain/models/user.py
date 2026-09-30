from typing import Optional
from datetime import datetime


class User:
    """Domain model representing a User in the business layer."""

    def __init__(
        self,
        id: Optional[int] = None,
        user_name: str = "",
        password: str = "",
        description: Optional[str] = None,
        status: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self, include_password: bool = False) -> dict:
        data = {
            "id": self.id,
            "user_name": self.user_name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
        if include_password:
            data["password"] = self.password
        return data