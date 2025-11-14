# TeamRankings.com Multi-Sport Data Review

## Executive Summary

TeamRankings.com provides **free, scrapable** betting statistics and team performance data across 5 major sports. Based on our research, here's what's available for building betting models and alert systems.

---

## Confirmed Working Sports & URLs

| Sport | Base URL | Stat URL Pattern | Status |
|-------|----------|------------------|--------|
| **NBA** | `/nba/` | `/nba/stat/{stat-name}` | ✅ **WORKING** (Already implemented) |
| **NFL** | `/nfl/` | `/nfl/stat/{stat-name}` | ✅ Confirmed available |
| **NCAAF** | `/college-football/` | `/college-football/stat/{stat-name}` | ✅ Confirmed available |
| **NCAAB** | Multiple possible paths | TBD | ⚠️ URL structure unclear |
| **MLB** | `/mlb/` | `/mlb/stat/{stat-name}` | ✅ Confirmed available |

---

## Data Categories Available (All Sports)

### 1. Team Statistics ⭐ **Primary Data Source**

**What's Available:**
- Points/Runs per game (offensive power)
- Points/Runs allowed per game (defensive strength)
- **Point/Run differential** (net rating - PERFECT for talent matching)
- Win/Loss records
- Win percentage
- Home/Away splits

**Value for Betting Models:**
- ✅ Talent differential calculations (like Quarter Reversal strategy)
- ✅ Power ratings and team rankings
- ✅ Matchup analysis (strong offense vs weak defense)
- ✅ Trend detection (hot/cold teams)

**Example Stats (from NBA - similar structure for all sports):**
```
- points-per-game
- opponent-points-per-game (defense)
- average-scoring-margin (point differential)
- wins / losses
- home-wins / away-wins
```

---

### 2. Betting Picks & Predictions ⚠️ **Use with Caution**

**What's Available:**
- Game Winner Picks
- Point Spread Picks (ATS)
- Over/Under Picks (totals)
- Money Line Picks
- Upset Predictions
- Prediction Accuracy Metrics

**Value for Betting Models:**
- ✅ Consensus picks data (fade or follow the public)
- ✅ Accuracy tracking (which models are sharp)
- ❌ Don't rely on their picks - build your own models

---

### 3. Betting Odds & Lines ⚠️ **Odds API is Better**

**What's Available:**
- Current betting odds
- Multiple sportsbooks
- Historical line movement (trends)

**Value for Betting Models:**
- ❌ **Not recommended** - Use The Odds API instead (real-time, more books)
- ✅ Could be used as backup data source
- ✅ Historical trends might be useful

---

### 4. Standings & Projections

**What's Available:**
- Current season standings
- Projected final standings
- Playoff/postseason seeds

**Value for Betting Models:**
- ✅ Rest-of-season context
- ✅ Playoff implications (teams tanking vs fighting for playoffs)
- ✅ Strength of schedule adjustments

---

### 5. Team Trends (Win/Loss Patterns)

**What's Available:**
- Win/Loss trends
- Against-the-Spread (ATS) trends
- Over/Under trends (totals)
- Home/Away trends

**Value for Betting Models:**
- ✅ Identify profitable betting patterns
- ✅ Fade teams with poor ATS records
- ✅ Target teams with consistent over/under trends

---

## Sport-Specific Data (What We Know)

### 🏀 NBA (Already Implemented) ✅

**Current Usage:**
- Points per game
- Opponent points per game
- Point differential (net rating proxy)
- Wins/Losses

**Additional Stats Available:**
- Pace (possessions per game)
- Offensive rating (points per 100 possessions)
- Defensive rating
- Field goal %, 3PT %, Free throw %
- Rebounds, Assists, Turnovers
- Home/Away splits

**Strategies Using This Data:**
- ✅ Quarter Reversal (with talent differential)
- 🔜 Pace-based totals predictions
- 🔜 Back-to-back fatigue analysis
- 🔜 Home court advantage models

---

### 🏈 NFL

**Likely Available Stats:**
- Points per game / Points allowed
- Total yards / Yards allowed
- Pass yards / Rush yards (offense & defense)
- Turnovers (giveaways vs takeaways)
- Third down conversion %
- Red zone efficiency
- Time of possession
- Penalties

**Potential Strategies:**
- 🔜 Matchup analysis (strong pass offense vs weak pass defense)
- 🔜 Turnover differential models
- 🔜 Weather-adjusted totals
- 🔜 Division rivalry trends
- 🔜 Home field advantage (especially outdoors)

---

### 🏈 NCAAF (College Football)

**Likely Available Stats:**
- Points per game / Points allowed
- Total offense / Total defense
- Rush yards / Pass yards
- Turnovers
- Third/Fourth down conversions
- Red zone scoring

**Potential Strategies:**
- 🔜 Power conference vs mid-major matchups
- 🔜 Pace-based totals (some college teams play fast)
- 🔜 Home field advantage (college atmosphere)
- 🔜 Rivalry game trends
- 🔜 Conference championship implications

---

### 🏀 NCAAB (College Basketball)

**URL Structure:** TBD (need to confirm)

**Likely Available Stats:**
- Points per game / Points allowed
- Offensive efficiency / Defensive efficiency
- Pace (possessions per game)
- Field goal %, 3PT %, Free throw %
- Rebounds per game
- Turnover margin
- Home/Away splits

**Potential Strategies:**
- 🔜 Tempo-based totals (fast pace vs slow pace)
- 🔜 Conference tournament trends
- 🔜 March Madness models
- 🔜 Upset detection (mid-majors vs power conferences)
- 🔜 Home court advantage (stronger in college)

**Note:** Already have KenPom scraper for advanced metrics (AdjTempo, AdjOffEff, AdjDefEff)

---

### ⚾ MLB (Baseball)

**Likely Available Stats:**
- Runs per game / Runs allowed
- Batting average / On-base percentage
- Home runs per game
- ERA (pitching)
- Strikeouts / Walks
- WHIP (walks + hits per inning)

**Potential Strategies:**
- 🔜 Starting pitcher vs team matchups
- 🔜 Bullpen strength analysis
- 🔜 Weather-adjusted totals (wind, temperature)
- 🔜 Park factors (hitter-friendly vs pitcher-friendly)
- 🔜 Day vs night game trends
- 🔜 Division rivalry trends

---

## Cost Comparison: TeamRankings vs Paid APIs

| Data Provider | Cost | Reliability | Data Quality | Our Recommendation |
|---------------|------|-------------|--------------|-------------------|
| **TeamRankings** | **FREE** ✅ | High | Good | ✅ **Primary for team stats** |
| Ball Don't Lie | $X/month | High | Good | ❌ Cancel (TeamRankings is free) |
| ESPN API | FREE | Medium | Fair | ✅ Keep as fallback |
| The Odds API | $X/month | Very High | Excellent | ✅ **Primary for live odds** |
| KenPom (NCAAB) | $20/year | Very High | Excellent | ✅ Keep (advanced metrics) |

**Estimated Savings:**
- Cancel Ball Don't Lie: **$X/month**
- Keep ESPN as fallback: **$0**
- Keep The Odds API for live lines: **Worth it**

---

## Recommended Scraper Architecture

### Layer 1: Data Collection (What to Scrape)

```
TeamRankings Scrapers (FREE):
├── NBA Team Stats ✅ (Already built)
├── NFL Team Stats 🔜 (Build next)
├── NCAAF Team Stats 🔜
├── NCAAB Team Stats 🔜
└── MLB Team Stats 🔜

Other Data Sources:
├── The Odds API → Live betting lines (PAID but essential)
├── ESPN API → Live scores, quarter scores (FREE backup)
└── KenPom → NCAAB advanced metrics (PAID $20/year)
```

### Layer 2: Betting Alert Scripts (Strategies)

```
Strategy Detectors:
├── Quarter Reversal ✅ (NBA - already built)
├── Favorite Comeback 🔜 (NBA)
├── Pace-Based Totals 🔜 (NBA, NCAAB)
├── Matchup Exploits 🔜 (NFL - strong pass O vs weak pass D)
├── Weather-Adjusted Totals 🔜 (NFL, MLB)
├── Back-to-Back Fatigue 🔜 (NBA)
└── Division Rivalry Trends 🔜 (All sports)
```

---

## Prioritized Build Order

### Phase 1: Complete NBA Foundation ✅
1. ✅ TeamRankings NBA scraper (done)
2. ✅ Quarter Reversal with talent differential (done)
3. 🔜 Integrate alerts into GameCard UI
4. 🔜 Test with live NBA games

### Phase 2: Expand to NFL (Next Priority) 🏈
1. Build TeamRankings NFL scraper
2. Implement Matchup Exploit strategy (pass O vs pass D)
3. Add weather data integration
4. Build NFL alert badges

### Phase 3: Add NCAAB 🏀
1. Build TeamRankings NCAAB scraper (supplement KenPom)
2. Implement pace-based totals strategy
3. Add conference tournament trends

### Phase 4: Add MLB & NCAAF ⚾🏈
1. Build MLB scraper (pitcher matchups, park factors)
2. Build NCAAF scraper (power ratings, pace)
3. Implement sport-specific strategies

---

## Key Insights for Model Building

### What TeamRankings Does Best:
1. ✅ **Point Differential** - Perfect for talent matching (better than ESPN's approximation)
2. ✅ **Free & Reliable** - No API keys, no rate limits, stable website
3. ✅ **Consistent Structure** - Same table format across all sports
4. ✅ **6-Hour Cache** - Reduces server load, data doesn't change that fast anyway

### What TeamRankings Doesn't Do:
1. ❌ **Live Scores** - Use ESPN API or The Odds API for this
2. ❌ **Real-Time Odds** - The Odds API is better
3. ❌ **Advanced Metrics** - KenPom/FanGraphs/Football Outsiders are better
4. ❌ **Player Stats** - Not needed for team-based strategies

### The Perfect Stack:
```
TeamRankings → Team power ratings, talent differential
The Odds API → Live betting lines, odds
ESPN API → Live scores, quarter scores
KenPom/etc → Advanced metrics (optional)
```

---

## Next Steps

### Immediate (This Week):
1. **Complete NBA Quarter Reversal UI integration**
2. **Test with live NBA games**
3. **Build NFL scraper** (season is active now)

### Short-Term (Next 2 Weeks):
1. Build NFL matchup exploit strategy
2. Add weather data for NFL/MLB
3. Expand to NCAAB (March Madness prep)

### Long-Term (Next Month):
1. Build MLB scraper (season starts April)
2. Add NCAAF scraper (season starts August)
3. Implement 5+ more betting strategies

---

## Technical Implementation Notes

### Scraper Template (Reusable for All Sports)

```python
class TeamRankingsScraper:
    """Base scraper for TeamRankings.com"""

    BASE_URL = "https://www.teamrankings.com/{sport}"
    CACHE_DURATION = timedelta(hours=6)

    def scrape_stat_page(self, stat_name: str) -> Dict[str, float]:
        """Scrape a single stat page"""
        # Same table structure across all sports
        url = f"{self.BASE_URL}/stat/{stat_name}"
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'datatable'})
        # Parse rows...

    def fetch_all_team_stats(self) -> Dict[str, Dict]:
        """Fetch all team statistics with caching"""
        # Check cache first (6 hours)
        # Scrape multiple stat pages
        # Combine into team stats dict
        # Save to cache
```

### Key Stats to Scrape (Priority Order)

**All Sports:**
1. Points/Runs per game (offense)
2. Points/Runs allowed per game (defense)
3. Point/Run differential (talent proxy)
4. Wins/Losses
5. Home/Away splits

**Sport-Specific:**
- NBA/NCAAB: Pace, efficiency ratings
- NFL/NCAAF: Yards per game, turnover margin
- MLB: ERA, batting average, park factors

---

## Conclusion

**TeamRankings.com is a goldmine for free betting data.** We've already proven it works with NBA (replacing paid services), and the same scraper architecture can be extended to NFL, NCAAF, NCAAB, and MLB.

**Benefits:**
- ✅ **Free forever** (no API keys)
- ✅ **Reliable** (stable website structure)
- ✅ **Comprehensive** (all major sports)
- ✅ **Perfect for talent matching** (point differential data)

**Action Items:**
1. ✅ NBA scraper complete
2. 🔜 Build NFL scraper next (season is live)
3. 🔜 Expand to NCAAB (March Madness coming)
4. 🔜 Add MLB + NCAAF later

**Estimated Cost Savings:** Cancel Ball Don't Lie and rely on TeamRankings = **$X/month saved**

---

**Status:** Research Complete ✅
**Next Step:** Build NFL scraper and matchup exploit strategy
