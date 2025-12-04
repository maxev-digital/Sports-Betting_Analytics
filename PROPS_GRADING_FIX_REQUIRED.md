# Props Grading System - Fix Required

**Date**: December 4, 2025
**Status**: ❌ NOT OPERATIONAL
**Priority**: MEDIUM (predictions work, but no performance tracking)

---

## Root Cause Identified

The props grading system (`results_tracker.py`) was written for an older database schema that no longer exists.

### Schema Mismatch

**What the grading code expects**:
```sql
player_props_lines
  - player_id
  - player_name
  - team
  - opponent
  - prop_type
  - market_line
  - date

player_props_results
  - player_id
  - date
  - prop_type
  - actual_value
  - result
```

**What actually exists**:
```sql
player_prop_predictions
  - id (INTEGER PRIMARY KEY)
  - prediction_date (TEXT)
  - player_name (TEXT)
  - team (TEXT)
  - opponent (TEXT)
  - prop_type (TEXT)
  - market_line (REAL)
  - predicted_value (REAL)
  - edge (REAL)
  - over_probability (REAL)
  - under_probability (REAL)
  - confidence (REAL)
  - recommendation (TEXT)
  - kelly_fraction (REAL)
  - sportsbook (TEXT)
  - game_id (TEXT)
  - model_predictions (TEXT/JSON)
  - generated_at (TEXT)
  - result (TEXT) -- NULL, needs grading
  - actual_value (REAL) -- NULL, needs grading
  - graded_at (TEXT) -- NULL, needs grading
  - created_at (TIMESTAMP)
```

### Current Status
- ✅ **Database path fixed**: Changed from `D:/backend/data/player_props.db` to `/root/sporttrader/backend/ml/predictions.db`
- ❌ **Table names wrong**: Code looks for `player_props_lines` and `player_props_results`, but should use `player_prop_predictions`
- ❌ **Column names different**: Field mappings don't match
- ❌ **0 props graded** out of 2,676 total

---

## Fix Options

### Option 1: Rewrite results_tracker.py (RECOMMENDED)
**Time**: 2-3 hours
**Complexity**: Medium

Update `results_tracker.py` to:
1. Use correct table name: `player_prop_predictions`
2. Update column references
3. Use in-place updates instead of separate results table
4. Test with BallDontLie API for NBA props

**Pseudocode**:
```python
def grade_previous_day_props(self, target_date):
    # Get ungraded props from yesterday
    cursor.execute("""
        SELECT id, player_name, team, prop_type, market_line, recommendation
        FROM player_prop_predictions
        WHERE date(prediction_date) = ?
        AND result IS NULL
    """, (target_date,))

    for prop in props:
        # Fetch actual stats from BallDontLie API
        actual = get_player_stats(prop['player_name'], target_date)

        # Determine result (WIN/LOSS)
        if prop['recommendation'] == 'OVER':
            result = 'WIN' if actual > market_line else 'LOSS'
        else:
            result = 'WIN' if actual < market_line else 'LOSS'

        # Update database
        cursor.execute("""
            UPDATE player_prop_predictions
            SET result = ?, actual_value = ?, graded_at = ?
            WHERE id = ?
        """, (result, actual, datetime.now(), prop['id']))
```

### Option 2: Create New Grading Script
**Time**: 1-2 hours
**Complexity**: Low

Write a new `grade_props_from_db.py` that:
- Works with current schema
- Simpler, focused logic
- Better error handling

### Option 3: Migrate to Old Schema
**Time**: 4-5 hours
**Complexity**: High
**Not Recommended**: Requires changing prediction generation code

---

## Implementation Steps (Option 1)

### 1. Update results_tracker.py

```python
# Line 26 - Already fixed
def __init__(self, db_path: str = "/root/sporttrader/backend/ml/predictions.db"):

# Lines 48-63 - Update query
cursor.execute("""
    SELECT id, player_name, team, opponent, prop_type, market_line,
           recommendation, prediction_date
    FROM player_prop_predictions
    WHERE date(prediction_date) = ?
    AND result IS NULL
    ORDER BY player_name
""", (target_date,))

# Lines 70-100 - Update grading logic
for prop in ungraded_props:
    prop_id, player_name, team, opponent, prop_type, market_line, recommendation, pred_date = prop

    # Fetch actual stat from API
    actual_value = self.stats_client.get_player_stat(
        player_name=player_name,
        stat_type=prop_type,
        game_date=target_date
    )

    if actual_value is None:
        continue  # Skip if stat not available

    # Determine result
    if recommendation == 'OVER':
        result = 'WIN' if actual_value > market_line else 'LOSS'
    elif recommendation == 'UNDER':
        result = 'WIN' if actual_value < market_line else 'LOSS'
    else:
        result = 'PUSH'  # NO_PLAY recommendations

    # Update database
    cursor.execute("""
        UPDATE player_prop_predictions
        SET result = ?,
            actual_value = ?,
            graded_at = ?
        WHERE id = ?
    """, (result, actual_value, datetime.now(), prop_id))

    graded_count += 1

conn.commit()
```

### 2. Test Manually

```bash
# SSH to VPS
ssh root@148.230.87.135

# Run grading for yesterday
cd /root/sporttrader/backend
source venv/bin/activate
python3 -c "
from scrapers.props.results_tracker import PropsResultsTracker
from datetime import date, timedelta
t = PropsResultsTracker()
r = t.grade_previous_day_props(date.today() - timedelta(days=1))
print(f'Graded: {r}')
"

# Check results
sqlite3 ml/predictions.db "SELECT COUNT(*), result FROM player_prop_predictions WHERE result IS NOT NULL GROUP BY result;"
```

### 3. Verify Cron Job

The cron job is already configured correctly:
```bash
0 3 * * * cd /root/sporttrader/backend && source venv/bin/activate && python3 -c "from scrapers.props.results_tracker import PropsResultsTracker; from datetime import date, timedelta; t=PropsResultsTracker(); r=t.grade_previous_day_props(date.today()-timedelta(days=1)); print(r)" >> logs/props_grading.log 2>&1
```

Just needs the code fixed.

---

## API Requirements

### BallDontLie API (NBA)
- **Free Tier**: 30 requests/minute
- **Endpoint**: `https://api.balldontlie.io/v1/stats`
- **API Key**: May be required (check `.env` for `BALLDONTLIE_API_KEY`)
- **Documentation**: https://docs.balldontlie.io/

### Required Stats Mapping
```python
prop_type_map = {
    'points': 'pts',
    'rebounds': 'reb',
    'assists': 'ast',
    'steals': 'stl',
    'blocks': 'blk',
    '3pm': 'fg3m',
    'turnovers': 'turnover'
}
```

---

## Testing Checklist

After fixing the code:

- [ ] Import works: `from scrapers.props.results_tracker import PropsResultsTracker`
- [ ] Database path correct: `/root/sporttrader/backend/ml/predictions.db`
- [ ] Can read ungraded props from `player_prop_predictions`
- [ ] API returns player stats for test player
- [ ] Grading logic correctly determines WIN/LOSS
- [ ] Database updates with result, actual_value, graded_at
- [ ] Handles missing stats gracefully
- [ ] Logs output to `logs/props_grading.log`
- [ ] Cron job runs at 3 AM successfully
- [ ] PropsPerformance page shows graded data

---

## Files to Modify

1. **`/root/sporttrader/backend/scrapers/props/results_tracker.py`**
   - Main grading logic
   - Database queries
   - Lines 26, 48-100 need updates

2. **`/root/sporttrader/backend/scrapers/props/balldontlie_client.py`**
   - May need method updates if interface changed
   - Verify API key handling

3. **Create `/root/sporttrader/backend/grade_props_simple.py`** (Optional)
   - Simpler standalone grading script
   - Easier to debug and test

---

## Why This Wasn't Caught Earlier

1. **Silent Failure**: Cron job redirects to log, but log was empty (0 bytes)
2. **No Monitoring**: Old systems check didn't verify grading success
3. **Schema Evolution**: Database evolved but grading code wasn't updated
4. **No Alerts**: No notification when grading fails

Now that comprehensive systems check is in place, this will be caught daily if it fails again.

---

## Impact Assessment

**Until Fixed**:
- ❌ No performance tracking for player props
- ❌ PropsPerformance page shows no data
- ❌ Can't calculate win rate, ROI, or model accuracy
- ✅ Predictions still generate (2,676/day)
- ✅ Users can still see props and place bets
- ✅ No data loss (predictions stored, just not graded)

**After Fixed**:
- ✅ Automatic nightly grading
- ✅ Win/loss tracking
- ✅ Model performance metrics
- ✅ ROI calculations
- ✅ PropsPerformance dashboard populated

---

## Estimated Work

**Quick Fix (Option 1)**:
- Code updates: 1 hour
- Testing: 1 hour
- Deployment: 15 minutes
- Verification: 24 hours (wait for next cron run)
- **Total**: 2-3 hours + 1 day monitoring

**Proper Solution**:
- Rewrite grading logic: 2 hours
- Add error handling: 1 hour
- Comprehensive testing: 2 hours
- Documentation: 30 minutes
- **Total**: 5-6 hours

---

## Next Steps

1. **Immediate**: Document findings (DONE - this file)
2. **Today**: Continue with odds scraper investigation
3. **Tomorrow**: Fix props grading system
4. **Day 3**: Verify grading works after cron run

---

**Created**: December 4, 2025
**Status**: Documented, ready for implementation
**Assigned**: Pending developer availability
