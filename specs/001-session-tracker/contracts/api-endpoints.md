# Piano Session Tracker - API Contracts

**Feature**: Piano Session Tracker | **Branch**: 001-session-tracker | **Created**: 2026-02-07

## Overview

All endpoints use standard HTTP methods and form-based submission. Server-side rendering returns HTML pages. Authentication is session-based with secure cookies.

---

## Authentication

### Session Management

All authenticated endpoints require an active session cookie (`session`).

**Session Requirements**:
- Session cookie set after successful login
- Session cookie removed after logout
- Session expires after 24 hours of inactivity (configurable)
- Secure cookie flag enabled (HTTPS in production)
- HttpOnly flag enabled (prevent JavaScript access)

---

## Endpoint Specifications

### 1. GET /

**Purpose**: Landing page for unauthenticated users

**Method**: `GET`

**Authentication**: None

**Response**: 
- **Status**: `200 OK`
- **Body**: HTML page with navigation to Register or Login

**Behavior**:
- If user is authenticated, redirect to `/dashboard` (302 Found)
- Display links to `/register` and `/login` endpoints

---

### 2. POST /register

**Purpose**: Create a new user account

**Method**: `POST`

**Authentication**: None

**Request**:

```
Content-Type: application/x-www-form-urlencoded

email=user@example.com&password=MySecurePassword123&password_confirm=MySecurePassword123
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `email` | String | Yes | Valid email format, max 255 chars, must be unique |
| `password` | String | Yes | Min 8 chars, max 255 chars |
| `password_confirm` | String | Yes | Must match `password` |

**Response - Success**:
- **Status**: `302 Found` (Redirect to `/dashboard`)
- **Headers**: `Set-Cookie: session=<token>`
- **Body**: None

**Response - Validation Error**:
- **Status**: `400 Bad Request`
- **Body**: HTML registration form with inline error messages
- **Errors Shown**:
  - "Please enter a valid email address" (if email format invalid)
  - "Email already in use. Please use a different email." (if email exists)
  - "Password must be at least 8 characters" (if password too short)
  - "Passwords do not match" (if password_confirm != password)

**Behavior**:
- Validate all inputs on server (even if client-side validation exists)
- Hash password using werkzeug.security.generate_password_hash
- Create User record in database
- Establish authenticated session
- Redirect to dashboard

---

### 3. GET /login

**Purpose**: Display login form

**Method**: `GET`

**Authentication**: None

**Response**:
- **Status**: `200 OK`
- **Body**: HTML login form with email and password fields

**Behavior**:
- If user is authenticated, redirect to `/dashboard` (302 Found)

---

### 4. POST /login

**Purpose**: Authenticate user and create session

**Method**: `POST`

**Authentication**: None

**Request**:

```
Content-Type: application/x-www-form-urlencoded

email=user@example.com&password=MySecurePassword123
```

| Field | Type | Required |
|-------|------|----------|
| `email` | String | Yes |
| `password` | String | Yes |

**Response - Success**:
- **Status**: `302 Found` (Redirect to `/dashboard`)
- **Headers**: `Set-Cookie: session=<token>`

**Response - Authentication Failure**:
- **Status**: `400 Bad Request`
- **Body**: HTML login form with error message "Invalid email or password"

**Behavior**:
- Look up user by email
- If not found or password mismatch, show generic error (do not reveal which field is wrong)
- Use werkzeug.security.check_password_hash to verify password
- Create session cookie on success
- Redirect to dashboard

---

### 5. GET /logout

**Purpose**: Terminate user session

**Method**: `GET`

**Authentication**: Required (session cookie)

**Response**:
- **Status**: `302 Found` (Redirect to `/`)
- **Headers**: `Set-Cookie: session=; Max-Age=0` (clear cookie)

**Behavior**:
- Clear session from server-side storage
- Delete session cookie from browser
- Redirect to landing page

---

### 6. GET /dashboard

**Purpose**: Display user dashboard

**Method**: `GET`

**Authentication**: Required

**Response - Success**:
- **Status**: `200 OK`
- **Body**: HTML dashboard page showing:
  - "New Session" button/link → `/session/new`
  - "Session History" button/link → `/session/history`
  - Welcome message with user's email
  - Quick stats: Total sessions logged, most frequent practice type (from history data)

**Response - Unauthenticated**:
- **Status**: `302 Found` (Redirect to `/login`)

---

### 7. GET /session/new

**Purpose**: Display form to create a new practice session with past routines and optional comments

**Method**: `GET`

**Authentication**: Required

**Response - Success**:
- **Status**: `200 OK`
- **Body**: HTML form with sections:

    **Past Routines Section** (if user has logged sessions before):
    - Heading: "Quick Select: Past Routines"
    - List showing all unique past practice combinations (sorted by most recently used)
    - Each routine displays: `{practice_type}` + (` at {tempo} BPM` if applicable) + (` - {comments}` if comments exist)
    - Clicking a routine pre-fills the form below with that routine's values

    **Create New/Edit Routine Section**:
    - Practice Type selector (dropdown or radio buttons): Chords, Scales, Course, Songs
    - Tempo input field (hidden by default, shown via JavaScript if Chords/Scales selected, or shown on page load if previously submitted)
    - Comments textarea field (optional, max 500 characters, shows character count)
    - "Save Session" button

**Response - Unauthenticated**:
- **Status**: `302 Found` (Redirect to `/login`)

**Dynamic Behavior**:
- When practice type changes, show/hide tempo field based on selection
- Tempo input has HTML5 `type="number"` with `min="40"` `max="180"`
- Tempo input is required if practice_type = Chords or Scales
- When user clicks a routine, JS pre-fills form and highlights the selected routine
- Comments field shows live character count (e.g., "45 / 500 characters")
- Routine selection can be modified before saving (user can edit pre-filled values)

---

### 8. POST /session

**Purpose**: Save a new practice session and create/update a routine

**Method**: `POST`

**Authentication**: Required

**Request**:

```
Content-Type: application/x-www-form-urlencoded

practice_type=Chords&tempo=120&comments=C%20Major%20arpeggios%20at%20increasing%20tempos
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `practice_type` | String | Yes | One of: Chords, Scales, Course, Songs |
| `tempo` | Integer | Conditional | Required if practice_type = Chords or Scales; must be 40-180; else omitted |
| `comments` | String | No | Optional free text (max 500 chars); can be empty/omitted |

**Response - Success**:
- **Status**: `302 Found` (Redirect to `/session/history?new=true`)
- **Body**: None
- **Page Render**: History page shows success message: "Session logged successfully!"

**Response - Validation Error**:
- **Status**: `400 Bad Request`
- **Body**: HTML form (same as GET /session/new) with inline error messages and retained form values
- **Errors Shown**:
  - "Please select a practice type" (if practice_type missing)
  - "Invalid practice type" (if practice_type not in enum)
  - "Tempo is required for Chords and Scales" (if tempo missing for tempo-based types)
  - "Tempo must be a number" (if tempo is not numeric)
  - "Tempo must be between 40 and 180 BPM" (if tempo out of range)
  - "Comments must be 500 characters or less" (if comments too long)

**Response - Unauthenticated**:
- **Status**: `302 Found` (Redirect to `/login`)

**Session Creation & Routine Management**:
- Create PracticeSession record with:
  - `user_id` from authenticated session
  - `practice_type` from form
  - `tempo` from form (null if not applicable)
  - `comments` from form (null if empty; max 500 chars)
  - `session_date` = today's date
  - `session_time` = current time
  - `created_at` = current UTC timestamp
- Check if a routine exists with same (user_id, practice_type, tempo, comments):
  - If exists: Update routine's `last_used_at` = current timestamp
  - If does not exist: Create new routine record with these values and `last_used_at` = current timestamp
- Commit transaction
- Redirect to history with success indicator

---

### 9. GET /session/history

**Purpose**: Display user's session history with filtering, statistics, and comments

**Method**: `GET`

**Authentication**: Required

**Query Parameters**:

| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `type` | String | Yes | Filter by practice type: Chords, Scales, Course, Songs |
| `new` | String | Yes | When present, show success message "Session logged successfully!" |

**Response - Success**:
- **Status**: `200 OK`
- **Body**: HTML page showing:

    **Statistics Section**:
    - Total sessions logged: `<number>`
    - Most frequent practice type: `<type>` (or "None yet" if no sessions)
    - Average tempo (tempo-based sessions): `<number>` BPM (or "N/A" if no tempo sessions)

    **Filter Section**:
    - Dropdown to select practice type (All, Chords, Scales, Course, Songs)
    - "Filter" button to apply filter

    **Success Message** (if ?new=true):
    - "Session logged successfully!" (green alert box)

    **Session List**:
    - If no sessions: "No sessions logged yet. Start practicing and logging your sessions!"
    - If sessions exist: Table or list showing each session with columns:
      - Date (e.g., "Feb 7, 2026")
      - Time (e.g., "14:30")
      - Practice Type (e.g., "Chords")
      - Tempo (e.g., "120 BPM") or "(No tempo)" if N/A
      - Comments (e.g., "C Major arpeggios") or "(No notes)" if empty; truncate to ~100 chars if longer
    - Ordered from most recent to oldest (DESC by session_date, then session_time)

**Response - Unauthenticated**:
- **Status**: `302 Found` (Redirect to `/login`)

**Filtering Behavior**:
- If `?type=Chords`, show only sessions where practice_type = 'Chords'
- If `?type` is missing or `?type=All`, show all sessions for user
- If `?type` is invalid, show all sessions (fallback gracefully)

---

## Error Responses

### 404 Not Found

**When**: User navigates to non-existent route

**Response**:
- **Status**: `404 Not Found`
- **Body**: HTML error page with message "Page not found" and link back to dashboard

### 500 Internal Server Error

**When**: Unhandled server exception occurs

**Response**:
- **Status**: `500 Internal Server Error`
- **Body**: HTML error page with generic message "Something went wrong. Please try again later." (no details)
- **Logging**: Server logs exception for debugging

---

## Security Considerations

### Password Hashing

All passwords are hashed using `werkzeug.security.generate_password_hash()` with:
- Default algorithm: pbkdf2:sha256
- Salt automatically generated
- Never store plaintext passwords

### Session Security

- Session tokens are cryptographically random (generated by Flask session management)
- Secure flag set in production (HTTPS only)
- HttpOnly flag set (no JavaScript access)
- Max-Age set for automatic expiration

### Input Validation

All user inputs validated on server:
- Email format validation
- Enum value validation for practice_type
- Numeric range validation for tempo
- Required field validation

### SQL Injection Prevention

- All database queries use SQLAlchemy ORM with parameterized queries
- No raw SQL strings in code
- Framework handles escaping automatically

### CSRF Protection

- Flask-WTF recommended for production (not required for MVP)
- Minimal form complexity reduces CSRF risk
- Session-based authentication sufficient for MVP

---

## Testing Contracts

Each endpoint should have integration tests covering:
- Happy path (valid input, expected behavior)
- Input validation failures (each validation error message)
- Authentication requirements (unauthenticated users redirected)
- State changes (verify database records created/modified correctly)

See `tests/` directory in source code for implementation.
