# Feature: Session History & Statistics

**Status:** Not Started  
**Priority:** P0 (Core Feature)  
**Effort:** Large (5-7 days)

---

## Description

View past practice sessions in a filterable list and see aggregate statistics with visualizations to understand practice patterns and progress over time.

---

## User Stories

- As a user, I want to see all my past practice sessions so I can review what I've been working on
- As a user, I want to filter sessions by date range and practice type so I can focus on specific areas
- As a user, I want to see total practice time so I know how much I've practiced
- As a user, I want to see my practice breakdown by type so I can identify imbalances
- As a user, I want to track my tempo improvement over time for chords and scales
- As a user, I want to see my practice streak to stay motivated to practice daily

---

## Acceptance Criteria

### Session List
- [ ] Display sessions in reverse chronological order (newest first)
- [ ] Show: date, duration, practice type, tempo (if applicable), notes preview
- [ ] Pagination: 20 sessions per page
- [ ] Filter controls: date range (preset + custom), practice type (all/specific)
- [ ] Search: filter by notes content (optional)
- [ ] Click session row → expand to show full details + edit/delete buttons
- [ ] Empty state when no sessions match filters
- [ ] Loading state while fetching

### Statistics Dashboard
- [ ] Summary cards:
  - Total practice time (current week/month/all-time toggle)
  - Total session count
  - Current practice streak (consecutive days)
  - Average session duration
- [ ] Practice type breakdown:
  - Bar chart or pie chart showing % and time per type
  - Table with counts and total minutes per type
- [ ] Tempo progression (chords & scales only):
  - Line chart showing average tempo over time
  - Separate lines for chords vs. scales
  - X-axis: date (week/month granularity), Y-axis: BPM
- [ ] Practice calendar heatmap:
  - Visual calendar showing practice days (color intensity = duration)
  - Click day → filter sessions to that date

### Filters & Controls
- [ ] Date range presets: This Week, This Month, Last 30 Days, All Time, Custom
- [ ] Practice type filter: All, Chords, Scales, Course, Songs (multi-select)
- [ ] Apply filters → update both list and statistics
- [ ] Clear filters button
- [ ] URL reflects filter state (shareable links, back button works)

---

## Technical Details

**Frontend:**
- Components: SessionList, SessionCard, StatsDashboard, FilterPanel
- Data fetching: React Query with pagination and filters
- Charts: Chart.js or Recharts
- Calendar heatmap: Custom component or library (react-calendar-heatmap)
- URL state: React Router search params

**Backend:**
- GET `/api/sessions?page=1&limit=20&type=scales&from=2026-01-01&to=2026-02-06`
  - Returns: sessions array + pagination metadata (total, hasNext)
- GET `/api/sessions/stats?period=month`
  - Returns: aggregated statistics (see TECHNICAL_SPEC.md for schema)
- Efficient queries:
  - Index on (user_id, date DESC) for fast filtering/sorting
  - Aggregation in SQL for stats (GROUP BY, AVG, SUM)

**Caching:**
- Stats endpoint: server-side cache (5min TTL)
- Session list: React Query cache (stale-while-revalidate)

---

## UI/UX Notes

### Layout
```
┌────────────────────────────────────────────────┐
│  Practice History                              │
├────────────────────────────────────────────────┤
│  [This Week ⌄] [All Types ⌄] [Clear Filters]  │
├────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────┐ │
│  │  Statistics                               │ │
│  │  ┌───────┐ ┌───────┐ ┌──────┐ ┌──────┐  │ │
│  │  │1350min│ │28 ses │ │7 day │ │48min │  │ │
│  │  │Total  │ │Count  │ │streak│ │Avg   │  │ │
│  │  └───────┘ └───────┘ └──────┘ └──────┘  │ │
│  │                                           │ │
│  │  [Bar Chart: Practice by Type]           │ │
│  │  [Line Chart: Tempo Progression]         │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  Sessions (48 total)                           │
│  ┌──────────────────────────────────────────┐ │
│  │ Feb 6, 2:30 PM · Scales · 45min · 108bpm│ │
│  │ "Worked on C major..."                   │ │
│  └──────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────┐ │
│  │ Feb 5, 3:00 PM · Songs · 60min          │ │
│  │ "Moonlight Sonata first movement"       │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  [← Previous]  Page 1 of 3  [Next →]          │
└────────────────────────────────────────────────┘
```

### Mobile Responsive
- Stack filters vertically
- Stats cards: 2 columns on mobile, 4 on desktop
- Charts: full width, scrollable on small screens
- Session cards: simplified view (hide preview, show on expand)

---

## Statistics Calculations

```sql
-- Total practice time (this month)
SELECT SUM(duration_minutes) 
FROM practice_sessions 
WHERE user_id = $1 
  AND date >= date_trunc('month', CURRENT_DATE);

-- Practice breakdown by type
SELECT 
  practice_type,
  COUNT(*) as count,
  SUM(duration_minutes) as total_minutes
FROM practice_sessions
WHERE user_id = $1
GROUP BY practice_type;

-- Average tempo progression (weekly)
SELECT 
  date_trunc('week', date) as week,
  practice_type,
  AVG(tempo) as avg_tempo
FROM practice_sessions
WHERE user_id = $1 
  AND practice_type IN ('chords', 'scales')
  AND tempo IS NOT NULL
GROUP BY week, practice_type
ORDER BY week ASC;

-- Practice streak (consecutive days)
WITH practice_dates AS (
  SELECT DISTINCT DATE(date) as practice_date
  FROM practice_sessions
  WHERE user_id = $1
  ORDER BY practice_date DESC
),
date_diffs AS (
  SELECT 
    practice_date,
    LAG(practice_date) OVER (ORDER BY practice_date DESC) as prev_date,
    practice_date - LAG(practice_date) OVER (ORDER BY practice_date DESC) as diff
  FROM practice_dates
)
SELECT COUNT(*) + 1 as streak
FROM date_diffs
WHERE diff = -1 OR diff IS NULL
  AND practice_date >= (SELECT MIN(practice_date) FROM date_diffs WHERE diff != -1 OR diff IS NULL);
```

---

## Testing

**Unit:**
- Filter logic (date range, type matching)
- Stats calculations (mocked data)
- Pagination math

**Integration:**
- Fetch sessions with filters
- Fetch stats with period parameter
- Filter changes trigger correct API calls

**E2E:**
- View history → see logged sessions
- Apply filter → list updates
- Navigate pages → pagination works
- View stats → charts render correctly
- Calendar heatmap → click day filters list

---

## Performance

- Initial load (list + stats): < 2s
- Filter application: < 300ms
- Page navigation: < 200ms
- Chart rendering: < 500ms
- Virtualize session list if > 100 items (unlikely per page)

---

## Accessibility

- Chart data available as table (toggle view)
- Skip link from filters to session list
- Screen reader announces filter changes and result counts
- Keyboard navigation through sessions
- Focus management on page change

---

## Dependencies

- Chart.js or Recharts
- Date utility library (date-fns or Day.js)
- React Query (data fetching)

---

## Future Enhancements

- Export data (CSV, JSON, PDF report)
- Custom date range picker with calendar UI
- Advanced stats: practice time by day of week, best practice time
- Comparative stats: this month vs. last month
- Goal tracking: set weekly/monthly goals, show progress
- Achievements/badges: milestones unlocked
