# Unified Settings Architecture - ARB Extension + Website Dashboard

## Current State Analysis

### ARB Extension Settings (Chrome Storage)

**Location:** `ARB_Auto_Bettor/extension/settings/settings.html`

**Categories:**

1. **💰 Bankroll Management**
   - Total Bankroll
   - Max Bet Percentage (1-3%)
   - Minimum Profit Threshold (%)
   - Bet Sizing Method (Flat/Kelly/Fixed)
   - Fixed Bet Amount

2. **📚 Sportsbook Balances**
   - Enable/Disable per book
   - Current balance per book
   - Books: DraftKings, FanDuel, BetMGM, Caesars, BetRivers

3. **🤖 Auto-Bet Behavior**
   - Auto-bet mode: `fill` or `manual`
   - Skip insufficient funds toggle
   - Alert on skipped bets toggle

4. **🔔 Alerts & Notifications**
   - Enable Arbitrage Alerts
   - Enable Steam Move Alerts
   - Enable Line Movement Alerts
   - Enable Goalie Pull Alerts
   - Sound enabled toggle
   - Voice enabled toggle
   - Sound volume slider
   - Voice rate/pitch controls
   - Low balance warnings

**Storage:** Chrome Storage Sync API (syncs across user's devices)

---

### Website Dashboard Settings (Potential)

**Location:** `backend/scrapers/nba/frontend/` (needs implementation)

**Categories (Proposed):**

1. **👤 User Profile**
   - Username
   - Email
   - Timezone
   - Preferred sports

2. **📊 Display Preferences**
   - Theme (light/dark)
   - Default sport view
   - Refresh interval
   - Odds format (American/Decimal/Fractional)
   - Table density (compact/comfortable/spacious)

3. **📈 Data & Analytics**
   - Historical data range
   - Performance tracking
   - Export preferences
   - Google Sheets integration

4. **🔔 Web Notifications**
   - Browser notification permissions
   - Email alerts
   - SMS alerts (future)

**Storage:** Backend database (PostgreSQL/MongoDB) or Browser LocalStorage

---

## The Problem: Duplicate Configuration

**Current Issues:**

1. ❌ User configures bankroll in **extension**
2. ❌ User might configure same bankroll on **website**
3. ❌ Settings get out of sync
4. ❌ User changes balance in extension, website doesn't know
5. ❌ Duplicate code maintaining two settings systems
6. ❌ Confusing UX - "Where do I change this?"

---

## Solution: Unified Settings with Smart Sync

### Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  SINGLE SOURCE OF TRUTH             │
│                                                     │
│        Backend API (localhost:8000/api/settings)    │
│                  PostgreSQL/MongoDB                 │
│                                                     │
│     Stores: Bankroll, Books, Alerts, Preferences   │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ Sync via REST API
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐    ┌───────────────┐
│   Extension   │    │    Website    │
│               │    │   Dashboard   │
│  Chrome Sync  │    │   LocalStore  │
│   (Cache)     │    │    (Cache)    │
└───────────────┘    └───────────────┘
     │                      │
     │                      │
     ▼                      ▼
  User sees            User sees
  same settings        same settings
```

---

## Proposed Unified Settings Structure

### Backend API Endpoints

**GET** `/api/settings`
```json
{
  "user_id": "user123",
  "bankroll": {
    "total": 10000,
    "max_bet_percentage": 2.0,
    "min_profit_threshold": 2.0,
    "bet_sizing_method": "flat_percentage",
    "fixed_bet_amount": 100
  },
  "sportsbooks": {
    "draftkings": { "enabled": true, "balance": 2000 },
    "fanduel": { "enabled": true, "balance": 2000 },
    "betmgm": { "enabled": false, "balance": 0 },
    "caesars": { "enabled": false, "balance": 0 },
    "betrivers": { "enabled": true, "balance": 1500 }
  },
  "auto_bet": {
    "mode": "fill",
    "skip_insufficient_funds": true,
    "alert_on_skipped": false
  },
  "alerts": {
    "arbitrage": true,
    "steam_moves": true,
    "line_movements": true,
    "goalie_pulls": true,
    "sound_enabled": true,
    "voice_enabled": true,
    "sound_volume": 0.5,
    "voice_rate": 1.0,
    "voice_pitch": 1.0
  },
  "display": {
    "theme": "dark",
    "default_sport": "NBA",
    "refresh_interval": 5,
    "odds_format": "american",
    "table_density": "comfortable"
  },
  "notifications": {
    "browser": true,
    "email": false,
    "sms": false
  },
  "updated_at": "2025-10-19T10:30:00Z"
}
```

**PUT** `/api/settings`
- Update any setting
- Returns updated settings object
- Emits WebSocket event to notify extension

---

## Implementation Strategy

### Phase 1: Backend Settings API (Week 1)

**Tasks:**
1. Create settings table/collection in database
2. Build REST API endpoints (GET, PUT)
3. Add authentication/authorization
4. Implement validation logic

**Files:**
```
backend/
├── api/
│   └── settings.py          # FastAPI endpoints
├── models/
│   └── user_settings.py     # Settings schema
└── database/
    └── settings_crud.py     # CRUD operations
```

---

### Phase 2: Website Settings Page (Week 1-2)

**Tasks:**
1. Create Settings page component
2. Fetch settings from API on load
3. Update settings via API on change
4. Show sync status indicator

**Files:**
```
frontend/src/
├── pages/
│   └── Settings.tsx         # Main settings page
├── components/
│   ├── BankrollSettings.tsx
│   ├── SportsbookSettings.tsx
│   ├── AlertSettings.tsx
│   └── DisplaySettings.tsx
└── hooks/
    └── useSettings.ts       # Custom hook for settings
```

**Example Component:**
```tsx
// Settings.tsx
import { useSettings } from '@/hooks/useSettings';

export function Settings() {
  const { settings, updateSettings, loading, syncing } = useSettings();

  return (
    <div className="settings-page">
      <header>
        <h1>⚙️ Settings</h1>
        {syncing && <span className="sync-indicator">Syncing...</span>}
      </header>

      <BankrollSettings
        bankroll={settings.bankroll}
        onUpdate={(data) => updateSettings({ bankroll: data })}
      />

      <SportsbookSettings
        sportsbooks={settings.sportsbooks}
        onUpdate={(data) => updateSettings({ sportsbooks: data })}
      />

      {/* ... more sections */}
    </div>
  );
}
```

---

### Phase 3: Extension Sync (Week 2)

**Tasks:**
1. Extension polls `/api/settings` every 30 seconds
2. On popup open, fetch latest settings
3. Cache settings in Chrome Storage (fallback)
4. Show "Settings updated" notification when backend changes

**Modified Files:**
```
extension/
├── background.js            # Add settings sync logic
├── settings/
│   └── settings.js          # Fetch from API instead of local
└── popup/
    └── popup.js             # Show sync status
```

**Example Logic:**
```javascript
// background.js

let cachedSettings = null;

// Fetch settings from backend every 30 seconds
async function syncSettings() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/settings`);
    const settings = await response.json();

    // Update Chrome Storage (cache)
    await chrome.storage.sync.set({ settings });

    // Notify if settings changed
    if (cachedSettings && JSON.stringify(cachedSettings) !== JSON.stringify(settings)) {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: 'Settings Updated',
        message: 'Your settings have been synced from the website.'
      });
    }

    cachedSettings = settings;
    console.log('[ARB] Settings synced from backend');

  } catch (error) {
    console.error('[ARB] Failed to sync settings, using cached:', error);
    // Fall back to cached settings in Chrome Storage
    const result = await chrome.storage.sync.get(['settings']);
    cachedSettings = result.settings || getDefaultSettings();
  }
}

// Sync on startup
syncSettings();

// Sync every 30 seconds
setInterval(syncSettings, 30000);
```

---

### Phase 4: Real-Time Sync (Week 3 - Optional)

**Tasks:**
1. Add WebSocket connection to backend
2. Backend emits `settings_updated` event on change
3. Extension/Website listens and updates immediately

**WebSocket Flow:**
```
User changes setting on Website
    ↓
PUT /api/settings
    ↓
Backend updates database
    ↓
Backend emits WebSocket: settings_updated
    ↓
Extension receives event
    ↓
Extension fetches latest settings
    ↓
Extension shows "Settings updated" notification
```

---

## Settings Page Location: Website vs Extension

### Recommendation: **Primary on Website, Secondary in Extension**

**Why:**

1. ✅ **Better UX on website** - Full screen, more space, better forms
2. ✅ **Easier to maintain** - One codebase (React) instead of two (HTML+React)
3. ✅ **Persistent storage** - Database > Chrome Storage
4. ✅ **Cross-device sync** - Works on any device
5. ✅ **Extension stays lightweight** - Just read settings, don't manage them

**Extension Settings Page:**
- Keep for **quick toggles** (sound on/off, voice on/off)
- Add **"⚙️ Advanced Settings"** button → Opens website in new tab
- Show **sync status** and last updated time

**Example Extension Settings (Minimal):**
```html
<!-- extension/settings/settings.html (Simplified) -->
<div class="quick-settings">
  <h2>Quick Settings</h2>

  <!-- Quick toggles -->
  <label>
    <input type="checkbox" id="soundEnabled">
    Sound Alerts
  </label>

  <label>
    <input type="checkbox" id="voiceEnabled">
    Voice Alerts
  </label>

  <!-- Link to full settings -->
  <button id="advancedSettingsBtn" class="btn btn-primary">
    ⚙️ Open Full Settings Page
  </button>

  <!-- Sync status -->
  <div class="sync-status">
    Last synced: <span id="lastSync">2 minutes ago</span>
    <button id="syncNowBtn">Sync Now</button>
  </div>
</div>
```

---

## User Flow Comparison

### Current Flow (Separate Settings) ❌

```
User wants to change bankroll
    ↓
Opens Extension → Settings
    ↓
Changes bankroll to $5000
    ↓
Saves in Chrome Storage
    ↓
Later... opens Website Dashboard
    ↓
Website shows old bankroll: $10000
    ↓
User confused: "Why is it different?"
```

---

### New Flow (Unified Settings) ✅

```
User wants to change bankroll
    ↓
Opens Website → Settings
    ↓
Changes bankroll to $5000
    ↓
Saves to backend database
    ↓
Backend emits WebSocket event
    ↓
Extension receives event
    ↓
Extension fetches new settings
    ↓
Extension shows notification: "Settings updated"
    ↓
Extension now uses $5000 bankroll
    ↓
Website shows $5000 bankroll
    ↓
Everything in sync! ✅
```

---

## Offline Support Strategy

**What if backend is down?**

1. ✅ Extension uses **cached settings** from Chrome Storage
2. ✅ Website uses **LocalStorage cache**
3. ✅ Show **"Offline Mode"** indicator
4. ✅ Queue changes for next sync
5. ✅ Retry connection every 30 seconds

**Example:**
```javascript
// Extension background.js
async function updateSetting(key, value) {
  // Always update local cache immediately
  const settings = await chrome.storage.sync.get(['settings']);
  settings.settings[key] = value;
  await chrome.storage.sync.set({ settings: settings.settings });

  // Try to sync to backend
  try {
    await fetch(`${BACKEND_URL}/api/settings`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ [key]: value })
    });
    console.log('[ARB] Setting synced to backend');
  } catch (error) {
    console.error('[ARB] Backend offline, using cached settings');
    // Queue for next sync
    queuedChanges.push({ key, value, timestamp: Date.now() });
  }
}
```

---

## Migration Plan

### Step 1: Add Backend API (No Breaking Changes)
- Build settings API endpoints
- Extension/Website continue using local storage
- Test API thoroughly

### Step 2: Update Website to Use API
- Website reads from API
- Website writes to API
- Extension still uses Chrome Storage

### Step 3: Update Extension to Sync from API
- Extension fetches from API on startup
- Extension caches in Chrome Storage (fallback)
- Extension can still work offline

### Step 4: Deprecate Extension Settings Page
- Remove complex forms from extension settings
- Keep only quick toggles
- Add "Open Full Settings" button

### Step 5: Add Real-Time Sync (Optional)
- Implement WebSocket
- Instant updates across devices

---

## Benefits of Unified Settings

### For Users ✅

1. ✅ **Single configuration point** - Change once, works everywhere
2. ✅ **Consistent experience** - Same settings in extension and website
3. ✅ **Cross-device sync** - Settings follow you across computers
4. ✅ **No confusion** - One source of truth
5. ✅ **Better UX** - Full-featured settings page on website

### For Development ✅

1. ✅ **Less code duplication** - One settings system
2. ✅ **Easier maintenance** - Update settings logic in one place
3. ✅ **Better testing** - Test one API instead of two storage systems
4. ✅ **Database persistence** - Settings survive Chrome uninstalls
5. ✅ **Audit trail** - Track setting changes in database

### For Features ✅

1. ✅ **User accounts** - Settings tied to user, not browser
2. ✅ **Multiple profiles** - "Conservative" vs "Aggressive" betting profiles
3. ✅ **Sharing** - Share settings with team members
4. ✅ **Backups** - Export/import settings
5. ✅ **Analytics** - See which settings lead to best ROI

---

## Recommended Architecture

### SINGLE SOURCE OF TRUTH: Backend API ✅

**Primary Settings Storage:** Backend Database (PostgreSQL)

**Extension Role:**
- Syncs settings FROM backend every 30 seconds
- Caches settings in Chrome Storage (offline fallback)
- Quick toggles only (sound/voice)
- "Advanced Settings" button opens website

**Website Role:**
- Full-featured settings page (forms, validation, etc.)
- Direct read/write to backend API
- Real-time updates via WebSocket (optional)
- Settings history/audit log

**Sync Strategy:**
- Extension polls API every 30 seconds
- Website uses WebSocket for instant updates
- Both cache locally for offline support
- Conflict resolution: Backend always wins

---

## Implementation Priority

### Must Have (MVP)

1. ✅ Backend settings API (GET, PUT)
2. ✅ Website settings page (full UI)
3. ✅ Extension sync logic (read from API)
4. ✅ Offline fallback (cached settings)

### Nice to Have (V2)

1. 🔄 WebSocket real-time sync
2. 🔄 Multiple betting profiles
3. 🔄 Settings export/import
4. 🔄 Settings audit log
5. 🔄 Team/shared settings

### Future Enhancements (V3)

1. 💡 AI-suggested settings based on performance
2. 💡 A/B testing different settings
3. 💡 Community settings templates
4. 💡 Mobile app settings sync

---

## Example: Unified Settings in Action

### User Journey

1. User opens **Website** at `http://localhost:5179/settings`
2. Changes **Total Bankroll** from $10,000 to $15,000
3. Clicks **Save Settings**
4. Backend saves to database
5. Backend emits WebSocket event
6. **Extension** (running in background) receives event
7. Extension fetches new settings from API
8. Extension shows notification: "💰 Bankroll updated to $15,000"
9. User clicks **Extension icon**
10. Extension popup shows **$15,000** bankroll
11. Everything in sync! ✅

---

## Decision: One Settings Page or Two?

### ANSWER: **One Primary (Website) + Quick Controls (Extension)**

**Website Settings Page:**
- 📊 Full settings management
- 💰 Bankroll, bet sizing, thresholds
- 📚 All sportsbooks with balances
- 🔔 All alert types and preferences
- 🎨 Display preferences
- 📈 Performance tracking settings

**Extension Quick Controls:**
- 🔊 Sound on/off
- 🗣️ Voice on/off
- 🔔 Quick alert type toggles
- ⚙️ Button to open full settings on website
- 📊 Sync status indicator

---

## Code Example: useSettings Hook

```typescript
// frontend/src/hooks/useSettings.ts
import { useState, useEffect } from 'react';

interface Settings {
  bankroll: BankrollSettings;
  sportsbooks: SportsbookSettings;
  alerts: AlertSettings;
  // ... more
}

export function useSettings() {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);

  // Fetch settings on mount
  useEffect(() => {
    fetchSettings();
  }, []);

  async function fetchSettings() {
    try {
      const response = await fetch('http://localhost:8000/api/settings');
      const data = await response.json();
      setSettings(data);
    } catch (error) {
      console.error('Failed to fetch settings:', error);
      // Fallback to localStorage
      const cached = localStorage.getItem('settings');
      if (cached) setSettings(JSON.parse(cached));
    } finally {
      setLoading(false);
    }
  }

  async function updateSettings(updates: Partial<Settings>) {
    setSyncing(true);
    try {
      const response = await fetch('http://localhost:8000/api/settings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      });
      const updated = await response.json();
      setSettings(updated);

      // Cache locally
      localStorage.setItem('settings', JSON.stringify(updated));

      // Show success toast
      toast.success('Settings saved successfully!');
    } catch (error) {
      console.error('Failed to update settings:', error);
      toast.error('Failed to save settings. Try again.');
    } finally {
      setSyncing(false);
    }
  }

  return { settings, updateSettings, loading, syncing };
}
```

---

## Final Recommendation

### ✅ Build ONE unified settings system:

1. **Backend API as single source of truth**
2. **Website as primary settings interface**
3. **Extension syncs from backend**
4. **Both cache locally for offline support**
5. **Extension has minimal quick controls**

### 🚀 Start with:

1. Build backend settings API (FastAPI)
2. Create website settings page (React)
3. Update extension to sync from API
4. Add offline fallback logic

### ⏱️ Timeline:

- **Week 1:** Backend API + Database
- **Week 2:** Website Settings Page
- **Week 3:** Extension Sync Logic
- **Week 4:** Testing + Polish

**Result:** One settings system, works everywhere, always in sync! 🎯
