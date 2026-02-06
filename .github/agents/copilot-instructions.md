# GitHub Copilot Context for Piano Practice Session Tracker

Auto-generated from feature plan `001-practice-tracker`. Last updated: 2026-02-06

## Project Overview

This repository contains the **Piano Practice Session Tracker**, a full-stack web application for tracking piano practice sessions.

- **Feature Branch**: `001-practice-tracker`
- **Tech Stack**: Python/FastAPI (backend), TypeScript/Vanilla JS (frontend), Azure CosmosDB
- **Status**: Phase 1 (Setup) complete, Phase 2+ in progress

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI (async, modern, fast)
- **Database**: Azure CosmosDB (NoSQL, SQL API)
- **Auth**: JWT (python-jose, bcrypt)
- **Testing**: pytest + pytest-asyncio
- **Key Dependencies**: Pydantic, Azure Cosmos SDK

### Frontend
- **Language**: TypeScript (strict mode, no `any`)
- **Architecture**: Vanilla TypeScript SPA (no framework)
- **Bundler**: Webpack 5
- **Validation**: Zod (schema-based, type-safe)
- **Visualization**: Chart.js (lightweight)
- **Testing**: Jest + Playwright (E2E)
- **Build Constraints**: Bundle < 200KB gzipped, Core Web Vitals targets

### Infrastructure
- **Containerization**: Docker (multi-stage builds)
- **Orchestration**: Docker Compose (local dev)
- **CI/CD**: GitHub Actions
- **Cloud**: Microsoft Azure (AppService, CosmosDB, ACR)
- **IaC**: Bicep (Azure Resource Manager)

## Project Structure

```text
backend/
├── src/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py           # Configuration (Pydantic BaseSettings)
│   ├── models/             # Pydantic models (User, PracticeSession)
│   ├── services/           # Business logic layer
│   ├── api/               # API endpoints (routers)
│   ├── db/                # Database client (CosmosDB)
│   └── security/          # JWT, crypto utilities
├── tests/
│   ├── unit/             # Unit tests (models, services)
│   └── integration/      # Integration tests (endpoints, DB)
├── requirements.txt
├── pytest.ini
├── Dockerfile
└── .env.example

frontend/
├── src/
│   ├── main.ts           # App entry point
│   ├── types/           # TypeScript interfaces
│   ├── services/        # API client, auth, state store
│   ├── pages/          # Page components (Login, Dashboard, History, etc.)
│   ├── components/     # Reusable components (forms, cards, charts)
│   └── utils/          # Validation (Zod), constants
├── public/
│   ├── index.html
│   └── styles.css
├── tests/
│   ├── unit/          # Jest unit tests
│   └── e2e/          # Playwright E2E tests
├── package.json
├── tsconfig.json
├── webpack.config.js
├── jest.config.js
└── .env.example

infrastructure/
├── bicep/
│   ├── main.bicep          # Azure resources (AppService, CosmosDB)
│   └── parameters.json     # Dev/staging/prod parameters
└── scripts/
    └── deploy.sh          # Deployment script
```

## Data Model

### User Entity
- `id` (UUID): Unique identifier
- `email` (string): Unique, lowercase, email format
- `password_hash` (string): bcrypt hash (cost 12)
- `name` (string): 1-100 characters
- `created_at`, `updated_at`: Timestamps (UTC)
- **Storage**: CosmosDB `users` container, partition key: "users"

### PracticeSession Entity
- `id` (UUID): Unique identifier
- `user_id` (UUID): Foreign key to User
- `date` (ISO 8601): Session date (current date only, not editable)
- `practice_type` (enum): "chords" | "scales" | "course" | "songs"
- `tempo` (integer): 90-120 BPM (required for chords/scales, null for course/songs)
- `notes` (string): Optional, max 500 characters
- `created_at`, `updated_at`: Timestamps
- **Storage**: CosmosDB `practice_sessions` container, partition key: user_id

### Relationships
- One User → Many PracticeSessions (1:N)
- Cascade delete: Deleting user removes all their sessions

## API Architecture

### Authentication Flow
1. `POST /api/auth/register` - Create account, get JWT access token
2. `POST /api/auth/login` - Authenticate, get access + refresh tokens
3. `POST /api/auth/refresh` - Refresh access token (return new refresh token)
4. `GET /api/auth/me` - Get current user (protected)
5. `POST /api/auth/logout` - Invalidate session (clear refresh cookie)

### Session Endpoints
- `POST /api/sessions` - Create session (protected, date auto-set, validate tempo)
- `GET /api/sessions` - List sessions paginated (protected, sortable, filterable)
- `GET /api/sessions/{id}` - Get single session (protected, verify ownership)
- `PUT /api/sessions/{id}` - Update notes only (protected)
- `DELETE /api/sessions/{id}` - Delete session (protected)
- `GET /api/sessions/stats` - Get statistics (protected, by period)

### Error Handling
- All errors return RFC 7807 format with `detail` field
- Status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 429 Too Many Requests

### Rate Limiting & Security
- Auth endpoints: 5 requests/minute per IP
- CORS: Whitelist origins (no wildcard in production)
- JWT: HS256, 15min access token, 7d refresh token
- HTTPS: Enforced in production

## Frontend State Management

### Store Pattern (Pub/Sub)
- `appStore.getState()`: Get current state
- `appStore.setState(partial)`: Set partial state
- `appStore.dispatch(action)`: Dispatch action
- `appStore.subscribe(listener)`: Subscribe to updates

### State Shape
```typescript
{
  currentUser: User | null,
  sessions: PracticeSession[],
  statistics: Statistics | null,
  isLoading: boolean,
  error: string | null,
  isAuthenticated: boolean
}
```

### Actions
- `SET_USER`, `CLEAR_USER`
- `SET_SESSIONS`, `ADD_SESSION`, `UPDATE_SESSION`, `DELETE_SESSION`
- `SET_STATISTICS`
- `SET_LOADING`, `SET_ERROR`
- `SET_AUTHENTICATED`

## Development Commands

### Backend
```bash
# Setup
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && cp .env.example .env

# Run
uvicorn src.main:app --reload

# Test
pytest --cov=src --cov-report=html

# Lint
ruff check src
```

### Frontend
```bash
# Setup
cd frontend && npm install && cp .env.example .env

# Run
npm run dev  # Starts http://localhost:3000

# Test
npm test                    # Unit tests
npm run test:e2e           # Playwright E2E
npm run build              # Production build

# Quality
npm run lint               # ESLint
npm run test:coverage      # Coverage report
npx webpack-bundle-analyzer dist/stats.json
```

### Docker
```bash
# Run locally with CosmosDB emulator
docker-compose up -d

# Backend: http://localhost:8000
# CosmosDB Emulator: https://localhost:8081/_explorer/index.html
# Frontend: http://localhost:3000
```

## Testing Strategy

### Test Pyramid
- **Unit Tests** (70%): Models, services, utilities
- **Integration Tests** (20%): API endpoints, database operations
- **E2E Tests** (10%): Complete user journeys

### Coverage Targets
- **Overall**: 80%+
- **Critical Paths**: 100% (auth, session CRUD, validation)

### Test Files
- Backend: `tests/unit/*.py`, `tests/integration/*.py`
- Frontend: `tests/**/*.test.ts`, `tests/e2e/*.spec.ts`

## Code Style & Quality

### TypeScript Standards
- ✅ `strict: true` in tsconfig.json
- ✅ No `any` types (use generics)
- ✅ Explicit return types on functions
- ✅ Components < 200 lines
- ✅ Services < 50 lines (break into smaller functions)

### Python Standards
- ✅ Type hints on all functions
- ✅ Docstrings on public APIs
- ✅ Functions < 50 lines (FastAPI handlers may be ~30 lines)
- ✅ Use Pydantic for validation
- ✅ Error handling with custom exceptions

### Design Principles
- ✅ Single Responsibility: Each function/class does one thing
- ✅ Composition over inheritance
- ✅ DRY (Don't Repeat Yourself): Extract 3+ repetitions
- ✅ KISS (Keep It Simple, Stupid): No premature optimization

## Key Constraints

### Performance
- Bundle size: < 200KB gzipped
- Core Web Vitals: LCP < 2.5s, FCP < 1.5s, TTI < 3.5s, CLS < 0.1
- API response: < 200ms reads, < 500ms writes
- UI: 60fps (16ms frame budget)

### Accessibility
- WCAG 2.1 AA compliance (required)
- Keyboard navigation for all forms
- Color contrast: 4.5:1 text, 3:1 UI
- Mobile: min viewport 320px, touch targets 44x44px

### Security
- JWT + bcrypt authentication
- HTTPS only (enforced)
- Input validation (client + server, dual)
- CORS whitelist (no wildcard)
- Rate limiting on auth endpoints

## User Stories

### P1 - Authentication (Highest Priority)
Users can register, log in, and access personalized sessions.
- Register with email+password (validate length, format)
- Login returns JWT (15min access, 7d refresh)
- Protected endpoints check Bearer token
- Logout invalidates session

### P2 - Session Logging (Core Feature)
Users can log piano practice sessions with type and optional tempo.
- Session types: chords, scales, course, songs
- Tempo required and validated (90-120 BPM, integer only) for chords/scales
- Tempo must be null for course/songs
- Date auto-set to current (no backdating in MVP)
- Users can log multiple sessions per day

### P3 - History & Statistics (Value Proposition)
Users can view past sessions and statistics showing practice patterns.
- View session list (date, type, tempo, notes)
- Filter by practice type
- Statistics: total count, breakdown by type, average tempo
- Charts: bar (by type), line (over time), doughnut (distribution)

## Important Decisions

### Why Vanilla TypeScript?
- Zero framework overhead
- Smaller bundle (< 200KB target)
- Demonstrates platform APIs
- Full control over rendering

### Why FastAPI?
- Native async/await support
- Automatic OpenAPI docs
- Pydantic integration for validation
- High performance (uvicorn + async)

### Why CosmosDB?
- Azure-native (AppService integration)
- Document model (schema flexibility)
- Partition key optimization
- Global scalability (future-proofing)

### Why Zod + Pydantic?
- End-to-end type safety
- Runtime validation (not just compile-time)
- Mirrors schema definitions (DRY)

## Monitoring & Observability

### Backend (Application Insights)
- Log all API requests (method, path, status, response time)
- Log all errors with stack traces
- Custom metrics: session creation rate, auth success rate
- Alerts: error rate > 5%, response time > 500ms

### Frontend (Application Insights JS SDK)
- Track page views and routes
- Log JavaScript errors
- Core Web Vitals (LCP, FCP, TTI, CLS)

## Deployment

### Local Development
```bash
docker-compose up -d
```

### Staging/Production
```bash
# Deploy infrastructure
az deployment group create --template-file infrastructure/bicep/main.bicep

# Deploy application (GitHub Actions handles this)
```

## Common Patterns

### API Error Handling
```python
# Backend
try:
    result = await service.do_something()
except ValidationError as e:
    raise HTTPException(status_code=422, detail=str(e))
except NotFoundException as e:
    raise HTTPException(status_code=404, detail=str(e))
```

### Form Validation
```typescript
// Frontend
const result = validateForm(SessionCreateSchema, formData);
if (result.success) {
    await createSession(result.data);
} else {
    setErrors(result.errors);
}
```

### Protected Routes
```python
# Backend
@router.get("/sessions")
async def list_sessions(current_user: User = Depends(get_current_user)):
    return await session_service.get_user_sessions(current_user.id)
```

## Documentation References

- **Specification**: `specs/001-practice-tracker/spec.md` (requirements, user stories)
- **Implementation Plan**: `specs/001-practice-tracker/plan.md` (architecture, tech stack)
- **Data Model**: `specs/001-practice-tracker/data-model.md` (entities, validation)
- **API Contract**: `specs/001-practice-tracker/contracts/openapi.yaml` (endpoints, schemas)
- **Quickstart**: `specs/001-practice-tracker/quickstart.md` (setup, local development)
- **Tasks**: `specs/001-practice-tracker/tasks.md` (breakdown, execution plan)

## Contact & Support

For questions about the feature:
- Check the documentation above
- Review issues in GitHub
- Reference the Spec Kit planning documents in `specs/`
