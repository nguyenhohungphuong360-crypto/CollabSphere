from typing import Optional
from datetime import datetime, date


class Course:
    """Domain model representing a Course in the business layer."""

    def __init__(
        self,
        id: Optional[int] = None,
        course_name: str = "",
        description: Optional[str] = None,
        status: str = "active",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.course_name = course_name
        self.description = description
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "course_name": self.course_name,
            "description": self.description,
            "status": self.status,
            "start_date": self.start_date.isoformat() if hasattr(self.start_date, 'isoformat') else self.start_date,
            "end_date": self.end_date.isoformat() if hasattr(self.end_date, 'isoformat') else self.end_date,
            "created_at": self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at,
            "updated_at": self.updated_at.isoformat() if hasattr(self.updated_at, 'isoformat') else self.updated_at,
        }