"""
Piano Session Tracker - Flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name: str = None) -> Flask:
    """
    Application factory function.

    Args:
        config_name: Configuration name (development, testing, production).
                    If None, uses FLASK_ENV environment variable.

    Returns:
        Flask application instance.
    """
    from config import get_config

    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Initialize database
    db.init_app(app)

    # Register database models
    with app.app_context():
        from src.models import User, PracticeSession, PracticeRoutine  # noqa: F401

    # Register blueprints and routes
    from src import routes

    app.register_blueprint(routes.bp)

    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask) -> None:
    """Register error handlers for the application."""

    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template

        return render_template("error.html", status_code=404, message="Page not found"), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template

        db.session.rollback()
        return (
            render_template(
                "error.html",
                status_code=500,
                message="Something went wrong. Please try again later.",
            ),
            500,
        )
