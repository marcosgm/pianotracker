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
│  │  TypeScript SPA + Vanilla JS        │   │
│  │  (HTML/CSS/TS, no framework)        │   │
│  └─────────────┬───────────────────────┘   │
└────────────────┼───────────────────────────┘
                 │ HTTPS/REST
┌────────────────┼───────────────────────────┐
│                ▼                            │
│  ┌──────────────────────────────────┐      │
│  │  Azure AppService (Python)       │      │
│  │  ┌────────────────────────────┐ │      │
│  │  │      FastAPI               │ │      │
│  │  │  ┌──────────┬────────────┐ │ │      │
│  │  │  │Auth Svc  │Session Svc │ │ │      │
│  │  │  └──────────┴────────────┘ │ │      │
│  │  └────────────┬───────────────┘ │      │
│  │               ▼                  │      │
│  │    ┌──────────────────────┐     │      │
│  │    │  Azure CosmosDB      │     │      │
│  │    │  (NoSQL Document DB) │     │      │
│  │    └──────────────────────┘     │      │
│  └────────────────────────────────┘       │
└─────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **Language**: TypeScript
- **Architecture**: Vanilla TypeScript SPA (no framework)
- **Build Tool**: Webpack or Parcel (minify, bundle)
- **HTTP Client**: Fetch API (with types)
- **Validation**: Zod (client-side)
- **Charts**: Chart.js (lightweight, no React needed)
- **Styling**: Plain CSS (mobile-first responsive design)
- **Testing**: Jest + Playwright (E2E)
- **Package Manager**: npm/pnpm

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI (async, modern, fast)
- **Authentication**: JWT (access + refresh tokens)
- **Password Hashing**: bcrypt
- **Validation**: Pydantic (schemas)
- **Database Client**: azure-cosmos-python (CosmosDB SDK)
- **Testing**: pytest + pytest-asyncio
- **ASGI Server**: Uvicorn
- **Dependencies**: APScheduler (background jobs), python-jose (JWT)

### Database
- **Primary**: Azure CosmosDB (NoSQL, document-based)
- **API**: SQL API (SQL queries on JSON documents)
- **Consistency**: Session-level (default)
- **Throughput**: RU-based billing, auto-scale capable
- **Backup**: Automatic daily backups by Azure

### Infrastructure
- **Hosting**: Azure AppService (Linux, Docker container)
- **Database**: Azure CosmosDB
- **Infrastructure as Code**: Bicep (Azure Resource Manager templates)
- **CI/CD**: GitHub Actions
- **Monitoring**: Azure Monitor + Application Insights
- **Container Registry**: Azure Container Registry (ACR)

---

## Data Model

### Core Entities (Pydantic Models)

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime

class User(BaseModel):
    id: str = Field(..., alias="_id")
    email: EmailStr
    password_hash: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    partition_key: str = "users"  # CosmosDB partition key

class PracticeSession(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    date: datetime
    duration_minutes: int  # min: 1
    practice_type: Literal["chords", "scales", "course", "songs"]
    tempo: Optional[int] = None  # 90-120, required for chords/scales
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    partition_key: str = None  # Will be set to user_id
```

### CosmosDB Document Schema

CosmosDB uses JSON documents. Two containers required:

**Container 1: users**
- Partition key: `/partition_key` (string "users")
- TTL: None (permanent)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "password_hash": "$2b$12$...",
  "name": "John Pianist",
  "created_at": "2026-02-06T12:00:00",
  "updated_at": "2026-02-06T12:00:00",
  "partition_key": "users",
  "_etag": "\"00000000-0000-0000-0000-000000000000\"",
  "_ts": 1707219600
}
```

**Container 2: practice_sessions**
- Partition key: `/partition_key` (user_id for query efficiency)
- TTL: None

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "_id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "date": "2026-02-06T14:30:00",
  "duration_minutes": 45,
  "practice_type": "scales",
  "tempo": 108,
  "notes": "Worked on C major, struggling with left hand",
  "created_at": "2026-02-06T14:31:00",
  "updated_at": "2026-02-06T14:31:00",
  "partition_key": "550e8400-e29b-41d4-a716-446655440000",
  "_etag": "\"00000000-0000-0000-0000-000000000001\"",
  "_ts": 1707220260
}
```

### CosmosDB Queries

```sql
-- Get user by email
SELECT * FROM users u WHERE u.email = @email AND u.partition_key = "users"

-- Get sessions for user (paginated)
SELECT * FROM practice_sessions s 
WHERE s.user_id = @userId AND s.partition_key = @userId
ORDER BY s.date DESC
OFFSET @offset LIMIT @limit

-- Get sessions by type (user filtered)
SELECT * FROM practice_sessions s 
WHERE s.user_id = @userId 
  AND s.partition_key = @userId 
  AND s.practice_type = @type
ORDER BY s.date DESC

-- Aggregate stats (group by type)
SELECT 
  s.practice_type,
  COUNT(1) as count,
  SUM(s.duration_minutes) as total_minutes
FROM practice_sessions s
WHERE s.user_id = @userId 
  AND s.partition_key = @userId 
  AND s.date >= @startDate
GROUP BY s.practice_type
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
- CosmosDB partition key optimization (partition by user_id)
- Composite indexes for common query patterns
- Pagination (limit/offset)
- Gzip compression on responses
- Connection pooling via CosmosDB SDK

### Monitoring
- Core Web Vitals tracking (RUM)
- API response time monitoring via Azure Application Insights
- CosmosDB request metrics and RU consumption
- Error tracking with stack traces (Application Insights)

---

## Testing Strategy

### Unit Tests (70%)
- Pydantic validation schemas
- Utility functions (date formatting, tempo calculations, stats)
- API route handlers (business logic)
- CosmosDB query builders

### Integration Tests (20%)
- API endpoint flows (auth → create session → fetch sessions)
- CosmosDB CRUD operations
- Frontend-backend integration (API calls)

### E2E Tests (10%)
- Complete user journey: register → login → create session → view history → logout
- Session filtering and statistics viewing
- Error states (invalid inputs, network failures)
- Performance benchmarks

### Target Coverage
- Overall: 80%+
- Critical paths: 100% (auth, session CRUD)
- Backend (pytest): All endpoints with fixture-based CosmosDB testing

---

## Deployment

### Environments
- **Development**: Local (Docker with CosmosDB emulator)
- **Staging**: Azure AppService slot (pre-production)
- **Production**: Azure AppService main slot

### Infrastructure as Code (Bicep)

Deploy via GitHub Actions:
```bicep
// main.bicep
param location string = 'eastus'
param environment string = 'prod'

resource appService 'Microsoft.Web/sites@2021-02-01' = {
  name: 'pianotracker-${environment}'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      alwaysOn: true
      linuxFxVersion: 'PYTHON|3.11'
      appSettings: [
        { name: 'COSMOSDB_ENDPOINT', value: cosmosAccount.properties.documentEndpoint }
        { name: 'COSMOSDB_KEY', value: cosmosAccount.listKeys().primaryMasterKey }
      ]
    }
  }
}

resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2021-04-15' = {
  name: 'pianotracker-cosmos-${environment}'
  location: location
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [{ locationName: location, failoverPriority: 0 }]
  }
}
```

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Deploy
on:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Frontend Tests
        run: npm test --prefix frontend
      - name: Backend Tests
        run: pytest backend/
      - name: Frontend Build
        run: npm run build --prefix frontend
      - name: Backend Build
        run: pip install -r backend/requirements.txt

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy Bicep
        run: |
          az deployment group create \
            --resource-group pianotracker \
            --template-file main.bicep \
            --parameters environment=prod
      - name: Deploy Frontend
        run: az webapp deployment source config-zip --resource-group pianotracker --name pianotracker-prod --src-path frontend.zip
      - name: Deploy Backend
        run: |
          az appservice plan create --resource-group pianotracker --name pianotracker-plan --sku B2 --is-linux
          az webapp deployment source config-zip --resource-group pianotracker --name pianotracker-api-prod --src-path backend.zip
      - name: Smoke Tests
        run: pytest tests/e2e/smoke_tests.py
```

### Rollback Strategy
- Azure AppService slot swaps (instant rollback)
- Keep previous deployment in staging slot
- CosmosDB has automatic daily backups (point-in-time restore available)

---

## Future Technical Enhancements

### Phase 2: Analytics
- CosmosDB analytical queries with dedicated analytical store
- Background jobs for stat pre-aggregation (APScheduler)
- Time-windowed statistics materialized views

### Phase 3: Intelligence
- ML model for recommendations (Python service within backend)
- Feature flags (Feature Management via Azure)
- User segment analysis

### Phase 4: Visual Learning
- SVG-based piano keyboard component (frontend TypeScript)
- Chord data library (CosmosDB collection)
- Advanced visualizations (Canvas/SVG)

---

## Configuration & Secrets

### Environment Variables

```bash
# Backend (.env)
FASTAPI_ENV=production
DEBUG=false
SECRET_KEY=<random-256-bit-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
JWT_REFRESH_EXPIRATION_DAYS=7

COSMOSDB_ENDPOINT=https://pianotracker-cosmos.documents.azure.com:443/
COSMOSDB_KEY=<primary-key>
COSMOSDB_DATABASE=pianotracker

CORS_ORIGINS=https://pianotracker.azurewebsites.net
LOG_LEVEL=INFO
```

### Frontend Configuration
```typescript
// config.ts
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://api.pianotracker.azurewebsites.net';
export const JWT_STORAGE_KEY = 'pianotracker_token';
export const JWT_REFRESH_KEY = 'pianotracker_refresh';
```

---

## Open Questions

- [ ] CosmosDB throughput: Fixed RU/s or autoscale?
- [ ] Email service for password reset (SendGrid, Azure Communication Services)?
- [ ] Internationalization needed (i18n)?
- [ ] Dark mode support?
- [ ] Custom domain (e.g., pianotracker.com) or Azure subdomain?

---

## Dependencies & Risks

### Critical Dependencies
- Azure AppService availability (99.95% SLA)
- Azure CosmosDB availability (99.99% SLA)
- Third-party libraries (FastAPI, Pydantic, Chart.js)

### Risks & Mitigation

- **Risk**: CosmosDB RU costs exceed budget  
  **Mitigation**: Autoscale with max RU caps, query optimization, dedicated analytical store
  
- **Risk**: Frontend TypeScript type errors in production  
  **Mitigation**: Strict TypeScript config, ESLint, pre-deployment build checks
  
- **Risk**: Python backend cold starts on AppService  
  **Mitigation**: Always-On setting, keep-alive pings, Premium tier if needed
  
- **Risk**: CosmosDB partition hotspots (user-based queries)  
  **Mitigation**: Distribute queries, consider synthetic partition key if needed
  
- **Risk**: User data loss  
  **Mitigation**: CosmosDB automatic daily backups + point-in-time restore (30 days)

---

**Next Steps:**
1. Create Bicep infrastructure templates
2. Set up local CosmosDB emulator for development
3. Scaffold FastAPI backend with Pydantic models
4. Create TypeScript frontend build pipeline
5. Configure GitHub Actions CI/CD
6. Deploy to Azure staging environment