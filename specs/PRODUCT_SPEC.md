# Piano Tracker - Product Specification

**Version:** 1.0  
**Last Updated:** February 6, 2026  
**Status:** In Development

---

## Product Vision

A simple, focused web application that helps pianists track their practice sessions, monitor progress, and build consistent practice habits through data-driven insights.

---

## Target Users

- **Primary**: Amateur and intermediate pianists practicing at home
- **Secondary**: Music students tracking structured practice routines
- **Tertiary**: Piano teachers monitoring student progress

---

## Core Features (MVP)

### 1. User Authentication
**What:** Secure login system for personal practice data  
**Why:** Each user needs private access to their practice history

- Email/password registration and login
- Password reset functionality
- Session persistence

### 2. Practice Session Recording
**What:** Quick logging of daily practice sessions  
**Why:** Core value—tracking what was practiced

**Session Attributes:**
- **Date/Time** (auto-captured, editable)
- **Duration** (manual input or timer)
- **Practice Type** (selector):
  - Chords
  - Scales
  - Course/Lessons
  - Songs/Repertoire
- **Tempo** (required for Chords & Scales):
  - Range: 90-120 BPM
  - Input: Number field or slider
- **Notes** (optional): Free-text field for observations

**User Flow:**
1. Click "Add Session"
2. Select practice type
3. If Chords/Scales → enter tempo
4. Enter duration
5. Add optional notes
6. Save

### 3. Session History & Statistics
**What:** View past sessions with summary statistics  
**Why:** Visualize progress and maintain motivation

**History View:**
- Chronological list of sessions (most recent first)
- Filters: Date range, practice type
- Pagination (20 sessions/page)

**Statistics Dashboard:**
- Total practice time (week/month/all-time)
- Sessions by practice type (breakdown %)
- Average tempo progression (for Chords/Scales)
- Practice streak (consecutive days)
- Most practiced type

**Visualization:**
- Simple bar charts for practice time by type
- Line chart for tempo progression over time
- Calendar heatmap showing practice days

---

## Future Features (Post-MVP)

### 4. Practice Recommendations
**What:** AI-suggested training sessions based on history  
**Why:** Help users identify gaps and balance practice types

- Analyze practice patterns
- Suggest underrepresented practice types
- Recommend tempo increases for Chords/Scales mastery
- Weekly practice plan generation

### 5. Visual Chord Reference
**What:** Interactive piano keyboard showing chord fingerings  
**Why:** Educational aid during practice

- Piano keyboard visualization
- Highlight notes for selected chords
- Common chord library (major, minor, 7th, etc.)
- Integration with session logging (select chord → auto-log)

---

## User Stories

### Authentication
- As a user, I want to create an account so I can securely save my practice data
- As a user, I want to log in so I can access my practice history from any device
- As a user, I want to reset my password if I forget it

### Session Logging
- As a user, I want to quickly log a practice session so I can track what I practiced today
- As a user, I want to record tempo when practicing chords/scales so I can monitor my speed improvement
- As a user, I want to add notes to sessions so I can remember specific challenges or breakthroughs
- As a user, I want to edit past sessions so I can correct mistakes

### History & Insights
- As a user, I want to see my practice history so I can review what I've been working on
- As a user, I want to filter sessions by type so I can focus on specific practice areas
- As a user, I want to see statistics so I can understand my practice habits
- As a user, I want to track my tempo progression so I can see my technical improvement
- As a user, I want to see my practice streak so I stay motivated to practice daily

### Future
- As a user, I want practice recommendations so I can balance my training
- As a user, I want to see chord visualizations so I can learn new chords while logging

---

## Success Metrics

**Engagement:**
- Daily active users
- Average sessions logged per user per week
- User retention (30-day, 90-day)

**Feature Usage:**
- Distribution of practice types logged
- % sessions with tempo data
- % sessions with notes

**Quality:**
- Time from login to session logged (< 30s target)
- Error rate on session submission (< 1%)
- User-reported bugs per release

---

## Non-Goals (Out of Scope)

- Video tutorials or lessons (content creation)
- Social features (sharing, following, competitions)
- Audio recording or playback
- Sheet music library or notation
- Mobile native apps (web-first, mobile-responsive)
- Multi-instrument support (piano only)

---

## Design Principles

1. **Speed First**: Logging a session should take < 30 seconds
2. **Data-Driven Motivation**: Show progress clearly and frequently
3. **Privacy-Focused**: User data is private by default
4. **Mobile-Friendly**: Responsive design for practice-side logging
5. **Accessible**: WCAG 2.1 AA compliant (per Constitution)

---

## Release Phases

### Phase 1: MVP (Current Focus)
- User auth
- Session logging (all types, tempo for Chords/Scales)
- Basic history list
- Simple statistics (totals, counts)

### Phase 2: Analytics
- Advanced statistics
- Visual charts and graphs
- Tempo progression tracking
- Practice streak badges

### Phase 3: Intelligence
- Practice recommendations
- Pattern analysis
- Goal setting and tracking

### Phase 4: Visual Learning
- Chord visualization
- Scale patterns on keyboard
- Integration with session logging

---

## Technical Constraints

See [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) for implementation details.

**Key Constraints:**
- Web-based (browser access)
- Offline-capable (view history without connection)
- Performance targets per Constitution (LCP < 2.5s)
- 80%+ test coverage

---

**Next Steps:**
1. UI/UX mockups for session logging flow
2. Database schema design
3. API endpoint specification
4. Sprint planning for Phase 1 features