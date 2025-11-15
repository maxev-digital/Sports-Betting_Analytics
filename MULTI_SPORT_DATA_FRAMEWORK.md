# MAX-EV-SPORTS - Multi-Sport Data Collection Framework
**Last Updated:** November 14, 2025

This document defines the **universal file structure and data organization framework** for all sports (NBA, NFL, NHL, NCAAB, NCAAF, MLB, etc.).

This framework applies to:
- **Player Stats Collection** (game logs, season averages, rolling stats, splits)
- **Player Props System** (lines, results, predictions, ML models)
- **Game Predictions** (outcomes, totals, spreads)
- **Performance Tracking** (results, ROI, accuracy)
- **Backend API** (routes, databases, utilities)
- **Frontend Dashboard** (pages, components)

**Current Implementation:** NBA (in progress - Week 2 of 8)
**Upcoming:** NFL, NHL, NCAAB, NCAAF, MLB (same structure)

---

## D: DRIVE (EXTERNAL HARD DRIVE) - PRIMARY DATA STORAGE

```
D:/
├── backend/                                  # Main backend directory
│   │
│   ├── data/                                # ALL DATA STORAGE
│   │   │
│   │   ├── DATABASES/
│   │   │   ├── player_stats.db             # Player stats database (NEW)
│   │   │   ├── player_props.db             # Props database (EXISTING)
│   │   │   └── game_predictions.db         # Game predictions (if needed)
│   │   │
│   │   ├── player_stats/                   # PLAYER STATISTICS (NEW)
│   │   │   ├── game_logs/
│   │   │   │   ├── 2025-11-14_game_logs.csv
│   │   │   │   ├── 2025-11-15_game_logs.csv
│   │   │   │   └── all_game_logs.csv       # Master file (all games)
│   │   │   ├── season_averages/
│   │   │   │   ├── 2025-11-14_season_avg.csv
│   │   │   │   └── current_season_averages.csv
│   │   │   ├── rolling_averages/
│   │   │   │   ├── 2025-11-14_rolling_avg.csv
│   │   │   │   └── current_rolling_averages.csv
│   │   │   ├── splits/
│   │   │   │   ├── home_away_splits.csv
│   │   │   │   └── opponent_matchups.csv
│   │   │   └── archive/
│   │   │       └── (old CSVs >30 days)
│   │   │
│   │   ├── props/                          # PLAYER PROPS DATA
│   │   │   ├── lines/
│   │   │   │   ├── 2025-11-14_props_lines.csv
│   │   │   │   └── all_props_lines.csv
│   │   │   ├── results/
│   │   │   │   ├── graded_props_data.csv
│   │   │   │   └── daily_collection_summary.csv
│   │   │   ├── predictions/
│   │   │   │   ├── 2025-11-14_props_predictions.csv
│   │   │   │   └── all_predictions.csv
│   │   │   └── archive/
│   │   │
│   │   ├── predictions/                    # GAME PREDICTIONS (EXISTING ML SYSTEM)
│   │   │   ├── nba/
│   │   │   │   └── nba_predictions_latest.csv
│   │   │   ├── ncaab/
│   │   │   │   └── ncaab_predictions_latest.csv
│   │   │   ├── nfl/
│   │   │   │   └── nfl_predictions_latest.csv
│   │   │   ├── nhl/
│   │   │   │   └── nhl_predictions_latest.csv
│   │   │   └── ncaaf/
│   │   │       └── ncaaf_predictions_latest.csv
│   │   │
│   │   ├── tracking/                       # PERFORMANCE TRACKING
│   │   │   ├── predictions_log_multi_bet.csv
│   │   │   ├── results_log.csv
│   │   │   ├── performance_summary.csv
│   │   │   └── props/
│   │   │       └── props_performance_log.csv
│   │   │
│   │   ├── models/                         # TRAINED ML MODELS
│   │   │   ├── props/
│   │   │   │   └── nba/
│   │   │   │       ├── points_model.pkl
│   │   │   │       ├── rebounds_model.pkl
│   │   │   │       ├── assists_model.pkl
│   │   │   │       ├── threes_model.pkl
│   │   │   │       ├── blocks_model.pkl
│   │   │   │       ├── steals_model.pkl
│   │   │   │       ├── ensemble_model.pkl
│   │   │   │       └── model_metadata.json
│   │   │   └── games/                      # Game outcome models
│   │   │       ├── nba/
│   │   │       │   ├── xgboost_model.pkl
│   │   │       │   ├── lgbm_model.pkl
│   │   │       │   └── rf_model.pkl
│   │   │       ├── ncaab/
│   │   │       ├── nfl/
│   │   │       ├── nhl/
│   │   │       └── ncaaf/
│   │   │
│   │   ├── raw/                            # RAW SCRAPED DATA
│   │   │   ├── nba/
│   │   │   │   ├── team_stats.csv
│   │   │   │   └── schedule.csv
│   │   │   ├── ncaab/
│   │   │   │   └── kenpom_ratings.csv
│   │   │   └── odds/
│   │   │       ├── nba_odds.csv
│   │   │       └── ncaab_odds.csv
│   │   │
│   │   ├── backtesting/                    # BACKTESTING RESULTS
│   │   │   ├── props/
│   │   │   └── games/
│   │   │
│   │   └── historical/                     # HISTORICAL DATA (ARCHIVE)
│   │       ├── 2023-24_season/
│   │       ├── 2024-25_season/
│   │       └── 2025-26_season/
│   │
│   ├── scrapers/                           # DATA COLLECTION SCRIPTS
│   │   │
│   │   ├── stats/                          # PLAYER STATS SCRAPERS (NEW)
│   │   │   ├── nba_stats_scraper.py       # Comprehensive NBA stats scraper
│   │   │   ├── stats_aggregator.py        # Calculate averages/splits
│   │   │   └── daily_stats_workflow.py    # Daily automation
│   │   │
│   │   ├── props/                          # PROPS SCRAPERS
│   │   │   ├── balldontlie_client.py      # BallDontLie API client
│   │   │   ├── daily_props_scraper.py     # Props lines scraper
│   │   │   ├── results_tracker.py         # Props grading
│   │   │   ├── player_stats_scraper.py    # Player stats for props
│   │   │   ├── IMPLEMENTATION_PLAN.md     # 8-week roadmap
│   │   │   ├── README.md                  # Props system status
│   │   │   └── FILE_STRUCTURE.md          # Props file org
│   │   │
│   │   ├── nba/                            # NBA GAME DATA
│   │   │   ├── nba_api_stats.py
│   │   │   └── schedule_scraper.py
│   │   │
│   │   ├── ncaab/                          # NCAAB DATA
│   │   │   └── ken_pom_scraper_selenium_fixed.py
│   │   │
│   │   ├── nfl/                            # NFL DATA
│   │   ├── nhl/                            # NHL DATA
│   │   ├── ncaaf/                          # NCAAF DATA
│   │   │
│   │   └── odds/                           # BETTING ODDS
│   │       ├── odds_api_scraper.py
│   │       └── ncaab_odds_scraper.py
│   │
│   ├── models/                             # ML MODEL CODE
│   │   │
│   │   ├── props/                          # PROPS ML MODELS
│   │   │   └── nba/
│   │   │       ├── feature_engineer.py    # Week 3 - 50+ features
│   │   │       ├── nba_props_trainer.py   # Week 5 - Model training
│   │   │       ├── predictor.py           # Week 7 - Generate predictions
│   │   │       └── model_evaluator.py     # Performance analysis
│   │   │
│   │   └── games/                          # GAME OUTCOME MODELS
│   │       ├── nba/
│   │       │   └── totals_predictor.py
│   │       └── ncaab/
│   │           └── totals_predictor.py
│   │
│   ├── routes/                             # API ENDPOINTS
│   │   ├── props_performance.py           # Props performance tracking
│   │   ├── props_predictions.py           # Props predictions API (Week 7)
│   │   ├── player_stats.py                # Player stats API (NEW)
│   │   ├── games.py                       # Game predictions API
│   │   ├── model_performance.py           # Model performance tracking
│   │   └── alerts.py                      # Live alerts
│   │
│   ├── utils/                              # UTILITY FUNCTIONS
│   │   ├── performance_tracker.py
│   │   └── db_utils.py
│   │
│   ├── main.py                             # FastAPI app
│   ├── config.py                           # Configuration
│   └── requirements.txt                    # Dependencies
│
└── roadmap/                                # PLANNING DOCUMENTS
    ├── PLAYER_PROPS_ML_IMPLEMENTATION_PLAN.md
    ├── ML_AUTONOMOUS_SYSTEM_REFERENCE.md
    └── CRITICAL_FIXES_DO_NOT_CHANGE.md
```

---

## C: DRIVE (LOCAL) - CODE & FRONTEND

```
C:/Users/nashr/
├── backend/                                # SYMLINK to D:/backend
│
├── frontend/                               # REACT FRONTEND
│   ├── src/
│   │   ├── pages/
│   │   │   ├── PropsPerformance.tsx       # Props performance dashboard
│   │   │   ├── PlayerStats.tsx            # Player stats page (NEW)
│   │   │   ├── ModelPerformance.tsx       # Game model performance
│   │   │   ├── EdgeLab.tsx                # Edge analysis
│   │   │   ├── Analytics.tsx              # Analytics dashboard
│   │   │   └── ...
│   │   │
│   │   ├── components/
│   │   │   ├── PlayerStatsTable.tsx       # (NEW)
│   │   │   ├── PropsTable.tsx
│   │   │   ├── GameCard.tsx
│   │   │   └── ...
│   │   │
│   │   └── api/
│   │       ├── playerStats.ts             # (NEW)
│   │       ├── props.ts
│   │       └── games.ts
│   │
│   ├── public/
│   └── package.json
│
├── PROPS_IMPLEMENTATION_STATUS.md         # Current props status
├── verify_props_progress.py               # Verification script
└── COMPLETE_FILE_STRUCTURE.md             # This file
```

---

## VPS (PRODUCTION SERVER)

```
/root/sporttrader/
├── backend/                                # Backend API
│   └── (mirrors D:/backend structure)
│
└── frontend/
    └── dist/                               # Built frontend
```

---

## DATABASE SCHEMAS

### **player_stats.db** (NEW)

**Tables:**
1. `players` - Player metadata
2. `player_game_logs` - Raw game-by-game stats
3. `player_season_stats` - Calculated season averages
4. `player_rolling_stats` - L5/L10/L20 averages
5. `player_splits` - Home/away, matchup splits

### **player_props.db** (EXISTING)

**Tables:**
1. `player_props_lines` - Props lines from bookmakers
2. `player_props_results` - Graded props results
3. `player_props_predictions` - ML predictions

---

## WORKFLOW FILES

**Daily Automation:**
- `run_daily_stats_scraper.py` - Scrape player stats (7am)
- `run_daily_props_scraper.py` - Scrape props lines (8am)
- `run_daily_predictions.py` - Generate predictions (9am)
- `run_props_grading.py` - Grade previous day props (after games)

**Weekly Automation:**
- `run_weekly_model_training.py` - Retrain models (Mondays 4am)
- `run_weekly_archive.py` - Archive old data (Sundays)

---

## KEY LOCATIONS BY FUNCTION

**Player Stats:**
- Database: `D:/backend/data/player_stats.db`
- CSVs: `D:/backend/data/player_stats/`
- Scraper: `D:/backend/scrapers/stats/nba_stats_scraper.py`
- API: `C:/Users/nashr/backend/routes/player_stats.py`

**Player Props:**
- Database: `D:/backend/data/player_props.db`
- CSVs: `D:/backend/data/props/`
- Scrapers: `D:/backend/scrapers/props/`
- API: `C:/Users/nashr/backend/routes/props_performance.py`

**Game Predictions:**
- CSVs: `D:/backend/data/predictions/{sport}/`
- Models: `D:/backend/data/models/games/{sport}/`
- Scrapers: `D:/backend/scrapers/{sport}/`

**ML Models:**
- Props: `D:/backend/data/models/props/nba/`
- Games: `D:/backend/data/models/games/{sport}/`

---

## NOTES

- D: drive is external hard drive - primary data storage
- C: drive has code and frontend - backed up to git
- Backend code symlinked: C:/Users/nashr/backend → D:/backend
- All databases on D: drive for persistence
- CSV exports for verification/backup
- Archive old data after 30 days
- VPS mirrors D:/backend structure
