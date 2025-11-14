# Twitter Automation - Implementation Checklist

Use this checklist to implement Twitter automation step-by-step.

---

## Pre-Implementation (10 minutes)

- [ ] **1.1** Go to [developer.twitter.com](https://developer.twitter.com/en/portal/dashboard)
- [ ] **1.2** Sign in with Twitter account
- [ ] **1.3** Click "Sign up for Free Account"
- [ ] **1.4** Fill application (use case: sports analytics bot)
- [ ] **1.5** Wait for approval (usually instant)

---

## Get API Credentials (5 minutes)

- [ ] **2.1** Create new project: "MAX-EV Sports Bot"
- [ ] **2.2** Create app: "max-ev-sports-alerts"
- [ ] **2.3** Copy API Key (Consumer Key)
- [ ] **2.4** Copy API Secret (Consumer Secret)
- [ ] **2.5** Generate Access Token
- [ ] **2.6** Copy Access Token
- [ ] **2.7** Copy Access Token Secret
- [ ] **2.8** Generate Bearer Token
- [ ] **2.9** Copy Bearer Token
- [ ] **2.10** Save all 5 credentials securely

---

## Local Setup (5 minutes)

- [ ] **3.1** Open `backend/.env` file
- [ ] **3.2** Add `TWITTER_API_KEY=your_api_key`
- [ ] **3.3** Add `TWITTER_API_SECRET=your_api_secret`
- [ ] **3.4** Add `TWITTER_ACCESS_TOKEN=your_access_token`
- [ ] **3.5** Add `TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret`
- [ ] **3.6** Add `TWITTER_BEARER_TOKEN=your_bearer_token`
- [ ] **3.7** Save `.env` file

---

## Install Dependencies (2 minutes)

- [ ] **4.1** Open terminal
- [ ] **4.2** `cd C:\Users\nashr\backend`
- [ ] **4.3** `venv\Scripts\activate`
- [ ] **4.4** `pip install tweepy python-dotenv`
- [ ] **4.5** `pip freeze > requirements.txt`
- [ ] **4.6** Verify: `pip list | grep tweepy`

---

## Integrate with main.py (5 minutes)

- [ ] **5.1** Open `backend/main.py`
- [ ] **5.2** Add imports (top of file):
  ```python
  from twitter_alert_service import TwitterAlertService
  from routes import twitter_admin
  ```
- [ ] **5.3** Add global variable after `app = FastAPI()`:
  ```python
  twitter_service_instance = None
  ```
- [ ] **5.4** Add startup event:
  ```python
  @app.on_event("startup")
  async def startup_twitter_service():
      global twitter_service_instance
      odds_api_key = os.getenv('ODDS_API_KEY')
      twitter_service_instance = TwitterAlertService(odds_api_key)
      twitter_admin.set_twitter_service(twitter_service_instance)
      asyncio.create_task(twitter_service_instance.start_monitoring())
  ```
- [ ] **5.5** Add route after other `app.include_router()` calls:
  ```python
  app.include_router(twitter_admin.router)
  ```
- [ ] **5.6** Save `main.py`

---

## Local Testing (10 minutes)

- [ ] **6.1** Start backend: `python main.py`
- [ ] **6.2** Check logs for "✅ Twitter authenticated"
- [ ] **6.3** Test health endpoint:
  ```bash
  curl http://localhost:8000/
  ```
- [ ] **6.4** Should see `"twitter_enabled": true`
- [ ] **6.5** Check Twitter status:
  ```bash
  curl http://localhost:8000/api/admin/twitter/status
  ```
- [ ] **6.6** Should see config and stats
- [ ] **6.7** Send test tweet:
  ```bash
  curl -X POST http://localhost:8000/api/admin/twitter/test-tweet \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Testing from local 🚀\"}"
  ```
- [ ] **6.8** Check your Twitter - tweet should appear
- [ ] **6.9** Enable automation:
  ```bash
  curl -X POST http://localhost:8000/api/admin/twitter/enable
  ```
- [ ] **6.10** Trigger scan:
  ```bash
  curl -X POST http://localhost:8000/api/admin/twitter/trigger-scan
  ```
- [ ] **6.11** Check stats:
  ```bash
  curl http://localhost:8000/api/admin/twitter/stats
  ```

---

## Production Deployment (15 minutes)

- [ ] **7.1** Upload files to VPS:
  ```bash
  scp -i ~/.ssh/hostinger_vps backend/twitter_integration.py root@148.230.87.135:/root/sporttrader/backend/
  scp -i ~/.ssh/hostinger_vps backend/twitter_alert_service.py root@148.230.87.135:/root/sporttrader/backend/
  scp -i ~/.ssh/hostinger_vps backend/routes/twitter_admin.py root@148.230.87.135:/root/sporttrader/backend/routes/
  ```
- [ ] **7.2** SSH into VPS:
  ```bash
  ssh root@148.230.87.135
  ```
- [ ] **7.3** Install dependencies:
  ```bash
  cd /root/sporttrader/backend
  source venv/bin/activate
  pip install tweepy python-dotenv
  ```
- [ ] **7.4** Add credentials to .env:
  ```bash
  nano /root/sporttrader/backend/.env
  ```
  Paste all 5 Twitter credentials
- [ ] **7.5** Update main.py:
  ```bash
  nano /root/sporttrader/backend/main.py
  ```
  Add integration code (imports, startup, route)
- [ ] **7.6** Save and exit (`Ctrl+X`, `Y`, `Enter`)
- [ ] **7.7** Restart service:
  ```bash
  systemctl restart sporttrader
  ```
- [ ] **7.8** Check status:
  ```bash
  systemctl status sporttrader
  ```
- [ ] **7.9** Check logs:
  ```bash
  journalctl -u sporttrader -n 50 | grep -i twitter
  ```
- [ ] **7.10** Should see "✅ Twitter authenticated"

---

## Production Verification (5 minutes)

- [ ] **8.1** Test health endpoint:
  ```bash
  curl http://localhost:8000/
  ```
- [ ] **8.2** Check Twitter status:
  ```bash
  curl http://localhost:8000/api/admin/twitter/status
  ```
- [ ] **8.3** Send test tweet from production:
  ```bash
  curl -X POST http://localhost:8000/api/admin/twitter/test-tweet \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Testing from production 🚀\"}"
  ```
- [ ] **8.4** Verify tweet appears on Twitter
- [ ] **8.5** Check from public URL:
  ```bash
  curl https://max-ev-sports.com/api/admin/twitter/status
  ```

---

## Initial Configuration (5 minutes)

- [ ] **9.1** Review default settings:
  ```bash
  curl https://max-ev-sports.com/api/admin/twitter/config
  ```
- [ ] **9.2** Adjust thresholds if needed (start conservative):
  ```bash
  curl -X PUT https://max-ev-sports.com/api/admin/twitter/config \
    -H "Content-Type: application/json" \
    -d '{
      "min_arbitrage_profit": 1.0,
      "min_steam_consensus": 70,
      "max_tweets_per_hour": 10
    }'
  ```
- [ ] **9.3** Enable automation:
  ```bash
  curl -X POST https://max-ev-sports.com/api/admin/twitter/enable
  ```
- [ ] **9.4** Trigger first scan:
  ```bash
  curl -X POST https://max-ev-sports.com/api/admin/twitter/trigger-scan
  ```
- [ ] **9.5** Monitor logs:
  ```bash
  journalctl -u sporttrader -f | grep -i twitter
  ```

---

## Monitoring (First 24 Hours)

- [ ] **10.1** Check stats every 4 hours:
  ```bash
  curl https://max-ev-sports.com/api/admin/twitter/stats
  ```
- [ ] **10.2** Review recent tweets:
  ```bash
  curl https://max-ev-sports.com/api/admin/twitter/recent-tweets?limit=20
  ```
- [ ] **10.3** Check Twitter analytics on twitter.com
- [ ] **10.4** Monitor for errors in logs:
  ```bash
  journalctl -u sporttrader -n 100 | grep -i "twitter.*error"
  ```
- [ ] **10.5** Verify no rate limit issues
- [ ] **10.6** Check follower engagement (likes, retweets)
- [ ] **10.7** Adjust thresholds based on performance
- [ ] **10.8** Document any issues in notes

---

## Optimization (After 7 Days)

- [ ] **11.1** Review 7-day statistics
- [ ] **11.2** Calculate engagement rate per alert type
- [ ] **11.3** Identify best-performing alert types
- [ ] **11.4** Adjust thresholds to optimize:
  - Increase for low-engagement types
  - Decrease for high-engagement types
- [ ] **11.5** Update configuration
- [ ] **11.6** Monitor for another 7 days
- [ ] **11.7** Iterate based on results

---

## Troubleshooting Checklist

If something isn't working, check these in order:

### Service Not Starting
- [ ] Check credentials in .env (all 5 present?)
- [ ] Verify tweepy installed: `pip list | grep tweepy`
- [ ] Check imports in main.py (typos?)
- [ ] View error logs: `journalctl -u sporttrader -n 50`

### No Tweets Posting
- [ ] Is automation enabled? Check status endpoint
- [ ] Are alerts being detected? Trigger manual scan
- [ ] Check thresholds (too strict?)
- [ ] Verify rate limit not exceeded
- [ ] Check Twitter API status: status.twitter.com

### Authentication Errors
- [ ] Regenerate tokens at developer.twitter.com
- [ ] Update .env with new tokens
- [ ] Restart service: `systemctl restart sporttrader`
- [ ] Check logs for specific error

### Rate Limit Errors
- [ ] Check tweets posted in last 3 hours
- [ ] Lower max_tweets_per_hour setting
- [ ] Wait for rate limit to reset (3 hours)
- [ ] Consider upgrading Twitter API plan

---

## Success Criteria

Your Twitter automation is working correctly when:

- ✅ Status endpoint shows `"enabled": true`
- ✅ Status endpoint shows `"authenticated": true`
- ✅ Test tweets post successfully
- ✅ Logs show "🔍 Scanning for alerts..." every 5 minutes
- ✅ Logs show "✅ Posted: https://twitter.com/..." when alerts found
- ✅ No error messages in logs
- ✅ Database `twitter_alerts.db` is being populated
- ✅ Stats show increasing tweet count
- ✅ Success rate is >95%
- ✅ Tweets appear on your Twitter timeline
- ✅ Followers are engaging with tweets

---

## Maintenance Schedule

### Daily
- Check stats via API
- Review recent tweets
- Monitor for errors

### Weekly
- Analyze engagement rates
- Adjust thresholds
- Review follower growth

### Monthly
- Deep dive into alert performance
- Optimize configuration
- Check API usage/costs

---

## Completed!

When all checkboxes are marked:

🎉 **Congratulations!** Your Twitter automation is fully operational.

Your bet alerts will now automatically post to Twitter, helping you:
- Build an engaged following
- Establish authority in sports betting
- Drive traffic to your platform
- Showcase your edge-finding capabilities

---

**Need Help?**

Refer to these documents:
- **TWITTER_AUTOMATION_SETUP.md** - Complete setup guide
- **TWITTER_AUTOMATION_SUMMARY.md** - Quick reference
- **TWITTER_INTEGRATION_MAIN_PY.md** - Integration code

**Questions?** Check the troubleshooting sections in the setup guide.

---

**Created by MAX-EV Sports**
**Date:** 2025-11-12
