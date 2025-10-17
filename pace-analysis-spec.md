# NBA Live Game Pace & Total Projection Module - Requirements

## Overview
Build a live betting dashboard module that calculates whether an NBA game is trending OVER or UNDER the posted total, and identifies betting value based on current odds using pace analysis, shooting efficiency, and statistical projections.

---

## 1. Data Inputs Required

### Current Game Stats (Both Teams)
- Minutes played in game
- Field goals made/attempted (FGM/FGA)
- 3-pointers made/attempted (3PM/3PA)
- Free throws made/attempted (FTM/FTA)
- Offensive rebounds (OREB)
- Turnovers (TO)
- Current score

### Season Averages (Both Teams)
- Season pace (possessions per 48 minutes)
- Season FG%, 3P%, FT%
- Season average points per game (PPG)

### Betting Data
- Game total line (e.g., 225.5)
- Current OVER odds (e.g., -110)
- Current UNDER odds (e.g., -110)

---

## 2. Calculation Logic

### Step A: Calculate Current Pace

```
Possessions (per team) = FGA - OREB + TO + (0.4 × FTA)

Current game pace = ((Team A possessions + Team B possessions) / 2) / (Minutes played / 48)

Expected pace = (Team A season pace + Team B season pace) / 2

Pace differential = Current game pace - Expected pace
```

### Step B: Calculate Shooting Efficiency Variance

```
For each team:
  FG efficiency ratio = Current FG% / Season FG%
  3P efficiency ratio = Current 3P% / Season 3P%
  FT efficiency ratio = Current FT% / Season FT%
  
  Overall efficiency factor = (FG efficiency × 0.50) + (3P efficiency × 0.30) + (FT efficiency × 0.20)
```

**Interpretation:**
- Efficiency factor > 1.0 = Team is shooting better than season average (hot)
- Efficiency factor < 1.0 = Team is shooting worse than season average (cold)
- Efficiency factor = 1.0 = Team is shooting at season average

### Step C: Project Final Score with Regression

```
Time-based confidence weight:
  - If minutes_played < 12: season_weight = 0.60, current_weight = 0.40
  - If minutes_played >= 12 AND < 24: season_weight = 0.40, current_weight = 0.60
  - If minutes_played >= 24: season_weight = 0.25, current_weight = 0.75

Regression factor = 0.7 + (0.3 × overall_efficiency_factor)
  (This regresses hot/cold shooting toward the mean)

For each team:
  Current points_per_minute = Current score / Minutes played
  
  Projected_from_current = points_per_minute × 48 × regression_factor
  
  Projected_final_score = (Projected_from_current × current_weight) + (Season_PPG × season_weight)

Projected total = Team A projected score + Team B projected score
```

### Step D: Calculate Betting Edge & Expected Value

```
Line differential = Projected total - Game total line

Convert American odds to implied probability:
  If odds < 0: Implied_prob = |odds| / (|odds| + 100)
  If odds > 0: Implied_prob = 100 / (odds + 100)

Calculate our true probability using normal distribution:
  Standard deviation = 10 points
  P(Over) = Probability that final score > line (using normal CDF with our projection as mean)
  P(Under) = 1 - P(Over)

Expected Value (EV) calculations:
  For a $100 bet:
    If odds = -110: Risk $110 to win $100
    If odds = +110: Risk $100 to win $110
  
  Over EV% = ((P(Over) - Implied_prob_over) / Implied_prob_over) × 100
  Under EV% = ((P(Under) - Implied_prob_under) / Implied_prob_under) × 100

Bet recommendation:
  - Only recommend if EV > 3%
  - Choose side with highest positive EV
  - Flag as "HIGH VALUE" if EV > 5%
```

---

## 3. Dashboard Display Requirements

### Visual Components Needed:

#### Game Header
- Team names and logos
- Current score
- Time remaining / Quarter
- Game status (Live/Final)

#### Pace Analysis Section
- **Current Pace:** Display with units (possessions/48min)
- **Expected Pace:** Based on season averages
- **Pace Differential:** Show as +/- with percentage
  - Green if significantly faster than expected
  - Red if significantly slower
  - Gray if near expected
- **Total Possessions:** Running count for both teams

#### Shooting Efficiency Section
Display for each team in a table or card format:
- **FG%:** Current vs Season (e.g., "45.2% vs 46.8%")
- **3P%:** Current vs Season
- **FT%:** Current vs Season
- **Overall Efficiency Factor:** Display as percentage above/below 100%
  - Color code: Green if > 105%, Red if < 95%, Yellow if 95-105%

#### Projection Panel (Most Prominent)
- **Projected Final Total:** Large display (e.g., "228.5")
- **Game Line:** Show for comparison (e.g., "Line: 225.5")
- **Differential:** +/- from line with color coding
  - Green if projecting OVER
  - Red if projecting UNDER
- **Confidence Level:** Based on minutes played
  - Low (< 12 min)
  - Medium (12-24 min)
  - High (24+ min)

#### Betting Recommendation Panel
Only display if positive EV exists:
- **Recommendation:** "BET OVER" or "BET UNDER" (bold, large)
- **Expected Value:** Display as percentage (e.g., "+4.2% EV")
- **Odds:** Current odds for recommended bet
- **Alert Badge:** "🔥 HIGH VALUE" if EV > 5%
- **Confidence Tag:** Show time-based confidence level

#### Additional Metrics (Expandable Section)
- Turnover differential vs season average
- Free throw attempt rate comparison
- Offensive rebound rate
- Time remaining in game
- Points per minute (current vs projected)

---

## 4. Technical Specifications

### Code Structure
- **Language:** TypeScript (preferred) or JavaScript
- **Architecture:** Modular, component-based
- **State Management:** Use appropriate framework (React context, Redux, or similar)
- **Real-time Updates:** Design for frequent recalculation (every 30-60 seconds)

### TypeScript Interfaces Needed

```typescript
interface TeamGameStats {
  fgm: number;
  fga: number;
  threePM: number;
  threePA: number;
  ftm: number;
  fta: number;
  oreb: number;
  turnovers: number;
  currentScore: number;
}

interface TeamSeasonStats {
  pace: number;
  fgPct: number;
  threePct: number;
  ftPct: number;
  avgPointsPerGame: number;
}

interface BettingData {
  totalLine: number;
  overOdds: number;
  underOdds: number;
}

interface GameData {
  minutesPlayed: number;
  teamA: TeamGameStats;
  teamB: TeamGameStats;
  teamASeasonStats: TeamSeasonStats;
  teamBSeasonStats: TeamSeasonStats;
  betting: BettingData;
}

interface ProjectionResult {
  projectedTotal: number;
  paceDifferential: number;
  recommendedBet: 'OVER' | 'UNDER' | 'NONE';
  expectedValue: number;
  confidenceLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  teamAProjection: number;
  teamBProjection: number;
}
```

### Configuration Object
Allow easy adjustment of parameters:

```javascript
const CONFIG = {
  weights: {
    fgWeight: 0.50,
    threePWeight: 0.30,
    ftWeight: 0.20
  },
  timeWeights: {
    early: { season: 0.60, current: 0.40 },  // < 12 min
    middle: { season: 0.40, current: 0.60 }, // 12-24 min
    late: { season: 0.25, current: 0.75 }    // > 24 min
  },
  regression: {
    baseWeight: 0.70,
    efficiencyWeight: 0.30
  },
  betting: {
    minEVThreshold: 3.0,  // Minimum 3% EV to recommend
    highValueThreshold: 5.0, // 5% EV is high value
    projectionStdDev: 10  // Standard deviation for probability calc
  },
  edgeCases: {
    blowoutThreshold: 15,  // Point differential
    blowoutTimeRemaining: 5, // Minutes
    minMinutesForConfidence: 8
  }
};
```

### Core Functions to Implement

1. `calculatePossessions(stats: TeamGameStats): number`
2. `calculateCurrentPace(teamAPoss: number, teamBPoss: number, minutesPlayed: number): number`
3. `calculateEfficiencyFactor(current: TeamGameStats, season: TeamSeasonStats): number`
4. `getTimeWeight(minutesPlayed: number): { season: number, current: number }`
5. `projectFinalScore(gameData: GameData): ProjectionResult`
6. `calculateImpliedProbability(odds: number): number`
7. `calculateExpectedValue(projection: number, line: number, odds: number): number`
8. `detectGarbageTime(gameData: GameData): boolean`

### Error Handling
- Validate all input data (check for null, undefined, negative values)
- Handle division by zero (e.g., zero attempts for shooting percentages)
- Gracefully degrade if season data is missing
- Display appropriate error messages in UI
- Log errors for debugging

### Testing Requirements
- Unit tests for all calculation functions
- Test edge cases:
  - Very early in game (< 5 minutes)
  - Blowout scenarios
  - Overtime games
  - Perfect/terrible shooting performances
  - Missing data scenarios
- Mock data for component testing
- Integration tests for full projection pipeline

### Performance Optimization
- Memoize calculations where appropriate
- Debounce real-time updates if needed
- Minimize re-renders in React components
- Use efficient data structures
- Profile calculation performance (should be < 100ms)

---

## 5. Edge Cases to Handle

### Blowout Games
- **Detection:** 15+ point differential with < 5 minutes remaining
- **Action:** Display warning that garbage time may skew projections
- **Adjustment:** Consider disabling recommendations or adjusting confidence

### Very Low Sample Size
- **Detection:** < 8 minutes played
- **Action:** Display "LOW CONFIDENCE - EARLY GAME" warning
- **Adjustment:** Heavily weight season averages

### Overtime Scenarios
- **Detection:** Minutes played > 48
- **Action:** Adjust pace calculation to use actual minutes
- **Note:** Projections become less relevant, focus on current trends

### Missing Season Data
- **Fallback:** Use league averages if team-specific data unavailable
- **Warning:** Display note that projections use league averages

### Extreme Shooting Performances
- **Detection:** Efficiency factor > 1.3 or < 0.7
- **Action:** Increase regression weight (expect more reversion to mean)
- **Warning:** Note "Unsustainable shooting pace"

### Garbage Time Detection
- If blowout detected, consider:
  - Reducing confidence level
  - Pausing recommendations
  - Showing warning indicator

---

## 6. File Structure Suggestion

```
/src
  /components
    /PaceAnalysis
      - PaceAnalysisPanel.tsx
      - ShootingEfficiency.tsx
      - ProjectionDisplay.tsx
      - BettingRecommendation.tsx
      - MetricsTable.tsx
  /utils
    - paceCalculations.ts
    - projectionEngine.ts
    - bettingMath.ts
    - dataValidation.ts
  /types
    - gameData.types.ts
    - projection.types.ts
  /config
    - constants.ts
  /tests
    - paceCalculations.test.ts
    - projectionEngine.test.ts
    - bettingMath.test.ts
  /hooks
    - useLiveProjection.ts
    - useGameData.ts
```

---

## 7. Implementation Priority

### Phase 1: Core Calculations
1. Implement all calculation functions
2. Create TypeScript interfaces
3. Write unit tests
4. Validate with sample data

### Phase 2: Basic UI
1. Create projection display component
2. Add pace analysis panel
3. Implement betting recommendation display
4. Basic styling and layout

### Phase 3: Enhanced Features
1. Add shooting efficiency visualizations
2. Implement confidence indicators
3. Add edge case handling
4. Create detailed metrics panel

### Phase 4: Integration & Polish
1. Connect to live data source
2. Add real-time updates
3. Performance optimization
4. Final testing and bug fixes

---

## 8. Example Data for Testing

```javascript
const sampleGameData = {
  minutesPlayed: 20,
  teamA: {
    fgm: 18, fga: 42,
    threePM: 6, threePA: 18,
    ftm: 8, fta: 10,
    oreb: 5,
    turnovers: 7,
    currentScore: 50
  },
  teamB: {
    fgm: 20, fga: 45,
    threePM: 8, threePA: 20,
    ftm: 6, fta: 8,
    oreb: 4,
    turnovers: 6,
    currentScore: 54
  },
  teamASeasonStats: {
    pace: 100.5,
    fgPct: 0.462,
    threePct: 0.358,
    ftPct: 0.785,
    avgPointsPerGame: 112.3
  },
  teamBSeasonStats: {
    pace: 98.2,
    fgPct: 0.478,
    threePct: 0.375,
    ftPct: 0.812,
    avgPointsPerGame: 115.7
  },
  betting: {
    totalLine: 225.5,
    overOdds: -110,
    underOdds: -110
  }
};
```

---

## Success Criteria

- [ ] All calculations produce mathematically accurate results
- [ ] UI clearly displays all required metrics
- [ ] Betting recommendations only show when EV > 3%
- [ ] Edge cases are handled gracefully
- [ ] Code is modular and testable
- [ ] Performance is acceptable for real-time updates
- [ ] Unit test coverage > 80%
- [ ] Documentation is clear and complete

---

## Notes

- This module should integrate seamlessly with existing dashboard
- Consider adding visualization charts (pace over time, shooting trends) in future iterations
- May want to add historical accuracy tracking of projections
- Consider adding multiple projection models and comparing them
- Future enhancement: Machine learning model trained on historical data