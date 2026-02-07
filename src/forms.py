"""
Flask-WTF forms for Piano Session Tracker.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional
from src.utils import VALID_PRACTICE_TYPES


class RegistrationForm(FlaskForm):
    """User registration form."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
            Length(max=255)
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
            Length(min=8, message="Password must be at least 8 characters")
        ]
    )
    password_confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(message="Please confirm your password")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """User login form."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required")]
    )
    submit = SubmitField("Login")


class PracticeSessionForm(FlaskForm):
    """Practice session form."""

    practice_type = SelectField(
        "Practice Type",
        choices=[(pt, pt) for pt in sorted(VALID_PRACTICE_TYPES)],
        validators=[DataRequired(message="Please select a practice type")],
        coerce=str
    )
    tempo = IntegerField(
        "Tempo (BPM)",
        validators=[Optional()]
    )
    comments = TextAreaField(
        "Comments",
        validators=[
            DataRequired(message="Comments are required"),
            Length(max=500, message="Comments must be 500 characters or less")
        ]
    )
    routine_name = StringField(
        "Save this Routine as",
        validators=[Optional(), Length(max=100, message="Routine name must be 100 characters or less")]
    )
    submit = SubmitField("Save Session")
