# Quick Troubleshooting Guide

**Last Updated:** November 13, 2025
**VPS:** 148.230.87.135

---

## 🚨 Something Broke? Start Here

### Step 1: Check Which Page Has Issues

**Edges Page (max-ev-sports.com/edges):**
- Shows 0 plays? → Jump to [Section A](#section-a-edges-page-shows-0-plays)
- Only showing one sport? → Jump to [Section B](#section-b-edges-showing-wrong-sport)
- Old/played games showing? → Jump to [Section C](#section-c-old-games-showing)

**Model Performance Page (max-ev-sports.com/model-performance):**
- Shows 0 results? → Jump to [Section D](#section-d-model-performance-shows-0-results)
- Wrong metrics (50% WR instead of 55%)? → Jump to [Section E](#section-e-wrong-performance-metrics)
- Charts show decline? → Jump to [Section F](#section-f-charts-show-misleading-decline)
- Time range filter not working? → Jump to [Section G](#section-g-time-range-filter-broken)

**Frontend Shows Old Data:**
- Jump to [Section H](#section-h-frontend-shows-stale-data)

---

## Section A: Edges Page Shows 0 Plays

**Symptom:** API returns `{"total_plays": 0}` despite having predictions

**Test:**
```bash
curl -s "https://max-ev-sports.com/api/edges/plays?sport=all&limit=5" | grep total_plays
# Should show: "total_plays": 50+ (NOT 0)
```

**Most Likely Cause:** Missing `!= 'all'` check in sport filter

**File:** `/root/sporttrader/backend/routes/edge_scanner.py` line ~597

**Check:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "grep -A2 'if sport' /root/sporttrader/backend/routes/edge_scanner.py | grep 'all'"
```

**Should see:**
```python
if sport and sport.lower() != "all":  # ✅ Correct
```

**If you see:**
```python
if sport:  # ❌ Broken - missing "all" check
```

**Fix:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "sed -i 's/if sport:/if sport and sport.lower() != \"all\":/' /root/sporttrader/backend/routes/edge_scanner.py"
# Restart API
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"
```

**Reference:** CRITICAL_FIXES_DO_NOT_CHANGE.md Section 1

---

## Section B: Edges Showing Wrong Sport

**Symptom:** Only NCAAF showing (or only one sport)

**Test:**
```bash
curl -s "https://max-ev-sports.com/api/edges/plays?sport=all&limit=20" | grep -o '"sport":"[A-Z]*"' | sort -u
# Should show: "sport":"NBA", "sport":"NCAAB", "sport":"NHL", etc.
```

**Most Likely Cause:** CSV predictions missing sport field

**Check:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "head -2 /root/sporttrader/backend/data/tracking/predictions_log_multi_bet.csv"
# Should have "sport" column in header
```

**Fix:** Regenerate predictions with correct format
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader/backend && /root/sporttrader/venv/bin/python generate_all_sport_predictions.py"
```

**Reference:** CRITICAL_FIXES_DO_NOT_CHANGE.md Section 7

---

## Section C: Old Games Showing

**Symptom:** Games from yesterday or earlier still appearing in edges

**Most Likely Cause:** Predictions CSV includes games that already completed

**Fix:** Predictions are filtered by game_date + game_time client-side. Check if system clock is correct:
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "date"
# Should match current CST time
```

If clock is wrong:
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "timedatectl set-timezone America/Chicago"
```

---

## Section D: Model Performance Shows 0 Results

**Symptom:** "No completed predictions in selected timeframe"

**Test:**
```bash
curl -s "https://max-ev-sports.com/api/model-performance/summary?days=30" | grep total_predictions
# Should show: "total_predictions": 1155+
```

**Most Likely Cause:** Merge strategy broken (using game details instead of prediction_id)

**File:** `/root/sporttrader/backend/routes/model_performance.py` line ~76

**Check:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "grep -A3 'merged_df = predictions_df.merge' /root/sporttrader/backend/routes/model_performance.py | head -5"
```

**Should see:**
```python
merged_df = predictions_df.merge(
    results_df_clean,
    on='prediction_id',  # ✅ Correct - unique identifier
    how='inner'
)
```

**If you see `on=['game_date', 'teams']` or similar:** That's the bug.

**Reference:** CRITICAL_FIXES_DO_NOT_CHANGE.md Section 2

---

## Section E: Wrong Performance Metrics

**Symptom:**
- Total predictions shows 4,983 instead of 1,155
- Win rate shows 50% instead of 55.4%
- ROI shows -3.1% instead of +5.34%

**Same as Section D** - Merge creating duplicates

**Verify:**
```bash
curl -s "https://max-ev-sports.com/api/model-performance/summary?days=30" | python -m json.tool
# Check:
# total_predictions: should be 1155 (NOT 4983)
# win_rate: should be ~0.554 (NOT ~0.50)
# roi: should be ~5.34 (NOT negative)
```

**Reference:** CRITICAL_FIXES_DO_NOT_CHANGE.md Section 2

---

## Section F: Charts Show Misleading Decline

**Symptom:**
- Win rate chart: 70% → 58% → 51% (looks like decline)
- ROI chart: +33% → +11% → -1.6% (goes negative!)

**Test:**
```bash
curl -s "https://max-ev-sports.com/api/model-performance/history?days=30" | python -m json.tool
# Check predictions field:
# Day 1: should be 41
# Day 2: should be 568 (cumulative, NOT 527)
# Day 3: should be 1155 (cumulative, NOT 587)
```

**If Day 2 shows 527 and Day 3 shows 587:** Using daily snapshots instead of cumulative

**Most Likely Cause:** History calculation using daily snapshots instead of cumulative totals

**File:** `/root/sporttrader/backend/routes/model_performance.py` line ~234

**Check:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "grep -A5 'cumulative_wins = 0' /root/sporttrader/backend/routes/model_performance.py | head -7"
```

**Should see:**
```python
cumulative_wins = 0
cumulative_losses = 0
cumulative_profit = 0
cumulative_bets = 0
```

**Reference:** CRITICAL_FIXES_DO_NOT_CHANGE.md Section 3

---

## Section G: Time Range Filter Broken

**Symptom:** Changing "Last 7 Days" / "Last 30 Days" dropdown doesn't update data

**File:** `C:/Users/nashr/frontend/src/pages/ModelPerformance.tsx` line ~141

**Check locally:**
```bash
grep "days:" frontend/src/pages/ModelPerformance.tsx | grep "predictionsParams"
```

**Should see:**
```typescript
days: days.toString(),  // ✅ Uses state variable
```

**If you see:**
```typescript
days: '7',  // ❌ Hardcoded
```

**Fix:**
```typescript
const predictionsParams = new URLSearchParams({
  days: days.toString(),  // Change to use state variable
  limit: '50'
});
```

**Reference:** CRITICAL_FIXES_DO_NOT_CHANGE.md Section 5

---

## Section H: Frontend Shows Stale Data

**Symptom:**
- Production site shows old data
- Local data different from VPS data
- Edges showing games from 2 days ago

**Most Likely Cause:** Frontend using localhost API instead of VPS

**File:** `C:/Users/nashr/frontend/src/config.ts`

**Check:**
```bash
grep "API_BASE_URL" frontend/src/config.ts
```

**Should see:**
```typescript
export const API_BASE_URL = 'https://max-ev-sports.com/api';
```

**If you see conditional with `isDevelopment` or `localhost`:** That's the bug

**Fix:**
```typescript
// Remove any conditional logic
export const API_BASE_URL = 'https://max-ev-sports.com/api';
```

**Then rebuild and deploy:**
```bash
cd frontend
npm run build
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "rm -rf /var/www/sporttrader/*"
scp -i ~/.ssh/hostinger_vps -r dist/* root@148.230.87.135:/var/www/sporttrader/
```

**Reference:** CRITICAL_FIXES_DO_NOT_CHANGE.md Section 4

---

## 📊 Expected Metrics (As of Nov 13, 2025)

Use these to verify the system is working correctly:

**Overall (3 Days):**
- Total Predictions: 1,155
- Win Rate: 55.38%
- ROI: +5.34%
- Record: 592W - 477L - 1P

**By Sport:**
- NHL: 132 preds, 65.3% WR, +23.3% ROI
- NFL: 15 preds, 80.0% WR
- NCAAB: 867 preds, 53.7% WR
- NBA: 141 preds, 53.2% WR
- NCAAF: 0 (system started Sunday Nov 10, NCAAF plays Saturdays)

**Cumulative History:**
```json
{
  "history": [
    {"period": "2025-11-10", "predictions": 41, "wins": 28, "win_rate": 0.70, "roi": 32.88},
    {"period": "2025-11-11", "predictions": 568, "wins": 312, "win_rate": 0.5943, "roi": 12.49},
    {"period": "2025-11-12", "predictions": 1155, "wins": 592, "win_rate": 0.5538, "roi": 5.34}
  ]
}
```

**If numbers don't match:** Something broke. Compare to CRITICAL_FIXES_DO_NOT_CHANGE.md

---

## 🔧 Emergency Recovery

### Nuclear Option: Restore All Critical Files from Backup

If everything is broken and you can't figure out what changed:

```bash
# 1. Check git log for recent changes
cd /root/sporttrader
git log --oneline -10

# 2. Restore specific files from last known good commit
git checkout <commit-hash> -- backend/routes/edge_scanner.py
git checkout <commit-hash> -- backend/routes/model_performance.py

# 3. Restart API
systemctl restart sporttrader

# 4. Verify endpoints
curl -s "https://max-ev-sports.com/api/edges/plays?sport=all&limit=5" | grep total_plays
curl -s "https://max-ev-sports.com/api/model-performance/summary?days=30" | grep win_rate
```

### Contact User

If you can't fix it and need help:
1. Document what broke (which endpoint/page)
2. Document what you tried
3. Show git diff of any changes made
4. Show API response that's incorrect
5. Ask user for guidance

**DO NOT make random changes hoping to fix it. Ask first.**

---

## 📝 Prevention Checklist

Before making ANY code changes:

- [ ] Read CRITICAL_FIXES_DO_NOT_CHANGE.md
- [ ] Check if change affects protected sections
- [ ] Ask user if changing protected code
- [ ] Test endpoint before deploying
- [ ] Verify metrics match expected values
- [ ] Git commit with descriptive message
- [ ] Document change if it affects critical systems

**Stability > Optimization**
