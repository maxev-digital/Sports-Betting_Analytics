# Bookmaker Filtering System - Only Show User's Books

## User Problem Statement

**Current Issue:**
- User has accounts at DraftKings, FanDuel, and BetMGM (3 books)
- Dashboard shows odds from 38+ NBA bookmakers
- Game cards cluttered with 35+ bookmakers user doesn't use
- Alerts include opportunities from books user can't access
- Information overload, poor UX

**User Need:**
> "I only want to see alerts, odds feeds, and game cards from the sportsbooks I actually use."

---

## Solution: Bookmaker Preference Filtering

### System Overview

```
┌─────────────────────────────────────────────┐
│         Settings Page                       │
│  User Selects Active Bookmakers:           │
│  ✅ DraftKings                              │
│  ✅ FanDuel                                 │
│  ✅ BetMGM                                  │
│  ❌ Caesars                                 │
│  ❌ BetRivers                               │
│  ❌ ... (59 more)                           │
└──────────────┬──────────────────────────────┘
               │
               │ Saves to backend
               ▼
┌─────────────────────────────────────────────┐
│         Backend API                         │
│  Stores: ["draftkings", "fanduel", "betmgm"]│
└──────────────┬──────────────────────────────┘
               │
               │ Filters all data
               ▼
┌─────────────────────────────────────────────┐
│    Frontend Displays                        │
│  • Game Cards: Only 3 bookmakers           │
│  • Alerts: Only DK/FD/BetMGM opportunities │
│  • Odds Feed: Only 3 bookmakers            │
│  • Clean, focused UI                       │
└─────────────────────────────────────────────┘
```

---

## Architecture

### 1. Settings Storage

**Backend Database:**
```json
{
  "user_id": "user123",
  "enabled_bookmakers": [
    "draftkings",
    "fanduel",
    "betmgm"
  ],
  "updated_at": "2025-10-19T10:30:00Z"
}
```

---

### 2. Settings API Endpoints

**GET /api/settings/bookmakers**
```json
{
  "enabled_bookmakers": [
    "draftkings",
    "fanduel",
    "betmgm"
  ],
  "available_bookmakers": [
    {
      "key": "draftkings",
      "name": "DraftKings",
      "region": ["US"],
      "enabled": true,
      "logo": "https://www.google.com/s2/favicons?domain=draftkings.com&sz=64"
    },
    {
      "key": "fanduel",
      "name": "FanDuel",
      "region": ["US"],
      "enabled": true,
      "logo": "https://www.google.com/s2/favicons?domain=fanduel.com&sz=64"
    },
    // ... all 62 bookmakers
  ]
}
```

**PUT /api/settings/bookmakers**
```json
{
  "enabled_bookmakers": [
    "draftkings",
    "fanduel",
    "betmgm",
    "caesars"  // User just enabled Caesars
  ]
}
```

**Response:**
```json
{
  "success": true,
  "enabled_bookmakers": ["draftkings", "fanduel", "betmgm", "caesars"],
  "updated_at": "2025-10-19T10:35:00Z"
}
```

---

### 3. Backend Filtering Logic

**Apply filtering to ALL odds/alert endpoints:**

**Example: GET /api/games endpoint**

```python
# backend/api/games.py

@app.get("/api/games")
async def get_games(user_id: str):
    # Get user's enabled bookmakers
    user_settings = await get_user_settings(user_id)
    enabled_books = user_settings.enabled_bookmakers

    # Fetch all games from Odds API
    all_games = await fetch_odds_from_api()

    # Filter odds to only include user's bookmakers
    filtered_games = []
    for game in all_games:
        filtered_odds = [
            odd for odd in game.bookmakers
            if odd.key in enabled_books
        ]

        # Only include game if user has at least 2 bookmakers with odds
        if len(filtered_odds) >= 2:
            game.bookmakers = filtered_odds
            filtered_games.append(game)

    return filtered_games
```

**Result:** User only receives data for their selected bookmakers

---

### 4. Settings Page UI

#### Bookmaker Selection Grid

```tsx
// frontend/src/pages/Settings.tsx

export function Settings() {
  const { bookmakers, enabledBookmakers, toggleBookmaker } = useBookmakerSettings();

  return (
    <div className="settings-page">
      <section className="bookmaker-settings">
        <h2>📚 Active Sportsbooks</h2>
        <p className="text-slate-400">
          Select which sportsbooks you want to see in game cards and alerts.
          Only odds from your selected books will be displayed.
        </p>

        {/* Quick Selection Buttons */}
        <div className="quick-select-buttons">
          <button onClick={selectPopularUS}>
            🇺🇸 Select Popular US Books
          </button>
          <button onClick={selectAll}>
            ✅ Select All
          </button>
          <button onClick={deselectAll}>
            ❌ Deselect All
          </button>
        </div>

        {/* Bookmaker Grid */}
        <div className="bookmaker-grid">
          {bookmakers.map(book => (
            <BookmakerCard
              key={book.key}
              bookmaker={book}
              enabled={enabledBookmakers.includes(book.key)}
              onToggle={() => toggleBookmaker(book.key)}
            />
          ))}
        </div>

        {/* Save Button */}
        <button className="save-btn" onClick={saveSettings}>
          💾 Save Bookmaker Settings
        </button>

        {/* Active Count */}
        <div className="active-count">
          {enabledBookmakers.length} / {bookmakers.length} bookmakers selected
        </div>
      </section>
    </div>
  );
}
```

---

#### BookmakerCard Component

```tsx
// frontend/src/components/settings/BookmakerCard.tsx

interface BookmakerCardProps {
  bookmaker: Bookmaker;
  enabled: boolean;
  onToggle: () => void;
}

export function BookmakerCard({ bookmaker, enabled, onToggle }: BookmakerCardProps) {
  return (
    <div
      className={`bookmaker-card ${enabled ? 'enabled' : 'disabled'}`}
      onClick={onToggle}
    >
      {/* Logo */}
      <img
        src={bookmaker.logo}
        alt={bookmaker.name}
        className="w-10 h-10 object-contain"
        onError={(e) => e.currentTarget.style.display = 'none'}
      />

      {/* Name */}
      <div className="bookmaker-name">{bookmaker.name}</div>

      {/* Region Badge */}
      <div className="region-badge">
        {bookmaker.region.join(', ')}
      </div>

      {/* Toggle Checkbox */}
      <div className="toggle-indicator">
        {enabled ? (
          <span className="text-green-500 text-2xl">✅</span>
        ) : (
          <span className="text-slate-600 text-2xl">⬜</span>
        )}
      </div>

      {/* Popular Badge */}
      {bookmaker.popular && (
        <div className="popular-badge">⭐ Popular</div>
      )}
    </div>
  );
}
```

**Styling:**
```css
.bookmaker-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 2px solid #334155;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.bookmaker-card.enabled {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.bookmaker-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.bookmaker-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
  margin: 24px 0;
}
```

---

### 5. Frontend Filtering Hook

```tsx
// frontend/src/hooks/useBookmakerSettings.ts

import { useState, useEffect } from 'react';
import { BOOKMAKERS } from '@/data/bookmakers';

export function useBookmakerSettings() {
  const [enabledBookmakers, setEnabledBookmakers] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  // Fetch enabled bookmakers on mount
  useEffect(() => {
    fetchEnabledBookmakers();
  }, []);

  async function fetchEnabledBookmakers() {
    try {
      const response = await fetch('http://localhost:8000/api/settings/bookmakers');
      const data = await response.json();
      setEnabledBookmakers(data.enabled_bookmakers);
    } catch (error) {
      console.error('Failed to fetch bookmaker settings:', error);
      // Default to popular US books
      setEnabledBookmakers(['draftkings', 'fanduel', 'betmgm', 'caesars', 'betrivers']);
    } finally {
      setLoading(false);
    }
  }

  async function toggleBookmaker(bookKey: string) {
    const newEnabled = enabledBookmakers.includes(bookKey)
      ? enabledBookmakers.filter(k => k !== bookKey)
      : [...enabledBookmakers, bookKey];

    setEnabledBookmakers(newEnabled);
  }

  async function saveSettings() {
    try {
      await fetch('http://localhost:8000/api/settings/bookmakers', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled_bookmakers: enabledBookmakers })
      });
      // Show success toast
      toast.success('Bookmaker settings saved!');
    } catch (error) {
      toast.error('Failed to save settings');
    }
  }

  function selectPopularUS() {
    setEnabledBookmakers([
      'draftkings', 'fanduel', 'betmgm', 'caesars', 'betrivers',
      'pointsbet', 'fanatics', 'espnbet', 'betonlineag', 'bovada'
    ]);
  }

  function selectAll() {
    setEnabledBookmakers(Object.keys(BOOKMAKERS));
  }

  function deselectAll() {
    setEnabledBookmakers([]);
  }

  return {
    bookmakers: Object.values(BOOKMAKERS),
    enabledBookmakers,
    toggleBookmaker,
    saveSettings,
    selectPopularUS,
    selectAll,
    deselectAll,
    loading
  };
}
```

---

### 6. Backend Implementation

#### Settings Model

```python
# backend/models/user_settings.py

from pydantic import BaseModel
from typing import List
from datetime import datetime

class BookmakerSettings(BaseModel):
    enabled_bookmakers: List[str] = [
        "draftkings",
        "fanduel",
        "betmgm",
        "caesars",
        "betrivers"
    ]  # Default to major US books

class UserSettings(BaseModel):
    user_id: str
    bookmakers: BookmakerSettings
    updated_at: datetime

class BookmakerUpdate(BaseModel):
    enabled_bookmakers: List[str]
```

---

#### Settings API

```python
# backend/api/settings.py

from fastapi import APIRouter, HTTPException
from models.user_settings import BookmakerSettings, BookmakerUpdate
from database.settings_crud import get_bookmaker_settings, update_bookmaker_settings
from data.bookmakers import BOOKMAKERS

router = APIRouter()

@router.get("/api/settings/bookmakers")
async def get_bookmaker_settings(user_id: str = "default"):
    """Get user's enabled bookmakers"""
    try:
        settings = await get_bookmaker_settings(user_id)

        # Return enabled bookmakers + full list with enabled flags
        available = []
        for key, book in BOOKMAKERS.items():
            available.append({
                "key": book["key"],
                "name": book["name"],
                "region": book["region"],
                "logo": book["logo"],
                "popular": book.get("popular", False),
                "enabled": key in settings.enabled_bookmakers
            })

        return {
            "enabled_bookmakers": settings.enabled_bookmakers,
            "available_bookmakers": available
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/settings/bookmakers")
async def update_bookmakers(
    update: BookmakerUpdate,
    user_id: str = "default"
):
    """Update user's enabled bookmakers"""
    try:
        # Validate all bookmaker keys exist
        invalid = [k for k in update.enabled_bookmakers if k not in BOOKMAKERS]
        if invalid:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid bookmaker keys: {invalid}"
            )

        # Update in database
        settings = await update_bookmaker_settings(user_id, update.enabled_bookmakers)

        return {
            "success": True,
            "enabled_bookmakers": settings.enabled_bookmakers,
            "updated_at": settings.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

#### Database CRUD

```python
# backend/database/settings_crud.py

from models.user_settings import BookmakerSettings, UserSettings
from datetime import datetime
from typing import List

# In-memory storage (replace with actual database)
user_settings_db = {}

async def get_bookmaker_settings(user_id: str) -> BookmakerSettings:
    """Get user's bookmaker settings"""
    if user_id not in user_settings_db:
        # Return defaults
        return BookmakerSettings()

    return user_settings_db[user_id].bookmakers

async def update_bookmaker_settings(user_id: str, enabled_bookmakers: List[str]) -> UserSettings:
    """Update user's bookmaker settings"""
    settings = UserSettings(
        user_id=user_id,
        bookmakers=BookmakerSettings(enabled_bookmakers=enabled_bookmakers),
        updated_at=datetime.now()
    )

    user_settings_db[user_id] = settings
    return settings
```

---

### 7. Filtering in Odds Endpoints

#### Apply Filter to Games Endpoint

```python
# backend/api/games.py

@router.get("/api/games")
async def get_games(user_id: str = "default"):
    """Get games filtered by user's enabled bookmakers"""

    # Get user's enabled bookmakers
    settings = await get_bookmaker_settings(user_id)
    enabled_books = set(settings.enabled_bookmakers)

    # Fetch all games from Odds API
    all_games = await fetch_odds_from_api()

    # Filter games
    filtered_games = []
    for game in all_games:
        # Filter bookmakers in each game
        filtered_bookmakers = [
            book for book in game["bookmakers"]
            if book["key"] in enabled_books
        ]

        # Only include game if at least 2 enabled bookmakers have odds
        if len(filtered_bookmakers) >= 2:
            game["bookmakers"] = filtered_bookmakers
            filtered_games.append(game)

    return {"games": filtered_games, "count": len(filtered_games)}
```

---

#### Apply Filter to Alerts Endpoint

```python
# backend/api/alerts.py

@router.get("/api/alerts/all")
async def get_all_alerts(user_id: str = "default"):
    """Get alerts filtered by user's enabled bookmakers"""

    # Get user's enabled bookmakers
    settings = await get_bookmaker_settings(user_id)
    enabled_books = set(settings.enabled_bookmakers)

    # Detect arbitrage opportunities
    all_opportunities = await detect_arbitrage()

    # Filter opportunities where BOTH books are enabled
    filtered_opportunities = [
        opp for opp in all_opportunities
        if opp["book1"] in enabled_books and opp["book2"] in enabled_books
    ]

    return {
        "arbitrage": {
            "alerts": filtered_opportunities,
            "count": len(filtered_opportunities)
        }
    }
```

---

### 8. Visual Design

#### Settings Page Layout

```
┌─────────────────────────────────────────────────────────┐
│  ⚙️ Settings                                             │
│                                                          │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 📚 Active Sportsbooks                              │ │
│  │                                                     │ │
│  │ Select which sportsbooks you want to see in game   │ │
│  │ cards and alerts. Only odds from your selected     │ │
│  │ books will be displayed.                           │ │
│  │                                                     │ │
│  │ [🇺🇸 Popular US] [✅ Select All] [❌ Deselect All] │ │
│  │                                                     │ │
│  │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐      │ │
│  │ │   📱   │ │   📱   │ │   📱   │ │        │      │ │
│  │ │DraftKng│ │FanDuel │ │ BetMGM │ │Caesars │      │ │
│  │ │  ✅    │ │  ✅    │ │  ✅    │ │  ⬜    │      │ │
│  │ └────────┘ └────────┘ └────────┘ └────────┘      │ │
│  │                                                     │ │
│  │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐      │ │
│  │ │   📱   │ │   📱   │ │   📱   │ │   📱   │      │ │
│  │ │BetRivrs│ │ Bovada │ │BetOnlne│ │  BetUS │      │ │
│  │ │  ✅    │ │  ⬜    │ │  ⬜    │ │  ⬜    │      │ │
│  │ └────────┘ └────────┘ └────────┘ └────────┘      │ │
│  │                                                     │ │
│  │ ... (58 more bookmakers)                          │ │
│  │                                                     │ │
│  │ [💾 Save Bookmaker Settings]                      │ │
│  │                                                     │ │
│  │ 5 / 62 bookmakers selected                        │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

### 9. User Experience Flow

#### Initial Setup

```
User opens Settings for first time
    ↓
Default: Popular US books pre-selected
    ↓
User sees:
  ✅ DraftKings
  ✅ FanDuel
  ✅ BetMGM
  ✅ Caesars
  ✅ BetRivers
  ⬜ 57 other books
    ↓
User clicks "Save Bookmaker Settings"
    ↓
Backend stores: ["draftkings", "fanduel", "betmgm", "caesars", "betrivers"]
```

---

#### Viewing Filtered Game Cards

```
User opens Dashboard → Live Games
    ↓
Backend fetches odds from Odds API (38 NBA bookmakers)
    ↓
Backend filters to user's 5 enabled bookmakers
    ↓
Frontend receives only 5 bookmakers per game
    ↓
GameCard displays clean, focused odds:
  ┌─────────────────────────────┐
  │ Lakers vs Warriors          │
  │                             │
  │ DraftKings: Over 225.5 -110 │
  │ FanDuel:    Under 225.5 -110│
  │ BetMGM:     Over 226.0 -115 │
  │ Caesars:    Over 225.0 -105 │
  │ BetRivers:  Under 226.0 -110│
  │                             │
  │ (Instead of 38 bookmakers!) │
  └─────────────────────────────┘
```

---

#### Changing Settings

```
User realizes they opened a Bovada account
    ↓
Opens Settings → Sportsbooks
    ↓
Clicks Bovada card (⬜ → ✅)
    ↓
Clicks "Save Bookmaker Settings"
    ↓
Backend updates: adds "bovada" to enabled list
    ↓
User returns to Dashboard
    ↓
Bovada odds now appear in all game cards
```

---

### 10. Extension Sync

**Extension also respects bookmaker preferences:**

```javascript
// extension/background.js

async function fetchOpportunities() {
  try {
    // Backend already filters by user's bookmakers
    const response = await fetch(`${BACKEND_URL}/api/alerts/all`);
    const data = await response.json();

    // Opportunities already filtered to user's books
    currentOpportunities = data.arbitrage.alerts;

    console.log('[ARB] Received', currentOpportunities.length, 'opportunities');
    console.log('[ARB] (Filtered to user's enabled bookmakers)');
  } catch (error) {
    console.error('[ARB] Failed to fetch opportunities:', error);
  }
}
```

---

### 11. Benefits

#### For User ✅

1. ✅ **Clean UI** - Only see bookmakers they use
2. ✅ **Relevant alerts** - No opportunities from inaccessible books
3. ✅ **Faster decisions** - Less cognitive load
4. ✅ **Personalized** - Dashboard tailored to their accounts
5. ✅ **Easy setup** - Quick selection buttons for common configurations

#### For System ✅

1. ✅ **Less data transfer** - Backend filters before sending
2. ✅ **Faster rendering** - Fewer odds to display
3. ✅ **Better performance** - Less DOM manipulation
4. ✅ **Cleaner code** - Single filter point in backend
5. ✅ **Extensible** - Easy to add new bookmakers

---

### 12. Implementation Priority

#### Phase 1: Backend API (This Terminal - Day 1-2) ✅

1. ✅ Create `backend/api/settings.py` - Bookmaker settings endpoints
2. ✅ Create `backend/models/user_settings.py` - Pydantic models
3. ✅ Create `backend/database/settings_crud.py` - CRUD operations
4. ✅ Test endpoints with curl/Postman

**No Conflict:** Backend work is 100% isolated from frontend design

---

#### Phase 2: Settings Page (This Terminal - Day 3-4) ✅

1. ✅ Create `frontend/src/pages/Settings.tsx` - Main settings page
2. ✅ Create `frontend/src/components/settings/BookmakerCard.tsx` - Card component
3. ✅ Create `frontend/src/hooks/useBookmakerSettings.ts` - Settings hook
4. ✅ Add route to `App.tsx` (coordinate with other terminal)
5. ✅ Test bookmaker selection and save

**Minimal Conflict:** New files, only App.tsx needs coordination

---

#### Phase 3: Backend Filtering (This Terminal - Day 5) ✅

1. ✅ Update `backend/api/games.py` - Filter odds by enabled bookmakers
2. ✅ Update `backend/api/alerts.py` - Filter alerts by enabled bookmakers
3. ✅ Test filtered responses

**No Conflict:** Backend work only

---

#### Phase 4: Frontend Integration (Coordinate - Day 6) ⚠️

1. ⚠️ Update `GameCard.tsx` to use filtered odds (coordinate with other terminal)
2. ⚠️ Update dashboard to show filtered bookmakers
3. ⚠️ Test end-to-end filtering

**Coordination Needed:** Other terminal may be working on GameCard styling

---

### 13. Default Configurations

#### Popular US Configuration (Default)
```json
{
  "enabled_bookmakers": [
    "draftkings",
    "fanduel",
    "betmgm",
    "caesars",
    "betrivers",
    "pointsbet",
    "fanatics",
    "espnbet"
  ]
}
```

#### Offshore Configuration
```json
{
  "enabled_bookmakers": [
    "betonlineag",
    "bovada",
    "mybookieag",
    "betus",
    "lowvig"
  ]
}
```

#### All Books (For Testing)
```json
{
  "enabled_bookmakers": [
    "draftkings",
    "fanduel",
    "betmgm",
    // ... all 62 bookmakers
  ]
}
```

---

## Summary

### What We're Building

**Settings Page:**
- Grid of all 62 bookmakers
- Click to enable/disable each
- Quick selection buttons
- Save to backend

**Backend Filtering:**
- Store user's enabled bookmakers
- Filter all odds/alerts by enabled books
- Only send relevant data to frontend

**Result:**
- User only sees bookmakers they care about
- Cleaner UI, faster decisions
- Personalized experience

### Can We Build This Without Conflicting?

**✅ YES - 95% of work is isolated:**
- Backend API: 100% separate
- Settings page: New files, no conflict
- Backend filtering: No conflict
- Only coordination needed: GameCard integration (Phase 4)

---

**Ready to start with backend bookmaker settings API?** 🚀
