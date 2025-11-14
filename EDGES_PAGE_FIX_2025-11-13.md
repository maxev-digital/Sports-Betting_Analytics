# Edges Page Fix - Complete Investigation & Resolution
## Date: November 13, 2025, 6:45 AM CST

---

## 🔍 Investigation Summary

### Initial Complaint
- Edges page showing only NCAAF predictions
- Previous days' games showing instead of upcoming games
- All sports were working "at one point but things keep getting broken"

### Root Cause Discovery Chain

**Problem 1: Local vs VPS Data Mismatch**
- Frontend was configured to use `localhost:8000` in development
- Local backend had OLD prediction files (Nov 10-11 - 3 days old)
- All predictions in local files were for games that already played
- Edge scanner filters out old games → No edges displayed

**Problem 2: Prediction Generation Stopped**
- VPS predictions also stale (last updated Oct 25)
- Cron jobs were scheduled but prediction runner script had bugs
- Script used RELATIVE PATHS instead of absolute paths
- Subprocess couldn't find scripts → Silent failures

**Problem 3: Prediction Format Mismatch**
- When prediction script DOES run, it saves in wrong CSV format
- Expected: `prediction_id,date_predicted,game_date,game_time,SPORT,away_team,home_team,bet_type...`
- Actual: `prediction_id,date_predicted,game_date,game_time,away_team,home_team,...,SPORT,bet_type...` (sport in wrong column)
- **CRITICAL:** Sport column is EMPTY in new predictions
- Edge scanner reads sport column to filter → Empty = filtered out → 0 edges displayed

---

## ✅ What's Working Now

### 1. VPS Backend API
**Status:** ✅ FULLY OPERATIONAL
- Running at https://max-ev-sports.com/api
- Model Performance API working perfectly
- All 5 sports data available (NBA, NCAAB, NHL, NFL, NCAAF)
- 1,155 total predictions tracked
- 55.4% win rate, +5.34% ROI

**Test Results:**
```bash
curl https://max-ev-sports.com/api/model-performance/overview?days=7
# Returns: 1155 predictions, all 5 sports present
```

### 2. Frontend Configuration
**Status:** ✅ FIXED
**File:** `C:\Users\nashr\frontend\src\config.ts`
**Change:** Set to ALWAYS use VPS backend (removed localhost switching)

```typescript
// BEFORE (broken):
export const API_BASE_URL = isDevelopment
  ? 'http://localhost:8000/api'  // ❌ Used stale local data
  : 'https://max-ev-sports.com/api';

// AFTER (fixed):
export const API_BASE_URL = 'https://max-ev-sports.com/api'; // ✅ Always VPS
```

### 3. Prediction Runner Script
**Status:** ✅ FIXED (absolute paths)
**File:** `C:\Users\nashr\backend\run_predictions_and_log.py`

**Changes Made:**
- ✅ Changed to absolute paths: `BASE_DIR = Path("/root/sporttrader/backend")`
- ✅ Added support for all 5 sports (was only NBA/NCAAB)
- ✅ Fixed subprocess calls with full paths
- ✅ Fixed log directory paths

**Test Result:**
```bash
ssh root@148.230.87.135 "cd /root/sporttrader/backend && python3 run_predictions_and_log.py --sport nba"
# Output: ✅ COMPLETE: NBA predictions generated and logged
# Logged 18 new predictions
```

### 4. Cron Schedule
**Status:** ✅ OPTIMIZED for 5 AM CST readiness

**Schedule (UTC times, VPS timezone):**
```cron
# Midnight CST (6 AM UTC) - Grade yesterday's results
0 6 * * * record_daily_results.py

# 1:00-1:30 AM CST (7:00-7:30 UTC) - Scrape fresh data
0 7 * * * run_all_scrapers.py
30 7 * * * run_kenpom_scraper.py

# 2:00-3:00 AM CST (8:00-9:00 UTC) - Generate predictions (STAGGERED)
0 8 * * * run_predictions_and_log.py --sport nba
15 8 * * * run_predictions_and_log.py --sport ncaab
30 8 * * * run_predictions_and_log.py --sport nhl
45 8 * * * run_predictions_and_log.py --sport nfl
0 9 * * * run_predictions_and_log.py --sport ncaaf

# RESULT: Everything ready by 5 AM CST
```

### 5. Prediction Generation Script
**Status:** ✅ WORKS but saves in wrong format
**File:** `/root/sporttrader/backend/generate_all_sport_predictions.py`

**Test Run (manual):**
```bash
python3 generate_all_sport_predictions.py --sport nba
# Output:
# Found 121 total games
# Sports: NBA: 8, NFL: 29, NCAAF: 57, NHL: 11, NCAAB: 16
# Generated 121 predictions
# High confidence: 22, Medium: 26, Low: 22
# Recommended bets: 70
```

Script successfully:
- ✅ Fetches upcoming games from API
- ✅ Generates predictions for all 5 sports
- ✅ Calculates edges and confidence levels
- ✅ Saves to predictions_log.csv

---

## ❌ What's Still Broken

### Edges Page Shows 0 Plays

**File:** `/root/sporttrader/backend/routes/edge_scanner.py`
- Reads from: `predictions_log_multi_bet.csv`
- Filters by sport column

**Problem:** Prediction CSV format mismatch

**Expected Format (by edge_scanner.py):**
```csv
prediction_id,date_predicted,game_date,game_time,sport,away_team,home_team,bet_type,model,predicted_value,market_value,edge,recommendation,confidence,bet_placed
NBA_20251114_...,2025-11-13 12:00:00,2025-11-14,07:00 PM,NBA,Team A,Team B,TOTALS,xgboost,230.5,228.0,2.5,OVER,MEDIUM,YES
```

**Actual Format (from generate_all_sport_predictions.py):**
```csv
prediction_id,date_predicted,game_date,game_time,away_team,home_team,predicted_total,market_total,edge,recommendation,confidence,bet_placed,sport,bet_type,predicted_value,market_value
2025-11-14_Team_A_Team_B,2025-11-13 12:00:00,2025-11-14,07:00 PM,Team A,Team B,230.5,228.0,2.5,OVER,MEDIUM,YES,,,,
```

**Issues:**
1. ❌ Column order different (sport at position 13 instead of 5)
2. ❌ Sport column is EMPTY (no value)
3. ❌ Missing bet_type column value
4. ❌ Missing model column
5. ❌ predicted_total/market_total instead of predicted_value/market_value

**Impact:**
- Edge scanner reads row, finds empty sport → filters out
- All 121 fresh predictions filtered out
- API returns: `{"total_plays": 0, "plays": []}`
- Frontend shows: "No edges found"

---

## 📋 The Proper Fix Plan

### Step 1: Fix Prediction Script Format
**File:** `/root/sporttrader/backend/generate_all_sport_predictions.py`

**Changes Needed:**
1. Update CSV column order to match expected format
2. Populate sport field in prediction dictionary
3. Add bet_type field (defaults to 'TOTALS' for now)
4. Add model field (defaults to 'ensemble' for now)
5. Use predicted_value/market_value instead of predicted_total/market_total
6. Save to BOTH predictions_log.csv AND predictions_log_multi_bet.csv

**Code Changes:**
```python
# Current (line ~150):
prediction = {
    'prediction_id': pred_id,
    'date_predicted': timestamp,
    'game_date': game_date,
    'game_time': game_time_str,
    'away_team': away_team,
    'home_team': home_team,
    'predicted_total': predicted_total,
    'market_total': market_total,
    'edge': edge,
    'recommendation': recommendation,
    'confidence': confidence,
    'bet_placed': bet_placed
}

# Fixed:
prediction = {
    'prediction_id': pred_id,
    'date_predicted': timestamp,
    'game_date': game_date,
    'game_time': game_time_str,
    'sport': sport.upper(),  # ✅ ADD SPORT
    'away_team': away_team,
    'home_team': home_team,
    'bet_type': 'TOTALS',  # ✅ ADD BET_TYPE
    'model': 'ensemble',  # ✅ ADD MODEL
    'predicted_value': predicted_total,  # ✅ RENAME
    'market_value': market_total,  # ✅ RENAME
    'edge': edge,
    'recommendation': recommendation,
    'confidence': confidence,
    'bet_placed': bet_placed
}
```

### Step 2: Update Prediction Runner
**File:** `/root/sporttrader/backend/run_predictions_and_log.py`

**Changes:**
- Ensure it calls generate_all_sport_predictions.py correctly
- Verify it checks for both prediction files

### Step 3: Regenerate Fresh Predictions
**Commands:**
```bash
# Generate for all sports
python3 generate_all_sport_predictions.py --sport nba
python3 generate_all_sport_predictions.py --sport nfl
python3 generate_all_sport_predictions.py --sport ncaaf
python3 generate_all_sport_predictions.py --sport nhl
python3 generate_all_sport_predictions.py --sport ncaab
```

### Step 4: Deploy Frontend Changes
**Commands:**
```bash
cd /c/Users/nashr/frontend
npm run build
# Deploy dist/ to VPS
```

### Step 5: Verify Everything
**Tests:**
1. Check predictions_log_multi_bet.csv has correct format
2. Test edge scanner API returns plays
3. Check frontend displays edges
4. Verify all 5 sports showing
5. Test Model Performance page

---

## 📊 Expected Results After Fix

### Edges API Response:
```bash
curl "https://max-ev-sports.com/api/edge-scanner/best-plays?sport=all"
```

**Expected:**
```json
{
  "total_plays": 70,
  "plays": [
    {
      "sport": "NBA",
      "away": "Atlanta Hawks",
      "home": "Utah Jazz",
      "game_date": "2025-11-14",
      "edge": 7.2,
      "confidence": "HIGH",
      "recommendation": "OVER",
      "predicted_value": 240.3,
      "market_value": 233.1
    },
    ...
  ]
}
```

### Edges Page:
- Display 70+ recommended bets
- All 5 sports visible
- Today and this week's games only
- High/Medium/Low confidence filters working
- No old games displayed

### Model Performance Page:
- Already working
- Shows all 5 sports
- 1,155+ predictions
- Win rates by sport/model/confidence

---

## 🔧 Files Modified in This Session

### Frontend Files:
1. **`frontend/src/config.ts`** - Changed to always use VPS backend
   - Line 12: `export const API_BASE_URL = 'https://max-ev-sports.com/api';`

### Backend Files (need to deploy):
2. **`backend/run_predictions_and_log.py`** - Fixed absolute paths, added all 5 sports
   - Lines 26-28: Absolute path configuration
   - Lines 42-92: Updated run_ml_predictions function
   - Line 192: Added all 5 sports to choices

### VPS Files:
3. **`/root/sporttrader/backend/run_predictions_and_log.py`** - Deployed fixed version
4. **`/tmp/new_crontab.txt`** - New optimized schedule (installed)

### Files TO BE Modified:
5. **`backend/generate_all_sport_predictions.py`** - Fix CSV format (NEXT STEP)

---

## 🎯 Success Criteria

After completing Option A fix, verify:

✅ **Edges Page:**
- Shows 50+ upcoming games across all 5 sports
- No games that already happened
- Confidence filters work
- Sport filters work
- All data from VPS (not localhost)

✅ **Model Performance:**
- Shows all 5 sports
- Previous day's results visible
- Charts updating daily
- ROI calculations correct

✅ **Automated Daily Workflow:**
- 12:00 AM CST: Results graded
- 1:00 AM CST: Data scraped
- 2:00-3:00 AM CST: Predictions generated
- 5:00 AM CST: Everything ready for user

✅ **Monday Weekly Retraining:**
- 87 ML models retrain with last week's data
- Improved models deployed automatically

---

## 📝 Next Session Checklist

Before closing the session, verify:
- [ ] generate_all_sport_predictions.py fixed and tested
- [ ] Fresh predictions generated for all 5 sports
- [ ] predictions_log_multi_bet.csv has correct format
- [ ] Edge scanner API returns plays
- [ ] Frontend deployed to VPS
- [ ] Edges page displays games
- [ ] Model Performance page working
- [ ] All changes committed to git
- [ ] Documentation updated

---

## 🚀 Long-term Improvements Needed

1. **Better Error Logging:** Cron jobs failing silently - add email alerts
2. **ML Model Integration:** Currently using simple heuristics - integrate real 87 ML models
3. **Real-time Data:** Add live game data updates during games
4. **Monitoring Dashboard:** Track prediction generation success/failure
5. **Automated Testing:** Add integration tests for prediction pipeline
6. **Data Validation:** Verify prediction format before saving

---

## 📞 Contact & Support

**VPS Access:**
- Host: 148.230.87.135
- SSH: `ssh -i ~/.ssh/hostinger_vps root@148.230.87.135`
- Backend: `/root/sporttrader/backend/`
- Logs: `/root/sporttrader/backend/logs/`

**Frontend:**
- Dev: http://localhost:5173 (always uses VPS backend now)
- Prod: https://max-ev-sports.com

**Key Endpoints:**
- Games: https://max-ev-sports.com/api/games
- Edges: https://max-ev-sports.com/api/edge-scanner/best-plays
- Performance: https://max-ev-sports.com/api/model-performance/overview

---

**Status:** Documentation complete. Ready to proceed with Option A fix.
**Estimated Time:** 30-45 minutes
**Next Step:** Fix generate_all_sport_predictions.py CSV format
