# Feature Specification: Piano Session Tracker

**Feature Branch**: `001-session-tracker`  
**Created**: 2026-02-07  
**Status**: Draft  
**Input**: User description: "I want to build a simple website with user login that allows to keep track of piano sessions, selecting the kind of practice that was done that day. It also shows a history of past session statistics. Each session has a selector (i.e chords, scales, course, songs). For chords and scales, it also asks for the tempo that was used (up to 180 bpm). In a near future, the website will also suggest new training sessions, and it will even be able to show chords using an image representing the piano keys with notes."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - User Registration and Authentication (Priority: P1)

As a pianist, I need to create an account and log in to the website so that I can securely track my practice sessions.

**Why this priority**: User authentication is the foundation for all other features. Without this capability, users cannot access or store their personal session data. This is the mandatory entry point to the system.

**Independent Test**: Can be fully tested by creating a new account with an email, setting a password, logging out, and logging back in. Delivers a secure account creation and authentication workflow.

**Acceptance Scenarios**:

1. **Given** I am on the registration page, **When** I enter a valid email and password and click "Sign Up", **Then** my account is created and I am logged in
2. **Given** I have a registered account, **When** I enter my email and password on the login page and click "Login", **Then** I am authenticated and taken to the dashboard
3. **Given** I entered an invalid email format, **When** I try to submit the registration form, **Then** I see an error message stating "Please enter a valid email address"
4. **Given** I entered a password that is less than 8 characters, **When** I try to submit the registration form, **Then** I see an error message stating "Password must be at least 8 characters"
5. **Given** I am logged in and click "Logout", **When** the action completes, **Then** I am redirected to the login page and my session is terminated

---

### User Story 2 - Log a Piano Practice Session with Details (Priority: P1)

As a pianist, I need to record a practice session by selecting the type, adding optional tempo, and documenting what I practiced so that I can remember what I worked on and reuse that routine later.

**Why this priority**: This is the core value proposition of the application. Users need the ability to create and save sessions immediately after creating an account to start building their practice history. Comments help users document their practice and create reusable routines. Without this feature, the application has no purpose.

**Independent Test**: Can be fully tested by logging in, creating a session with a practice type, optional tempo, and comments, and verifying it appears in the session list with comments visible. Delivers the core session recording capability with documentation.

**Acceptance Scenarios**:

1. **Given** I am logged in and on the dashboard, **When** I click "New Session", **Then** a form appears with options to select a practice type
2. **Given** the session form is open, **When** I select "Chords" from the practice type selector, **Then** a tempo input field appears allowing me to enter a value between 40-180 BPM
3. **Given** the session form is open, **When** I select "Scales" from the practice type selector, **Then** a tempo input field appears allowing me to enter a value between 40-180 BPM
4. **Given** the session form is open, **When** I select "Course" or "Songs", **Then** no tempo field is displayed (these types don't require tempo input)
5. **Given** the session form is open, **When** I look at the form, **Then** I see a "Comments" text field where I can describe what I practiced (optional, up to 500 characters)
6. **Given** I filled in all required fields (practice type and tempo if applicable), **When** I click "Save Session", **Then** the session is recorded with a timestamp and any comments, and I see a success confirmation
7. **Given** I started entering a session but don't complete it, **When** I navigate away from the form, **Then** the incomplete session data is not saved
8. **Given** I entered a tempo value outside the 40-180 BPM range, **When** I try to submit the form, **Then** I see an error message stating "Tempo must be between 40 and 180 BPM"

---

### User Story 3 - Select or Create a Practice Session Routine (Priority: P2)

As a pianist, I need to see my past practice combinations (type, tempo, comments) and quickly reuse them or create new routines so that I can efficiently log sessions without re-entering the same information.

**Why this priority**: This feature significantly improves the user experience by reducing repetitive data entry. Since many practice sessions follow similar patterns (e.g., "C Major Scales at 100 BPM"), offering them as quick-select options makes the app more useful. However, basic session logging (P1) is more critical than optimization.

**Independent Test**: Can be fully tested by logging 2-3 sessions, then starting a new session and verifying past routines appear as selectable options. Delivers efficient session creation workflow.

**Acceptance Scenarios**:

1. **Given** I am logged in and have previously logged sessions, **When** I click "New Session", **Then** I see a section showing "Past Routines" with my previous session combinations listed
2. **Given** I am viewing past routines, **When** I click on a routine (e.g., "Chords at 120 BPM - C Major arpeggios"), **Then** the form pre-fills with that routine's practice type, tempo, and comments
3. **Given** a routine is pre-selected, **When** I optionally modify any field and click "Save Session", **Then** a new session is created with the modified values
4. **Given** I have never logged a session before, **When** I click "New Session", **Then** I see no past routines section, only the "Create New Routine" form
5. **Given** I am creating a session, **When** I complete all fields and click "Save Session", **Then** this combination is automatically remembered as a routine for future sessions
6. **Given** multiple sessions have the same type/tempo/comments combination, **When** I view past routines, **Then** only one routine entry appears for that combination (de-duplicated)

---

### User Story 4 - View Session History and Statistics (Priority: P2)

As a pianist, I need to see a history of all my past practice sessions with statistics and comments so that I can understand my practice patterns and progress over time, and remind myself what I worked on.

**Why this priority**: This feature provides value to users who want to track their progress and review their practice habits. While essential for long-term engagement, the ability to log sessions (P1) is more immediately valuable than reviewing history. This can be implemented once the core logging capability is solid.

**Independent Test**: Can be fully tested by creating multiple sessions of different types with comments and verifying they appear in a chronological list with correct session details, comments, and date/time information. Delivers a functional practice history view.

**Acceptance Scenarios**:

1. **Given** I am logged in and have recorded multiple sessions, **When** I click on "Session History", **Then** I see a list of all my sessions ordered from most recent to oldest
2. **Given** I am viewing the session history, **When** I look at each session entry, **Then** I see the practice type, date, time, tempo (if applicable), and comments (if any) for that session
3. **Given** I have sessions recorded over multiple days, **When** I view the session history, **Then** I can see statistics such as total sessions logged, most frequent practice type, and average tempo for tempo-based sessions
4. **Given** I am viewing the session history, **When** I filter by a specific practice type (e.g., "Chords"), **Then** I see only sessions of that type
5. **Given** I have no sessions logged, **When** I click on "Session History", **Then** I see a message stating "No sessions logged yet. Start practicing and logging your sessions!"

---

### Edge Cases

- What happens when a user tries to input a tempo value as text instead of a number?
- How does the system handle if a user's internet connection drops while saving a session?
- What happens if a user tries to log a session with tomorrow's date or a date far in the future?
- How does the system behave if a user tries to access their history while not authenticated (e.g., session cookie expires)?
- What happens if a user enters comments longer than 500 characters?
- How does the system deduplicate routines when the same type/tempo/comments combination is logged multiple times?
- What happens to past routines if the user never logs a session again?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a registration page where users can create a new account with email and password
- **FR-002**: System MUST validate that email addresses are in a valid format before accepting account creation
- **FR-003**: System MUST enforce a minimum password length of 8 characters
- **FR-004**: System MUST provide a login page where users can authenticate with their registered email and password
- **FR-005**: System MUST maintain user sessions securely so authenticated users remain logged in across page visits
- **FR-006**: System MUST provide a logout function that terminates the user's session and redirects to login
- **FR-007**: System MUST provide a "New Session" interface accessible from the dashboard after login
- **FR-008**: System MUST allow users to select one of four practice types: Chords, Scales, Course, or Songs
- **FR-009**: System MUST display a tempo input field (range 40-180 BPM) when "Chords" or "Scales" practice type is selected
- **FR-010**: System MUST NOT display a tempo input field when "Course" or "Songs" practice type is selected
- **FR-011**: System MUST validate that tempo input for Chords and Scales is a numeric value between 40 and 180 BPM (inclusive)
- **FR-012**: System MUST provide a "Comments" text field (max 500 characters) where users can document what they practiced (optional)
- **FR-013**: System MUST record the session with the practice type, tempo (if applicable), comments (if provided), and the current date/time as soon as the user saves
- **FR-014**: System MUST persist all session data securely so that sessions remain available after logout and login
- **FR-015**: System MUST extract and remember Practice Session Routines (unique combinations of practice_type, tempo, and comments) from past sessions
- **FR-016**: System MUST display past routines as quick-select options when creating a new session
- **FR-017**: System MUST pre-fill the new session form with practice_type, tempo, and comments when a user selects a past routine
- **FR-018**: System MUST allow users to modify pre-filled routine values before saving
- **FR-019**: System MUST deduplicate routines so only one appears per unique combination of practice_type, tempo, and comments
- **FR-020**: System MUST provide a "Session History" view that displays all logged sessions for the authenticated user
- **FR-021**: System MUST display sessions in reverse chronological order (most recent first) in the Session History view
- **FR-022**: System MUST show for each session: practice type, date, time, tempo (if applicable), and comments (if provided)
- **FR-023**: System MUST calculate and display aggregate statistics including: total sessions logged and most frequent practice type
- **FR-024**: System MUST allow users to filter the session history by practice type
- **FR-025**: System MUST display a helpful message when a user has no sessions logged yet
- **FR-026**: System MUST handle invalid input in tempo fields by displaying a user-friendly error message
- **FR-027**: System MUST truncate comments longer than 500 characters or reject them with an error message

### Key Entities

- **User**: Represents a registered pianist with a unique email address, hashed password, and an account creation timestamp. Each user can have many sessions and routines associated with their account.
- **PracticeSession**: Represents a single practice session logged by a user, containing the practice type (Chords, Scales, Course, or Songs), optional tempo value (40-180 BPM for tempo-based types), optional comments (up to 500 characters describing what was practiced), session date, and session time. Each session belongs to exactly one user.
- **PracticeRoutine**: Represents a reusable practice template derived from unique combinations of practice_type, tempo (if applicable), and comments. When a user logs a session with the same combination multiple times, it becomes a routine available for quick selection. Each routine belongs to one user and is displayed as a quick-select option when creating new sessions.
- **PracticeType**: Represents the classification of a practice session. Values are: Chords, Scales, Course, Songs. Each practice type has different associated metadata requirements (tempo for Chords and Scales only).

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can register, log in, and securely access their personal session data without seeing other users' data
- **SC-002**: Users can log a new practice session (with all required fields and optional comments) in under 1 minute after choosing to create a session
- **SC-003**: All practice sessions are persisted and available in the session history immediately after creation (no data loss)
- **SC-004**: Session history displays all logged sessions with 100% accuracy of recorded practice type, date, time, tempo, and comments
- **SC-005**: The application correctly calculates and displays session statistics (total count, most frequent practice type) with zero calculation errors
- **SC-006**: Session filtering by practice type returns only sessions of the selected type with 100% accuracy
- **SC-007**: Form validation prevents invalid data entry (invalid email, short passwords, out-of-range tempos, oversized comments) and provides clear error messages
- **SC-008**: Past practice routines are displayed as quick-select options, reducing session creation time for returning users
- **SC-009**: Routines are correctly deduplicated so each unique combination of type/tempo/comments appears only once in the routine list
- **SC-010**: Pre-filled routine values can be modified before saving without errors
- **SC-011**: The system supports at least 100 concurrent users without degradation in response times for session logging and retrieval
- **SC-012**: System responds to user actions (session creation, history retrieval, filtering, routine selection) in under 2 seconds in normal operating conditions

## Assumptions

- Email/password authentication is sufficient for MVP; no SSO or OAuth integration is required at this stage
- A user's practice history is personal to that user; no sharing or collaboration features are in scope
- Session data does not require real-time synchronization across devices; eventual consistency is acceptable
- All sessions are recorded with the user's local time; timezone conversion is not required for MVP
- Future feature items (session suggestions, piano key visualizations) are not included in this MVP specification
- Users may log sessions from the current date only; backdating or future-dating sessions beyond reasonable bounds should be prevented
- Routines are automatically derived from past sessions; users cannot manually create routines without logging a session first
- Comments are free-form text (no markdown, no special formatting required)
- Routines are shown in order of most recently used for quick access
- When a user selects a routine, all fields are pre-filled; they can optionally modify any field, and saving creates a new session (not modifying the routine)
