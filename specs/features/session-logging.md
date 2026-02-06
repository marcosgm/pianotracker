# Feature: Practice Session Logging

**Status:** Not Started  
**Priority:** P0 (Core Feature)  
**Effort:** Medium (4-6 days)

---

## Description

Quick and intuitive interface for logging practice sessions with type selection, duration tracking, and optional tempo (for chords/scales) and notes.

---

## User Stories

- As a user, I want to quickly log today's practice session in under 30 seconds
- As a user, I want to select what I practiced (chords, scales, course, songs)
- As a user, I want to record tempo when practicing chords/scales to track speed improvement
- As a user, I want to add notes about my session for future reference
- As a user, I want to edit past sessions to correct mistakes
- As a user, I want to delete sessions I logged by accident

---

## Acceptance Criteria

### Create Session
- [ ] Display form with fields: date/time, duration, type, tempo (conditional), notes
- [ ] Date defaults to now, editable
- [ ] Duration: number input (minutes) or timer widget
- [ ] Practice type: radio buttons or select dropdown (chords, scales, course, songs)
- [ ] Tempo field: only show when type is "chords" or "scales"
- [ ] Tempo range: 90-120 BPM, validated
- [ ] Notes: optional textarea
- [ ] Submit creates session and shows success feedback
- [ ] Validation errors shown inline
- [ ] Optimistic UI update (show immediately, rollback on error)

### Edit Session
- [ ] Click session in history → open edit form with pre-filled data
- [ ] Same validation as create
- [ ] Save updates session
- [ ] Cancel discards changes

### Delete Session
- [ ] Delete button with confirmation dialog
- [ ] Success: remove from list with feedback
- [ ] Undo option (5-second window)

---

## Technical Details

**Frontend:**
- Form component: React Hook Form + Zod schema
- Optimistic updates: React Query mutations
- Tempo input: Number input or range slider (90-120)
- Type selector: Radio button group for easy selection
- Date/time picker: Native input or lightweight library

**Backend:**
- POST `/api/sessions` - create
- PUT `/api/sessions/:id` - update
- DELETE `/api/sessions/:id` - delete
- Validation: Zod schema shared with frontend
  - Duration > 0
  - Tempo: null OR (type in [chords, scales] AND tempo 90-120)
  - Date not in future

**Database:**
- practice_sessions table
- Check constraint: tempo required for chords/scales types

---

## UI/UX Notes

### Form Layout
```
┌─────────────────────────────────┐
│  Add Practice Session           │
├─────────────────────────────────┤
│                                 │
│  Date: [Feb 6, 2026 2:30 PM] ⌄ │
│                                 │
│  Duration: [45] minutes         │
│                                 │
│  Practice Type:                 │
│  ○ Chords  ○ Scales             │
│  ○ Course  ○ Songs              │
│                                 │
│  Tempo: [108] BPM  (90-120)     │
│  [━━━━━━●━━] slider             │
│                                 │
│  Notes (optional):              │
│  ┌───────────────────────────┐ │
│  │                           │ │
│  └───────────────────────────┘ │
│                                 │
│  [Cancel]  [Save Session]       │
└─────────────────────────────────┘
```

### Quick Add Variant (Future)
- Minimal version: just type + duration
- Appears as modal/sidebar for speed
- Advanced options collapsible

---

## Validation Rules

```typescript
const sessionSchema = z.object({
  date: z.date().max(new Date(), "Cannot log future sessions"),
  durationMinutes: z.number().int().min(1).max(480), // Max 8 hours
  practiceType: z.enum(['chords', 'scales', 'course', 'songs']),
  tempo: z.number().int().min(90).max(120).optional(),
  notes: z.string().max(1000).optional()
}).refine(
  (data) => {
    if (['chords', 'scales'].includes(data.practiceType)) {
      return data.tempo !== undefined;
    }
    return true;
  },
  { message: "Tempo required for chords and scales", path: ["tempo"] }
);
```

---

## Testing

**Unit:**
- Validation schema (all rules)
- Tempo conditional logic

**Integration:**
- Create session API flow
- Edit session API flow
- Delete session API flow
- Optimistic update rollback on error

**E2E:**
- Log session with all field types
- Log chords session (requires tempo)
- Log songs session (no tempo field shown)
- Edit session and verify changes
- Delete session with confirmation

---

## Performance

- Form renders < 100ms
- Submit response < 500ms
- Optimistic update feels instant

---

## Accessibility

- Keyboard navigable form
- Labels for all inputs
- ARIA live region for success/error messages
- Focus management (error → first invalid field)
- Screen reader announces tempo requirement when chords/scales selected

---

## Dependencies

- React Hook Form
- Zod (validation)
- React Query (mutations)
- Date picker library (optional, can use native)

---

## Future Enhancements

- Timer mode: start/stop practice, auto-calculate duration
- Templates: save common session configs for one-click logging
- Bulk edit: adjust multiple sessions at once
- Import from CSV/JSON
