# Configuration settings for the Flask application
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

DEFAULT_SQLITE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'default.db')}"


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'collabsphere_clean_arch_secret_key_2026')
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1']
    TESTING = os.environ.get('TESTING', 'False').lower() in ['true', '1']
    DATABASE_URI = os.environ.get('DATABASE_URI') or DEFAULT_SQLITE_URI
    CORS_HEADERS = 'Content-Type'

    # JWT Settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_EXPIRATION_SECONDS = int(os.environ.get('JWT_EXPIRATION_SECONDS', 86400))  # 24 hours


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URI = os.environ.get('DATABASE_URI') or DEFAULT_SQLITE_URI


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or f"sqlite:///{os.path.join(BASE_DIR, 'test.db')}"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI') or DEFAULT_SQLITE_URI


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}