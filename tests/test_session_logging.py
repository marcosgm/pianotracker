"""
Session logging and routine tests for Piano Session Tracker.
"""

import pytest
from datetime import date
from src.models import PracticeSession, PracticeRoutine


class TestSessionLogging:
    """Tests for practice session logging."""

    def test_new_session_page_requires_login(self, client):
        """Test that new session page requires authentication."""
        response = client.get("/session/new", follow_redirects=True)
        assert b"log in first" in response.data

    def test_new_session_form_loads(self, client, auth, test_user):
        """Test that new session form loads for authenticated user."""
        auth.login()
        response = client.get("/session/new")
        
        assert response.status_code == 200
        assert b"Log a Practice Session" in response.data

    def test_log_chords_session_with_tempo(self, client, auth, test_user, app):
        """Test logging a Chords session with tempo."""
        auth.login()
        
        response = client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major arpeggios"
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert b"Session logged successfully" in response.data

        # Verify session was created
        with app.app_context():
            session = PracticeSession.query.first()
            assert session is not None
            assert session.practice_type == "Chords"
            assert session.tempo == 120
            assert session.comments == "C Major arpeggios"
            assert session.user_id == test_user.id

    def test_log_scales_session_with_tempo(self, client, auth, test_user, app):
        """Test logging a Scales session with tempo."""
        auth.login()
        
        response = client.post(
            "/session/new",
            data={
                "practice_type": "Scales",
                "tempo": "90",
                "comments": "C Major scale"
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert b"Session logged successfully" in response.data

    def test_log_course_session_without_tempo(self, client, auth, test_user, app):
        """Test logging a Course session without tempo."""
        auth.login()
        
        response = client.post(
            "/session/new",
            data={
                "practice_type": "Course",
                "comments": "Lesson 5 - Hand positions"
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200
        
        with app.app_context():
            session = PracticeSession.query.first()
            assert session.practice_type == "Course"
            assert session.tempo is None

    def test_log_songs_session(self, client, auth, test_user, app):
        """Test logging a Songs session."""
        auth.login()
        
        response = client.post(
            "/session/new",
            data={
                "practice_type": "Songs",
                "comments": "Moonlight Sonata 1st movement"
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200

    def test_invalid_practice_type(self, client, auth, test_user):
        """Test that invalid practice type is rejected."""
        auth.login()
        
        response = client.post(
            "/session/new",
            data={
                "practice_type": "InvalidType",
                "comments": "Test"
            },
            follow_redirects=False
        )
        
        # Form validation should prevent invalid practice type from being submitted
        assert response.status_code == 200
        # Form should still be displayed with the invalid choice
        assert b"Log a Practice Session" in response.data

    def test_tempo_out_of_range(self, client, auth, test_user):
        """Test that out-of-range tempo is rejected."""
        auth.login()
        
        response = client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "200",  # Too high
                "comments": "Test"
            },
            follow_redirects=True
        )
        
        assert response.status_code == 400
        assert b"between 40 and 180" in response.data

    def test_comments_max_length(self, client, auth, test_user):
        """Test that comments longer than 500 chars are rejected."""
        auth.login()
        
        long_comments = "x" * 501
        response = client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "100",
                "comments": long_comments
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert b"500 characters" in response.data


class TestRoutines:
    """Tests for practice routine creation and selection."""

    def test_first_session_creates_routine(self, client, auth, test_user, app):
        """Test that first session with a combination creates a routine."""
        auth.login()
        
        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major arpeggios"
            },
            follow_redirects=True
        )

        with app.app_context():
            routine = PracticeRoutine.query.first()
            assert routine is not None
            assert routine.practice_type == "Chords"
            assert routine.tempo == 120
            assert routine.comments == "C Major arpeggios"
            assert routine.last_used_at is not None

    def test_identical_session_updates_routine(self, client, auth, test_user, app):
        """Test that logging same combination updates routine's last_used_at."""
        auth.login()
        
        # Log first session
        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major arpeggios"
            },
            follow_redirects=True
        )

        with app.app_context():
            routine1 = PracticeRoutine.query.first()
            first_timestamp = routine1.last_used_at

        # Log identical session
        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major arpeggios"
            },
            follow_redirects=True
        )

        with app.app_context():
            routines = PracticeRoutine.query.all()
            assert len(routines) == 1  # Should still be only one routine
            assert routines[0].last_used_at > first_timestamp  # Updated

    def test_different_sessions_create_separate_routines(self, client, auth, test_user, app):
        """Test that different combinations create separate routines."""
        auth.login()
        
        # Log Chords session
        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major"
            },
            follow_redirects=True
        )

        # Log different Scales session
        client.post(
            "/session/new",
            data={
                "practice_type": "Scales",
                "tempo": "100",
                "comments": "C Major scale"
            },
            follow_redirects=True
        )

        with app.app_context():
            routines = PracticeRoutine.query.all()
            assert len(routines) == 2

    def test_routines_displayed_on_new_session_form(self, client, auth, test_user):
        """Test that past routines appear on new session form."""
        auth.login()
        
        # Log a session first
        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major"
            },
            follow_redirects=True
        )

        # View new session form
        response = client.get("/session/new")
        assert response.status_code == 200
        assert b"Quick Select" in response.data
        assert b"Chords" in response.data
