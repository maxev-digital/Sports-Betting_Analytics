# ⚠️ CRITICAL FIXES - DO NOT CHANGE ⚠️

**Last Updated:** November 13, 2025 8:55 AM CST
**Status:** ALL FIXES VERIFIED WORKING IN PRODUCTION
**VPS:** 148.230.87.135

---

## 🚨 PROTECTED CODE - DO NOT MODIFY WITHOUT USER APPROVAL 🚨

This document lists code that has been fixed and is currently working correctly in production.
**DO NOT change these sections unless explicitly requested by the user.**

---

## 1. Edge Scanner Sport Filtering (CRITICAL)

**File:** `/root/sporttrader/backend/routes/edge_scanner.py`
**Line:** ~597
**Status:** ✅ WORKING - Fixed Nov 13, 2025

### ✅ CORRECT CODE (DO NOT CHANGE):
```python
# Filter by sport (if not "all")
if sport and sport.lower() != 'all':  # ✅ CHECK FOR "all" BEFORE FILTERING
    all_plays = [p for p in all_plays if p['sport'].lower() == sport.lower()]
```

### ❌ BROKEN CODE (NEVER USE THIS):
```python
# BROKEN - filters out everything when sport="all"
if sport:  # ❌ NO CHECK FOR "all"
    all_plays = [p for p in all_plays if p['sport'].lower() == sport.lower()]
```

**Why This Matters:**
- Frontend calls API with `sport="all"` to show all sports
- Without the `!= 'all'` check, it filters for plays where sport field equals the string "all"
- This returns 0 plays even though we have 50+ predictions
- **Symptom:** Edges page shows "No plays found" despite having data

**Test Command:**
```bash
curl -s "https://max-ev-sports.com/api/edges/plays?sport=all&limit=10" | grep -o '"total_plays":[0-9]*'
# Should return: "total_plays":50+ (NOT 0)
```

---

## 2. Model Performance Merge Strategy (CRITICAL)

**File:** `/root/sporttrader/backend/routes/model_performance.py`
**Line:** ~73
**Status:** ✅ WORKING - Fixed Nov 13, 2025

### ✅ CORRECT CODE (DO NOT CHANGE):
```python
# Merge predictions with results using UNIQUE prediction_id
results_cols_to_keep = ['prediction_id', 'away_score', 'home_score', 'actual_total', 'result', 'profit_loss']
results_df_clean = results_df[results_cols_to_keep].drop_duplicates()

merged_df = predictions_df.merge(
    results_df_clean,
    on='prediction_id',  # ✅ USE UNIQUE IDENTIFIER
    how='inner'
)
```

### ❌ BROKEN CODE (NEVER USE THIS):
```python
# BROKEN - creates cartesian product (1,155 predictions → 4,983 duplicates)
merged_df = predictions_df.merge(
    results_df_clean,
    on=['game_date_only', 'away_team_normalized', 'home_team_normalized'],  # ❌ NOT UNIQUE
    how='inner'
)
```

**Why This Matters:**
- Merging on game details (date + teams) creates multiple matches per prediction
- Example: 5 predictions for 1 game × 5 results = 25 duplicate matches
- This inflates 1,155 real predictions into 4,983 artificial records
- **Symptom:** Win rate shows 50% instead of 55.4%, ROI shows -3.1% instead of +5.34%

**Verification:**
```python
print(f"Predictions: {len(predictions_df)}")  # Should be 1,155
print(f"Results: {len(results_df_clean)}")     # Should be 1,155
print(f"Merged: {len(merged_df)}")            # Should be 1,155 (NOT 4,983)
```

---

## 3. Charts Display Cumulative (Not Daily Snapshots)

**File:** `/root/sporttrader/backend/routes/model_performance.py`
**Line:** ~250
**Status:** ✅ WORKING - Fixed Nov 13, 2025

### ✅ CORRECT CODE (DO NOT CHANGE):
```python
# Calculate CUMULATIVE performance over time
cumulative_wins = 0
cumulative_losses = 0
cumulative_profit = 0
cumulative_bets = 0

for day in sorted(merged_df['day'].unique()):
    day_df = merged_df[merged_df['day'] == day]
    day_wins = len(day_df[day_df['result'] == 'WIN'])
    day_losses = len(day_df[day_df['result'] == 'LOSS'])
    day_profit = day_df['profit_loss'].sum()

    # ADD to cumulative totals (running total)
    cumulative_wins += day_wins
    cumulative_losses += day_losses
    cumulative_bets += len(day_df)
    cumulative_profit += day_profit

    # Calculate cumulative metrics
    cumulative_total = cumulative_wins + cumulative_losses
    cumulative_win_rate = cumulative_wins / cumulative_total if cumulative_total > 0 else 0
    cumulative_roi = (cumulative_profit / cumulative_bets) * 100 if cumulative_bets > 0 else 0

    history_data.append({
        'period': day,
        'predictions': cumulative_bets,      # ✅ Running total
        'wins': cumulative_wins,             # ✅ Running total
        'win_rate': cumulative_win_rate,     # ✅ Cumulative percentage
        'roi': cumulative_roi,               # ✅ Cumulative ROI
        'units_won': cumulative_profit       # ✅ Running profit
    })
```

### ❌ BROKEN CODE (NEVER USE THIS):
```python
# BROKEN - shows daily snapshots (misleading downward trend)
for day in sorted(merged_df['day'].unique()):
    day_df = merged_df[merged_df['day'] == day]
    day_wins = len(day_df[day_df['result'] == 'WIN'])
    day_total = len(day_df[day_df['result'].isin(['WIN', 'LOSS'])])
    day_win_rate = day_wins / day_total if day_total > 0 else 0  # ❌ That day only
    day_roi = (day_df['profit_loss'].sum() / len(day_df)) * 100  # ❌ That day only

    history_data.append({
        'period': day,
        'win_rate': day_win_rate,  # ❌ Daily snapshot
        'roi': day_roi             # ❌ Daily snapshot
    })
```

**Why This Matters:**
- Daily snapshots show: Nov 10 (70% WR) → Nov 11 (58% WR) → Nov 12 (51% WR) = looks like decline
- Daily ROI shows: Nov 10 (+33%) → Nov 11 (+11%) → Nov 12 (-1.6%) = goes NEGATIVE
- Cumulative shows: Nov 10 (70% WR) → Nov 11 (59.4% WR) → Nov 12 (55.4% WR) = stabilizing
- Cumulative ROI: Nov 10 (+32.9%) → Nov 11 (+12.5%) → Nov 12 (+5.3%) = stays POSITIVE
- **Symptom:** Charts show decline when we're actually profitable

**Expected Output:**
```json
{
  "history": [
    {"period": "2025-11-10", "predictions": 41, "wins": 28, "win_rate": 0.70, "roi": 32.88},
    {"period": "2025-11-11", "predictions": 568, "wins": 312, "win_rate": 0.5943, "roi": 12.49},
    {"period": "2025-11-12", "predictions": 1155, "wins": 592, "win_rate": 0.5538, "roi": 5.34}
  ]
}
```

---

## 4. Frontend Always Uses VPS API (Not Localhost)

**File:** `C:/Users/nashr/frontend/src/config.ts`
**Status:** ✅ WORKING - Fixed Nov 13, 2025

### ✅ CORRECT CODE (DO NOT CHANGE):
```typescript
// ALWAYS use production VPS API (never localhost)
export const API_BASE_URL = 'https://max-ev-sports.com/api';

// DO NOT use this:
// const isDevelopment = process.env.NODE_ENV === 'development';
// export const API_BASE_URL = isDevelopment
//   ? 'http://localhost:8000/api'  // ❌ BROKEN - uses stale local data
//   : 'https://max-ev-sports.com/api';
```

**Why This Matters:**
- Local backend has old data (Nov 10-11)
- VPS backend has current data (Nov 10-12+)
- Using localhost causes frontend to show stale/missing data
- **Symptom:** Production site shows different data than VPS has

---

## 5. Time Range Filter Applied to All Sections

**File:** `C:/Users/nashr/frontend/src/pages/ModelPerformance.tsx`
**Line:** 141
**Status:** ✅ WORKING - Fixed Nov 13, 2025

### ✅ CORRECT CODE (DO NOT CHANGE):
```typescript
// Fetch predictions table with DYNAMIC days parameter
const predictionsParams = new URLSearchParams({
  days: days.toString(),  // ✅ Uses state variable (changes with dropdown)
  limit: '50'
});
if (selectedSport !== 'all') predictionsParams.append('sport', selectedSport);
if (selectedModel !== 'all') predictionsParams.append('model', selectedModel);
if (selectedBetType !== 'all') predictionsParams.append('bet_type', selectedBetType);

const predictionsResponse = await fetch(
  `${API_BASE_URL}/model-performance/predictions?${predictionsParams}`
);
```

### ❌ BROKEN CODE (NEVER USE THIS):
```typescript
// BROKEN - predictions always show 7 days regardless of dropdown
const predictionsParams = new URLSearchParams({
  days: '7',  // ❌ HARDCODED - ignores time range dropdown
  limit: '50'
});
```

**Why This Matters:**
- Time range dropdown didn't affect predictions table
- Summary cards and charts would update, but table stayed the same
- **Symptom:** Changing time range dropdown does nothing to predictions table

---

## 6. Charts Display Above Results Table

**File:** `C:/Users/nashr/frontend/src/pages/ModelPerformance.tsx`
**Lines:** 289-363
**Status:** ✅ WORKING - Fixed Nov 13, 2025

### ✅ CORRECT ORDER (DO NOT CHANGE):
```tsx
{/* 1. Summary Cards */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
  {/* Win Rate, ROI, Predictions, Avg Edge cards */}
</div>

{/* 2. CHARTS - Above table */}
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
  {/* Win Rate Over Time chart */}
  {/* ROI Over Time chart */}
</div>

{/* 3. PREDICTIONS TABLE - Below charts */}
{predictions.length > 0 && (
  <div className="bg-slate-900 border-2 border-slate-700 rounded-lg p-6 mb-8">
    <h3>Recent Predictions</h3>
    <table>...</table>
  </div>
)}

{/* 4. Breakdown Tables */}
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
  {/* By Confidence, By Sport, By Model */}
</div>
```

**Why This Matters:**
- Charts show high-level trends (most important visualization)
- Individual predictions are details (less important, below charts)
- User requested: "move the charts above the results table"

---

## 7. Prediction CSV Format (MUST Include sport, bet_type, model)

**File:** `/root/sporttrader/backend/generate_all_sport_predictions.py`
**Lines:** 108-124
**Status:** ✅ WORKING - Fixed Nov 13, 2025

### ✅ CORRECT FORMAT (DO NOT CHANGE):
```python
prediction = {
    'prediction_id': f"{sport.upper()}_{game_date.replace('-', '')}_{away_team.replace(' ', '_')}_{home_team.replace(' ', '_')}_TOTALS",
    'date_predicted': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'game_date': game_date,
    'game_time': game_time_str,
    'sport': sport.upper(),           # ✅ REQUIRED - Frontend filters by this
    'away_team': away_team,
    'home_team': home_team,
    'bet_type': 'TOTALS',            # ✅ REQUIRED - Frontend filters by this
    'model': 'ensemble',              # ✅ REQUIRED - Frontend filters by this
    'predicted_value': round(predicted_total, 1),  # ✅ Renamed from predicted_total
    'market_value': market_total,     # ✅ Renamed from market_total
    'edge': round(edge, 1),
    'recommendation': recommendation,
    'confidence': confidence,
    'bet_placed': bet_placed
}
```

### ❌ BROKEN FORMAT (NEVER USE THIS):
```python
# BROKEN - missing sport, bet_type, model fields
prediction = {
    'prediction_id': '...',
    'game_date': game_date,
    'away_team': away_team,
    'home_team': home_team,
    'predicted_total': predicted_total,  # ❌ Wrong field name
    'market_total': market_total,        # ❌ Wrong field name
    # ❌ Missing: sport, bet_type, model
}
```

**Why This Matters:**
- Edge scanner filters by sport - without sport field, filtering breaks
- Model performance page filters by model and bet_type
- Frontend expects `predicted_value` and `market_value` (not `predicted_total`/`market_total`)
- **Symptom:** Filtering returns 0 results, or "sport field missing" errors

---

## 📋 Verification Checklist

After any code changes, verify these endpoints return correct data:

### 1. Edge Scanner - All Sports
```bash
curl -s "https://max-ev-sports.com/api/edges/plays?sport=all&limit=5" | python -m json.tool | head -20
# Should show: total_plays > 0, multiple sports
```

### 2. Model Performance - Summary
```bash
curl -s "https://max-ev-sports.com/api/model-performance/summary?days=30" | python -m json.tool
# Should show: total_predictions=1155, win_rate≈0.554, roi≈5.34
```

### 3. Model Performance - History (Cumulative)
```bash
curl -s "https://max-ev-sports.com/api/model-performance/history?days=30" | python -m json.tool
# Should show 3 days with INCREASING predictions count (41 → 568 → 1155)
```

### 4. Model Performance - Predictions Table
```bash
curl -s "https://max-ev-sports.com/api/model-performance/predictions?days=7&limit=10" | python -m json.tool | head -30
# Should show: individual predictions with game details and results
```

### 5. NHL Performance (Sport Filter)
```bash
curl -s "https://max-ev-sports.com/api/model-performance/summary?sport=nhl&days=30" | python -m json.tool
# Should show: total_predictions=132, win_rate≈0.653, roi≈23.27
```

---

## 🎯 Expected Performance Metrics (As of Nov 13, 2025)

**Overall (3 Days - Nov 10-12):**
- Total Predictions: 1,155
- Record: 592W - 477L - 1P - 85 UNKNOWN
- Win Rate: 55.38%
- ROI: +5.34%
- Profit: +61.72 units

**By Sport:**
- **NHL:** 132 predictions, 65.3% WR, +23.3% ROI 🔥
- **NFL:** 15 predictions, 80.0% WR
- **NCAAB:** 867 predictions, 53.7% WR
- **NBA:** 141 predictions, 53.2% WR
- **NCAAF:** 0 predictions (system started Nov 10 Sunday, NCAAF plays Saturdays)

**Cumulative Chart Data:**
- Day 1 (Nov 10): 41 predictions, 70% WR, +32.9% ROI
- Day 2 (Nov 11): 568 predictions cumulative, 59.4% WR, +12.5% ROI
- Day 3 (Nov 12): 1,155 predictions cumulative, 55.4% WR, +5.3% ROI

If these numbers don't match, something broke.

---

## 🚨 Common Breaking Scenarios

### Scenario 1: Edge Scanner Returns 0 Plays
**Cause:** Missing `sport.lower() != 'all'` check in edge_scanner.py line 597
**Fix:** Add the check back (see Section 1)

### Scenario 2: Model Performance Shows Wrong Metrics
**Cause:** Merging on game details instead of prediction_id
**Fix:** Change merge to use prediction_id only (see Section 2)

### Scenario 3: Charts Show Downward Trend
**Cause:** Using daily snapshots instead of cumulative totals
**Fix:** Restore cumulative calculation (see Section 3)

### Scenario 4: Frontend Shows Old Data
**Cause:** config.ts using localhost instead of VPS
**Fix:** Set API_BASE_URL to 'https://max-ev-sports.com/api' (see Section 4)

### Scenario 5: Time Range Filter Doesn't Work
**Cause:** Hardcoded days: '7' in predictions fetch
**Fix:** Change to days: days.toString() (see Section 5)

---

## 📝 Change Log

**Nov 13, 2025 8:55 AM CST:**
- Created this document to protect working code
- All 7 critical fixes documented
- Verification checklist added
- Expected metrics recorded

**Future Changes:**
- DO NOT modify protected sections without documenting here first
- ADD new critical fixes to this document when made
- UPDATE expected metrics as more data accumulates
- VERIFY all endpoints still work after any changes

---

## ⚠️ FINAL WARNING

**If you are a future Claude session reading this:**

The code sections marked ✅ CORRECT CODE in this document are **WORKING IN PRODUCTION** and have been **VERIFIED BY THE USER**.

**DO NOT:**
- "Optimize" or "improve" these sections
- Change merge strategies
- Change calculation methods
- Change API URLs
- Modify filtering logic
- Reorder UI components

**Unless the user explicitly requests a change.**

The user has experienced multiple instances of "fixes" that broke working code.
**Stability > Optimization**

If you think something needs to be changed, **ASK THE USER FIRST** before making any modifications.
