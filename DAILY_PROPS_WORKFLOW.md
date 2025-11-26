# Daily Player Props Workflow

**Manual workflow for grading, scraping, and generating player props predictions**

---

## Quick Reference (Copy-Paste Commands)

### Full Daily Workflow (Run All Steps)
```bash
# Navigate to backend folder
cd C:\Users\nashr\backend

# Step 1: Grade yesterday's props
python -c "
import sys; sys.path.insert(0, '.')
from scrapers.props.results_tracker import PropsResultsTracker
from datetime import date, timedelta
tracker = PropsResultsTracker(db_path='data/player_props.db')
result = tracker.grade_previous_day_props(date.today() - timedelta(days=1))
print(f'Graded: {result[\"graded\"]}, Skipped: {result[\"skipped\"]}, Errors: {result[\"errors\"]}')
"

# Step 2: Scrape new props for ALL sports (~47 API calls)
python scrapers/props/multi_sport_props_scraper.py --sports all --db data/player_props.db

# Step 3: Generate ML predictions
python run_daily_props_workflow.py --task predictions
```

---

## Detailed Steps

### Step 1: Grade Yesterday's Props (2:00 AM CST)

Grades props from yesterday using BallDontLie API (FREE - no API key needed).

**Full command:**
```bash
cd C:\Users\nashr\backend
python -c "
import sys; sys.path.insert(0, '.')
from scrapers.props.results_tracker import PropsResultsTracker
from datetime import date, timedelta
tracker = PropsResultsTracker(db_path='data/player_props.db')
result = tracker.grade_previous_day_props(date.today() - timedelta(days=1))
print(f'Graded: {result[\"graded\"]}, Skipped: {result[\"skipped\"]}, Errors: {result[\"errors\"]}')
"
```

**Grade a specific date:**
```bash
python -c "
import sys; sys.path.insert(0, '.')
from scrapers.props.results_tracker import PropsResultsTracker
from datetime import date
tracker = PropsResultsTracker(db_path='data/player_props.db')
result = tracker.grade_previous_day_props(date(2025, 11, 25))  # Change date here
print(f'Graded: {result[\"graded\"]}, Skipped: {result[\"skipped\"]}, Errors: {result[\"errors\"]}')
"
```

---

### Step 2: Scrape Props Lines (8:00-9:00 AM CST)

Fetches player props from The Odds API for all supported sports.

**API Cost Estimate:**
- NBA: ~9 calls (1 events + 8 games)
- NCAAB: ~16 calls (1 events + 15 games)
- NFL: ~4 calls (1 events + 3 games)
- NCAAF: ~11 calls (1 events + 10 games)
- NHL: ~7 calls (1 events + 6 games)
- **Total: ~47 API calls for full scrape**

**Scrape ALL sports:**
```bash
cd C:\Users\nashr\backend
python scrapers/props/multi_sport_props_scraper.py --sports all --db data/player_props.db
```

**Scrape specific sports:**
```bash
# NBA only
python scrapers/props/multi_sport_props_scraper.py --sports nba --db data/player_props.db

# NBA and NHL
python scrapers/props/multi_sport_props_scraper.py --sports nba,nhl --db data/player_props.db

# NFL and NCAAF
python scrapers/props/multi_sport_props_scraper.py --sports nfl,ncaaf --db data/player_props.db
```

**Supported sports:** `nba`, `ncaab`, `nfl`, `ncaaf`, `nhl`

**Prop types by sport:**
| Sport | Prop Types |
|-------|-----------|
| NBA | points, rebounds, assists, threes, PRA, blocks, steals |
| NCAAB | points, rebounds, assists, threes |
| NFL | pass_yards, pass_tds, rush_yards, rush_tds, receptions, receiving_yards, anytime_td |
| NCAAF | pass_yards, pass_tds, rush_yards, rush_tds, receptions, receiving_yards |
| NHL | points, assists, goals, shots_on_goal, anytime_goal |

---

### Step 3: Generate ML Predictions (9:00 AM CST)

Uses trained ML models to generate predictions and identify edges.

```bash
cd C:\Users\nashr\backend
python run_daily_props_workflow.py --task predictions
```

**Alternative (manual prediction generation):**
```bash
python -c "
import sqlite3
from datetime import date
from ml.predictions.daily_props_predictor_fast import EnhancedPropsPredictor

today = date.today().strftime('%Y-%m-%d')
predictor = EnhancedPropsPredictor(db_path='data/player_props.db')
predictor.load_models()
predictor.load_team_stats()

conn = sqlite3.connect('data/player_props.db')
cursor = conn.cursor()
cursor.execute('''SELECT DISTINCT player_id, player_name, team, opponent, home_away, prop_type, market_line FROM player_props_lines WHERE date = ?''', (today,))
props = cursor.fetchall()
print(f'Found {len(props)} props to predict')

saved = 0
for prop in props:
    player_id, player_name, team, opponent, home_away, prop_type, market_line = prop
    try:
        prediction = predictor.predict_prop(player_id=player_id, player_name=player_name, team=team, opponent=opponent, prop_type=prop_type, market_line=market_line, home_away=home_away or 'HOME')
        if prediction:
            predicted_value = prediction['predicted_value']
            edge = predicted_value - market_line
            edge_pct = (edge / market_line) * 100 if market_line > 0 else 0
            recommendation = 'OVER' if edge > 0 else 'UNDER'
            cursor.execute('''INSERT OR REPLACE INTO player_props_predictions (prediction_date, game_date, player_id, player_name, team, opponent, prop_type, market_line, predicted_value, confidence, model_type, edge_pct, recommendation, sport) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (today, today, player_id, player_name, team, opponent, prop_type, market_line, predicted_value, prediction.get('confidence', 0.5), 'ensemble', edge_pct, recommendation, 'nba'))
            saved += 1
    except: pass
conn.commit()
conn.close()
print(f'Saved {saved} predictions')
"
```

---

## Verification Queries

### Check database status:
```bash
cd C:\Users\nashr\backend
sqlite3 data/player_props.db "SELECT 'Lines:' as type, COUNT(*) as count FROM player_props_lines UNION ALL SELECT 'Predictions:' as type, COUNT(*) FROM player_props_predictions UNION ALL SELECT 'Graded:' as type, COUNT(*) FROM player_props_predictions WHERE result IS NOT NULL"
```

### Check today's data:
```bash
sqlite3 data/player_props.db "SELECT date, COUNT(*) as props FROM player_props_lines GROUP BY date ORDER BY date DESC LIMIT 5"
```

### Check graded results summary:
```bash
sqlite3 data/player_props.db "SELECT result, COUNT(*) as count FROM player_props_predictions WHERE result IS NOT NULL GROUP BY result"
```

### Check performance by prop type:
```bash
sqlite3 data/player_props.db "SELECT prop_type, COUNT(*) as total, SUM(CASE WHEN result='WIN' THEN 1 ELSE 0 END) as wins, ROUND(SUM(CASE WHEN result='WIN' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as win_pct FROM player_props_predictions WHERE result IS NOT NULL GROUP BY prop_type ORDER BY win_pct DESC"
```

### Check performance by sport:
```bash
sqlite3 data/player_props.db "SELECT COALESCE(sport, 'nba') as sport, COUNT(*) as total, SUM(CASE WHEN result='WIN' THEN 1 ELSE 0 END) as wins, ROUND(SUM(CASE WHEN result='WIN' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as win_pct FROM player_props_predictions WHERE result IS NOT NULL GROUP BY sport"
```

---

## API Endpoints (VPS)

After running the workflow, data is available at:

- **Overview:** `https://max-ev-sports.com/api/props-performance/overview?days=30`
- **History:** `https://max-ev-sports.com/api/props-performance/history?days=90`
- **Predictions:** `https://max-ev-sports.com/api/props-performance/predictions?limit=50`
- **With filters:** `https://max-ev-sports.com/api/props-performance/overview?sport=nba&prop_type=points&days=30`

---

## Weekly Model Retraining (Mondays 4:00 AM CST)

Retrain ML models with latest graded results:

```bash
cd C:\Users\nashr\backend
python ml/models/nba_props_trainer.py --prop-type all
```

---

## Backup Data

After completing workflow, backup data to D: drive:

```bash
python backup_props_data.py
```

---

## Sync to VPS

After local workflow completes, sync database to VPS:

```bash
# Copy database to VPS
scp -i ~/.ssh/hostinger_vps C:\Users\nashr\backend\data\player_props.db root@148.230.87.135:/root/sporttrader/backend/data/

# Restart backend on VPS
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"
```

---

## Troubleshooting

### "No props found for today"
- Check if games are scheduled for today
- Verify Odds API key is valid and has remaining requests
- Try scraping a specific sport first: `--sports nba`

### "Could not find player"
- BallDontLie API may not have all players
- Some college players may be missing
- Check player name spelling matches database

### Database locked
- Close any SQLite browser connections
- Wait a few seconds and retry

### API rate limit
- Check remaining requests in scraper output
- Spread scraping across multiple runs if needed

---

## Schedule Summary

| Time (CST) | Task | Command |
|------------|------|---------|
| 2:00 AM | Grade yesterday | `python run_daily_props_workflow.py --task night` |
| 8:00 AM | Scrape props | `python scrapers/props/multi_sport_props_scraper.py --sports all` |
| 9:00 AM | Generate predictions | `python run_daily_props_workflow.py --task predictions` |
| Monday 4:00 AM | Retrain models | `python ml/models/nba_props_trainer.py --prop-type all` |

---

## Files Reference

| File | Purpose |
|------|---------|
| `scrapers/props/multi_sport_props_scraper.py` | Scrape props from all sports |
| `scrapers/props/results_tracker.py` | Grade props using BallDontLie API |
| `run_daily_props_workflow.py` | Orchestrate daily workflow |
| `ml/predictions/daily_props_predictor_fast.py` | ML prediction engine |
| `routes/props_performance.py` | API endpoints for frontend |
| `data/player_props.db` | SQLite database with all props data |

---

**Last Updated:** 2025-11-26
