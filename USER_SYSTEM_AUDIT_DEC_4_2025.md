# MAX EV SPORTS - USER SYSTEM AUDIT
**Date:** December 4, 2025
**Analysis:** Authentication, Signup, Data Storage, Bookmaker Filtering, & Security

---

## EXECUTIVE SUMMARY

### ✅ **WHAT WORKS**
1. **Signup flow exists and functions** - Users can self-register via `/api/auth/register`
2. **Settings persist across sessions** - Bookmaker preferences saved in SQLite
3. **Bet tracking fully operational** - Complete history with analytics in SQLite
4. **Subscription management integrated** - Stripe-backed tier system with feature gates
5. **Brevo CRM integration active** - Welcome emails and admin notifications

### ❌ **CRITICAL ISSUES FOUND**
1. **GameCards DO NOT filter by user's enabled bookmakers** - Shows all odds regardless of settings
2. **Fragmented database architecture** - 8+ separate databases/JSON files for user data
3. **Weak password security** - Using SHA256 instead of bcrypt/argon2
4. **No centralized user ID** - Username as primary key across disconnected systems
5. **JSON files for critical auth data** - Users, sessions, activity logs stored in files

---

## 1. GAMECARD BOOKMAKER FILTERING ❌ **NOT IMPLEMENTED**

### Current Behavior:
**GameCard component DOES NOT filter odds by user's enabled bookmakers.**

```typescript
// GameCard.tsx line 2392 - Shows ALL odds regardless of settings
const oddsWithTotal = odds.filter(o => o.total !== null && o.total !== undefined);
```

### What Should Happen:
```typescript
// SHOULD BE:
const { settings } = useSettings(username);
const oddsWithTotal = odds
  .filter(o => settings.enabled_bookmakers.includes(normalizeBookmaker(o.bookmaker)))
  .filter(o => o.total !== null);
```

### Impact:
- Users select their bookmakers in Settings page
- Settings save correctly to database
- **But GameCards ignore this and show ALL bookmakers**
- Users see 20+ bookmakers even if they only enabled 3

### Fix Required:
1. Import `useSettings` hook in GameCard.tsx
2. Filter `odds` array by `settings.enabled_bookmakers`
3. Apply filter before rendering totals, spreads, moneylines

---

## 2. SIGNUP FLOW IMPLEMENTATION ✅ **FULLY FUNCTIONAL**

### Endpoints:
1. **`POST /api/auth/register`** - Full registration with password
2. **`POST /api/auth/signup`** - Email-only validation (Pricing page capture)

### Registration Flow:
```
User submits form → /api/auth/register
  ├─ Validates all fields (name, email, username, password)
  ├─ Checks email blocklist
  ├─ Validates referral code (optional)
  ├─ Creates user in users.json (SHA256 password hash)
  ├─ Creates 14-day trial subscription (Semi Pro tier)
  ├─ Generates session token (7-day expiry)
  ├─ Syncs to Brevo CRM
  ├─ Sends welcome email
  └─ Notifies admin
```

### Features:
- ✅ 14-day free trial (Semi Pro access)
- ✅ Referral code support (50% discount tracking)
- ✅ Promo code validation
- ✅ Email blocklist enforcement
- ✅ Duplicate username/email detection
- ✅ Terms of service checkbox requirement
- ✅ Brevo CRM sync (contact creation + welcome email)

### Gaps:
- ❌ No email verification (users can register with fake emails)
- ❌ No password reset flow
- ❌ No rate limiting visible
- ❌ Weak password requirements (min 6 chars only)

---

## 3. PASSWORD SECURITY AUDIT ⚠️ **CRITICAL WEAKNESS**

### Current Implementation:
```python
# backend/auth.py:102-104
def hash_password(password: str) -> str:
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()
```

### Problems:
1. **SHA256 is NOT a password hashing algorithm** - Designed for data integrity, not passwords
2. **No salt** - Identical passwords = identical hashes (rainbow table vulnerable)
3. **Too fast** - Can brute-force billions of passwords/second on GPU
4. **No work factor** - Cannot increase difficulty over time as hardware improves

### Industry Standard:
```python
# SHOULD USE:
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(username: str, password: str) -> bool:
    stored_hash = users[username]["password_hash"]
    return bcrypt.checkpw(password.encode(), stored_hash.encode())
```

### Recommended Fix:
1. **Install bcrypt:** `pip install bcrypt`
2. **Migrate existing password hashes:**
   - On next login, re-hash with bcrypt
   - Store migration flag in user record
3. **Update auth.py** with bcrypt functions
4. **Force password reset** for all existing users (security notice)

### Alternative (even better):
- **Argon2** - Winner of Password Hashing Competition (PHC)
- More resistant to GPU/ASIC attacks than bcrypt
- `pip install argon2-cffi`

---

## 4. DATA PERSISTENCE ANALYSIS ✅ **WORKS BUT FRAGMENTED**

### Current Database Architecture:

```
USER DATA STORAGE (8+ Separate Files/Databases)
├─ backend/users.json                         [JSON] Auth accounts
├─ backend/sessions.json                      [JSON] Active sessions
├─ backend/user_activity_log.json             [JSON] Login/logout events
├─ backend/user_settings.db                   [SQLite] Bookmaker prefs, bankroll
├─ backend/database/subscriptions.db          [SQLite] Stripe subs, tiers, payments
├─ backend/data/bets/user_bets.db             [SQLite] Bet tracking
├─ backend/data/bankroll/user_bankrolls.json  [JSON] Bankroll snapshots
└─ backend/database/sports_betting.db         [SQLite] Unknown (may be duplicate)
```

### Persistence Status:

| **Data Type**              | **Storage**          | **Persists?** | **Status** |
|---------------------------|---------------------|--------------|-----------|
| User credentials          | users.json          | ✅ Yes       | File-based |
| Active sessions           | sessions.json       | ✅ Yes       | File-based |
| Login/logout history      | activity_log.json   | ✅ Yes       | File-based |
| Bookmaker preferences     | user_settings.db    | ✅ Yes       | SQLite |
| Subscription tier         | subscriptions.db    | ✅ Yes       | SQLite |
| Bet tracking              | user_bets.db        | ✅ Yes       | SQLite |
| Bankroll snapshots        | user_bankrolls.json | ✅ Yes       | File-based |

### Issues:
1. **No unified user ID** - Username used as primary key across all systems
2. **Mix of JSON and SQLite** - Inconsistent data storage patterns
3. **File locking risks** - JSON files can corrupt under concurrent writes
4. **No referential integrity** - User deletion won't cascade to subscriptions/bets
5. **Backup complexity** - Must backup 8+ files/databases separately
6. **Migration complexity** - Username change requires updating 8+ locations

---

## 5. SINGLE DATABASE CONSOLIDATION RECOMMENDATION

### **YES - You should consolidate to a single SQLite database.**

### Proposed Schema: `backend/database/maxev_sports.db`

```sql
-- ========== USERS TABLE ==========
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,  -- bcrypt hash
    full_name TEXT,
    role TEXT DEFAULT 'user',
    stripe_customer_id TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    email_verified INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1
);

-- ========== SESSIONS TABLE ==========
CREATE TABLE sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP,
    activity_count INTEGER DEFAULT 0,
    user_agent TEXT,
    ip_address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== USER ACTIVITY LOG ==========
CREATE TABLE user_activity (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,  -- login, logout, password_change, etc.
    details TEXT,  -- JSON blob for extra data
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== SUBSCRIPTIONS ==========
CREATE TABLE subscriptions (
    subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stripe_subscription_id TEXT UNIQUE,
    tier TEXT NOT NULL DEFAULT 'free',
    status TEXT NOT NULL DEFAULT 'active',
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end INTEGER DEFAULT 0,
    trial_end TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== SUBSCRIPTION HISTORY ==========
CREATE TABLE subscription_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subscription_id INTEGER,
    event_type TEXT NOT NULL,
    tier TEXT,
    status TEXT,
    metadata TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);

-- ========== PAYMENT HISTORY ==========
CREATE TABLE payment_history (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stripe_invoice_id TEXT UNIQUE,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'usd',
    status TEXT NOT NULL,
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== USER SETTINGS ==========
CREATE TABLE user_settings (
    settings_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    enabled_bookmakers TEXT NOT NULL,  -- JSON array
    total_bankroll REAL DEFAULT 10000.0,
    unit_size REAL DEFAULT 100.0,
    risk_level TEXT DEFAULT 'medium',
    min_arb_profit REAL DEFAULT 1.0,
    steam_move_threshold REAL DEFAULT 5.0,
    line_movement_threshold REAL DEFAULT 3.0,
    alert_sound_enabled INTEGER DEFAULT 1,
    show_latency INTEGER DEFAULT 1,
    highlight_pinnacle INTEGER DEFAULT 1,
    dark_mode INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== USER BETS ==========
CREATE TABLE user_bets (
    bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    bet_uuid TEXT UNIQUE NOT NULL,  -- Keep UUID for API compatibility
    game_id TEXT NOT NULL,
    sport TEXT NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    commence_time TEXT NOT NULL,
    bet_type TEXT NOT NULL,
    bet_side TEXT NOT NULL,
    stake REAL,
    odds REAL NOT NULL,
    bookmaker TEXT NOT NULL,
    alert_id TEXT,
    confidence TEXT,
    edge_percent REAL,
    strategy TEXT,
    clicked_at TIMESTAMP NOT NULL,
    logged_at TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'pending',
    result TEXT,
    payout REAL,
    profit_loss REAL,
    settled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== REFERRALS (from influencer_system) ==========
CREATE TABLE referrals (
    referral_id INTEGER PRIMARY KEY AUTOINCREMENT,
    influencer_user_id INTEGER NOT NULL,
    referred_user_id INTEGER NOT NULL,
    referral_code TEXT NOT NULL,
    subscription_tier TEXT,
    referral_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (influencer_user_id) REFERENCES users(user_id),
    FOREIGN KEY (referred_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ========== INDEXES ==========
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_stripe_customer ON users(stripe_customer_id);
CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);
CREATE INDEX idx_activity_user ON user_activity(user_id);
CREATE INDEX idx_activity_action ON user_activity(action);
CREATE INDEX idx_subs_user ON subscriptions(user_id);
CREATE INDEX idx_subs_stripe ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_subs_status ON subscriptions(status);
CREATE INDEX idx_payments_user ON payment_history(user_id);
CREATE INDEX idx_bets_user ON user_bets(user_id);
CREATE INDEX idx_bets_status ON user_bets(status);
CREATE INDEX idx_bets_uuid ON user_bets(bet_uuid);
CREATE INDEX idx_bets_sport ON user_bets(sport);
```

---

## 6. MIGRATION BENEFITS

### Before (Current):
```
8 separate databases/files
├─ Concurrent write conflicts (JSON files)
├─ No referential integrity
├─ Username changes break everything
├─ Inconsistent transaction handling
├─ Complex backup/restore procedures
└─ No foreign key constraints
```

### After (Single Database):
```
1 unified SQLite database
├─ ACID transactions across all tables
├─ Foreign key constraints enforce integrity
├─ User deletion cascades cleanly
├─ Single backup file
├─ Integer user_id primary key (performance)
└─ Consistent query patterns
```

### Performance Impact:
- **SQLite handles 100,000+ reads/second** for small datasets
- **Concurrent reads** work perfectly (MVCC)
- **Concurrent writes** queue automatically (not an issue for <10,000 users)
- **Single file backup** with WAL mode for safety

### When to Move to PostgreSQL:
- **10,000+ concurrent users** (SQLite bottleneck)
- **High write volume** (>100 writes/sec sustained)
- **Multi-server deployment** (SQLite is single-machine only)
- **Advanced features needed** (full-text search, JSON queries, etc.)

**For now: SQLite is perfect for your scale.**

---

## 7. MIGRATION PLAN

### Phase 1: Create Unified Database
1. Create `backend/database/maxev_sports.db` with schema above
2. Write migration script: `backend/migrations/consolidate_user_data.py`
3. Migrate data from JSON files → SQLite tables
4. **Upgrade password hashes** during migration (SHA256 → bcrypt)
5. Run validation to ensure all data migrated

### Phase 2: Update Code
1. Create unified database client: `backend/database/db_client.py`
2. Replace `auth.py` JSON functions with SQL queries
3. Replace `settings_database.py` to use new unified DB
4. Update `bet_storage_sqlite.py` to reference new schema
5. Update `subscription_db.py` to use unified DB

### Phase 3: Deploy
1. Stop backend
2. Run migration script
3. Deploy updated code
4. Test all endpoints
5. Keep JSON backups for 30 days (rollback safety)

### Phase 4: Fix GameCard Filtering
1. Add `useSettings` import to GameCard.tsx
2. Filter odds by enabled_bookmakers
3. Test with different bookmaker selections
4. Deploy frontend

---

## 8. SECURITY IMPROVEMENTS CHECKLIST

### High Priority (Do Immediately):
- [ ] **Replace SHA256 with bcrypt** for password hashing
- [ ] **Add rate limiting** to login/register endpoints (e.g., 5 attempts/minute)
- [ ] **Implement HTTPS only** for production (no HTTP)
- [ ] **Add CSRF protection** for state-changing endpoints
- [ ] **Strengthen password requirements** (min 8 chars, complexity rules)

### Medium Priority (Next Sprint):
- [ ] **Email verification flow** (prevent fake email registrations)
- [ ] **Password reset flow** (forgot password)
- [ ] **2FA support** (TOTP authenticator apps)
- [ ] **Session invalidation** on password change
- [ ] **IP-based suspicious login detection**

### Low Priority (Future):
- [ ] **OAuth login** (Google, Twitter, etc.)
- [ ] **Account lockout** after N failed login attempts
- [ ] **Security audit logs** (separate from activity logs)
- [ ] **Penetration testing**

---

## 9. FINAL RECOMMENDATIONS

### **What to Do Next:**

1. **FIX GAMECARD FILTERING** (1-2 hours)
   - This is user-facing and directly impacts UX
   - Users expect settings to work

2. **MIGRATE TO UNIFIED DATABASE** (4-6 hours)
   - Solves data fragmentation
   - Enables proper foreign keys
   - Simplifies codebase

3. **UPGRADE PASSWORD SECURITY** (2-3 hours)
   - Critical security vulnerability
   - Force password reset for existing users

4. **ADD EMAIL VERIFICATION** (3-4 hours)
   - Prevents fake email signups
   - Improves account security

5. **IMPLEMENT RATE LIMITING** (1-2 hours)
   - Prevents brute-force attacks
   - Low effort, high security impact

---

## 10. CODE EXAMPLES

### Fix GameCard Filtering:
```typescript
// frontend/src/components/GameCard.tsx

import { useSettings } from '../hooks/useSettings';

export function GameCard({ game }: GameCardProps) {
  const { username } = useAuth();
  const { settings } = useSettings(username || 'default');

  // Normalize bookmaker names for matching
  const normalizeBookmaker = (name: string) => {
    return name.toLowerCase().replace(/\s+/g, '').replace(/\./g, '');
  };

  // Filter odds by enabled bookmakers
  const filteredOdds = useMemo(() => {
    if (!settings?.enabled_bookmakers?.length) return odds;

    return odds.filter(odd => {
      const normalized = normalizeBookmaker(odd.bookmaker);
      return settings.enabled_bookmakers.some(
        enabled => normalizeBookmaker(enabled) === normalized
      );
    });
  }, [odds, settings?.enabled_bookmakers]);

  // Use filteredOdds instead of odds throughout component
  const oddsWithTotal = filteredOdds.filter(o => o.total !== null);
  // ... rest of component
}
```

### Unified Database Client:
```python
# backend/database/db_client.py

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Dict, List, Any

DB_PATH = Path(__file__).parent / "maxev_sports.db"

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  # Enable FK constraints
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get user by username"""
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        return dict(row) if row else None

def create_user(username: str, email: str, password_hash: str, **kwargs) -> int:
    """Create new user, returns user_id"""
    with get_db() as db:
        cursor = db.execute(
            """INSERT INTO users (username, email, password_hash, full_name, role)
               VALUES (?, ?, ?, ?, ?)""",
            (username, email, password_hash,
             kwargs.get('full_name'), kwargs.get('role', 'user'))
        )

        # Create default settings for user
        db.execute(
            """INSERT INTO user_settings (user_id, enabled_bookmakers)
               VALUES (?, ?)""",
            (cursor.lastrowid, '["draftkings", "fanduel", "pinnacle"]')
        )

        return cursor.lastrowid
```

---

**End of Audit Report**
