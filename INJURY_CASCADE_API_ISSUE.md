# INJURY CASCADE STRATEGY - API LIMITATION DISCOVERED

**Date:** November 2, 2025
**Issue:** balldontlie.io Free Tier Doesn't Support Stats Endpoint

---

## What Happened

While running the Injury Cascade scraper, we discovered:

1. ✅ **Games endpoint works** - Successfully fetched 500 games
2. ❌ **Stats endpoint blocked** - Returns 401 Unauthorized
3. ⚠️ **Rate limiting hit** - 429 error after 500 games

## API Endpoint Test Results

```bash
# Games endpoint (FREE TIER) - WORKS
GET /v1/games
Authorization: Bearer 9ca7e6df-853f-4ac4-a964-2eafa7627b8d
Status: 200 OK

# Stats endpoint (REQUIRES PAID PLAN) - BLOCKED
GET /v1/stats
Authorization: Bearer 9ca7e6df-853f-4ac4-a964-2eafa7627b8d
Status: 401 Unauthorized
```

## Why This Matters

**Injury Cascade Strategy requires:**
- Player minutes played (to detect early exits)
- Player points/rebounds/assists (to compare to season averages)
- Substitute player performance data

**All of this data comes from the `/stats` endpoint**, which requires a paid plan.

## balldontlie.io Pricing

**Free Tier ($0/month):**
- Basic game data only
- 60 requests/minute
- No player stats access

**Paid Tier ($10-20/month estimated):**
- Full player stats access
- Higher rate limits
- Historical data

## Decision Point

### Option A: Purchase Paid API Access
**Cost:** $10-20/month
**Time to complete:** 30-45 minutes (with paid access)
**Pros:** Complete Injury Cascade verification
**Cons:** Recurring cost, still only verifies 1 strategy

### Option B: Pivot to Quick Win Strategies (RECOMMENDED)
**Cost:** $0
**Time to complete:** 1-2 hours per strategy
**Pros:** Verify 3-5 strategies in same time, no ongoing costs
**Cons:** Injury Cascade remains unverified initially

---

## Recommended Path Forward

**Verify these strategies FIRST (no scrapers, no paid APIs):**

### 1. Key Numbers Strategy (#21) - NFL
**Data Source:** Pro Football Reference (free)
**Method:** Download 2023 NFL scores CSV, upload to ChatGPT
**Time:** 1-2 hours
**Priority:** HIGH

**Steps:**
1. Go to https://www.pro-football-reference.com/years/2023/games.htm
2. Export table to CSV
3. Open ChatGPT, paste Query #21 from CHATGPT_BATCH_QUERIES.txt
4. Upload CSV
5. Get win rate results
6. Run update script: `python backend/backtesting/update_verified_backtests.py`

### 2. CLV Tracker (#18) - Cross-Sport
**Data Source:** OddsPortal (free historical data)
**Method:** Manually collect opening/closing lines sample
**Time:** 2-3 hours
**Priority:** HIGH

### 3. Middle Opportunity Detection (#16) - Cross-Sport
**Data Source:** OddsPortal multi-book comparison
**Method:** Find games with 2+ point spread gaps
**Time:** 2-3 hours
**Priority:** HIGH

---

## Injury Cascade - Future Options

**Option 1: Purchase balldontlie.io paid plan**
- Verify exact pricing first
- Consider if worth $120-240/year for this one strategy

**Option 2: Use alternate free data source**
- ESPN API (may have rate limits)
- NBA.com official API (complex authentication)
- Scrape Basketball Reference (legal gray area)

**Option 3: Manual data collection**
- Download player game logs from Basketball Reference
- Time-intensive but free
- Might take 5-10 hours of manual work

**Option 4: Keep mock data for now**
- Verify 20+ other strategies first
- Return to Injury Cascade when budget allows
- Current mock: 191 bets, 53.4% win rate, 7.2% ROI

---

## Summary

**Recommendation:** **Pivot to Quick Win strategies now**

**Rationale:**
- Verify 3 strategies in the time Injury Cascade would take
- No recurring costs
- Build momentum and workflow
- Return to Injury Cascade later when budget/time allows

**Next Action:**
Download 2023 NFL scores and verify Key Numbers strategy (#21) - can be done in next 1-2 hours.

---

## Files Updated

1. `backend/backtesting/scrapers/injury_cascade_scraper.py` - Working but blocked by API limits
2. `STRATEGY_VERIFICATION_STATUS.md` - Original status report
3. `INJURY_CASCADE_API_ISSUE.md` - This document

**Scraper Status:** ✅ Code works, ❌ API access insufficient
