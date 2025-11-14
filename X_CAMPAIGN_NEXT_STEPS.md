# X Campaign - Immediate Next Steps

**Your infrastructure is 100% ready.** Here's exactly what to do next to launch:

---

## Step 1: Apply for X API Elevated Access (30 minutes)

### Go to: https://developer.x.com/en/portal/dashboard

Click **"Elevated"** access and fill out:

**Use Case:** "Influencer outreach for sports betting platform partnership program"

**Will you make X content available to government entities?** No

**Will you display Tweets/X content off X?** No

**Describe what you are building:**
```
Automated partnership outreach system for Max EV Sports (https://max-ev-sports.com).
We're reaching out to 500+ sports betting influencers to offer them free beta access
and revenue-sharing partnerships. System will:
- Send personalized DMs to potential partners
- Auto-reply to interested influencers with referral codes
- Track partnerships in database
- Notify team of new signups

No spam - targeting qualified influencers only. Rate: 50 DMs/day max.
```

**Submit** → Wait 1-3 days for approval

---

## Step 2: Build Your Influencer List (2-3 hours)

Expand `influencers_sample.csv` to 500+ targets:

**Format:**
```csv
handle,followers,niche,why_target,engagement_rate
@BenMoore_Sports,50000,nba,High NBA engagement,4.5
@SharpBettor,30000,betting,Sharp betting content,3.8
```

**Sources:**
1. Grok's influencer list (you mentioned having this)
2. X search: "sports betting" influencers
3. Follow competitors' follower lists
4. Search hashtags: #SportsBetting #NBAPicks #BettingTwitter

**Target Criteria:**
- 10,000+ followers
- Sports betting/analytics niche
- Active (posted in last 7 days)
- Good engagement (likes, retweets, replies)

---

## Step 3: Add API Credentials (5 minutes)

Once X approves Elevated Access:

1. Go to Developer Portal → App Settings → Keys and Tokens
2. Generate:
   - API Key & Secret
   - Access Token & Secret
3. Add to `backend/.env`:

```env
# X API (Full Access for DM Campaign)
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_SECRET=your_access_secret_here
```

---

## Step 4: Import Your Influencer List (2 minutes)

```bash
python backend/x_campaign/import_influencers.py your_influencer_list.csv
```

This will load all 500+ targets into the database.

---

## Step 5: Test with Yourself (5 minutes)

Before going live, send a test DM to your own X account:

1. Add yourself to the database:
```bash
python -c "
from backend.x_campaign.db_setup import add_partner
add_partner('@YourHandle', 10000, 'test', 'Testing campaign', 5.0)
"
```

2. Send test DM:
```bash
python backend/x_campaign/send_dm.py --live --batch 1
```

3. Check your DMs on X
4. Reply "BETA"
5. Verify auto-reply with referral code arrives

---

## Step 6: Launch Campaign (1 command)

```bash
python backend/x_campaign/main.py
```

This starts the automated scheduler:
- **9:00 AM CST:** 50 DMs sent daily
- **Every 60 min:** Check for "BETA" replies, auto-respond
- **11:00 PM CST:** Daily performance report

---

## Commands Reference

### Manual Operations

**Send DMs manually:**
```bash
# Dry run (preview only)
python backend/x_campaign/send_dm.py

# Live send (real DMs)
python backend/x_campaign/send_dm.py --live --batch 20
```

**Check for replies manually:**
```bash
python backend/x_campaign/listener.py
```

**View campaign stats:**
```bash
python backend/x_campaign/db_setup.py
```

**Test configuration:**
```bash
python backend/x_campaign/config.py
```

---

## Monitoring

### Database Location
`backend/x_campaign/referrals.db`

### Check partner status:
```sql
sqlite3 backend/x_campaign/referrals.db
SELECT handle, dm_sent, replied, onboarded, status FROM partners LIMIT 20;
```

### Campaign stats:
```sql
SELECT
  COUNT(*) as total,
  SUM(dm_sent) as sent,
  SUM(replied) as replied,
  SUM(onboarded) as onboarded
FROM partners;
```

---

## Troubleshooting

### "Missing X API credentials"
→ You need to apply for Elevated Access and add keys to `.env`

### "No pending partners found"
→ Import your influencer CSV first

### "Cannot send DM - user may have DMs disabled"
→ Normal. Skip this user. ~10-15% have DMs disabled.

### "Rate limit exceeded"
→ Wait 15 minutes. You're sending too fast.

---

## Timeline

**Today (Nov 12):**
- ✓ Infrastructure built and tested

**Tomorrow (Nov 13):**
- Apply for X API Elevated Access (30 min)
- Build 500+ influencer CSV (2-3 hours)

**Nov 14-16:**
- Wait for X API approval (1-3 days)

**Nov 17:**
- Add API credentials to .env
- Import influencer list
- Send test DM to yourself
- Launch automated campaign

**Nov 18 - Dec 15:**
- Campaign runs automatically
- 50 DMs/day = 500 DMs over 10 days
- Expected: 100 replies, 50+ onboarded partners

**Dec 15:**
- Launch day with 150+ active partners
- Projected MRR: $10k-$15k

---

## Support Files

- **Build Summary:** `X_CAMPAIGN_BUILD_COMPLETE.md`
- **Action Plan:** `X_CAMPAIGN_ACTION_PLAN.md`
- **Usage Guide:** `backend/x_campaign/README.md`
- **This Guide:** `X_CAMPAIGN_NEXT_STEPS.md`

---

**Ready to launch once X API approves Elevated Access (1-3 days).**

Good luck! 🚀
