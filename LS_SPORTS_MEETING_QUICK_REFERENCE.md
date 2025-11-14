# LS Sports Meeting - Quick Reference
**Date:** November 9, 2025 | **Company:** MAX EV SPORTS | **Contact:** Will Austin

---

## Who We Are
- **Platform:** Sports betting analytics and tools (like OddsJam/Unabated)
- **Stage:** Pre-launch, launching in 4-6 weeks
- **Tech Stack:** Python/FastAPI backend, React frontend
- **Target Users:** Sharp bettors, line shopping, arbitrage, edge detection
- **Current Traffic:** Pre-launch (expecting 1K-5K users in first month)

---

## Current Data Setup
**Providers:**
- The Odds API (~15 US bookmakers, $30-250/month)
- Sports Data IO (~20 US bookmakers, $200-500/month)

**Coverage:**
- Sports: NBA, NFL, NHL, NCAAB, NCAAF, MLB
- Markets: Spreads, Totals, Moneylines
- Update Frequency: 5-10 seconds

**Gap:** Need more bookmaker coverage (30-50+ books) to compete with OddsJam

---

## What We Need from LS Sports

### Must-Haves
1. **US Bookmaker Coverage**
   - FanDuel, DraftKings, BetMGM, Caesars, BetRivers, etc.
   - Target: 30+ US books (we currently have ~20)

2. **Real-Time Odds**
   - Live + pre-match
   - Update frequency: <10 seconds
   - Low latency: <200ms API response time

3. **Trial Access**
   - 14-30 day trial preferred
   - Sandbox environment for testing
   - Technical support during integration

4. **Clear Pricing**
   - Startup discount if possible
   - Monthly contract (not annual initially)
   - Usage-based or flat rate?

---

## Key Questions

### Technical (Priority 1)
- [ ] API base URL and authentication method?
- [ ] REST API or WebSocket or both?
- [ ] Rate limits for our expected usage (100K-500K calls/month)?
- [ ] Which US sportsbooks are covered? (list of specific books)
- [ ] Response format and sample payload?
- [ ] Code examples in Python?
- [ ] Webhook support for push notifications?

### Data Quality (Priority 2)
- [ ] Odds update frequency? (target: every 5-10 seconds)
- [ ] API response time / latency?
- [ ] Uptime SLA? (target: 99.5%+)
- [ ] Data accuracy guarantees?
- [ ] Historical odds data available?

### Business (Priority 3)
- [ ] Trial period length and API limits?
- [ ] Pricing tiers: what's included at each level?
- [ ] Startup pricing / discounts?
- [ ] Contract terms: monthly vs annual?
- [ ] Integration support provided?
- [ ] Expected onboarding timeline?

---

## Our Integration Plan

**Timeline:**
- Week 1: Build LS Sports API adapter
- Week 2: Integrate into existing hybrid client
- Week 3: Test and validate
- Week 4: Evaluate ROI and make decision

**Architecture:**
```
Current:        The Odds API + Sports Data IO = ~20 books
With LS Sports: The Odds API + Sports Data IO + LS Sports = 30-50+ books
```

**Technical Approach:**
- Create `lsports_odds_client.py` adapter
- Merge with existing providers
- Deduplicate bookmakers
- Track data source for each book

---

## Success Criteria for Trial

**Deal Breakers:**
- ✅ Must add at least 10 unique US bookmakers
- ✅ API response time <500ms (95th percentile)
- ✅ Uptime >99% during trial
- ✅ Easy integration (working in <3 days)

**Nice to Have:**
- Push notifications / webhooks
- Historical line movement data
- European/Asian books (for arbitrage)
- Startup pricing discount

---

## Budget Context

**Current Spend:**
- The Odds API: ~$100/month
- Sports Data IO: ~$300/month
- **Total: ~$400/month**

**LS Sports Budget:**
- Research shows: $2,000-10,000/month
- We can justify up to **$3,000/month** initially
- ROI: 41 Elite subscribers ($49/month) = break-even
- Target: 100+ Elite subscribers in 3 months

---

## Competitive Comparison

| Metric | OddsJam | Unabated | MAX EV (Current) | MAX EV (+ LS Sports) |
|--------|---------|----------|------------------|----------------------|
| Bookmakers | ~30 | ~25 | ~20 | **30-50+** ⭐ |
| Price | $49/mo | $99/mo | $49/mo | $49/mo |
| Edge Tools | ✅ | ✅ | ✅ | ✅ |
| Live Betting | ✅ | ❌ | ✅ | ✅ |

**Goal:** Match or exceed OddsJam coverage at same price point

---

## Decision Framework

**After Trial:**

✅ **Commit if:**
- Adds 15+ unique US bookmakers
- Response time <200ms
- Uptime >99%
- Pricing <$3,000/month
- Integration took <5 days

❌ **Cancel if:**
- Only adds <5 unique bookmakers (not worth it)
- Too slow (>500ms response time)
- Poor uptime (<95%)
- Too expensive (>$5,000/month with no discount)
- Integration nightmare (>10 days to implement)

---

## Action Items - Post Meeting

**Immediate:**
- [ ] Get trial API credentials
- [ ] Save API documentation
- [ ] Add credentials to `.env`
- [ ] Test authentication

**This Week:**
- [ ] Build `lsports_odds_client.py`
- [ ] Fetch live games successfully
- [ ] Count unique bookmakers
- [ ] Compare vs existing providers

**Next Week:**
- [ ] Integrate into `hybrid_odds_client.py`
- [ ] Run performance tests
- [ ] Evaluate coverage improvement
- [ ] Calculate ROI

**Decision Point:**
- [ ] End of trial: Commit or cancel

---

## Contact Info to Share

**Company:** MAX EV SPORTS
**Website:** https://max-ev-sports.com (pre-launch)
**Email:** willaustin@max-ev-sports.com
**Tech Stack:** Python 3.12, FastAPI, React, PostgreSQL
**Deployment:** AWS / Cloud hosting
**Expected Traffic:** 1K-5K users month 1, 10K+ by month 3

---

## Questions for LS Sports Team

**To Sales:**
- What's your recommended tier for our use case?
- Any startup/pre-launch discounts available?
- Can we start monthly and upgrade to annual later?
- What happens if we exceed rate limits?

**To Technical:**
- What's the best way to test the API? (sandbox vs production)
- Do you have Python SDK or code examples?
- What's your typical integration time for a platform like ours?
- Any gotchas we should know about?

**To Support:**
- What support is included during trial?
- What's the SLA for support tickets?
- Do you offer integration consulting?

---

## Red Flags to Watch For

⚠️ **Cancel meeting if:**
- They won't offer a trial
- They require long-term contract upfront
- They can't provide list of US bookmakers
- They can't provide API documentation

⚠️ **Negotiate harder if:**
- Pricing >$5,000/month with no volume discount
- Integration requires their professional services ($$$)
- They have poor API documentation
- No integration support during trial

---

## Print This Section - Meeting Notes

**Trial Details:**
- Trial Length: _______________
- API Key: _______________
- Rate Limit: _______________
- Restrictions: _______________

**Pricing:**
- Tier: _______________
- Monthly: $_______________
- Annual: $_______________
- Discount: _______________

**Technical:**
- Base URL: _______________
- Auth: _______________
- Sports Covered: _______________
- US Books Count: _______________

**Next Steps:**
1. _______________
2. _______________
3. _______________

**Follow-up Date:** _______________

---

**Prepared by:** Claude Code
**Date:** November 9, 2025
**Version:** 1.0
