# Implementation Plan: Piano Practice Session Tracker

**Branch**: `001-practice-tracker` | **Date**: 2026-02-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-practice-tracker/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a web-based piano practice session tracker enabling users to authenticate, log daily practice sessions (with type: chords, scales, course, songs; and optional tempo for chords/scales), and view historical session data with statistics. The system uses a TypeScript vanilla SPA frontend, Python FastAPI backend, and Azure CosmosDB for data persistence. Focus is on the three priority user stories: P1-Authentication, P2-Session Logging, P3-History & Statistics.

## Technical Context

**Language/Version**: 
- Frontend: TypeScript (latest stable)
- Backend: Python 3.11+

**Primary Dependencies**: 
- Frontend: Webpack/Parcel (bundling), Fetch API, Zod (validation), Chart.js (stats visualization)
- Backend: FastAPI (async web framework), Pydantic (validation), python-jose (JWT), bcrypt (password hashing), azure-cosmos (CosmosDB SDK)

**Storage**: Azure CosmosDB (NoSQL document database, SQL API)
- Two containers: `users` (partition key: "users"), `practice_sessions` (partition key: user_id)

**Testing**: 
- Frontend: Jest + Playwright (E2E)
- Backend: pytest + pytest-asyncio

**Target Platform**: 
- Frontend: Modern browsers (Chrome, Firefox, Safari, Edge)
- Backend: Linux (Azure AppService)

**Project Type**: Web application (frontend + backend)

**Performance Goals**: 
- Core Web Vitals: LCP < 2.5s, FCP < 1.5s, TTI < 3.5s, CLS < 0.1
- API response: < 200ms reads, < 500ms writes
- Bundle size: < 200KB gzipped

**Constraints**: 
- Mobile-first design (min viewport 320px)
- WCAG 2.1 AA compliance mandatory
- 60fps UI rendering
- Session date is current date only (no backdating in MVP)
- Tempo values are integers only (90-120 bpm)

**Scale/Scope**: 
- Initial target: 1,000 users
- 3 main user stories (P1-P3)
- 25 functional requirements
- Estimated 4-6 weeks development (full-stack)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Code Quality Gates

- ✅ **Single Responsibility**: Functions must be < 50 lines, components < 200 lines
  - *Status*: No violations expected in design
- ✅ **TypeScript Strict Mode**: Avoid `any`, explicit public APIs
  - *Status*: Configured in tsconfig.json with strict: true
- ✅ **Error Handling**: All errors handled explicitly, use error boundaries
  - *Status*: FastAPI exception handlers + try/catch in TypeScript services
- ✅ **Code Review**: All PRs reviewed, < 400 lines, single concern
  - *Status*: Process requirement, enforced via PR templates

### Testing Standards Gates

- ✅ **80% Minimum Coverage / 100% Critical Paths**
  - *Critical paths*: Auth flow (register, login, JWT validation), session CRUD, tempo validation
  - *Status*: pytest-cov + Jest coverage configured with enforcement
- ✅ **Test Pyramid**: 70% unit, 20% integration, 10% E2E
  - *Status*: Designed with pytest (backend) + Jest/Playwright (frontend)
- ✅ **TDD for Complex Logic**: Tempo validation, statistics calculations, JWT token handling
  - *Status*: Tests written first for auth and validation logic
- ✅ **All Tests Pass Before Merge**
  - *Status*: GitHub Actions gate blocks merge on test failure

### User Experience Gates

- ✅ **WCAG 2.1 AA Compliance**
  - *Requirements*: Keyboard accessible, ARIA labels, 4.5:1 text contrast, 3:1 UI contrast
  - *Status*: Verified via axe-core in Playwright E2E tests
- ✅ **Mobile-First Design**: Min viewport 320px, touch targets 44x44px
  - *Status*: CSS media queries, tested on mobile viewports
- ✅ **Loading States for Async > 300ms**
  - *Status*: Loading spinners for API calls in SessionForm, SessionList
- ✅ **Helpful Empty and Error States**
  - *Status*: Empty state for new users ("Log your first session"), error messages for validation failures

### Performance Gates

- ✅ **Core Web Vitals**
  - LCP < 2.5s, FCP < 1.5s, TTI < 3.5s, CLS < 0.1
  - *Status*: Lighthouse CI checks in GitHub Actions
- ✅ **Bundle < 200KB gzipped**
  - *Status*: Webpack bundle analyzer enforces budget
- ✅ **API Response Times**: < 200ms reads, < 500ms writes
  - *Status*: CosmosDB partition key optimization + Application Insights monitoring
- ✅ **60fps UI**: 16ms frame budget
  - *Status*: Debounced inputs (300ms), throttled scroll (100ms)

### Security Gates

- ✅ **Input Validation Client + Server**
  - *Status*: Zod schemas (frontend) + Pydantic models (backend)
- ✅ **Encrypt at Rest and in Transit**
  - *Status*: HTTPS enforced, CosmosDB encryption enabled by default
- ✅ **Password Security**: bcrypt hashing (cost 12)
  - *Status*: Implemented in auth_service.py
- ✅ **JWT Security**: Short-lived access tokens (15min), refresh tokens (7d)
  - *Status*: python-jose with HS256 algorithm

### Documentation Gates

- ✅ **Comment Complex Logic**: JWT validation, statistics aggregation queries
  - *Status*: Inline comments + docstrings for service methods
- ✅ **JSDoc for Public APIs**: TypeScript service exports
  - *Status*: Required in ESLint configuration
- ✅ **Keep ARCHITECTURE.md Current**
  - *Status*: TECHNICAL_SPEC.md already comprehensive

### Deployment Gates

- ✅ **Staged Rollout**: dev → staging → production
  - *Status*: Azure AppService slots configured
- ✅ **Feature Flags**: Gradual releases if needed
  - *Status*: Not required for MVP (all features released together)
- ✅ **All Tests Pass**: Smoke tests post-deployment
  - *Status*: pytest e2e/smoke_tests.py in GitHub Actions

### Gate Evaluation: ✅ PASSED

All constitution requirements are satisfied by the planned architecture and development workflow. No violations or complexity justifications needed.

---

## Post-Design Constitution Re-Check

*Performed after Phase 1 (data-model.md, contracts/, quickstart.md generated)*

### Design Validation

**Data Model Compliance**:
- ✅ Single Responsibility: Each entity (User, PracticeSession) has clear, focused purpose
- ✅ Validation: Client (Zod) + Server (Pydantic) dual validation enforced
- ✅ Security: Password hashing (bcrypt), JWT tokens, input sanitization
- ✅ Performance: Partition key strategy optimizes queries (single-partition reads/writes)

**API Contract Compliance**:
- ✅ RESTful Design: Standard HTTP methods, proper status codes
- ✅ Validation: All endpoints have request/response schemas with constraints
- ✅ Documentation: OpenAPI 3.0.3 spec with examples and error responses
- ✅ Security: JWT Bearer authentication, rate limiting specified
- ✅ Performance: Pagination (limit/offset), filtering to reduce payload size

**Architecture Compliance**:
- ✅ Code Quality: Separation of concerns (models, services, API, DB layers)
- ✅ Testing: 70/20/10 test pyramid specified in quickstart
- ✅ UX: Mobile-first, accessibility (WCAG 2.1 AA), loading states
- ✅ Performance: Bundle budget (< 200KB), Core Web Vitals targets, lazy loading
- ✅ Deployment: Staged rollout (dev → staging → prod), CI/CD pipeline

### Post-Design Gate Result: ✅ PASSED

No changes to architecture required. Design artifacts (data-model.md, contracts/, quickstart.md) fully align with Constitution principles. Implementation can proceed to Phase 2 (tasks breakdown) and Phase 3 (coding).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py              # User Pydantic model
│   │   └── practice_session.py  # PracticeSession Pydantic model
│   ├── services/
│   │   ├── auth_service.py      # Authentication logic (JWT, bcrypt)
│   │   ├── session_service.py   # Session CRUD operations
│   │   └── stats_service.py     # Statistics calculations
│   ├── api/
│   │   ├── auth.py              # Auth endpoints (/api/auth/*)
│   │   ├── sessions.py          # Session endpoints (/api/sessions/*)
│   │   └── middleware.py        # JWT validation, CORS, error handling
│   ├── db/
│   │   └── cosmos_client.py     # CosmosDB connection and queries
│   └── main.py                  # FastAPI app initialization
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_auth_service.py
│   │   └── test_session_service.py
│   ├── integration/
│   │   ├── test_auth_api.py
│   │   └── test_sessions_api.py
│   └── e2e/
│       └── test_full_flow.py
├── requirements.txt
└── pytest.ini

frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.ts
│   │   │   └── RegisterForm.ts
│   │   ├── sessions/
│   │   │   ├── SessionForm.ts   # Log new session
│   │   │   └── SessionList.ts   # Display session history
│   │   └── stats/
│   │       └── StatsCard.ts     # Statistics visualization
│   ├── pages/
│   │   ├── LoginPage.ts
│   │   ├── DashboardPage.ts
│   │   ├── LogSessionPage.ts
│   │   └── HistoryPage.ts
│   ├── services/
│   │   ├── api.ts               # Fetch API wrapper
│   │   ├── auth.ts              # Auth service (token storage)
│   │   └── sessions.ts          # Session API calls
│   ├── types/
│   │   └── index.ts             # TypeScript interfaces
│   ├── utils/
│   │   └── validation.ts        # Zod schemas
│   └── main.ts                  # Entry point
├── tests/
│   ├── unit/
│   └── e2e/                     # Playwright tests
├── public/
│   ├── index.html
│   └── styles.css
├── package.json
├── tsconfig.json
└── webpack.config.js

infrastructure/
├── bicep/
│   ├── main.bicep               # Azure resources
│   └── cosmos.bicep             # CosmosDB configuration
└── .github/
    └── workflows/
        └── deploy.yml           # CI/CD pipeline
```

**Structure Decision**: Web application structure selected. Frontend and backend are separate codebases with independent build/test pipelines. This separation enables independent deployment, clear API contracts, and specialized tooling for each layer. Infrastructure as Code (Bicep) lives in dedicated directory for environment provisioning.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
