# Implementation Plan: Piano Session Tracker

**Branch**: `001-session-tracker` | **Date**: 2026-02-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-session-tracker/spec.md`

**Status**: Phase 1 - Design & Contracts

## Summary

Build a user-friendly piano practice session tracker website using Flask and SQLite. Pianists register, log their daily practice sessions (selecting from Chords, Scales, Course, or Songs), with optional tempo input (40-180 BPM) for tempo-based practice types. The app displays a complete session history with statistics (total sessions, most frequent practice type) and supports filtering by practice type. All data persists securely per user, accessible only when logged in.

**Technical Approach**: Server-side rendered Flask application with Jinja2 templates and CSS styling. SQLite database for reliable local/development storage. Simple form-based UI with progressive enhancement. Minimal JavaScript, emphasis on clarity and ease of use for beginner pianists.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Flask 3.0+, SQLAlchemy 2.0+, Flask-SQLAlchemy, werkzeug (password hashing)  
**Storage**: SQLite (development/MVP), upgradeable to PostgreSQL  
**Testing**: pytest with integration tests for user stories, manual smoke tests, no unit test emphasis  
**Target Platform**: Web browser (desktop + mobile responsive)  
**Project Type**: Web application (single Flask server with server-side rendering)  
**Performance Goals**: Page load <500ms, database queries <100ms, support 100+ users with 1000+ sessions each  
**Constraints**: Minimal CSS framework (no build step), no JavaScript frameworks, privacy-first minimal data collection  
**Scale/Scope**: MVP phase supporting concurrent beginners, expandable to suggestions + piano visualization in future releases

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constraints Verification

| Principle | Status | Details |
|-----------|--------|---------|
| **Simplicity First** | ✅ PASS | Flask + SQLite is the simplest web stack. Server-side rendering avoids complexity of SPAs. No complex architectures or premature optimization. |
| **Server-Side Rendering** | ✅ PASS | Flask with Jinja2 templates for all pages. Forms use standard HTTP POST. No JavaScript frameworks or SPA patterns. CSS is plain with optional minimal framework. |
| **Beginner-Friendly Design** | ✅ PASS | Clear labels, simple 4-option selector for practice type. Tempo input only appears when needed. Straightforward history view with obvious filtering. No jargon. |
| **Data Integrity** | ✅ PASS | SQLAlchemy ensures database transactions. Input validation on server side (email format, password length, tempo range). Secure password hashing with werkzeug. Clear confirmations for session saves. |
| **Privacy & Minimal Data** | ✅ PASS | Only collect: email, password hash, practice type, tempo, date/time. No tracking scripts, analytics, or third-party integrations. User data isolated per account. |

**Conclusion**: ✅ **APPROVED** - Implementation plan fully aligns with Piano Tracker Constitution v1.0.0. All core principles satisfied.

---

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── app.py                      # Flask application factory and config
├── models.py                   # SQLAlchemy User and PracticeSession models
├── forms.py                    # Form definitions (registration, login, session)
├── utils.py                    # Helper functions (password hashing, validation)
├── templates/
│   ├── base.html               # Base layout (header, nav, footer)
│   ├── index.html              # Landing page (unauthenticated)
│   ├── auth/
│   │   ├── register.html       # Registration form
│   │   └── login.html          # Login form
│   ├── dashboard.html          # Logged-in user dashboard
│   ├── session/
│   │   ├── new.html            # New session form
│   │   └── history.html        # Session history + filtering + stats
│   └── error.html              # Error page template
├── static/
│   └── styles.css              # Main CSS stylesheet (responsive, minimal)
└── instance/
    └── pianotracker.db         # SQLite database (created at runtime)

tests/
├── conftest.py                 # Pytest fixtures (test client, test DB)
├── test_auth.py                # Authentication user journey tests
├── test_session_logging.py     # Session creation user journey tests
├── test_session_history.py     # History viewing user journey tests
└── test_validation.py          # Input validation tests

requirements.txt                # Python dependencies
config.py                       # Configuration for dev/prod environments
```

**Structure Decision**: Single Flask web application (Option 1 simplified for web). Server-side rendering with Jinja2 templates. SQLite database stored in `instance/` directory. Static CSS in `static/` directory. Models, forms, and utilities in root module files for simplicity. Tests organized by user story rather than test type to reinforce specification testing.

## Phase 0: Research

**Status**: Complete - No clarifications needed

### Technology Decisions Confirmed

- **Flask 3.0+**: Minimal dependencies, built-in routing, excellent for server-side rendering. Aligns with simplicity principle.
- **SQLAlchemy 2.0+**: ORM provides data integrity, type hints, simple query pattern matching spec requirements.
- **Werkzeug**: Standard password hashing for secure authentication (salted + bcrypt-equivalent).
- **Jinja2**: Flask default templating, familiar syntax, supports template inheritance for DRY layouts.
- **Plain CSS**: No build step, no npm dependencies, faster development. Use CSS Grid/Flexbox for responsive design.
- **pytest**: Standard Python testing framework, minimal configuration, `conftest.py` for fixtures.

### Rationale for Each Choice

| Choice | Why Selected | Alternatives Considered |
|--------|-------------|-------------------------|
| Flask | Simplest web framework, minimal boilerplate, easy debugging, great for learners | Django (too heavy), FastAPI (overkill for MVP) |
| SQLite | Zero-configuration database, perfect for MVP, easy migration to PostgreSQL later | PostgreSQL (unnecessary complexity), MongoDB (wrong data model) |
| SQLAlchemy | ORM ensures data integrity, supports migrations, declarative models match spec entities | Raw SQL (error-prone, no transactions), Django ORM (requires Django) |
| Jinja2 | Familiar syntax, powerful but not complex, works perfectly with Flask | Template strings (too minimal), React (violates rendering principle) |
| Plain CSS | Fastest time-to-beautiful UI, no build step, responsive is native | Tailwind (requires build), Bootstrap (opinionated classes), inline styles (maintainability nightmare) |
| pytest | Pytest fixtures are simpler than unittest, parametrization matches multiple scenarios | unittest (more boilerplate), hypothesis (overkill for simple sessions) |

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md)

**Key Entities**:
- **User**: id, email (unique), password_hash, created_at
- **PracticeSession**: id, user_id (FK), practice_type, tempo (optional), session_date, session_time, created_at

### API Routes & Contracts

See [contracts/](contracts/)

**Key Endpoints**:
- `POST /register` - Create new user account
- `POST /login` - Authenticate user
- `GET /logout` - Terminate session
- `GET /dashboard` - User dashboard (requires auth)
- `GET /session/new` - New session form (requires auth)
- `POST /session` - Save new session (requires auth)
- `GET /session/history` - View history with optional ?type=Chords filter (requires auth)

### Quick Start Guide

See [quickstart.md](quickstart.md)

## Complexity Tracking

No violations detected. Implementation aligns fully with Piano Tracker Constitution.
````
