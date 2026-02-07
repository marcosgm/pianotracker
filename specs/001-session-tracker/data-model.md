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
│ created_at  │         │ session_date     │
│             │         │ session_time     │
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

**Purpose**: Record a single practice session logged by a user with type, optional tempo, and timestamp.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `id` | Integer | PRIMARY KEY, NOT NULL, AUTO INCREMENT | Unique session identifier |
| `user_id` | Integer | NOT NULL, FOREIGN KEY → User.id | Reference to the owning User |
| `practice_type` | String (20) | NOT NULL, ENUM ('Chords', 'Scales', 'Course', 'Songs') | Type of practice performed |
| `tempo` | Integer | NULLABLE | BPM value; only applicable when practice_type = 'Chords' or 'Scales'; else NULL |
| `session_date` | Date | NOT NULL | Date when the practice occurred (e.g., 2026-02-07) |
| `session_time` | Time | NOT NULL | Time when the practice started (e.g., 14:30:00) |
| `created_at` | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp when record was created (UTC) |

**Validation Rules**:
- `practice_type` must be one of: 'Chords', 'Scales', 'Course', 'Songs'
- `tempo` must be NULL if practice_type is 'Course' or 'Songs'
- `tempo` must be between 40 and 180 (inclusive) if practice_type is 'Chords' or 'Scales'
- `tempo` must be numeric (if provided)
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

## Key Design Decisions

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
- If User is deleted, all PracticeSessions are cascade-deleted
- No orphaned sessions; data integrity maintained
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
