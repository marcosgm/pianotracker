"""
Database models for Piano Session Tracker.
"""

from datetime import datetime
from src import db


class User(db.Model):
    """User account model."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    sessions = db.relationship(
        "PracticeSession", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    routines = db.relationship(
        "PracticeRoutine", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def get_routines(self):
        """Get user's practice routines ordered by most recently used."""
        return PracticeRoutine.query.filter_by(user_id=self.id).order_by(
            PracticeRoutine.last_used_at.desc()
        ).all()


class PracticeSession(db.Model):
    """Practice session model."""

    __tablename__ = "practice_session"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    practice_type = db.Column(
        db.String(20), nullable=False
    )  # Chords, Scales, Course, Songs
    tempo = db.Column(db.Integer, nullable=True)  # 40-180 BPM, or NULL
    comments = db.Column(db.Text, nullable=True)  # Optional documentation
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.Index("ix_user_date", "user_id", "session_date"),
        db.Index("ix_user_type", "user_id", "practice_type"),
    )

    def __repr__(self) -> str:
        return f"<PracticeSession {self.practice_type} {self.session_date} {self.session_time}>"


class PracticeRoutine(db.Model):
    """Practice routine model - auto-derived from unique session combinations."""

    __tablename__ = "practice_routine"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    practice_type = db.Column(
        db.String(20), nullable=False
    )  # Chords, Scales, Course, Songs
    tempo = db.Column(db.Integer, nullable=True)  # 40-180 BPM, or NULL
    comments = db.Column(db.Text, nullable=True)  # Optional documentation
    last_used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "practice_type", "tempo", "comments",
                           name="uq_user_routine"),
        db.Index("ix_routine_user_recency", "user_id", "last_used_at"),
    )

    def __repr__(self) -> str:
        return f"<PracticeRoutine {self.practice_type} {self.tempo} {self.comments[:20] if self.comments else ''}>"
