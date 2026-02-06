# Phase 1: Data Model Design

**Feature**: Piano Practice Session Tracker  
**Date**: 2026-02-06  
**Phase**: Data Model & Entity Design

---

## Overview

This document defines the data model for the Piano Practice Session Tracker feature, including entity schemas, relationships, validation rules, and storage patterns. The model is designed for Azure CosmosDB (NoSQL document database) with a focus on query performance and partition key optimization.

---

## Entity Definitions

### Entity 1: User

**Purpose**: Represents a piano student who uses the application to track practice sessions.

**Attributes**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | string (UUID) | Yes | Unique, immutable | Primary identifier |
| `email` | string | Yes | Valid email format, unique, lowercase | User login credential |
| `password_hash` | string | Yes | bcrypt hash (60 chars) | Encrypted password (never stored plain) |
| `name` | string | Yes | 1-100 characters | User display name |
| `created_at` | datetime (ISO 8601) | Yes | Auto-generated on creation | Account creation timestamp |
| `updated_at` | datetime (ISO 8601) | Yes | Auto-updated on modification | Last modification timestamp |
| `partition_key` | string | Yes | Always "users" | CosmosDB partition key |

**Validation Rules**:
- Email must match regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Password must be at least 8 characters before hashing
- Name cannot be empty or only whitespace
- Email is case-insensitive (normalized to lowercase before storage)

**Indexes**:
- Primary: `id` (automatic)
- Secondary: `email` (for login lookups)

**Storage Pattern** (CosmosDB):
- Container: `users`
- Partition Key: `/partition_key` (string literal "users")
- Why single partition: Small dataset (~1,000-10,000 users), enables efficient email lookups without cross-partition queries

**Example Document**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.pianist@example.com",
  "password_hash": "$2b$12$KLZh5hG4rF.4YQZg8ygQ5uP9XwV7vB8X3z2kN6MqZrL8tH9jK0yDO",
  "name": "John Pianist",
  "created_at": "2026-02-06T10:00:00Z",
  "updated_at": "2026-02-06T10:00:00Z",
  "partition_key": "users",
  "_etag": "\"00000000-0000-0000-0000-000000000000\"",
  "_ts": 1707219600
}
```

**Business Rules**:
- One user per email address (uniqueness enforced)
- Passwords never exposed in API responses (excluded from serialization)
- User data is private (not shared with other users)
- No soft deletes in MVP (hard delete removes all associated sessions)

---

### Entity 2: Practice Session

**Purpose**: Represents a single practice activity logged by a user on a specific date.

**Attributes**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | string (UUID) | Yes | Unique, immutable | Primary identifier |
| `user_id` | string (UUID) | Yes | Foreign key to User.id | Owner of the session |
| `date` | datetime (ISO 8601) | Yes | Auto-set to current date, not editable | Session date (date only, no backdating) |
| `practice_type` | enum | Yes | One of: "chords", "scales", "course", "songs" | Type of practice activity |
| `tempo` | integer | Conditional | 90-120 (inclusive), required if practice_type is "chords" or "scales" | Practice tempo in beats per minute |
| `notes` | string | No | 0-500 characters | Optional user notes about the session |
| `duration_minutes` | integer | No | 1-600 (10 hours max) | Session duration (future feature, not in MVP) |
| `created_at` | datetime (ISO 8601) | Yes | Auto-generated on creation | Record creation timestamp |
| `updated_at` | datetime (ISO 8601) | Yes | Auto-updated on modification | Last modification timestamp |
| `partition_key` | string (UUID) | Yes | Always equals `user_id` | CosmosDB partition key for query optimization |

**Validation Rules**:
- `practice_type` must be one of the enum values (case-sensitive)
- If `practice_type` is "chords" or "scales", `tempo` must be provided and within 90-120 range
- If `practice_type` is "course" or "songs", `tempo` must be null/undefined
- `tempo` must be an integer (no decimals)
- `notes` is optional but if provided, max 500 characters
- `date` cannot be in the future
- `date` cannot be edited after creation (immutable in MVP)

**Indexes**:
- Primary: `id` (automatic)
- Composite: `(user_id, date DESC)` (for session history queries)
- Composite: `(user_id, practice_type)` (for filtered views)

**Storage Pattern** (CosmosDB):
- Container: `practice_sessions`
- Partition Key: `/partition_key` (equals `user_id`)
- Why partition by user: All queries are user-scoped, prevents cross-partition queries, enables efficient session retrieval per user

**Example Documents**:

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "date": "2026-02-06T00:00:00Z",
  "practice_type": "scales",
  "tempo": 105,
  "notes": "Worked on C major scale, still struggling with left hand coordination",
  "created_at": "2026-02-06T14:30:00Z",
  "updated_at": "2026-02-06T14:30:00Z",
  "partition_key": "550e8400-e29b-41d4-a716-446655440000",
  "_etag": "\"00000000-0000-0000-0000-000000000001\"",
  "_ts": 1707228600
}
```

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440002",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "date": "2026-02-06T00:00:00Z",
  "practice_type": "songs",
  "tempo": null,
  "notes": "Practiced Für Elise, getting better with dynamics",
  "created_at": "2026-02-06T16:00:00Z",
  "updated_at": "2026-02-06T16:00:00Z",
  "partition_key": "550e8400-e29b-41d4-a716-446655440000",
  "_etag": "\"00000000-0000-0000-0000-000000000002\"",
  "_ts": 1707234000
}
```

**Business Rules**:
- Multiple sessions per day are allowed (same user, same date)
- Sessions are ordered by date (most recent first) in history view
- Sessions cannot be backdated in MVP (always current date)
- Deleting a user cascades to delete all their sessions
- Tempo is only meaningful for chords and scales (ignored/null for course and songs)
- Session date uses UTC timezone for consistency

---

## Entity Relationships

```
User (1) ──────< (N) Practice Session
  │                       │
  │                       │
  id ────────────────> user_id
  
- One user can have many practice sessions
- Each practice session belongs to exactly one user
- Relationship is enforced via user_id foreign key
- Cascade delete: deleting user removes all their sessions
```

**Relationship Type**: One-to-Many (User → Practice Sessions)

**Referential Integrity**:
- Enforced at application level (CosmosDB does not support foreign key constraints)
- Before creating session: verify user exists
- Before deleting user: delete all sessions with matching user_id
- No orphaned sessions allowed

---

## Validation Schema (Pydantic Models)

### User Model

```python
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password_strength(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isalpha() for c in v):
            raise ValueError('Password must contain at least one letter')
        return v

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        # Exclude password_hash from all responses
        fields = {'password_hash': {'exclude': True}}

class User(UserBase):
    id: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    partition_key: str = "users"
    
    @validator('email')
    def email_to_lowercase(cls, v):
        return v.lower()
```

### Practice Session Model

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Literal

PracticeType = Literal["chords", "scales", "course", "songs"]

class SessionBase(BaseModel):
    practice_type: PracticeType
    tempo: Optional[int] = Field(None, ge=90, le=120)
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('tempo')
    def validate_tempo_for_practice_type(cls, v, values):
        practice_type = values.get('practice_type')
        if practice_type in ['chords', 'scales']:
            if v is None:
                raise ValueError(f'Tempo is required for {practice_type}')
            if not isinstance(v, int):
                raise ValueError('Tempo must be an integer (no decimals)')
        elif practice_type in ['course', 'songs']:
            if v is not None:
                raise ValueError(f'Tempo should not be provided for {practice_type}')
        return v

class SessionCreate(SessionBase):
    pass  # Date is auto-set to current date, not provided by user

class SessionUpdate(BaseModel):
    notes: Optional[str] = Field(None, max_length=500)
    # Only notes can be updated (date, type, tempo are immutable)

class SessionResponse(SessionBase):
    id: str
    user_id: str
    date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PracticeSession(SessionBase):
    id: str
    user_id: str
    date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    partition_key: str  # Set to user_id
    
    @validator('partition_key', always=True)
    def set_partition_key(cls, v, values):
        return values.get('user_id')
```

---

## Query Patterns & Performance

### Common Queries

#### Q1: Get User by Email (Login)
```sql
SELECT * FROM users u 
WHERE u.email = @email 
  AND u.partition_key = "users"
```
- **Performance**: Single partition query, indexed on email
- **RU Cost**: ~2-3 RU

#### Q2: Get All Sessions for User (History)
```sql
SELECT * FROM practice_sessions s 
WHERE s.user_id = @userId 
  AND s.partition_key = @userId
ORDER BY s.date DESC
OFFSET @offset LIMIT @limit
```
- **Performance**: Single partition query, composite index on (user_id, date)
- **RU Cost**: ~3-5 RU per query (20 items)
- **Pagination**: Default 20 items, max 100

#### Q3: Get Sessions by Type for User
```sql
SELECT * FROM practice_sessions s 
WHERE s.user_id = @userId 
  AND s.partition_key = @userId 
  AND s.practice_type = @type
ORDER BY s.date DESC
```
- **Performance**: Single partition query, composite index on (user_id, practice_type)
- **RU Cost**: ~3-5 RU per query

#### Q4: Count Sessions by Type (Statistics)
```sql
SELECT 
  s.practice_type,
  COUNT(1) as count,
  AVG(s.tempo) as avg_tempo
FROM practice_sessions s
WHERE s.user_id = @userId 
  AND s.partition_key = @userId 
  AND s.date >= @startDate
GROUP BY s.practice_type
```
- **Performance**: Single partition aggregation
- **RU Cost**: ~5-10 RU depending on date range
- **Optimization**: Consider pre-computing for large datasets (future)

### Performance Optimization Strategies

1. **Partition Key Design**: User-scoped partitions ensure all queries are single-partition
2. **Composite Indexes**: 
   - `(user_id, date DESC)` for history queries
   - `(user_id, practice_type)` for filtered views
3. **Pagination**: Always use OFFSET/LIMIT to prevent large result sets
4. **Projection**: Select only needed fields (e.g., `SELECT s.id, s.date, s.practice_type` instead of `SELECT *`)
5. **Caching**: Cache statistics for 5 minutes (future: Redis)

---

## Data Consistency & Integrity

### Consistency Level
- **Selected**: Session-level consistency (CosmosDB default)
- **Rationale**: Balances consistency with performance for single-user workloads

### Data Validation Layers

1. **Client-Side (Zod)**:
   - Validate form inputs before submission
   - Provide immediate feedback to user
   - Prevent unnecessary API calls

2. **Server-Side (Pydantic)**:
   - Validate all request bodies
   - Enforce business rules (tempo required for chords/scales)
   - Return 422 Unprocessable Entity on validation failure

3. **Database**:
   - CosmosDB does not enforce schema
   - Application layer is responsible for consistency
   - Use Pydantic serialization to ensure valid documents

### Concurrency Control
- **Optimistic Locking**: Use `_etag` field for updates
- **Pattern**: 
  1. Read document, get `_etag`
  2. Modify document
  3. Update with `if_match=etag` condition
  4. If `_etag` mismatch (412 Precondition Failed), retry or return error

**Example**:
```python
async def update_session(session_id: str, updates: SessionUpdate, etag: str):
    try:
        container.replace_item(
            item=session_id,
            body=updated_document,
            if_match=etag
        )
    except exceptions.CosmosHttpResponseError as e:
        if e.status_code == 412:
            raise ConcurrencyError("Session was modified by another request")
        raise
```

---

## Data Migration & Evolution

### Schema Evolution Strategy

**Current Version**: 1.0 (MVP)

**Future Changes** (not in MVP, for reference):
- Add `duration_minutes` field to sessions (nullable for backward compatibility)
- Add `user.preferences` field (JSON object for settings)
- Add `session.difficulty_rating` (1-5 scale for perceived difficulty)

**Migration Approach**:
1. Add new fields as optional (nullable) in Pydantic models
2. Update application to handle both old and new documents
3. Background job to backfill defaults for existing documents (if needed)
4. CosmosDB schemaless nature enables gradual migration

**Example Migration**:
```python
# Reading old documents without duration_minutes
class PracticeSession(BaseModel):
    # ... existing fields
    duration_minutes: Optional[int] = None  # None for legacy documents
    
    @validator('duration_minutes', always=True)
    def set_default_duration(cls, v):
        # Backfill default if missing
        return v if v is not None else 30  # Default 30 minutes
```

---

## Data Retention & Deletion

### Retention Policy
- **Users**: Retained indefinitely (no auto-deletion)
- **Sessions**: Retained indefinitely (no TTL)
- **Backup**: CosmosDB automatic daily backups (30-day retention)

### User Deletion Flow
1. User requests account deletion
2. Application deletes all sessions for user (`WHERE user_id = @userId`)
3. Application deletes user document
4. Cascade is manual (CosmosDB does not support automatic cascades)

**Example**:
```python
async def delete_user(user_id: str):
    # Step 1: Delete all sessions
    query = "SELECT c.id FROM c WHERE c.user_id = @userId AND c.partition_key = @userId"
    sessions = sessions_container.query_items(
        query=query,
        parameters=[{"name": "@userId", "value": user_id}],
        partition_key=user_id
    )
    
    for session in sessions:
        await sessions_container.delete_item(
            item=session['id'],
            partition_key=user_id
        )
    
    # Step 2: Delete user
    await users_container.delete_item(
        item=user_id,
        partition_key="users"
    )
```

---

## Security Considerations

### Password Storage
- **Hashing**: bcrypt with cost factor 12 (2^12 = 4096 iterations)
- **Salt**: Unique per password (handled automatically by bcrypt)
- **Never Log**: Password hashes excluded from logs and responses

### Data Access Control
- **Authentication**: JWT tokens required for all session endpoints
- **Authorization**: Users can only access their own sessions
  - Enforced in query: `WHERE user_id = @currentUserId`
- **Admin Access**: Not in MVP (future: admin role for support)

### Data Exposure
- **Public Fields**: id, email, name (in user's own profile only)
- **Private Fields**: password_hash (never exposed in API)
- **Session Data**: Private to owning user (not visible to others)

---

## Summary

### Entity Count
- **2 Entities**: User, Practice Session
- **1 Relationship**: User → Practice Sessions (1:N)

### Storage Requirements (Estimate)
- **Users**: ~1KB per document × 1,000 users = ~1MB
- **Sessions**: ~0.5KB per document × 50 sessions/user × 1,000 users = ~25MB
- **Total Initial**: ~26MB (negligible for CosmosDB)

### Performance Characteristics
- **Read Latency**: < 10ms (single-digit milliseconds, single partition)
- **Write Latency**: < 10ms (document insert/update)
- **Query Throughput**: ~100-200 RU/s for typical workload

### Validation Summary
- **25 Functional Requirements**: All covered by data model
- **Constitutional Compliance**: Data model supports all Constitution requirements (validation, security, performance)

---

**Next Step**: Generate API contracts (OpenAPI specification) in `contracts/` directory
