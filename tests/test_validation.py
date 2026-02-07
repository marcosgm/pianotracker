"""
Validation tests for Piano Session Tracker.
"""

import pytest
from src.utils import (
    validate_email, validate_password, validate_practice_type,
    validate_tempo, validate_comments
)


class TestEmailValidation:
    """Tests for email validation."""

    def test_valid_email(self):
        """Test valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@example.co.uk",
            "first+last@example.com"
        ]
        for email in valid_emails:
            is_valid, error = validate_email(email)
            assert is_valid is True
            assert error is None

    def test_invalid_email_format(self):
        """Test invalid email formats."""
        invalid_emails = [
            "notanemail",
            "missing@domain",
            "@example.com",
            "user@",
            ""
        ]
        for email in invalid_emails:
            is_valid, error = validate_email(email)
            assert is_valid is False

    def test_email_max_length(self):
        """Test email exceeding max length."""
        long_email = "a" * 250 + "@example.com"
        is_valid, error = validate_email(long_email)
        assert is_valid is False


class TestPasswordValidation:
    """Tests for password validation."""

    def test_valid_password(self):
        """Test valid passwords."""
        is_valid, error = validate_password("password123", "password123")
        assert is_valid is True
        assert error is None

    def test_password_too_short(self):
        """Test password shorter than 8 characters."""
        is_valid, error = validate_password("short", "short")
        assert is_valid is False
        assert "8 characters" in error

    def test_password_mismatch(self):
        """Test mismatched passwords."""
        is_valid, error = validate_password("password123", "different")
        assert is_valid is False
        assert "not match" in error or "do not match" in error

    def test_empty_password(self):
        """Test empty password."""
        is_valid, error = validate_password("", "")
        assert is_valid is False


class TestPracticeTypeValidation:
    """Tests for practice type validation."""

    def test_valid_practice_types(self):
        """Test all valid practice types."""
        for ptype in ["Chords", "Scales", "Course", "Songs"]:
            is_valid, error = validate_practice_type(ptype)
            assert is_valid is True
            assert error is None

    def test_invalid_practice_type(self):
        """Test invalid practice type."""
        is_valid, error = validate_practice_type("InvalidType")
        assert is_valid is False

    def test_empty_practice_type(self):
        """Test empty practice type."""
        is_valid, error = validate_practice_type("")
        assert is_valid is False


class TestTempoValidation:
    """Tests for tempo validation."""

    def test_valid_tempo_for_chords(self):
        """Test valid tempos for Chords."""
        for tempo in ["40", "100", "180"]:
            is_valid, error = validate_tempo(tempo, "Chords")
            assert is_valid is True, f"Tempo {tempo} should be valid"

    def test_valid_tempo_for_scales(self):
        """Test valid tempos for Scales."""
        for tempo in ["50", "120", "180"]:
            is_valid, error = validate_tempo(tempo, "Scales")
            assert is_valid is True

    def test_no_tempo_for_course(self):
        """Test that Course doesn't require tempo."""
        is_valid, error = validate_tempo("", "Course")
        assert is_valid is True

    def test_no_tempo_for_songs(self):
        """Test that Songs doesn't require tempo."""
        is_valid, error = validate_tempo("", "Songs")
        assert is_valid is True

    def test_tempo_out_of_range_low(self):
        """Test tempo below minimum."""
        is_valid, error = validate_tempo("30", "Chords")
        assert is_valid is False
        assert "between 40 and 180" in error

    def test_tempo_out_of_range_high(self):
        """Test tempo above maximum."""
        is_valid, error = validate_tempo("200", "Chords")
        assert is_valid is False
        assert "between 40 and 180" in error

    def test_tempo_not_numeric(self):
        """Test non-numeric tempo."""
        is_valid, error = validate_tempo("abc", "Chords")
        assert is_valid is False
        assert "number" in error

    def test_missing_tempo_for_tempo_based_type(self):
        """Test missing tempo for Chords/Scales."""
        is_valid, error = validate_tempo("", "Chords")
        assert is_valid is False
        assert "required" in error


class TestCommentsValidation:
    """Tests for comments validation (comments are mandatory)."""

    def test_empty_comments_rejected(self):
        """Test that empty comments are rejected."""
        is_valid, error = validate_comments("")
        assert is_valid is False
        assert "required" in error.lower()

    def test_blank_comments_rejected(self):
        """Test that whitespace-only comments are rejected."""
        is_valid, error = validate_comments("   ")
        assert is_valid is False
        assert "required" in error.lower()

    def test_none_comments_rejected(self):
        """Test that None comments are rejected."""
        is_valid, error = validate_comments(None)
        assert is_valid is False
        assert "required" in error.lower()

    def test_valid_comments(self):
        """Test valid comments."""
        is_valid, error = validate_comments("C Major arpeggios")
        assert is_valid is True

    def test_comments_at_max_length(self):
        """Test comments at maximum length."""
        comments = "x" * 500
        is_valid, error = validate_comments(comments)
        assert is_valid is True

    def test_comments_exceeds_max_length(self):
        """Test comments exceeding maximum length."""
        comments = "x" * 501
        is_valid, error = validate_comments(comments)
        assert is_valid is False
        assert "500 characters" in error


class TestRoutineNameValidation:
    """Tests for routine name validation."""

    def test_valid_routine_name(self):
        """Test valid routine name."""
        from src.utils import validate_routine_name
        is_valid, error = validate_routine_name("Morning Scales")
        assert is_valid is True

    def test_empty_routine_name_rejected(self):
        """Test that empty name is rejected."""
        from src.utils import validate_routine_name
        is_valid, error = validate_routine_name("")
        assert is_valid is False

    def test_blank_routine_name_rejected(self):
        """Test that whitespace-only name is rejected."""
        from src.utils import validate_routine_name
        is_valid, error = validate_routine_name("   ")
        assert is_valid is False

    def test_routine_name_exceeds_max_length(self):
        """Test name over 100 characters is rejected."""
        from src.utils import validate_routine_name
        is_valid, error = validate_routine_name("x" * 101)
        assert is_valid is False
        assert "100 characters" in error
