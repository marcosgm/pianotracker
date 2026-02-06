# Implementation Tasks: Piano Practice Session Tracker

**Feature**: Piano Practice Session Tracker | **Branch**: `001-practice-tracker`  
**Created**: 2026-02-06 | **Estimated Duration**: 4-6 weeks | **Team Size**: 1-2 developers

---

## Overview

This document breaks down the implementation plan into actionable tasks organized by user story and phase. Each task is independently testable and can be completed by a developer without waiting for other tasks to complete (where possible).

**Structure**:
- Phase 1: Setup & Infrastructure (4 days)
- Phase 2: Foundational Systems (3 days)
- Phase 3: User Story 1 - Authentication (5 days)
- Phase 4: User Story 2 - Session Logging (5 days)
- Phase 5: User Story 3 - History & Statistics (5 days)
- Phase 6: Polish & Cross-Cutting Concerns (2 weeks)

**Total Estimated**: 30-35 development days (4-5 weeks at 6-8 hours/day)

---

## Phase 1: Setup & Infrastructure (Days 1-4)

### Backend Setup

- [ ] T001 Initialize Python backend project structure with FastAPI
  - Create: `backend/src/main.py`
  - Create: `backend/src/__init__.py`
  - Create: `backend/requirements.txt` with FastAPI, Uvicorn, Pydantic, python-jose, bcrypt, azure-cosmos
  - Create: `backend/pytest.ini` for test configuration
  - Create: `backend/.env.example` template for environment variables
  - Install dependencies and verify `uvicorn src.main:app --reload` starts successfully

- [ ] T002 Configure backend environment and dependencies
  - Create: `backend/.env` (copy from .env.example)
  - Add FASTAPI_ENV, DEBUG, SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_MINUTES, COSMOSDB_ENDPOINT, COSMOSDB_KEY, COSMOSDB_DATABASE, CORS_ORIGINS
  - Create: `backend/src/config.py` to load environment variables using Pydantic BaseSettings
  - Verify all required env vars are read correctly with test configuration script

- [ ] T003 Setup Python virtual environment and Docker support
  - Create: `backend/Dockerfile` for containerized deployment
  - Create: `docker-compose.yml` for local development (includes CosmosDB emulator)
  - Create: `.dockerignore` to exclude unnecessary files
  - Verify Docker image builds and uvicorn starts in container

### Frontend Setup

- [ ] T004 Initialize TypeScript frontend project with Webpack
  - Create: `frontend/src/main.ts` entry point
  - Create: `frontend/webpack.config.js` with TypeScript and CSS loaders
  - Create: `frontend/tsconfig.json` with strict mode enabled
  - Create: `frontend/package.json` with dependencies: zod, chart.js, webpack, typescript, jest
  - Create: `frontend/public/index.html` with basic HTML structure
  - Create: `frontend/public/styles.css` with mobile-first responsive design
  - Run `npm run build` and verify bundle size is < 200KB

- [ ] T005 Configure frontend environment and build pipeline
  - Create: `frontend/.env.example` template for API_BASE_URL, JWT_STORAGE_KEY
  - Create: `frontend/.env` (copy from .env.example, set API_BASE_URL=http://localhost:8000)
  - Create: `frontend/jest.config.js` for unit testing
  - Create: `frontend/eslint.config.js` for code quality
  - Create: `frontend/.gitignore` to exclude node_modules, dist, coverage
  - Verify `npm run build` and `npm test` work without errors

- [ ] T006 Setup TypeScript types and validation schemas
  - Create: `frontend/src/types/index.ts` with interfaces: User, Session, AuthResponse, SessionCreateRequest, etc.
  - Create: `frontend/src/utils/validation.ts` with Zod schemas for all forms (register, login, session creation)
  - Create: `frontend/src/utils/constants.ts` with constants: PRACTICE_TYPES, TEMPO_MIN, TEMPO_MAX, API_BASE_URL
  - Write unit tests in `frontend/tests/unit/validation.test.ts` to verify all schemas work correctly

### Database Setup

- [ ] T007 Setup Azure CosmosDB (cloud or emulator) and create containers
  - Create: `infrastructure/azure/cosmos-setup.sh` script to create database and containers
  - Or use Azure CLI to manually create:
    - Database: `pianotracker`
    - Container 1: `users` with partition key `/partition_key`
    - Container 2: `practice_sessions` with partition key `/partition_key`
  - Verify connection by running test query: `SELECT * FROM c WHERE c.id = 'test'`
  - Document CosmosDB endpoint, key, and connection string in setup guide

- [ ] T008 Create database initialization and migration infrastructure
  - Create: `backend/src/db/migrations.py` with functions to create containers and indexes if not exist
  - Create composite indexes on:
    - `practice_sessions`: `(user_id, date DESC)`
    - `practice_sessions`: `(user_id, practice_type)`
  - Create: `backend/src/db/seed.py` to optionally seed test data
  - Run migrations on app startup to ensure schema is consistent

### CI/CD Setup

- [ ] T009 Configure GitHub Actions CI/CD pipeline
  - Create: `.github/workflows/ci.yml` with jobs:
    - Lint frontend (ESLint)
    - Test frontend (Jest, coverage)
    - Build frontend
    - Lint backend (Ruff, type checking)
    - Test backend (pytest, coverage)
    - Build Docker image
  - Add branch protection rules: require CI to pass before merge
  - Configure artifacts: save test coverage reports
  - Test pipeline with a dummy commit

- [ ] T010 Setup project documentation structure
  - Create: `README.md` (project overview, quick start)
  - Create: `CONTRIBUTING.md` (development guidelines, PR process)
  - Create: `docs/API_GUIDE.md` (generated from OpenAPI)
  - Create: `docs/SETUP.md` (detailed setup instructions)
  - Create: `docs/DEPLOYMENT.md` (deployment procedures)
  - Verify all docs are readable and links work

---

## Phase 2: Foundational Systems (Days 5-7)

### Backend Foundation

- [ ] T011 [P] Implement CosmosDB client and connection management
  - Create: `backend/src/db/cosmos_client.py` with:
    - CosmosClient initialization from environment variables
    - Functions to get database, users container, sessions container
    - Dependency injection setup for FastAPI (Depends helper)
    - Error handling for connection failures
    - Context manager for transaction-like operations
  - Create: `backend/tests/unit/test_cosmos_client.py` to verify initialization and container access
  - Test locally with emulator or Azure CosmosDB

- [ ] T012 [P] Create Pydantic data models for User and PracticeSession
  - Create: `backend/src/models/user.py` with:
    - UserBase (email, name)
    - UserCreate (+ password)
    - UserResponse (+ id, created_at, updated_at, excludes password_hash)
    - User (internal model with password_hash)
    - Validators for email format, password strength, email lowercase normalization
  - Create: `backend/src/models/practice_session.py` with:
    - SessionBase (practice_type, tempo, notes)
    - SessionCreate (without date, tempo validated conditionally)
    - SessionUpdate (only notes can be updated)
    - SessionResponse (+ id, user_id, date, created_at, updated_at)
    - PracticeSession (internal model with partition_key)
    - Validators for practice_type enum, conditional tempo requirement, date immutability
  - Create: `backend/tests/unit/test_models.py` to test validation rules with pytest
  - Verify all edge cases are handled (invalid tempo, missing required fields, etc.)

- [ ] T013 [P] Setup FastAPI application with middleware and error handling
  - Create: `backend/src/api/middleware.py` with:
    - CORS middleware (allow localhost:3000 in dev, production origin in prod)
    - Request/response logging middleware
    - Error handling middleware (catch exceptions, return RFC 7807 error format)
    - Rate limiting middleware on auth endpoints (5 req/min per IP)
  - Create: `backend/src/api/exceptions.py` with custom exception classes:
    - AuthenticationError (401)
    - AuthorizationError (403)
    - ValidationError (422)
    - NotFoundError (404)
    - ConflictError (409)
  - Update: `backend/src/main.py` to:
    - Initialize FastAPI app
    - Add middleware
    - Add exception handlers
    - Add health check endpoint `GET /health`
  - Create: `backend/tests/unit/test_middleware.py` to verify error handling

- [ ] T014 [P] Implement authentication utilities (JWT, password hashing)
  - Create: `backend/src/security/crypto.py` with:
    - `hash_password(password: str) -> str` using bcrypt cost 12
    - `verify_password(password: str, hash: str) -> bool`
    - Tests for various password lengths and special characters
  - Create: `backend/src/security/jwt.py` with:
    - `create_access_token(sub: str, expires_delta: timedelta) -> str`
    - `create_refresh_token(sub: str, expires_delta: timedelta) -> str`
    - `decode_token(token: str) -> dict` with expiration validation
    - `get_current_user(token: str) -> User` as dependency for protected routes
    - Tests for token generation, expiration, invalid tokens
  - Create: `backend/tests/unit/test_crypto.py` and `test_jwt.py` with pytest

### Frontend Foundation

- [ ] T015 [P] Create API client with error handling and JWT injection
  - Create: `frontend/src/services/api.ts` with:
    - ApiClient class with baseUrl and authService dependencies
    - `request<T>(endpoint, options): Promise<T>` generic method
    - Automatic JWT header injection from authService.getAccessToken()
    - Error handling: retry on 401 (token refresh), redirect to login on 401 after refresh
    - Rate limit handling (return 429 errors)
    - Timeout handling with configurable timeout (default 30s)
  - Create: `frontend/src/services/auth.ts` with:
    - `register(email, password, name): Promise<AuthResponse>`
    - `login(email, password): Promise<AuthResponse>`
    - `logout(): Promise<void>`
    - `refreshToken(): Promise<boolean>`
    - `getAccessToken(): string | null`
    - `setTokens(accessToken, refreshToken): void`
    - Token storage in memory (accessToken) and httpOnly cookie (refreshToken)
  - Create: `frontend/tests/unit/api.test.ts` with mocked fetch calls

- [ ] T016 [P] Setup client-side routing and page structure
  - Create: `frontend/src/components/router.ts` simple router without dependencies
  - Create: `frontend/src/pages/LoginPage.ts` with LoginForm rendering
  - Create: `frontend/src/pages/RegisterPage.ts` with RegisterForm rendering
  - Create: `frontend/src/pages/DashboardPage.ts` (landing after login)
  - Create: `frontend/src/pages/LogSessionPage.ts` (session logging form)
  - Create: `frontend/src/pages/HistoryPage.ts` (session history + stats)
  - Update: `frontend/src/main.ts` to:
    - Initialize router
    - Render appropriate page based on route
    - Check authentication on app load, redirect to login if not authenticated
  - Create: `frontend/tests/unit/router.test.ts` to verify routing logic

- [ ] T017 [P] Create simple state management (Store pattern)
  - Create: `frontend/src/services/store.ts` with:
    - AppStore class with pub/sub pattern
    - State: currentUser, sessions, isLoading, error
    - Methods: getState(), subscribe(listener), dispatch(action)
    - Action types: SET_USER, SET_SESSIONS, SET_LOADING, SET_ERROR, CLEAR_ERROR
  - Create: `frontend/tests/unit/store.test.ts` to verify pub/sub and state updates

---

## Phase 3: User Story 1 - Authentication (Days 8-12)

### Backend: Authentication API

- [ ] T018 [US1] Implement user registration endpoint
  - Create: `backend/src/api/auth.py` with POST `/api/auth/register`
  - Validate request body with UserCreate schema
  - Check if email already exists (query users container)
  - Hash password with bcrypt
  - Create User document in users container with UUID
  - Generate access token and refresh token
  - Return: UserResponse + access_token, token_type
  - Handle errors: 409 Conflict if email exists, 422 Validation error if invalid input

- [ ] T019 [US1] Implement user login endpoint
  - Add to: `backend/src/api/auth.py` POST `/api/auth/login`
  - Validate request body with UserLogin schema
  - Query users container: SELECT * WHERE email = @email
  - Verify password with bcrypt
  - Generate access token (15min) and refresh token (7d)
  - Return access token + user info
  - Return Set-Cookie header with refresh token (httpOnly, Secure, SameSite=Strict)
  - Handle errors: 401 Unauthorized if email/password invalid

- [ ] T020 [US1] Implement token refresh endpoint
  - Add to: `backend/src/api/auth.py` POST `/api/auth/refresh`
  - Extract refresh token from cookie
  - Decode and validate refresh token
  - Issue new access token (15min) and new refresh token (7d)
  - Return new access token + new Set-Cookie with rotated refresh token
  - Handle errors: 401 if refresh token invalid or expired

- [ ] T021 [US1] Implement logout endpoint
  - Add to: `backend/src/api/auth.py` POST `/api/auth/logout`
  - Require authentication (Bearer token)
  - Optionally: add token to blacklist for revocation (future: Redis)
  - Return 204 No Content
  - Set Set-Cookie with empty refresh token (Max-Age=0) to clear cookie

- [ ] T022 [US1] Implement get current user endpoint
  - Add to: `backend/src/api/auth.py` GET `/api/auth/me`
  - Require authentication (Bearer token)
  - Extract user_id from token
  - Query users container: SELECT * WHERE id = @userId
  - Return UserResponse (exclude password_hash)
  - Handle errors: 404 if user not found (deleted), 401 if token invalid

- [ ] T023 [US1] Write backend authentication tests (80%+ coverage)
  - Create: `backend/tests/integration/test_auth_api.py` with:
    - Test successful registration with valid data (201 Created)
    - Test registration with invalid email (400)
    - Test registration with short password (400)
    - Test registration with duplicate email (409)
    - Test successful login (200)
    - Test login with wrong password (401)
    - Test login with non-existent email (401)
    - Test token refresh (200)
    - Test refresh with expired token (401)
    - Test get current user (200)
    - Test logout (204)
    - Test protected endpoint without token (401)
    - Test protected endpoint with invalid token (401)
  - Use pytest with TestClient for FastAPI
  - Mock CosmosDB with fixtures for test data
  - Achieve 100% coverage of auth endpoints

### Frontend: Authentication UI

- [ ] T024 [US1] Implement LoginForm component
  - Create: `frontend/src/components/auth/LoginForm.ts` extending HTMLElement
  - Render: email input, password input, login button, error message display
  - Validate inputs with Zod schemas before submission
  - On submit:
    - Call authService.login(email, password)
    - Show loading spinner
    - Handle success: store token, redirect to dashboard
    - Handle error: display error message on form
  - Handle edge cases: form submission while loading (disable button), network error
  - Create: `frontend/tests/unit/LoginForm.test.ts` with Jest

- [ ] T025 [US1] Implement RegisterForm component
  - Create: `frontend/src/components/auth/RegisterForm.ts` extending HTMLElement
  - Render: email input, password input, confirm password input, name input, register button, error message
  - Validate inputs pre-submit with Zod schemas
  - Show password strength indicator (8+ chars, contains digit, contains letter)
  - On submit:
    - Call authService.register(email, password, name)
    - Show loading spinner
    - Handle success: store token, redirect to dashboard
    - Handle error: display error message
    - Handle 409 Conflict: show "Email already registered"
  - Create: `frontend/tests/unit/RegisterForm.test.ts`

- [ ] T026 [US1] Implement login/register page routing and navigation
  - Update: `frontend/src/pages/LoginPage.ts` to:
    - Check if already logged in → redirect to dashboard
    - Render LoginForm component
    - Add "Don't have account? Register here" link to register page
  - Update: `frontend/src/pages/RegisterPage.ts` to:
    - Check if already logged in → redirect to dashboard
    - Render RegisterForm component
    - Add "Already have account? Login here" link to login page
  - Create: `frontend/tests/unit/LoginPage.test.ts` and `RegisterPage.test.ts`
  - Verify navigation works with router

- [ ] T027 [US1] Implement logout functionality
  - Update: `frontend/src/pages/DashboardPage.ts` to add logout button
  - On logout button click:
    - Show confirmation dialog or directly call logoutlogout
    - Call authService.logout()
    - Clear auth tokens
    - Redirect to login page
    - Update app store to clear currentUser
  - Test logout in `frontend/tests/unit/DashboardPage.test.ts`

- [ ] T028 [US1] Add E2E tests for complete authentication flow
  - Create: `frontend/tests/e2e/auth.spec.ts` with Playwright:
    - Test: Register new user → verify success message → verify redirected to dashboard
    - Test: Login with valid credentials → verify logged in
    - Test: Login with invalid credentials → verify error message
    - Test: Logout → verify redirected to login
    - Test: Access protected page without authentication → verify redirected to login
    - Test: Registration with duplicate email → verify error message
    - Test: Password doesn't match confirm password → verify error before submit
  - Run tests: `npm run test:e2e`
  - All tests should pass

---

## Phase 4: User Story 2 - Session Logging (Days 13-17)

### Backend: Session CRUD API

- [ ] T029 [US2] Implement create practice session endpoint
  - Create new endpoints file or extend in: `backend/src/api/sessions.py`
  - POST `/api/sessions` endpoint:
    - Require authentication (current_user from dependency)
    - Accept SessionCreate body
    - Validate: practice_type enum, conditional tempo (required for chords/scales)
    - Set date to current date (server-side, not from request)
    - Create PracticeSession document in sessions container
    - Set partition_key = user_id
    - Return SessionResponse (201 Created)
    - Handle errors: 422 if validation fails, 401 if not authenticated

- [ ] T030 [US2] Implement get sessions endpoint
  - Add to: `backend/src/api/sessions.py`
  - GET `/api/sessions` with query parameters:
    - limit (default 20, max 100)
    - offset (default 0)
    - practice_type (optional filter)
    - date_from (optional, ISO date)
    - date_to (optional, ISO date)
  - Query sessions container: SELECT * WHERE user_id = @userId ORDER BY date DESC LIMIT/OFFSET
  - Apply optional filters on practice_type and date range
  - Return: { sessions: [], total, limit, offset }
  - Handle errors: 401 if not authenticated, invalid query parameters

- [ ] T031 [US2] Implement get single session endpoint
  - Add to: `backend/src/api/sessions.py`
  - GET `/api/sessions/{sessionId}` endpoint:
    - Require authentication
    - Query session by id and verify user_id matches current_user
    - Return SessionResponse
    - Return 404 if not found
    - Return 403 if user doesn't own session

- [ ] T032 [US2] Implement update session endpoint
  - Add to: `backend/src/api/sessions.py`
  - PUT `/api/sessions/{sessionId}` endpoint:
    - Require authentication
    - Accept SessionUpdate body (only notes can be updated)
    - Verify user owns session
    - Update notes field only
    - Return updated SessionResponse
    - Return 403 if not owner, 404 if not found

- [ ] T033 [US2] Implement delete session endpoint
  - Add to: `backend/src/api/sessions.py`
  - DELETE `/api/sessions/{sessionId}` endpoint:
    - Require authentication
    - Verify user owns session
    - Delete from sessions container
    - Return 204 No Content
    - Return 403 if not owner, 404 if not found

- [ ] T034 [US2] Write backend session CRUD tests (80%+ coverage)
  - Create: `backend/tests/integration/test_sessions_api.py` with:
    - Test create session with valid data (201)
    - Test create chords session with tempo (201)
    - Test create scales session with tempo (201)
    - Test create songs session without tempo (201)
    - Test create session without required tempo for chords (422)
    - Test create session with tempo for songs (422)
    - Test create session with tempo out of range (422)
    - Test create session with invalid practice_type (422)
    - Test list sessions (200, returns paginated list)
    - Test list sessions with filters (200)
    - Test list with limit and offset (200, pagination)
    - Test get single session (200)
    - Test get session you don't own (403)
    - Test get non-existent session (404)
    - Test update session notes (200)
    - Test update session with invalid notes (422)
    - Test delete session (204)
    - Test delete session you don't own (403)
    - Test protected endpoints without authentication (401)
  - Achieve 100% coverage of session endpoints

### Frontend: Session Logging UI

- [ ] T035 [US2] Create session API service
  - Create: `frontend/src/services/sessions.ts` with:
    - `createSession(data: SessionCreate): Promise<Session>`
    - `getSessions(limit?, offset?, type?, dateFrom?, dateTo?): Promise<SessionsPage>`
    - `getSession(id: string): Promise<Session>`
    - `updateSession(id: string, notes: string): Promise<Session>`
    - `deleteSession(id: string): Promise<void>`
    - All methods use apiClient with JWT authentication
  - Test with mocked API in `frontend/tests/unit/sessions.test.ts`

- [ ] T036 [US2] Implement SessionForm component
  - Create: `frontend/src/components/sessions/SessionForm.ts` extending HTMLElement
  - Render:
    - Practice type selector (buttons or dropdown for chords, scales, course, songs)
    - Conditional tempo input (90-120 slider or text input, shown only for chords/scales)
    - Optional notes textarea (max 500 chars, show char count)
    - Submit button
    - Cancel button (clear form)
    - Error message display
  - On practice_type change: show/hide tempo field, enable/disable based on type
  - On tempo input: validate 90-120 range, show error if invalid
  - On submit:
    - Validate form with Zod schemas
    - Call sessionsService.createSession()
    - Show loading spinner
    - Handle success: show confirmation message, clear form, emit event to update session list
    - Handle error: display error message
  - Create: `frontend/tests/unit/SessionForm.test.ts` with Jest

- [ ] T037 [US2] Implement LogSessionPage
  - Create: `frontend/src/pages/LogSessionPage.ts` extending HTMLElement
  - Render:
    - Page heading "Log Practice Session"
    - SessionForm component
    - "Back to Dashboard" link
    - Success message after session created
  - On session created:
    - Clear form
    - Show success toast "Session logged successfully"
    - Update app store with new session
    - Option to log another or go back
  - Create: `frontend/tests/unit/LogSessionPage.test.ts`

- [ ] T038 [US2] Add session logging to dashboard
  - Update: `frontend/src/pages/DashboardPage.ts` to:
    - Add "Log New Session" button
    - On click: navigate to LogSessionPage
    - Show quick stats: "You've logged X sessions this week"
  - Create: `frontend/tests/unit/DashboardPage.test.ts`

- [ ] T039 [US2] Add E2E tests for session logging flow
  - Create: `frontend/tests/e2e/sessions.spec.ts` with Playwright:
    - Test: Login → navigate to log session → log chords with tempo → verify success
    - Test: Log scales with tempo → verify success
    - Test: Log songs without tempo → verify success
    - Test: Try to log chords without tempo → verify error
    - Test: Try to log with tempo out of range → verify error
    - Test: Log multiple sessions on same day → verify all appear in list
    - Test: Log session with max length notes (500 chars) → verify success
    - Test: Try to log session with oversized notes → verify error
  - All tests should pass

---

## Phase 5: User Story 3 - History & Statistics (Days 18-22)

### Backend: Statistics API

- [ ] T040 [US3] Implement statistics endpoint
  - Create: `backend/src/services/stats_service.py` with:
    - `get_user_statistics(user_id: str, period: str) -> Statistics`
    - Calculate: total_sessions, count by type, average tempo, session streak
    - Support periods: "week", "month", "year", "all"
  - Add to: `backend/src/api/sessions.py`
  - GET `/api/sessions/stats` endpoint:
    - Require authentication
    - Query parameter: period (default "month")
    - Call stats_service.get_user_statistics()
    - Return Statistics object with:
      - total_sessions
      - by_type: { chords: {count, percentage}, scales: {...}, ... }
      - average_tempo: { chords: 105.5, scales: 110.2 }
      - recent_activity: { "2026-02-06": 2, "2026-02-05": 1, ... }
      - period
    - Handle errors: 401 if not authenticated

- [ ] T041 [US3] Write backend statistics tests
  - Create: `backend/tests/integration/test_stats_api.py` with:
    - Test get stats for user with no sessions → all zeros
    - Test get stats for user with 5 sessions → correct counts
    - Test get stats by different periods (week, month, year, all)
    - Test average tempo calculation (ignore null tempos)
    - Test percentage calculations
    - Test session streak calculation
  - Achieve 100% coverage of stats endpoint

### Frontend: History & Statistics UI

- [ ] T042 [US3] Implement SessionList component
  - Create: `frontend/src/components/sessions/SessionList.ts` extending HTMLElement
  - Render:
    - List of sessions (order by date desc)
    - Each session shows: date, practice_type, tempo (if applicable), notes preview
    - Session filters: by practice type
    - Empty state: "No sessions logged yet. Log your first session!"
    - Virtual scrolling if > 100 sessions (future optimization)
  - Properties/methods:
    - setSessions(sessions: Session[])
    - setLoading(loading: boolean)
    - onSessionDeleted(callback)
  - Click on session: show detail modal with delete option
  - Create: `frontend/tests/unit/SessionList.test.ts`

- [ ] T043 [US3] Implement StatsCard component
  - Create: `frontend/src/components/stats/StatsCard.ts` extending HTMLElement
  - Render:
    - Key metric display (e.g., "150 Total Sessions")
    - Bar chart: sessions by type (using Chart.js)
    - Line chart: sessions over time (last 30 days)
    - Doughnut chart: practice type distribution
  - Properties/methods:
    - setStatistics(stats: Statistics)
    - setLoading(loading: boolean)
  - Lazy load Chart.js only when needed (code splitting)
  - Create: `frontend/tests/unit/StatsCard.test.ts`

- [ ] T044 [US3] Implement HistoryPage
  - Create: `frontend/src/pages/HistoryPage.ts` extending HTMLElement
  - Render:
    - Page heading "Practice History"
    - Stats component (showing stats for the month)
    - Filters: practice type dropdown, date range (future enhancement)
    - SessionList component
    - "Back to Dashboard" link
  - On load:
    - Fetch sessionsService.getSessions()
    - Fetch sessionsService.getStatistics()
    - Render list and stats
    - Show loading spinners while fetching
  - On practice type filter change:
    - Refetch sessions with filter
    - Update list
  - Create: `frontend/tests/unit/HistoryPage.test.ts`

- [ ] T045 [US3] Add history link to dashboard
  - Update: `frontend/src/pages/DashboardPage.ts` to:
    - Add "View History" button
    - On click: navigate to HistoryPage
    - Show quick stat: "150 total sessions" (from cached stats)
  - Update navigation to include link to history page

- [ ] T046 [US3] Add E2E tests for history and statistics
  - Create: `frontend/tests/e2e/history.spec.ts` with Playwright:
    - Test: Login → navigate to history → verify sessions listed
    - Test: View statistics → verify charts render
    - Test: Filter by practice type → verify only that type shown
    - Test: View session details → verify all info displayed
    - Test: Delete session → verify removed from list and stats update
    - Test: Empty history message shown for new user
    - Test: Statistics match session counts
    - Test: Recent activity chart shows last 7 days
  - All tests should pass

---

## Phase 6: Polish & Cross-Cutting Concerns (Days 23-30)

### Testing & Quality

- [ ] T047 [P] Complete test coverage for all layers (80%+ total)
  - Backend: Run `pytest --cov=src --cov-report=html`
    - Target: 80%+ overall, 100% for auth and session services
    - Fill gaps with additional unit tests
    - Add integration tests for edge cases
  - Frontend: Run `npm test -- --coverage`
    - Target: 80%+ overall
    - Focus on component rendering, event handling
    - Add tests for error states and edge cases
  - Commit: Create test coverage report artifact

- [ ] T048 [P] Add accessibility tests (WCAG 2.1 AA compliance)
  - Add axe-core to Playwright tests: `npm install --save-dev @axe-core/playwright`
  - Create: `frontend/tests/e2e/accessibility.spec.ts` with:
    - Run axe scan on each page
    - Verify no accessibility violations
    - Test keyboard navigation (Tab, Enter, Escape)
    - Test screen reader with ARIA labels
    - Verify color contrast (4.5:1 for text, 3:1 for UI)
  - Run accessibility audit: all pages should pass

- [ ] T049 [P] Performance optimization and bundle analysis
  - Frontend: Run `npm run build && npm run analyze`
    - Verify bundle size < 200KB gzipped
    - Identify and optimize large dependencies
    - Lazy load Chart.js on HistoryPage only
    - Remove dead code with tree-shaking
  - Run Lighthouse: `npx lighthouse http://localhost:3000`
    - Target: LCP < 2.5s, FCP < 1.5s, TTI < 3.5s, CLS < 0.1
    - Fix performance issues: optimize images, reduce layout shifts
  - Backend: Verify API response times < 200ms with Apache Bench

- [ ] T050 [P] Security review and hardening
  - Backend:
    - Verify CORS whitelist (no wildcard in production)
    - Verify rate limiting on auth endpoints
    - Verify password hashing with bcrypt cost 12
    - Verify JWT token expiration times
    - Add security headers: X-Content-Type-Options, X-Frame-Options, CSP
    - Run OWASP dependency check: `pip install safety && safety check`
  - Frontend:
    - Verify JWT token not in localStorage (use memory or httpOnly cookie)
    - Verify no sensitive data in console logs
    - Verify API errors don't expose internal details
    - Add CSP headers in response from backend
  - Create: `docs/SECURITY.md` with security guidelines

- [ ] T051 [P] Error handling and user feedback
  - Backend:
    - Verify all endpoints return appropriate errors with `detail` field
    - Add logging for all errors (with context but not sensitive data)
    - Add request ID to all error responses for debugging
  - Frontend:
    - Verify all forms show validation errors inline
    - Verify all async operations show loading state
    - Verify all errors show user-friendly messages
    - Add error boundary component to catch unexpected errors
    - Add retry button for failed API calls
  - Test error states in E2E tests

### Documentation & Deployment

- [ ] T052 Add complete API documentation
  - OpenAPI spec is already in `specs/001-practice-tracker/contracts/openapi.yaml`
  - Generate HTML docs: backend serves Swagger UI at `/docs` (automatic with FastAPI)
  - Update: `docs/API_GUIDE.md` with examples for each endpoint
  - Add: curl examples for common workflows
  - Add: response examples with real data

- [ ] T053 Create developer setup documentation
  - Update: `README.md` with:
    - Quick start (5 min setup)
    - Development workflow
    - Common commands (build, test, run)
    - Troubleshooting section
  - Update: `docs/SETUP.md` with detailed setup instructions
  - Add: Docker Compose for one-command setup
  - Add: screenshots or GIFs of UI

- [ ] T054 Setup deployment infrastructure
  - Create: `infrastructure/bicep/main.bicep` with:
    - Azure AppService (Linux, Python 3.11, Docker)
    - Azure CosmosDB (SQL API)
    - Application Insights for monitoring
    - Key Vault for secrets management
  - Create: `infrastructure/bicep/parameters.json` for dev/staging/prod
  - Create: `infrastructure/scripts/deploy.sh` to deploy infrastructure
  - Test deployment: Deploy to dev/staging environment

- [ ] T055 Configure CI/CD deployment pipeline
  - Update: `.github/workflows/ci.yml` to add deploy job (triggered on merge to main)
  - Deployment steps:
    - Build Docker image
    - Push to Azure Container Registry
    - Deploy Azure Bicep infrastructure
    - Deploy Docker container to AppService
    - Run smoke tests
    - Create deployment artifact (link to AppService URL)
  - Configure: Branch protection rules
    - Require all checks to pass
    - Require code review approval
    - Require up-to-date branch before merge

- [ ] T056 Add monitoring and observability
  - Backend:
    - Enable Application Insights logging (Azure SDK)
    - Log all API requests (method, path, status code, response time)
    - Log all errors with full stack trace
    - Add custom metrics: session creation rate, auth success rate
    - Set up alerts: error rate > 5%, response time > 500ms
  - Frontend:
    - Integrate with Application Insights (JavaScript SDK)
    - Track page views and custom metrics
    - Log JavaScript errors
    - Track Core Web Vitals
  - Create: `docs/MONITORING.md` with dashboard setup

- [ ] T057 Create rollback and disaster recovery procedures
  - Document: Azure AppService deployment slots (blue-green deployment)
  - Document: CosmosDB point-in-time restore (30-day window)
  - Create: Health check script to verify deployment
  - Create: Rollback script to revert to previous version
  - Test: Automated rollback on failed health check

### Final Integration & Polish

- [ ] T058 End-to-end feature validation
  - Manual QA: Walk through complete user journey
    - Register new user
    - Log 5 different practice sessions (all types, with/without tempo)
    - View history and verify all sessions listed
    - Check statistics are correct
    - Filter history by practice type
    - Update session notes
    - Delete session
    - Logout and login again
    - Verify data persisted
  - Test on multiple browsers: Chrome, Firefox, Safari, Edge
  - Test on mobile: iPhone, Android
  - Verify accessibility: Test with keyboard navigation, screen reader

- [ ] T059 Code review and cleanup
  - Review backend code:
    - All functions < 50 lines
    - All error handling correct
    - All validation in place
    - Remove print statements and debug code
    - Add JSDoc comments for public APIs
  - Review frontend code:
    - All components < 200 lines
    - All types properly defined (no `any`)
    - All error states handled
    - Remove console.log statements
    - Add comments for complex logic
  - Run linters: ESLint (frontend), Ruff (backend)
  - Fix all warnings

- [ ] T060 Prepare release and documentation
  - Create: `CHANGELOG.md` with version 1.0.0 release notes
  - Create: `DEPLOYMENT.md` with step-by-step deployment guide
  - Create: `USER_GUIDE.md` with how to use the application
  - Create: `CONTRIBUTING.md` for future contributors
  - Tag: Request code review from team lead
  - Merge: Feature branch to main with merge commit
  - Tag: Create git tag v1.0.0
  - Deploy: Trigger deployment to production

---

## Task Dependencies & Execution Order

### Critical Path (Must complete in order)
1. T001-T003 (Backend setup)
2. T007-T008 (Database)
3. T011-T014 (Backend foundation)
4. T004-T006 (Frontend setup)
5. T015-T017 (Frontend foundation)
6. T018-T023 (Backend auth)
7. T024-T028 (Frontend auth)
8. T029-T034 (Backend sessions)
9. T035-T039 (Frontend sessions)
10. T040-T046 (Backend & frontend stats)

### Parallel Execution Opportunities

**Can run in parallel after each phase:**
- Setup Phase (T001-T010): All tasks can run in parallel
- Foundation Phase (T011-T017): Once databases are ready (T007-T008)
- Backend & Frontend: Can develop auth in parallel (T018-T028)
- Backend & Frontend: Can develop sessions in parallel (T029-T039)
- Backend & Frontend: Can develop stats in parallel (T040-T046)
- Polish Phase (T047-T060): Can run in parallel after feature complete

### Example Parallel Execution Plan

**Week 1 (Days 1-5)**:
- Developer A: T001-T003 (backend setup), T007-T008 (database)
- Developer B: T004-T006 (frontend setup), T009-T010 (CI/CD)
- Both: T011-T017 (foundation) once setup complete

**Week 2 (Days 6-10)**:
- Developer A: T018-T023 (backend auth)
- Developer B: T024-T028 (frontend auth)
- Both can work independently

**Week 3 (Days 11-15)**:
- Developer A: T029-T034 (backend sessions)
- Developer B: T035-T039 (frontend sessions)
- Both can work independently

**Week 4 (Days 16-20)**:
- Developer A: T040-T041 (backend stats)
- Developer B: T042-T046 (frontend stats)
- Both can work independently

**Week 5-6 (Days 21-30)**:
- Both developers: T047-T060 (testing, polish, deployment)
- Can run tests and optimization in parallel

---

## Success Criteria

Each task is complete when:
- [ ] Code is written following Constitution standards (functions < 50 lines, components < 200 lines)
- [ ] Unit/integration tests pass with > 80% coverage (100% for critical paths)
- [ ] Code passes linting (zero errors, zero warnings)
- [ ] All error cases are handled
- [ ] Accessibility requirements met (WCAG 2.1 AA)
- [ ] Performance targets met (Core Web Vitals, < 200KB bundle, < 200ms API response)
- [ ] Code reviewed and approved (< 400 lines per PR, single concern)
- [ ] Changes committed with descriptive message

---

## Estimation Summary

| Phase | Tasks | Estimated Days | Notes |
|-------|-------|-----------------|-------|
| Phase 1: Setup | T001-T010 | 4 | Can run in parallel (compress to 2-3 days with 2 devs) |
| Phase 2: Foundation | T011-T017 | 3 | Depends on Phase 1 complete |
| Phase 3: Auth [US1] | T018-T028 | 5 | Frontend + Backend can run in parallel |
| Phase 4: Sessions [US2] | T029-T039 | 5 | Frontend + Backend can run in parallel |
| Phase 5: History [US3] | T040-T046 | 5 | Frontend + Backend can run in parallel |
| Phase 6: Polish | T047-T060 | 3-5 | Testing, optimization, deployment |
| **Total** | **60 tasks** | **4-6 weeks** | **Can compress to 3-4 weeks with 2 devs** |

---

## Next Steps

1. **Review this task breakdown** with team
2. **Assign tasks** to team members
3. **Track progress** in GitHub Issues or project board
4. **Commit frequently** (after each task complete)
5. **Run tests** before committing
6. **Create PRs** for code review (< 400 lines per PR)
7. **Deploy to staging** after Phase 5 complete
8. **Deploy to production** after Phase 6 complete

---

**Ready to start development!** 🎹✨
