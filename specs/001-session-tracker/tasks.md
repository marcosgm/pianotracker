# Tasks: Piano Session Tracker

**Input**: Design documents from `/specs/001-session-tracker/`
**Prerequisites**: plan.md ✅, spec.md ✅, data-model.md ✅, contracts/api-endpoints.md ✅, quickstart.md ✅

**Tests**: Integration tests for user stories per Piano Tracker Constitution (minimal testing approach)

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **Checkbox**: Always `- [ ]` (markdown checkbox)
- **[ID]**: Sequential number (T001, T002, T003...) in execution order
- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story (US1, US2, US3, US4) - only for user story phases
- **Description**: Clear action with exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per plan.md (src/, tests/, instance/ directories)
- [ ] T002 Initialize Flask project with requirements.txt (Flask 3.0+, SQLAlchemy 2.0+, Flask-WTF 1.2.1, WTForms 3.1.1, email-validator 2.1.0, pytest 7.4.3)
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
- [ ] T008 Create src/models.py - add PracticeRoutine model (id, user_id FK, name String(100) NOT NULL, practice_type, tempo nullable, comments NOT NULL, last_used_at, created_at, UNIQUE constraint on (user_id, name))
- [ ] T009 Create database initialization in src/app.py (app factory, db.create_all())

### Authentication & Session Management

- [ ] T010 [P] Create src/utils.py with password hashing functions (hash_password, check_password using werkzeug.security)
- [ ] T011 [P] Create src/utils.py - add validate_email function with regex pattern for registration
- [ ] T012 [P] Create src/utils.py - add validate_password function (min 8 characters)
- [ ] T013 [P] Create src/forms.py with Flask-WTF form definitions (RegistrationForm, LoginForm)
- [ ] T014 Implement Flask session management in src/app.py (session cookie configuration, secret key)
- [ ] T015 Configure PRAGMA foreign_keys = ON for SQLite in src/app.py

### Base Templates & Styling

- [ ] T016 Create src/templates/base.html with header, navigation, footer layout (extends block content)
- [ ] T017 Create src/static/styles.css with responsive CSS for mobile + desktop (no CSS frameworks)
- [ ] T018 [P] Create src/templates/error.html for 404 and 500 error pages

**Checkpoint**: Foundation ready - user story implementation can proceed in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can create accounts and securely log in to access their personal session data

**Independent Test**: Create account with email/password → Log out → Log back in → Verify session persists

### Implementation for US1

- [ ] T019 [US1] Create routes GET/POST /register in src/routes.py (show form, validate input, create User, establish session)
- [ ] T020 [P] [US1] Create src/templates/auth/register.html with email and password fields (inline validation errors)
- [ ] T021 [P] [US1] Create routes GET/POST /login in src/routes.py (show form, validate credentials, create session)
- [ ] T022 [P] [US1] Create src/templates/auth/login.html with email and password form (generic "Invalid email or password" error)
- [ ] T023 [US1] Create GET /logout route in src/routes.py (clear session, redirect to landing page)
- [ ] T024 [US1] Create src/templates/index.html landing page with Register/Login links (redirect to dashboard if authenticated)
- [ ] T025 [US1] Implement login_required decorator in src/utils.py for protecting authenticated routes
- [ ] T026 [US1] Create tests/test_auth.py with integration tests (successful registration, validation errors, successful login, login failure, logout, unauthorized access redirect)

**Checkpoint**: User Story 1 complete - users can register, log in, log out, and access authenticated routes

---

## Phase 4: User Story 2 - Log a Piano Practice Session with Details (Priority: P1) 🎯 MVP

**Goal**: Users can record practice sessions with practice type, optional tempo, mandatory comments, and optionally save as a named routine

**Independent Test**: Log session with Chords + 120 BPM + "C Major arpeggios" → Verify appears in history with exact data → Optionally check "Save as Routine" with name "Morning Practice" → Verify routine saved

### Implementation for US2

- [ ] T027 [P] [US2] Create src/utils.py - add validate_practice_type function (enum: Chords, Scales, Course, Songs)
- [ ] T028 [P] [US2] Create src/utils.py - add validate_tempo function (40-180 for Chords/Scales, None for Course/Songs)
- [ ] T029 [P] [US2] Create src/utils.py - add validate_comments function (required non-empty, max 500 chars)
- [ ] T030 [P] [US2] Create src/utils.py - add validate_routine_name function (optional, max 100 chars if provided)
- [ ] T031 [P] [US2] Create src/forms.py - add PracticeSessionForm (practice_type SelectField, tempo IntegerField optional, comments TextAreaField mandatory, routine_name StringField optional)
- [ ] T032 [US2] Create routes GET /session/new in src/routes.py (fetch user's saved routines, render form)
- [ ] T033 [US2] Create src/templates/session/new.html with:
  - Practice type selector (dropdown: Chords, Scales, Course, Songs)
  - Tempo input field (type="number", min=40, max=180, hidden initially, shown via JS for Chords/Scales)
  - Comments textarea (mandatory, max 500 chars, character count display)
  - "Save this as a Routine" checkbox that toggles routine_name field visibility
  - Routine name input field (initially hidden, shown when checkbox checked)
  - JavaScript for tempo field show/hide based on practice_type selection
  - "Save Session" button
- [ ] T034 [US2] Create routes POST /session in src/routes.py to:
  - Validate practice_type, tempo (if applicable), comments (mandatory), routine_name (if provided)
  - Create PracticeSession record (user_id, practice_type, tempo, comments, session_date=today, session_time=now)
  - If routine_name provided: call create_or_update_routine with name-based upsert
  - Redirect to /session/history?new=true on success
  - Return form with validation errors on failure
- [ ] T035 [P] [US2] Create src/utils.py - add create_or_update_routine function (user_id, name, practice_type, tempo, comments) with name-based upsert logic per (user_id, name) uniqueness
- [ ] T036 [US2] Create tests/test_session_logging.py with integration tests:
  - Log Chords session with tempo (40, 100, 180 BPM) and comments
  - Log Scales session with tempo and comments
  - Log Course session without tempo, with comments
  - Log Songs session without tempo, with comments
  - Validation: invalid tempo, out-of-range tempo, empty comments, oversized comments
  - Named routine creation when routine_name provided
- [ ] T037 [US2] Create tests/test_validation.py with validation tests (email format, password strength, practice_type enum, tempo range per type, comments required/max length, routine name max length)

**Checkpoint**: User Story 2 complete - users can log practice sessions with mandatory comments and optionally save as named routines

---

## Phase 5: User Story 3 - Use Saved Routines to Log Sessions Quickly (Priority: P2)

**Goal**: Users see saved named routines and can quickly reuse them with locked type/comments and editable tempo

**Independent Test**: Save routine "Morning Scales" (Scales, 100 BPM, "C Major scales...") → Start new session → Click "Morning Scales" → Verify form pre-fills with locked type/comments, editable tempo → Adjust tempo to 110 → Save → Verify new session created without modifying routine

### Implementation for US3

- [ ] T038 [P] [US3] Create src/utils.py - add get_user_routines function (user_id) to query PracticeRoutine ordered by last_used_at DESC
- [ ] T039 [P] [US3] Create src/utils.py - add format_routine_display function to format routine for UI display (type + tempo + comments truncated)
- [ ] T040 [US3] Modify src/templates/session/new.html to add "Saved Routines" section:
  - Display heading "Saved Routines" when user has routines
  - Show routine list ordered by last_used_at DESC
  - Each routine displays as clickable card: practice_type + tempo (if applicable) + comments (truncated)
  - JavaScript selectRoutine function to pre-fill form when routine clicked
  - Lock practice_type select (disabled attribute) and comments textarea (readOnly attribute)
  - Set tempo value (editable)
  - Display banner with "Clear" link to unlock fields
  - On form submit, re-enable disabled practice_type select so value submits
- [ ] T041 [US3] Update POST /session route in src/routes.py to handle locked form submission (ensure disabled fields are re-enabled before validation)
- [ ] T042 [US3] Create tests/test_routines.py with integration tests:
  - Create named routine via session save with routine_name
  - Load new session page and verify routine appears in "Saved Routines" section
  - Simulate routine selection and verify form pre-fills correctly
  - Test that practice_type and comments are locked (readonly) after selection
  - Test that tempo remains editable after selection
  - Test Clear functionality unlocks all fields
  - Test routine name uniqueness per user (saving duplicate name updates existing)
  - Test routine ordering (most recently used first)

**Checkpoint**: User Story 3 complete - users can select saved routines with locked type/comments and editable tempo

---

## Phase 6: User Story 4 - View Session History and Statistics (Priority: P2)

**Goal**: Users see complete history of all past sessions with comments, statistics, and filtering capabilities

**Independent Test**: Log 3 sessions (Chords, Scales, Course) with different comments → View history → Verify all shown with comments → Filter by Chords → Verify only Chords shown → Check stats (total=3, most frequent, average tempo)

### Implementation for US4

- [ ] T043 [P] [US4] Create src/utils.py - add calculate_total_sessions function (user_id)
- [ ] T044 [P] [US4] Create src/utils.py - add calculate_most_frequent_type function (user_id) using GROUP BY practice_type
- [ ] T045 [P] [US4] Create src/utils.py - add calculate_average_tempo function (user_id) for Chords/Scales sessions only
- [ ] T046 [US4] Create routes GET /session/history in src/routes.py to:
  - Accept optional ?type=Chords query param for filtering by practice type
  - Accept optional ?new=true query param to show success message
  - Query PracticeSession records filtered by user_id and optionally practice_type
  - Order by session_date DESC, session_time DESC
  - Calculate statistics (total, most frequent, average tempo)
  - Require authentication (redirect to login if not authenticated)
- [ ] T047 [US4] Create src/templates/session/history.html with:
  - Statistics section (total sessions, most frequent type, average tempo)
  - Filter dropdown (All, Chords, Scales, Course, Songs) with "Filter" button
  - Success message (green alert) if ?new=true
  - Session list showing date, time, practice type, tempo (or "No tempo"), comments
  - Ordered most recent first
  - Empty state message: "No sessions logged yet. Start practicing and logging your sessions!"
  - Link back to "New Session"
- [ ] T048 [US4] Create tests/test_session_history.py with integration tests:
  - History displays all sessions in reverse chronological order
  - History shows session details (type, date, time, tempo, comments)
  - Filtering by practice type returns only selected type
  - Filtering with invalid type shows all sessions (graceful fallback)
  - Statistics calculations (total, most frequent, average tempo) are accurate
  - Empty history message when no sessions logged
  - Success message appears when ?new=true
  - Comments display correctly (no truncation needed for history - show full comments up to 500)
  - Unauthenticated access redirects to login

**Checkpoint**: All user stories complete - full feature working end-to-end

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements and validation

- [ ] T049 [P] Create src/templates/dashboard.html for authenticated user dashboard:
  - Welcome message with user's email
  - "New Session" button → /session/new
  - "Session History" button → /session/history
  - Quick stats (total sessions, most frequent type)
  - "Logout" link
- [ ] T050 Create GET /dashboard route in src/routes.py (require auth, fetch stats, render dashboard.html)
- [ ] T051 Update src/templates/base.html to show:
  - Navigation links (Dashboard, New Session, History, Logout) if authenticated
  - Navigation links (Register, Login) if not authenticated
  - Responsive hamburger menu for mobile
- [ ] T052 [P] Update src/static/styles.css for full responsive design:
  - Clean, minimal design following Piano Tracker Constitution simplicity principle
  - Mobile-first responsive layout (mobile, tablet, desktop)
  - Proper spacing, typography, accessible colors
  - Form styling with clear focus states and error colors
  - Table styling for session history
  - Button styling consistent across all pages
  - Routine card styling in "Saved Routines" section
- [ ] T053 [P] Add error handling middleware in src/app.py:
  - 404 error handler → error.html with "Page not found"
  - 500 error handler → error.html with generic message (don't expose details)
  - Logging for errors
- [ ] T054 [P] Verify requirements.txt includes all dependencies:
  - Flask 3.0+
  - Flask-SQLAlchemy 3.1.1
  - SQLAlchemy 2.0.23
  - Flask-WTF 1.2.1
  - WTForms 3.1.1
  - email-validator 2.1.0
  - Werkzeug 3.0.1 (password hashing)
  - pytest 7.4.3 (for testing)
- [ ] T055 Write README.md with:
  - Project overview
  - Quick start instructions (virtualenv, pip install, db init, run server)
  - File structure overview
  - How to run tests
  - Links to documentation (plan.md, data-model.md, contracts/)
- [ ] T056 Test quickstart.md instructions end-to-end:
  - Verify setup steps work (venv, pip, db init)
  - Verify Flask server starts on port 5000
  - Verify all quickstart test scenarios work (register, login, log session, view history, filter, logout)
- [ ] T057 [P] Create .env.example with configuration template (SECRET_KEY, FLASK_ENV)
- [ ] T058 Verify all URLs match contracts/api-endpoints.md specification
- [ ] T059 Security review:
  - Password hashing using werkzeug.security
  - Session cookies secure (HttpOnly, HTTPS in prod)
  - Input validation on all forms (server-side)
  - SQL injection prevention (SQLAlchemy parameterized queries)
- [ ] T060 Performance validation:
  - Database queries optimized (indexes on user_id, session_date, etc.)
  - Page load times < 500ms for typical operations
  - Session history filtering responds in < 2 seconds

**Checkpoint**: Feature complete, tested, validated, ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - can start immediately after Phase 2
- **User Story 2 (Phase 4)**: Depends on Foundational - can start immediately after Phase 2 (independent of US1)
- **User Story 3 (Phase 5)**: Depends on Foundational AND US2 (needs PracticeRoutine model and session creation with routine_name)
- **User Story 4 (Phase 6)**: Depends on Foundational AND US2 (needs PracticeSession data to display)
- **Polish (Phase 7)**: Depends on all user stories being complete

### Within Each User Story

1. Validation/utility functions first (parallel opportunities)
2. Forms definitions (parallel with utilities)
3. Routes and templates (sequential, depends on forms/utils)
4. Tests last (verify implementation works)

### Parallel Opportunities

**Phase 1 Setup**: All [P] tasks (T003, T004) can run in parallel

**Phase 2 Foundational**: 
- T010-T012 (utilities, validation) can run in parallel
- T013 (forms) can run in parallel with T010-T012
- T016-T018 (templates, styling) can run in parallel after database tasks
- But all must complete before Phase 3 starts

**User Stories (Phases 3-6)**:
- Once Foundational completes, US1 and US2 can be worked on simultaneously by different developers
- Once US2 completes, US3 and US4 can start in parallel (both depend on US2)
- All [P] tasks within each story can run in parallel

**Phase 7 Polish**:
- T049, T052, T053, T054, T057 marked [P] can run in parallel

### Example Parallel Execution: Team of 3

```
Day 1-2: All developers complete Phase 1 (Setup) + Phase 2 (Foundational)

Day 3-4:
  Developer A: Phase 3 - User Story 1 (Authentication)
  Developer B: Phase 4 - User Story 2 (Session Logging with named routines)
  Developer C: Phase 2 polish - Styling and error templates

Day 5-6:
  Developer A: Phase 5 - User Story 3 (Saved Routines) - starts after US2 completes
  Developer B: Phase 6 - User Story 4 (History & Stats) - starts after US2 completes
  Developer C: Phase 7 - Polish & validation

Day 7:
  All: Testing, validation, deployment
```

---

## Parallel Example: User Story 2

Tasks T027-T031 (all utilities and forms) can run in parallel:

```bash
# Launch all utilities together:
Task: "Create src/utils.py - add validate_practice_type function"
Task: "Create src/utils.py - add validate_tempo function"
Task: "Create src/utils.py - add validate_comments function"
Task: "Create src/utils.py - add validate_routine_name function"
Task: "Create src/forms.py - add PracticeSessionForm"
```

---

## Implementation Strategy

### MVP First (Recommended)

1. **Complete Phase 1-2**: Setup + Foundational (days 1-2)
2. **Complete Phase 3**: User Story 1 - Authentication (day 3)
3. **Complete Phase 4**: User Story 2 - Session Logging with mandatory comments and optional named routines (day 4)
4. **STOP and VALIDATE**: Test both stories independently, deploy MVP
5. **Expand**: Add US3 (Saved Routines with locked pre-fill) and US4 (History & Stats) next

### MVP Scope for Deployment

- User authentication (register/login/logout)
- Session logging (practice type, optional tempo, mandatory comments)
- Optional named routine save
- Basic session history view

This is fully functional and delivers core value immediately. US3 (routine quick-select with locked pre-fill) and US4 (statistics & filtering) are enhancements.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (auth working!)
3. Add User Story 2 → Test independently → Deploy/Demo (MVP! users can log sessions)
4. Add User Story 3 → Test independently → Deploy/Demo (efficiency boost with saved routines)
5. Add User Story 4 → Test independently → Deploy/Demo (full feature with history & stats)

---

## Quality Gates & Validation Checkpoints

| Checkpoint | After Task | Validation |
|------------|-----------|-----------|
| **Foundation Ready** | T018 | All models created, auth framework in place, base templates exist |
| **US1 Complete** | T026 | Users can register → login → logout → access protected routes |
| **US1+US2 MVP** | T037 | Users can create sessions with mandatory comments; optional named routine save |
| **US3 Routines** | T042 | Users see saved routines; can select and pre-fill with locked type/comments, editable tempo |
| **US4 History** | T048 | Users see session history with comments; statistics calculated; filtering works |
| **Feature Complete** | T060 | All user stories working end-to-end; performance validated |

---

## Notes

- All file paths relative to repository root (`src/`, `tests/`, etc.)
- Tests use pytest with fixtures in conftest.py
- Templates use Jinja2 with minimal JavaScript (server-side rendering first)
- Database schema automatically created by SQLAlchemy on first run
- Tests run against in-memory SQLite per conftest.py
- After each task, run tests to verify no regressions
- Commit after logical groups of tasks (e.g., after completing a user story)
- Piano Tracker Constitution principle: Simplicity First - no premature optimization
- Comments are mandatory at application level (form validation) but DB column remains nullable for migration flexibility
- Routines are user-named presets created opt-in; they pre-fill the form with locked type/comments and editable tempo
- Routine uniqueness enforced per user by (user_id, name) constraint

