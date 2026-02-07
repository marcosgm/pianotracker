"""
WSGI entry point for Piano Session Tracker.
Run with: python wsgi.py
"""

import os
from src import create_app, db

app = create_app(os.environ.get("FLASK_ENV", "development"))


@app.shell_context_processor
def make_shell_context():
    """Make db and models available in shell."""
    return {
        "db": db,
        "User": __import__("src.models", fromlist=["User"]).User,
        "PracticeSession": __import__("src.models", fromlist=["PracticeSession"]).PracticeSession,
        "PracticeRoutine": __import__("src.models", fromlist=["PracticeRoutine"]).PracticeRoutine,
    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=os.environ.get("FLASK_ENV") == "development")
