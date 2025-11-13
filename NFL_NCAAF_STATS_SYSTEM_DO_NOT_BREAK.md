# NFL & NCAAF Stats System - CRITICAL SYSTEM DOCUMENTATION

**🚨 DO NOT MODIFY THESE FILES WITHOUT READING THIS FIRST 🚨**

**Last Updated:** 2025-11-13
**Status:** WORKING - NFL Fixed, NCAAF Pending

---

## Overview

The NFL and NCAAF game cards display team statistics with **rankings** using the TeamRankings scraper. This system took multiple fixes to get working correctly. **DO NOT break it again.**

---

## Critical Files - DO NOT MESS UP

### 1. **backend/scrapers/teamrankings_nfl_scraper.py**
**Purpose:** Scrapes NFL team stats from TeamRankings.com with rankings

**CRITICAL METHOD (lines 383-449):** `_calculate_rankings()`
- This method MUST exist and MUST be called at line 374 in `fetch_all_team_stats()`
- It calculates rank numbers (1-32) for all stats: PPG, 3rd Down %, Red Zone %, etc.
- Without this, all ranks show as N/A

**DO NOT:**
- Remove the `_calculate_rankings()` method
- Remove the call to `self._calculate_rankings(team_stats)` at line 374
- Change the rank key names (e.g., `points_per_game_rank`, `third_down_pct_rank`)

**Cache Location:** `backend/data/raw/nfl/teamrankings_cache.json`
- Cache duration: 6 hours
- Force refresh: Run `python backend/force_nfl_refresh.py`

### 2. **backend/scrapers/teamrankings_ncaaf_scraper.py**
**Purpose:** Scrapes NCAAF team stats from TeamRankings.com with rankings

**MUST HAVE:** Same `_calculate_rankings()` method as NFL scraper
**Cache Location:** `backend/backend/data/raw/ncaaf/teamrankings_cache.json`

### 3. **backend/game_tracker.py**
**Purpose:** Main game tracking service that fetches stats for all sports

**CRITICAL SECTIONS:**

#### NFL Stats (lines 968-1022): `_get_nfl_teamrankings_stats()`
```python
def _get_nfl_teamrankings_stats(self, team_name: str, is_ncaaf: bool = False) -> Optional[NFLTeamStats]:
    # Fetches TeamRankings stats
    # Maps to NFLTeamStats model with ALL rank fields
    # Lines 1003-1014: Rank field assignments
```

**CRITICAL:** Percentage conversion at lines 999-1000:
```python
third_down_pct=float(tr_stats.get('third_down_conversion_pct', 40.0)) / 100.0,  # Convert to decimal
red_zone_pct=float(tr_stats.get('red_zone_scoring_pct', 55.0)) / 100.0,  # Convert to decimal
```
**WHY:** Backend sends decimals (0.42), frontend multiplies by 100 to display (42%)

#### NFL Assignment (lines 1470-1475):
```python
if sport_key == 'americanfootball_nfl':
    home_nfl_stats_tr = self._get_nfl_teamrankings_stats(game_state.home_team.name, is_ncaaf=False)
    away_nfl_stats_tr = self._get_nfl_teamrankings_stats(game_state.away_team.name, is_ncaaf=False)
    # DO NOT assign to home_stats/away_stats - those are for NBA/NCAAB only!
```

**🚨 CRITICAL - DO NOT:**
```python
# WRONG - This breaks validation:
home_stats = home_nfl_stats_tr  # NO!
away_stats = away_nfl_stats_tr  # NO!
```

**WHY:** `LiveGame` model has separate fields:
- `home_team_stats`/`away_team_stats`: For NBA/NCAAB (TeamStats model)
- `home_nfl_stats`/`away_nfl_stats`: For NFL/NCAAF (NFLTeamStats model)
- Assigning wrong type causes Pydantic validation to fail silently

#### Final Assignment (lines 1863-1870):
```python
# This is correct - stats go to proper NFL-specific fields
if home_nfl_stats_tr:
    home_nfl_stats = home_nfl_stats_tr
if away_nfl_stats_tr:
    away_nfl_stats = away_nfl_stats_tr
```

### 4. **backend/live_models.py**
**Purpose:** Pydantic models for game data validation

**CRITICAL STRUCTURE (lines 325-342):**
```python
class LiveGame(BaseModel):
    # NBA/NCAAB only
    home_team_stats: Optional[TeamStats] = None
    away_team_stats: Optional[TeamStats] = None

    # NFL/NCAAF specific
    home_nfl_stats: Optional[NFLTeamStats] = None
    away_nfl_stats: Optional[NFLTeamStats] = None
    home_ncaaf_stats: Optional[NFLTeamStats] = None
    away_ncaaf_stats: Optional[NFLTeamStats] = None

    # NHL specific
    home_nhl_stats: Optional[NHLTeamStats] = None
    away_nhl_stats: Optional[NHLTeamStats] = None
```

**DO NOT:** Mix model types or remove these fields

---

## What Was Fixed (2025-11-13)

### Issue 1: NFL Games Not Showing (0 games)
**Problem:** All 29 NFL games were being dropped from API response

**Root Cause:** Lines 1474-1475 incorrectly assigned `NFLTeamStats` to `home_stats`/`away_stats` fields that expect `TeamStats`, causing Pydantic validation to fail

**Fix:** Removed incorrect assignments - NFL stats now correctly go to `home_nfl_stats`/`away_nfl_stats` fields only

### Issue 2: All NFL Rankings Showing N/A
**Problem:** PPG Rank: None, 3rd Down Rank: None, all ranks missing

**Root Cause:** VPS had old version of `teamrankings_nfl_scraper.py` without `_calculate_rankings()` method

**Fix:**
1. Deployed updated scraper with `_calculate_rankings()` method
2. Force refreshed cache with `python backend/force_nfl_refresh.py`
3. Restarted backend to load new cache

**Result:** All ranks now showing correctly (Patriots: Rank 8, Jets: Rank 25, etc.)

### Issue 3: Percentage Format
**Problem:** Could display as 4000% if percentages sent as whole numbers

**Fix:** Convert to decimals in `game_tracker.py` lines 999-1000:
```python
third_down_pct=float(tr_stats.get('third_down_conversion_pct', 40.0)) / 100.0
```

---

## How to Verify System is Working

### 1. Check API Response
```bash
curl -s "http://148.230.87.135:8000/api/games" | python -c "
import sys, json
data = json.load(sys.stdin)
nfl = [g for g in data if g.get('state', {}).get('sport_key') == 'americanfootball_nfl']
if nfl:
    home = nfl[0].get('home_nfl_stats')
    print(f'NFL games: {len(nfl)}')
    print(f'PPG Rank: {home.get(\"points_per_game_rank\")}')
    print(f'3rd Down Rank: {home.get(\"third_down_pct_rank\")}')
"
```

**Expected Output:**
```
NFL games: 29
PPG Rank: 8
3rd Down Rank: 7
```

**If you see:**
- `NFL games: 0` → Pydantic validation failing (check game_tracker.py lines 1470-1481)
- `PPG Rank: None` → Rankings not calculated (check scraper has `_calculate_rankings()`)

### 2. Check Cache Has Ranks
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "python3 -c \"
import json
cache = json.load(open('/root/sporttrader/backend/backend/data/raw/nfl/teamrankings_cache.json'))
patriots = cache['data'].get('New England', {})
print(f'PPG Rank exists: {\\\"points_per_game_rank\\\" in patriots}')
print(f'PPG Rank value: {patriots.get(\\\"points_per_game_rank\\\")}')
\""
```

**Expected Output:**
```
PPG Rank exists: True
PPG Rank value: 8
```

### 3. Check VPS Has Correct Scraper Version
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "grep -n 'def _calculate_rankings' /root/sporttrader/backend/scrapers/teamrankings_nfl_scraper.py"
```

**Expected Output:**
```
383:    def _calculate_rankings(self, team_stats: Dict[str, Dict]):
```

**If empty:** Old version deployed, run deployment script again

---

## Force Refresh Cache (When Data Looks Wrong)

### NFL:
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader/backend && python3 force_nfl_refresh.py"
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"
```

### NCAAF:
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader/backend && python3 force_ncaaf_refresh.py"
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"
```

---

## Deployment Checklist

When deploying NFL/NCAAF changes:

1. ✅ Verify `_calculate_rankings()` method exists in scraper
2. ✅ Verify method is called in `fetch_all_team_stats()`
3. ✅ Deploy scraper to VPS: `scp backend/scrapers/teamrankings_nfl_scraper.py root@VPS:/root/sporttrader/backend/scrapers/`
4. ✅ Force cache refresh on VPS
5. ✅ Restart backend service
6. ✅ Verify API shows ranks (not None)
7. ✅ Commit to git with clear message

---

## Git Commit Convention

When modifying these files, use descriptive commits:

**Good:**
```
Fix NFL Rankings - Add _calculate_rankings method to TeamRankings scraper
```

**Bad:**
```
Update scraper
```

---

## Known Issues and Solutions

### Issue: "Only 8 teams have records instead of 32"
**Cause:** TeamRankings standings page HTML structure changed
**Solution:** Update `scrape_standings()` method regex and parsing logic

### Issue: "Ranks showing MISSING after cache refresh"
**Cause:** `_calculate_rankings()` method not present or not being called
**Solution:** Check method exists and is called at line 374

### Issue: "Percentages showing as 4000%"
**Cause:** Sending whole numbers (40) instead of decimals (0.40)
**Solution:** Divide by 100 in `_get_nfl_teamrankings_stats()` lines 999-1000

---

## Contact Points

If this system breaks again:
1. Read this document first
2. Check the "How to Verify" section
3. Compare current files to this documentation
4. DO NOT deploy without testing locally first

**Remember:** This took multiple iterations to get right. Don't break it with careless changes.

---

## Summary

**Working System:**
- ✅ NFL stats with rankings showing correctly
- ✅ 29 NFL games displaying
- ✅ Patriots: PPG Rank 8, 3rd Down Rank 7
- ✅ Jets: PPG Rank 25, 3rd Down Rank 28
- ✅ Percentages formatted correctly (42.0%)

**DO NOT:**
- Remove `_calculate_rankings()` method
- Assign NFL stats to NBA stat fields
- Change percentage format conversion
- Deploy without verifying locally first

**ALWAYS:**
- Test locally before deploying
- Force refresh cache after scraper changes
- Restart backend after cache refresh
- Verify API response shows ranks
- Document any changes to this system
