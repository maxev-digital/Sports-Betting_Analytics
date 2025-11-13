# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ CRITICAL: BEFORE MAKING ANY CODE CHANGES ⚠️

**📖 READ FIRST: [CRITICAL_FIXES_DO_NOT_CHANGE.md](./CRITICAL_FIXES_DO_NOT_CHANGE.md)**

This document contains **PROTECTED CODE** that is currently **WORKING IN PRODUCTION**.

**DO NOT modify these sections without explicit user approval:**
1. Edge scanner sport filtering (edge_scanner.py line 597)
2. Model performance merge strategy (model_performance.py line 76)
3. Charts cumulative calculation (model_performance.py line 234)
4. Frontend API configuration (config.ts)
5. Time range filter implementation (ModelPerformance.tsx)
6. UI component ordering (ModelPerformance.tsx)
7. CSV prediction format (generate_all_sport_predictions.py)

**The user has experienced multiple instances of "fixes" breaking working code.**
**Stability > Optimization. ASK FIRST before changing anything in the protected sections.**

---

## IMPORTANT: For ML/Autonomous System Questions

**📖 See [ML_AUTONOMOUS_SYSTEM_REFERENCE.md](./ML_AUTONOMOUS_SYSTEM_REFERENCE.md)** for complete documentation on:
- Autonomous learning system (5 sports: NBA, NCAAB, NHL, NFL, NCAAF)
- 87 ML models (XGBoost, LightGBM, Random Forest, Linear)
- Weekly retraining schedule (Mondays 4-9am CST)
- Daily prediction schedule (9-11am CST)
- Live alert system (6-11pm CST every 5 min)
- VPS configuration and troubleshooting
- Scaling projections and maintenance

This document below covers legacy prediction workflows and manual operations.

---

## Project Overview

This is a sports betting analytics platform with a **fully autonomous machine learning system** that:
- Generates daily predictions for NBA, NCAAB, NHL, NFL, NCAAF
- Retrains models weekly with actual game results
- Deploys improved models automatically
- Runs live betting alerts during games
- **No manual intervention required**

The system also includes legacy pace-based prediction models for NBA and NCAA Basketball totals (over/under).

## Architecture

### Directory Structure

```
C:\Users\nashr\
├── backend/                          # Core prediction system
│   ├── models/                       # Prediction models
│   │   ├── nba/totals_predictor.py  # NBA totals prediction model
│   │   └── ncaab/totals_predictor.py # NCAA Basketball prediction model
│   ├── scrapers/                     # Data collection modules
│   │   ├── nba/
│   │   │   ├── nba_api_stats.py     # NBA team stats from official API
│   │   │   └── schedule_scraper.py  # Schedule data for rest days
│   │   ├── ncaab/
│   │   │   └── ken_pom_scraper_selenium_fixed.py  # KenPom ratings scraper
│   │   └── odds/
│   │       ├── odds_api_scraper.py         # NBA odds scraper
│   │       └── ncaab_odds_scraper.py       # NCAA odds scraper
│   ├── sheets_integration/           # Google Sheets uploaders
│   │   ├── nba_sheets_uploader.py
│   │   └── ncaab_sheets_uploader.py
│   ├── utils/
│   │   └── performance_tracker.py    # Track predictions vs actual results
│   ├── data/                         # All data files
│   │   ├── raw/                      # Scraped stats (NBA, NCAAB)
│   │   ├── predictions/              # Generated predictions CSVs
│   │   ├── tracking/                 # Performance logs
│   │   ├── backtesting/              # Historical backtests
│   │   └── historical/               # Historical data for analysis
│   └── config.py                     # Configuration and constants
├── run_daily_predictions.py          # NBA workflow runner
├── run_ncaab_predictions.py          # NCAA workflow runner
├── config.py                         # NCAA configuration
└── config_calibrated.py              # Calibrated NCAA parameters
```

### Key Components

**Prediction Models:**
- Use pace-adjusted efficiency ratings to predict game totals
- NBA model: Uses official NBA API stats (pace, offensive rating, defensive rating)
- NCAA model: Uses KenPom efficiency data (AdjTempo, AdjOffEff, AdjDefEff)
- Both models adjust for home court advantage and rest days

**Data Flow:**
1. Scrape team statistics (NBA API or KenPom)
2. Fetch betting odds from Odds API
3. Generate predictions with confidence levels
4. Log predictions for tracking
5. Upload to Google Sheets
6. Record actual results and calculate performance metrics

## Common Development Workflows

### Running NBA Daily Predictions

```bash
python run_daily_predictions.py
```

This master script runs the complete NBA workflow:
1. Scrapes current NBA team stats (30 teams)
2. Fetches betting odds for next 14 days
3. Analyzes rest days and back-to-back situations
4. Generates predictions with edge calculations
5. Logs predictions to tracking system
6. Uploads to Google Sheets (ID: 1bFNPXj2wOOBid8d-dnHbKmSs5U90a66X29-PFRmkgvo)

Output: `backend/data/predictions/nba_predictions_latest.csv`

### Running NCAA Basketball Predictions

```bash
python run_ncaab_predictions.py
```

NCAA workflow:
1. Loads most recent KenPom data from `backend/data/raw/ncaab/`
2. Fetches NCAA betting odds
3. Generates predictions using KenPom efficiency ratings
4. Uploads to Google Sheets

**Note:** KenPom data must be scraped separately first:
```bash
python backend/scrapers/ncaab/ken_pom_scraper_selenium_fixed.py
```

### Running Individual Components

**Scrape NBA team stats only:**
```bash
python backend/scrapers/nba/nba_api_stats.py
```

**Scrape betting odds only:**
```bash
python backend/scrapers/odds/odds_api_scraper.py
```

**Test the NBA prediction model:**
```bash
python backend/models/nba/totals_predictor.py
```

**Track performance interactively:**
```bash
python backend/utils/performance_tracker.py
```
This tool allows you to:
- Log predictions
- Record actual game results
- Calculate win rates and ROI
- View performance by confidence level

## Configuration

### Environment Variables
Located in `backend/.env`:
- `ODDS_API_KEY`: API key for The Odds API (https://the-odds-api.com/)
- `GOOGLE_SHEETS_CREDENTIALS`: Path to service account JSON
- `GOOGLE_SHEETS_SHEET_ID`: Target Google Sheet ID

### Model Parameters

**NBA (in `backend/models/nba/totals_predictor.py`):**
- Home court advantage: 2.5 points
- Confidence thresholds:
  - HIGH: 5.0+ point edge
  - MEDIUM: 3.0-4.9 point edge
  - LOW: 2.0-2.9 point edge
- Rest day adjustments:
  - Back-to-back (0 days): -2.0 pace
  - Both teams rested (2+ days): +1.0 pace
  - One team fresh (3+ days): +1.5 pace

**NCAA (in `config.py` and `config_calibrated.py`):**
- Two configuration files exist for testing different parameter sets
- `config.py`: Original NCAA parameters (HCA=4.0, EFF=110.0)
- `config_calibrated.py`: Calibrated to reduce prediction bias (HCA=3.0, EFF=98.0)

## Data Files

### Predictions Format
CSV files in `backend/data/predictions/` contain:
- Game metadata (date, time, teams)
- Rest day information
- Pace and efficiency breakdown
- Predicted total vs market total
- Edge size and recommendation (OVER/UNDER)
- Confidence level (HIGH/MEDIUM/LOW)
- Bet decision (YES/NO)

### Tracking Files
Located in `backend/data/tracking/`:
- `predictions_log.csv`: All logged predictions with metadata
- `results_log.csv`: Actual game results with win/loss/push outcomes
- `performance_summary.csv`: Historical performance metrics by date

## Python Environment

**Python Version:** 3.12.7

**Virtual Environment:** Located in `venv/` directory

**Key Dependencies (inferred from code):**
- pandas
- numpy
- nba_api (for NBA stats)
- requests (for Odds API)
- gspread (for Google Sheets)
- selenium (for KenPom scraping)

**Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

## Model Methodology

### NBA Totals Prediction

1. **Calculate Expected Pace:**
   - Geometric mean of both teams' pace ratings
   - Adjust for rest days and back-to-back games

2. **Calculate Expected Efficiency:**
   - Home team: `home_off_rating - (away_def_rating - league_avg) + 2.5` (home court)
   - Away team: `away_off_rating - (home_def_rating - league_avg)`

3. **Convert to Points:**
   - `expected_points = (efficiency / 100) * expected_pace`

4. **Total:**
   - `predicted_total = home_expected_points + away_expected_points`

### NCAA Totals Prediction

Similar methodology using KenPom's adjusted tempo and efficiency metrics with NCAA-specific parameters.

## Important Notes

- **API Rate Limits:** The Odds API has usage limits. Monitor your quota.
- **KenPom Scraping:** Requires Selenium and may need authentication credentials.
- **Google Sheets:** Requires service account credentials with appropriate permissions.
- **Season Updates:** Update `current_season` in scrapers when NBA/NCAA seasons change.
- **Team Name Mapping:** NCAA team names often differ between data sources. The `team_name_mapper.py` script helps resolve mismatches.

## Backtesting and Analysis

NCAA backtesting tools are available in `backend/data/backtesting/` and various analysis scripts in `backend/scrapers/ncaab/`. These allow testing model parameters against historical data.

Key backtesting files:
- `run_ncaab_backtest.py`: Run historical backtests
- `check_backtest_ready.py`: Verify data readiness
- `calibrate_model.py`: Optimize model parameters
- `analyze_closing_line_accuracy.py`: Compare predictions to closing lines
