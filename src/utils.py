"""
Utility functions for validation, password hashing, and routine management.
"""

import re
from typing import Optional, Tuple
from datetime import datetime, time, date
from werkzeug.security import generate_password_hash, check_password_hash
from src import db
from src.models import PracticeRoutine


# Email validation pattern
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Valid practice types
VALID_PRACTICE_TYPES = {"Chords", "Scales", "Course", "Songs"}


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format.

    Returns:
        (is_valid, error_message)
    """
    if not email or len(email) > 255:
        return False, "Email is required and must be less than 255 characters"

    if not re.match(EMAIL_REGEX, email):
        return False, "Please enter a valid email address"

    return True, None


def validate_password(password: str, confirm_password: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength.

    Returns:
        (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if confirm_password is not None and password != confirm_password:
        return False, "Passwords do not match"

    return True, None


def validate_practice_type(practice_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate practice type.

    Returns:
        (is_valid, error_message)
    """
    if not practice_type:
        return False, "Please select a practice type"

    if practice_type not in VALID_PRACTICE_TYPES:
        return False, "Invalid practice type"

    return True, None


def validate_tempo(tempo: Optional[str], practice_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate tempo for practice type.

    Args:
        tempo: String value from form (may be empty)
        practice_type: One of VALID_PRACTICE_TYPES

    Returns:
        (is_valid, error_message)
    """
    # Tempo not required for Course and Songs
    if practice_type in {"Course", "Songs"}:
        return True, None

    # Tempo required for Chords and Scales
    if not tempo:
        return False, "Tempo is required for Chords and Scales"

    try:
        tempo_int = int(tempo)
    except (ValueError, TypeError):
        return False, "Tempo must be a number"

    if tempo_int < 40 or tempo_int > 180:
        return False, "Tempo must be between 40 and 180 BPM"

    return True, None


def validate_comments(comments: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate session comments (mandatory).

    Returns:
        (is_valid, error_message)
    """
    if not comments or not comments.strip():
        return False, "Comments are required"

    if len(comments) > 500:
        return False, "Comments must be 500 characters or less"

    return True, None


def validate_routine_name(name: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate routine name (when provided).

    Returns:
        (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Routine name is required"

    if len(name) > 100:
        return False, "Routine name must be 100 characters or less"

    return True, None


def hash_password(password: str) -> str:
    """Hash a password using werkzeug.security."""
    return generate_password_hash(password, method="pbkdf2:sha256")


def check_password(password_hash: str, password: str) -> bool:
    """Check a password against its hash."""
    return check_password_hash(password_hash, password)


def create_or_update_routine(
    user_id: int, name: str, practice_type: str, tempo: Optional[int], comments: str
) -> PracticeRoutine:
    """
    Create a new named routine or update an existing one.

    Args:
        user_id: User ID
        name: User-chosen routine name
        practice_type: Type of practice (Chords, Scales, Course, Songs)
        tempo: Optional default tempo (40-180 for Chords/Scales, None for others)
        comments: Practice description

    Returns:
        PracticeRoutine instance (newly created or updated)
    """
    # Find existing routine with same name for this user
    routine = PracticeRoutine.query.filter_by(
        user_id=user_id,
        name=name
    ).first()

    if routine:
        # Update existing routine
        routine.practice_type = practice_type
        routine.tempo = tempo
        routine.comments = comments
        routine.last_used_at = datetime.utcnow()
    else:
        # Create new routine
        routine = PracticeRoutine(
            user_id=user_id,
            name=name,
            practice_type=practice_type,
            tempo=tempo,
            comments=comments,
            last_used_at=datetime.utcnow()
        )
        db.session.add(routine)

    db.session.commit()
    return routine


def get_user_routines(user_id: int) -> list:
    """
    Get user's practice routines ordered by most recently used.

    Args:
        user_id: User ID

    Returns:
        List of PracticeRoutine instances
    """
    return PracticeRoutine.query.filter_by(user_id=user_id).order_by(
        PracticeRoutine.last_used_at.desc()
    ).all()


def format_routine_display(routine: PracticeRoutine) -> str:
    """Format a routine for display."""
    parts = [routine.practice_type]

    if routine.tempo:
        parts.append(f"at {routine.tempo} BPM")

    if routine.comments:
        parts.append(f"- {routine.comments}")

    return " ".join(parts)


def calculate_total_sessions(user_id: int) -> int:
    """Calculate total practice sessions for user."""
    from src.models import PracticeSession
    return PracticeSession.query.filter_by(user_id=user_id).count()


def calculate_most_frequent_type(user_id: int) -> Optional[str]:
    """Calculate most frequent practice type for user."""
    from src.models import PracticeSession
    from sqlalchemy import func

    result = db.session.query(
        PracticeSession.practice_type,
        func.count(PracticeSession.id).label("frequency")
    ).filter_by(user_id=user_id).group_by(
        PracticeSession.practice_type
    ).order_by(
        func.count(PracticeSession.id).desc()
    ).first()

    return result[0] if result else None


def calculate_average_tempo(user_id: int) -> Optional[float]:
    """Calculate average tempo for tempo-based sessions (Chords and Scales only)."""
    from src.models import PracticeSession
    from sqlalchemy import func

    result = db.session.query(
        func.avg(PracticeSession.tempo)
    ).filter(
        PracticeSession.user_id == user_id,
        PracticeSession.practice_type.in_(["Chords", "Scales"]),
        PracticeSession.tempo.isnot(None)
    ).scalar()

    return float(result) if result else None
