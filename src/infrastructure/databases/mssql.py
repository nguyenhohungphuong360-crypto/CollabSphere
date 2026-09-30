from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from infrastructure.databases.database import engine, session, ScopedSession, init_db
from infrastructure.databases.base import Base

# Database configuration
DATABASE_URI = Config.DATABASE_URI
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
def init_mssql(app):
    Base.metadata.create_all(bind=engine)
SessionLocal = ScopedSession

def init_mssql(app=None):
    init_db(app)

__all__ = ["engine", "session", "ScopedSession", "SessionLocal", "init_mssql", "Base"]