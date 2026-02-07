"""
Routes for Piano Session Tracker application.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from src import db
from src.models import User, PracticeSession, PracticeRoutine
from src.forms import RegistrationForm, LoginForm, PracticeSessionForm
from src.utils import (
    validate_email, validate_password, hash_password, check_password,
    validate_practice_type, validate_tempo, validate_comments,
    create_or_update_routine, get_user_routines,
    calculate_total_sessions, calculate_most_frequent_type, calculate_average_tempo
)
from datetime import datetime, date, time

bp = Blueprint("main", __name__)


def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function


@bp.route("/")
def index():
    """Landing page."""
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration."""
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Additional validation
        is_valid, error = validate_email(form.email.data)
        if not is_valid:
            form.email.errors.append(error)
            return render_template("auth/register.html", form=form), 400

        is_valid, error = validate_password(form.password.data, form.password_confirm.data)
        if not is_valid:
            if "password" not in [e[0] for e in form._fields.items()]:
                form.password.errors.append(error)
            else:
                form.password.errors.append(error)
            return render_template("auth/register.html", form=form), 400

        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            form.email.errors.append("Email already in use. Please use a different email.")
            return render_template("auth/register.html", form=form), 400

        # Create new user
        user = User(
            email=form.email.data,
            password_hash=hash_password(form.password.data)
        )
        db.session.add(user)
        db.session.commit()

        # Log user in
        session["user_id"] = user.id
        flash(f"Welcome, {user.email}! Your account has been created.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """User login."""
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password(user.password_hash, form.password.data):
            session["user_id"] = user.id
            flash(f"Welcome back, {user.email}!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            form.email.errors.append("Invalid email or password")
            return render_template("auth/login.html", form=form), 400

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    """User logout."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))


@bp.route("/dashboard")
@login_required
def dashboard():
    """User dashboard."""
    user_id = session["user_id"]
    user = User.query.get(user_id)

    if not user:
        session.clear()
        return redirect(url_for("main.login"))

    total_sessions = calculate_total_sessions(user_id)
    most_frequent_type = calculate_most_frequent_type(user_id)

    return render_template(
        "dashboard.html",
        user=user,
        total_sessions=total_sessions,
        most_frequent_type=most_frequent_type
    )


@bp.route("/session/new", methods=["GET", "POST"])
@login_required
def new_session():
    """Create a new practice session."""
    user_id = session["user_id"]
    form = PracticeSessionForm()
    routines = get_user_routines(user_id)

    if form.validate_on_submit():
        # Validate practice type
        is_valid, error = validate_practice_type(form.practice_type.data)
        if not is_valid:
            flash(error, "danger")
            return render_template("session/new.html", form=form, routines=routines), 400

        # Validate tempo
        tempo_value = form.tempo.data if form.practice_type.data in ["Chords", "Scales"] else None
        is_valid, error = validate_tempo(str(tempo_value) if tempo_value else "", form.practice_type.data)
        if not is_valid:
            flash(error, "danger")
            return render_template("session/new.html", form=form, routines=routines), 400

        # Validate comments
        is_valid, error = validate_comments(form.comments.data)
        if not is_valid:
            flash(error, "danger")
            return render_template("session/new.html", form=form, routines=routines), 400

        # Create session
        session_obj = PracticeSession(
            user_id=user_id,
            practice_type=form.practice_type.data,
            tempo=tempo_value,
            comments=form.comments.data if form.comments.data else None,
            session_date=date.today(),
            session_time=datetime.now().time()
        )
        db.session.add(session_obj)
        db.session.commit()

        # Create or update routine
        create_or_update_routine(
            user_id=user_id,
            practice_type=form.practice_type.data,
            tempo=tempo_value,
            comments=form.comments.data if form.comments.data else None
        )

        flash("Session logged successfully!", "success")
        return redirect(url_for("main.session_history", new="true"))

    return render_template("session/new.html", form=form, routines=routines)


@bp.route("/session/history")
@login_required
def session_history():
    """View session history with optional filtering."""
    user_id = session["user_id"]
    practice_type_filter = request.args.get("type", "all")
    new_session = request.args.get("new", "false") == "true"

    # Get filtered sessions
    query = PracticeSession.query.filter_by(user_id=user_id)

    if practice_type_filter != "all":
        query = query.filter_by(practice_type=practice_type_filter)

    sessions = query.order_by(
        PracticeSession.session_date.desc(),
        PracticeSession.session_time.desc()
    ).all()

    # Calculate statistics
    total_sessions = calculate_total_sessions(user_id)
    most_frequent_type = calculate_most_frequent_type(user_id)
    average_tempo = calculate_average_tempo(user_id)

    return render_template(
        "session/history.html",
        sessions=sessions,
        total_sessions=total_sessions,
        most_frequent_type=most_frequent_type,
        average_tempo=average_tempo,
        current_filter=practice_type_filter,
        new_session=new_session
    )
