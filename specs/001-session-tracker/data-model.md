# Data Model: Piano Session Tracker

**Feature**: Piano Session Tracker | **Branch**: 001-session-tracker | **Created**: 2026-02-07

## Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────────┐
│    User     │────1:N──│ PracticeSession  │
├─────────────┤         ├──────────────────┤
│ id (PK)     │         │ id (PK)          │
│ email       │         │ user_id (FK)     │
│ password_   │         │ practice_type    │
│   hash      │         │ tempo (nullable) │
│ created_at  │         │ comments         │
│             │         │ session_date     │
│             │         │ session_time     │
│             │         │ created_at       │
│             │         
│             │         ┌──────────────────┐
│             │ ────1:N─│ PracticeRoutine  │
│             │         ├──────────────────┤
│             │         │ id (PK)          │
│             │         │ user_id (FK)     │
│             │         │ practice_type    │
│             │         │ tempo (nullable) │
│             │         │ comments         │
│             │         │ last_used_at     │
│             │         │ created_at       │
└─────────────┘         └──────────────────┘
```

---

## Entity Specifications

### User

**Purpose**: Represent a registered pianist with secure account credentials.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `id` | Integer | PRIMARY KEY, NOT NULL, AUTO INCREMENT | Unique user identifier |
| `email` | String (255) | UNIQUE, NOT NULL | Email address for login; must be valid email format |
| `password_hash` | String (255) | NOT NULL | Hashed password using werkzeug.security (salted bcrypt-equivalent) |
| `created_at` | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp in UTC |

**Validation Rules**:
- Email must match regex pattern for valid email format (e.g., `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
- Email must be unique across all users (enforced by UNIQUE constraint)
- Password must be at least 8 characters (validated before hashing)
- Password is never stored plaintext; only `password_hash` is persisted

**Relationships**:
- One User has many PracticeSessions (1:N)
- When a User is deleted, all associated PracticeSessions must be deleted (CASCADE)

**Indexes**:
- UNIQUE on `email` (for login lookups)

---

### PracticeSession

**Purpose**: Record a single practice session logged by a user with type, optional tempo, optional comments, and timestamp.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `id` | Integer | PRIMARY KEY, NOT NULL, AUTO INCREMENT | Unique session identifier |
| `user_id` | Integer | NOT NULL, FOREIGN KEY → User.id | Reference to the owning User |
| `practice_type` | String (20) | NOT NULL, ENUM ('Chords', 'Scales', 'Course', 'Songs') | Type of practice performed |
| `tempo` | Integer | NULLABLE | BPM value; only applicable when practice_type = 'Chords' or 'Scales'; else NULL |
| `comments` | Text | NULLABLE | Free-form text (max 500 characters) describing what was practiced (e.g., "C Major scales, increasing tempo gradually") |
| `session_date` | Date | NOT NULL | Date when the practice occurred (e.g., 2026-02-07) |
| `session_time` | Time | NOT NULL | Time when the practice started (e.g., 14:30:00) |
| `created_at` | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp when record was created (UTC) |

**Validation Rules**:
- `practice_type` must be one of: 'Chords', 'Scales', 'Course', 'Songs'
- `tempo` must be NULL if practice_type is 'Course' or 'Songs'
- `tempo` must be between 40 and 180 (inclusive) if practice_type is 'Chords' or 'Scales'
- `tempo` must be numeric (if provided)
- `comments` must be max 500 characters (rejected or truncated if longer)
- `comments` is optional; NULL is valid
- `session_date` must not be in the future (cannot log sessions for tomorrow)
- `session_date` must not be more than 30 days in the past (prevent accidental backdating)
- `session_time` must be in valid time format (00:00:00 to 23:59:59)
- `user_id` must reference an existing User

**Relationships**:
- Many PracticeSessions belong to one User (N:1)
- User is foreign key; enforced by database constraint

**Indexes**:
- Index on `user_id` (for efficient filtering by user)
- Index on `user_id, session_date DESC` (for efficient history retrieval in reverse chronological order)
- Index on `user_id, practice_type` (for efficient filtering by type)

---

### PracticeRoutine

**Purpose**: Remember and offer quick-select options for frequently used practice combinations (practice_type, tempo, comments).

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `id` | Integer | PRIMARY KEY, NOT NULL, AUTO INCREMENT | Unique routine identifier |
| `user_id` | Integer | NOT NULL, FOREIGN KEY → User.id | Reference to the owning User |
| `practice_type` | String (20) | NOT NULL, ENUM ('Chords', 'Scales', 'Course', 'Songs') | Type of practice for this routine |
| `tempo` | Integer | NULLABLE | BPM value; only applicable when practice_type = 'Chords' or 'Scales'; else NULL |
| `comments` | Text | NULLABLE | Free-form text (max 500 characters) describing the routine |
| `last_used_at` | DateTime | NULLABLE | Timestamp when this routine was last used (for sorting routines by recency) |
| `created_at` | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp when routine was first created (UTC) |

**Validation Rules**:
- `practice_type` must be one of: 'Chords', 'Scales', 'Course', 'Songs'
- `tempo` must be NULL if practice_type is 'Course' or 'Songs'
- `tempo` must be between 40 and 180 (inclusive) if practice_type is 'Chords' or 'Scales'
- `comments` must be max 500 characters
- `comments` is optional; NULL is valid
- Combination of `user_id`, `practice_type`, `tempo`, and `comments` must be unique (no duplicate routines per user)
- Database enforces uniqueness with UNIQUE constraint on (user_id, practice_type, tempo, comments)

**Relationships**:
- Many PracticeRoutines belong to one User (N:1)
- User is foreign key; enforced by database constraint
- When a User is deleted, all associated PracticeRoutines are deleted (CASCADE)

**Indexes**:
- Index on `user_id` (for retrieving user's routines)
- Index on `user_id, last_used_at DESC` (for efficient sorting by recency)
- UNIQUE constraint on (user_id, practice_type, tempo, comments) (for deduplication)

**Notes**:
- Routines are NOT manually created; they are automatically derived from sessions
- When a user saves a session, the system checks if a routine with the same practice_type, tempo, and comments exists
- If routine exists, update `last_used_at` timestamp
- If routine does not exist, create a new routine record
- When displaying routines, order by `last_used_at DESC` (most recently used first)
- Routines with NULL `last_used_at` are new routines not yet used (theoretical case)



---

## Key Design Decisions

### Comments and Routines

- `comments` field is optional (nullable) to support users who prefer not to document their sessions
- Routines are NOT a separate user-created entity; they are automatically derived from the unique combinations of practice_type, tempo, and comments already saved in sessions
- When a session is saved, the system checks if a routine with that exact combination exists and either creates a new routine or updates the `last_used_at` timestamp
- This approach avoids requiring users to manage routines separately and ensures routines always reflect actual practice patterns
- Routines are displayed ordered by `last_used_at DESC` to show most-recently used practices first
- Comments are limited to 500 characters to keep them brief but meaningful; longer documentation can be tracked externally

### Timezone Handling
- Store `session_time` as local time (no timezone conversion in MVP)
- User is responsible for selecting correct time when logging session
- Future feature: Add timezone field to User if cross-device sync is needed

### Tempo as Optional Field
- `tempo` is nullable in database to support both tempo-based (Chords, Scales) and non-tempo (Course, Songs) practice types
- Application layer enforces that tempo is either required or forbidden based on practice_type
- Database constraint would require CHECK clause, but validation is simpler in application

### Date/Time Separation
- `session_date` and `session_time` are separate fields for flexibility
- Allows filtering by date easily in queries
- Combined they form the complete session timestamp
- `created_at` is separate and tracks when the record was saved (useful for auditing)

### Deletion Cascade
- If User is deleted, all PracticeSessions and PracticeRoutines are cascade-deleted
- No orphaned sessions or routines; data integrity maintained
- Explicit confirmation UI required before user deletion (future feature)

---

## Statistics Calculations (Not Stored, Computed)

### Total Sessions
```sql
SELECT COUNT(*) AS total_sessions 
FROM PracticeSession 
WHERE user_id = ?
```

### Most Frequent Practice Type
```sql
SELECT practice_type, COUNT(*) AS frequency
FROM PracticeSession
WHERE user_id = ?
GROUP BY practice_type
ORDER BY frequency DESC
LIMIT 1
```

### Average Tempo (Tempo-based Sessions Only)
```sql
SELECT AVG(tempo) AS avg_tempo
FROM PracticeSession
WHERE user_id = ? 
  AND practice_type IN ('Chords', 'Scales')
  AND tempo IS NOT NULL
```

---

## Migration & Deployment Notes

### Schema Creation Order
1. Create `User` table (no dependencies)
2. Create `PracticeSession` table with FOREIGN KEY to User

### SQLite Compatibility
- SQLite does not support ENUM type; `practice_type` is String with CHECK constraint in DDL
- SQLite cascading deletes must be enabled: `PRAGMA foreign_keys = ON`
- DateTime columns use ISO 8601 format strings in SQLite

### Future Migration Path
- PostgreSQL migration: Change `practice_type` to ENUM type for better type safety
- Add timezone field to User: `timezone VARCHAR(50) DEFAULT 'UTC'`
- Add session end_time optional field: `session_end_time TIME NULLABLE`
- Add session notes field: `notes TEXT NULLABLE`
