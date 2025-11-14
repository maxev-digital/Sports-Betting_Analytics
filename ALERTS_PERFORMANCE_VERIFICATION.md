# Alerts Performance - Verification Guide
**Date:** 2025-11-12

## ✅ Changes Verified in Code

All changes have been:
1. ✅ Saved to `frontend/src/components/AlertsPerformance.tsx`
2. ✅ Compiled into production build (`frontend/dist/`)
3. ✅ Function `getTeamForRecommendation` exists in built files
4. ✅ Pagination controls compiled into build

## What You Should See NOW

### 1. Team Names (Not HOME/AWAY)
**BEFORE:**
```
Pick Column: "HOME" or "AWAY" for spreads/moneylines
```

**AFTER:**
```
Pick Column: "Akron Zips" or "Kent State Golden Flashes" (actual team names)
```

### 2. Lines Rounded to .5 or Whole Numbers
**BEFORE:**
```
Line Column: -4.77, 156.17, 0.7462
```

**AFTER:**
```
Line Column: -4.5, 156.0, 0.5 (or +745 for moneylines)
```

### 3. Pagination Controls at Bottom
**BEFORE:**
```
"Showing most recent alerts with completed games"
[No pagination buttons]
```

**AFTER:**
```
"Showing page 1 of 20 (25 results)"
« First | ‹ Prev | 1 2 3 4 5 | Next › | Last »
```

## How to Verify Changes

### Step 1: Clear ALL Cache
```
1. Open browser DevTools (F12)
2. Right-click the Refresh button
3. Select "Empty Cache and Hard Reload"
4. OR: Ctrl+Shift+Delete → Clear cache → Time range: All time
```

### Step 2: Check Which Frontend You're Using

**Are you viewing:**
- ✅ LOCAL DEV: http://localhost:5173
- ✅ LOCAL PROD: http://localhost:5173 (after build)
- ❌ PRODUCTION: https://max-ev-sports.com (changes NOT deployed yet)

**If viewing production**, the changes won't show until we deploy to production.

### Step 3: Navigate to Alerts Page
```
1. Go to: http://localhost:5173/alerts
2. Scroll all the way to the bottom
3. Look for "📊 Alerts Performance" section
4. Verify the 3 changes above
```

### Step 4: Check Browser Console
```
1. Press F12
2. Go to Console tab
3. Look for any errors (red text)
4. If errors exist, copy and share them
```

## API Test (Backend Working Correctly)
```bash
# This returns correct data:
curl "http://localhost:8000/api/performance/recent-predictions?limit=3"

# Sample response shows:
- recommendation: "AWAY" (will be converted to team name in frontend)
- market_total: -4.77 (will be rounded to -4.5)
- Works correctly! ✅
```

## If Still Not Visible

### Option 1: Force Vite Dev Server Restart
```bash
# Kill existing vite
taskkill /F /IM node.exe

# Restart frontend
cd frontend
npm run dev
```

### Option 2: Use Preview Server (Production Build)
```bash
cd frontend
npm run preview
# Then visit: http://localhost:4173
```

### Option 3: Check Service Worker
```
1. F12 → Application tab → Service Workers
2. Click "Unregister" if any are listed
3. Hard refresh
```

## Expected API Response Format
```json
{
  "prediction_id": "2025-11-12_Kent State_Akron_spreads_ensemble",
  "recommendation": "AWAY",  // ← Will show "Kent State Golden Flashes"
  "market_total": -4.77,     // ← Will show "-4.5"
  "bet_type": "SPREADS"
}
```

## Visual Confirmation Checklist

- [ ] Pick column shows team names (not HOME/AWAY) for spreads
- [ ] Pick column shows team names (not HOME/AWAY) for moneylines
- [ ] Pick column still shows OVER/UNDER for totals
- [ ] Line column shows -4.5, -10.0, 236.5 (no .7, .3, .17 decimals)
- [ ] Pagination shows: "Showing page 1 of X (25 results)"
- [ ] Pagination has 5 navigation buttons at bottom
- [ ] Can click "Next ›" to see page 2

---

**Note:** If you're viewing https://max-ev-sports.com (production), these changes are NOT deployed yet. They only exist in your local development build at http://localhost:5173.
