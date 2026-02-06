# Phase 0: Technical Research & Decisions

**Feature**: Piano Practice Session Tracker  
**Date**: 2026-02-06  
**Phase**: Research & Technology Validation

---

## Research Summary

This document consolidates technical decisions, best practices, and patterns for implementing the Piano Practice Session Tracker. All technology choices are based on existing project standards documented in [TECHNICAL_SPEC.md](../../specs/TECHNICAL_SPEC.md).

---

## Core Technology Decisions

### Decision 1: Vanilla TypeScript SPA (No Framework)

**Decision**: Use vanilla TypeScript with Web Components pattern instead of React/Vue/Angular

**Rationale**:
- **Simplicity**: Small application scope (4 main pages, ~10 components) doesn't justify framework overhead
- **Performance**: Zero framework runtime cost, faster initial load (target < 200KB bundle)
- **Learning**: Demonstrates core web platform APIs without abstraction layers
- **Constitution alignment**: Meets bundle size requirement (< 200KB gzipped)
- **Existing standard**: Project TECHNICAL_SPEC already specifies "Vanilla JS/TS, no framework"

**Best Practices**:
- Use TypeScript classes for components with lifecycle methods (mount, unmount, render)
- Implement custom element pattern for reusability: `class SessionForm extends HTMLElement`
- Use Shadow DOM for style encapsulation where appropriate
- Centralize state management in a simple Store pattern (pub/sub)
- Use template literals for HTML generation with proper escaping

**Alternatives Considered**:
- React: Rejected due to bundle size (~40KB minified) and project standard preference
- Lit: Rejected to avoid additional dependencies (already have vanilla TS requirement)
- Svelte: Rejected due to compilation step complexity vs. direct TypeScript

**References**:
- MDN Web Components Guide: https://developer.mozilla.org/en-US/docs/Web/API/Web_components
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/

---

### Decision 2: FastAPI for Backend API

**Decision**: Use FastAPI (Python async framework) for REST API implementation

**Rationale**:
- **Performance**: Async/await support enables high concurrency with low resource usage
- **Type Safety**: Pydantic models provide runtime validation + automatic OpenAPI docs
- **Developer Experience**: Auto-generated API docs (/docs), clear error messages
- **CosmosDB Integration**: Async SDK (azure-cosmos) works seamlessly with FastAPI async
- **Existing standard**: Specified in TECHNICAL_SPEC.md

**Best Practices**:
- Use dependency injection for database client (FastAPI Depends)
- Implement middleware for JWT validation, CORS, request logging
- Use Pydantic BaseSettings for configuration management (environment variables)
- Separate business logic into service layer (not in route handlers)
- Use APIRouter for modular endpoint organization
- Enable CORS with specific origin whitelist (not wildcard)

**API Structure Pattern**:
```python
# api/sessions.py (route handlers)
@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    session: SessionCreate,
    current_user: User = Depends(get_current_user),
    service: SessionService = Depends(get_session_service)
):
    return await service.create_session(user_id=current_user.id, data=session)
```

**Alternatives Considered**:
- Flask: Rejected due to lack of native async support (requires extensions)
- Django: Rejected due to ORM overhead (not needed with CosmosDB NoSQL)

**References**:
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pydantic Validation: https://docs.pydantic.dev/

---

### Decision 3: Azure CosmosDB with SQL API

**Decision**: Use CosmosDB NoSQL (SQL API) for data persistence

**Rationale**:
- **Scalability**: Built-in horizontal scaling with partition keys
- **Performance**: Single-digit millisecond read/write latency
- **Schema Flexibility**: NoSQL allows easy schema evolution (future features)
- **Azure Integration**: Native integration with Azure AppService, Application Insights
- **Existing standard**: Specified in TECHNICAL_SPEC.md

**Partition Key Strategy**:
- **users container**: Partition key = `"users"` (string literal)
  - All users in same partition (small dataset, <10k users expected)
  - Enables efficient user email lookups
- **practice_sessions container**: Partition key = `user_id`
  - Each user's sessions in separate partition
  - Optimal for queries: "get all sessions for user X"
  - Prevents cross-partition queries for session history

**Best Practices**:
- Use composite indexes for common query patterns:
  - `(user_id, date DESC)` for session history
  - `(user_id, practice_type)` for filtered views
- Set TTL (Time-To-Live) = None (don't auto-delete sessions)
- Use parameterized queries to prevent injection: `WHERE c.user_id = @userId`
- Implement optimistic concurrency with `_etag` for updates
- Use bulk operations for batch inserts if needed (future import feature)

**Query Optimization**:
```sql
-- Efficient: Single partition query
SELECT * FROM c 
WHERE c.user_id = @userId 
  AND c.partition_key = @userId
ORDER BY c.date DESC

-- Avoid: Cross-partition aggregation (use pre-computed stats instead)
SELECT COUNT(1) FROM c WHERE c.practice_type = 'scales'
```

**Alternatives Considered**:
- PostgreSQL: Rejected due to relational overhead for simple document model
- MongoDB: Rejected in favor of Azure-native solution for better integration

**References**:
- CosmosDB Best Practices: https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet
- Partition Key Design: https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning-overview

---

### Decision 4: JWT Authentication Strategy

**Decision**: Use JWT access tokens (15min) + refresh tokens (7d) stored in httpOnly cookies

**Rationale**:
- **Security**: httpOnly cookies prevent XSS token theft
- **Stateless**: JWT enables horizontal scaling without session storage
- **Standard**: Industry best practice for SPA authentication
- **Refresh Flow**: Short-lived access tokens limit damage if compromised

**Token Structure**:
```python
# Access Token Payload
{
  "sub": "user_id",       # Subject (user identifier)
  "email": "user@example.com",
  "exp": 1707220800,      # Expiration (15 minutes from issue)
  "iat": 1707219900,      # Issued at
  "type": "access"
}

# Refresh Token Payload (stored in httpOnly cookie)
{
  "sub": "user_id",
  "exp": 1707824700,      # Expiration (7 days from issue)
  "iat": 1707219900,
  "type": "refresh",
  "jti": "unique_id"      # JWT ID for revocation tracking
}
```

**Best Practices**:
- Store refresh token in httpOnly, Secure, SameSite=Strict cookie
- Store access token in memory (not localStorage to prevent XSS)
- Implement token rotation: issue new refresh token on each refresh request
- Use RS256 if multi-service architecture needed (future), otherwise HS256 sufficient
- Implement token blacklist/revocation for logout (use Redis or CosmosDB)
- Set proper CORS headers to allow credentials

**Security Considerations**:
- HTTPS-only in production (configured in Azure AppService)
- Rotate JWT secret key regularly (stored in Azure Key Vault)
- Implement rate limiting on auth endpoints (5 requests/minute per IP)
- Add CSRF token for cookie-based requests if needed

**Alternatives Considered**:
- Session cookies: Rejected due to stateful requirement (not scalable)
- OAuth2 (third-party): Out of scope for MVP (email/password only)

**References**:
- JWT Best Practices: https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/

---

### Decision 5: Chart.js for Statistics Visualization

**Decision**: Use Chart.js for rendering session statistics charts

**Rationale**:
- **Bundle Size**: ~60KB minified (fits within 200KB budget with other dependencies)
- **Framework-Agnostic**: Works with vanilla JavaScript/TypeScript
- **Accessibility**: Built-in keyboard navigation and screen reader support (WCAG 2.1 AA)
- **Responsive**: Auto-resizes on viewport changes
- **Sufficient Features**: Bar/line charts adequate for session statistics

**Chart Types for Feature**:
- **Bar Chart**: Sessions by practice type (chords, scales, course, songs)
- **Line Chart**: Sessions over time (last 7/30 days trend)
- **Doughnut Chart**: Practice type distribution (percentage breakdown)

**Best Practices**:
- Lazy load Chart.js only on History page (code splitting)
- Use high contrast colors for accessibility (WCAG AA compliant)
- Provide alt text descriptions for screen readers
- Implement keyboard navigation for chart interactions
- Use responsive configuration: `maintainAspectRatio: false`

**Example Configuration**:
```typescript
import { Chart } from 'chart.js/auto';

const config = {
  type: 'bar',
  data: {
    labels: ['Chords', 'Scales', 'Course', 'Songs'],
    datasets: [{
      label: 'Sessions',
      data: [10, 15, 5, 8],
      backgroundColor: ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B']
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true }
    },
    scales: {
      y: { beginAtZero: true }
    }
  }
};
```

**Alternatives Considered**:
- D3.js: Rejected due to complexity and bundle size (~250KB)
- Recharts: Requires React (not using framework)
- ApexCharts: Larger bundle size (~150KB alone, exceeds budget)

**References**:
- Chart.js Documentation: https://www.chartjs.org/docs/latest/
- Accessibility Guide: https://www.chartjs.org/docs/latest/general/accessibility.html

---

### Decision 6: Zod for Client-Side Validation

**Decision**: Use Zod for TypeScript-first schema validation on frontend

**Rationale**:
- **Type Safety**: Automatically infers TypeScript types from schemas
- **Bundle Size**: ~13KB minified (minimal impact)
- **Developer Experience**: Clear error messages, composable schemas
- **Consistency**: Mirrors Pydantic validation on backend

**Validation Schemas**:
```typescript
import { z } from 'zod';

// Session creation schema
export const SessionCreateSchema = z.object({
  practiceType: z.enum(['chords', 'scales', 'course', 'songs']),
  tempo: z.number().int().min(90).max(120).optional(),
  notes: z.string().max(500).optional()
}).refine(
  (data) => {
    // Tempo required for chords and scales
    if (['chords', 'scales'].includes(data.practiceType)) {
      return data.tempo !== undefined;
    }
    return true;
  },
  {
    message: 'Tempo is required for chords and scales',
    path: ['tempo']
  }
);

// User registration schema
export const RegisterSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords must match',
  path: ['confirmPassword']
});
```

**Best Practices**:
- Define schemas in `src/utils/validation.ts` for reuse
- Use `.safeParse()` for error handling without exceptions
- Display validation errors inline on form fields
- Validate on blur and submit (not on every keystroke for UX)

**Alternatives Considered**:
- Yup: Similar features but larger bundle size (~25KB)
- Joi: Not designed for browser use (Node.js focused)
- Manual validation: Error-prone, no type inference

**References**:
- Zod Documentation: https://zod.dev/

---

### Decision 7: Webpack for Bundling & Code Splitting

**Decision**: Use Webpack 5 for module bundling and code splitting

**Rationale**:
- **Code Splitting**: Automatic chunk splitting for route-based lazy loading
- **Tree Shaking**: Dead code elimination reduces bundle size
- **Bundle Analysis**: webpack-bundle-analyzer visualizes size breakdown
- **TypeScript Integration**: ts-loader for TypeScript compilation
- **Asset Management**: CSS, images handled in single build pipeline

**Webpack Configuration Strategy**:
```javascript
// webpack.config.js
module.exports = {
  entry: './src/main.ts',
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    clean: true
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        },
        chartjs: {
          test: /[\\/]node_modules[\\/]chart\.js/,
          name: 'chartjs',
          priority: 20
        }
      }
    }
  },
  performance: {
    maxEntrypointSize: 200000, // 200KB
    maxAssetSize: 200000,
    hints: 'error' // Fail build if budget exceeded
  }
};
```

**Code Splitting Strategy**:
- **Vendor chunk**: All node_modules (e.g., Zod, Fetch API polyfills)
- **Chart.js chunk**: Lazy loaded only on History page
- **Route chunks**: Each page as separate chunk (async import)

**Best Practices**:
- Use contenthash in filenames for cache busting
- Enable source maps in development only (not production)
- Minify with Terser (default in Webpack 5)
- Use compression-webpack-plugin for gzip output
- Configure bundle budget enforcement (fail build if > 200KB)

**Alternatives Considered**:
- Parcel: Simpler but less control over chunk splitting
- Vite: Excellent DX but project standard specifies Webpack

**References**:
- Webpack Documentation: https://webpack.js.org/
- Code Splitting Guide: https://webpack.js.org/guides/code-splitting/

---

## Integration Patterns

### Pattern 1: Frontend-Backend API Communication

**Pattern**: Centralized API client with JWT injection and error handling

```typescript
// src/services/api.ts
class ApiClient {
  private baseUrl: string;
  private authService: AuthService;

  constructor(baseUrl: string, authService: AuthService) {
    this.baseUrl = baseUrl;
    this.authService = authService;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.authService.getAccessToken();
    
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers
      }
    });

    if (response.status === 401) {
      // Attempt token refresh
      const refreshed = await this.authService.refreshToken();
      if (refreshed) {
        return this.request(endpoint, options); // Retry
      }
      // Redirect to login
      window.location.href = '/login';
      throw new Error('Unauthorized');
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Request failed');
    }

    return response.json();
  }

  // Convenience methods
  get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
}

export const apiClient = new ApiClient(
  process.env.API_BASE_URL,
  authService
);
```

**Benefits**:
- Single source of truth for API configuration
- Automatic JWT injection
- Centralized error handling and retry logic
- Type-safe responses with generics

---

### Pattern 2: Optimistic UI Updates

**Pattern**: Update UI immediately, revert on error

```typescript
// src/services/sessions.ts
async function createSession(data: SessionCreate): Promise<Session> {
  // Generate temporary ID
  const tempSession: Session = {
    id: `temp-${Date.now()}`,
    ...data,
    date: new Date(),
    createdAt: new Date(),
    updatedAt: new Date()
  };

  // Update UI immediately
  sessionStore.addSession(tempSession);

  try {
    // Send to backend
    const created = await apiClient.post<Session>('/api/sessions', data);
    
    // Replace temp with real session
    sessionStore.replaceSession(tempSession.id, created);
    
    return created;
  } catch (error) {
    // Revert on error
    sessionStore.removeSession(tempSession.id);
    throw error;
  }
}
```

**Benefits**:
- Perceived performance improvement (instant feedback)
- Better UX for slow network conditions
- Aligns with Constitution performance goal (60fps UI)

---

### Pattern 3: Service Layer Abstraction (Backend)

**Pattern**: Separate business logic from API route handlers

```python
# services/session_service.py
class SessionService:
    def __init__(self, db_client: CosmosClient):
        self.db = db_client
        self.container = db_client.get_database_client('pianotracker') \
                                  .get_container_client('practice_sessions')
    
    async def create_session(
        self,
        user_id: str,
        data: SessionCreate
    ) -> PracticeSession:
        # Validation
        if data.practice_type in ['chords', 'scales'] and data.tempo is None:
            raise ValueError('Tempo required for chords/scales')
        
        # Business logic
        session = PracticeSession(
            id=str(uuid4()),
            user_id=user_id,
            date=datetime.utcnow(),
            **data.dict(),
            partition_key=user_id
        )
        
        # Persistence
        await self.container.create_item(body=session.dict())
        
        return session
    
    async def get_user_sessions(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[PracticeSession]:
        query = """
            SELECT * FROM c 
            WHERE c.user_id = @userId 
              AND c.partition_key = @userId
            ORDER BY c.date DESC
            OFFSET @offset LIMIT @limit
        """
        
        items = self.container.query_items(
            query=query,
            parameters=[
                {"name": "@userId", "value": user_id},
                {"name": "@offset", "value": offset},
                {"name": "@limit", "value": limit}
            ],
            partition_key=user_id
        )
        
        return [PracticeSession(**item) async for item in items]
```

**Benefits**:
- Testable business logic (mock database client)
- Reusable across multiple endpoints
- Clear separation of concerns (aligns with Constitution)

---

## Security Best Practices

### Input Validation
- **Client**: Zod schemas validate all form inputs before submission
- **Server**: Pydantic models validate all request bodies
- **Database**: Parameterized queries prevent SQL injection

### Password Security
- **Hashing**: bcrypt with cost factor 12 (2^12 iterations)
- **Storage**: Never log or display password hashes
- **Transmission**: HTTPS only (enforce with HSTS header)

### CORS Configuration
```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pianotracker.azurewebsites.net",
        "http://localhost:3000"  # Development only
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)
```

### Rate Limiting
```python
# middleware.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest):
    # Login logic
    pass
```

---

## Performance Optimization Strategies

### Frontend
1. **Code Splitting**: Route-based lazy loading reduces initial bundle
2. **Memoization**: Cache computed statistics to avoid recalculation
3. **Debouncing**: 300ms debounce on search/filter inputs
4. **Virtualization**: If session list exceeds 100 items, use virtual scroll

### Backend
1. **Database Indexing**: Composite indexes on `(user_id, date)` and `(user_id, practice_type)`
2. **Connection Pooling**: CosmosDB SDK handles connection pooling automatically
3. **Caching**: Cache user statistics for 5 minutes (future: Redis)
4. **Pagination**: Default 20 items per page, max 100

### Network
1. **Gzip Compression**: Enable on Azure AppService
2. **HTTP/2**: Enabled by default on Azure AppService
3. **CDN**: Not needed for MVP (static assets minimal)

---

## Testing Strategy

### Unit Tests (70% coverage target)

**Frontend (Jest)**:
- Validation schemas (Zod)
- API client methods
- Component rendering logic
- Utility functions (date formatting, tempo validation)

**Backend (pytest)**:
- Pydantic model validation
- Service layer methods (business logic)
- JWT token generation/verification
- Password hashing/verification

### Integration Tests (20% coverage target)

**Frontend**:
- API client + mock server (MSW)
- Form submission flows

**Backend**:
- API endpoint flows (FastAPI TestClient)
- Database queries (CosmosDB emulator)
- Authentication flow (register → login → access protected endpoint)

### E2E Tests (10% coverage target)

**Playwright**:
- Complete user journey: register → login → create session → view history → logout
- Session filtering and statistics
- Error states (invalid input, network failure)
- Accessibility checks (axe-core)

---

## Monitoring & Observability

### Azure Application Insights

**Metrics to Track**:
- API response times (percentiles: p50, p95, p99)
- Error rates by endpoint
- CosmosDB RU consumption
- Active users (daily/weekly)

**Custom Events**:
- Session created (track practice_type distribution)
- Login success/failure
- Token refresh rate

**Alerts**:
- API response time > 500ms for 5 minutes
- Error rate > 5% for 5 minutes
- CosmosDB RU consumption exceeds 80% of provisioned

### Frontend Monitoring

**Real User Monitoring (RUM)**:
- Core Web Vitals (LCP, FCP, TTI, CLS)
- JavaScript errors with stack traces
- Network request timings

---

## Deployment Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
      - name: Run linter
        run: npm run lint
      - name: Run unit tests
        run: npm test -- --coverage
      - name: Check bundle size
        run: npm run build && npm run analyze

  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        working-directory: ./backend
        run: pip install -r requirements.txt
      - name: Run linter
        run: ruff check .
      - name: Run tests
        run: pytest --cov=src --cov-report=term-missing

  deploy-staging:
    needs: [test-frontend, test-backend]
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Azure Staging
        run: |
          az webapp deployment slot create \
            --name pianotracker \
            --resource-group pianotracker-rg \
            --slot staging

  deploy-production:
    needs: [test-frontend, test-backend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Azure Production
        run: |
          az webapp deployment slot swap \
            --name pianotracker \
            --resource-group pianotracker-rg \
            --slot staging \
            --target-slot production
```

---

## Open Questions Resolved

All technical unknowns from the Technical Context have been resolved:

1. ✅ **Language/Version**: TypeScript (latest), Python 3.11+
2. ✅ **Dependencies**: FastAPI, Pydantic, Chart.js, Zod, Webpack
3. ✅ **Storage**: Azure CosmosDB with partition key strategy defined
4. ✅ **Testing**: Jest + Playwright (frontend), pytest (backend)
5. ✅ **Platform**: Modern browsers, Azure AppService (Linux)
6. ✅ **Performance**: Core Web Vitals targets, bundle budget
7. ✅ **Constraints**: WCAG 2.1 AA, mobile-first, integer tempo, no backdating

No additional research required. Ready for Phase 1 (Design).

---

**Next Phase**: Phase 1 - Generate data-model.md, API contracts, and quickstart.md
