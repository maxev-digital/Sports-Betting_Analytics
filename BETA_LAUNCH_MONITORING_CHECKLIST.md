# Beta Launch Monitoring Checklist
## November 5-10, 2025

---

## ⏰ DAILY TASKS (Check Every Morning)

### 1. X Ads Campaign Status
- [ ] Login to https://ads.twitter.com
- [ ] Check if approved (first 24 hours only)
- [ ] Check spend vs budget ($50/day cap)
- [ ] Note: Impressions, Clicks, CTR, CPC

**Target Metrics:**
- CPC: Should be 3-10¢
- CTR: Should be >1%
- Daily spend: ~$50

---

### 2. Twitter Bot Status
- [ ] Check @GTE_APW timeline for new posts
- [ ] Should see 4 posts per day (every 6 hours)
- [ ] Verify member count is incrementing in tweets

**Bot Schedule:**
- Every 6 hours automatically
- Runs until Sunday 11/10 midnight CST

**If bot stopped:**
```bash
cd /c/Users/nashr/backend
python twitter_retweet_bot.py
```

---

### 3. Conversion Tracking
- [ ] Login to ads.twitter.com → Events Manager
- [ ] Check pixel events:
  - PageView (should be hundreds/day)
  - InitiateCheckout (clicks on Subscribe)
  - Purchase (completed signups)
  - Lead (waitlist signups)

**Expected After Campaign Starts:**
- InitiateCheckout: 20-40% of clicks
- Purchase: 5-20% of clicks

---

### 4. Beta Signups
- [ ] Check production database for new subscriptions
- [ ] Or check Stripe dashboard for new customers
- [ ] Compare to member count on pricing page

**Command to check:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "sqlite3 /root/sporttrader/backend/subscriptions.db 'SELECT COUNT(*) FROM subscriptions WHERE tier=\"beta\" AND status=\"active\"'"
```

---

## 📊 PERFORMANCE TARGETS (By Sunday)

### Conservative Goals:
- **Total Clicks:** 5,000
- **Conversion Rate:** 20%
- **New Beta Signups:** 1,000
- **Total Spend:** $250
- **Revenue:** $9,990 MRR
- **ROI:** 3,896%

### Stretch Goals:
- **Total Clicks:** 8,000
- **Conversion Rate:** 40%
- **New Beta Signups:** 3,200
- **Total Spend:** $250
- **Revenue:** $31,968 MRR
- **ROI:** 12,687%

---

## 🚨 RED FLAGS (Take Action If You See These)

### X Ads Issues:
- ❌ **CPC above 15¢** → Pause campaign, adjust targeting
- ❌ **CTR below 0.5%** → Change ad copy, test new creative
- ❌ **No conversions after 100 clicks** → Check pixel, verify pricing page works
- ❌ **Daily spend over $60** → Check budget settings

### Twitter Bot Issues:
- ❌ **No posts for 8+ hours** → Restart bot script
- ❌ **Error messages in console** → Check Twitter API limits
- ❌ **Member count stuck** → API endpoint may be down (uses fallback)

### Website Issues:
- ❌ **Pricing page not loading** → Check server status
- ❌ **Subscribe button not working** → Check Stripe integration
- ❌ **Pixel not firing** → Check browser console for errors

---

## 📈 OPTIMIZATION OPPORTUNITIES

### If CTR is Low (<1%):
- Change ad headline
- Add more urgency ("24h left")
- Test different ROI claims
- Add image/video if text-only

### If CPC is High (>10¢):
- Narrow targeting (remove lowest-engaged followers)
- Lower max bid
- Improve ad relevance score

### If Conversion Rate is Low (<10%):
- A/B test pricing page headlines
- Add more social proof
- Simplify checkout flow
- Add live chat support

---

## 🎯 WEEKEND PUSH (Saturday-Sunday)

### Saturday Actions:
- [ ] Post manual hype tweet (boost $10)
- [ ] Increase X Ads budget to $75/day if ROAS positive
- [ ] Send email to waitlist (if any signups)
- [ ] Update ad copy: "36h left" → "24h left"

### Sunday Actions:
- [ ] Morning: Final push tweet "12h left"
- [ ] Noon: Update ad "FINAL HOURS"
- [ ] 6pm: Last call tweet
- [ ] Midnight: Let bot post "BETA CLOSED" automatically
- [ ] Pause X Ads campaign manually

---

## 📞 CONTACTS & SUPPORT

### If Something Breaks:
- **X Ads Support:** ads.twitter.com → Help Center
- **Stripe Issues:** dashboard.stripe.com → Support
- **Server Issues:** SSH to 148.230.87.135
- **Twitter API Issues:** developer.twitter.com

### Quick Fixes:
```bash
# Restart Twitter bot
cd /c/Users/nashr/backend
python twitter_retweet_bot.py

# Check server status
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl status sporttrader"

# Restart backend
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"

# Check logs
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "journalctl -u sporttrader -n 50"
```

---

## ✅ END-OF-CAMPAIGN ANALYSIS (Monday Nov 11)

### Calculate Final Metrics:
- [ ] Total impressions
- [ ] Total clicks
- [ ] Average CPC
- [ ] Total conversions
- [ ] Conversion rate
- [ ] Total spend
- [ ] Total revenue (beta signups × $9.99)
- [ ] ROI percentage
- [ ] Cost per acquisition

### Export Data:
- [ ] Download X Ads campaign report (CSV)
- [ ] Export pixel events from Events Manager
- [ ] Export beta subscriber list from database
- [ ] Save screenshots of dashboards

### Post-Mortem Questions:
- What ad creative performed best?
- Which competitor followers converted highest?
- What time of day had best CTR?
- What should we do differently for full launch?

---

*Created: November 5, 2025*
*Campaign Duration: Nov 5-10, 2025 (5 days)*
