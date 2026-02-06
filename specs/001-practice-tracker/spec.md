# Feature Specification: Piano Practice Session Tracker

**Feature Branch**: `001-practice-tracker`  
**Created**: 2026-02-06  
**Status**: Draft  
**Input**: User description: "This is a simple website with user login that allows to keep track of piano sessions, selecting the kind of practice that was done that day. It also shows a history of past session statistics. Each session has a selector (i.e chords, scales, course, songs). For chords and scales, it also asks for the tempo that was used (90 to 120 bpm). In a near future, the website will also suggest new training sessions, and it will even be able to show chords using an image representing the piano keys with notes."

## Clarifications

### Session 2026-02-06

- Q: How should future enhancements (practice recommendations, visual chord reference) be handled relative to this feature? → A: Create them as separate future features entirely (not mentioned in this spec)
- Q: Should tempo values accept decimals (105.5 bpm) or only integers (105 bpm)? → A: Accept only integer values (90, 91, 92... 120) - reject decimals with validation error
- Q: When a user logs multiple sessions on the same day, how should they be distinguished in the history view? → A: Display sessions with date only, multiple entries per date sequentially
- Q: Should session history use pagination, infinite scrolling, or show all sessions? → A: Show all sessions without pagination initially (add pagination only if needed later)
- Q: Can users backdate sessions or only use current date? → A: Current date only (not editable) - users cannot backdate sessions

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication (Priority: P1)

As a piano student, I need to create an account and log in to the website so that I can securely access my personal practice tracking data.

**Why this priority**: Authentication is the foundation that enables all other features. Without it, users cannot access personalized session tracking. This is the entry point for the entire application.

**Independent Test**: Can be fully tested by attempting account creation with valid/invalid credentials and verifying login/logout functionality. Delivers secure access to the application.

**Acceptance Scenarios**:

1. **Given** I am a new user on the registration page, **When** I provide a valid email and password, **Then** my account is created and I am logged into the system
2. **Given** I am an existing user on the login page, **When** I enter my correct credentials, **Then** I am successfully logged into my account
3. **Given** I am logged in, **When** I choose to log out, **Then** I am logged out and redirected to the login page
4. **Given** I am on the login page, **When** I enter incorrect credentials, **Then** I see an error message and remain on the login page

---

### User Story 2 - Log Practice Session (Priority: P2)

As a piano student, I want to log my practice sessions by selecting the type of practice I did, so that I can keep a record of my training activities.

**Why this priority**: This is the core value proposition of the application. Logging sessions is the primary action users will take and the foundation for all tracking and analytics features.

**Independent Test**: Can be fully tested by logging in and creating sessions with different practice types (chords, scales, course, songs). Delivers immediate value by capturing practice data.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I navigate to the session logging page, **Then** I see options to select practice type: chords, scales, course, or songs
2. **Given** I am on the session logging page, **When** I select a practice type and submit, **Then** my session is saved with the current date and selected type
3. **Given** I select "chords" as practice type, **When** I proceed to log the session, **Then** I am prompted to enter the tempo used (90-120 bpm)
4. **Given** I select "scales" as practice type, **When** I proceed to log the session, **Then** I am prompted to enter the tempo used (90-120 bpm)
5. **Given** I select "course" or "songs" as practice type, **When** I proceed to log the session, **Then** the session is saved without requiring tempo input
6. **Given** I am entering tempo for chords or scales, **When** I enter a value outside 90-120 bpm range, **Then** I see a validation error message
7. **Given** I have completed all required fields, **When** I submit the session, **Then** I see a confirmation message and the form is cleared for the next session

---

### User Story 3 - View Session History (Priority: P3)

As a piano student, I want to view my past practice sessions with statistics, so that I can track my progress and maintain motivation.

**Why this priority**: Viewing history transforms individual session logging into a meaningful tracking system. It provides the "why" behind logging sessions and enables users to see patterns and progress over time.

**Independent Test**: Can be fully tested by logging in, viewing the history page, and verifying that previously logged sessions are displayed with relevant statistics. Delivers value by making practice patterns visible.

**Acceptance Scenarios**:

1. **Given** I am logged in and have previously logged sessions, **When** I navigate to the history page, **Then** I see a list of my past sessions showing date, practice type, and tempo (where applicable)
2. **Given** I am viewing my session history, **When** I look at the statistics summary, **Then** I see total number of sessions, sessions by type, and recent activity patterns
3. **Given** I am a new user with no logged sessions, **When** I navigate to the history page, **Then** I see a message encouraging me to log my first practice session
4. **Given** I am viewing sessions that include chords or scales, **When** I look at the details, **Then** the tempo information (90-120 bpm) is displayed alongside the session type
5. **Given** I have multiple sessions logged, **When** I view the history, **Then** sessions are ordered by date with the most recent first

---

### Edge Cases

- What happens when a user tries to log multiple practice sessions on the same day? (System allows multiple sessions per day; they appear as separate entries with the same date in history)
- What if a user forgets to log a session and wants to add it later? (System only supports current date; backdating is not available in this version)
- What happens when a user navigates away during session logging without submitting? (Unsaved data should be lost, or user should be warned)
- How does the system behave if a user has no internet connection while trying to log a session? (System should show appropriate error message)
- What happens when a user tries to access the application without being logged in? (System should redirect to login page)
- How does the system handle sessions logged in different time zones? (System should use user's local time or UTC consistently)
- What happens when viewing history with hundreds of logged sessions? (System displays all sessions; pagination can be added later if performance degrades)
- How does the system handle invalid characters or excessively long inputs in session fields? (System should validate and sanitize all inputs)

## Requirements *(mandatory)*

### Functional Requirements

**Authentication & User Management**

- **FR-001**: System MUST allow new users to create an account using email and password
- **FR-002**: System MUST validate email addresses are in proper format before account creation
- **FR-003**: System MUST validate passwords meet minimum security requirements (minimum 8 characters)
- **FR-004**: System MUST allow existing users to log in with their credentials
- **FR-005**: System MUST allow logged-in users to log out of their session
- **FR-006**: System MUST prevent access to session logging and history features for non-authenticated users
- **FR-007**: System MUST display appropriate error messages for invalid login attempts

**Session Logging**

- **FR-008**: System MUST allow authenticated users to log a practice session
- **FR-009**: System MUST provide four practice type options: chords, scales, course, songs
- **FR-010**: System MUST require tempo input (90-120 bpm) when practice type is "chords"
- **FR-011**: System MUST require tempo input (90-120 bpm) when practice type is "scales"
- **FR-012**: System MUST NOT require tempo input when practice type is "course" or "songs"
- **FR-013**: System MUST validate tempo values are integer numbers within 90-120 bpm range (no decimal values)
- **FR-014**: System MUST automatically record the current date when a session is logged (date is not user-editable; backdating is not supported)
- **FR-015**: System MUST allow users to log multiple practice sessions per day
- **FR-016**: System MUST confirm successful session logging with a clear message
- **FR-017**: System MUST associate each logged session with the currently authenticated user

**Session History & Statistics**

- **FR-018**: System MUST display a list of all previously logged sessions for the authenticated user
- **FR-019**: System MUST show session date, practice type, and tempo (when applicable) for each logged session
- **FR-020**: System MUST sort sessions by date with most recent sessions appearing first
- **FR-021**: System MUST display summary statistics including total number of sessions
- **FR-022**: System MUST display session count broken down by practice type
- **FR-023**: System MUST show recent activity patterns (e.g., sessions in the last week/month)
- **FR-024**: System MUST display an appropriate message when a user has no logged sessions yet
- **FR-025**: System MUST display all logged sessions for the user (pagination can be added in future if performance requires)

### Key Entities

- **User**: Represents a piano student who uses the application to track practice sessions. Key attributes include unique identifier, email address, password (encrypted), and account creation date. Each user has exclusive access to their own session data.

- **Practice Session**: Represents a single practice activity logged by a user. Key attributes include unique identifier, associated user, practice date, practice type (chords/scales/course/songs), and optional tempo value (90-120 bpm, required only for chords and scales). Sessions belong to exactly one user and are ordered chronologically.

### Assumptions

- User authentication uses email/password as the primary method (standard for simple web applications)
- Sessions track date but not specific start/end times or duration (not specified in requirements; can be added in future iterations)
- Tempo values are accepted as integers only within the 90-120 range (decimal values are not supported and will be rejected during validation)
- System is designed for single-user personal tracking (no sharing or multi-user collaboration features)
- Each user's session data is private and not visible to other users
- Session history displays all sessions without filtering options initially (filtering by type or date range can be added later)
- System operates with standard internet connection; offline functionality is not part of initial requirements

## Success Criteria *(mandatory)*

### Measurable Outcomes

**User Onboarding & Authentication**

- **SC-001**: New users can create an account and log in within 2 minutes
- **SC-002**: 95% of login attempts with correct credentials succeed on first try
- **SC-003**: Users receive clear feedback within 3 seconds for authentication errors

**Session Logging Efficiency**

- **SC-004**: Users can log a complete practice session (including tempo when required) in under 30 seconds
- **SC-005**: 100% of session submissions with valid data are successfully saved
- **SC-006**: Tempo validation catches and reports errors within 1 second of input
- **SC-007**: Users can log multiple sessions per day without confusion or errors

**History & Statistics Value**

- **SC-008**: Users can view their session history within 2 seconds of navigation
- **SC-009**: Session history clearly displays all required information (date, type, tempo) without scrolling for up to 20 sessions
- **SC-010**: Statistics summary provides meaningful insights (total count, breakdown by type) at a glance
- **SC-011**: System displays session history correctly even with 100+ logged sessions

**User Satisfaction & Adoption**

- **SC-012**: 80% of users who create an account log at least one session
- **SC-013**: 90% of users successfully complete their intended task (log session or view history) on first attempt
- **SC-014**: Users understand which practice types require tempo input without external documentation
- **SC-015**: Zero security vulnerabilities in authentication system that could expose user data
