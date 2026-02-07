# Tasks: Piano Session Tracker

**Input**: Design documents from `/specs/001-session-tracker/`
**Prerequisites**: plan.md ✅, spec.md ✅, data-model.md ✅, contracts/api-endpoints.md ✅

**Tests**: Minimal testing per Piano Tracker Constitution - integration tests for user stories only

**Organization**: Tasks grouped by user story with shared foundational phase enabling independent parallel development

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1, US2, US3, US4)
- **File paths**: Exact locations included in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per plan.md (src/, tests/, instance/ directories)
- [ ] T002 Initialize Flask project with requirements.txt (Flask 3.0+, SQLAlchemy 2.0+, SQLite)
- [ ] T003 [P] Create config.py with development and production configuration
- [ ] T004 [P] Create src/__init__.py to make src a Python package
- [ ] T005 Create .gitignore with Python patterns (venv, __pycache__, *.db, instance/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: All user stories depend on this phase - must complete before US1/US2/US3/US4

### Database & Models

- [ ] T006 Create src/models.py with SQLAlchemy User model (id, email UNIQUE, password_hash, created_at)
- [ ] T007 Create src/models.py - add PracticeSession model (id, user_id FK, practice_type, tempo nullable, comments nullable, session_date, session_time, created_at)
- [ ] T008 Create src/models.py - add PracticeRoutine model (id, user_id FK, practice_type, tempo nullable, comments nullable, last_used_at, created_at with UNIQUE constraint)
- [ ] T009 Create database initialization in src/app.py (app factory, db.create_all())

### Authentication & Session Management

- [ ] T010 [P] Create src/utils.py with password hashing functions (generate_password_hash, check_password_hash using werkzeug.security)
- [ ] T011 [P] Create src/utils.py - add email validation regex pattern for registration
- [ ] T012 [P] Create src/forms.py with WTForms form definitions for registration and login validation
- [ ] T013 [P] Implement Flask session management in src/app.py (session cookie configuration, secret key)
- [ ] T014 Configure PRAGMA foreign_keys = ON for SQLite in src/app.py

### Base Templates & Styling

- [ ] T015 Create src/templates/base.html with header, navigation, footer layout (extends block content)
- [ ] T016 Create src/static/styles.css with responsive CSS for mobile + desktop (no CSS frameworks)
- [ ] T017 [P] Create src/templates/error.html for 404 and 500 error pages

**Checkpoint**: Foundation ready - user story implementation can proceed in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can create accounts and securely log in to access their personal session data

**Independent Test**: Create account with email/password → Log out → Log back in → Verify session persists

### Implementation for US1

- [ ] T018 Create routes GET/POST /register in src/app.py (show form, validate input, create User, establish session)
- [ ] T019 Create src/templates/auth/register.html with email and password fields (inline validation errors)
- [ ] T020 [P] Create routes GET/POST /login in src/app.py (show form, validate credentials, create session)
- [ ] T021 [P] Create src/templates/auth/login.html with email and password form (generic "Invalid email or password" error)
- [ ] T022 Create GET /logout route in src/app.py (clear session, redirect to landing page)
- [ ] T023 Create src/templates/index.html landing page with Register/Login links (redirect to dashboard if authenticated)
- [ ] T024 Implement @login_required decorator or session check utility in src/utils.py for protecting routes
- [ ] T025 Add password validation (minimum 8 characters) to src/utils.py and forms.py
- [ ] T026 Create tests/test_auth.py with integration tests:
  - [ ] T026a Test successful registration with valid email and password
  - [ ] T026b Test registration validation (invalid email format, short password, password mismatch)
  - [ ] T026c Test successful login with correct credentials
  - [ ] T026d Test login failure with invalid email or password
  - [ ] T026e Test logout and session termination
  - [ ] T026f Test unauthorized access redirect to login when not authenticated

**Checkpoint**: User Story 1 complete - users can register, log in, log out, and access authenticated routes

---

## Phase 4: User Story 2 - Log a Piano Practice Session with Details (Priority: P1) 🎯 MVP

**Goal**: Users can record practice sessions with type, optional tempo, and comments; routines are automatically remembered

**Independent Test**: Log session with Chords + 120 BPM + "C Major arpeggios" → Verify appears in history with exact data

### Implementation for US2

- [ ] T027 [P] Create src/models.py - add helper method to User model for getting user's routines (relationship)
- [ ] T028 [P] Create src/utils.py - add validate_tempo(value, practice_type) function (40-180 for Chords/Scales, None for others)
- [ ] T029 [P] Create src/utils.py - add validate_comments(text) function (max 500 chars)
- [ ] T030 [P] Create src/utils.py - add validate_practice_type(type_str) function (one of Chords, Scales, Course, Songs)
- [ ] T031 Create routes GET /session/new in src/app.py (fetch user's routines, pass to template)
- [ ] T032 Create src/templates/session/new.html with:
  - [ ] T032a Practice type selector (dropdown: Chords, Scales, Course, Songs)
  - [ ] T032b Tempo input field (type="number", min=40, max=180, initially hidden, show on JS change for Chords/Scales)
  - [ ] T032c Comments textarea (optional, max 500 chars, show character count)
  - [ ] T032d "Past Routines" section displaying user's routines with clickable routine items
  - [ ] T032e "Save Session" button
  - [ ] T032f Client-side JavaScript to handle tempo field show/hide and routine pre-fill (minimal, no framework)
- [ ] T033 Create routes POST /session in src/app.py to:
  - [ ] T033a Validate practice_type, tempo (if applicable), comments on server
  - [ ] T033b Create PracticeSession record with user_id, practice_type, tempo, comments, session_date=today, session_time=now
  - [ ] T033c Check if routine exists with (user_id, practice_type, tempo, comments) - if yes update last_used_at, if no create new
  - [ ] T033d Redirect to /session/history?new=true on success
  - [ ] T033e Return form with validation error messages on failure
- [ ] T034 Create tests/test_session_logging.py with integration tests:
  - [ ] T034a Test logging Chords session with tempo (40, 100, 180 BPM)
  - [ ] T034b Test logging Scales session with tempo
  - [ ] T034c Test logging Course session without tempo
  - [ ] T034d Test logging Songs session without tempo
  - [ ] T034e Test logging session with comments
  - [ ] T034f Test validation: invalid tempo, out-of-range tempo, oversized comments
  - [ ] T034g Test routine creation on first session with this combination
  - [ ] T034h Test routine update (last_used_at) when same combination logged again
  - [ ] T034i Test unauthenticated access redirects to login

**Checkpoint**: User Story 2 complete - users can log practice sessions and routines auto-populate

---

## Phase 5: User Story 3 - Select or Create a Practice Session Routine (Priority: P2)

**Goal**: Users see past practice combinations and can quickly reuse them by pre-filling the form; routines are deduplicated

**Independent Test**: Log 2 Chords + 120 BPM sessions → Start new session → Verify routine appears once in list → Click routine → Form pre-fills → Modify and save → New session created without creating duplicate routine

### Implementation for US3

- [ ] T035 Create src/utils.py - add get_user_routines(user_id) function to query deduped routines ordered by last_used_at DESC
- [ ] T036 Create src/utils.py - add create_or_update_routine(user_id, practice_type, tempo, comments) function
- [ ] T037 Modify T032 (src/templates/session/new.html) to display routines dynamically:
  - [ ] T037a Order routines by most recently used (last_used_at DESC)
  - [ ] T037b Format routine display: "{practice_type} at {tempo} BPM - {comments}" (omit tempo if N/A, omit comments if empty)
  - [ ] T037c Add JavaScript to pre-fill form when routine is clicked
- [ ] T038 Modify T033 (POST /session route) to call create_or_update_routine after session is saved
- [ ] T039 Create tests/test_routines.py with integration tests:
  - [ ] T039a Test first session creates new routine
  - [ ] T039b Test identical second session updates routine's last_used_at, doesn't create duplicate
  - [ ] T039c Test different sessions create separate routines
  - [ ] T039d Test routine deduplication: same type/tempo/comments = no duplicate
  - [ ] T039e Test routine deduplication with empty comments (NULL = NULL in database)
  - [ ] T039f Test routine display order (most recently used first)
  - [ ] T039g Test clicking routine pre-fills form correctly
  - [ ] T039h Test modifying pre-filled routine values before saving creates new session without routine change

**Checkpoint**: User Story 3 complete - users can select and reuse past routines efficiently

---

## Phase 6: User Story 4 - View Session History and Statistics (Priority: P2)

**Goal**: Users see complete history of all past sessions with comments, statistics, and filtering capabilities

**Independent Test**: Log 3 sessions (Chords, Scales, Course) → View history → Verify all shown with comments → Filter by Chords → Verify only Chords shown → Check stats (total=3, most frequent=Chords or Scales)

### Implementation for US4

- [ ] T040 [P] Create src/utils.py - add calculate_total_sessions(user_id) function
- [ ] T040b [P] Create src/utils.py - add calculate_most_frequent_type(user_id) function (GROUP BY practice_type)
- [ ] T040c [P] Create src/utils.py - add calculate_average_tempo(user_id) function (for Chords/Scales sessions only)
- [ ] T041 Create routes GET /session/history in src/app.py to:
  - [ ] T041a Accept optional ?type=Chords query param for filtering by practice type
  - [ ] T041b Accept optional ?new=true query param to show success message
  - [ ] T041c Query PracticeSession records, filter by user_id and optionally by practice_type
  - [ ] T041d Order by session_date DESC, then session_time DESC
  - [ ] T041e Calculate and pass statistics to template
  - [ ] T041f Require authentication (redirect to login if not authenticated)
- [ ] T042 Create src/templates/session/history.html with:
  - [ ] T042a Statistics section: total sessions, most frequent type, average tempo
  - [ ] T042b Filter dropdown (All, Chords, Scales, Course, Songs) with "Filter" button
  - [ ] T042c Success message (green alert) if ?new=true
  - [ ] T042d Session list (table or rows) showing:
    - [ ] T042d1 Date (e.g., "Feb 7, 2026")
    - [ ] T042d2 Time (e.g., "14:30")
    - [ ] T042d3 Practice Type (e.g., "Chords")
    - [ ] T042d4 Tempo (e.g., "120 BPM") or "(No tempo)"
    - [ ] T042d5 Comments (truncate to ~100 chars if longer) or "(No notes)"
    - [ ] T042d6 Ordered most recent first
  - [ ] T042e Empty state message: "No sessions logged yet. Start practicing and logging your sessions!"
  - [ ] T042f Link back to "New Session"
- [ ] T043 Create tests/test_session_history.py with integration tests:
  - [ ] T043a Test history displays all sessions in reverse chronological order
  - [ ] T043b Test history displays session details (type, date, time, tempo, comments)
  - [ ] T043c Test filtering by practice type returns only selected type
  - [ ] T043d Test filtering with invalid type shows all sessions (graceful fallback)
  - [ ] T043e Test statistics calculations (total, most frequent, average tempo)
  - [ ] T043f Test empty history message when no sessions logged
  - [ ] T043g Test success message appears when ?new=true
  - [ ] T043h Test comments display with truncation for long text
  - [ ] T043i Test comments display as "(No notes)" when empty
  - [ ] T043j Test unauthenticated access redirects to login
- [ ] T044 Create tests/test_validation.py with validation tests:
  - [ ] T044a Test comment length validation (accept 500, reject 501+)
  - [ ] T044b Test practice_type validation (reject invalid types)
  - [ ] T044c Test tempo validation per type (Chords/Scales: 40-180, Course/Songs: reject tempo value)
  - [ ] T044d Test email format validation in registration
  - [ ] T044e Test password strength validation (min 8 chars)

**Checkpoint**: All user stories complete - full feature working end-to-end

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and validation

- [ ] T045 Create src/templates/dashboard.html for authenticated user dashboard showing:
  - [ ] T045a Welcome message with user's email
  - [ ] T045b "New Session" button → /session/new
  - [ ] T045c "Session History" button → /session/history
  - [ ] T045d Quick stats (total sessions, most frequent type)
  - [ ] T045e "Logout" link
- [ ] T046 Create GET /dashboard route in src/app.py (require auth, fetch stats, render dashboard.html)
- [ ] T047 Update src/templates/base.html to show:
  - [ ] T047a Navigation links (Dashboard, History, Logout if authenticated)
  - [ ] T047b Navigation links (Register, Login if not authenticated)
  - [ ] T047c Responsive hamburger menu for mobile
- [ ] T048 [P] Update src/static/styles.css for full responsive design:
  - [ ] T048a Clean, minimal design following simplicity principle
  - [ ] T048b Mobile-first responsive layout (mobile, tablet, desktop)
  - [ ] T048c Proper spacing, typography, accessible colors
  - [ ] T048d Form styling with clear focus states and error colors
  - [ ] T048e Table styling for session history
  - [ ] T048f Button styling consistent across all pages
- [ ] T049 [P] Add error handling middleware in src/app.py:
  - [ ] T049a 404 error handler → error.html with "Page not found"
  - [ ] T049b 500 error handler → error.html with generic message (don't expose details)
  - [ ] T049c Logging for errors
- [ ] T050 Create requirements.txt with all dependencies:
  - [ ] Flask 3.0+
  - [ ] Flask-SQLAlchemy
  - [ ] SQLAlchemy 2.0+
  - [ ] Werkzeug (password hashing)
  - [ ] pytest (for testing)
- [ ] T051 Write README.md with:
  - [ ] Project overview
  - [ ] Quick start instructions (virtualenv, pip install, db init, run server)
  - [ ] File structure overview
  - [ ] How to run tests
  - [ ] Links to documentation (plan.md, data-model.md, contracts/)
- [ ] T052 Test quickstart.md instructions end-to-end:
  - [ ] T052a Verify setup steps work (venv, pip, db init)
  - [ ] T052b Verify Flask server starts on port 5000
  - [ ] T052c Verify all quickstart test scenarios work (register, login, log session, view history, filter, logout)
- [ ] T053 [P] Create .env.example with configuration template (SECRET_KEY, FLASK_ENV)
- [ ] T054 [P] Create scripts/ directory with helper scripts:
  - [ ] T054a init_db.py - script to initialize database
  - [ ] T054b reset_db.py - script to drop and recreate database for development
- [ ] T055 Verify all URLs match contracts/api-endpoints.md specification
- [ ] T056 Security review:
  - [ ] T056a Password hashing using werkzeug.security
  - [ ] T056b Session cookies secure (HttpOnly, HTTPS in prod)
  - [ ] T056c Input validation on all forms (server-side)
  - [ ] T056d SQL injection prevention (SQLAlchemy parameterized queries)
  - [ ] T056e CSRF check if needed (minimal for simple forms)
- [ ] T057 Performance validation:
  - [ ] T057a Database queries optimized (indexes on user_id, session_date, etc.)
  - [ ] T057b Page load times < 500ms for typical operations
  - [ ] T057c Session history filtering responds in < 2 seconds

**Checkpoint**: Feature complete, tested, validated, ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - no dependencies on other stories
- **User Story 2 (Phase 3)**: Depends on Foundational - can start immediately after Foundation
- **User Story 3 (Phase 5)**: Depends on Foundational AND US2 (needs PracticeRoutine model and session creation)
- **User Story 4 (Phase 6)**: Depends on Foundational AND US2 (needs session data to display)
- **Polish (Phase 7)**: Depends on all user stories being complete

### Within Each User Story

1. Models/database changes first (tasks T006-T008)
2. Utilities and validation functions (tasks T010-T014)
3. Base templates and styling (tasks T015-T017)
4. Routes and templates for each user story
5. Tests last (verify they fail first, then pass after implementation)

### Parallel Opportunities

**Phase 1 Setup**: All [P] tasks (T003, T004) can run in parallel

**Phase 2 Foundational**: 
- T010-T012 (utilities, validation, forms) can run in parallel
- T015-T017 (templates, styling) can run in parallel
- But all must complete before Phase 3 starts

**Phase 3-6 User Stories**:
- Once Foundational completes, all user story model/utility tasks marked [P] can start in parallel
- US1 and US2 can be worked on simultaneously by different developers
- Once US2 completes, US3 can start (needs US2 session data)
- Once US2 completes, US4 can start (needs US2 session data)

**Phase 7 Polish**:
- T048, T049, T053, T054 marked [P] can run in parallel

### Example Parallel Execution: Team of 3

```
Day 1-2: All developers complete Phase 1 (Setup) + Phase 2 (Foundational)

Day 3-5:
  Developer A: Phase 3 - User Story 1 (Authentication)
  Developer B: Phase 4 - User Story 2 (Session Logging)
  Developer C: Phase 2b - Polish styling T048

Day 6-7:
  Developer A: Phase 5 - User Story 3 (Routines) - starts after US2 completes
  Developer B: Phase 6 - User Story 4 (History) - starts after US2 completes
  Developer C: Phase 7 - Polish & validation

Day 8:
  All: Testing, validation, deployment
```

---

## Implementation Strategy

### MVP First (Recommended)

1. **Complete Phase 1-2**: Setup + Foundational (days 1-2)
2. **Complete Phase 3**: User Story 1 - Authentication (days 3)
3. **Complete Phase 4**: User Story 2 - Session Logging (days 4)
4. **STOP and VALIDATE**: Test both stories independently, deploy MVP
5. **Expand**: Add US3 (Routines) and US4 (History) next

### MVP Scope for Deployment

- User authentication (register/login/logout)
- Session logging (practice type, optional tempo, optional comments)
- Automatic routine memory and pre-fill
- Basic session history view with filtering

This is fully functional and delivers value immediately. Everything in Phase 5+ is enhancement.

---

## Quality Gates & Validation Checkpoints

| Checkpoint | After Task | Validation |
|------------|-----------|-----------|
| **Foundation Ready** | T017 | All models created, auth framework in place, base templates exist |
| **US1 Complete** | T026 | Users can register → login → logout → access protected routes |
| **US1+US2 MVP** | T034 | Users can create sessions; routines auto-remembered |
| **US3 Routines** | T039 | Users see past routines; can select and pre-fill |
| **US4 History** | T043 | Users see session history; statistics calculated; filtering works |
| **Feature Complete** | T057 | All user stories working end-to-end; performance validated |

---

## Notes

- All file paths relative to repository root (`src/`, `tests/`, etc.)
- Tests use pytest with simple fixtures (no complex mocking needed)
- Templates use Jinja2 with minimal JavaScript (server-side rendering first)
- Database schema automatically created by SQLAlchemy on first run
- No build step required - pure Flask application
- Tests can run against temporary in-memory SQLite or test database per conftest.py
- After each task, run tests to verify no regressions
- Commit after logical groups of tasks (e.g., after completing a user story)
