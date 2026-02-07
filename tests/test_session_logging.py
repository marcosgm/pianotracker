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

    def test_log_session_with_empty_tempo_string(self, client, auth, test_user, app):
        """Test that browser-style submission with tempo='' works for non-tempo types.

        Browsers send hidden fields as empty strings, not absent keys.
        This must not cause a form validation failure.
        """
        auth.login()

        response = client.post(
            "/session/new",
            data={
                "practice_type": "Course",
                "tempo": "",
                "comments": "Regression test"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Session logged successfully" in response.data

        with app.app_context():
            session_obj = PracticeSession.query.first()
            assert session_obj is not None
            assert session_obj.practice_type == "Course"
            assert session_obj.tempo is None

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
    """Tests for named practice routines and routine-based sessions."""

    def test_session_without_routine_name_creates_no_routine(self, client, auth, test_user, app):
        """Test that logging a session without naming a routine doesn't create one."""
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
            routines = PracticeRoutine.query.all()
            assert len(routines) == 0

    def test_session_with_routine_name_creates_routine(self, client, auth, test_user, app):
        """Test that providing a routine name saves the routine."""
        auth.login()

        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major arpeggios",
                "routine_name": "Morning Scales"
            },
            follow_redirects=True
        )

        with app.app_context():
            routine = PracticeRoutine.query.first()
            assert routine is not None
            assert routine.name == "Morning Scales"
            assert routine.practice_type == "Chords"
            assert routine.tempo == 120
            assert routine.comments == "C Major arpeggios"
            assert routine.last_used_at is not None

    def test_same_routine_name_updates_existing(self, client, auth, test_user, app):
        """Test that using the same routine name updates the existing routine."""
        auth.login()

        # Create routine
        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major arpeggios",
                "routine_name": "Daily Chords"
            },
            follow_redirects=True
        )

        # Save again with same name but different data
        client.post(
            "/session/new",
            data={
                "practice_type": "Scales",
                "tempo": "100",
                "comments": "G Major scales",
                "routine_name": "Daily Chords"
            },
            follow_redirects=True
        )

        with app.app_context():
            routines = PracticeRoutine.query.all()
            assert len(routines) == 1
            assert routines[0].practice_type == "Scales"
            assert routines[0].tempo == 100
            assert routines[0].comments == "G Major scales"

    def test_different_routine_names_create_separate_routines(self, client, auth, test_user, app):
        """Test that different names create separate routines."""
        auth.login()

        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major",
                "routine_name": "Chord Practice"
            },
            follow_redirects=True
        )

        client.post(
            "/session/new",
            data={
                "practice_type": "Scales",
                "tempo": "100",
                "comments": "C Major scale",
                "routine_name": "Scale Practice"
            },
            follow_redirects=True
        )

        with app.app_context():
            routines = PracticeRoutine.query.all()
            assert len(routines) == 2

    def test_saved_routines_displayed_on_new_session_form(self, client, auth, test_user, app):
        """Test that saved routines appear on new session form."""
        auth.login()

        # Create a named routine
        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major",
                "routine_name": "My Chords"
            },
            follow_redirects=True
        )

        # View new session form
        response = client.get("/session/new")
        assert response.status_code == 200
        assert b"Saved Routines" in response.data
        assert b"My Chords" in response.data
        assert b"Chords" in response.data

    def test_use_routine_prefills_normal_session(self, client, auth, test_user, app):
        """Test that submitting pre-filled routine data creates a normal session."""
        auth.login()

        # Create routine first
        client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": "C Major arpeggios",
                "routine_name": "Arpeggio Warmup"
            },
            follow_redirects=True
        )

        # Submit session with routine's data pre-filled (different tempo)
        response = client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "130",
                "comments": "C Major arpeggios"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Session logged successfully" in response.data

        with app.app_context():
            sessions = PracticeSession.query.all()
            assert len(sessions) == 2
            latest = sessions[1]
            assert latest.practice_type == "Chords"
            assert latest.tempo == 130
            assert latest.comments == "C Major arpeggios"

    def test_use_routine_course_no_tempo(self, client, auth, test_user, app):
        """Test using pre-filled routine data for a non-tempo practice type."""
        auth.login()

        client.post(
            "/session/new",
            data={
                "practice_type": "Course",
                "comments": "Lesson 3",
                "routine_name": "Course Progress"
            },
            follow_redirects=True
        )

        # Submit with routine's pre-filled data
        response = client.post(
            "/session/new",
            data={
                "practice_type": "Course",
                "tempo": "",
                "comments": "Lesson 3"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Session logged successfully" in response.data

    def test_session_requires_comments(self, client, auth, test_user):
        """Test that a session without comments is rejected."""
        auth.login()

        response = client.post(
            "/session/new",
            data={
                "practice_type": "Chords",
                "tempo": "120",
                "comments": ""
            },
            follow_redirects=False
        )

        # Should not redirect — form re-shown
        assert response.status_code == 200
        assert b"Log a Practice Session" in response.data
