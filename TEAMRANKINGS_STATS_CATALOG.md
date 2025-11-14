# TeamRankings Stats Catalog - Game Card Enhancement

**Last Updated:** November 12, 2025
**Purpose:** Comprehensive list of all available TeamRankings.com stats for enhancing game cards (Stats, Ranks, Baseline tabs)

---

## Overview

TeamRankings provides **50 total stats** across 4 sports (NBA, NFL, NCAAF, MLB). All stats include:
- **Rank** (1-30 for NBA/MLB, 1-32 for NFL, 1-136 for NCAAF)
- **Value** (actual stat value)
- **Last 3 games** trends
- **Home/Away splits** (on some)

### Sports Covered
- ✅ **NBA**: 13 stats available
- ✅ **NFL**: 17 stats available
- ✅ **NCAAF**: 11 stats available
- ✅ **MLB**: 9 stats available
- ⚠️ **NCAAB**: Not yet available (would need custom scraper or API)
- ⚠️ **NHL**: Not available on TeamRankings (use different source)

---

## 🏀 NBA Stats (13 Available)

### Offense (5 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Points Per Game | `points-per-game` | 125.5 ppg | **Stats**, Baseline |
| Possessions Per Game | `possessions-per-game` | 109.7 | Stats, **Baseline** (pace indicator) |
| Assists Per Game | `assists-per-game` | 30.9 apg | Stats |
| True Shooting % | `true-shooting-percentage` | 123.5% | **Stats** (shooting efficiency) |
| Points In Paint Per Game | `points-in-paint-per-game` | 59.1 ppg | Stats |

### Defense (1 stat)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Opponent Points Per Game | `opponent-points-per-game` | 108.3 ppg | **Stats**, Baseline |

### Rebounding (2 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Offensive Rebounds Per Game | `offensive-rebounds-per-game` | 15.3 orpg | Stats |
| Defensive Rebounds Per Game | `defensive-rebounds-per-game` | 37.1 drpg | Stats |

### Other (5 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Average Scoring Margin | `average-scoring-margin` | +14.4 | **Ranks**, Baseline |
| Turnovers Per Game | `turnovers-per-game` | 10.9 tpg | Stats |
| Steals Per Game | `steals-per-game` | 10.7 spg | Stats |
| Blocks Per Game | `blocks-per-game` | 6.9 bpg | Stats |
| Personal Fouls Per Game | `personal-fouls-per-game` | 18.3 fpg | Stats |

### 🎯 Recommended Display Priority (NBA)
**MUST HAVE (Stats Tab):**
1. Points Per Game (rank + value)
2. Opponent Points Per Game (rank + value)
3. True Shooting % (rank + value)
4. Possessions Per Game (rank + value) - labeled as "Pace"
5. Average Scoring Margin (rank + value)

**NICE TO HAVE (Stats Tab):**
6. Points In Paint Per Game
7. Assists Per Game
8. Turnovers Per Game
9. Defensive Rebounds Per Game

**BASELINE TAB:**
- Possessions Per Game (both teams) - shows pace matchup
- Average Scoring Margin (both teams) - shows quality gap

---

## 🏈 NFL Stats (17 Available)

### Offense (9 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Points Per Game | `points-per-game` | 32.1 ppg | **Stats**, Baseline |
| Yards Per Game | `yards-per-game` | 396.9 ypg | **Stats** |
| Passing Yards Per Game | `passing-yards-per-game` | 261.4 pypg | Stats |
| Rushing Yards Per Game | `rushing-yards-per-game` | 153.2 rypg | Stats |
| Third Down Conversion % | `third-down-conversion-pct` | 47.79% | **Stats** (critical!) |
| Red Zone Scoring % | `red-zone-scoring-pct` | 80.95% | **Stats** (critical!) |
| First Downs Per Game | `first-downs-per-game` | 23.9 fdpg | Stats |
| Penalties Per Game | `penalties-per-game` | 4.6 ppg | Stats |
| Takeaways Per Game | `takeaways-per-game` | 2.2 tpg | Stats |

### Defense (7 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Opponent Points Per Game | `opponent-points-per-game` | 16.7 ppg | **Stats**, Baseline |
| Opponent Yards Per Game | `opponent-yards-per-game` | 261.3 ypg | **Stats** |
| Opponent Passing Yards Per Game | `opponent-passing-yards-per-game` | 162.3 pypg | Stats |
| Opponent Rushing Yards Per Game | `opponent-rushing-yards-per-game` | 79.2 rypg | Stats |
| Opponent Third Down Conversion % | `opponent-third-down-conversion-pct` | 28.06% | **Stats** (critical!) |
| Opponent Red Zone Scoring % | `opponent-red-zone-scoring-pct` | 37.50% | **Stats** (critical!) |
| Sacks Per Game | `sacks-per-game` | 4.6 spg | Stats |

### Other (1 stat)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Average Scoring Margin | `average-scoring-margin` | +11.5 | **Ranks**, Baseline |

### 🎯 Recommended Display Priority (NFL)
**MUST HAVE (Stats Tab):**
1. Points Per Game (rank + value)
2. Opponent Points Per Game (rank + value)
3. Yards Per Game (rank + value)
4. Opponent Yards Per Game (rank + value)
5. Third Down Conversion % (rank + value)
6. Opponent Third Down Conversion % (rank + value)
7. Red Zone Scoring % (rank + value)
8. Opponent Red Zone Scoring % (rank + value)

**NICE TO HAVE (Stats Tab):**
9. Passing Yards Per Game
10. Rushing Yards Per Game
11. Sacks Per Game
12. Takeaways Per Game

**BASELINE TAB:**
- Average Scoring Margin (both teams) - shows quality gap
- Third Down % vs Opp Third Down % - shows critical situational advantage

---

## 🏈 NCAAF Stats (11 Available)

### Offense (6 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Points Per Game | `points-per-game` | 43.6 ppg | **Stats**, Baseline |
| Yards Per Game | `yards-per-game` | 503.2 ypg | **Stats** |
| Passing Yards Per Game | `passing-yards-per-game` | 347.8 pypg | Stats |
| Rushing Yards Per Game | `rushing-yards-per-game` | 285.0 rypg | Stats |
| Third Down Conversion % | `third-down-conversion-pct` | 55.26% | **Stats** (critical!) |
| Red Zone Scoring % | `red-zone-scoring-pct` | 100.00% | **Stats** (critical!) |

### Defense (3 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Opponent Points Per Game | `opponent-points-per-game` | 8.1 ppg | **Stats**, Baseline |
| Opponent Yards Per Game | `opponent-yards-per-game` | 217.3 ypg | **Stats** |
| Sacks Per Game | `sacks-per-game` | 4.0 spg | Stats |

### Other (2 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Average Scoring Margin | `average-scoring-margin` | +27.9 | **Ranks**, Baseline |
| Takeaways Per Game | `takeaways-per-game` | 2.9 tpg | Stats |

### 🎯 Recommended Display Priority (NCAAF)
**MUST HAVE (Stats Tab):**
1. Points Per Game (rank + value)
2. Opponent Points Per Game (rank + value)
3. Yards Per Game (rank + value)
4. Opponent Yards Per Game (rank + value)
5. Third Down Conversion % (rank + value)
6. Red Zone Scoring % (rank + value)

**NICE TO HAVE (Stats Tab):**
7. Passing Yards Per Game
8. Rushing Yards Per Game
9. Sacks Per Game
10. Takeaways Per Game

**BASELINE TAB:**
- Average Scoring Margin (both teams) - shows talent gap (huge in college)
- Points Per Game vs Opponent Points Per Game - shows matchup style

---

## ⚾ MLB Stats (9 Available)

### Offense (6 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Runs Per Game | `runs-per-game` | 5.19 rpg | **Stats**, Baseline |
| Batting Average | `batting-average` | .267 | **Stats** |
| Home Runs Per Game | `home-runs-per-game` | 1.66 hrpg | Stats |
| Hits Per Game | `hits-per-game` | 9.15 hpg | Stats |
| Walks Per Game | `walks-per-game` | 3.90 wpg | Stats |
| Strikeouts Per Game | `strikeouts-per-game` | 6.77 kpg | Stats (pitcher K's) |

### Defense (3 stats)
| Stat Name | URL Slug | Example Value | Best For Tab |
|-----------|----------|---------------|--------------|
| Opponent Runs Per Game | `opponent-runs-per-game` | 3.73 rpg | **Stats**, Baseline |
| Earned Run Average | `earned-run-average` | 3.49 ERA | **Stats** (pitching quality) |
| Errors Per Game | `errors-per-game` | 0.32 epg | Stats |

### 🎯 Recommended Display Priority (MLB)
**MUST HAVE (Stats Tab):**
1. Runs Per Game (rank + value)
2. Opponent Runs Per Game (rank + value)
3. Batting Average (rank + value)
4. Earned Run Average (rank + value)
5. Home Runs Per Game (rank + value)

**NICE TO HAVE (Stats Tab):**
6. Hits Per Game
7. Walks Per Game
8. Strikeouts Per Game

**BASELINE TAB:**
- Runs Per Game vs Opponent Runs Per Game (both teams) - shows offensive/defensive balance

---

## ⚠️ Missing Sports

### NCAAB (College Basketball)
**Status:** Not available on TeamRankings.com's standard stat pages
**Alternative:** Use KenPom (already integrated) or ESPN API
**Current Solution:** Continue using KenPom for NCAAB stats

### NHL (Hockey)
**Status:** Not available on TeamRankings.com
**Alternative:** Use MoneyPuck.com (already mentioned in docs) or NHL official API
**Action Needed:** Implement NHL scraper from different source

---

## Implementation Notes

### Current Scraper Status
✅ **NBA Scraper:** `backend/scrapers/teamrankings_nba_scraper.py`
- Currently scrapes: All 13 stats
- Cache duration: 6 hours
- Returns: Full team stats dict with 20+ calculated fields

✅ **NFL Scraper:** `backend/scrapers/teamrankings_nfl_scraper.py`
- Currently scrapes: All 17 stats
- Cache duration: 6 hours
- Returns: Full team stats dict with 20+ calculated fields

✅ **NCAAF Scraper:** `backend/scrapers/teamrankings_ncaaf_scraper.py`
- Currently scrapes: All 11 stats
- Cache duration: 6 hours
- Returns: Full team stats dict

✅ **MLB Scraper:** `backend/scrapers/teamrankings_mlb_scraper.py`
- Currently scrapes: All 9 stats
- Cache duration: 6 hours
- Returns: Full team stats dict

### Data Structure Returned

Each scraper returns a dict like this:

```python
{
    'Los Angeles Lakers': {
        'team_name': 'Los Angeles Lakers',
        'pts_per_game': 118.5,
        'pts_allowed': 110.2,
        'point_diff': 8.3,
        'wins': 42,
        'losses': 30,
        'games_played': 72,
        'win_pct': 0.583,
        'pace': 102.3,  # possessions
        'offensive_rebounds': 10.5,
        'defensive_rebounds': 34.8,
        'total_rebounds': 45.3,
        'assists': 27.2,
        'turnovers': 13.1,
        'steals': 8.2,
        'blocks': 5.4,
        'true_shooting_pct': 58.9,
        'personal_fouls': 19.6,
        'points_in_paint': 52.3,
        'net_rating': 8.3,
        'off_rating': 118.5,
        'def_rating': 110.2,
        'assist_turnover_ratio': 2.08,
        'source': 'teamrankings',
        'last_updated': '2025-11-12T08:00:00'
    }
}
```

**Important:** The dict does NOT include ranks by default. You would need to:
1. Fetch all teams
2. Sort by stat value
3. Assign ranks (1 = best)

---

## Game Card UI Recommendations

### Stats Tab Layout

**Option A: Side-by-Side Comparison**
```
┌─────────────────────────────────────────────────────────────┐
│                         STATS                               │
├─────────────────────────────────────────────────────────────┤
│  Stat                    Away (Rank)      Home (Rank)       │
├─────────────────────────────────────────────────────────────┤
│  Points Per Game         118.5 (#3)       112.4 (#12)       │
│  Opp Points Per Game     110.2 (#8)       108.9 (#5)        │
│  Pace (Possessions)      102.3 (#5)       98.1 (#22)        │
│  True Shooting %         58.9% (#7)       56.2% (#18)       │
│  Points In Paint         52.3 (#9)        48.7 (#19)        │
│  Assists Per Game        27.2 (#4)        24.1 (#15)        │
└─────────────────────────────────────────────────────────────┘
```

**Option B: Team-Specific Cards**
```
┌───────────────────────┐  ┌───────────────────────┐
│   AWAY TEAM STATS     │  │   HOME TEAM STATS     │
├───────────────────────┤  ├───────────────────────┤
│ PPG: 118.5 (#3)       │  │ PPG: 112.4 (#12)      │
│ Def: 110.2 (#8)       │  │ Def: 108.9 (#5)       │
│ Pace: 102.3 (#5)      │  │ Pace: 98.1 (#22)      │
│ TS%: 58.9% (#7)       │  │ TS%: 56.2% (#18)      │
└───────────────────────┘  └───────────────────────┘
```

### Ranks Tab (NEW!)

Show overall team quality rankings:
```
┌─────────────────────────────────────────────────────────────┐
│                        RANKINGS                             │
├─────────────────────────────────────────────────────────────┤
│  Category               Away (Rank)      Home (Rank)        │
├─────────────────────────────────────────────────────────────┤
│  Overall Margin         +8.3 (#5)        +2.1 (#18)         │
│  Offensive Rating       118.5 (#3)       112.4 (#12)        │
│  Defensive Rating       110.2 (#8)       108.9 (#5)         │
│  Win %                  .583 (#6)        .514 (#14)         │
└─────────────────────────────────────────────────────────────┘
```

### Baseline Tab

Show pace/style matchup:
```
┌─────────────────────────────────────────────────────────────┐
│                     MATCHUP BASELINE                        │
├─────────────────────────────────────────────────────────────┤
│  Pace Matchup:          102.3 (#5)  vs  98.1 (#22)         │
│  ➜ FAST PACED GAME EXPECTED (Away dictates tempo)          │
│                                                             │
│  Offensive Strength:    118.5 (#3)  vs  108.9 (#5 def)     │
│  ➜ ADVANTAGE: Away (Elite offense vs good defense)         │
│                                                             │
│  Defensive Strength:    110.2 (#8)  vs  112.4 (#12 off)    │
│  ➜ SLIGHT ADVANTAGE: Away                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

### Immediate (This Week)
1. ✅ Catalog all available stats (DONE - this document)
2. ⏳ Review which stats to display per sport
3. ⏳ Design UI mockups for Stats/Ranks/Baseline tabs
4. ⏳ Update game_tracker.py to fetch TeamRankings data for each game
5. ⏳ Add stats fields to LiveGame model
6. ⏳ Update frontend GameCard component

### Short Term (Next 2 Weeks)
7. ⏳ Add rank calculation logic (sort all teams, assign 1-30/32)
8. ⏳ Add color coding (green = top 10, yellow = middle, red = bottom 10)
9. ⏳ Add trend indicators (↑ improving, ↓ declining over last 3 games)
10. ⏳ Test with real game data

### Medium Term (Future)
11. ⏳ Add NHL stats from different source (MoneyPuck or NHL API)
12. ⏳ Add NCAAB stats (continue using KenPom)
13. ⏳ Add historical comparisons (team vs season average)
14. ⏳ Add situational stats (home/away splits, last 10 games)

---

## Questions to Answer

**For User:**

1. **Which stats matter most to you for each sport?**
   - Do you want the comprehensive list or just the top 5-7 per sport?

2. **How should ranks be displayed?**
   - Option A: Just number (#3)
   - Option B: Number with color (🟢 #3 for top 10)
   - Option C: Percentile (Top 10%)

3. **Should we show ALL stats or have "Show More" button?**
   - Default view: 5 key stats
   - Expanded view: All 13-17 stats

4. **Do you want trend indicators?**
   - Example: "PPG: 118.5 (#3) ↑" means improving
   - Requires fetching "Last 3 games" data (available on TeamRankings)

5. **Baseline Tab format?**
   - Option A: Auto-generated analysis ("FAST PACED GAME EXPECTED")
   - Option B: Just raw comparisons with visual bars
   - Option C: Both

---

**Report Generated:** November 12, 2025 @ 8:55 AM CST
**Status:** ✅ Complete - Ready for review and implementation planning
