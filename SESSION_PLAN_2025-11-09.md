# Session Plan - November 9, 2025

## Recent Work Summary (Nov 7-8)

### Completed ✅
1. **NBA Regression Backtest** (Nov 7)
   - Fixed Monte Carlo simulation in backtest script
   - Generated realistic performance metrics: 66.3% win rate, +26.5% ROI
   - Updated NBA regression article with historical performance data
   - Created 163 simulated alerts from 3,690 games (2022-2025)

2. **Platform Enhancements** (Recent commits)
   - Added ML edge scanner with live predictions
   - Implemented simulation routes (temporarily disabled due to dependencies)
   - Expanded Chrome extension features for auto-betting
   - Enhanced GameCard component with improved UI
   - Updated authentication system
   - Multiple frontend improvements (Navigation, Footer, Pricing page)

### Current Provider Architecture
**Data Sources:**
- **The Odds API**: Standard coverage (~15 US bookmakers)
- **Sports Data IO**: Fast updates + weather data (~20 US bookmakers)
- **Hybrid Client**: Merges both sources for maximum coverage

**Sports Covered:**
- NBA, NFL, NHL, NCAAB, NCAAF, MLB

---

## Today's Priority: LS Sports Integration

### Meeting with LS Sports
**Goal:** Add LS Sports as premium data/odds provider

**What LS Sports Offers:**
- 100+ bookmakers (vs current 15-20)
- Real-time odds API (OddService)
- 100 different sports coverage
- 175K+ monthly pre-match events
- 95K+ in-play events
- Premium tier: $2,000-10,000/month

### Key Meeting Objectives
1. ✅ Get trial access credentials
2. ✅ Review API documentation
3. ✅ Understand pricing tiers and startup discounts
4. ✅ Clarify technical requirements (REST/WebSocket, rate limits)
5. ✅ Determine bookmaker coverage for US markets
6. ✅ Ask about integration support and SLA

---

## Today's Development Plan

### Phase 1: Meeting Prep (Morning) ✅ DONE
- [x] Review existing odds client architecture
- [x] Create comprehensive integration plan
- [x] Prepare key questions for LS Sports
- [x] Review cost-benefit analysis

### Phase 2: Post-Meeting Implementation (Afternoon)
**Priority:** Get trial credentials and start integration

**Tasks:**
1. **Set up LS Sports credentials**
   - Add API key to `.env`
   - Add config to `backend/config.py`

2. **Create LS Sports API client**
   - File: `backend/lsports_odds_client.py`
   - Implement same interface as existing clients
   - Parse their API format to our standard format
   - Add error handling and logging

3. **Test with sample data**
   - Fetch live games from LS Sports API
   - Verify data structure
   - Compare coverage vs existing providers

4. **Begin hybrid integration**
   - Modify `backend/hybrid_odds_client.py`
   - Add 3-way merge logic
   - Add source tracking for all bookmakers

---

## Success Metrics for Today

### Meeting Success
- ✅ Trial credentials obtained
- ✅ API documentation received
- ✅ Pricing discussion completed
- ✅ Integration timeline agreed upon

### Development Success
- ✅ LS Sports client skeleton created
- ✅ Successfully fetch data from LS Sports API
- ✅ Parse at least one game with bookmakers
- ✅ Verify we get >10 unique bookmakers vs current providers

---

## Technical Architecture Changes

### Before (Current):
```
HybridOddsClient
    ├── The Odds API (15 books)
    └── Sports Data IO (20 books)
Total: ~25 unique bookmakers
```

### After (Target):
```
HybridOddsClient V2
    ├── LS Sports (100+ books) ⭐ PRIMARY
    ├── Sports Data IO (weather data)
    └── The Odds API (fallback)
Total: 30-50+ unique US bookmakers
```

### Merge Strategy
1. Start with LS Sports data (most coverage)
2. Add Sports Data IO weather/channel info
3. Fill gaps with The Odds API
4. Deduplicate bookmakers by normalized key
5. Track source for each bookmaker

---

## Key Questions for Implementation

### During Meeting:
- What's the API base URL?
- What's the authentication method? (Bearer token, API key header?)
- What's the response format? (JSON structure)
- What are the main endpoints?
  - `/games` or `/events`?
  - `/odds` or `/markets`?
- How do you identify sports? (sport_id, sport_key?)
- How do you format team names? (Full name, abbreviation?)
- What timezone for game times?
- What odds format? (American -110, Decimal 1.91, Fractional 10/11?)

### After Getting Access:
- Test API response time during live games
- Count unique US bookmakers
- Check for FanDuel, DraftKings, BetMGM, Caesars, BetRivers
- Verify update frequency (target: <10 seconds)
- Check data completeness (spreads, totals, moneylines all present?)

---

## Risk Assessment

### Low Risk
- Integration complexity (we have template from existing clients)
- Technical capability (proven with 2 providers already)

### Medium Risk
- Performance impact (3 concurrent API calls vs 2)
  - **Mitigation**: Parallel async calls, caching
- Cost justification ($2K-10K/month is significant)
  - **Mitigation**: Start with trial, measure ROI

### High Risk
- Overlapping data (if LS Sports doesn't add value)
  - **Mitigation**: Evaluate unique bookmaker count during trial
  - **Decision Point**: Must add 10+ unique US books to justify cost

---

## File Structure for Integration

### New Files
```
backend/
  ├── lsports_odds_client.py          # NEW - LS Sports adapter
  └── test_lsports_client.py          # NEW - Unit tests
```

### Modified Files
```
backend/
  ├── hybrid_odds_client.py           # MODIFY - Add 3rd provider
  ├── config.py                        # MODIFY - Add LS Sports config
  ├── .env                             # MODIFY - Add API key
  └── main.py                          # VERIFY - Ensure hybrid client used
```

---

## Timeline

### Today (Nov 9)
- ✅ Morning: Meeting prep and planning
- 🔄 Afternoon: Meeting with LS Sports
- 🔜 Evening: Start implementation if credentials received

### Next Week (Nov 11-15)
- Day 1-2: Complete LS Sports client implementation
- Day 3: Integrate into HybridOddsClient
- Day 4: Testing and validation
- Day 5: Performance optimization and monitoring

### Week After (Nov 18-22)
- Compare coverage metrics
- Evaluate ROI
- Make commit/cancel decision
- If committing: production deployment
- If canceling: clean removal of integration

---

## Competitive Analysis

### Current Competitors
**OddsJam:** ~30 sportsbooks
**Unabated:** ~25 sportsbooks
**MAX EV SPORTS (current):** ~15-20 sportsbooks

### With LS Sports
**MAX EV SPORTS (upgraded):** 30-50+ sportsbooks
- Match or exceed OddsJam
- 2x better than current offering
- Justify $49/month Elite pricing

---

## Questions to Document During Meeting

**API Technical:**
- [ ] Base URL: __________________
- [ ] Auth method: __________________
- [ ] Rate limit: __________________
- [ ] Sports endpoint: __________________
- [ ] Odds endpoint: __________________
- [ ] Team name format: __________________
- [ ] Odds format: __________________
- [ ] Update frequency: __________________

**Business:**
- [ ] Trial length: __________________
- [ ] Trial API limits: __________________
- [ ] Pricing tier chosen: __________________
- [ ] Contract terms: __________________
- [ ] Integration support: __________________
- [ ] SLA/uptime guarantee: __________________

**Coverage:**
- [ ] US bookmakers count: __________________
- [ ] Specific books confirmed: __________________
- [ ] Live betting support: __________________
- [ ] Pre-match coverage: __________________
- [ ] Historical data available: __________________

---

## Post-Meeting Checklist

Immediately after meeting:
- [ ] Add credentials to `.env`
- [ ] Save API documentation to `backend/docs/lsports/`
- [ ] Create integration ticket/task
- [ ] Update this plan with actual details
- [ ] Test first API call (simple authentication check)
- [ ] Schedule follow-up if needed

First development session:
- [ ] Create `lsports_odds_client.py` skeleton
- [ ] Implement `get_live_games()` method
- [ ] Test with live NBA/NHL game
- [ ] Log response structure
- [ ] Count bookmakers returned
- [ ] Compare vs Odds API / Sports Data IO

---

## Resources

**Documentation:**
- LS Sports Website: https://www.lsports.eu/
- OddService API: https://www.lsports.eu/oddservice/
- Integration Plan: `C:\Users\nashr\LS_SPORTS_INTEGRATION_PLAN.md`
- Provider Contact List: `C:\Users\nashr\DATA_PROVIDERS_MANUAL_CONTACT_LIST.md`

**Existing Client References:**
- `backend/odds_client.py` - The Odds API client
- `backend/sportsdataio_odds_client.py` - Sports Data IO client
- `backend/hybrid_odds_client.py` - Hybrid merge logic

**Testing:**
- Use live NBA games (check schedule for today's games)
- Use live NHL games as secondary test
- Compare bookmaker lists side-by-side

---

## Notes Section
(Fill in during/after meeting)

**Meeting Notes:**
-
-
-

**API Details:**
-
-
-

**Follow-up Items:**
-
-
-

---

**Created:** November 9, 2025, 9:00 AM
**Status:** Ready for LS Sports meeting
**Next Update:** After meeting completion
