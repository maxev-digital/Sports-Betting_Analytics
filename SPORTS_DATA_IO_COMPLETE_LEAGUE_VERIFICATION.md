# Sports Data IO - Complete League Verification
## Date: November 6, 2025

---

## ✅ LEAGUES WITH FULL ACCESS

| League | Endpoint Type | Games Today | Live Scores | Odds | Status |
|--------|--------------|-------------|-------------|------|---------|
| **NBA** | Date-based | 1 | ✅ | ✅ | **WORKING** |
| **NHL** | Date-based | 9 | ✅ | ✅ | **WORKING** |
| **NFL** | Week-based | 14 (Week 10) | ✅ | ✅ | **WORKING** (needs backend update) |
| **NCAAF** | Date-based | 2 | ✅ | ✅ | **WORKING** |
| **NCAAB** | Date-based | 44 | ✅ | ✅ | **WORKING** |
| **MLB** | Date-based | - | ❌ | ❌ | **NO ACCESS** (401 Unauthorized) |

---

## 📊 DATA STRUCTURE COMPARISON

### Common Fields (ALL LEAGUES)

**Odds Data:**
- `PointSpread` - Point spread (home team perspective)
- `OverUnder` - Total points/goals line
- `AwayTeamMoneyLine` - Away ML odds
- `HomeTeamMoneyLine` - Home ML odds
- `PointSpreadAwayTeamMoneyLine` - Away spread juice
- `PointSpreadHomeTeamMoneyLine` - Home spread juice
- `OverPayout` - Over juice
- `UnderPayout` - Under juice

**Game Info:**
- `Status` - "Scheduled", "InProgress", "Final", "F/OT"
- `DateTime` - Game start time
- `AwayTeam` - Away team abbreviation
- `HomeTeam` - Home team abbreviation
- `Channel` - Broadcast channel
- `Attendance` - Stadium attendance
- `IsClosed` - Boolean for closed betting
- `GameEndDateTime` - When game ended

### Live Score Fields by League

#### NBA (basketball_nba)
```
SCORES:
  AwayTeamScore: 121
  HomeTeamScore: 132

GAME STATE:
  Quarter: null (or "1", "2", "3", "4")
  TimeRemainingMinutes: 7
  TimeRemainingSeconds: 23
  Status: "InProgress" | "Final"

QUARTER-BY-QUARTER:
  Quarters: [
    {
      QuarterID: 175048,
      GameID: 22636,
      Number: 1,
      Name: "1",
      AwayScore: 27,
      HomeScore: 41
    }
  ]
```

#### NHL (icehockey_nhl)
```
SCORES:
  AwayTeamScore: 3
  HomeTeamScore: 5

GAME STATE:
  Period: null (or "1", "2", "3", "OT", "SO")
  TimeRemainingMinutes: 12
  TimeRemainingSeconds: 45
  Status: "InProgress" | "Final"

PERIOD-BY-PERIOD:
  Periods: [
    {
      PeriodID: 75602,
      GameID: 24186,
      Name: "1",
      AwayScore: 1,
      HomeScore: 0,
      ScoringPlays: [...]
    }
  ]
```

#### NFL (americanfootball_nfl)
```
SCORES:
  AwayScore: 28
  HomeScore: 6

GAME STATE:
  Quarter: 1-4 (or "F", "H" for halftime, "OT")
  TimeRemaining: "7:23"
  Status: "InProgress" | "Final" | "Scheduled"

DRIVE DATA (LIVE):
  Possession: "DEN" | "LV"
  Down: 3
  Distance: 7
  YardLine: 35
  YardLineTerritory: "DEN"
  RedZone: true/false
  DownAndDistance: "3rd & 7"
  LastPlay: "Rush for 5 yards..."

QUARTER-BY-QUARTER:
  AwayScoreQuarter1: 7
  AwayScoreQuarter2: 7
  AwayScoreQuarter3: 14
  AwayScoreQuarter4: 0
  HomeScoreQuarter1: 3
  HomeScoreQuarter2: 3
  HomeScoreQuarter3: 0
  HomeScoreQuarter4: 0

WEATHER:
  ForecastTempLow: 63
  ForecastTempHigh: 64
  ForecastDescription: "Scattered Clouds"
  ForecastWindSpeed: 18 mph
  ForecastWindChill: 63°F
```

#### NCAAF (americanfootball_ncaaf)
```
SCORES:
  AwayTeamScore: 13
  HomeTeamScore: 17

GAME STATE:
  Period: "F" (or "1", "2", "3", "4")
  TimeRemainingMinutes: 7
  TimeRemainingSeconds: 23
  Status: "InProgress" | "Final"

DRIVE DATA (LIVE):
  Possession: "BALLST" | "KENTST"
  Down: 3
  Distance: 7
  YardLine: 35
  YardLineTerritory: "BALLST"

PERIODS:
  Periods: [
    {
      PeriodID: 60854,
      GameID: 16366,
      Number: 1,
      Name: "1",
      AwayScore: 0,
      HomeScore: 3
    }
  ]
```

#### NCAAB (basketball_ncaab)
```
SCORES:
  AwayTeamScore: 76
  HomeTeamScore: 92

GAME STATE:
  Period: "F" (or "H1", "H2" for halves)
  TimeRemainingMinutes: 0
  TimeRemainingSeconds: 0
  Status: "InProgress" | "Final"

TOURNAMENT INFO:
  TournamentID: null (or tournament ID)
  Bracket: null
  Round: null
  AwayTeamSeed: null
  HomeTeamSeed: null
```

---

## 🔄 ENDPOINT DIFFERENCES

### Date-Based Endpoints (NBA, NHL, NCAAF, NCAAB)
```
https://api.sportsdata.io/v3/{sport}/scores/json/GamesByDate/{YYYY-MM-DD}
```
**Examples:**
- NBA: `/v3/nba/scores/json/GamesByDate/2025-11-06`
- NHL: `/v3/nhl/scores/json/GamesByDate/2025-11-06`
- NCAAF: `/v3/cfb/scores/json/GamesByDate/2025-11-06`
- NCAAB: `/v3/cbb/scores/json/GamesByDate/2025-11-06`

### Week-Based Endpoint (NFL Only)
```
https://api.sportsdata.io/v3/nfl/scores/json/ScoresByWeek/{Season}{Type}/{Week}
```
**Examples:**
- Regular Season Week 10: `/v3/nfl/scores/json/ScoresByWeek/2025REG/10`
- Playoffs Wild Card: `/v3/nfl/scores/json/ScoresByWeek/2025POST/1`

**Season Types:**
- `REG` = Regular Season (Weeks 1-18)
- `PRE` = Preseason (Weeks 1-4)
- `POST` = Playoffs (Weeks 1-4: Wild Card, Divisional, Conference, Super Bowl)

---

## 📋 FIELD NAME MAPPING

### Score Fields
| Field Type | NBA/NHL/NCAAF/NCAAB | NFL |
|------------|---------------------|-----|
| Away Score | `AwayTeamScore` | `AwayScore` |
| Home Score | `HomeTeamScore` | `HomeScore` |

### Time Fields
| Field Type | All Sports |
|------------|------------|
| Time Minutes | `TimeRemainingMinutes` |
| Time Seconds | `TimeRemainingSeconds` |
| NFL Only | `TimeRemaining` (formatted string "7:23") |

### Period/Quarter Fields
| Sport | Field Name | Values |
|-------|-----------|---------|
| NBA | `Quarter` | null, "1", "2", "3", "4" |
| NHL | `Period` | null, "1", "2", "3", "OT", "SO" |
| NFL | `Quarter` | null, 1, 2, 3, 4, "H", "F", "OT" |
| NCAAF | `Period` | null, "1", "2", "3", "4", "F" |
| NCAAB | `Period` | null, "H1", "H2", "F" |

### Breakdown Arrays
| Sport | Array Name | Sub-Object Fields |
|-------|-----------|-------------------|
| NBA | `Quarters` | `QuarterID`, `Number`, `Name`, `AwayScore`, `HomeScore` |
| NHL | `Periods` | `PeriodID`, `Name`, `AwayScore`, `HomeScore`, `ScoringPlays` |
| NFL | N/A (flat fields) | `AwayScoreQuarter1-4`, `HomeScoreQuarter1-4` |
| NCAAF | `Periods` | `PeriodID`, `Number`, `Name`, `AwayScore`, `HomeScore` |
| NCAAB | N/A | Similar to NBA (has Periods array) |

---

## 🎯 VERIFIED GAME COUNTS (Nov 6, 2025)

| League | Today's Games | Tomorrow's Games | Notes |
|--------|---------------|------------------|-------|
| NBA | 1 game | 11+ games | Regular season active |
| NHL | 9 games | 10+ games | Regular season active |
| NFL | 1 game (TNF) | 0 games | Week 10 in progress |
| NCAAF | 2 games | Many (Saturday) | Week 11 |
| NCAAB | 44 games | Many | Season starting |
| MLB | No access | No access | Off-season + No API access |

---

## ✅ INTEGRATION CHECKLIST

### Backend Adapter Updates Needed

#### 1. Handle League-Specific Score Fields
```python
# Current (wrong for some leagues):
away_score = game.get('AwayScore')
home_score = game.get('HomeScore')

# Should be:
if sport in ['nba', 'nhl', 'cfb', 'cbb']:
    away_score = game.get('AwayTeamScore')
    home_score = game.get('HomeTeamScore')
else:  # NFL
    away_score = game.get('AwayScore')
    home_score = game.get('HomeScore')
```

#### 2. Handle Period/Quarter Naming
```python
# NBA/NCAAB
quarter = game.get('Quarter')

# NHL/NCAAF
period = game.get('Period')

# NFL
quarter = game.get('Quarter')
```

#### 3. Handle Time Remaining Formats
```python
# All sports except NFL
time_str = f"{game['TimeRemainingMinutes']}:{game['TimeRemainingSeconds']:02d}"

# NFL also provides formatted string
time_str = game.get('TimeRemaining') or f"{game['TimeRemainingMinutes']}:{game['TimeRemainingSeconds']:02d}"
```

#### 4. Add NFL Week-Based Endpoint Logic
```python
def get_game_odds(self, sport='NBA', date=None):
    if sport == 'NFL':
        # Calculate week from date
        week = calculate_nfl_week(date)
        endpoint = f'v3/nfl/scores/json/ScoresByWeek/2025REG/{week}'
    else:
        # Date-based for all other sports
        endpoint = f'v3/{sport_lower}/scores/json/GamesByDate/{date}'
```

---

## 🚀 DEPLOYMENT READINESS

### Ready for Production (5 Leagues)
✅ **NBA** - No changes needed (already working)
✅ **NHL** - No changes needed (already working)
✅ **NCAAF** - No changes needed (already working)
✅ **NCAAB** - No changes needed (already working)
🔧 **NFL** - Needs week-based endpoint implementation

### Not Available
❌ **MLB** - No API access (would need to upgrade subscription)

---

## 📝 SUMMARY

**Total Sports Verified:** 6 leagues
**Fully Working:** 4 leagues (NBA, NHL, NCAAF, NCAAB)
**Needs Backend Update:** 1 league (NFL - week endpoint)
**No Access:** 1 league (MLB - subscription limitation)

**Data Available Across All Working Leagues:**
- ✅ Pre-game odds (spread, ML, totals with juice)
- ✅ Live scores (total + by quarter/period)
- ✅ Game state (quarter/period, time remaining)
- ✅ Status tracking (Scheduled, InProgress, Final)
- ✅ Additional metadata (channel, stadium, weather for NFL)

**Consistent Fields:**
- All use `PointSpread`, `OverUnder`, money lines
- All use `Status` for game state
- All provide `TimeRemainingMinutes` and `TimeRemainingSeconds`
- All have breakdown by quarter/period

**Variations:**
- Score fields: `AwayTeamScore`/`HomeTeamScore` vs `AwayScore`/`HomeScore` (NFL)
- Period naming: `Quarter` vs `Period`
- Breakdown format: Array of objects vs flat fields (NFL)
- Endpoint: Date-based vs week-based (NFL)
