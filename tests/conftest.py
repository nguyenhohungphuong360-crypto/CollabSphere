import pytest
import sys
import os
from sqlalchemy import text

# Add src directory to python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from create_app import create_app
from config import Config
from infrastructure.databases.database import ScopedSession, Base, engine
import infrastructure.models  # noqa - ensure all models are imported/registered


@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask app for testing (reuses shared engine)."""
    test_app = create_app(Config)
    test_app.config['TESTING'] = True

    with test_app.app_context():
        # Ensure all tables exist
        Base.metadata.create_all(bind=engine)
        yield test_app


@pytest.fixture
def client(app):
    """Test client fixture for HTTP requests."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Truncate all tables before each test for isolation."""
    # Clean before test
    with app.app_context():
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM flask_user"))
            conn.execute(text("DELETE FROM todos"))
            conn.execute(text("DELETE FROM courses"))
            conn.execute(text("DELETE FROM course_register"))
            conn.execute(text("DELETE FROM feedbacks"))
            conn.execute(text("DELETE FROM appointments"))
            conn.execute(text("DELETE FROM consultants"))
            conn.execute(text("DELETE FROM programs"))
            conn.execute(text("DELETE FROM surveys"))
            conn.commit()
        ScopedSession.remove()

    yield

    # Clean after test too
    with app.app_context():
        ScopedSession.remove()
