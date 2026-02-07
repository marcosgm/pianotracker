<!--
Sync Impact Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Version Change: None → 1.0.0 (Initial constitution)
Modified Principles: N/A (new constitution)
Added Sections:
  - Core Principles (5 principles tailored to simple server-side beginner app)
  - Technical Constraints
  - Development Standards
  - Governance
Templates Status:
  ✅ spec-template.md - Reviewed, aligned with user story priorities
  ✅ plan-template.md - Reviewed, aligned with constitution check requirements
  ✅ tasks-template.md - Reviewed, aligned with simplicity-first development
Follow-up TODOs: None
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-->

# Piano Tracker Constitution

## Core Principles

### I. Simplicity First (NON-NEGOTIABLE)
Every feature MUST be implemented in the simplest way that solves the user's need. Complex solutions require explicit justification and approval before implementation.

- Start with the most straightforward implementation
- No premature optimization or abstraction
- YAGNI (You Aren't Gonna Need It) strictly enforced
- Reject feature creep - if it doesn't help beginners track practice, it doesn't belong

**Rationale**: The project serves beginner pianists who need clarity and ease of use, not technical sophistication. Complexity becomes a maintenance burden and barrier to contribution.

### II. Server-Side Rendering
All UI rendering MUST happen on the server. No client-side JavaScript frameworks or single-page application patterns.

- Use server-side templates for all pages
- Forms submit via standard HTTP POST
- Progressive enhancement acceptable for non-essential interactions
- Keep the frontend dependency footprint minimal

**Rationale**: Server-side rendering ensures fast initial loads, works without JavaScript, simplifies debugging, and aligns with the "extremely simple" project mandate.

### III. Beginner-Friendly Design
Every user-facing feature MUST be designed for pianists with no technical expertise.

- Clear, jargon-free language
- Intuitive workflows requiring minimal explanation
- Forgiving UX - easy to undo mistakes
- Responsive to common beginner needs (motivation tracking, simple metrics)

**Rationale**: The target audience is beginner pianists, not power users. If the interface requires reading documentation, it has failed.

### IV. Data Integrity
Practice session data MUST be reliable, accurate, and protected from loss.

- Database transactions for all state changes
- Input validation on both client and server
- Automatic backups or export functionality
- Clear confirmation before destructive actions

**Rationale**: Users trust the system with their practice history. Data loss or corruption destroys that trust and undermines the entire value proposition.

### V. Privacy & Minimal Data Collection
User data MUST be treated as private and sensitive. Collect only what is necessary for core functionality.

- No tracking or analytics beyond essential error monitoring
- User data belongs to the user - easy export required
- No third-party data sharing without explicit consent
- Local-first storage options preferred where feasible

**Rationale**: Practice habits are personal. Users should feel safe using the tool without surveillance concerns.

## Technical Constraints

**Technology Stack**:
- Server-side language: Python (Flask/Django) or similar simple framework
- Database: SQLite for development, PostgreSQL for production
- Templates: Jinja2 or framework-native templating
- Styling: Plain CSS or minimal framework (no build step required)

**Performance Standards**:
- Page load time: <500ms for typical operations
- Database queries: <100ms for standard views
- Mobile responsive required (beginners practice on all devices)

**Storage Scope**:
- Support 100+ users with 1000+ practice sessions per user
- Plan for data retention of years, not months

## Development Standards

**Testing Requirements**:
- Integration tests for all user journeys (spec.md user stories)
- Contract tests for any API endpoints
- Manual smoke testing before each release

**Code Quality**:
- Clear variable and function names (prefer verbose over clever)
- Comments explaining "why", not "what"
- Consistent formatting via automated tooling
- Maximum function length: 50 lines (exceptions require justification)

**Documentation**:
- README with quick start instructions
- Inline comments for non-obvious logic
- User-facing help text embedded in UI where needed

## Governance

This constitution supersedes all other development practices and preferences. Changes to core principles require:
1. Written justification explaining why the existing principle fails
2. Discussion of alternatives considered
3. Migration plan for affected code
4. Version bump according to semantic versioning

**Compliance Verification**:
- All PRs MUST reference constitution alignment for new features
- Constitution checks integrated into plan.md template
- Complexity violations require documented justification

**Versioning Policy**:
- MAJOR: Breaking changes to core principles (e.g., removing server-side rendering requirement)
- MINOR: New principles added or significant expansion of existing ones
- PATCH: Clarifications, typo fixes, non-semantic refinements

**Amendment Process**:
- Proposed changes documented in `.specify/memory/` with version bump proposal
- Review period of at least 24 hours for major changes
- Update all dependent templates and documentation upon ratification

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07
