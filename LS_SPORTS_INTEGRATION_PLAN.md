# LS Sports Integration Plan
**Date:** November 9, 2025
**Meeting:** LS Sports Partnership Discussion
**Goal:** Add LS Sports as a premium data/odds provider to MAX EV SPORTS platform

---

## 1. Meeting Preparation - Key Questions for LS Sports

### A. Technical Integration
- [ ] **API Documentation**: Can we get access to technical docs before trial?
- [ ] **Authentication Method**: API key, OAuth, or other?
- [ ] **API Endpoints**: REST, WebSocket, or both?
- [ ] **Rate Limits**: What are the call limits for our tier?
- [ ] **Sandbox/Test Environment**: Do you offer test credentials?
- [ ] **Data Format**: JSON, XML, or other response formats?
- [ ] **Sports Coverage**: Which US sports are covered (NBA, NFL, NHL, NCAAB, NCAAF, MLB)?
- [ ] **Bookmaker Coverage**: Which of the 100+ bookmakers include US books (FanDuel, DraftKings, BetMGM, etc.)?

### B. Data Quality & Speed
- [ ] **Update Frequency**: How often do odds update (seconds)?
- [ ] **Latency**: What's the typical response time (<100ms preferred)?
- [ ] **Live vs Pre-Match**: Both available? Separate endpoints?
- [ ] **Historical Data**: Do you provide historical odds/line movement data?
- [ ] **Data Accuracy**: What's your SLA on data accuracy?
- [ ] **Downtime**: What's your uptime guarantee?

### C. Pricing & Trial
- [ ] **Trial Period**: How long is the trial (14 days, 30 days)?
- [ ] **Trial Limits**: API call limits during trial?
- [ ] **Startup Pricing**: Any discounts for pre-launch platforms?
- [ ] **Pricing Tiers**: What do we get at different price points?
  - Current estimate: $2,000-10,000/month (from our research)
  - What's included at each tier?
- [ ] **Growth Scaling**: How does pricing scale as we grow?
- [ ] **Commitment**: Monthly vs annual contract?

### D. Support & Integration
- [ ] **Integration Support**: Do you provide technical support during integration?
- [ ] **Documentation Quality**: Do you have code examples (Python preferred)?
- [ ] **Webhook Support**: Can you push data to us vs polling?
- [ ] **Custom Features**: Can you customize data feeds for our needs?
- [ ] **SLA/Support Hours**: What support do we get?

### E. Competitive Differentiation
- [ ] **vs Sports Data IO**: What makes LS Sports better than our current provider?
- [ ] **vs The Odds API**: Coverage differences?
- [ ] **Unique Features**: What exclusive data do you offer?
- [ ] **Market Coverage**: Asian/European books (for arbitrage opportunities)?

---

## 2. Current Architecture Overview

### Existing Data Providers

**Current Setup:**
```
┌─────────────────────────────────────────────────┐
│          HybridOddsClient                       │
│  (Merges multiple providers for max coverage)  │
└─────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐    ┌────────▼──────────┐
│  The Odds API  │    │  Sports Data IO   │
│  (Standard)    │    │  (Fast + Weather) │
└────────────────┘    └───────────────────┘
```

**LS Sports Integration Goal:**
```
┌──────────────────────────────────────────────────────────┐
│               HybridOddsClient V2                        │
│    (3-way merge: Odds API + SportsDataIO + LS Sports)   │
└──────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌─────▼─────────┐
│ The Odds API │  │ SportsDataIO│  │   LS Sports   │
│  (Standard)  │  │(Weather Data)│  │(100+ Books)   │
└──────────────┘  └─────────────┘  └───────────────┘
```

### Key Files to Modify

1. **`backend/lsports_odds_client.py`** (NEW)
   - Create LS Sports adapter implementing same interface
   - Parse their API format into our standard format
   - Handle authentication and error handling

2. **`backend/hybrid_odds_client.py`** (MODIFY)
   - Add LS Sports as 3rd data source
   - Update merge logic to handle 3 providers
   - Add source tracking for LS Sports books

3. **`backend/config.py`** (MODIFY)
   - Add LS Sports API credentials
   - Add LS Sports configuration options

4. **`backend/.env`** (MODIFY)
   - Add LS Sports API key/credentials

---

## 3. Technical Implementation Plan

### Phase 1: API Client Creation (Day 1 - Post-Meeting)

**File:** `backend/lsports_odds_client.py`

**Requirements:**
```python
class LSportsOddsClient:
    """
    Adapter for LS Sports API - implements OddsAPIClient interface
    """

    def __init__(self):
        # Initialize with API credentials
        self.api_key = os.getenv("LSPORTS_API_KEY")
        self.base_url = "https://api.lsports.eu/v2"  # TBD from meeting

    async def get_live_games(self) -> List[dict]:
        """
        Fetch games from LS Sports OddService API
        Returns data in same format as OddsAPIClient
        """
        # Implementation based on their API structure
        pass

    async def get_game_scores(self) -> dict:
        """
        Fetch game scores from LS Sports
        """
        pass

    def _parse_bookmakers(self, lsports_data):
        """
        Convert LS Sports format to our standard bookmaker format:
        {
            'key': 'fanduel',
            'title': 'FanDuel',
            'source': 'LSports',
            'markets': [
                {
                    'key': 'spreads',
                    'outcomes': [...]
                }
            ]
        }
        """
        pass
```

**Key Tasks:**
- [ ] Understand LS Sports JSON response structure
- [ ] Map their sport keys to our sport keys (e.g., their NBA → our `basketball_nba`)
- [ ] Map their bookmaker names to our standardized keys
- [ ] Handle their odds format (American, Decimal, Fractional?)
- [ ] Parse spreads, totals, moneyline markets
- [ ] Add error handling and logging
- [ ] Add retry logic for API failures

### Phase 2: Integration with Hybrid Client (Day 2)

**File:** `backend/hybrid_odds_client.py`

**Changes:**
```python
class HybridOddsClient:
    def __init__(self):
        self.odds_api_client = OddsAPIClient()
        self.sportsdataio_client = SportsDataIOOddsClient()
        self.lsports_client = LSportsOddsClient()  # NEW

    async def get_live_games(self) -> List[dict]:
        # Fetch from all 3 providers concurrently
        sdi_task = self.sportsdataio_client.get_live_games()
        oddsapi_task = self.odds_api_client.get_live_games()
        lsports_task = self.lsports_client.get_live_games()  # NEW

        sdi_games, oddsapi_games, lsports_games = await asyncio.gather(
            sdi_task, oddsapi_task, lsports_task
        )

        # 3-way merge logic
        merged_games = self._merge_three_sources(
            sdi_games, oddsapi_games, lsports_games
        )

        return merged_games
```

**Merge Strategy:**
1. **Priority Order:**
   - LS Sports (most bookmakers, premium data)
   - Sports Data IO (weather data, channel info)
   - The Odds API (fallback coverage)

2. **Bookmaker Deduplication:**
   - If FanDuel appears in LS Sports AND Odds API, use LS Sports version
   - Track source for each bookmaker
   - Compare timestamps if available (use most recent)

3. **Game Matching:**
   - Match by team names (fuzzy matching)
   - Match by commence time (within 1 hour window)
   - Handle team name variations

### Phase 3: Configuration (Day 2)

**File:** `backend/config.py`

```python
# LS Sports API
LSPORTS_API_KEY = os.getenv("LSPORTS_API_KEY", "")
LSPORTS_API_BASE = "https://api.lsports.eu/v2"  # TBD
LSPORTS_ENABLED = os.getenv("LSPORTS_ENABLED", "true").lower() == "true"

# Data Provider Priority
PROVIDER_PRIORITY = ["lsports", "sportsdataio", "oddsapi"]  # NEW
```

**File:** `backend/.env`

```bash
# LS Sports API (Premium Provider)
LSPORTS_API_KEY=your_trial_key_here
LSPORTS_ENABLED=true
```

### Phase 4: Testing (Day 3)

**Test Plan:**

1. **Unit Tests** (`backend/test_lsports_client.py`)
   - [ ] Test API authentication
   - [ ] Test game parsing
   - [ ] Test bookmaker parsing
   - [ ] Test error handling
   - [ ] Test rate limiting

2. **Integration Tests** (`backend/test_hybrid_3way.py`)
   - [ ] Test 3-way merge logic
   - [ ] Test bookmaker deduplication
   - [ ] Test source tracking
   - [ ] Test fallback behavior (if LS Sports down)

3. **Live Testing**
   - [ ] Fetch live games during NBA/NHL game time
   - [ ] Compare odds across all 3 providers
   - [ ] Verify LS Sports provides more bookmakers
   - [ ] Check response times (<200ms target)
   - [ ] Monitor for duplicates

4. **Load Testing**
   - [ ] Test during high-traffic times (weekend NBA/NFL)
   - [ ] Verify all 3 providers can handle concurrent requests
   - [ ] Check memory usage with 3 providers active

---

## 4. Success Metrics

### A. Coverage Improvement
**Before LS Sports:**
- Avg bookmakers per game: 8-12
- Primary sources: 2 (Odds API + SportsDataIO)

**After LS Sports (Target):**
- Avg bookmakers per game: 20-30+
- Primary sources: 3 (Odds API + SportsDataIO + LS Sports)
- US sportsbook coverage: FanDuel, DraftKings, BetMGM, Caesars, BetRivers, etc.

### B. Speed & Reliability
- API response time: <200ms (95th percentile)
- Odds update frequency: Every 5-10 seconds
- Uptime: 99.5%+ across all providers
- Failover: If one provider down, others continue

### C. Data Quality
- More line shopping opportunities (more books = better prices)
- Arbitrage detection improvement (cross-book comparison)
- Better edge calculation (consensus from 20+ books vs 8-12)

---

## 5. Cost-Benefit Analysis

### Costs
- **LS Sports Subscription:** $2,000-10,000/month (estimated)
- **Development Time:** 3 days (1 developer)
- **Maintenance:** Ongoing monitoring and updates

### Benefits
- **User Value:** 2-3x more bookmakers = better line shopping
- **Competitive Edge:** Match or exceed OddsJam/Unabated coverage
- **Arbitrage Opportunities:** More books = more arb opportunities
- **Premium Positioning:** Justify $49/month Elite tier pricing
- **Data Redundancy:** 3 providers = better uptime

### ROI Calculation
If LS Sports helps convert **10 additional Elite subscribers** ($49/month):
- Revenue: 10 × $49 = **$490/month**
- If LS Sports costs $2,000/month, need **41 subscribers to break even**
- Target: 100+ Elite subscribers = $4,900/month revenue vs $2,000 cost = **$2,900 profit/month**

---

## 6. Post-Meeting Action Items

### Immediate (Day 1)
- [ ] Get LS Sports trial credentials
- [ ] Review API documentation
- [ ] Set up test environment
- [ ] Create `lsports_odds_client.py` skeleton

### Week 1
- [ ] Complete LS Sports adapter implementation
- [ ] Integrate into HybridOddsClient
- [ ] Write unit tests
- [ ] Test with live data during games

### Week 2
- [ ] Compare coverage vs existing providers
- [ ] Optimize merge logic for performance
- [ ] Add monitoring/logging for LS Sports
- [ ] Document integration for team

### Before Production
- [ ] Load test with all 3 providers
- [ ] Set up alerting for LS Sports downtime
- [ ] Create fallback strategy if LS Sports fails
- [ ] Review pricing tier and commit if trial successful

---

## 7. Questions to Ask During Integration

**If API Returns Errors:**
- What does HTTP 401 mean? (authentication issue)
- What does HTTP 429 mean? (rate limit exceeded)
- What's the retry-after header value?

**If Data Looks Wrong:**
- Are odds in American format (-110) or Decimal (1.91)?
- How are team names formatted? (Full names vs abbreviations)
- What timezone are commence times in?

**If Performance Issues:**
- Should we use webhooks instead of polling?
- Can we request specific sports only? (NBA, NFL, NHL vs all 100 sports)
- Is there a bulk endpoint for multiple games?

---

## 8. Comparison Matrix

| Feature | The Odds API | Sports Data IO | LS Sports | Winner |
|---------|--------------|----------------|-----------|--------|
| **Bookmaker Coverage** | ~15 US books | ~20 US books | 100+ global books | ⭐ LS Sports |
| **Update Speed** | 10-30 sec | 5-10 sec | <5 sec (TBD) | 🤔 TBD |
| **US Sports Coverage** | ✅ All major | ✅ All major | ✅ All major | ➖ Tie |
| **Weather Data** | ❌ No | ✅ Yes | ❌ No (TBD) | ⭐ SportsDataIO |
| **Price (est.)** | $30-250/mo | $200-500/mo | $2,000-10,000/mo | ⭐ Odds API |
| **API Documentation** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good | 🤔 TBD | 🤔 TBD |
| **Live Data** | ✅ Yes | ✅ Yes | ✅ Yes | ➖ Tie |
| **Historical Data** | ❌ Limited | ✅ Yes | 🤔 TBD | ⭐ SportsDataIO |
| **Best For** | Budget/backup | Primary + weather | Premium coverage | - |

---

## 9. Risk Mitigation

### Risk 1: LS Sports is Too Expensive
**Mitigation:**
- Start with 1-month trial/contract (not annual)
- Use only for Elite tier users (premium feature)
- Fallback to Odds API + SportsDataIO if ROI negative

### Risk 2: Integration Too Complex
**Mitigation:**
- Request detailed API docs and code examples before committing
- Ask for integration support during trial
- Build adapter layer to isolate LS Sports specific code

### Risk 3: Overlapping Data (No Value Add)
**Mitigation:**
- Test bookmaker coverage during trial
- If LS Sports doesn't add >10 unique bookmakers, cancel
- Track "unique bookmakers from LS Sports" metric

### Risk 4: Performance Degradation
**Mitigation:**
- Run performance benchmarks before/after
- Set timeout limits on LS Sports API calls (2 second max)
- Implement caching for LS Sports data (30 second TTL)

---

## 10. Success Criteria for Trial

**Must Have (Deal Breakers):**
- ✅ Adds at least **10 unique US bookmakers** not in other providers
- ✅ API response time <500ms (95th percentile)
- ✅ Uptime >99% during trial period
- ✅ Easy integration (working prototype in <3 days)

**Nice to Have:**
- ✅ Webhooks for push-based updates
- ✅ Historical odds data
- ✅ Asian/European bookmakers (for arbitrage)
- ✅ Startup pricing discount

**Evaluation Period:** 14-30 day trial
**Decision Point:** End of trial - commit or cancel based on metrics

---

## Next Steps After Meeting

1. **Get credentials** → Add to `.env`
2. **Review docs** → Understand API structure
3. **Build adapter** → `lsports_odds_client.py`
4. **Test live** → Fetch real game data
5. **Integrate** → Add to `HybridOddsClient`
6. **Evaluate** → Measure coverage improvement
7. **Decide** → Commit or cancel based on ROI

---

**Created:** November 9, 2025
**Owner:** Will Austin / Development Team
**Status:** Pre-Meeting Preparation
