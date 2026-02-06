# Feature: Visual Chord Reference (Future)

**Status:** Planned  
**Priority:** P2 (Post-MVP)  
**Effort:** Medium (5-7 days)

---

## Description

Interactive piano keyboard visualization showing chord fingerings and note positions, serving as an educational reference and optionally integrating with session logging.

---

## User Stories

- As a user, I want to see a visual representation of chords on a piano keyboard so I can learn proper finger positions
- As a beginner, I want to browse common chords so I can expand my repertoire
- As a user, I want to click a chord and have it auto-fill when logging a practice session
- As a user, I want to search for chords by name so I can quickly find what I need
- As a user, I want to see different chord variations (inversions) for learning

---

## Acceptance Criteria

### Chord Library
- [ ] List of common chords organized by type:
  - Major, Minor
  - 7th, Major 7th, Minor 7th
  - Diminished, Augmented
  - Suspended (sus2, sus4)
- [ ] All 12 root notes for each chord type (C, C#, D, etc.)
- [ ] Search/filter: by name, type, root note
- [ ] Total: ~150-200 chords in library

### Piano Keyboard Visualization
- [ ] SVG-based piano keyboard (1-2 octaves visible)
- [ ] Highlight notes that make up selected chord
- [ ] Color coding:
  - Root note (distinct color, e.g., blue)
  - Other notes (secondary color, e.g., green)
  - Optional: finger numbers (1-5)
- [ ] Responsive: adapts to screen size
- [ ] Accessible: keyboard navigation, ARIA labels

### Chord Details
- [ ] Chord name (e.g., "C Major", "F# Minor 7th")
- [ ] Notes in chord (e.g., C, E, G)
- [ ] Intervals (e.g., Root, Major 3rd, Perfect 5th)
- [ ] Common fingerings (optional, future)
- [ ] Inversions toggle (root position, 1st inversion, 2nd inversion)

### Integration with Session Logging
- [ ] "Practice this chord" button → pre-fill session form with "Chords" type
- [ ] Optional: tag session with specific chord practiced (future extension)

---

## Technical Details

**Frontend:**
- Component: `<PianoKeyboard notes={['C', 'E', 'G']} />`
- SVG generation: Custom component or library (react-piano)
- Chord data: JSON file or database table

**Chord Data Structure:**
```typescript
interface Chord {
  id: string;
  name: string;          // "C Major"
  rootNote: Note;        // "C"
  type: ChordType;       // "major"
  notes: Note[];         // ["C", "E", "G"]
  intervals: string[];   // ["Root", "Major 3rd", "Perfect 5th"]
  inversions?: {
    first: Note[];       // ["E", "G", "C"]
    second: Note[];      // ["G", "C", "E"]
  };
}

type Note = 'C' | 'C#' | 'D' | 'D#' | 'E' | 'F' | 'F#' | 'G' | 'G#' | 'A' | 'A#' | 'B';
type ChordType = 'major' | 'minor' | '7th' | 'maj7' | 'min7' | 'dim' | 'aug' | 'sus2' | 'sus4';
```

**Data Source:**
- Static JSON file (MVP): `/public/data/chords.json`
- Future: Database table for user-contributed chords

**Backend (Optional):**
- GET `/api/chords` - list all chords (with filters)
- GET `/api/chords/:id` - get chord details

---

## UI/UX Notes

### Layout
```
┌──────────────────────────────────────────────┐
│  Chord Reference                             │
├──────────────────────────────────────────────┤
│  Search: [C Major______] 🔍                  │
│                                              │
│  Filter: [All Types ⌄] [All Roots ⌄]        │
├──────────────────────────────────────────────┤
│  Results (48)                                │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  C Major                               │ │
│  │  ┌──────────────────────────────────┐ │ │
│  │  │  Piano Keyboard (C, E, G lit)    │ │ │
│  │  │  ▓░▓░▓ ▓░▓░▓░▓                  │ │ │
│  │  │   █ █ █ █ █ █ █ █               │ │ │
│  │  └──────────────────────────────────┘ │ │
│  │  Notes: C, E, G                        │ │
│  │  Intervals: Root, Major 3rd, P5th      │ │
│  │  [Inversions ⌄] [Practice This]        │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  C Minor                               │ │
│  │  [Piano keyboard...]                   │ │
│  └────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

### Keyboard Visual (SVG)
- Keys: White keys full height, black keys 60% height offset
- Highlighted notes: Glow effect or solid fill
- Responsive: 2 octaves on desktop, 1 octave on mobile (scroll/swipe)
- Touch-friendly: tappable keys (play sound? optional)

---

## Piano Keyboard Component

```tsx
interface PianoKeyboardProps {
  highlightedNotes: Note[];
  rootNote?: Note;
  octaves?: number; // Default: 2
  interactive?: boolean; // Click to play sound
  showLabels?: boolean; // Show note names on keys
}

// Usage
<PianoKeyboard 
  highlightedNotes={['C', 'E', 'G']}
  rootNote='C'
  octaves={2}
/>
```

---

## Chord Generation Algorithm

```typescript
// Generate all chords programmatically
const notes: Note[] = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

const intervals = {
  major: [0, 4, 7],        // Root, Major 3rd, Perfect 5th
  minor: [0, 3, 7],        // Root, Minor 3rd, Perfect 5th
  '7th': [0, 4, 7, 10],    // Major triad + Minor 7th
  'maj7': [0, 4, 7, 11],   // Major triad + Major 7th
  // ... etc
};

function generateChord(root: Note, type: ChordType): Chord {
  const rootIndex = notes.indexOf(root);
  const chordIntervals = intervals[type];
  const chordNotes = chordIntervals.map(interval => 
    notes[(rootIndex + interval) % 12]
  );
  
  return {
    id: `${root}-${type}`,
    name: `${root} ${type}`,
    rootNote: root,
    type,
    notes: chordNotes,
    intervals: getIntervalNames(chordIntervals)
  };
}

// Generate all combinations
const allChords = notes.flatMap(root => 
  Object.keys(intervals).map(type => 
    generateChord(root, type as ChordType)
  )
);
```

---

## Testing

**Unit:**
- Chord generation algorithm
- Note highlighting logic
- Piano key mapping (note → key position)

**Integration:**
- Render keyboard with various chord combinations
- Search/filter functionality

**E2E:**
- Browse chords → select C Major → see highlighted keyboard
- Search for "F# Minor" → find correct chord
- Click "Practice This" → session form opens with Chords selected

---

## Accessibility

- Keyboard navigation: Tab through chords, arrow keys on piano
- Screen reader: Announce chord name, notes, intervals
- High contrast mode: Ensure note highlights visible
- Alternative text view: List notes as text for screen readers

---

## Performance

- SVG optimization: minimize DOM nodes
- Lazy load chord list (virtualized scrolling if > 50)
- Memoize keyboard rendering (avoid re-render on every chord select)

---

## Dependencies

- SVG manipulation (plain SVG or library)
- Chord data (static JSON or generate on-the-fly)
- Optional: Web Audio API for playing notes (future)

---

## Future Enhancements

- **Audio playback**: Click chord → hear it played
- **Custom chords**: Users can create and save custom chord voicings
- **Scales visualization**: Show scale patterns on keyboard
- **Ear training**: Quiz mode to identify chords by sound
- **MIDI integration**: Connect MIDI keyboard, show played notes
- **Practice mode**: Follow-along for practicing chord progressions
- **Hand position photos/videos**: Show proper fingering technique
- **Printable chord charts**: Export PDF of chord collection

---

## Music Theory Notes

### Common Piano Chords (MVP Scope)

**Triads (Major, Minor, Diminished, Augmented):**
- 12 root notes × 4 types = 48 chords

**Seventh Chords (7th, Maj7, Min7, Dim7):**
- 12 root notes × 4 types = 48 chords

**Suspended Chords (Sus2, Sus4):**
- 12 root notes × 2 types = 24 chords

**Total: ~120 chords** (MVP)

Future: Extended chords (9th, 11th, 13th), altered chords, specialized voicings

---

## Open Questions

- Include inversions in initial release or later?
- Audio playback in MVP or Phase 4?
- User-contributed chords (requires moderation)?
- Integration depth with session logging (just type or specific chord tracking)?
