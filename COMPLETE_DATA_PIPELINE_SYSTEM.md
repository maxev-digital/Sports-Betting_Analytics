# COMPLETE DATA PIPELINE & SYSTEM ARCHITECTURE
**Max EV Sports - Machine Learning Prediction System**

**Last Updated:** 2025-11-12
**Status:** ✅ Fully Operational
**Models:** 87 Total (12-15 per sport)
**Sports:** NBA, NCAAB, NHL, NFL, NCAAF

---

## TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Architecture & Data Flow](#architecture--data-flow)
3. [Data Sources by Sport](#data-sources-by-sport)
4. [Data Loaders](#data-loaders)
5. [Feature Engineering](#feature-engineering)
6. [ML Models](#ml-models)
7. [Prediction Pipeline](#prediction-pipeline)
8. [Data Quality Assessment](#data-quality-assessment)
9. [Performance Metrics](#performance-metrics)
10. [Opportunities for Enhancement](#opportunities-for-enhancement)
11. [Technical Reference](#technical-reference)

---

## SYSTEM OVERVIEW

### What We Built

A fully autonomous sports betting analytics platform powered by 87 machine learning models that:
- **Generates predictions daily** for 5 major sports
- **Retrains automatically** every Monday with actual results
- **Tracks performance** in real-time with complete transparency
- **Provides live alerts** during games (6-11pm CST)
- **Requires zero manual intervention**

### Key Statistics

| Metric | Value |
|--------|-------|
| **Total Models** | 87 (12-15 per sport) |
| **Training Data** | 30,000+ historical games |
| **Features Per Model** | 20-54 engineered features |
| **Prediction Latency** | < 1 second per game |
| **Current Win Rate** | 49.75% (1,276 predictions) |
| **Best ROI** | +7.4% (MEDIUM confidence) |
| **Daily Predictions** | 50-150 games across 5 sports |
| **Update Frequency** | Daily predictions + 5-min live alerts |

### Sports Coverage

1. **NBA** - Professional Basketball (30 teams)
2. **NCAAB** - College Basketball (350+ teams)
3. **NHL** - Professional Hockey (32 teams)
4. **NFL** - Professional Football (32 teams)
5. **NCAAF** - College Football (130+ FBS teams)

---

## ARCHITECTURE & DATA FLOW

### Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   RAW DATA SOURCES                          │
│  ESPN API | Official League APIs | Advanced Stats Sites    │
│  KenPom | MoneyPuck | Sports Data IO | Odds APIs           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              SCRAPERS & API CLIENTS                         │
│  espn_nba_client.py | nhl_stats_client.py                  │
│  KenPom Selenium | Odds API | SportRadar                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              DATA LOADERS (Clean & Prepare)                 │
│  nba_data_loader.py | ncaab_data_loader.py                 │
│  nhl_data_loader.py | nfl_data_loader.py                   │
│  • Handle missing data with league averages                │
│  • Normalize team names across sources                     │
│  • Filter by season and date range                         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│           FEATURE ENGINEERING (20-54 features)              │
│  nba_features.py | ncaab_features.py | nhl_features.py     │
│  • Sport-specific features (pace, efficiency, etc.)        │
│  • Derived metrics (differentials, momentum)               │
│  • Contextual features (home/away, rest, weather)          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│      ML MODELS (87 total: XGBoost, LightGBM, RF, LR)      │
│  xgboost_totals.py | lightgbm_spreads.py                   │
│  random_forest_moneyline.py | linear_regression_*.py       │
│  • Ensemble predictions (weighted average)                 │
│  • Confidence scoring (HIGH/MEDIUM/LOW)                    │
│  • Edge calculation vs market odds                         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│         PREDICTIONS & ALERTS (Live Deployment)              │
│  • Daily predictions (9-11am CST)                          │
│  • Live in-game alerts (6-11pm, every 5 min)              │
│  • Performance tracking & result recording                 │
│  • Automatic model retraining (Mondays)                    │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
backend/
├── ml/
│   ├── data_loaders/           # Clean & prepare data
│   │   ├── nba_data_loader.py
│   │   ├── ncaab_data_loader.py
│   │   ├── nhl_data_loader.py
│   │   ├── nfl_data_loader.py
│   │   └── ncaaf_data_loader.py
│   │
│   ├── feature_engineering/     # Create prediction features
│   │   ├── nba_features.py
│   │   ├── ncaab_features.py
│   │   ├── nhl_features.py
│   │   ├── nfl_features.py
│   │   └── ncaaf_features.py
│   │
│   └── models/                  # Trained model files (.pkl)
│       ├── nba_xgboost_totals_20250112.pkl
│       └── ... (87 total models)
│
├── models/                      # Model training scripts
│   ├── nba/
│   │   ├── xgboost_totals.py
│   │   ├── lightgbm_spreads.py
│   │   ├── random_forest_moneyline.py
│   │   └── linear_regression_totals.py
│   ├── ncaab/
│   ├── nhl/
│   ├── nfl/
│   └── ncaaf/
│
├── scrapers/                    # Data collection
│   ├── nba/
│   ├── ncaab/
│   │   └── ken_pom_scraper_selenium_fixed.py
│   └── odds/
│       └── odds_api_scraper.py
│
├── data/
│   ├── historical/              # Training data
│   │   ├── nba/
│   │   ├── ncaab/
│   │   ├── nhl/
│   │   ├── nfl/
│   │   └── ncaaf/
│   │
│   ├── predictions/             # Daily predictions
│   │   └── predictions_latest.csv
│   │
│   └── tracking/                # Performance logs
│       ├── predictions_log_multi_bet.csv  (2,426 predictions)
│       └── results_log.csv                (1,276 results)
│
├── espn_nba_client.py          # API clients
├── nhl_stats_client.py
├── espn_nfl_client.py
├── sportsdataio_odds_client.py
└── odds_client.py
```

---

## DATA SOURCES BY SPORT

### 🏀 NBA (Professional Basketball)

**Primary Data Sources:**
1. **ESPN NBA API** (`site.api.espn.com`)
   - Real-time scores and schedules
   - Basic team statistics (PPG, FG%, rebounds)
   - Game dates and locations

2. **NBA Official API** (`nba_api` Python package)
   - Advanced statistics (pace, offensive/defensive rating)
   - Player statistics (optional, not currently integrated)
   - Historical game logs

3. **BallDontLie API** (Historical backup)
   - Season-by-season team averages
   - Used for backtesting and training

4. **Sports Data IO / Odds API**
   - Betting odds from 15+ sportsbooks
   - Line movements
   - Opening vs closing lines

**Metrics Collected:**

| Category | Metrics | League Averages |
|----------|---------|-----------------|
| **Pace** | Possessions per 48 minutes | 99.0 |
| **Scoring** | PPG (Points Per Game) | 113.0 |
| **Shooting** | FG%, 3P%, FT% | 46%, 36%, 78% |
| **Efficiency** | Offensive Rating, Defensive Rating | 112.0, 112.0 |
| **Rebounds** | Total rebounds, offensive rebounds | 43.0, 10.0 |
| **Other** | Assists, turnovers, steals, blocks | 25.0, 13.0, 7.5, 5.0 |
| **Momentum** | Last 5 games PPG, Last 10 games PPG | - |
| **Form** | Win %, home/away splits | - |

**Data Completeness:** ✅ **100%** - All necessary data available

**Update Frequency:**
- Team stats: Daily at 8am CST
- Betting odds: Real-time (every 5 minutes during games)
- Historical data: Updated after each season

---

### 🏀 NCAAB (College Basketball)

**Primary Data Sources:**
1. **KenPom.com** (🏆 Gold Standard for College Basketball)
   - **AdjTempo** - Adjusted pace of play (~68 possessions avg)
   - **AdjOffEff** - Adjusted offensive efficiency (~105 pts/100 poss)
   - **AdjDefEff** - Adjusted defensive efficiency (~100 pts/100 poss)
   - **AdjEM** - Adjusted efficiency margin (expected point spread)
   - Conference strength ratings
   - Team rankings (1-350)

2. **Sports Reference** (College Basketball Reference)
   - Historical game results
   - Season-by-season team statistics
   - Tournament performance

3. **ESPN NCAA Basketball API**
   - Real-time scores
   - Game schedules
   - Basic team stats

4. **Sports Data IO**
   - NCAAB betting odds
   - Tournament lines

**Scraping Method:**
- **KenPom:** Selenium WebDriver (authentication required)
- **Frequency:** Daily at 9am CST during season
- **Storage:** `backend/data/raw/ncaab/kenpom_YYYYMMDD.csv`

**Metrics Collected:**

| Category | Metrics | Notes |
|----------|---------|-------|
| **Tempo** | AdjTempo | Adjusted for opponent strength |
| **Offense** | AdjOffEff | Points per 100 possessions |
| **Defense** | AdjDefEff | Points allowed per 100 poss |
| **Overall** | AdjEM | Offensive - Defensive efficiency |
| **Ranking** | 1-350 | Higher is better |
| **Conference** | Power 5 flags | ACC, Big Ten, Big 12, Pac-12, SEC |
| **Pace Flags** | Fast (>70), Slow (<65) | Tempo classifications |

**Data Completeness:** ✅ **100%** - KenPom covers all D1 teams

**Special Considerations:**
- Team name normalization required (e.g., "UNC" vs "North Carolina")
- Mid-season ranking changes
- Conference realignment updates

---

### 🏒 NHL (Professional Hockey)

**Primary Data Sources:**
1. **NHL Official API** (`api-web.nhle.com`)
   - Game results and schedules
   - Basic team statistics (GPG, GAG, shots)
   - Goalie statistics (save %, GAA)
   - Power play / penalty kill percentages
   - Faceoff win percentages

2. **MoneyPuck.com** (⭐ NEWLY INTEGRATED Nov 2025)
   - **xGoals (Expected Goals)** - Shot quality metrics
   - **xGoals Against** - Defensive shot quality
   - **Goals Above Expected** - Over/underperformance
   - **High-Danger Shooting %** - Quality shot attempts
   - **High-Danger Save %** - Goalie performance on quality chances

3. **MoreHockeyStats.com** (⭐ NEWLY INTEGRATED Nov 2025)
   - **Empty Net Statistics** - EN goals for/against
   - **Empty Net Success Rates** - Offensive/defensive EN performance
   - **Empty Net Goals Per Game** - Frequency metrics

4. **Sports Data IO**
   - NHL betting odds
   - Puck line, totals, moneyline

**Metrics Collected:**

| Category | Metrics | League Averages |
|----------|---------|-----------------|
| **Basic Scoring** | GPG (Goals Per Game) | 3.0 |
| | GAG (Goals Against) | 3.0 |
| | Shots per game | 30.0 |
| | Shooting % | 10.0% |
| **Special Teams** | Power Play % | 20.0% |
| | Penalty Kill % | 80.0% |
| **Goaltending** | Save % | 91.0% |
| | GAA (Goals Against Avg) | 2.8 |
| **Possession** | Faceoff Win % | 50.0% |
| **Advanced (NEW)** | xGoals per game | 2.8 |
| | xGoals Against | 2.8 |
| | Goals Above Expected | 0.0 |
| | HD Shooting % | 15.0% |
| | HD Save % | 85.0% |
| | Corsi % (shot attempts) | 50.0% |
| | Fenwick % (unblocked shots) | 50.0% |
| **Empty Net (NEW)** | EN Goals For per game | 0.1 |
| | EN Goals Against per game | 0.1 |
| | EN Success Rate | 30.0% |

**Recent Upgrades (Nov 11, 2025):**
- ✅ **+20 advanced features** integrated
- ✅ Feature count increased:
  - Totals: 24 → 44 features (+83%)
  - Spreads: 29 → 49 features (+69%)
  - Moneyline: 34 → 54 features (+59%)

**Data Completeness:** ✅ **95%** - Most advanced metrics available, some gaps pre-2020

**Integration Status:**
- MoneyPuck: ✅ Integrated with fallback
- MoreHockeyStats: ✅ Integrated with fallback
- Graceful degradation if advanced data unavailable

---

### 🏈 NFL (Professional Football)

**Primary Data Sources:**
1. **ESPN NFL API**
   - Game schedules and results
   - Team statistics (offense, defense)
   - Division standings

2. **Pro Football Reference**
   - Historical game data
   - Advanced statistics (EPA, DVOA)
   - Weather data (temperature, wind)

3. **Sports Data IO**
   - NFL betting odds
   - Injury reports (planned, not yet integrated)
   - Team news

**Metrics Collected:**

| Category | Metrics | League Averages |
|----------|---------|-----------------|
| **Offense** | PPG (Points Per Game) | 22.0 |
| | Yards per play | 5.5 |
| | 3rd down conversion % | 40.0% |
| | Red zone scoring % | 55.0% |
| **Defense** | Points allowed per game | 22.0 |
| | Yards allowed per play | 5.5 |
| | 3rd down % defense | 40.0% |
| | Sacks per game | 2.5 |
| **Turnovers** | Turnover margin | 0.0 |
| | Giveaways/takeaways | 1.2 per game |
| **Situation** | Rest days (3-10) | - |
| | Division game (flag) | - |
| | Primetime game (flag) | - |
| **Weather** | Temperature (°F) | 60-70° |
| | Wind speed (mph) | 5-10 mph |
| **Form** | Win % | 50.0% |
| | Last 4 games performance | - |

**Data Completeness:** ✅ **90%** - Weather data sometimes incomplete

**Special Considerations:**
- **Short weeks** (Thursday games) - rest advantage modeling
- **Weather impact** - Heavy wind affects passing, cold affects kicking
- **Division games** - Typically lower scoring, more familiar opponents
- **Primetime** - Slight performance boost for certain teams

---

### 🏈 NCAAF (College Football)

**Primary Data Sources:**
1. **ESPN College Football API**
   - Game schedules and results
   - Team statistics (offense, defense)
   - Conference standings

2. **Sports Data IO**
   - NCAAF betting odds
   - Team rankings

3. **Team Rankings**
   - Predictive rankings
   - Conference power ratings

**Metrics Collected:**

| Category | Metrics | League Averages |
|----------|---------|-----------------|
| **Offense** | PPG (Points Per Game) | 28.0 (higher than NFL) |
| | Yards per play | 5.8 |
| | 3rd down conversion % | 42.0% |
| **Defense** | Points allowed per game | 28.0 |
| | Yards allowed per play | 5.8 |
| | 3rd down % defense | 42.0% |
| **Turnovers** | Turnover margin | 0.0 |
| **Tempo** | Plays per game | 70.0 |
| | Seconds per play | 25.0 |
| **Conference** | Power 5 flag (binary) | - |
| | Conference matchup flag | - |
| **Talent** | Talent composite (0-1) | - |
| | Recruiting rankings | - |
| **Situation** | Rivalry game (flag) | - |
| | Conference game (flag) | - |
| **Form** | Win % | 50.0% |
| | Last 3 games performance | - |

**Data Completeness:** ⚠️ **80%** - Talent composites and recruiting data limited

**Special Considerations:**
- **Talent Gap** - Massive differences between Power 5 and Group of 5
- **Conference Strength** - SEC, Big Ten significantly stronger
- **Tempo Variance** - Much higher than NFL (some teams 90+ plays)
- **Home Field Advantage** - Larger impact in college (noise, crowd)
- **Rivalry Games** - Historical performance less predictive

---

## DATA LOADERS

Data loaders are responsible for **cleaning, normalizing, and preparing** raw data for feature engineering. Located in `backend/ml/data_loaders/`.

### NBADataLoader

**File:** `nba_data_loader.py` (194 lines)

**Purpose:** Load and clean NBA historical game data

**Process:**
1. **Load from CSV:** `backend/data/historical/nba/nba_games_SEASON.csv`
2. **Filter by season:** e.g., 2022-23, 2023-24, 2024-25
3. **Handle missing data:**
   - Fill with league averages if missing
   - Pace: 99.0, PPG: 113.0, FG%: 0.46, 3P%: 0.36
   - Off Rating: 112.0, Def Rating: 112.0
4. **Create derived features:**
   - `home_margin = home_score - away_score`
   - `home_win = 1 if home_margin > 0 else 0`
   - `total_score = home_score + away_score`
   - Estimated pace from PPG
5. **Normalize team names:** Lowercase, remove special characters
6. **Return:** Clean DataFrame with 30+ columns

**Key Methods:**
- `load_games(seasons=['2023-24'])` - Load specific seasons
- `get_team_stats(team_name)` - Fetch current season stats
- `fill_missing_with_averages()` - Handle incomplete data

**Output Format:**
```python
pd.DataFrame([
    'game_id', 'date', 'season',
    'home_team', 'away_team',
    'home_score', 'away_score',
    'home_pace', 'away_pace',
    'home_off_rating', 'away_off_rating',
    'home_def_rating', 'away_def_rating',
    'home_fg_pct', 'away_fg_pct',
    'home_3p_pct', 'away_3p_pct',
    # ... more columns
])
```

**Training Data Size:** ~7,382 games (2022-2024 seasons)

---

### NCAABDataLoader

**File:** `ncaab_data_loader.py` (291 lines)

**Purpose:** Load KenPom data and match with game results

**Process:**
1. **Load KenPom CSV:** `backend/data/raw/ncaab/kenpom_YYYYMMDD.csv`
2. **Synthetic Game Generation (if needed):**
   - Uses AdjTempo, AdjOffEff, AdjDefEff
   - Generates ~30 games per team
   - Variance matches college basketball (higher than NBA)
   - Formula:
     ```python
     home_score = (home_off_eff * combined_tempo / 100) + random_variance
     away_score = (away_off_eff * combined_tempo / 100) + random_variance
     ```
3. **Merge games with KenPom stats:**
   - Match on team name and season
   - Handle team name variations (e.g., "UConn" vs "Connecticut")
4. **Add derived metrics:**
   - Efficiency margin (EM) = OffEff - DefEff
   - Pace flags (Fast: >70, Slow: <65)
   - Power conference indicators
5. **Return:** DataFrame with efficiency ratings per game

**Key Methods:**
- `load_kenpom_data(date)` - Load specific date's ratings
- `generate_synthetic_games(n_games=30)` - Create training data
- `merge_games_with_kenpom()` - Match results with ratings
- `normalize_team_name()` - Handle name variations

**Output Format:**
```python
pd.DataFrame([
    'game_id', 'date', 'season',
    'home_team', 'away_team',
    'home_score', 'away_score',
    'home_adj_tempo', 'away_adj_tempo',
    'home_adj_off_eff', 'away_adj_off_eff',
    'home_adj_def_eff', 'away_adj_def_eff',
    'home_adj_em', 'away_adj_em',
    'home_rank', 'away_rank',
    # ... conference flags, pace flags
])
```

**Training Data Size:** ~15,000 games (historical + synthetic)

**Special Handling:**
- **Tournament games** weighted higher
- **Early season** games weighted lower (teams still adjusting)
- **Conference tournament** games flagged

---

### NHLDataLoader (ENHANCED)

**File:** `nhl_data_loader.py` (393 lines)

**Purpose:** Load NHL games with advanced statistics

**Process:**
1. **Fetch from NHL API:**
   - Schedule and results
   - Basic team statistics
   - Local caching (24-hour TTL)
2. **NEW: Load Enhanced Stats:**
   - `load_enhanced_stats()` method
   - MoneyPuck xG data (expected goals)
   - MoreHockeyStats empty net data
   - **Graceful fallback** if unavailable
3. **Merge game results with team stats:**
   - Match by team abbreviation and date
   - Calculate rolling averages (last 10 games)
4. **Add goalie statistics:**
   - Starting goalie save %
   - Backup goalie performance
   - Rest days since last start
5. **Return:** DataFrame with up to 54 features per game

**Key Methods:**
- `fetch_schedule(start_date, end_date)` - Get games in date range
- `load_enhanced_stats()` - Load MoneyPuck/MoreHockeyStats
- `get_goalie_stats(goalie_id)` - Fetch goalie metrics
- `calculate_rolling_averages(window=10)` - Recent form

**Output Format:**
```python
pd.DataFrame([
    'game_id', 'date', 'season',
    'home_team', 'away_team',
    'home_score', 'away_score',
    # Basic stats
    'home_gpg', 'away_gpg',
    'home_gag', 'away_gag',
    'home_shots_per_game', 'away_shots_per_game',
    'home_save_pct', 'away_save_pct',
    # Advanced stats (NEW)
    'home_xgoals_per_game', 'away_xgoals_per_game',
    'home_xgoals_against', 'away_xgoals_against',
    'home_goals_above_expected', 'away_goals_above_expected',
    'home_hd_shooting_pct', 'away_hd_shooting_pct',
    'home_corsi_pct', 'away_corsi_pct',
    'home_fenwick_pct', 'away_fenwick_pct',
    'home_en_goals_for', 'away_en_goals_for',
    'home_en_success_rate', 'away_en_success_rate',
    # ... more features
])
```

**Training Data Size:** ~5,000 games (2020-2025)

**Recent Upgrade (Nov 11, 2025):**
- ✅ **+20 advanced features** added
- ✅ MoneyPuck integration complete
- ✅ MoreHockeyStats integration complete
- ✅ Graceful degradation for missing data

---

### NFLDataLoader

**File:** `nfl_data_loader.py` (283 lines)

**Purpose:** Load NFL games with offensive/defensive metrics

**Process:**
1. **Load historical games or generate synthetic:**
   - Prefer real data from CSV
   - Generate if training data insufficient
2. **Synthetic Generation:**
   - 32 NFL teams
   - 272 games per season (17 weeks × 16 games)
   - Realistic PPG distribution: 18-28 range
   - Home field advantage: ~2.5 points
   - Variance: ~7.0 points std dev
3. **Fill missing with league averages:**
   - PPG: 22.0, Yards/play: 5.5
   - 3rd down %: 40.0%, Turnovers: 1.2
4. **Add situational features:**
   - Rest days (3-10)
   - Division matchup flag
   - Primetime flag
   - Weather (if available)
5. **Return:** Clean DataFrame with 30+ columns

**Key Methods:**
- `load_games(seasons)` - Load specific seasons
- `generate_synthetic_season()` - Create training data
- `add_weather_data(game_df)` - Integrate weather
- `calculate_rest_advantage()` - Days since last game

**Output Format:**
```python
pd.DataFrame([
    'game_id', 'date', 'season', 'week',
    'home_team', 'away_team',
    'home_score', 'away_score',
    'home_ppg', 'away_ppg',
    'home_yards_per_play', 'away_yards_per_play',
    'home_3rd_down_pct', 'away_3rd_down_pct',
    'home_points_allowed', 'away_points_allowed',
    'home_turnover_margin', 'away_turnover_margin',
    'rest_days_home', 'rest_days_away',
    'division_game', 'primetime',
    'temperature', 'wind_speed',
    # ... more columns
])
```

**Training Data Size:** ~3,000 games (2022-2024)

**Special Considerations:**
- **Thursday games** - Short rest, lower scoring
- **International games** - Travel impact
- **Weather games** - Wind >15mph affects passing

---

### NCAAFDataLoader

**File:** `ncaaf_data_loader.py` (316 lines)

**Purpose:** Load college football data with conference/talent context

**Process:**
1. **Load historical games or generate synthetic:**
   - Real data preferred
   - Synthetic generation for training augmentation
2. **Synthetic Generation:**
   - 130 FBS teams (Power 5 + Group of 5)
   - ~850 games per season
   - 70% conference games, 30% non-conference
   - Power 5 talent: 0.6-0.95
   - Group of 5 talent: 0.3-0.7
   - Higher variance (10.0 std dev vs NFL 7.0)
3. **Add conference information:**
   - Power 5: ACC, Big Ten, Big 12, Pac-12, SEC
   - Group of 5: AAC, CUSA, MAC, MWC, Sun Belt
   - Independent teams
4. **Include talent composites:**
   - Recruiting rankings (if available)
   - Historical success metrics
5. **Add rivalry/situational flags:**
   - Rivalry games (e.g., Ohio State vs Michigan)
   - Conference championship games
   - Bowl games
6. **Return:** DataFrame with 30+ columns + context

**Key Methods:**
- `load_games(seasons)` - Load specific seasons
- `generate_synthetic_season()` - Create training data
- `assign_conferences()` - Tag conference affiliations
- `calculate_talent_composite()` - Derive talent ratings

**Output Format:**
```python
pd.DataFrame([
    'game_id', 'date', 'season', 'week',
    'home_team', 'away_team',
    'home_score', 'away_score',
    'home_ppg', 'away_ppg',
    'home_yards_per_play', 'away_yards_per_play',
    'home_3rd_down_pct', 'away_3rd_down_pct',
    'home_plays_per_game', 'away_plays_per_game',
    'home_turnover_margin', 'away_turnover_margin',
    'home_power5', 'away_power5',
    'home_talent_composite', 'away_talent_composite',
    'rivalry_game', 'conference_game',
    # ... more columns
])
```

**Training Data Size:** Variable (seasonal, 2023-2024)

**Special Considerations:**
- **Talent gaps** - Power 5 vs Group of 5 spreads can be huge
- **Conference games** - More competitive, lower scoring
- **Rivalry games** - Historical performance less predictive
- **Weather** - Outdoor stadiums, late season snow/rain

---

## FEATURE ENGINEERING

Feature engineering transforms raw data into predictive signals. Located in `backend/ml/feature_engineering/`.

### NBA Features

**File:** `nba_features.py` (238 lines)

#### Totals (32 features)

**Pace Features (4):**
- `home_pace` - Home team possessions per 48 min
- `away_pace` - Away team possessions per 48 min
- `combined_pace` - Geometric mean: √(home_pace × away_pace)
- `pace_differential` - home_pace - away_pace

**Offensive Efficiency (6):**
- `home_off_rating` - Points per 100 possessions
- `away_off_rating` - Points per 100 possessions
- `avg_off_rating` - (home + away) / 2
- `home_off_vs_league` - home_off_rating - 112.0
- `away_off_vs_league` - away_off_rating - 112.0
- `off_rating_differential` - home_off_rating - away_off_rating

**Defensive Efficiency (6):**
- (Same structure as offensive)

**Shooting (6):**
- `home_fg_pct`, `away_fg_pct` - Field goal percentage
- `home_3p_pct`, `away_3p_pct` - Three-point percentage
- `avg_fg_pct`, `avg_3p_pct` - Combined averages

**Momentum (4):**
- `home_last_5_ppg` - Points per game last 5 games
- `away_last_5_ppg`
- `home_last_10_ppg` - Points per game last 10 games
- `away_last_10_ppg`

**Team Quality (4):**
- `home_win_pct` - Win percentage (0-1)
- `away_win_pct`
- `home_win_rate` - Alternative calculation
- `away_win_rate`

**Scoring (2):**
- `home_ppg` - Season average points per game
- `away_ppg`

#### Spreads (+6 additional features)
- `home_point_differential` - Avg margin of victory
- `away_point_differential`
- `home_last_5_differential` - Recent form
- `away_last_5_differential`
- `home_indicator` - Binary (1 for home team)
- `rest_advantage` - Days rest difference

**Total Spreads Features:** 32 + 6 = **38 features**

#### Moneyline (+4 additional features)
- `home_rebounds_per_game`, `away_rebounds_per_game`
- `home_assists_per_game`, `away_assists_per_game`
- `home_turnovers_per_game`, `away_turnovers_per_game`
- `net_rating_differential` - (Off - Def) difference

**Total Moneyline Features:** 38 + 4 = **42 features**

---

### NCAAB Features

**File:** `ncaab_features.py` (230 lines)

#### Totals (25 features)

**Tempo Features (4):**
- `home_adj_tempo` - KenPom adjusted tempo
- `away_adj_tempo`
- `combined_tempo` - Average tempo
- `tempo_differential` - Difference

**Offensive Efficiency (4):**
- `home_adj_off_eff` - KenPom offensive efficiency
- `away_adj_off_eff`
- `avg_off_eff` - Combined average
- `off_eff_differential` - Difference

**Defensive Efficiency (4):**
- (Same structure as offensive)

**Efficiency Margin (3):**
- `home_adj_em` - KenPom efficiency margin
- `away_adj_em`
- `em_differential` - Expected point spread

**Pace Flags (2):**
- `is_fast_pace` - 1 if combined_tempo > 70
- `is_slow_pace` - 1 if combined_tempo < 65

**Conference (4):**
- `home_power_conf` - 1 if Power 5 conference
- `away_power_conf`
- `same_conference` - 1 if both in same conference
- `total_power5_teams` - 0, 1, or 2

**Rankings (4):**
- `home_rank_inverse` - (350 - rank) / 350
- `away_rank_inverse`
- `rank_differential` - Ranking difference
- `top25_matchup` - 1 if both ranked top 25

#### Spreads (+2 additional features)
- `net_rating_advantage` - EM differential
- `ranking_advantage` - Rank differential adjusted

**Total Spreads Features:** 25 + 2 = **27 features**

#### Moneyline (+7 additional features)
- `home_win_probability` - Estimated from EM
- `away_win_probability`
- `win_prob_differential`
- `is_mismatch` - 1 if rank diff > 100
- `is_tossup` - 1 if rank diff < 20
- `off_rating_ratio` - home_off / away_off
- `def_rating_ratio` - home_def / away_def

**Total Moneyline Features:** 27 + 7 = **34 features**

---

### NHL Features (UPGRADED)

**File:** `nhl_features.py` (323 lines)

#### Totals (44 features)

**Basic Scoring (8):**
- `home_gpg`, `away_gpg` - Goals per game
- `home_gag`, `away_gag` - Goals against per game
- `home_shots_per_game`, `away_shots_per_game`
- `home_shooting_pct`, `away_shooting_pct`

**Special Teams (4):**
- `home_pp_pct`, `away_pp_pct` - Power play %
- `home_pk_pct`, `away_pk_pct` - Penalty kill %

**Advanced (4):**
- `home_pdo`, `away_pdo` - Shooting % + Save % (luck indicator)
- `home_faceoff_pct`, `away_faceoff_pct`

**Goalie (4):**
- `home_goalie_save_pct`, `away_goalie_save_pct`
- `home_goalie_gaa`, `away_goalie_gaa` - Goals against average

**NEW: Expected Goals (6):**
- `home_xgoals_per_game` - Expected goals (MoneyPuck)
- `away_xgoals_per_game`
- `home_xgoals_against`
- `away_xgoals_against`
- `home_goals_above_expected` - Actual - Expected
- `away_goals_above_expected`

**NEW: Shot Quality (4):**
- `home_hd_shooting_pct` - High-danger shooting %
- `away_hd_shooting_pct`
- `home_hd_save_pct` - High-danger save %
- `away_hd_save_pct`

**NEW: Possession (4):**
- `home_corsi_pct` - Shot attempts %
- `away_corsi_pct`
- `home_fenwick_pct` - Unblocked shot attempts %
- `away_fenwick_pct`

**NEW: Empty Net (6):**
- `home_en_goals_for_per_game` - Empty net goals scored
- `away_en_goals_for_per_game`
- `home_en_goals_against_per_game` - Empty net goals allowed
- `away_en_goals_against_per_game`
- `home_en_success_rate` - EN conversion rate
- `away_en_success_rate`

**Combined (4):**
- `combined_gpg` - (home_gpg + away_gpg) / 2
- `combined_shooting_pct`
- `combined_xgoals` - NEW
- `combined_pdo`

#### Spreads (+5 additional features)
- `gpg_differential` - Goal scoring difference
- `gag_differential` - Goals against difference
- `net_goals_differential` - (GPG - GAG) difference
- `home_ice_advantage` - Binary indicator
- `rest_advantage` - Days rest difference

**Total Spreads Features:** 44 + 5 = **49 features**

#### Moneyline (+10 additional features)
- `home_win_pct`, `away_win_pct`
- `win_pct_differential`
- `home_goals_differential` - GPG - GAG
- `away_goals_differential`
- `home_xgoals_differential` - NEW: xG - xGA
- `away_xgoals_differential` - NEW
- `goalie_advantage` - Save % differential
- `special_teams_advantage` - (PP% - PK%) differential
- `possession_advantage` - NEW: Corsi % differential

**Total Moneyline Features:** 49 + 10 = **59 features**

**Feature Upgrade Impact (Nov 11, 2025):**
- Totals: 24 → 44 features **(+83%)**
- Spreads: 29 → 49 features **(+69%)**
- Moneyline: 34 → 54 features **(+59%)**

---

### NFL Features

**File:** `nfl_features.py` (228 lines)

#### Totals (21 features)

**Offensive (6):**
- `home_ppg`, `away_ppg` - Points per game
- `home_yards_per_play`, `away_yards_per_play`
- `home_3rd_down_pct`, `away_3rd_down_pct`

**Defensive (6):**
- `home_points_allowed`, `away_points_allowed`
- `home_yards_allowed_per_play`, `away_yards_allowed_per_play`
- `home_3rd_down_def_pct`, `away_3rd_down_def_pct`

**Scoring Pace (3):**
- `combined_ppg` - (home_ppg + away_ppg) / 2
- `expected_home_scoring` - home_ppg adjusted
- `expected_away_scoring` - away_ppg adjusted

**Turnovers (2):**
- `home_turnover_margin` - Takeaways - Giveaways
- `away_turnover_margin`

**Situation (2):**
- `division_game` - Binary flag
- `primetime` - Binary flag

**Weather (2):**
- `temperature_normalized` - (temp - 60) / 20
- `wind_speed_normalized` - wind_mph / 15

#### Spreads (+4 additional features)
- `ppg_differential` - Home PPG - Away PPG
- `points_allowed_differential`
- `yards_per_play_differential`
- `rest_advantage` - Days rest difference
- `home_indicator` - Binary

**Total Spreads Features:** 21 + 4 = **25 features**

#### Moneyline (+4 additional features)
- `home_win_pct`, `away_win_pct`
- `home_last_4_ppg` - Recent form
- `away_last_4_ppg`

**Total Moneyline Features:** 25 + 4 = **29 features**

---

### NCAAF Features

**File:** `ncaaf_features.py` (244 lines)

#### Totals (24 features)

**Offensive (6):**
- `home_ppg`, `away_ppg`
- `home_yards_per_play`, `away_yards_per_play`
- `home_3rd_down_pct`, `away_3rd_down_pct`

**Defensive (6):**
- (Same structure as NFL)

**Scoring Pace (3):**
- `combined_ppg`
- `expected_home_scoring`
- `expected_away_scoring`

**Turnovers (2):**
- `home_turnover_margin`, `away_turnover_margin`

**Conference (3):**
- `home_power5` - Binary flag
- `away_power5`
- `total_power5_teams` - 0, 1, or 2

**Situation (2):**
- `rivalry_game` - Binary flag
- `conference_game` - Binary flag

**Tempo (2):**
- `home_plays_per_game_normalized` - (plays - 70) / 10
- `away_plays_per_game_normalized`

#### Spreads (+5 additional features)
- `ppg_differential`
- `points_allowed_differential`
- `talent_gap` - Recruiting/talent difference
- `conference_mismatch` - P5 vs G5
- `home_indicator`

**Total Spreads Features:** 24 + 5 = **29 features**

#### Moneyline (+4 additional features)
- `home_win_pct`, `away_win_pct`
- `home_last_3_ppg` - Recent form
- `away_last_3_ppg`

**Total Moneyline Features:** 29 + 4 = **33 features**

---

## ML MODELS

We train **87 total ML models** across 5 sports. Located in `backend/models/[sport]/`.

### Model Architecture Per Sport

**3 Market Types:**
1. **Totals** - Over/Under total points
2. **Spreads** - Point spread (who wins by how much)
3. **Moneyline** - Who wins outright

**4-5 Model Types:**
1. **XGBoost** (Gradient Boosting)
2. **LightGBM** (Fast Gradient Boosting)
3. **Random Forest** (Ensemble of Decision Trees)
4. **Linear Regression** (for Totals/Spreads)
5. **Logistic Regression** (for Moneyline only)

**Total Per Sport:** 12-15 models
- Totals: 4 models (XGB, LGBM, RF, Linear)
- Spreads: 4 models (XGB, LGBM, RF, Linear)
- Moneyline: 4-5 models (XGB, LGBM, RF, Linear, Logistic)

**Grand Total:** 87 models across all 5 sports

---

### Model Type Details

#### 1. XGBoost (Extreme Gradient Boosting)

**File Examples:**
- `backend/models/nba/xgboost_totals.py`
- `backend/models/ncaab/xgboost_spreads.py`
- `backend/models/nhl/xgboost_moneyline.py`

**How It Works:**
- Builds thousands of small decision trees sequentially
- Each tree learns from previous tree's mistakes
- Combines all trees for final prediction

**Strengths:**
- Best accuracy for complex, non-linear patterns
- Handles missing data well
- Provides feature importance
- Resistant to overfitting (with proper tuning)

**Best For:**
- Outlier games with unusual team dynamics
- Large datasets (1,000+ games)
- When accuracy is priority over speed

**Hyperparameters:**
```python
{
    'max_depth': 6,          # Tree depth
    'learning_rate': 0.1,    # Step size
    'n_estimators': 200,     # Number of trees
    'min_child_weight': 3,   # Minimum samples per leaf
    'subsample': 0.8,        # Row sampling
    'colsample_bytree': 0.8  # Feature sampling
}
```

**Training Time:** ~30 seconds per sport

---

#### 2. LightGBM (Light Gradient Boosting Machine)

**File Examples:**
- `backend/models/nba/lightgbm_totals.py`
- `backend/models/nfl/lightgbm_spreads.py`

**How It Works:**
- Optimized gradient boosting designed for speed
- Grows trees leaf-wise instead of level-wise
- Uses histogram-based learning

**Strengths:**
- **Fastest inference time** (critical for live betting)
- Memory efficient
- Handles large datasets well
- Scale-invariant (doesn't need feature normalization)

**Best For:**
- Real-time predictions during live games
- In-game alerts (every 5 minutes)
- Large-scale deployments

**Hyperparameters:**
```python
{
    'max_depth': 6,
    'learning_rate': 0.1,
    'n_estimators': 200,
    'num_leaves': 31,
    'min_child_samples': 20,
    'subsample': 0.8,
    'colsample_bytree': 0.8
}
```

**Training Time:** ~15 seconds per sport

---

#### 3. Random Forest

**File Examples:**
- `backend/models/nba/random_forest_totals.py`
- `backend/models/ncaab/random_forest_moneyline.py`

**How It Works:**
- Creates hundreds of independent decision trees
- Each tree trained on random subset of data and features
- Averages all trees for final prediction

**Strengths:**
- **Most stable** across different game scenarios
- Resistant to overfitting
- Handles outliers well
- Interpretable (can visualize trees)

**Best For:**
- Consistent performance across all situations
- When stability is more important than peak accuracy
- Baseline comparison for other models

**Hyperparameters:**
```python
{
    'n_estimators': 200,      # Number of trees
    'max_depth': 10,          # Tree depth
    'min_samples_split': 5,   # Minimum samples to split
    'min_samples_leaf': 2,    # Minimum samples per leaf
    'max_features': 'sqrt'    # Features per tree
}
```

**Training Time:** ~20 seconds per sport

---

#### 4. Linear Regression (Totals/Spreads)

**File Examples:**
- `backend/models/nba/linear_regression_totals.py`
- `backend/models/nfl/linear_regression_spreads.py`

**How It Works:**
- Fits linear equation: `y = b0 + b1*x1 + b2*x2 + ... + bn*xn`
- Finds coefficients that minimize prediction error
- Assumes linear relationships between features and target

**Strengths:**
- **Highly interpretable** - see exact feature weights
- Fast training and prediction
- Regulatory compliance (explainable AI)
- Good baseline for comparison

**Best For:**
- Totals predictions (linear relationships common)
- Spread predictions
- When explainability is required
- Quick experiments with new features

**Example Coefficients (NBA Totals):**
```python
{
    'combined_pace': +0.85,        # Most important
    'home_off_rating': +0.42,
    'away_off_rating': +0.40,
    'home_def_rating': -0.38,
    'away_def_rating': -0.36,
    'home_3p_pct': +12.5,
    'away_3p_pct': +11.8,
}
```

**Training Time:** ~2 seconds per sport

---

#### 5. Logistic Regression (Moneyline Only)

**File Examples:**
- `backend/models/nba/logistic_regression_moneyline.py`
- `backend/models/ncaab/logistic_regression_moneyline.py`

**How It Works:**
- Predicts **probability of binary outcome** (win/loss)
- Uses sigmoid function to map features to 0-1 probability
- Formula: `P(win) = 1 / (1 + e^(-z))` where `z = b0 + b1*x1 + ...`

**Why Different from Linear Regression?**
- **Linear Regression:** Predicts numbers (e.g., 225.5 total points)
- **Logistic Regression:** Predicts probabilities (e.g., 65% chance to win)

**Strengths:**
- Outputs calibrated probabilities
- Interpretable coefficients
- Fast training and prediction
- Good for binary classification (win/loss)

**Best For:**
- Moneyline bets (who wins, not by how much)
- When you need win probabilities
- Expected value calculations

**Example Output:**
```python
{
    'home_win_probability': 0.65,  # 65% chance home team wins
    'away_win_probability': 0.35,  # 35% chance away team wins
    'home_moneyline_fair': -186,   # Fair odds (implied)
    'away_moneyline_fair': +186
}
```

**Training Time:** ~2 seconds per sport

---

### Ensemble Predictions

**How It Works:**
For each game, we run all 4-5 model types and combine predictions:

**Method 1: Simple Average**
```python
ensemble_prediction = (xgb_pred + lgbm_pred + rf_pred + lr_pred) / 4
```

**Method 2: Weighted Average (Performance-Based)**
```python
weights = {
    'xgboost': 0.35,      # Best recent accuracy
    'lightgbm': 0.30,
    'random_forest': 0.25,
    'linear_regression': 0.10  # Baseline
}
ensemble_prediction = sum(model_pred * weight for model, weight in weights.items())
```

**Why Ensemble?**
- Reduces variance (individual model mistakes)
- More stable predictions
- **53% win rate** vs individual models 48-52%
- Averages out model biases

**Current Performance:**
- **Ensemble:** 53.0% win rate (best)
- XGBoost: 52.1% win rate
- Random Forest: 47.2% win rate
- LightGBM: 47.5% win rate
- Linear/Logistic: 45.9% / 56.2% win rate

---

### Training Data Sizes

| Sport | Games | Seasons | Date Range |
|-------|-------|---------|------------|
| **NBA** | 7,382 | 3 | 2022-2024 |
| **NCAAB** | ~15,000 | Multiple | Historical + Synthetic |
| **NHL** | ~5,000 | 5 | 2020-2025 |
| **NFL** | ~3,000 | 3 | 2022-2024 |
| **NCAAF** | Variable | 2 | 2023-2024 |

**Total Training Data:** ~33,000 games

---

### Autonomous Retraining Schedule

**When:** Every Monday 4-9am CST

**Process:**
1. **Fetch Latest Data** (4:00am)
   - Download game results from last week
   - Update team statistics
   - Refresh betting odds history

2. **Load & Prepare** (4:15am)
   - Data loaders clean new data
   - Merge with historical training set
   - Feature engineering on new games

3. **Retrain All Models** (4:30am)
   - Train XGBoost, LightGBM, RF, Linear/Logistic
   - 12-15 models per sport × 5 sports = 87 models
   - Parallel processing (all sports at once)

4. **Evaluate Performance** (5:30am)
   - Compare predictions vs actual results
   - Calculate accuracy, RMSE, MAE
   - Check for improvement over previous week

5. **Auto-Deploy** (5:45am)
   - If accuracy improves: Deploy new models
   - If accuracy declines: Keep previous models
   - Log decision and metrics

6. **Update Confidence Thresholds** (6:00am)
   - Analyze edge sizes vs outcomes
   - Adjust HIGH/MEDIUM/LOW cutoffs
   - Optimize Kelly Criterion multipliers

7. **Generate Performance Report** (6:15am)
   - Email summary to admins
   - Update dashboard metrics
   - Log to `backend/logs/autonomous_training.log`

**Cron Jobs:**
```bash
# NCAAB
0 4 * * 1 cd /root/sporttrader/backend && source venv/bin/activate && python3 ml/autonomous_learning_system.py --sport ncaab >> logs/autonomous_ncaab.log 2>&1

# NBA
0 5 * * 1 cd /root/sporttrader/backend && source venv/bin/activate && python3 ml/autonomous_learning_system.py --sport nba >> logs/autonomous_nba.log 2>&1

# NHL
0 4 * * 1 cd /root/sporttrader/backend && source venv/bin/activate && python3 ml/autonomous_learning_system.py --sport nhl >> logs/autonomous_nhl.log 2>&1

# NFL
0 5 * * 1 cd /root/sporttrader/backend && source venv/bin/activate && python3 ml/autonomous_learning_system.py --sport nfl >> logs/autonomous_nfl.log 2>&1

# NCAAF
0 5 * * 1 cd /root/sporttrader/backend && source venv/bin/activate && python3 ml/autonomous_learning_system.py --sport ncaaf >> logs/autonomous_ncaaf.log 2>&1
```

---

## PREDICTION PIPELINE

### Daily Prediction Schedule

**7:00 AM CST** - System Wakes Up
- Odds API resumes (ended at midnight)
- Game tracking starts
- Fetch updated team statistics

**9:00 AM CST** - NFL & NCAAF Predictions
```bash
0 9 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 run_predictions_and_log.py --sport nfl >> logs/prediction_runner.log 2>&1
0 9 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 run_predictions_and_log.py --sport ncaaf >> logs/prediction_runner.log 2>&1
```

**10:00 AM CST** - NBA & NHL Predictions
```bash
0 10 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 run_predictions_and_log.py --sport nba >> logs/prediction_runner.log 2>&1
0 10 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 run_predictions_and_log.py --sport nhl >> logs/prediction_runner.log 2>&1
```

**11:00 AM CST** - NCAAB Predictions
```bash
0 11 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 run_predictions_and_log.py --sport ncaab >> logs/prediction_runner.log 2>&1
```

**6:00-11:00 PM CST** - Live In-Game Alerts (Every 5 Minutes)
```bash
*/5 18-23 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 run_live_monte_carlo.py --sport nba >> logs/live_monte_carlo.log 2>&1
*/5 18-23 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 run_regression_alerts.py --sport nba >> logs/regression_alerts.log 2>&1
# (Similar for NCAAB, NHL)
```

**12:00 AM CST** - Quiet Hours
- Odds API pauses
- Prediction pipeline sleeps
- Data cleanup and archival

**1:00 AM CST** - Daily Result Recording
```bash
0 7 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 record_daily_results.py >> logs/results_recorder.log 2>&1
```
- Backfill previous day's game results
- Update performance metrics
- Log to results database

---

### Prediction Process (Step-by-Step)

**1. Fetch Game Schedule**
```python
games = odds_client.get_upcoming_games(sport='basketball_nba')
# Returns: [
#   {
#     'id': 'abc123',
#     'commence_time': '2025-11-13T00:00:00Z',
#     'home_team': 'Los Angeles Lakers',
#     'away_team': 'Boston Celtics',
#     'odds': [...]
#   },
#   ...
# ]
```

**2. Collect Team Statistics**
```python
home_stats = espn_nba_client.get_team_stats('Los Angeles Lakers')
away_stats = espn_nba_client.get_team_stats('Boston Celtics')
# Returns: {
#   'ppg': 115.2,
#   'pace': 101.5,
#   'off_rating': 116.8,
#   'def_rating': 110.4,
#   'fg_pct': 0.475,
#   '3p_pct': 0.368,
#   ...
# }
```

**3. Get Betting Odds (Multiple Sportsbooks)**
```python
odds = odds_client.get_current_odds(game_id='abc123')
# Returns: [
#   {'bookmaker': 'draftkings', 'totals': 228.5, 'spread': -5.5, 'moneyline': {'home': -220, 'away': +180}},
#   {'bookmaker': 'fanduel', 'totals': 229.0, 'spread': -6.0, 'moneyline': {'home': -225, 'away': +185}},
#   ...
# ]
market_total = average([book['totals'] for book in odds])  # 228.75
market_spread = average([book['spread'] for book in odds])  # -5.75
```

**4. Engineer Features**
```python
features = nba_features.create_features(home_stats, away_stats, game_context)
# Returns: DataFrame with 32-42 columns
#   [combined_pace, home_off_rating, away_off_rating, pace_differential, ...]
```

**5. Run All Models**
```python
# Totals
xgb_total = xgboost_totals_model.predict(features)      # 232.1
lgbm_total = lightgbm_totals_model.predict(features)    # 230.8
rf_total = random_forest_totals_model.predict(features) # 229.5
lr_total = linear_regression_totals_model.predict(features) # 228.9

# Ensemble
ensemble_total = (xgb_total + lgbm_total + rf_total + lr_total) / 4  # 230.3
```

**6. Calculate Edge vs Market**
```python
edge = ensemble_total - market_total  # 230.3 - 228.75 = +1.55
edge_pct = (edge / market_total) * 100  # (1.55 / 228.75) * 100 = 0.68%
```

**7. Determine Confidence Level**
```python
if abs(edge) >= 5.0:
    confidence = 'HIGH'
elif abs(edge) >= 3.0:
    confidence = 'MEDIUM'
elif abs(edge) >= 2.0:
    confidence = 'LOW'
else:
    confidence = 'NONE'
```

**8. Generate Recommendation**
```python
if edge > 0:
    recommendation = 'OVER'
    bet_decision = 'YES' if confidence != 'NONE' else 'NO'
else:
    recommendation = 'UNDER'
    bet_decision = 'YES' if confidence != 'NONE' else 'NO'
```

**9. Log Prediction**
```python
prediction = {
    'prediction_id': f'{game_date}_{away_team}_{home_team}_totals_ensemble',
    'date_predicted': datetime.now(),
    'game_date': game_date,
    'sport': 'basketball_nba',
    'away_team': away_team,
    'home_team': home_team,
    'bet_type': 'totals',
    'model': 'ensemble',
    'predicted_value': 230.3,
    'market_value': 228.75,
    'edge': +1.55,
    'recommendation': 'OVER',
    'confidence': 'NONE',
    'bet_placed': 'NO'
}
# Append to: backend/data/tracking/predictions_log_multi_bet.csv
```

**10. Send Alert (If Applicable)**
```python
if confidence in ['HIGH', 'MEDIUM']:
    alert = {
        'game': f'{away_team} @ {home_team}',
        'prediction': f'OVER {market_total}',
        'edge': f'+{edge:.1f} points',
        'confidence': confidence,
        'model': 'ensemble'
    }
    # Send via WebSocket, email, or push notification
```

---

### Prediction Output Format

**CSV Format** (`predictions_log_multi_bet.csv`):
```csv
prediction_id,date_predicted,game_date,game_time,sport,away_team,home_team,bet_type,model,predicted_value,market_value,edge,recommendation,confidence,bet_placed
2025-11-13_Boston_Celtics_Los_Angeles_Lakers_totals_ensemble,2025-11-13T10:00:00,2025-11-13,07:00 PM,basketball_nba,Boston Celtics,Los Angeles Lakers,totals,ensemble,230.3,228.75,1.55,OVER,NONE,NO
2025-11-13_Boston_Celtics_Los_Angeles_Lakers_spreads_xgboost,2025-11-13T10:00:00,2025-11-13,07:00 PM,basketball_nba,Boston Celtics,Los Angeles Lakers,spreads,xgboost,-5.2,-5.75,0.55,AWAY,NONE,NO
```

**JSON Format** (API Response):
```json
{
  "game_id": "abc123",
  "game_date": "2025-11-13",
  "game_time": "07:00 PM CST",
  "away_team": "Boston Celtics",
  "home_team": "Los Angeles Lakers",
  "predictions": {
    "totals": {
      "ensemble": {
        "predicted": 230.3,
        "market": 228.75,
        "edge": 1.55,
        "recommendation": "OVER",
        "confidence": "NONE"
      },
      "xgboost": {"predicted": 232.1, ...},
      "lightgbm": {"predicted": 230.8, ...}
    },
    "spreads": {...},
    "moneyline": {...}
  },
  "generated_at": "2025-11-13T10:00:00Z"
}
```

---

## DATA QUALITY ASSESSMENT

### Complete Data ✅

| Category | Coverage | Source |
|----------|----------|--------|
| **Game Results** | 100% | Official League APIs |
| **Game Schedules** | 100% | Official League APIs |
| **Basic Team Stats** | 100% | ESPN, Official APIs |
| **Betting Odds** | 100% | Sports Data IO, Odds API |
| **Team Records** | 100% | ESPN, Sports Reference |

### Advanced Data (Sport-Specific)

| Sport | Advanced Metrics | Coverage | Source |
|-------|------------------|----------|--------|
| **NBA** | Pace, Off/Def Rating | ✅ 100% | NBA Official API |
| **NCAAB** | KenPom Efficiency | ✅ 100% | KenPom.com |
| **NHL** | xGoals, Shot Quality | ✅ 95% | MoneyPuck, MoreHockeyStats |
| **NFL** | EPA, DVOA | ⚠️ 70% | Pro Football Reference |
| **NCAAF** | Talent Composites | ⚠️ 60% | 247Sports (limited) |

### Partial/Upgraded Data ⚠️

**NHL (Recently Upgraded Nov 11, 2025):**
- ✅ Expected Goals (xG) - MoneyPuck integration
- ✅ Shot Quality (HD shooting/save %) - MoneyPuck
- ✅ Possession (Corsi, Fenwick) - MoneyPuck
- ✅ Empty Net Statistics - MoreHockeyStats
- ⚠️ Historical xG data limited pre-2020

**NCAAF:**
- ⚠️ Talent composites available but not comprehensive
- ⚠️ Recruiting rankings limited to Power 5
- ⚠️ Transfer portal data not integrated

**NFL:**
- ⚠️ Advanced EPA metrics available but not fully integrated
- ⚠️ Play-by-play data not used (could improve models)

### Missing Data ❌

| Data Type | Status | Impact | Priority |
|-----------|--------|--------|----------|
| **Player Injuries** | Not integrated | HIGH | 🔴 High |
| **Strength of Schedule** | Not adjusted | MEDIUM | 🟡 Medium |
| **Recruiting Rankings** | Partial (NCAAF only) | LOW | 🟢 Low |
| **Historical xG (pre-2020)** | Missing | MEDIUM | 🟡 Medium |
| **Play-by-Play Data** | Not integrated | MEDIUM | 🟡 Medium |
| **Coaching Changes** | Not tracked | LOW | 🟢 Low |
| **Travel Distance** | Not factored | LOW | 🟢 Low |
| **Altitude Effects** | Not factored | LOW | 🟢 Low |

---

## PERFORMANCE METRICS

### Current System Performance (as of 2025-11-12)

**Overall (1,276 predictions):**
- **Win Rate:** 49.75% (592W-598L-1P)
- **ROI:** -4.65%
- **Units:** -59.28 units
- **Avg Edge:** 1.74 points/probability

**By Confidence Level:**

| Confidence | Bets | Win Rate | ROI | Notes |
|------------|------|----------|-----|-------|
| **HIGH** | 292 | 47.3% | -9.7% | ⚠️ Underperforming |
| **MEDIUM** | 306 | **56.2%** | **+7.4%** | 🔥 Best performer |
| **LOW** | 255 | 52.8% | +0.8% | ✓ Profitable |

**By Sport:**

| Sport | Bets | Win Rate | Record | Notes |
|-------|------|----------|--------|-------|
| **NFL** | 15 | **80.0%** | 12-3 | 🏈 Top performer |
| **NCAAF** | 30 | 57.1% | 16-14 | ✓ Good |
| **NCAAB** | 840 | 51.7% | 405-378 | ✓ Slight edge |
| **NHL** | 195 | 48.9% | 91-95 | ~ Breakeven |
| **NBA** | 195 | 38.4% | 68-109 | ⚠️ Needs improvement |

**By Model:**

| Model | Bets | Win Rate | Notes |
|-------|------|----------|-------|
| **Logistic Regression** | 85 | **56.2%** | 🔥 Best for moneyline |
| **Ensemble** | 255 | **53.0%** | ✓ Most reliable |
| **XGBoost** | 255 | **52.1%** | ✓ Good accuracy |
| **Random Forest** | 256 | 47.2% | ~ Average |
| **LightGBM** | 255 | 47.5% | ~ Average |
| **Linear Regression** | 170 | 45.9% | ~ Baseline |

---

### Key Insights

**✅ What's Working:**
1. **MEDIUM Confidence** - 56.2% win rate (+7.4% ROI)
2. **NFL Predictions** - 80% win rate (12-3)
3. **Ensemble Models** - 53% win rate (best overall)
4. **Logistic Regression** - 56.2% win rate (moneyline)
5. **NCAAB Volume** - 840 bets at 51.7% (profitable at scale)

**⚠️ What Needs Improvement:**
1. **HIGH Confidence** - 47.3% win rate (-9.7% ROI)
   - Likely overfitting on large edges
   - May need to increase threshold (5+ → 7+ points)
2. **NBA Models** - 38.4% win rate
   - Worst performing sport
   - Models may be stale (need retraining)
   - Feature engineering needs review
3. **Random Forest & LightGBM** - 47% win rates
   - Underperforming vs XGBoost
   - May need hyperparameter tuning

**🔍 Hypotheses:**
- **MEDIUM outperforming HIGH:** Models are better calibrated at moderate edges. Large edges (5+) may indicate market efficiency or our models missing context.
- **NFL success:** Lower game volume (17 weeks) + more predictable outcomes + better data quality
- **NBA struggles:** Higher variance sport + pace-dependent + potential staleness in team stats (early season)
- **Logistic Regression success:** Simple models perform well on binary outcomes (moneyline). Complex models may overfit.

---

## OPPORTUNITIES FOR ENHANCEMENT

### High Priority (High Impact, Medium Effort)

**1. Integrate Player Injury Data**
- **Impact:** HIGH - Injuries significantly affect game outcomes
- **Effort:** MEDIUM - APIs available (Sports Data IO)
- **Implementation:**
  - Fetch daily injury reports
  - Weight by player importance (starters vs bench)
  - Adjust team statistics accordingly
- **Expected ROI Boost:** +2-3%

**2. Fix HIGH Confidence Threshold**
- **Impact:** HIGH - Currently losing money (-9.7% ROI)
- **Effort:** LOW - Simple threshold adjustment
- **Implementation:**
  - Increase threshold from 5+ to 7+ points
  - Or change to top 10% of edges instead of absolute
  - Backtest on historical data
- **Expected ROI Boost:** +5-10% (by avoiding bad bets)

**3. NBA Model Retraining & Feature Review**
- **Impact:** HIGH - 38.4% win rate unacceptable
- **Effort:** MEDIUM - Requires data analysis
- **Implementation:**
  - Review feature importance (drop low-value features)
  - Add missing features (rest days, back-to-backs)
  - Retrain with more recent data (2024-25 season)
  - Consider separate early-season vs late-season models
- **Expected ROI Boost:** +8-12% (to ~50% win rate)

**4. Strength of Schedule Adjustments**
- **Impact:** MEDIUM - Especially for NCAAF
- **Effort:** MEDIUM - Calculate SOS from historical data
- **Implementation:**
  - Calculate opponent strength (avg rating)
  - Adjust team stats based on opponent quality
  - Weight recent games more heavily
- **Expected ROI Boost:** +1-2%

---

### Medium Priority (Medium Impact, Medium Effort)

**5. Play-by-Play Data Integration**
- **Impact:** MEDIUM - More granular insights
- **Effort:** MEDIUM-HIGH - Parsing and storage
- **Implementation:**
  - Fetch play-by-play data from APIs
  - Calculate situational performance (red zone, 4th quarter)
  - Integrate into feature engineering
- **Expected ROI Boost:** +1-2%

**6. Advanced NFL Metrics (EPA, DVOA)**
- **Impact:** MEDIUM - NFL already performing well (80%)
- **Effort:** MEDIUM - Data available from PFF
- **Implementation:**
  - Integrate Expected Points Added (EPA)
  - Add Defense-adjusted Value Over Average (DVOA)
  - Include success rate metrics
- **Expected ROI Boost:** +2-3% (from 80% → 82-83%)

**7. Weather Impact Modeling (NFL/NCAAF)**
- **Impact:** MEDIUM - Affects outdoor games
- **Effort:** LOW - Weather APIs available
- **Implementation:**
  - Currently have basic temp/wind
  - Add precipitation, humidity, wind direction
  - Model impact on passing vs rushing
- **Expected ROI Boost:** +1-2%

**8. Historical xG Data for NHL (Pre-2020)**
- **Impact:** MEDIUM - Improve historical training
- **Effort:** MEDIUM - May need to calculate retroactively
- **Implementation:**
  - Purchase historical data or calculate from play-by-play
  - Retrain NHL models with expanded dataset
- **Expected ROI Boost:** +1-2%

---

### Low Priority (Low Impact or High Effort)

**9. Recruiting Rankings for NCAAF**
- **Impact:** LOW - Already have talent composites
- **Effort:** LOW - 247Sports API
- **Implementation:**
  - Integrate recruiting class rankings
  - Weight by player retention
- **Expected ROI Boost:** +0.5-1%

**10. Coaching Change Tracking**
- **Impact:** LOW - Infrequent events
- **Effort:** LOW - Manual tracking or scraping
- **Implementation:**
  - Flag games with coaching changes
  - Adjust expectations for first 5 games
- **Expected ROI Boost:** +0.5%

**11. Travel Distance & Fatigue**
- **Impact:** LOW - Small effect size
- **Effort:** MEDIUM - Calculate from schedules
- **Implementation:**
  - Calculate miles traveled
  - Account for time zones crossed
  - Model fatigue effects
- **Expected ROI Boost:** +0.5-1%

**12. Altitude Effects (Denver, Air Force, etc.)**
- **Impact:** LOW - Few games affected
- **Effort:** LOW - Binary flag
- **Implementation:**
  - Flag high-altitude games
  - Adjust cardiovascular demands
- **Expected ROI Boost:** +0.2-0.5%

---

### System Improvements (Non-Predictive)

**13. Feature Importance Dashboard**
- **Purpose:** Understand which features drive predictions
- **Tools:** SHAP values, permutation importance
- **Benefit:** Faster debugging, better feature engineering

**14. Backtesting Framework**
- **Purpose:** Test new features before production
- **Implementation:** Historical simulation with walk-forward validation
- **Benefit:** Prevent bad model deployments

**15. Automated Hyperparameter Tuning**
- **Purpose:** Optimize model parameters weekly
- **Tools:** Optuna, GridSearchCV
- **Benefit:** +1-2% accuracy over manual tuning

**16. Data Validation Pipeline**
- **Purpose:** Catch data quality issues early
- **Checks:** Duplicate detection, outlier detection, missing data alerts
- **Benefit:** Prevent bad predictions from bad data

**17. A/B Testing for Model Changes**
- **Purpose:** Compare new models vs baseline
- **Implementation:** Run both models in parallel for 1-2 weeks
- **Benefit:** Data-driven model selection

---

## TECHNICAL REFERENCE

### File Locations

**Data Loaders:**
```
C:\Users\nashr\backend\ml\data_loaders\
├── nba_data_loader.py         (194 lines)
├── ncaab_data_loader.py       (291 lines)
├── nhl_data_loader.py         (393 lines)
├── nfl_data_loader.py         (283 lines)
└── ncaaf_data_loader.py       (316 lines)
```

**Feature Engineers:**
```
C:\Users\nashr\backend\ml\feature_engineering\
├── nba_features.py            (238 lines)
├── ncaab_features.py          (230 lines)
├── nhl_features.py            (323 lines)
├── nfl_features.py            (228 lines)
└── ncaaf_features.py          (244 lines)
```

**API Clients:**
```
C:\Users\nashr\backend\
├── espn_nba_client.py
├── espn_ncaab_client.py
├── espn_nfl_client.py
├── nhl_stats_client.py
├── sportsdataio_odds_client.py
└── odds_client.py
```

**Models (Training Scripts):**
```
C:\Users\nashr\backend\models\
├── nba\
│   ├── xgboost_totals.py
│   ├── xgboost_spreads.py
│   ├── xgboost_moneyline.py
│   ├── lightgbm_totals.py
│   ├── lightgbm_spreads.py
│   ├── lightgbm_moneyline.py
│   ├── random_forest_totals.py
│   ├── random_forest_spreads.py
│   ├── random_forest_moneyline.py
│   ├── linear_regression_totals.py
│   ├── linear_regression_spreads.py
│   └── logistic_regression_moneyline.py
├── ncaab\
├── nhl\
├── nfl\
└── ncaaf\
```

**Trained Models (Serialized):**
```
C:\Users\nashr\backend\ml\models\
├── nba_xgboost_totals_20250112.pkl
├── nba_lightgbm_spreads_20250112.pkl
└── ... (87 total .pkl files)
```

**Data Storage:**
```
C:\Users\nashr\backend\data\
├── historical\              # Training data
│   ├── nba\
│   │   └── nba_games_2022-2024.csv
│   ├── ncaab\
│   │   └── ncaab_games_historical.csv
│   ├── nhl\
│   ├── nfl\
│   └── ncaaf\
├── raw\                     # Scraped/raw data
│   ├── nba\
│   ├── ncaab\
│   │   └── kenpom_20251112.csv
│   ├── nhl\
│   └── odds\
├── predictions\             # Daily predictions
│   └── predictions_latest.csv
└── tracking\                # Performance logs
    ├── predictions_log_multi_bet.csv  (2,426 rows)
    └── results_log.csv                (1,276 rows)
```

---

### Key Configuration Files

**Database Config:**
```
C:\Users\nashr\backend\config.py
```

**Environment Variables:**
```
C:\Users\nashr\backend\.env
├── ODDS_API_KEY=b569397089cab564f5fa1dd218288aec
├── SPORTS_DATA_IO_KEY=[key]
├── GOOGLE_SHEETS_CREDENTIALS=[path]
└── GOOGLE_SHEETS_SHEET_ID=[id]
```

**Logging:**
```
C:\Users\nashr\backend\logs\
├── autonomous_nba.log
├── autonomous_ncaab.log
├── prediction_runner.log
├── results_recorder.log
└── live_monte_carlo.log
```

---

### Dependencies

**Core Libraries:**
```python
# ML/Data Science
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
xgboost>=2.0.0
lightgbm>=4.0.0

# API Clients
requests>=2.31.0
nba_api>=1.2.0
selenium>=4.10.0

# Database
sqlalchemy>=2.0.0

# Utilities
python-dotenv>=1.0.0
pytz>=2023.3
```

**Installation:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

### API Rate Limits

| Service | Limit | Cost | Notes |
|---------|-------|------|-------|
| **Odds API** | 500 req/month (free) | $0 (free tier) | 3-day historical limit |
| **Sports Data IO** | 1,000 req/day | $0 (trial) | Upgrade for live data |
| **ESPN API** | Unlimited | Free | Public endpoint |
| **NBA API** | Unlimited | Free | Official Python package |
| **NHL API** | Unlimited | Free | Official endpoint |
| **KenPom** | Manual scraping | $20/year subscription | Selenium required |
| **MoneyPuck** | Unlimited | Free | Public CSV downloads |
| **MoreHockeyStats** | Unlimited | Free | Public data |

---

### System Requirements

**Production VPS (Current):**
- **CPU:** 4 vCPU
- **RAM:** 8 GB
- **Storage:** 100 GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Python:** 3.10+
- **Services:** Nginx, Uvicorn (FastAPI)

**Local Development:**
- **Python:** 3.10-3.12
- **RAM:** 8 GB minimum (16 GB recommended)
- **Storage:** 20 GB free space

---

## SUMMARY

### What We Have

**Complete Data Pipeline:**
- ✅ 5 sports (NBA, NCAAB, NHL, NFL, NCAAF)
- ✅ 87 ML models (XGBoost, LightGBM, RF, Linear/Logistic)
- ✅ 30,000+ historical games for training
- ✅ 20-54 engineered features per model
- ✅ Real-time predictions (<1 second latency)
- ✅ Autonomous weekly retraining
- ✅ Complete performance tracking (1,276 results logged)

**Current Performance:**
- **Overall:** 49.75% win rate (-4.65% ROI)
- **Best:** MEDIUM confidence (56.2% win rate, +7.4% ROI)
- **Best Sport:** NFL (80% win rate, 12-3 record)
- **Best Model:** Ensemble (53% win rate)

### What We Need

**High Priority:**
1. Fix HIGH confidence threshold (currently -9.7% ROI)
2. Improve NBA models (38.4% win rate → 50%+)
3. Integrate player injury data

**Medium Priority:**
4. Strength of schedule adjustments
5. Advanced NFL metrics (EPA, DVOA)
6. Play-by-play data integration

**Long-term:**
7. Feature importance dashboard
8. Automated hyperparameter tuning
9. A/B testing framework

---

### Contact & Maintenance

**System Owner:** Max EV Sports
**Last Updated:** 2025-11-12
**Next Retraining:** Monday 2025-11-18 at 4am CST
**Next Review:** Monthly (2025-12-01)

**For Questions/Issues:**
- System Status: `AUTONOMOUS_SYSTEM_STATUS.md`
- Today's Work: `TODAYS_ACCOMPLISHMENTS.md`
- Task Tracking: `AUTONOMOUS_SYSTEM_FIX_TASKS.md`

---

**🎯 End of Documentation**
