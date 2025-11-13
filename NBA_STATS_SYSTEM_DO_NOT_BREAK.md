# NBA Stats System - CRITICAL SYSTEM DOCUMENTATION

**🚨 DO NOT MODIFY THESE FILES WITHOUT AUTHORIZATION 🚨**

**Last Updated:** 2025-11-13
**Status:** WORKING - Rankings and Current Season Data Fixed

---

## Overview

The NBA game cards display team statistics with **rankings** using BallDontLie API for records and TeamRankings for detailed stats. This system uses a hybrid approach and took multiple fixes to get working correctly. **DO NOT break it again.**

---

## Critical Files - DO NOT MESS UP

### 1. **backend/balldontlie_nba_client.py**
**Purpose:** Fetches NBA team records and standings from BallDontLie API

**Key Methods:**
- `get_team_standings(season=2025)` - Gets W-L records for current season
- `get_team_from_standings(team_id, season=2025)` - Gets specific team record
- `get_team_id_by_name(team_name)` - Maps team names to BallDontLie IDs

**CRITICAL:** Always use `season=2025` for current season (lines 43, 72)

**DO NOT:**
- Change the season parameter to 2024 or hardcode old seasons
- Remove the team ID mapping (lines 212-246)
- Modify the base_url: `https://api.balldontlie.io/v1`

**API Key:** `BALLDONTLIE_API_KEY` in `.env`

### 2. **backend/scrapers/teamrankings_nba_scraper.py**
**Purpose:** Scrapes detailed NBA stats with rankings from TeamRankings.com

**CRITICAL METHOD (lines 294-360):** `_calculate_rankings()`
- Calculates rank numbers (1-30) for all stats
- Offensive stats (higher = better): PPG, Pace, ORtg
- Defensive stats (lower = better): Opp PPG, DRtg

**DO NOT:**
- Remove the `_calculate_rankings()` method
- Remove the call to `self._calculate_rankings(team_stats)` at line 243
- Change rank extraction from Column 0 (lines 151-158)

**CRITICAL FIX (lines 151-158):** Rank Extraction from Column 0
```python
# Column 0: Rank
rank_text = cols[0].text.strip()
try:
    rank = int(rank_text)
except ValueError:
    rank = None

stats[team_name] = {
    'value': float(stat_value),
    'rank': rank
}
```

**WHY:** TeamRankings tables have rank in Column 0, team name in Column 1, stat value in Column 2. Without extracting Column 0, all ranks show N/A.

**Cache Location:** `backend/backend/data/raw/nba/teamrankings_cache.json`
- Cache duration: 6 hours
- Contains pace, ratings, and advanced stats

### 3. **backend/game_tracker.py**
**Purpose:** Main game tracking service - fetches and combines data from both sources

**CRITICAL SECTION (lines 647-782):** `_get_nba_team_stats()`

#### BallDontLie Integration (lines 708-736):
```python
# Get record from BallDontLie (authoritative source for W-L records)
bdl_team_id = self.balldontlie_nba_client.get_team_id_by_name(team_name)
if bdl_team_id:
    bdl_standing = await self.balldontlie_nba_client.get_team_from_standings(
        bdl_team_id,
        season=2025  # CRITICAL: Current season
    )
    if bdl_standing:
        wins = bdl_standing.get('wins', 0)
        losses = bdl_standing.get('losses', 0)
```

**CRITICAL:** Always use `season=2025` for current season data

#### TeamRankings Integration (lines 738-772):
```python
# Get detailed stats from TeamRankings (rankings, pace, ratings)
teamrankings_stats = self.teamrankings_nba_scraper.get_team_stats(team_name)
if teamrankings_stats:
    pace = teamrankings_stats.get('pace', 100.0)
    pace_rank = teamrankings_stats.get('pace_rank')  # From Column 0
    off_rating = teamrankings_stats.get('off_rating', 110.0)
    off_rating_rank = teamrankings_stats.get('off_rating_rank')
    # ... etc
```

**DO NOT:**
- Assign NBA stats to `home_nfl_stats` or other sport fields
- Change the season parameter from 2025
- Remove rank field assignments

#### Model Assignment (lines 774-782):
```python
team_stats = TeamStats(
    team_id=str(bdl_team_id or ''),
    team_name=team_name,
    games_played=games_played,
    wins=wins,
    losses=losses,
    pace=pace,
    pace_rank=pace_rank,  # Must include all rank fields
    off_rating=off_rating,
    off_rating_rank=off_rating_rank,
    # ...
)
```

#### Final Assignment (lines 1814-1817):
```python
# Correct field assignment for NBA
if home_stats:
    home_team_stats = home_stats
if away_stats:
    away_team_stats = away_stats
```

### 4. **backend/live_models.py**
**Purpose:** Pydantic models for game data validation

**CRITICAL STRUCTURE (lines 119-144): TeamStats Model**
```python
class TeamStats(BaseModel):
    """NBA/NCAAB team statistics with rankings"""
    team_id: str
    team_name: str
    games_played: int
    wins: int
    losses: int
    win_pct: Optional[float] = None

    # Pace and efficiency with ranks
    pace: Optional[float] = None
    pace_rank: Optional[int] = None
    off_rating: Optional[float] = None
    off_rating_rank: Optional[int] = None
    def_rating: Optional[float] = None
    def_rating_rank: Optional[int] = None
    # ... etc
```

**DO NOT:**
- Remove rank fields (pace_rank, off_rating_rank, etc.)
- Use this model for NFL/NCAAF (they use NFLTeamStats)
- Make rank fields required (they must be Optional)

---

## What Was Fixed (2025-11-13)

### Issue 1: NBA Rankings Showing N/A
**Problem:** All rankings showed N/A despite having stat values

**Root Cause:** TeamRankings scraper was only extracting stat values from Column 2, not rank from Column 0

**Fix:** Updated `scrape_stat_page()` to extract rank from Column 0 (lines 151-158):
```python
rank_text = cols[0].text.strip()
rank = int(rank_text)
stats[team_name] = {
    'value': float(stat_value),
    'rank': rank
}
```

### Issue 2: NBA Records Showing 0-0 or Wrong Season
**Problem:** All teams showing 0-0 records or 2024 season data

**Root Cause:** BallDontLie API call using `season=2024` instead of `season=2025`

**Fix:** Changed season parameter to 2025 in:
- `balldontlie_nba_client.py` line 43: `season: int = 2025`
- `game_tracker.py` line 731: `season=2025`

**Result:** Now showing correct 2025 season records

### Issue 3: Missing BallDontLie Integration
**Problem:** Only using TeamRankings which doesn't have accurate W-L records

**Root Cause:** System wasn't using BallDontLie API for authoritative standings data

**Fix:** Added BallDontLie client integration in game_tracker.py (lines 708-736)

---

## Hybrid Data System (Why Two Sources?)

**BallDontLie API:**
- ✅ Accurate W-L records from official NBA API
- ✅ Current season standings
- ✅ Conference rankings
- ❌ Does NOT provide pace, offensive rating, defensive rating
- ❌ Does NOT provide stat rankings

**TeamRankings.com:**
- ✅ Detailed advanced stats (pace, ORtg, DRtg)
- ✅ Rankings for all stats (1-30)
- ✅ Historical consistency
- ⚠️ W-L records can be cached/delayed

**Solution:** Use BallDontLie for records, TeamRankings for stats and rankings

---

## How to Verify System is Working

### 1. Check API Response
```bash
curl -s "http://148.230.87.135:8000/api/games" | python -c "
import sys, json
data = json.load(sys.stdin)
nba = [g for g in data if g.get('state', {}).get('sport_key') == 'basketball_nba']
if nba:
    home = nba[0].get('home_team_stats')
    print(f'NBA games: {len(nba)}')
    print(f'Record: {home.get(\"wins\")}-{home.get(\"losses\")} ({home.get(\"games_played\")} GP)')
    print(f'Pace: {home.get(\"pace\")} (Rank: {home.get(\"pace_rank\")})')
    print(f'ORtg: {home.get(\"off_rating\")} (Rank: {home.get(\"off_rating_rank\")})')
"
```

**Expected Output:**
```
NBA games: 8
Record: 12-1 (13 GP)
Pace: 101.2 (Rank: 5)
ORtg: 118.5 (Rank: 3)
```

**If you see:**
- `Record: 0-0` → BallDontLie season wrong or API key issue
- `Pace: 101.2 (Rank: None)` → TeamRankings not extracting Column 0 ranks
- `NBA games: 0` → Pydantic validation failing

### 2. Check BallDontLie API Key
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "grep BALLDONTLIE_API_KEY /root/sporttrader/backend/.env"
```

**Expected:** Should show API key (not empty)

### 3. Check TeamRankings Cache Has Ranks
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "python3 -c \"
import json
cache = json.load(open('/root/sporttrader/backend/backend/data/raw/nba/teamrankings_cache.json'))
team = list(cache['data'].values())[0]
print(f'Has pace_rank: {\\\"pace_rank\\\" in team}')
print(f'Pace rank value: {team.get(\\\"pace_rank\\\")}')
\""
```

**Expected Output:**
```
Has pace_rank: True
Pace rank value: 5
```

---

## Force Refresh Cache (When Data Looks Wrong)

### Refresh BallDontLie Records:
```bash
# No cache - always fetches live data from API
# Just restart backend to get fresh standings
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"
```

### Refresh TeamRankings Stats:
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader/backend && python3 -c '
from scrapers.teamrankings_nba_scraper import TeamRankingsNBAScraper
scraper = TeamRankingsNBAScraper()
stats = scraper.fetch_all_team_stats(force_refresh=True)
print(f\"Refreshed {len(stats)} teams\")
'"
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"
```

---

## Deployment Checklist

When deploying NBA changes:

1. ✅ Verify BallDontLie API key in `.env`
2. ✅ Verify `season=2025` in all API calls
3. ✅ Verify Column 0 rank extraction in TeamRankings scraper
4. ✅ Verify `_calculate_rankings()` method exists and is called
5. ✅ Deploy files to VPS
6. ✅ Restart backend service
7. ✅ Verify API shows correct records (not 0-0)
8. ✅ Verify API shows ranks (not None)
9. ✅ Commit to git with clear message

---

## Known Issues and Solutions

### Issue: "All teams showing 0-0 records"
**Cause:** Wrong season parameter or BallDontLie API key missing
**Solution:** Check season=2025 in all calls, verify API key exists

### Issue: "Rankings showing None"
**Cause:** TeamRankings scraper not extracting Column 0
**Solution:** Verify `scrape_stat_page()` extracts rank from cols[0]

### Issue: "Old season data (2024)"
**Cause:** Hardcoded season=2024 in code
**Solution:** Change all season parameters to 2025

### Issue: "BallDontLie API errors"
**Cause:** Invalid API key or rate limiting
**Solution:** Check API key, check rate limits on BallDontLie dashboard

---

## Team Name Mappings

**BallDontLie IDs (lines 212-246):**
- Atlanta Hawks: 1
- Boston Celtics: 2
- Brooklyn Nets: 3
- LA Clippers: 13
- LA Lakers: 14
- ... (30 teams total)

**DO NOT** modify these IDs - they are official BallDontLie team IDs

---

## Summary

**Working System:**
- ✅ NBA stats with rankings showing correctly
- ✅ Current 2025 season records from BallDontLie
- ✅ Advanced stats (pace, ratings) from TeamRankings
- ✅ All ranks showing (1-30)
- ✅ Celtics: 12-1 record, Pace Rank 5, ORtg Rank 3 (example)

**DO NOT:**
- Remove Column 0 rank extraction
- Change season from 2025
- Remove `_calculate_rankings()` method
- Remove BallDontLie integration
- Assign NBA stats to NFL/NHL fields
- Deploy without testing locally first

**ALWAYS:**
- Use season=2025 for current season
- Extract rank from Column 0 in TeamRankings
- Test locally before deploying
- Verify both records AND ranks in API response
- Document any changes to this system

**Data Sources:**
- **Records:** BallDontLie API (authoritative)
- **Stats & Rankings:** TeamRankings.com
- **Why Both:** BallDontLie has accurate W-L, TeamRankings has rankings

---

🚨 **AUTHORIZATION REQUIRED TO MODIFY THESE FILES** 🚨
