# Feature: Practice Recommendations (Future)

**Status:** Planned  
**Priority:** P2 (Post-MVP)  
**Effort:** Large (7-10 days)

---

## Description

AI-powered suggestions for practice sessions based on historical patterns, helping users balance their practice routine and identify areas for improvement.

---

## User Stories

- As a user, I want practice recommendations so I know what to work on next
- As a user, I want to see which practice types I'm neglecting so I can balance my routine
- As a user, I want tempo increase suggestions for chords/scales I've mastered at lower speeds
- As a user, I want weekly practice plan suggestions based on my goals and history

---

## Acceptance Criteria

### Daily Recommendation
- [ ] Show 1-3 suggested practice sessions on dashboard
- [ ] Recommendations based on:
  - Least practiced type in last 7 days
  - Tempo progression readiness (practiced 3+ times at current tempo)
  - Practice pattern gaps (e.g., no scales in 5 days)
- [ ] Click suggestion → pre-fill session form with recommended type/tempo
- [ ] Dismiss suggestion → don't show again for 24h

### Practice Balance Insights
- [ ] Visual indicator of practice type distribution (target: 25% each)
- [ ] Alert when one type drops below 15% of total time (last 30 days)
- [ ] Suggested focus area with reasoning: "You haven't practiced scales in 8 days"

### Tempo Progression Suggestions
- [ ] Analyze tempo history for chords/scales
- [ ] If 3+ sessions at same tempo with consistent duration → suggest +5 BPM
- [ ] Show progression path: "You've mastered 100 BPM, try 105 BPM next"
- [ ] Track tempo milestones (every 10 BPM increase)

### Weekly Practice Plan
- [ ] Generate recommended weekly schedule (7 days)
- [ ] Balance all practice types
- [ ] Suggest optimal practice times based on historical patterns
- [ ] Allow customization: adjust days, durations, types
- [ ] One-click log sessions from plan (pre-filled forms)

---

## Technical Details

**Recommendation Engine:**
- Rule-based algorithm (MVP), ML model (future)
- Inputs: user session history, time period (7/30 days)
- Rules:
  1. Balance: suggest type with lowest % of recent practice
  2. Streak: suggest type not practiced in 3+ days
  3. Tempo: if avg tempo stable (±2 BPM) for 3+ sessions → +5 BPM
  4. Novelty: rotate recommendations to avoid repetition

**Backend:**
- GET `/api/recommendations/daily` - get today's suggestions
- GET `/api/recommendations/weekly-plan` - generate weekly plan
- POST `/api/recommendations/dismiss/:id` - dismiss suggestion

**Calculation Example:**
```typescript
function calculateRecommendations(sessions: Session[]): Recommendation[] {
  // Last 7 days
  const recent = sessions.filter(s => s.date > sevenDaysAgo);
  
  // Calculate practice % by type
  const distribution = calculateDistribution(recent);
  
  // Find underrepresented types (< 20% of practice time)
  const underrepresented = Object.entries(distribution)
    .filter(([type, pct]) => pct < 20)
    .sort((a, b) => a[1] - b[1]); // Least practiced first
  
  // Tempo analysis for chords/scales
  const tempoRecommendations = analyzeTempoProgression(sessions);
  
  return [
    ...underrepresented.map(([type]) => ({
      type: 'balance',
      practiceType: type,
      reason: `Only ${distribution[type]}% of recent practice`
    })),
    ...tempoRecommendations
  ];
}
```

---

## UI/UX Notes

### Dashboard Widget
```
┌─────────────────────────────────────────┐
│  Recommended for Today                  │
├─────────────────────────────────────────┤
│  🎯 Practice Scales                     │
│  You haven't practiced scales in 5 days │
│  Suggested: 30 min at 100 BPM           │
│  [Start Session]  [Dismiss]             │
├─────────────────────────────────────────┤
│  📈 Level Up: Chords                    │
│  You've mastered 95 BPM, try 100 BPM!   │
│  [Start Session]  [Dismiss]             │
└─────────────────────────────────────────┘
```

### Weekly Plan View
```
Mon: Scales (30min, 100bpm) + Songs (45min)
Tue: Chords (30min, 95bpm) + Course (30min)
Wed: Scales (30min, 105bpm)
Thu: Songs (60min)
Fri: Chords (30min, 100bpm) + Scales (30min, 105bpm)
Sat: Course (45min) + Songs (45min)
Sun: Rest day / Light practice

[Customize Plan]  [Save & Use]
```

---

## Testing

**Unit:**
- Recommendation algorithm (various history scenarios)
- Tempo progression detection
- Practice balance calculation

**Integration:**
- Recommendations API with different user histories
- Dismiss functionality

**E2E:**
- View recommendations on dashboard
- Click recommendation → session form pre-filled
- Dismiss recommendation → doesn't reappear

---

## Machine Learning (Future)

### Feature Engineering
- Session frequency patterns (time of day, day of week)
- Duration preferences per practice type
- Tempo progression velocity
- Practice streak patterns
- User goals (if added)

### Model
- Collaborative filtering (similar users' patterns)
- Time-series forecasting (practice schedule prediction)
- Ranking model (prioritize multiple recommendations)

### Training Data
- Anonymized user sessions
- Feedback: accepted vs. dismissed recommendations
- Session outcomes: completed vs. planned

---

## Privacy & Ethics

- Recommendations are personal, not social (no comparisons to other users)
- Opt-out option: disable recommendations entirely
- Transparent reasoning: always explain why something is recommended
- No guilt or shame language: encouraging, not judgmental

---

## Dependencies

- Existing session data (minimum 2 weeks of history)
- Analytics tracking (accepted/dismissed recommendations)

---

## Metrics

- Recommendation acceptance rate (target: 40%+)
- Practice balance improvement after 30 days of use
- User-reported helpfulness (survey)

---

## Future Enhancements

- Goal-based recommendations (e.g., "Preparing for recital")
- Integration with external calendars (Google Calendar sync)
- Smart notifications: "Good time to practice scales!"
- Adaptive recommendations based on feedback
