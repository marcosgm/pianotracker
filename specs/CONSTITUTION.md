# Piano Tracker Constitution

**Version:** 1.0 | Updated: February 6, 2026

Core principles guiding development decisions to deliver quality, performance, and delightful user experience.

---

## 1. Code Quality

**Write for humans, optimize for machines**

- Clarity over cleverness—readable, maintainable code
- Single responsibility: functions < 50 lines, components < 200 lines
- TypeScript strict mode, avoid `any`, explicit public APIs
- Abstract after 3+ repetitions
- Handle all errors explicitly, use error boundaries
- All PRs reviewed, < 400 lines, single concern

---

## 2. Testing Standards

**Minimum 80% coverage | 100% for critical paths**

**Test Pyramid:**
- 70% Unit Tests
- 20% Integration Tests  
- 10% E2E Tests

**Principles:**
- Test behavior, not implementation
- One behavior per test, clear naming
- Deterministic tests only—no flakes
- TDD for complex logic and bug fixes
- All tests pass before merge

---

## 3. User Experience

**WCAG 2.1 AA compliance is mandatory**

- Use design system tokens exclusively
- Keyboard accessible, proper ARIA labels
- Contrast: 4.5:1 (text), 3:1 (UI)
- Mobile-first, min viewport 320px, touch targets 44x44px
- Loading states for async > 300ms
- Consistent patterns and terminology
- Helpful empty and error states
- Offline support for viewing data

---

## 4. Performance

**Core Web Vitals Targets:**
- LCP < 2.5s
- FCP < 1.5s
- TTI < 3.5s
- CLS < 0.1
- Bundle < 200KB gzipped

**Runtime:**
- 60fps UI (16ms updates)
- Virtualize lists > 50 items
- Debounce inputs (300ms), throttle scroll (100ms)
- API: < 200ms reads, < 500ms writes
- Optimistic updates, pagination (20/page)

**Assets:**
- WebP images, lazy load
- Code splitting, tree-shaking
- Monitor RUM, enforce budgets in CI

---

## 5. Data & Security

- Validate input client + server
- Collect minimal necessary data
- Allow export and deletion
- Encrypt at rest and in transit
- Use transactions, automated backups

---

## 6. Documentation

- Comment complex logic (the "why")
- JSDoc for public APIs
- Keep ARCHITECTURE.md current
- Update feature docs with code

---

## 7. Deployment

- Staged rollout: dev → staging → production
- Feature flags for gradual releases
- All tests pass, rollback plans documented
- Monitor errors and key metrics

---

## Evolution

Living document—quarterly reviews. Propose changes via RFC, team approval required.

**Next Review:** May 6, 2026

---

*Quality is a habit. Build great habits.*
