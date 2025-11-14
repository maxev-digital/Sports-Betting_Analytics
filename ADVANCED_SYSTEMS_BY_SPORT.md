# Advanced Betting Systems by Sport
## Frontend Component Reference Guide

This document lists all advanced betting systems available in MAX EV Sports, organized by sport. Use this to create the "Advanced Systems" dropdown component for each sport's game cards.

---

## 🏀 NBA (16 Systems)

### ✅ FULLY IMPLEMENTED - ML POWERED

#### 1. **Max EV Boost** (Regression to Mean)
- **Status**: ✅ LIVE - Fully Operational
- **Backend**: `backend/ml/nba_regression_analyzer.py`
- **Performance**: 66.3% win rate, +26.5% ROI (163 alerts, 3,690 games)
- **Description**: XGBoost-powered live total analysis. Detects when live lines drift 2+ standard deviations from predicted value.
- **Confidence Levels**: STRONG (2.5+ SD), MODERATE (2.0-2.49 SD)
- **API Endpoint**: `/api/strategies/regression-to-mean/analyze`
- **Kelly %**: 3-5% of bankroll
- **Sports**: NBA only
- **Difficulty**: MEDIUM

---

### ✅ ACTIVE - BACKTESTED

#### 2. **Quarter Reversal Strategy** (Strategy ID: 14)
- **Status**: ✅ ACTIVE - Backend Complete
- **Performance**: 55-61% win rate, +8-35% ROI
- **Description**: Teams winning 2 consecutive quarters lose the next quarter at 55-61% rate
- **Data**: 1,230 NBA games (2023-2024 season)
- **Breakdown**:
  - Q1-Q2 winners → Q3 loss: 55.3% (+12.1% ROI)
  - Q2-Q3 winners → Q4 loss: 52.7% (+8.9% ROI)
  - Q3-Q4 winners → OT loss: 60.7% (+35.2% ROI)
- **Sports**: NBA
- **Difficulty**: MEDIUM
- **EV Range**: +8% to +35%

#### 3. **Halftime Tracker** (Strategy ID: 23)
- **Status**: ✅ ACTIVE - Backend Complete
- **Performance**: 60.2% ATS, +11.3% ROI (2015-2023)
- **Description**: 2H betting opportunities based on 1H performance and regression
- **Scoring System**: 5 factors (shooting deviation, pace, fatigue, score situation, coaching)
- **Theory**: Teams regress to season averages in 2H
- **Sports**: NBA, NCAAB
- **Difficulty**: MEDIUM
- **EV Range**: +9% to +13%

#### 4. **Momentum Detector** (Strategy ID: 24)
- **Status**: ✅ ACTIVE - Backend Complete
- **Description**: Detects when teams are 'on a run' and live odds haven't adjusted
- **Triggers**:
  - NBA: 10+ point runs
  - Books slow to adjust during momentum shifts
- **Sports**: NBA, NHL
- **Difficulty**: MEDIUM
- **EV Range**: +6% to +15%

#### 5. **Pace Mismatch Detector** (Strategy ID: 25)
- **Status**: ✅ ACTIVE - Backend Complete
- **Performance**: 56-58% ATS on totals
- **Description**: Detects EV opportunities based on pace tempo mismatches
- **Factors**: Fast vs slow teams, rest advantages, home court tempo control
- **Threshold**: 5+ possession mismatch
- **Sports**: NBA, NCAAB
- **Difficulty**: MEDIUM
- **EV Range**: +8% to +15%

#### 6. **End-Game Unders** (Strategy ID: 8)
- **Status**: ✅ ACTIVE - Has Backtest Data
- **Description**: Bet Q4 under when there's a blowout after Q3
- **Trigger**: 15+ point differential after Q3
- **Theory**: Garbage time clock management, both teams sub benches
- **Sports**: NBA, NCAAB
- **Difficulty**: EASY
- **EV Range**: +10% to +20%

---

### ⚠️ PENDING - PLANNED

#### 7. **Favorite Comeback Detection** (Strategy ID: 13)
- **Status**: ⚠️ PENDING - Backend Exists
- **Backend**: `backend/strategies/favorite_comeback_detector.py`
- **Historical Performance**: 60.3% cover 2H spread (2005-2023)
- **Description**: Identifies when pre-game favorites trailing after hot underdog starts are prime comeback candidates
- **Trigger**: Talent gap 5+ PPG, favorite down at halftime
- **Theory**: Underdog variance (hot shooting, crowd energy) regresses to mean
- **Sports**: NBA
- **Difficulty**: MEDIUM
- **EV Range**: +8% to +12%

#### 8. **Hot-Shooting Fade** (Strategy ID: 1)
- **Status**: ⚠️ PENDING
- **Description**: Fade teams that had an unusually hot shooting night in their previous game
- **Trigger**: Teams shooting 15%+ above season average
- **Theory**: Shooting percentages regress to the mean
- **Sports**: NBA, NCAAB
- **Difficulty**: EASY
- **EV Range**: +8% to +15%

#### 9. **Momentum Shift Betting** (Strategy ID: 2)
- **Status**: ⚠️ PENDING
- **Description**: Bet on teams immediately after a major momentum shift in the game
- **Triggers**: Ejections, injury timeouts, flagrant fouls
- **Theory**: Books slow to adjust lines after key events
- **Sports**: NBA, NFL, NHL
- **Difficulty**: MEDIUM
- **EV Range**: +5% to +12%

#### 10. **Injury Cascade Props** (Strategy ID: 3)
- **Status**: ⚠️ PENDING
- **Description**: Target player props on role players when stars get injured mid-game
- **Theory**: Usage rates shift dramatically to role players
- **Sports**: NBA, NFL
- **Difficulty**: HARD
- **EV Range**: +15% to +30%

#### 11. **The Pace Trap** (Strategy ID: 4)
- **Status**: ⚠️ PENDING
- **Description**: Bet overs when slow-paced teams fall behind early
- **Trigger**: Teams ranked 25-30 in pace, trailing by 10+ points
- **Theory**: Slow teams forced to speed up when trailing
- **Sports**: NBA, NCAAB
- **Difficulty**: EASY
- **EV Range**: +10% to +18%

#### 12. **Foul Trouble Overs** (Strategy ID: 5)
- **Status**: ⚠️ PENDING
- **Description**: Bet team totals over when key defenders pick up early fouls
- **Trigger**: Elite defenders sitting with foul trouble
- **Theory**: Opposing team efficiency skyrockets, books undervalue defensive replacements
- **Sports**: NBA, NCAAB
- **Difficulty**: MEDIUM
- **EV Range**: +8% to +16%

#### 13. **Blowout Contrarian Spreads** (Strategy ID: 7)
- **Status**: ⚠️ PENDING
- **Description**: Bet underdogs when they're down big at halftime but showing fight
- **Trigger**: Down 20-25 at half, still competing
- **Theory**: Public hammers favorites, inflating 2H spreads. Garbage time and favorite complacency.
- **Sports**: NBA, NFL
- **Difficulty**: MEDIUM
- **EV Range**: +6% to +14%

#### 14. **Overtime Total Resets** (Strategy ID: 9)
- **Status**: ⚠️ PENDING
- **Description**: Bet under on adjusted OT totals after high-scoring regulation
- **Theory**: Teams exhausted, variance regresses
- **Sports**: NBA, NFL, NHL
- **Difficulty**: MEDIUM
- **EV Range**: +7% to +15%

#### 15. **Fatigue Spreads (Back-to-Backs)** (Strategy ID: 10)
- **Status**: ⚠️ PENDING
- **Backend**: `backend/strategies/b2b_vs_rested_strategy.py`
- **Description**: Bet against teams on 2nd night of B2B playing against rested opponents
- **Theory**: Live lines don't adjust enough for cumulative fatigue. Performance drops Q3-Q4.
- **Sports**: NBA, NHL
- **Difficulty**: EASY
- **EV Range**: +8% to +16%

#### 16. **Coaching Timeout Value** (Strategy ID: 11)
- **Status**: ⚠️ PENDING
- **Description**: Bet against teams immediately after burning all timeouts early
- **Theory**: Can't stop opponent runs or draw up plays in crucial moments
- **Sports**: NBA, NFL
- **Difficulty**: HARD
- **EV Range**: +5% to +12%

---

## 🏀 NCAA BASKETBALL (7 Systems)

### ✅ FULLY IMPLEMENTED - ML POWERED

#### 1. **Max EV Boost** (Regression to Mean)
- **Status**: ✅ LIVE - Fully Operational
- **Backend**: `backend/ml/ncaab_regression_analyzer.py`
- **Performance**: 60.0% win rate, +14.5% ROI (30 alerts, 675 games)
- **Description**: XGBoost-powered live total analysis using KenPom efficiency ratings
- **Features**: 8 KenPom metrics (AdjEM, OffEff, DefEff, Tempo)
- **Confidence Levels**: EXTREME (2.5+ SD), STRONG (2.0-2.49 SD), MODERATE (1.5-1.99 SD)
- **API Endpoint**: `/api/strategies/regression-to-mean/analyze`
- **Kelly %**: 3-5% of bankroll
- **Sports**: NCAAB only
- **Difficulty**: MEDIUM

---

### ✅ ACTIVE - BACKTESTED

#### 2. **Halftime Tracker** (Strategy ID: 23)
- Same as NBA - see above

#### 3. **Pace Mismatch Detector** (Strategy ID: 25)
- Same as NBA - see above

#### 4. **End-Game Unders** (Strategy ID: 8)
- Same as NBA - see above

---

### ⚠️ PENDING - PLANNED

#### 5. **Hot-Shooting Fade** (Strategy ID: 1)
- Same as NBA - see above

#### 6. **The Pace Trap** (Strategy ID: 4)
- Same as NBA - see above

#### 7. **Foul Trouble Overs** (Strategy ID: 5)
- Same as NBA - see above

---

## 🏒 NHL (5 Systems)

### ✅ PROVEN - LIVE

#### 1. **Goalie Pull Alert** (Strategy ID: 6)
- **Status**: ✅ PROVEN - Verified with Moneypuck data
- **Backend**: `backend/strategies/Goalie_Pull_Predictor.py`
- **Performance**: 80.4% hit rate, +42% ROI
- **Description**: Bet team totals over when trailing teams pull their goalie early
- **Data**: 581 goalie pulls (2023-24 NHL season)
- **Statistics**: 0.97 goals added per game on average
- **Theory**: Empty net situations create asymmetric scoring opportunities
- **Sports**: NHL only
- **Difficulty**: EASY
- **EV Range**: +45% to +65%

---

### ✅ ACTIVE - BACKTESTED

#### 2. **Momentum Detector** (Strategy ID: 24)
- **Status**: ✅ ACTIVE - Backend Complete
- **Description**: Detects when teams are 'on a run' and live odds haven't adjusted
- **Triggers**:
  - Goal clusters: 2+ goals in 5 minutes
  - Shot spikes
- **Sports**: NBA, NHL
- **Difficulty**: MEDIUM
- **EV Range**: +6% to +15%

---

### ⚠️ PENDING - PLANNED

#### 3. **Momentum Shift Betting** (Strategy ID: 2)
- Same as NBA - see above

#### 4. **Overtime Total Resets** (Strategy ID: 9)
- Same as NBA - see above

#### 5. **Fatigue Spreads (Back-to-Backs)** (Strategy ID: 10)
- Same as NBA - see above

---

## 🏈 NFL (7 Systems)

### ⚠️ ALL PENDING - PLANNED

#### 1. **Momentum Shift Betting** (Strategy ID: 2)
- Same as NBA - see above

#### 2. **Injury Cascade Props** (Strategy ID: 3)
- Same as NBA - see above

#### 3. **Blowout Contrarian Spreads** (Strategy ID: 7)
- Same as NBA - see above

#### 4. **Overtime Total Resets** (Strategy ID: 9)
- Same as NBA - see above

#### 5. **Coaching Timeout Value** (Strategy ID: 11)
- Same as NBA - see above

#### 6. **Weather-Driven Live Totals** (Strategy ID: 12)
- **Status**: ⚠️ PENDING
- **Backend**: `backend/strategies/weather_strategy.py`
- **Description**: Bet unders when weather deteriorates during outdoor games
- **Trigger**: Wind gusts, rain intensity worse than forecast
- **Theory**: Pregame totals set on forecasts, live totals lag real-time weather impact
- **Sports**: NFL, MLB
- **Difficulty**: MEDIUM
- **EV Range**: +10% to +20%

#### 7. **Key Numbers Strategy** (Strategy ID: 21)
- **Status**: ⚠️ PENDING
- **Backend**: `backend/strategies/key_numbers.py`
- **Description**: Analyzes NFL spreads for key number opportunities (3, 7, 10)
- **Statistics**:
  - Key number 3: 15.1% of NFL games
  - Key number 7: 9.0% of NFL games
- **Theory**: Half-point positions near key numbers provide significant edge
- **Sports**: NFL only
- **Difficulty**: EASY
- **EV Range**: +10% to +18%

---

## ⚾ MLB (1 System)

### ⚠️ PENDING - PLANNED

#### 1. **Weather-Driven Live Totals** (Strategy ID: 12)
- Same as NFL - see above

---

## 🌐 MULTI-SPORT / UNIVERSAL TOOLS (7 Systems)

These systems work across ALL sports: NBA, NFL, NHL, MLB, NCAAB, NCAAF

### ⚠️ ALL PENDING - PLANNED

#### 1. **Line Movement Arbitrage** (Strategy ID: 15)
- **Status**: ⚠️ PENDING
- **Description**: Capitalize on line movement discrepancies between bookmakers
- **Theory**: Different books adjust lines at different speeds
- **Sports**: NBA, NFL, NHL, MLB, NCAAB, NCAAF
- **Difficulty**: MEDIUM
- **EV Range**: +2% to +8%

#### 2. **Middle Opportunity Detection** (Strategy ID: 16)
- **Status**: ⚠️ PENDING
- **Description**: Identify and exploit middle betting opportunities across multiple bookmakers
- **Theory**: Line discrepancies create windows where you can bet both sides with a chance to win both
- **Sports**: NBA, NFL, NHL, MLB, NCAAB, NCAAF
- **Difficulty**: EASY
- **EV Range**: +5% to +15%

#### 3. **Sharp Money Tracking** (Strategy ID: 17)
- **Status**: ⚠️ PENDING
- **Backend**: `backend/strategies/sharp_money_tracker.py`
- **Description**: Follow professional betting patterns by monitoring line movements without corresponding public betting trends
- **Theory**: Sharp money moves lines even when public is betting the other side (reverse line movement)
- **Sports**: NBA, NFL, NHL, MLB, NCAAB, NCAAF
- **Difficulty**: HARD
- **EV Range**: +4% to +10%

#### 4. **CLV Tracker (Closing Line Value)** (Strategy ID: 18)
- **Status**: ⚠️ PENDING
- **Backend**: `backend/strategies/clv_tracker.py`
- **Description**: Tracks whether user bets beat the closing line - the most important metric for long-term profitability
- **Theory**: Beating closing line = 53%+ win rate long-term. Market is most efficient at closing.
- **Benchmark**: Sharp bettors average +2 to +5 points CLV
- **Sports**: NBA, NFL, NHL, MLB, NCAAB, NCAAF
- **Difficulty**: MEDIUM
- **EV Range**: +4% to +10%

#### 5. **Home/Away Splits Strategy** (Strategy ID: 19)
- **Status**: ⚠️ PENDING
- **Backend**: `backend/strategies/home_away_splits.py`
- **Description**: Identifies betting value based on team performance differentials between home and away games
- **Statistics**:
  - Teams with 10+ point home/away differential: 56-58% ATS
  - Extreme home teams hosting weak road teams: 60%+ ATS
- **Theory**: Market often undervalues these splits
- **Sports**: NBA, NFL, NHL, MLB, NCAAB, NCAAF
- **Difficulty**: MEDIUM
- **EV Range**: +6% to +14%

#### 6. **Divisional Rivalries Strategy** (Strategy ID: 20)
- **Status**: ⚠️ PENDING
- **Backend**: `backend/strategies/divisional_rivalries.py`
- **Description**: Identifies betting value in division games based on historical trends and rivalry dynamics
- **Statistics**:
  - NFL Division Games: Underdogs 54-56% ATS (vs 48-50% non-division)
  - NBA Division Games: Totals 53% UNDER
- **Theory**: Division games are MORE competitive as teams know each other well
- **Sports**: NBA, NFL, NHL, NCAAB, NCAAF
- **Difficulty**: MEDIUM
- **EV Range**: +4% to +10%

#### 7. **Low-Hold Opportunities** (Strategy ID: 22)
- **Status**: ⚠️ PENDING
- **Backend**: `backend/strategies/low_hold.py`
- **Description**: Identifies betting opportunities with low bookmaker hold (vig)
- **Benchmark**: Sharp books (Pinnacle, Circa) have 2-3% hold
- **Theory**: Betting only <3% hold games improves expected ROI by 1-2%
- **Sports**: NBA, NFL, NHL, MLB, NCAAB, NCAAF
- **Difficulty**: EASY
- **EV Range**: +2% to +5%

---

## Summary Statistics

### By Implementation Status

- **✅ FULLY IMPLEMENTED (ML-Powered)**: 2 systems
  - NBA Max EV Boost
  - NCAAB Max EV Boost

- **✅ PROVEN (Verified)**: 1 system
  - NHL Goalie Pull Alert

- **✅ ACTIVE (Backtested)**: 5 systems
  - Quarter Reversal Strategy (NBA)
  - Halftime Tracker (NBA/NCAAB)
  - Momentum Detector (NBA/NHL)
  - Pace Mismatch Detector (NBA/NCAAB)
  - End-Game Unders (NBA/NCAAB)

- **⚠️ PENDING (Planned)**: 17 systems
  - Various sport-specific and multi-sport strategies

### By Sport

- **NBA**: 16 systems (6 active, 10 pending)
- **NCAAB**: 7 systems (4 active, 3 pending)
- **NHL**: 5 systems (2 active, 3 pending)
- **NFL**: 7 systems (0 active, 7 pending)
- **MLB**: 1 system (0 active, 1 pending)
- **Multi-Sport**: 7 systems (0 active, 7 pending)

### By Difficulty

- **EASY**: 8 systems
- **MEDIUM**: 16 systems
- **HARD**: 3 systems

---

## Frontend Implementation Notes

### Dropdown Component Structure

```typescript
interface AdvancedSystem {
  id: number;
  name: string;
  status: 'live' | 'active' | 'proven' | 'pending';
  description: string;
  sports: string[];
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  evRange: {
    min: number;
    max: number;
  };
  performance?: {
    winRate?: number;
    roi?: number;
    alerts?: number;
    games?: number;
  };
  backend?: string;
  apiEndpoint?: string;
}
```

### Display Icons by Status

- ✅ **LIVE**: Green checkmark, "Fully Operational"
- ✅ **PROVEN**: Gold star, "Verified Performance"
- ✅ **ACTIVE**: Blue checkmark, "Backtested"
- ⚠️ **PENDING**: Yellow warning, "Coming Soon"

### Filtering Logic

When displaying on game cards:
1. Filter systems by current sport (NBA game → show only NBA + Multi-Sport systems)
2. Sort by status: LIVE > PROVEN > ACTIVE > PENDING
3. Show performance metrics only for LIVE/PROVEN/ACTIVE systems
4. For PENDING systems, show "Expected EV Range" instead

### API Integration

For LIVE systems only:
- NBA Max EV Boost: `POST /api/strategies/regression-to-mean/analyze`
- NCAAB Max EV Boost: `POST /api/strategies/regression-to-mean/analyze`

All strategy metadata: `GET /api/strategies?sport=NBA`

---

## Next Steps for Backend Integration

Once frontend dropdown is built, connect these systems to backend:

1. **Immediate Priority** (LIVE systems):
   - NBA Max EV Boost live alerts
   - NCAAB Max EV Boost live alerts
   - NHL Goalie Pull alerts

2. **High Priority** (ACTIVE systems):
   - Quarter Reversal detection
   - Halftime Tracker analysis
   - Momentum Detector
   - Pace Mismatch alerts

3. **Future Development** (PENDING systems):
   - Implement remaining 17 strategies
   - Build backtesting infrastructure
   - Create API endpoints for each strategy

---

**Last Updated**: 2025-11-08
**Backend Contact**: Backend ML systems fully operational
**Frontend Contact**: Ready for component creation
