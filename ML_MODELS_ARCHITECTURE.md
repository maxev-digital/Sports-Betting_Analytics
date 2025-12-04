# ML Models Architecture - Complete System Documentation

**Last Updated**: December 1, 2025
**Status**: NBA & NCAAB Working | NFL & NCAAF Partial

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Current Architecture](#current-architecture)
3. [What We Built Today](#what-we-built-today)
4. [Data Flow](#data-flow)
5. [Model Training & Storage](#model-training--storage)
6. [Prediction Generation](#prediction-generation)
7. [Frontend Display](#frontend-display)
8. [Issues & Solutions](#issues--solutions)
9. [Next Steps](#next-steps)

---

## System Overview

The Max EV Sports platform uses machine learning models to generate daily predictions for 5 sports:
- **NBA** ✅ Working
- **NCAAB** ✅ Working
- **NHL** ⚠️ No stats source configured
- **NFL** ⚠️ Predictions generating but feature mismatch
- **NCAAF** ⚠️ Predictions generating but feature mismatch

### Single Source of Truth
- **Database**: `/root/sporttrader/backend/ml/predictions.db`
- **Schema**: 18 columns including prediction_id, sport, bet_type, predicted_value, market_value, edge, recommendation, confidence

---

## Current Architecture

### VPS Server (148.230.87.135)
```
/root/sporttrader/
├── backend/
│   ├── main.py                          # FastAPI app (port 8000)
│   ├── ml/
│   │   ├── predictions.db               # SINGLE SOURCE OF TRUTH
│   │   ├── models/                      # 87 trained .joblib files
│   │   │   ├── nba_xgboost_totals_latest.joblib
│   │   │   ├── nba_lightgbm_totals_latest.joblib
│   │   │   ├── nba_random_forest_totals_latest.joblib
│   │   │   ├── ncaab_xgboost_totals_latest.joblib
│   │   │   ├── nfl_xgboost_totals_latest.joblib
│   │   │   ├── nfl_totals_metadata_latest.joblib  # Feature names
│   │   │   └── ... (87 total models)
│   │   └── feature_engineering/
│   │       ├── nba_features.py          # NBAFeatureEngineer
│   │       ├── ncaab_features.py        # NCAABFeatureEngineer
│   │       ├── nhl_features.py          # NHLFeatureEngineer
│   │       ├── nfl_features.py          # NFLFeatureEngineer
│   │       └── ncaaf_features.py        # NCAAFFeatureEngineer
│   ├── data/raw/                        # Scraped data
│   │   ├── nba/team_stats.csv           # Official NBA API
│   │   ├── ncaab/kenpom_YYYYMMDD.csv    # KenPom ratings
│   │   ├── nhl/moneypuck/team_stats.csv # NHL advanced stats
│   │   ├── nfl/teamrankings_cache.json  # 32 teams, 100+ stats/team
│   │   └── ncaaf/teamrankings_cache.json # 136 teams
│   ├── routes/
│   │   └── ui_endpoints.py              # API endpoints for frontend
│   ├── run_ml_predictions_all_sports.py # Daily prediction script (CURRENT)
│   └── run_ml_predictions_all_sports_v2.py # Enhanced script (IN PROGRESS)
└── frontend/
    └── dist/                            # Built React app (served by nginx)
```

### Backend Servers
1. **Port 8000**: Main FastAPI (predictions.db, games, etc.)
   - URL: `http://localhost:8000`
   - Nginx proxy: `https://api.max-ev-sports.com`

2. **Port 8888**: Edge Scanner FastAPI (Max EV edges)
   - URL: `http://localhost:8888`
   - Different service, different data source

---

## What We Built Today

### 1. Multi-Sport ML Prediction Script
**File**: `/root/sporttrader/backend/run_ml_predictions_all_sports.py`

**Purpose**: Generate daily predictions for all 5 sports using trained ML models

**Features**:
- Loads 3 models per sport (XGBoost, LightGBM, Random Forest)
- Uses ensemble prediction (median of 3 models)
- Fetches games from `/api/games` endpoint
- Extracts features using sport-specific engineers
- Calculates edge: `((predicted - market) / market) * 100`
- Saves to `predictions.db`

**Current Results** (12/1/2025):
```
NBA:    29 predictions, +4.77% avg edge  ✅
NCAAB:  47 predictions, +5.53% avg edge  ✅
NFL:    11 predictions, -33.33% avg edge (UNDER bets)  ⚠️
NCAAF:  10 predictions, -31.87% avg edge (UNDER bets)  ⚠️
NHL:    0 predictions (no stats source)  ❌
```

### 2. Enhanced Script with Real TeamRankings Data
**File**: `/root/sporttrader/backend/run_ml_predictions_all_sports_v2.py`

**Purpose**: Load REAL team stats from TeamRankings cache for NFL/NCAAF

**Key Changes**:
- Loads TeamRankings cache: `data/raw/nfl/teamrankings_cache.json`
- Maps cache fields to feature engineer expectations:
  ```python
  'pts_per_game' → 'home_ppg'
  'yards_per_play' → 'home_yards_per_play'
  'third_down_conversion_pct' → 'home_third_down_pct'
  'opponent_yards_per_play' → 'home_yards_per_play_allowed'
  'turnover_diff' → 'home_turnover_margin'
  ```
- Team name matching with fuzzy logic
- Bypasses games API for NFL/NCAAF stats

**Status**: Generated predictions but feature mismatch causing low totals

---

## Data Flow

### Daily Workflow (Automated via Cron)

```
7:00 AM CST - Data Collection
├── run_all_scrapers.py
│   ├── NBA: Official NBA API → team_stats.csv
│   ├── NCAAB: KenPom scraper → kenpom_YYYYMMDD.csv
│   ├── NFL: TeamRankings scraper → teamrankings_cache.json
│   ├── NCAAF: TeamRankings scraper → teamrankings_cache.json
│   └── NHL: MoneyPuck scraper → team_stats.csv

8:00 AM CST - ML Predictions
├── run_ml_predictions_all_sports.py
│   ├── Fetch today's games from /api/games
│   ├── Load 3 models per sport (XGB, LGB, RF)
│   ├── Extract features using sport-specific engineer
│   ├── Generate ensemble predictions (median)
│   ├── Calculate edge vs market odds
│   └── Save to predictions.db
│
└── predictions.db (SINGLE SOURCE OF TRUTH)
    ├── prediction_id (PRIMARY KEY)
    ├── sport, bet_type, game_date
    ├── away_team, home_team
    ├── predicted_value, market_value, edge
    ├── recommendation (OVER/UNDER/NO BET)
    ├── confidence (HIGH/MEDIUM/LOW)
    └── created_at

Frontend Display
├── User visits https://max-ev-sports.com
├── React app calls API: https://api.max-ev-sports.com/api/ui/...
└── Backend queries predictions.db and returns JSON
```

### Cron Schedule
```bash
# Daily scraping (7:00 AM CST)
0 7 * * * cd /root/sporttrader && python3 backend/run_all_scrapers.py

# ML Predictions (8:00 AM CST)
0 8 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 run_ml_predictions_all_sports.py >> logs/ml_predictions.log 2>&1
```

---

## Model Training & Storage

### Trained Models (87 files)
**Location**: `/root/sporttrader/backend/ml/models/`

**Format**: `.joblib` (sklearn serialization)

**Per Sport**:
- 3 Totals models: `{sport}_xgboost_totals_latest.joblib`
- 3 Spreads models: `{sport}_xgboost_spreads_latest.joblib`
- 3 Moneyline models: `{sport}_xgboost_moneyline_latest.joblib`
- 1 Metadata file: `{sport}_totals_metadata_latest.joblib`

### Model Metadata Example (NFL)
```json
{
  "feature_names": [
    "home_ppg",
    "away_ppg",
    "home_yards_per_play",
    "away_yards_per_play",
    "home_third_down_pct",
    "away_third_down_pct",
    "home_points_allowed",          // ⚠️ Note: not "home_points_allowed_per_game"
    "away_points_allowed",
    "home_yards_per_play_allowed",
    "away_yards_per_play_allowed",
    "home_third_down_pct_defense",
    "away_third_down_pct_defense",
    "combined_ppg",                  // Derived feature
    "expected_home_scoring",         // Derived feature
    "expected_away_scoring",         // Derived feature
    "home_turnover_margin",
    "away_turnover_margin",
    "is_division_game",
    "is_primetime",
    "temperature_normalized",        // Derived feature
    "wind_speed_normalized"          // Derived feature
  ],
  "feature_count": 21
}
```

### Training Schedule
```bash
# Weekly retraining (Mondays at 4:00 AM - 5:00 AM CST)
0 4 * * 1 python3 ml/autonomous_learning_system.py --sport ncaab
0 4 * * 1 python3 ml/autonomous_learning_system.py --sport nhl
0 5 * * 1 python3 ml/autonomous_learning_system.py --sport nba
0 5 * * 1 python3 ml/autonomous_learning_system.py --sport ncaaf
0 5 * * 1 python3 ml/autonomous_learning_system.py --sport nfl
```

---

## Prediction Generation

### Feature Engineering Flow

#### NBA (Working ✅)
```python
# Games API provides stats
game = {
  'home_team_stats': {
    'pace': 100.5,
    'off_rating': 115.2,
    'def_rating': 108.3,
    'ts_pct': 0.58,
    'efg_pct': 0.54,
    ...
  }
}

# Feature engineer extracts
features = NBAFeatureEngineer.get_totals_features(game_data)
# Returns: numpy array [100.5, 102.3, 115.2, ...]

# Model predicts
prediction = nba_xgboost_model.predict(features)  # e.g., 224.5
market = 220.0
edge = ((224.5 - 220) / 220) * 100  # +2.05%
```

#### NFL (Partial ⚠️)
```python
# TeamRankings cache provides stats
cache = {
  "Dallas": {
    "pts_per_game": 28.5,
    "yards_per_play": 6.2,
    "third_down_conversion_pct": 42.5,
    "opponent_yards_per_play": 5.1,
    "turnover_diff": 3.0,
    ...
  }
}

# Need to map to expected feature names
game_data = {
  'home_ppg': 28.5,
  'home_yards_per_play': 6.2,
  'home_third_down_pct': 42.5,
  'home_yards_per_play_allowed': 5.1,
  'home_turnover_margin': 3.0,
  'home_points_allowed': ???,  # ⚠️ ISSUE: Model expects this exact name
  ...
}
```

### Ensemble Approach
```python
# Load 3 models
models = {
  'xgboost': joblib.load('nba_xgboost_totals_latest.joblib'),
  'lightgbm': joblib.load('nba_lightgbm_totals_latest.joblib'),
  'random_forest': joblib.load('nba_random_forest_totals_latest.joblib')
}

# Get predictions from each
preds = {
  'xgboost': 224.5,
  'lightgbm': 226.2,
  'random_forest': 223.8
}

# Take median (more robust than mean)
ensemble = np.median([224.5, 226.2, 223.8])  # 224.5

# Constrain to valid range
ensemble = max(110, min(270, ensemble))  # NBA valid range
```

### Recommendation Logic
```python
edge = ((predicted - market) / market) * 100

if edge > 2.5:
    recommendation = "OVER"
    confidence = "HIGH" if edge > 5 else "MEDIUM"
elif edge < -2.5:
    recommendation = "UNDER"
    confidence = "HIGH" if edge < -5 else "MEDIUM"
else:
    recommendation = "NO BET"
    confidence = "LOW"
```

---

## Frontend Display

### API Endpoints (Port 8000)

#### 1. Historical Predictions
```
GET /api/ui/historical-predictions
Query params:
  - sport: NBA, NCAAB, NHL, NFL, NCAAF (optional)
  - days: 7 (default)
  - result: WIN, LOSS, PUSH, PENDING (optional)
  - limit: 100 (default)

Response:
{
  "predictions": [
    {
      "game_id": "2025-12-01_Lakers_Warriors_totals_ensemble",
      "game_date": "2025-12-01",
      "sport": "NBA",
      "away_team": "Lakers",
      "home_team": "Warriors",
      "matchup": "Lakers @ Warriors",
      "bet_type": "Totals",
      "predicted_value": 224.5,
      "market_value": 220.0,
      "edge": 2.05,
      "display_edge": "+2.0%",
      "confidence": "MEDIUM",
      "recommendation": "OVER",
      "result": "PENDING",
      "model": "ensemble"
    }
  ],
  "count": 29,
  "date": "2025-12-01"
}
```

#### 2. Today's Best Plays
```
GET /api/ui/best-plays
Query params:
  - min_edge: 2.0 (default)
  - sport: NBA (optional)

Response: Same format as historical-predictions
Filters: game_date = today AND edge >= min_edge
```

#### 3. Model Performance
```
GET /api/ui/model-performance
Query params:
  - sport: NBA, NCAAB, etc.
  - days: 30 (default)

Response:
{
  "sport": "NBA",
  "total_predictions": 450,
  "wins": 247,
  "losses": 198,
  "pushes": 5,
  "win_rate": 0.555,
  "roi": 0.08,
  "total_profit": 36.5,
  "by_bet_type": {
    "totals": {...},
    "spreads": {...},
    "moneyline": {...}
  }
}
```

### Frontend Pages

#### Predictions Database (`/predictions-database`)
- Fetches: `/api/ui/historical-predictions?days=7`
- Displays: Table with filters for sport, date, result
- Shows: All predictions with edges, results, P&L

#### Model Performance (`/model-performance`)
- Fetches: `/api/ui/model-performance?sport=NBA&days=30`
- Displays: Charts and metrics for model accuracy
- Shows: Win rate, ROI, profit by bet type

#### Max EV Edges (`/max-ev-edges`)
- Fetches: `/api/ui/best-plays?min_edge=2.0`
- Displays: Today's top opportunities
- Shows: Only PENDING predictions above threshold

---

## Issues & Solutions

### Issue 1: NFL/NCAAF Feature Mismatch ⚠️
**Problem**: Models trained with feature names that don't match current feature engineer output
- Model expects: `home_points_allowed`
- Engineer provides: `home_points_allowed_per_game`

**Impact**: All NFL predictions = 30.0 (constant), NCAAF predictions = 35-42 (constant)

**Evidence**:
```python
# Model metadata
feature_names = [
  "home_ppg",
  "away_ppg",
  "home_yards_per_play",
  "away_yards_per_play",
  "home_third_down_pct",
  "away_third_down_pct",
  "home_points_allowed",          # ← Model expects this
  "away_points_allowed",
  ...
]

# Feature engineer returns
features = np.array([
  28.5,  # home_ppg
  24.2,  # away_ppg
  6.2,   # home_yards_per_play
  5.8,   # away_yards_per_play
  42.5,  # home_third_down_pct
  38.1,  # away_third_down_pct
  22.0,  # home_points_allowed_per_game  ← Name mismatch!
  ...
])
```

**Solution Options**:
1. **Retrain models** with current feature engineer schema (1 week)
2. **Update feature engineer** to match model expectations (1 hour)
3. **Create adapter layer** to rename features (30 min)

### Issue 2: NHL Missing Stats Source ❌
**Problem**: No stats source configured for NHL in games API or TeamRankings

**Current Sources**:
- NBA: Official NBA API ✅
- NCAAB: KenPom ✅
- NFL: TeamRankings ✅
- NCAAF: TeamRankings ✅
- NHL: ❌ Missing

**Available Options**:
- MoneyPuck (exists in `data/raw/nhl/moneypuck/`)
- MoreHockeyStats (referenced in docs)
- NHL Official API

**Solution**: Configure NHL scraper and add stats enrichment to games API

### Issue 3: TeamRankings Team Name Matching
**Problem**: Games API uses full names ("New England Patriots"), TeamRankings uses short names ("New England")

**Current Workaround**: Fuzzy matching in v2 script
```python
def find_team_stats(full_name, cache, sport):
    # Try exact match
    if full_name in cache:
        return cache[full_name]

    # Try partial match
    for short_name in cache.keys():
        if short_name in full_name:
            return cache[short_name]

    return None
```

**Issues**:
- "New York Giants" vs "New York Jets" (both match "New York")
- "Los Angeles Rams" vs "Los Angeles Chargers"
- "North Texas Mean Green" matches "Texas" instead of "North Texas"

**Better Solution**: Maintain team name mapping table

---

## Next Steps

### Immediate (This Week)
1. ✅ **Fix NFL/NCAAF feature mapping** (DONE - updated v2 script)
2. ⏳ **Test predictions with corrected features** (IN PROGRESS)
3. ⏳ **Verify models produce realistic totals** (NFL should be 40-50, not 30)
4. ⏳ **Configure NHL stats source**
5. ⏳ **Update cron to use working script**

### Short Term (Next 2 Weeks)
1. **Retrain NFL/NCAAF models** with current feature schema
2. **Add team name mapping table** for better matching
3. **Implement NHL predictions** with MoneyPuck data
4. **Add model confidence intervals** (not just point estimates)
5. **Backtest predictions** against historical results

### Long Term (Next Month)
1. **Add player props predictions** (separate models)
2. **Live in-game predictions** (update during games)
3. **Multi-model stacking** (use meta-learner)
4. **Auto-retraining pipeline** (weekly with new data)
5. **A/B testing framework** (compare model versions)

---

## Database Schema

### predictions.db

```sql
CREATE TABLE predictions (
    prediction_id TEXT PRIMARY KEY,
    sport TEXT NOT NULL,
    bet_type TEXT NOT NULL,
    game_date TEXT NOT NULL,
    game_time TEXT,
    away_team TEXT NOT NULL,
    home_team TEXT NOT NULL,
    predicted_value REAL NOT NULL,
    market_value REAL NOT NULL,
    edge REAL NOT NULL,
    recommendation TEXT NOT NULL,
    confidence TEXT NOT NULL,
    model TEXT NOT NULL,
    kelly_pct REAL DEFAULT 0.0,
    over_probability REAL DEFAULT 0.5,
    under_probability REAL DEFAULT 0.5,
    expected_value REAL DEFAULT 0.0,
    created_at TEXT NOT NULL,
    result TEXT,
    actual_value REAL,
    profit_loss REAL
);

CREATE INDEX idx_sport_date ON predictions(sport, game_date);
CREATE INDEX idx_created_at ON predictions(created_at);
CREATE INDEX idx_result ON predictions(result);
```

### Sample Row
```json
{
  "prediction_id": "nba_totals_2025-12-01_Lakers_Warriors",
  "sport": "NBA",
  "bet_type": "totals",
  "game_date": "2025-12-01",
  "game_time": "19:30",
  "away_team": "Los Angeles Lakers",
  "home_team": "Golden State Warriors",
  "predicted_value": 224.5,
  "market_value": 220.0,
  "edge": 2.05,
  "recommendation": "OVER",
  "confidence": "MEDIUM",
  "model": "ensemble",
  "kelly_pct": 0.0,
  "over_probability": 0.5,
  "under_probability": 0.5,
  "expected_value": 0.0,
  "created_at": "2025-12-01T14:00:00+00:00",
  "result": "PENDING",
  "actual_value": null,
  "profit_loss": null
}
```

---

## Key Files Reference

### Scripts
- `run_ml_predictions_all_sports.py` - Current production script (NBA/NCAAB working)
- `run_ml_predictions_all_sports_v2.py` - Enhanced script with TeamRankings (testing)
- `grade_yesterday_predictions.py` - Daily grading script
- `backup_predictions_daily.py` - Database backup

### Routes
- `routes/ui_endpoints.py` - Frontend API endpoints
- `routes/model_performance.py` - Model metrics API
- `routes/ui_props.py` - Player props API

### Data Sources
- `data/raw/nba/team_stats.csv` - NBA official API stats
- `data/raw/ncaab/kenpom_YYYYMMDD.csv` - KenPom ratings
- `data/raw/nfl/teamrankings_cache.json` - NFL team stats (32 teams, 100+ stats)
- `data/raw/ncaaf/teamrankings_cache.json` - NCAAF team stats (136 teams)
- `data/raw/nhl/moneypuck/` - NHL advanced stats

### Logs
- `logs/ml_predictions.log` - Daily prediction generation log
- `logs/grading_daily.log` - Results grading log
- `logs/cron_scraper.log` - Data scraping log

---

## Summary

### What's Working ✅
- NBA predictions (29/day, +4.77% avg edge)
- NCAAB predictions (47/day, +5.53% avg edge)
- Database storage (predictions.db)
- API endpoints (port 8000)
- Frontend display (historical predictions)
- Daily automation (cron jobs)

### What Needs Work ⚠️
- NFL predictions (feature mismatch causing constant 30.0)
- NCAAF predictions (feature mismatch causing 35-42 range)
- Team name matching (fuzzy logic has edge cases)

### What's Missing ❌
- NHL predictions (no stats source configured)
- Model retraining pipeline (weekly scheduled but needs testing)
- Confidence intervals (only point estimates)
- Live updates (predictions are static once generated)

---

**Generated**: December 1, 2025
**Author**: Claude Code
**Version**: 1.0
