"""
Pytest configuration and fixtures for Piano Session Tracker.
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src import create_app, db
from src.models import User, PracticeSession, PracticeRoutine


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    """Helper class for authentication in tests."""
    class Auth:
        @staticmethod
        def register(email="test@example.com", password="password123"):
            return client.post(
                "/register",
                data={"email": email, "password": password, "password_confirm": password},
                follow_redirects=True
            )

        @staticmethod
        def login(email="test@example.com", password="password123", follow=True):
            return client.post(
                "/login",
                data={"email": email, "password": password},
                follow_redirects=follow
            )

        @staticmethod
        def logout():
            return client.get("/logout", follow_redirects=True)

    return Auth()


@pytest.fixture
def test_user(app):
    """Create a test user in the database."""
    from src.utils import hash_password

    user = User(
        email="test@example.com",
        password_hash=hash_password("password123")
    )
    db.session.add(user)
    db.session.commit()
    return user
