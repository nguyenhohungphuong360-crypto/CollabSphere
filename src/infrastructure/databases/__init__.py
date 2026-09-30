from infrastructure.databases.base import Base
from infrastructure.databases.database import (
    engine,
    session,
    ScopedSession,
    get_db,
    init_db,
)
from infrastructure.databases.mssql import init_mssql
from infrastructure.models import course_register_model, todo_model, user_model, course_model, consultant_model, appointment_model, program_model, feedback_model,survey_model

def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base
__all__ = [
    "Base",
    "engine",
    "session",
    "ScopedSession",
    "get_db",
    "init_db",
    "init_mssql",
]