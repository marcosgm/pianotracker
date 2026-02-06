# Piano Tracker - Development Tasks (Single Developer, 1 Week)

**Last Updated:** February 6, 2026  
**Scope**: MVP only - simple, focused feature set  
**Total Effort**: ~40-48 hours (1 developer, 1 week)

---

## Task Legend

- **Estimate**: Hours (not days)
- **Critical**: Blocks other work
- **Nice-to-have**: Cut if running out of time

---

## Day 1: Scaffolding & Auth (8-10 hours)

### Setup
- [ ] Create GitHub repo, basic directory structure
- [ ] Initialize FastAPI backend (main.py, requirements.txt)
- [ ] Initialize TypeScript frontend (index.html, main.ts, styles.css)
- [ ] Configure pytest for backend tests
- **Estimate: 2 hours**

### Python Backend - Auth
- [ ] Implement User Pydantic model
- [ ] Create POST /auth/register endpoint
  - Hash password with bcrypt
  - Store in CosmosDB
  - Return JWT token
- [ ] Create POST /auth/login endpoint
  - Verify credentials
  - Return JWT token
- [ ] Create simple JWT middleware for protected routes
- [ ] Tests: register, login (valid + error cases)
- **Estimate: 4 hours**

### TypeScript Frontend - Auth UI
- [ ] Create login form (email, password, submit button)
- [ ] Create register form (name, email, password, confirm, submit)
- [ ] Implement form validation (client-side)
- [ ] Store JWT token in localStorage
- [ ] Route protection (redirect unauth users to login)
- **Estimate: 2-3 hours**

---

## Day 2: Session Logging (8-10 hours)

### Backend - Session CRUD
- [ ] Create PracticeSession Pydantic model
- [ ] POST /sessions - Create session
  - Validate tempo requirement (chords/scales only)
  - Insert into CosmosDB
  - Return session
- [ ] GET /sessions - List sessions (user-specific, paginated)
- [ ] DELETE /sessions/:id - Delete session
- [ ] Tests: create, list, validation errors
- **Estimate: 4 hours**

### Frontend - Session Form & List
- [ ] Create session form:
  - Date input (default today)
  - Duration input (minutes)
  - Type selector (chords, scales, course, songs)
  - Conditional tempo field (show only for chords/scales)
  - Notes textarea
  - Submit button
- [ ] Form validation (client-side)
- [ ] Submit → API call → show in list
- [ ] Create session list component:
  - Display all sessions (newest first)
  - Show: date, type, duration, tempo, notes
  - Delete button
- [ ] Style with basic CSS (functional, not fancy)
- **Estimate: 4-5 hours**

---

## Day 3: Statistics & Dashboard (6-8 hours)

### Backend - Stats
- [ ] POST /sessions/stats endpoint
  - Total practice time
  - Sessions by type (counts + minutes)
  - Average tempo by type
  - Practice streak
- [ ] Simple aggregation queries (no complex analytics)
- **Estimate: 2 hours**

### Frontend - Dashboard
- [ ] Create stats display:
  - Total practice time (card)
  - Session count (card)
  - Practice type breakdown (simple list, not fancy chart)
  - Current streak (card)
- [ ] Fetch stats from API on page load
- [ ] Update stats after each new session
- [ ] Add simple date filter (This Week / This Month / All Time)
- [ ] Basic CSS styling
- **Estimate: 3-4 hours**

### Optional (if time permits)
- [ ] Simple bar chart using Chart.js (practice time by type)
- **Estimate: 1-2 hours**

---

## Day 4: Polish & Testing (6-8 hours)

### Backend Testing
- [ ] Core unit tests (Pydantic models, JWT)
- [ ] Integration tests (auth flow, session CRUD)
- [ ] Error handling (validation errors, 404s, 401s)
- [ ] Aim for 80%+ coverage on critical paths only
- **Estimate: 2-3 hours**

### Frontend Testing
- [ ] Basic form validation tests
- [ ] API integration tests (mock API calls)
- [ ] Simple E2E test (register → login → add session → view)
- **Estimate: 1-2 hours**

### UI Polish
- [ ] Mobile responsive CSS (basic, mobile-first)
- [ ] Loading states (spinner on API calls)
- [ ] Error messages (form validation, API errors)
- [ ] Success confirmations (session created)
- [ ] Basic accessibility (form labels, semantic HTML)
- **Estimate: 2-3 hours**

---

## Day 5: Deployment & Final Tweaks (6-8 hours)

### Local Environment
- [ ] Create docker-compose.yml (backend, frontend, CosmosDB emulator)
- [ ] Document local setup (5-10 min quick start)
- [ ] Test locally end-to-end
- **Estimate: 2 hours**

### Azure Deployment
- [ ] Create basic Bicep template (AppService + CosmosDB)
- [ ] Deploy to Azure (staging)
- [ ] Test deployed version
- [ ] Set up env vars properly
- [ ] Create simple deployment docs
- **Estimate: 2-3 hours**

### Final Testing & Bug Fixes
- [ ] Smoke test on deployed site
- [ ] Fix any critical bugs
- [ ] Verify all features work
- [ ] Check performance (basics)
- **Estimate: 1-2 hours**

### Documentation
- [ ] Quick README (what it does, how to run locally)
- [ ] Basic API endpoints list
- [ ] Environment variables setup
- [ ] Known limitations / bugs
- **Estimate: 1 hour**

---

## Scope - What's Included (MVP)

✅ **Core Features:**
- User registration & login
- Add practice session
- View session list
- Delete session
- Simple statistics (totals, breakdown)
- Date-based filtering

✅ **Technical:**
- FastAPI backend with JWT auth
- TypeScript + vanilla JS frontend with CSS
- CosmosDB database
- Deployed on Azure AppService
- Basic tests (unit + E2E)

---

## Scope - What's NOT Included

❌ **Deferred to Phase 2+:**
- Edit session (only delete available)
- Advanced charts/visualizations
- Practice recommendations
- Visual chord reference
- Goal tracking
- User profile/settings
- Export/reporting
- Dark mode
- Advanced analytics
- Offline support

❌ **Not Priority:**
- Comprehensive accessibility (basic only)
- Extensive performance optimization
- Advanced error handling
- Complex form validation (basic only)
- Detailed documentation
- Complex CI/CD

---

## Critical Path (Do These First)

1. ✅ Backend scaffolding + auth (Day 1, ~4h)
2. ✅ Frontend login/register UI (Day 1, ~2h)
3. ✅ Backend session CRUD (Day 2, ~4h)
4. ✅ Frontend session form + list (Day 2, ~4h)
5. ✅ Backend stats endpoint (Day 3, ~2h)
6. ✅ Frontend stats display (Day 3, ~3h)
7. ✅ End-to-end test (Day 4, ~1h)
8. ✅ Deploy to Azure (Day 5, ~2h)

**Total Critical Path: ~22-23 hours**

Remaining ~18-26 hours available for:
- Polish and bug fixes
- Basic testing
- Mobile responsiveness
- Documentation
- Unexpected issues

---

## Time Breakdown by Component

| Component | Time | Notes |
|-----------|------|-------|
| Backend setup | 1h | FastAPI boilerplate |
| Auth (backend) | 4h | Register, login, JWT middleware |
| Auth (frontend) | 2h | Forms, validation, token management |
| Sessions (backend) | 4h | CRUD endpoints, validation |
| Sessions (frontend) | 4h | Form, list, delete UI |
| Stats (backend) | 2h | Simple aggregations |
| Stats (frontend) | 3h | Display, filtering |
| Testing | 4h | Unit + E2E, critical paths only |
| Deployment | 3h | Bicep, Azure, env setup |
| Polish & docs | 3h | CSS, responsiveness, README |
| **Total** | **~40h** | **1 developer, 1 week** |

---

## Realistic Daily Schedule

**Day 1 (7-8h):** Auth complete (backend + frontend)
**Day 2 (8h):** Sessions complete (backend + frontend)
**Day 3 (7h):** Stats complete + start testing
**Day 4 (6h):** Testing, UI polish, bug fixes
**Day 5 (6h):** Deployment, final testing, docs

---

## Must-Have vs Nice-to-Have

### Must Have (Do Not Cut)
- ✅ Login/Register
- ✅ Add session
- ✅ View sessions
- ✅ Delete session
- ✅ Basic stats
- ✅ Date filtering
- ✅ Deployed & working

### Nice-to-Have (Cut if Time Low)
- Edit session
- Advanced stats
- Charts/visualizations
- Accessibility extras
- Comprehensive testing
- Detailed documentation

---

## Potential Shortcuts to Save Time

1. **Skip chart library** - Show stats as simple numbers/lists instead of Chart.js
2. **Skip advanced styling** - Functional CSS, no fancy animations
3. **Minimal testing** - Unit tests for validation only, basic E2E
4. **Simple deployment** - Manual Azure deploy, no complex CI/CD
5. **No advanced filtering** - Just date range, no type filtering initially
6. **No edit feature** - Only add/delete, add edit in Phase 2
7. **Skip offline support** - Online only (no service workers)
8. **Simple forms** - No fancy UX, just functional inputs

---

## Success Criteria (Minimal MVP)

✅ User can register and login  
✅ User can add a practice session  
✅ User can see list of past sessions  
✅ User can delete a session  
✅ User can see total practice time & stats  
✅ User can filter by date range  
✅ Deployed on Azure and accessible  
✅ No major bugs or crashes  
✅ Works on mobile (basic responsive)  

---

## Known Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Scope creep | Keep features strict, defer to Phase 2 |
| CosmosDB learning curve | Use official samples, keep queries simple |
| CSS/styling take too long | Use minimal functional CSS, not pretty |
| Testing takes too long | Test critical paths only (auth, CRUD) |
| Deployment issues | Test locally first, use simple Bicep |
| Time runs out | Have clear cut-off scope, what to skip |

---

## Tools & Libraries (Minimal Setup)

**Backend:**
- FastAPI (auto-generated docs)
- Pydantic (validation)
- python-jose + bcrypt (auth)
- azure-cosmos (CosmosDB)
- pytest (testing)

**Frontend:**
- TypeScript (vanilla, no React)
- Fetch API (HTTP)
- Zod (validation)
- Chart.js (optional stats viz)
- Plain CSS (no CSS framework)

**Deployment:**
- Azure AppService
- Azure CosmosDB
- Bicep (IaC)
- Docker (local dev only)

---

## Post-MVP Roadmap (Phase 2+)

After launch:
1. Edit session feature
2. Chart visualizations
3. Advanced filtering
4. User profile
5. Recommendations engine
6. Visual chord reference

---

**Created:** February 6, 2026  
**Target Launch:** ~February 13, 2026 (1 week)  
**Scope:** MVP only, single developer

