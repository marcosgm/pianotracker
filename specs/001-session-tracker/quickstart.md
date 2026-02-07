# Quick Start Guide: Piano Session Tracker

**Feature**: Piano Session Tracker | **Branch**: 001-session-tracker | **Created**: 2026-02-07

## Overview

Piano Session Tracker is a Flask-based web application that helps pianists log and track their daily practice sessions. This guide gets you from zero to running code in 5 minutes.

---

## Prerequisites

- Python 3.10 or higher installed
- Git installed
- A terminal/command prompt

**Check versions**:
```bash
python --version
git --version
```

---

## Setup (5 minutes)

### 1. Clone and Enter Repository

```bash
git clone [repository-url] pianotracker
cd pianotracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Activate virtual environment**:
- **macOS/Linux**: `source venv/bin/activate`
- **Windows**: `venv\Scripts\activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python -c "from src.app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 5. Start Development Server

```bash
python -m flask --app src.app run --debug
```

You should see output like:
```
 * Serving Flask app 'src.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open `http://localhost:5000` in your browser. You should see the Piano Tracker landing page.

---

## First Test Run

### 1. Create an Account

1. Click "Register" on landing page
2. Enter email: `test@example.com`
3. Enter password: `TestPassword123`
4. Confirm password: `TestPassword123`
5. Click "Sign Up"

You should be redirected to the dashboard.

### 2. Log a Practice Session

1. Click "New Session" button
2. Select "Chords" from the practice type dropdown
3. Enter tempo: `120`
4. Click "Save Session"

You should see success message and be redirected to history.

### 3. View Session History

History page should display:
- **Statistics**:
  - Total sessions logged: 1
  - Most frequent practice type: Chords
  - Average tempo: 120 BPM
- **Session List**: Your Chords session at the current time with "120 BPM"

### 4. Filter by Practice Type

1. Select "Chords" from the filter dropdown
2. Click "Filter"

History should show only the Chords session.

### 5. Try Logout

1. Click "Logout" link
2. You should be redirected to landing page (and unable to access `/dashboard`)

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `src/app.py` | Flask application factory and configuration |
| `src/models.py` | User and PracticeSession SQLAlchemy models |
| `src/forms.py` | WTForms form definitions |
| `src/utils.py` | Validation and password hashing utilities |
| `src/templates/base.html` | Base layout template (inherited by others) |
| `src/templates/auth/*.html` | Registration and login forms |
| `src/templates/session/*.html` | Session creation and history views |
| `src/static/styles.css` | CSS styling (responsive, clean design) |
| `tests/` | Integration tests (pytest) |
| `requirements.txt` | Python dependencies |

---

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
```

### Run Tests Verbosely (See Output)

```bash
pytest tests/ -v
```

### Run Single Test Function

```bash
pytest tests/test_session_logging.py::test_user_can_log_chords_session -v
```

---

## Common Development Tasks

### Adding a New Route

1. Create a route function in `src/app.py`:

```python
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
```

2. Create the template in `src/templates/about.html`

3. Test by navigating to `http://localhost:5000/about`

### Modifying the Database Schema

1. Update the model in `src/models.py`
2. Drop existing database: `rm instance/pianotracker.db`
3. Reinitialize: `python -c "from src.app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"`
4. Restart Flask server

### Changing Styling

Edit `src/static/styles.css` directly. Flask's debug mode auto-reloads CSS without restarting the server.

### Writing a New Test

Create a test file in `tests/` (e.g., `test_new_feature.py`):

```python
def test_my_feature(client):
    """Test description of what this tests"""
    # Arrange: Set up preconditions
    
    # Act: Perform the action being tested
    response = client.get('/path')
    
    # Assert: Verify expected outcome
    assert response.status_code == 200
    assert b'expected text' in response.data
```

Then run: `pytest tests/test_new_feature.py -v`

---

## Troubleshooting

### Port 5000 Already in Use

If Flask won't start because port 5000 is in use:

```bash
python -m flask --app src.app run --debug --port 5001
```

Then visit `http://localhost:5001`

### Database Lock Error

If you see "database is locked":

1. Stop the Flask server (Ctrl+C)
2. Delete the database: `rm instance/pianotracker.db`
3. Reinitialize: `python -c "from src.app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"`
4. Restart Flask server

### Virtual Environment Not Activated

If you see command not found errors, ensure your virtual environment is activated:

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Template Not Found Error

Ensure you're running Flask from the project root directory:

```bash
cd /path/to/pianotracker
python -m flask --app src.app run --debug
```

---

## Development Workflow

1. **Create or modify a feature**: Edit files in `src/`
2. **Test the feature**: Run manually in browser or write pytest test in `tests/`
3. **Check all tests pass**: `pytest tests/`
4. **Commit your changes**: `git add . && git commit -m "feature: brief description"`

---

## Next Steps

- Read [data-model.md](../data-model.md) to understand the database schema
- Read [contracts/api-endpoints.md](../contracts/api-endpoints.md) to understand all API endpoints
- Read [spec.md](../spec.md) to understand the requirements this implements
- Check `tests/` directory to see example tests for all user stories

---

## Production Deployment

Before deploying to production, you must:

1. **Switch database to PostgreSQL**: Update `config.py` with PostgreSQL connection string
2. **Set environment variables**: `FLASK_ENV=production`, `SECRET_KEY=<random-secret>`
3. **Enable HTTPS**: Use a reverse proxy (nginx) or platform like Heroku
4. **Run migrations**: Update database schema scripts if needed
5. **Disable debug mode**: Set `DEBUG=False` in production config

See `config.py` for configuration options.

---

## Getting Help

- Check error messages carefully (Flask debug page is very helpful)
- Look at tests in `tests/` for usage examples
- Check `src/templates/base.html` for available template blocks to override
- Review [contracts/api-endpoints.md](../contracts/api-endpoints.md) for endpoint details
