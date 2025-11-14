# Twitter Integration - main.py Changes

## Quick Integration Guide

Add these code snippets to `backend/main.py` to integrate Twitter automation.

---

## Step 1: Add Imports (Top of File)

Add after existing imports:

```python
import asyncio
from twitter_alert_service import TwitterAlertService
from routes import twitter_admin
```

---

## Step 2: Initialize Global Twitter Service

Add after `app = FastAPI()`:

```python
# Global Twitter service instance
twitter_service_instance = None
```

---

## Step 3: Add Startup Event

Add this startup event handler:

```python
@app.on_event("startup")
async def startup_twitter_service():
    """Initialize and start Twitter alert service"""
    global twitter_service_instance

    try:
        # Get API key from environment
        odds_api_key = os.getenv('ODDS_API_KEY')

        if not odds_api_key:
            logger.warning("⚠️ ODDS_API_KEY not found, Twitter service disabled")
            return

        # Initialize Twitter service
        twitter_service_instance = TwitterAlertService(odds_api_key)

        # Set global reference for admin API
        twitter_admin.set_twitter_service(twitter_service_instance)

        # Start monitoring loop in background
        asyncio.create_task(twitter_service_instance.start_monitoring())

        logger.info("✅ Twitter alert service started successfully")

    except Exception as e:
        logger.error(f"❌ Failed to start Twitter service: {e}")
```

---

## Step 4: Include Admin Routes

Add after other `app.include_router()` calls:

```python
# Include Twitter admin routes
app.include_router(twitter_admin.router)
```

---

## Complete Example

Here's what the relevant sections should look like:

```python
# ============================================
# IMPORTS
# ============================================
from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv
import asyncio

# Your existing imports...
from game_tracker import GameTracker
from routes import auth, subscriptions, games, predictions

# NEW: Twitter integration
from twitter_alert_service import TwitterAlertService
from routes import twitter_admin

# ============================================
# SETUP
# ============================================
load_dotenv()
logger = logging.getLogger(__name__)

app = FastAPI(title="MAX-EV Sports API", version="1.0.0")

# NEW: Global Twitter service
twitter_service_instance = None

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# STARTUP EVENT
# ============================================
@app.on_event("startup")
async def startup_twitter_service():
    """Initialize and start Twitter alert service"""
    global twitter_service_instance

    try:
        odds_api_key = os.getenv('ODDS_API_KEY')

        if not odds_api_key:
            logger.warning("⚠️ ODDS_API_KEY not found, Twitter service disabled")
            return

        # Initialize service
        twitter_service_instance = TwitterAlertService(odds_api_key)
        twitter_admin.set_twitter_service(twitter_service_instance)

        # Start monitoring
        asyncio.create_task(twitter_service_instance.start_monitoring())

        logger.info("✅ Twitter alert service started")

    except Exception as e:
        logger.error(f"❌ Failed to start Twitter service: {e}")

# ============================================
# ROUTES
# ============================================
# Your existing routes
app.include_router(auth.router)
app.include_router(subscriptions.router)
app.include_router(games.router)
app.include_router(predictions.router)

# NEW: Twitter admin routes
app.include_router(twitter_admin.router)

# Health check
@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "1.0.0",
        "twitter_enabled": twitter_service_instance is not None if twitter_service_instance else False
    }
```

---

## Verification

After adding the code and restarting:

### 1. Check Health Endpoint

```bash
curl http://localhost:8000/
```

Should return:
```json
{
  "status": "online",
  "version": "1.0.0",
  "twitter_enabled": true
}
```

### 2. Check Twitter Status

```bash
curl http://localhost:8000/api/admin/twitter/status
```

Should return configuration and stats.

### 3. Check Logs

```bash
journalctl -u sporttrader -f | grep -i twitter
```

Should see:
```
✅ Twitter authenticated as @your_username
✅ Twitter alert service started successfully
🔍 Scanning for alerts...
```

---

## Deployment to Production

### 1. Install Dependencies

```bash
ssh root@148.230.87.135
cd /root/sporttrader/backend
source venv/bin/activate
pip install tweepy python-dotenv
```

### 2. Add Credentials to .env

```bash
nano /root/sporttrader/backend/.env
```

Add Twitter credentials:
```bash
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### 3. Upload New Files

```bash
# From local machine
scp -i ~/.ssh/hostinger_vps backend/twitter_integration.py root@148.230.87.135:/root/sporttrader/backend/
scp -i ~/.ssh/hostinger_vps backend/twitter_alert_service.py root@148.230.87.135:/root/sporttrader/backend/
scp -i ~/.ssh/hostinger_vps backend/routes/twitter_admin.py root@148.230.87.135:/root/sporttrader/backend/routes/
```

### 4. Update main.py

```bash
ssh root@148.230.87.135
cd /root/sporttrader/backend
nano main.py
```

Add the code snippets from above.

### 5. Restart Service

```bash
systemctl restart sporttrader
systemctl status sporttrader
```

### 6. Verify

```bash
curl http://localhost:8000/api/admin/twitter/status
```

---

## Troubleshooting

### "Twitter service not initialized"

**Check:**
```bash
journalctl -u sporttrader -n 50 | grep -i twitter
```

**Common causes:**
- Missing credentials in .env
- Import error (typo in filename)
- Python version incompatibility

### "Module not found: tweepy"

**Fix:**
```bash
ssh root@148.230.87.135
cd /root/sporttrader/backend
source venv/bin/activate
pip install tweepy
```

### Service starts but no tweets

**Check config:**
```bash
curl http://localhost:8000/api/admin/twitter/config
```

**Enable if disabled:**
```bash
curl -X POST http://localhost:8000/api/admin/twitter/enable
```

**Check for alerts:**
```bash
curl -X POST http://localhost:8000/api/admin/twitter/trigger-scan
```

---

## Testing Locally First

Before deploying to production, test locally:

### 1. Run Backend Locally

```bash
cd C:\Users\nashr\backend
python main.py
```

### 2. Send Test Tweet

```bash
curl -X POST http://localhost:8000/api/admin/twitter/test-tweet \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Testing from local 🚀\"}"
```

### 3. Trigger Scan

```bash
curl -X POST http://localhost:8000/api/admin/twitter/trigger-scan
```

### 4. Check Stats

```bash
curl http://localhost:8000/api/admin/twitter/stats
```

---

**Once local testing works, deploy to production!**
