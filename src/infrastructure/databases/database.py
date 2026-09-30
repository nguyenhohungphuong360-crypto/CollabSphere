import logging
import os
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config, BASE_DIR
from infrastructure.databases.base import Base

logger = logging.getLogger(__name__)


def create_database_engine():
    """Create SQLAlchemy engine with automatic fallback to SQLite if target DB is unavailable."""
    uri = Config.DATABASE_URI
    is_sqlite = uri.startswith("sqlite")
    
    engine_args = {
        "pool_pre_ping": True,
        "echo": False,
    }
    
    # SQLite specific options
    if is_sqlite:
        engine_args["connect_args"] = {"check_same_thread": False}
        return create_engine(uri, **engine_args)

    try:
        # Try creating engine with given URI
        test_engine = create_engine(uri, **engine_args)
        # Verify connection with quick ping
        with test_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"Successfully connected to database: {uri.split('@')[-1] if '@' in uri else uri}")
        return test_engine
    except Exception as e:
        logger.warning(
            f"Could not connect to configured database ({uri}): {e}. "
            f"Falling back to local SQLite database."
        )
        sqlite_fallback = f"sqlite:///{os.path.join(BASE_DIR, 'default.db')}"
        return create_engine(sqlite_fallback, connect_args={"check_same_thread": False}, pool_pre_ping=True)


# Global engine and thread-safe scoped session
engine = create_database_engine()
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ScopedSession = scoped_session(session_factory)

# For backward compatibility with modules importing `session` directly
session = ScopedSession


@contextmanager
def get_db():
    """Context manager for safe transactional database sessions."""
    db_session = ScopedSession()
    try:
        yield db_session
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        ScopedSession.remove()


def init_db(app=None):
    """Initializes database tables from Base metadata and registers session teardown."""
    # Ensure all models are imported so Base.metadata knows about them
    import infrastructure.models  # noqa: F401

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

    if app is not None:
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            ScopedSession.remove()
