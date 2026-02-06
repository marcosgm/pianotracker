# Piano Tracker - Technical Specification

**Version:** 1.0  
**Last Updated:** February 6, 2026  
**Status:** In Development

---

## System Architecture

### Architecture Pattern
**Monolithic web application** with client-side rendering and RESTful API

```
┌─────────────────────────────────────────────┐
│            Client (Browser)                 │
│  ┌─────────────────────────────────────┐   │
│  │   React SPA + State Management      │   │
│  └─────────────┬───────────────────────┘   │
└────────────────┼───────────────────────────┘
                 │ HTTPS/REST
┌────────────────┼───────────────────────────┐
│                ▼                            │
│  ┌──────────────────────────────────┐      │
│  │      API Gateway/Router          │      │
│  └──────────┬───────────────────────┘      │
│             │                               │
│  ┌──────────┼───────────────────────┐      │
│  │  ┌───────▼────────┐  ┌─────────┐ │      │
│  │  │ Auth Service   │  │ Session │ │      │
│  │  │                │  │ Service │ │      │
│  │  └───────┬────────┘  └────┬────┘ │      │
│  │          │                 │      │      │
│  │          └────────┬────────┘      │      │
│  │                   ▼               │      │
│  │          ┌─────────────────┐      │      │
│  │          │   Database      │      │      │
│  │          │  (PostgreSQL)   │      │      │
│  │          └─────────────────┘      │      │
│  └────────────────────────────────────┘     │
│              Backend Server                 │
└─────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **State Management**: React Context API + React Query (server state)
- **Routing**: React Router v6
- **Forms**: React Hook Form + Zod validation
- **UI Components**: Custom components with design system
- **Charts**: Chart.js or Recharts (lightweight)
- **Styling**: CSS Modules or Styled Components
- **Build Tool**: Vite
- **Testing**: Vitest + React Testing Library + Playwright (E2E)

### Backend
- **Runtime**: Node.js 18+ LTS
- **Framework**: Express.js or Fastify
- **Language**: TypeScript
- **Authentication**: JWT (access + refresh tokens)
- **Password Hashing**: bcrypt
- **Validation**: Zod (shared schemas with frontend)
- **ORM**: Prisma or Drizzle
- **Testing**: Vitest + Supertest

### Database
- **Primary**: PostgreSQL 15+
- **Caching** (future): Redis for session storage
- **Migrations**: Prisma Migrate or custom SQL migrations

### Infrastructure
- **Hosting**: TBD (Vercel, Netlify, Railway, or similar)
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry (errors) + Analytics tool (TBD)

---

## Data Model

### Core Entities

```typescript
// User
interface User {
  id: string;              // UUID
  email: string;           // Unique
  passwordHash: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

// Practice Session
interface PracticeSession {
  id: string;              // UUID
  userId: string;          // FK to User
  date: Date;              // Practice date/time
  durationMinutes: number; // Required
  practiceType: PracticeType; // Enum
  tempo?: number;          // Required if type is CHORDS or SCALES
  notes?: string;          // Optional
  createdAt: Date;
  updatedAt: Date;
}

// Practice Type Enum
enum PracticeType {
  CHORDS = 'chords',
  SCALES = 'scales',
  COURSE = 'course',
  SONGS = 'songs'
}
```

### Database Schema (PostgreSQL)

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

CREATE TYPE practice_type AS ENUM ('chords', 'scales', 'course', 'songs');

CREATE TABLE practice_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date TIMESTAMP NOT NULL DEFAULT NOW(),
  duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
  practice_type practice_type NOT NULL,
  tempo INTEGER CHECK (tempo IS NULL OR (tempo >= 90 AND tempo <= 120)),
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- Constraint: tempo required for chords/scales
  CONSTRAINT tempo_required_for_tempo_types 
    CHECK (
      (practice_type IN ('chords', 'scales') AND tempo IS NOT NULL) OR
      (practice_type NOT IN ('chords', 'scales'))
    )
);

CREATE INDEX idx_sessions_user_date ON practice_sessions(user_id, date DESC);
CREATE INDEX idx_sessions_user_type ON practice_sessions(user_id, practice_type);
```

---

## API Specification

### Authentication Endpoints

```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh
POST   /api/auth/forgot-password
POST   /api/auth/reset-password
GET    /api/auth/me
```

### Practice Session Endpoints

```
POST   /api/sessions          - Create session
GET    /api/sessions          - List sessions (paginated, filtered)
GET    /api/sessions/:id      - Get single session
PUT    /api/sessions/:id      - Update session
DELETE /api/sessions/:id      - Delete session
GET    /api/sessions/stats    - Get statistics
```

### Example: Create Session

**Request:**
```http
POST /api/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "2026-02-06T14:30:00Z",
  "durationMinutes": 45,
  "practiceType": "scales",
  "tempo": 108,
  "notes": "Worked on C major, struggling with left hand"
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "date": "2026-02-06T14:30:00Z",
  "durationMinutes": 45,
  "practiceType": "scales",
  "tempo": 108,
  "notes": "Worked on C major, struggling with left hand",
  "createdAt": "2026-02-06T14:31:00Z",
  "updatedAt": "2026-02-06T14:31:00Z"
}
```

### Example: Get Statistics

**Request:**
```http
GET /api/sessions/stats?period=month
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "totalMinutes": 1350,
  "totalSessions": 28,
  "byType": {
    "scales": { "count": 10, "minutes": 450 },
    "chords": { "count": 8, "minutes": 360 },
    "songs": { "count": 7, "minutes": 420 },
    "course": { "count": 3, "minutes": 120 }
  },
  "averageTempo": {
    "scales": 105,
    "chords": 98
  },
  "streak": 7,
  "period": "month"
}
```

---

## Security

### Authentication Flow
1. User registers → password hashed with bcrypt (cost: 12)
2. User logs in → JWT access token (15min) + refresh token (7d)
3. Access token in Authorization header for protected routes
4. Refresh token in httpOnly cookie, rotated on use
5. Logout invalidates refresh token (blacklist or version check)

### Security Measures
- HTTPS only (enforced)
- CORS with allowed origins whitelist
- Rate limiting on auth endpoints (5 req/min)
- Input validation on all endpoints (Zod schemas)
- SQL injection prevention (parameterized queries via ORM)
- XSS prevention (React auto-escaping + CSP headers)
- CSRF protection for cookie-based requests

---

## Performance Optimization

### Frontend
- Code splitting by route
- Lazy load chart libraries
- React.memo for session list items
- Debounced search/filter inputs
- Optimistic updates for session creation
- Service Worker for offline history viewing

### Backend
- Database connection pooling
- Index on user_id + date for fast queries
- Pagination (limit/offset or cursor-based)
- Response caching for statistics (5min TTL)
- Gzip compression on responses

### Monitoring
- Core Web Vitals tracking (RUM)
- API response time monitoring
- Database query performance logging (slow query log)
- Error tracking with stack traces (Sentry)

---

## Testing Strategy

### Unit Tests (70%)
- Validation schemas
- Utility functions (date formatting, tempo calculations)
- React hooks (custom hooks)
- API route handlers (business logic)

### Integration Tests (20%)
- API endpoint flows (auth → create session → fetch sessions)
- Database interactions (CRUD operations)
- Form submission flows

### E2E Tests (10%)
- User registration → login → create session → view history → logout
- Session filtering and statistics viewing
- Error states (invalid inputs, network failures)

### Target Coverage
- Overall: 80%+
- Critical paths: 100% (auth, session CRUD)

---

## Deployment

### Environments
- **Development**: Local (Docker Compose for DB)
- **Staging**: Preview deployments (per PR)
- **Production**: Main branch auto-deploy

### CI/CD Pipeline
```yaml
1. Trigger: Push to branch
2. Lint & Type Check (TypeScript)
3. Run Unit Tests
4. Run Integration Tests
5. Build Frontend (Vite)
6. Build Backend (tsc)
7. Run E2E Tests (Playwright)
8. Deploy to Staging (if PR)
9. Deploy to Production (if main branch)
10. Smoke Tests on Production
```

### Rollback Strategy
- Keep last 3 deployments ready
- Instant rollback via hosting provider
- Database migrations backward-compatible

---

## Future Technical Enhancements

### Phase 2: Analytics
- Time-series database for efficient stat queries (TimescaleDB)
- Background jobs for stat aggregation (BullMQ)

### Phase 3: Intelligence
- ML model for recommendations (Python microservice or Edge Function)
- Feature flags for gradual rollout (LaunchDarkly or custom)

### Phase 4: Visual Learning
- SVG-based piano keyboard component
- Chord data library (JSON or DB table)
- WebGL for advanced visualizations (optional)

---

## Open Questions

- [ ] Preferred hosting provider (cost vs. features)?
- [ ] Analytics tool (privacy-focused: Plausible, Fathom)?
- [ ] Email service for password reset (SendGrid, AWS SES)?
- [ ] Internationalization needed (i18n)?
- [ ] Dark mode support?

---

## Dependencies & Risks

### Dependencies
- PostgreSQL database availability
- Hosting provider uptime SLA
- Third-party libraries (React, Express)

### Risks & Mitigation
- **Risk**: Database schema changes break existing data  
  **Mitigation**: Comprehensive migration tests, staging validation
  
- **Risk**: Frontend bundle size exceeds targets  
  **Mitigation**: Bundle analysis in CI, lazy loading, tree-shaking
  
- **Risk**: User data loss  
  **Mitigation**: Automated daily backups, point-in-time recovery

---

**Next Steps:**
1. Set up project scaffolding (Vite + Express)
2. Database schema creation and seed data
3. Auth endpoints implementation
4. Session CRUD implementation
5. Frontend session logging UI