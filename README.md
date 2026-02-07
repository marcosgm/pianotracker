# Piano Tracker

A simple web application for tracking piano practice sessions, selecting the kind of practice done each day, and reviewing history and statistics.

Built with Flask, SQLite, and server-side rendered templates.

## Development Setup

**Prerequisites:** Python 3.10+

```bash
# 1. Clone and enter the project
cd pianotracker

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the development server
python wsgi.py
```

The app will be available at **http://127.0.0.1:5000**.

The SQLite database is created automatically on first run inside the `instance/` directory.

### Running Tests

```bash
source venv/bin/activate
pytest tests/ -v
```

## Features

- **User accounts** – register and log in with email and password
- **Session logging** – record practice type (Chords, Scales, Course, Songs), optional tempo (40–180 BPM), and free-form comments (up to 500 characters)
- **Routine memory** – the app remembers past practice combinations and offers them for quick selection
- **History & statistics** – view past sessions, filter by type, and see totals and averages
