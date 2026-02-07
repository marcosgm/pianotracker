"""
Authentication tests for Piano Session Tracker.
"""

import pytest


class TestRegistration:
    """Tests for user registration."""

    def test_register_page_loads(self, client):
        """Test that registration page loads."""
        response = client.get("/register")
        assert response.status_code == 200
        assert b"Create Account" in response.data

    def test_successful_registration(self, client, app):
        """Test successful user registration."""
        from src.models import User

        response = client.post(
            "/register",
            data={
                "email": "newuser@example.com",
                "password": "password123",
                "password_confirm": "password123"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Welcome, newuser@example.com" in response.data

        # Verify user was created
        with app.app_context():
            user = User.query.filter_by(email="newuser@example.com").first()
            assert user is not None

    def test_registration_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post(
            "/register",
            data={
                "email": "invalidemail",
                "password": "password123",
                "password_confirm": "password123"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"valid email" in response.data

    def test_registration_short_password(self, client):
        """Test registration with password too short."""
        response = client.post(
            "/register",
            data={
                "email": "test@example.com",
                "password": "short",
                "password_confirm": "short"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"at least 8" in response.data

    def test_registration_password_mismatch(self, client):
        """Test registration with mismatched passwords."""
        response = client.post(
            "/register",
            data={
                "email": "test@example.com",
                "password": "password123",
                "password_confirm": "different"
            },
            follow_redirects=True
        )

        assert response.status_code == 400
        assert b"not match" in response.data or b"do not match" in response.data

    def test_registration_duplicate_email(self, client, test_user):
        """Test registration with email already in use."""
        response = client.post(
            "/register",
            data={
                "email": test_user.email,
                "password": "password123",
                "password_confirm": "password123"
            },
            follow_redirects=True
        )

        assert response.status_code == 400
        assert b"already in use" in response.data


class TestLogin:
    """Tests for user login."""

    def test_login_page_loads(self, client):
        """Test that login page loads."""
        response = client.get("/login")
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_successful_login(self, client, auth, test_user):
        """Test successful user login."""
        response = auth.login()
        assert response.status_code == 200
        assert b"Welcome back" in response.data

    def test_login_invalid_email(self, client, auth):
        """Test login with non-existent email."""
        response = auth.login(email="nonexistent@example.com", password="password123", follow=False)
        assert response.status_code == 400
        assert b"Invalid email or password" in response.data

    def test_login_wrong_password(self, client, auth, test_user):
        """Test login with wrong password."""
        response = auth.login(password="wrongpassword", follow=False)
        assert response.status_code == 400
        assert b"Invalid email or password" in response.data

    def test_authenticated_user_redirect_to_dashboard(self, client, auth, test_user):
        """Test that authenticated users are redirected to dashboard from auth pages."""
        auth.login()
        
        # Accessing register/login while logged in should redirect to dashboard
        response = client.get("/register")
        assert response.status_code == 302  # Redirect

        response = client.get("/login")
        assert response.status_code == 302  # Redirect


class TestLogout:
    """Tests for user logout."""

    def test_logout_successful(self, client, auth, test_user):
        """Test successful logout."""
        auth.login()
        response = auth.logout()
        
        assert response.status_code == 200
        assert b"logged out" in response.data

    def test_logout_requires_login(self, client):
        """Test that logout requires authentication."""
        response = client.get("/logout", follow_redirects=True)
        assert b"log in first" in response.data


class TestDashboard:
    """Tests for dashboard access."""

    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires authentication."""
        response = client.get("/dashboard", follow_redirects=True)
        assert b"log in first" in response.data

    def test_dashboard_loads_for_authenticated_user(self, client, auth, test_user):
        """Test that authenticated users can access dashboard."""
        auth.login()
        response = client.get("/dashboard")
        
        assert response.status_code == 200
        assert b"Welcome" in response.data
        assert b"test@example.com" in response.data
