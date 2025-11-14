# Advanced Systems Data Mismatch Analysis
**Date:** 2025-11-11
**Issue:** Hardcoded sample data in game cards doesn't match real database

---

## PROBLEM

The "Max EV Boost Alerts" section in game cards uses **hardcoded sample data** from `frontend/src/data/advancedSystems.ts` instead of pulling from the actual strategy results database.

### Mismatches Found:

| Strategy | advancedSystems.ts (WRONG) | Database (CORRECT) | Difference |
|----------|---------------------------|-------------------|------------|
| **Goalie Pull (#6)** | 42.0% ROI | 6.8% ROI | -35.2% |
| **Halftime Tracker (#23)** | 11.3% ROI | 3.9% ROI | -7.4% |
| **Quarter Reversal (#14)** | 12.1% ROI | 10.5% ROI | -1.6% |
| **Pace Mismatch (#25)** | 10.0% ROI | 8.4% ROI | -1.6% |
| **Momentum Detector (#24)** | No ROI shown | 2.3% ROI | Missing |

---

## ROOT CAUSE

### Current Flow (WRONG):
```
GameCard.tsx
  → AdvancedSystemsDropdown.tsx
    → advancedSystems.ts (HARDCODED DATA)
      → Displays outdated sample ROI values
```

### Correct Flow (What Strategy Results page does):
```
StrategyResults.tsx
  → API: /api/strategies (fetches ALL strategies)
    → API: /api/strategies/{id}/backtest-results (fetches backtest data)
      → Displays REAL database values
```

---

## EXAMPLES OF HARDCODED SAMPLE DATA

### From advancedSystems.ts:

```typescript
{
  id: 6,
  name: "Goalie Pull Alert",
  performance: {
    winRate: 80.4,
    roi: 42.0,  // ❌ WRONG - Database has 6.8%
    games: 581
  }
}

{
  id: 23,
  name: "Halftime Tracker",
  performance: {
    winRate: 60.2,
    roi: 11.3  // ❌ WRONG - Database has 3.9%
  }
}

{
  id: 1,
  name: "Max EV Boost",
  performance: {
    winRate: 66.3,
    roi: 26.5,  // ❌ WRONG - Database has realistic values
    alerts: 163,
    games: 3690
  }
}
```

---

## SOLUTION OPTIONS

### Option 1: Fetch from API (RECOMMENDED)
Create a hook to fetch strategy backtest results and use real data:

```typescript
// New hook: useStrategyResults.ts
export const useStrategyResults = (strategyId: number) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`/api/strategies/${strategyId}/backtest-results`)
      .then(res => res.json())
      .then(data => setData(data.results));
  }, [strategyId]);

  return data;
};
```

Then update AdvancedSystemCard to use real data instead of hardcoded.

### Option 2: Remove performance data from cards
Just show strategy names/descriptions without ROI claims until data is live.

### Option 3: Update hardcoded values manually
Quick fix: Update advancedSystems.ts with correct values from database, but this will require manual updates every time database changes.

---

## RECOMMENDED FIX

**Update advancedSystems.ts to use corrected ROI values matching the database:**

```typescript
{
  id: 6,
  name: "Goalie Pull Alert",
  performance: {
    winRate: 80.4,
    roi: 6.8,  // ✅ CORRECTED
    games: 581
  }
}

{
  id: 23,
  name: "Halftime Tracker",
  performance: {
    winRate: 60.2,
    roi: 3.9  // ✅ CORRECTED
  }
}

{
  id: 14,
  name: "Quarter Reversal Strategy",
  performance: {
    winRate: 55.7,
    roi: 10.5,  // ✅ CORRECTED
    games: 423
  }
}

{
  id: 24,
  name: "Momentum Detector",
  performance: {
    winRate: 57.8,
    roi: 2.3,  // ✅ ADDED
    games: 234
  }
}

{
  id: 25,
  name: "Pace Mismatch Detector",
  performance: {
    winRate: 56.8,
    roi: 8.4,  // ✅ CORRECTED
    games: 256
  }
}

{
  id: 8,
  name: "End-Game Unders",
  performance: {
    winRate: 61.7,
    roi: 5.1,  // ✅ ADD THIS
    games: 223
  }
}
```

---

## FILES TO UPDATE

1. **frontend/src/data/advancedSystems.ts** - Update hardcoded ROI values
2. **frontend/src/components/AdvancedSystemCard.tsx** - Verify it displays performance.roi correctly

---

## FUTURE IMPROVEMENT

Later, refactor to fetch from API instead of hardcoded data:
- Create useStrategyBacktestResults hook
- Fetch from `/api/strategies/{id}/backtest-results`
- Display live data that stays in sync with database

For now, just update the hardcoded values to match the corrected database.
