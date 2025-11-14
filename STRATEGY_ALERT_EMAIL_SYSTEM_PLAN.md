# Strategy Alert Email System - Implementation Plan

## Current State Analysis

### Frontend (Pricing & Strategy Pages)
**Location:** `frontend/src/pages/StrategyResults.tsx` & `PreGameStrategyResults.tsx`

**What Exists:**
- ✅ AlertModal component (lines 82-145)
- ✅ Email input form
- ✅ Subscribe button UI
- ✅ Frontend calls `POST /strategies/subscribe` with `{strategy_id, email}`

**Problem:** Backend endpoint `/strategies/subscribe` **DOES NOT EXIST** ❌

---

### Backend Alert Monitoring System
**Location:** `backend/alert_monitor.py`

**What Exists:**
- ✅ `AlertMonitor` class that monitors odds in real-time
- ✅ Detects 3 types of alerts:
  1. **Arbitrage** - Risk-free profit opportunities
  2. **Steam Moves** - Sharp money line movements
  3. **Middle Opportunities** - Bet both sides to win both
- ✅ Stores alerts in `alert_storage` database
- ✅ Used by `game_tracker.py` via FastAPI WebSocket connections

**Alert Detection Flow:**
```
GameTracker fetches odds every 10-30s
    ↓
AlertMonitor.detect_opportunities()
    ↓
Checks for arbitrage/steam/middles
    ↓
Stores in alert_storage
    ↓
Returns to frontend via WebSocket
```

---

### Email Infrastructure
**Location:** `backend/brevo_crm.py`

**What Exists:**
- ✅ `BrevoClient` class fully configured
- ✅ `send_transac_email()` method for transactional emails
- ✅ Already used for:
  - Welcome emails (signup)
  - Admin notifications
  - Payment notifications
- ✅ Environment variable: `BREVO_API_KEY`

**Example Send Code:**
```python
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
    to=[{"email": user_email, "name": user_name}],
    sender={"email": "noreply@max-ev-sports.com", "name": "MAX-EV Sports"},
    subject="Strategy Alert: Goalie Pull Detected!",
    html_content="<html>...</html>"
)
api_response = self.transactional_api.send_transac_email(send_smtp_email)
```

---

## Missing Pieces

### 1. Backend Endpoint Missing ❌
**Need:** `POST /api/strategies/subscribe`
- Store strategy subscriptions in database
- Link user email → strategy IDs

### 2. Subscription Database Table Missing ❌
**Need:** SQLite table to store subscriptions
```sql
CREATE TABLE strategy_subscriptions (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    strategy_id INTEGER NOT NULL,
    username TEXT,
    subscribed_at TIMESTAMP,
    active BOOLEAN DEFAULT 1,
    UNIQUE(email, strategy_id)
);
```

### 3. Alert Email Sender Missing ❌
**Need:** Background service that:
- Monitors for new strategy alerts
- Queries subscriptions database
- Sends emails to subscribers via Brevo

### 4. Strategy Alert Detection Missing ❌
**Current:** AlertMonitor only detects arbitrage/steam/middles
**Need:** Add detection for 25 strategies from `routes/strategies.py`:
- Goalie Pull Alert (#6)
- Quarter Reversal (#14)
- Halftime Tracker (#23)
- Momentum Detector (#24)
- Pace Mismatch (#25)
- etc.

---

## Implementation Plan

### Phase 1: Database & Backend Endpoint (30 minutes)
**File:** `backend/routes/strategies.py`

1. Create SQLite database table for subscriptions
2. Add `POST /api/strategies/subscribe` endpoint
3. Add `GET /api/strategies/subscriptions` (for user to view their subscriptions)
4. Add `DELETE /api/strategies/unsubscribe` endpoint

**Database:**
```python
# backend/database/strategy_subscriptions_db.py
class StrategySubscriptionsDB:
    def subscribe(self, email, strategy_id, username):
        # Add subscription
    def unsubscribe(self, email, strategy_id):
        # Remove subscription
    def get_subscribers(self, strategy_id):
        # Get all emails subscribed to a strategy
    def get_user_subscriptions(self, email):
        # Get all strategies a user is subscribed to
```

### Phase 2: Email Alert Sender (45 minutes)
**File:** `backend/strategy_alert_mailer.py`

Create background service that:
1. Checks `alert_storage` every 30 seconds
2. For each new alert:
   - Match alert type → strategy_id
   - Query subscriptions database for emails
   - Send personalized emails via Brevo
   - Track sent alerts to avoid duplicates

**Email Template:**
```html
Subject: 🔔 Strategy Alert: {strategy_name}

Hi {user},

A betting opportunity matching your "{strategy_name}" strategy was just detected!

📊 Game: {home_team} vs {away_team}
🎯 Signal: {alert_description}
💰 Expected Edge: +{edge}%
⏰ Window: {time_remaining}

Recommended Action:
- Book: {bookmaker}
- Bet: {bet_type} {side}
- Line: {line}
- Odds: {odds}

View full details: https://max-ev-sports.com/#/alerts

Good luck!
MAX-EV Sports
```

### Phase 3: Strategy Detection Enhancement (2 hours)
**File:** `backend/strategies/` (various strategy detectors)

Add strategy-specific alert detectors:
1. `goalie_pull_detector.py` - Already exists ✅
2. `quarter_reversal_detector.py` - Already exists ✅
3. `halftime_tracker_detector.py` - Need to create
4. `momentum_detector.py` - Partially exists
5. etc.

Integrate each detector into `AlertMonitor` or `GameTracker`.

### Phase 4: Frontend Subscription Management (30 minutes)
**Files:**
- `frontend/src/pages/StrategySettings.tsx` (new page)
- Update Navigation to include "Alert Subscriptions"

Features:
- View all active subscriptions
- Unsubscribe from strategies
- Configure email frequency (instant, hourly digest, daily)

---

## Technical Architecture

```
┌─────────────────────────────────────────────┐
│         Frontend (StrategyResults.tsx)      │
│  User clicks "Subscribe" → sends email      │
└─────────────────┬───────────────────────────┘
                  │ POST /strategies/subscribe
                  ▼
┌─────────────────────────────────────────────┐
│  Backend (routes/strategies.py)             │
│  - Stores subscription in DB                │
│  - Returns success                          │
└─────────────────────────────────────────────┘


┌─────────────────────────────────────────────┐
│  GameTracker (main.py)                      │
│  - Fetches odds every 10-30s                │
│  - Calls AlertMonitor.detect_opportunities()│
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  AlertMonitor (alert_monitor.py)            │
│  - Detects arbitrage/steam/middles          │
│  - **NEW:** Calls Strategy Detectors        │
│  - Stores alerts in alert_storage           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Strategy Alert Mailer (NEW SERVICE)        │
│  - Runs every 30s in background             │
│  - Queries new alerts from alert_storage    │
│  - Maps alerts → strategy_id                │
│  - Queries subscriptions DB                 │
│  - Sends emails via Brevo                   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Brevo Email Service (brevo_crm.py)         │
│  - Sends transactional email                │
│  - Tracks delivery status                   │
└─────────────────────────────────────────────┘
                  │
                  ▼
              User's Email 📧
```

---

## Database Schema

### Table: `strategy_subscriptions`
```sql
CREATE TABLE strategy_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    strategy_id INTEGER NOT NULL,
    username TEXT,  -- Optional, links to auth.users
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT 1,
    email_frequency TEXT DEFAULT 'instant',  -- 'instant', 'hourly', 'daily'
    last_sent_at TIMESTAMP,
    total_emails_sent INTEGER DEFAULT 0,
    UNIQUE(email, strategy_id)
);

CREATE INDEX idx_strategy_subscriptions_email ON strategy_subscriptions(email);
CREATE INDEX idx_strategy_subscriptions_strategy_id ON strategy_subscriptions(strategy_id);
CREATE INDEX idx_strategy_subscriptions_active ON strategy_subscriptions(active);
```

### Table: `strategy_alerts_sent` (prevent duplicate emails)
```sql
CREATE TABLE strategy_alerts_sent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_id TEXT NOT NULL,  -- From alert_storage
    email TEXT NOT NULL,
    strategy_id INTEGER NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(alert_id, email)
);
```

---

## Environment Variables Needed

Already exists in `.env`:
```bash
BREVO_API_KEY=xkeysib-...
BREVO_SENDER_EMAIL=noreply@max-ev-sports.com
ADMIN_EMAIL=gte.apw@gmail.com
```

---

## Testing Plan

1. **Backend Endpoint Test:**
   ```bash
   curl -X POST http://localhost:8000/api/strategies/subscribe \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "strategy_id": 6}'
   ```

2. **Database Verification:**
   ```bash
   sqlite3 backend/database/strategy_subscriptions.db
   SELECT * FROM strategy_subscriptions;
   ```

3. **Email Test:**
   - Subscribe to Goalie Pull Alert (#6)
   - Manually trigger goalie pull detection
   - Verify email received within 30 seconds

4. **Unsubscribe Test:**
   - Click unsubscribe in email footer
   - Verify subscription marked inactive in DB

---

## Next Steps

1. Create `strategy_subscriptions_db.py`
2. Add `/subscribe` endpoint to `routes/strategies.py`
3. Create `strategy_alert_mailer.py` background service
4. Add email templates
5. Integrate with existing alert system
6. Test end-to-end flow

**Estimated Total Time:** 4-5 hours

**Priority:** HIGH (users are clicking Subscribe and getting no response)
