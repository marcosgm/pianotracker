"""
Configuration for Piano Session Tracker application.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SESSION_COOKIE_SECURE = True  # Requires HTTPS in production
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Allow HTTP during development
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/pianotracker.db"
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing configuration."""

    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # In-memory database for tests
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://user:password@localhost/pianotracker"
    )


def get_config(env: str = None) -> Config:
    """Get configuration object based on environment."""
    if env is None:
        env = os.environ.get("FLASK_ENV", "development")

    config_mapping = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    return config_mapping.get(env, DevelopmentConfig)()
