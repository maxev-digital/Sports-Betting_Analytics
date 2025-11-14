# Twitter Automation Setup Guide

Complete guide to setting up automated bet alert posting to Twitter for MAX-EV Sports.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Getting Twitter API Credentials](#getting-twitter-api-credentials)
4. [Environment Setup](#environment-setup)
5. [Installing Dependencies](#installing-dependencies)
6. [Starting the Service](#starting-the-service)
7. [API Endpoints](#api-endpoints)
8. [Configuration](#configuration)
9. [Tweet Examples](#tweet-examples)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Twitter automation system automatically posts high-value bet alerts from your platform to Twitter, including:

- **Arbitrage opportunities** (risk-free profit)
- **Steam moves** (sharp money indicators)
- **Middle opportunities** (chance to win both bets)
- **Model predictions** (high-confidence ML predictions)
- **Strategy alerts** (Quarter Reversal, Favorite Comeback, etc.)

**Key Features:**
- Intelligent filtering (only posts high-value alerts)
- Duplicate prevention (won't post same alert twice)
- Rate limiting (respects Twitter API limits)
- Admin controls via API
- Statistics tracking
- Auto-generated engaging tweets with emojis

---

## Features

### Alert Types Supported

| Alert Type | Description | Example Tweet |
|------------|-------------|---------------|
| **Arbitrage** | Risk-free profit by betting both sides | "🚨 ARBITRAGE ALERT 🏀\nLakers @ Warriors\nTOTALS: 2.1% GUARANTEED PROFIT" |
| **Steam Move** | Multiple books moving lines simultaneously | "🔥 STEAM MOVE 🏒\nBruins @ Leafs\nTOTALS: 📈 1.5 pts\n75% of books moved!" |
| **Middle** | Gap between lines (chance to win both) | "⚡ MIDDLE OPPORTUNITY 🏀\nHeat @ Celtics\n3.0 pt GAP - Win BOTH!" |
| **Model Predictions** | High-confidence ML predictions | "🔥 HIGH CONFIDENCE 🏀\nWarriors @ Lakers\nUNDER 228.5\nEdge: +7.2%" |
| **Strategy Alerts** | Quarter Reversal, Favorite Comeback | "🔄 NBA Quarter Reversal 🏀\nQ2 hot start detected\nBet UNDER 2H" |

### Smart Filtering

Only posts alerts that meet your thresholds:
- Arbitrage: Minimum 0.5% profit
- Steam Moves: Minimum 50% book consensus
- Middles: Minimum 1.0 pt gap (NHL), 3.0 pt gap (NBA)
- Model Predictions: Minimum 5% edge, HIGH/CRITICAL confidence only
- Strategy Alerts: HIGH/CRITICAL confidence only

### Rate Limiting

- **Twitter API Limit:** 300 tweets per 3 hours
- **Our Default:** 20 tweets per hour (conservative)
- **Configurable:** Adjust via admin API

---

## Getting Twitter API Credentials

### Step 1: Apply for Twitter Developer Account

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign in with your Twitter account
3. Click **"Sign up for Free Account"**
4. Fill out the application:
   - **Use case:** Sports analytics and automated alerts
   - **Description:** "Automated betting alerts for sports analytics platform"
   - **Will your app use Tweet, Retweet, Like, Follow, or Direct Message functionality?** Yes
   - **Do you plan to analyze Twitter data?** No

**Approval Time:** Usually instant for basic access, up to 24 hours for elevated access.

### Step 2: Create a Twitter App

1. In the Developer Portal, click **"+ Create Project"**
2. **Project Name:** MAX-EV Sports Bot
3. **Use Case:** Making a bot
4. **Project Description:** Automated sports betting alerts
5. Click **"Create App"**
6. **App Name:** max-ev-sports-alerts (must be unique)

### Step 3: Get API Keys

After creating the app, you'll see:

**API Key (Consumer Key)**
```
Example: xvz1evFS4wEEPTGEFPHBog
```

**API Secret (Consumer Secret)**
```
Example: L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg
```

**IMPORTANT:** Save these immediately - Twitter only shows them once!

### Step 4: Generate Access Tokens

1. In your app settings, click **"Keys and tokens"** tab
2. Under **"Authentication Tokens"**, click **"Generate"**
3. Save:

**Access Token**
```
Example: 1234567890-AbC1234567890DefGhiJklMnoPqrStUvWxYz
```

**Access Token Secret**
```
Example: AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
```

### Step 5: Get Bearer Token

1. Still in **"Keys and tokens"** tab
2. Under **"Bearer Token"**, click **"Generate"**
3. Save:

**Bearer Token**
```
Example: AAAAAAAAAAAAAAAAAAAAAG%2FGEAAAAAAlNGM4ZGQ4N2I0OGUy...
```

---

## Environment Setup

### Add to `.env` File

Add these 5 credentials to your `backend/.env` file:

```bash
# Twitter API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# Existing credentials (keep these)
ODDS_API_KEY=your_existing_odds_key
```

**Example:**
```bash
TWITTER_API_KEY=xvz1evFS4wEEPTGEFPHBog
TWITTER_API_SECRET=L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg
TWITTER_ACCESS_TOKEN=1234567890-AbC1234567890DefGhiJklMnoPqrStUvWxYz
TWITTER_ACCESS_TOKEN_SECRET=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAG%2FGEAAAAAAlNGM4ZGQ4N2I0OGUy...
```

---

## Installing Dependencies

The Twitter bot requires the `tweepy` library:

```bash
# Activate virtual environment
cd C:\Users\nashr\backend
venv\Scripts\activate

# Install tweepy
pip install tweepy python-dotenv

# Save to requirements.txt
pip freeze > requirements.txt
```

---

## Starting the Service

### Option 1: Start as Background Service (Recommended)

Add to `backend/main.py`:

```python
import asyncio
from twitter_alert_service import TwitterAlertService
from routes import twitter_admin

# Initialize Twitter service (at app startup)
@app.on_event("startup")
async def startup_event():
    # Start Twitter alert service in background
    odds_api_key = os.getenv('ODDS_API_KEY')
    twitter_service = TwitterAlertService(odds_api_key)

    # Set global reference for admin API
    twitter_admin.set_twitter_service(twitter_service)

    # Start monitoring loop in background
    asyncio.create_task(twitter_service.start_monitoring())

    logger.info("✅ Twitter alert service started")

# Include admin routes
app.include_router(twitter_admin.router)
```

Then restart your backend:
```bash
systemctl restart sporttrader
```

### Option 2: Run Standalone (Testing)

```bash
cd C:\Users\nashr\backend
python twitter_alert_service.py
```

This runs the service in the foreground (good for testing).

---

## API Endpoints

### Get Status

```bash
GET /api/admin/twitter/status
```

**Response:**
```json
{
  "enabled": true,
  "authenticated": true,
  "config": {
    "enabled": "true",
    "post_arbitrage": "true",
    "min_arbitrage_profit": "0.5",
    ...
  },
  "stats": {
    "total_tweets": 127,
    "by_type": {
      "arbitrage": 45,
      "steam_move": 38,
      "middle": 22,
      "model_prediction": 15,
      "strategy_alert": 7
    },
    "last_24h": 34,
    "success_rate": "98.4%"
  }
}
```

### Enable/Disable

```bash
# Enable
POST /api/admin/twitter/enable

# Disable
POST /api/admin/twitter/disable
```

### Update Configuration

```bash
PUT /api/admin/twitter/config
Content-Type: application/json

{
  "enabled": true,
  "post_arbitrage": true,
  "post_steam_moves": true,
  "post_middles": true,
  "min_arbitrage_profit": 0.5,
  "min_steam_consensus": 50,
  "min_middle_gap_nhl": 1.0,
  "min_middle_gap_nba": 3.0,
  "max_tweets_per_hour": 20,
  "scan_interval_seconds": 300
}
```

### Send Test Tweet

```bash
POST /api/admin/twitter/test-tweet
Content-Type: application/json

{
  "message": "Testing MAX-EV Sports Twitter bot 🚀"
}
```

### Trigger Manual Scan

```bash
POST /api/admin/twitter/trigger-scan
```

Forces an immediate scan for alerts (bypasses normal schedule).

### Get Recent Tweets

```bash
GET /api/admin/twitter/recent-tweets?limit=50
```

Returns last 50 tweets with details.

---

## Configuration

### Default Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Master on/off switch |
| `post_arbitrage` | `true` | Post arbitrage alerts |
| `post_steam_moves` | `true` | Post steam move alerts |
| `post_middles` | `true` | Post middle alerts |
| `post_model_predictions` | `true` | Post ML predictions |
| `post_strategy_alerts` | `true` | Post strategy alerts |
| `min_arbitrage_profit` | `0.5` | Minimum 0.5% profit |
| `min_steam_consensus` | `50` | Minimum 50% book agreement |
| `min_middle_gap_nhl` | `1.0` | Min 1.0 pt gap for NHL |
| `min_middle_gap_nba` | `3.0` | Min 3.0 pt gap for NBA |
| `min_model_edge` | `5.0` | Minimum 5% edge |
| `min_model_confidence` | `HIGH` | HIGH or CRITICAL only |
| `max_tweets_per_hour` | `20` | Max 20 tweets/hour |
| `scan_interval_seconds` | `300` | Scan every 5 minutes |

### Recommended Settings

**Conservative (Quality Over Quantity):**
```json
{
  "min_arbitrage_profit": 1.0,
  "min_steam_consensus": 70,
  "min_middle_gap_nhl": 1.5,
  "min_middle_gap_nba": 4.0,
  "min_model_edge": 8.0,
  "max_tweets_per_hour": 10
}
```

**Aggressive (More Alerts):**
```json
{
  "min_arbitrage_profit": 0.3,
  "min_steam_consensus": 40,
  "min_middle_gap_nhl": 0.5,
  "min_middle_gap_nba": 2.0,
  "min_model_edge": 3.0,
  "max_tweets_per_hour": 30
}
```

---

## Tweet Examples

### Arbitrage Alert

```
🚨 ARBITRAGE ALERT 🏀

Lakers @ Warriors
📊 TOTALS

💰 2.14% GUARANTEED PROFIT

Bet Over 228.5 at DraftKings: -105
Bet Under 228.5 at FanDuel: -105

#SportsBetting #Arbitrage #ValueBet
```

### Steam Move Alert

```
🔥 STEAM MOVE 🏒

Maple Leafs @ Bruins
TOTALS: 📈 1.5 pts

75% of books moved!

🎯 VALUE: BetMGM still has stale line at -110

#SteamMove #SharpMoney #SportsBetting
```

### Middle Alert

```
⚡ MIDDLE OPPORTUNITY 🏀

Heat @ Celtics
SPREADS

3.5 pt GAP - Chance to WIN BOTH!

Celtics -2.5 at DraftKings: -110
Celtics -6.0 at FanDuel: -110

#MiddleBet #SportsBetting
```

### Model Prediction

```
🔥 HIGH CONFIDENCE 🏀

Warriors @ Lakers

🎯 UNDER 228.5

Edge: +7.2%
Win Rate: 62.3%
Model: XGBoost Totals

#SportsBetting #MLPredictions #ValueBet
```

### Strategy Alert

```
🔄 NBA Quarter Reversal 🏀

Celtics @ Heat

📊 Q2 hot start reversal detected

🎯 Bet UNDER 2H total

Edge: +8.5%
ROI: +12.1%

#SportsBetting #BettingStrategy
```

---

## Monitoring & Stats

### View Statistics

```bash
curl http://localhost:8000/api/admin/twitter/stats
```

**Response:**
```json
{
  "total_tweets": 127,
  "by_type": {
    "arbitrage": 45,
    "steam_move": 38,
    "middle": 22
  },
  "last_24h": 34,
  "success_rate": "98.4%",
  "enabled": true,
  "current_config": {...}
}
```

### Database Location

All posted tweets are tracked in:
```
C:\Users\nashr\backend\twitter_alerts.db
```

**Tables:**
- `posted_tweets` - All tweets with details
- `twitter_config` - Configuration settings

---

## Troubleshooting

### "Twitter client not authenticated"

**Cause:** Missing or invalid Twitter API credentials

**Fix:**
1. Verify all 5 credentials in `.env` file
2. Check for typos or extra spaces
3. Regenerate tokens if needed at [developer.twitter.com](https://developer.twitter.com)

### "Rate limit exceeded"

**Cause:** Too many tweets posted in 3 hour window

**Fix:**
1. Lower `max_tweets_per_hour` setting
2. Wait 3 hours for limit to reset
3. Check Twitter's [rate limit status](https://developer.twitter.com/en/docs/twitter-api/rate-limits)

### "Tweet too long"

**Cause:** Alert details exceed 280 characters

**Fix:**
- Tweets are automatically truncated to 277 characters + "..."
- Team names are auto-shortened ("Golden State Warriors" → "Warriors")
- If issue persists, modify `_shorten_team()` in `twitter_integration.py`

### No tweets being posted

**Check:**
1. Is automation enabled?
   ```bash
   curl http://localhost:8000/api/admin/twitter/status
   ```

2. Are alerts being detected?
   ```bash
   curl http://localhost:8000/api/admin/twitter/trigger-scan
   ```

3. Check thresholds - they might be too strict:
   ```bash
   curl http://localhost:8000/api/admin/twitter/config
   ```

4. Check logs:
   ```bash
   journalctl -u sporttrader -f | grep -i twitter
   ```

### Service won't start

**Check:**
1. Is `tweepy` installed?
   ```bash
   pip list | grep tweepy
   ```

2. Are environment variables loaded?
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('TWITTER_API_KEY'))"
   ```

3. Check main.py includes startup code

---

## Best Practices

### 1. Start Conservative

Begin with strict thresholds and increase gradually:
```json
{
  "min_arbitrage_profit": 1.0,
  "max_tweets_per_hour": 10
}
```

### 2. Monitor Performance

Check stats daily:
```bash
curl http://localhost:8000/api/admin/twitter/stats
```

### 3. Test Before Launch

Send test tweets to verify formatting:
```bash
curl -X POST http://localhost:8000/api/admin/twitter/test-tweet \
  -H "Content-Type: application/json" \
  -d '{"message": "Testing 🚀"}'
```

### 4. Adjust Based on Feedback

- If getting too many low-value alerts: Increase thresholds
- If missing good opportunities: Lower thresholds
- If followers complain: Reduce tweet frequency

### 5. Backup Configuration

Save your optimal settings:
```bash
curl http://localhost:8000/api/admin/twitter/config > twitter_config_backup.json
```

---

## Security Notes

### Protect API Credentials

- **NEVER** commit `.env` file to Git
- Keep credentials in environment variables only
- Regenerate tokens if accidentally exposed

### API Access Control

- Add authentication to admin endpoints before going live
- Restrict `/api/admin/*` routes to admin users only
- Consider adding API keys for external access

---

## Support

### Logs

View Twitter service logs:
```bash
# Real-time logs
journalctl -u sporttrader -f | grep -i twitter

# Last 100 lines
journalctl -u sporttrader -n 100 | grep -i twitter
```

### Database Queries

Query posted tweets:
```bash
sqlite3 backend/twitter_alerts.db "SELECT * FROM posted_tweets ORDER BY posted_at DESC LIMIT 10"
```

### Contact

For Twitter API issues: [Twitter Developer Support](https://developer.twitter.com/en/support)

For bot issues: Check logs and review this documentation

---

## Next Steps

1. ✅ Get Twitter API credentials
2. ✅ Add credentials to `.env`
3. ✅ Install dependencies (`pip install tweepy`)
4. ✅ Update `main.py` with startup code
5. ✅ Restart backend
6. ✅ Send test tweet
7. ✅ Enable automation
8. ✅ Monitor stats

**You're ready to start automating your bet alerts to Twitter!** 🚀

---

**Generated by MAX-EV Sports**
