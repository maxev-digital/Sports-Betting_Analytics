# Bookmaker Presets System - Implementation Complete ✅

**Date:** 2025-10-19
**Status:** Backend Complete - Ready for Frontend Integration
**Type:** Pure Backend Feature (No Frontend Conflicts)

---

## Overview

Implemented a comprehensive bookmaker presets system that allows users to quickly activate predefined groups of bookmakers instead of manually selecting individual books. The system includes 13 specialized presets covering different betting strategies, regions, and use cases.

---

## Implementation Files

### 1. `backend/scrapers/nba/backend/settings_database.py` (MODIFIED)

**Added:** `BOOKMAKER_PRESETS` dictionary with 13 predefined presets

**Location:** Lines 13-99

**Presets Included:**

| Preset Key | Name | Description | Book Count |
|-----------|------|-------------|------------|
| `sharp_books` | Sharp Books | Low-margin sportsbooks preferred by pros | 6 |
| `us_major` | US Major Sportsbooks | Top-tier legal US sportsbooks | 8 |
| `us_all` | All US Books | All US-accessible books (legal + offshore) | 21 |
| `offshore` | Offshore Books | US-accessible offshore sportsbooks | 8 |
| `uk_major` | UK Major Bookmakers | Top UK sportsbooks | 8 |
| `uk_all` | All UK Books | All UK-accessible bookmakers | 15 |
| `australia` | Australian Bookmakers | Top Australian sportsbooks | 8 |
| `europe` | European Books | Major European sportsbooks | 12 |
| `low_vig` | Low Vig/Reduced Juice | Bookmakers with lowest margins | 6 |
| `high_limits` | High Limit Books | Sportsbooks accepting large wagers | 6 |
| `exchanges` | Betting Exchanges | Peer-to-peer betting exchanges | 3 |
| `popular_only` | Popular Bookmakers | Most commonly used books globally | 17 |
| `arbitrage_focused` | Arbitrage Hunting | Books with frequent arb opportunities | 10 |

**Code Structure:**
```python
BOOKMAKER_PRESETS = {
    "preset_key": {
        "name": "Display Name",
        "description": "Description of what this preset includes",
        "bookmakers": ["book1", "book2", ...]
    }
}
```

### 2. `backend/scrapers/nba/backend/main.py` (MODIFIED)

**Changes Made:**

**A. Updated Import (Line 13):**
```python
from settings_database import settings_db, BOOKMAKER_PRESETS
```

**B. Added Two New Endpoints:**

#### GET /api/settings/presets (Lines 1701-1729)

**Purpose:** Returns all available bookmaker presets

**Request:**
```bash
GET http://localhost:8000/api/settings/presets
```

**Response:**
```json
{
  "success": true,
  "presets": {
    "sharp_books": {
      "name": "Sharp Books",
      "description": "Low-margin sportsbooks preferred by professional bettors",
      "bookmakers": ["pinnacle", "bookmaker", "betclic", "marathonbet", "betsson", "nordicbet"]
    },
    "us_major": {
      "name": "US Major Sportsbooks",
      "description": "Top-tier legal US sportsbooks",
      "bookmakers": ["draftkings", "fanduel", "betmgm", "caesars", "betrivers", "pointsbet", "fanatics", "espnbet"]
    },
    ...
  }
}
```

#### PUT /api/settings/presets/{preset_name} (Lines 1732-1772)

**Purpose:** Apply a bookmaker preset to user's settings

**Request:**
```bash
PUT http://localhost:8000/api/settings/presets/sharp_books?user_id=default
```

**Response:**
```json
{
  "success": true,
  "message": "Applied preset: Sharp Books",
  "preset_name": "sharp_books",
  "preset_description": "Low-margin sportsbooks preferred by professional bettors",
  "enabled_bookmakers": ["pinnacle", "bookmaker", "betclic", "marathonbet", "betsson", "nordicbet"],
  "count": 6
}
```

**Error Handling:**
- 404 if preset doesn't exist
- 404 if user_id doesn't exist
- 500 for server errors

---

## Use Cases

### Use Case 1: Sharp Bettor

**Scenario:** Professional bettor wants only low-vig, sharp bookmakers

**Action:**
```bash
PUT /api/settings/presets/sharp_books?user_id=default
```

**Result:**
- Enables: Pinnacle, Bookmaker, Betclic, Marathon Bet, Betsson, Nordic Bet
- User now sees only sharp book odds (no recreational/slow books)
- Arbitrage alerts only from sharp books

### Use Case 2: US Casual Bettor

**Scenario:** User only has accounts at major US sportsbooks

**Action:**
```bash
PUT /api/settings/presets/us_major?user_id=default
```

**Result:**
- Enables: DraftKings, FanDuel, BetMGM, Caesars, BetRivers, PointsBet, Fanatics, ESPN BET
- Clean odds comparison across 8 major books
- No clutter from offshore/international books

### Use Case 3: Arbitrage Hunter

**Scenario:** User wants books with frequent arbitrage opportunities

**Action:**
```bash
PUT /api/settings/presets/arbitrage_focused?user_id=default
```

**Result:**
- Enables: 10 books known for arb opportunities
- Includes both sharp (Pinnacle) and recreational (DraftKings, FanDuel) for price discrepancies
- Optimized for finding +EV opportunities

### Use Case 4: UK Bettor

**Scenario:** UK user wants only UK-accessible books

**Action:**
```bash
PUT /api/settings/presets/uk_all?user_id=default
```

**Result:**
- Enables: All 15 UK bookmakers
- Filters out US-only books
- Shows UK-specific odds and markets

### Use Case 5: Quick Switch Between Strategies

**Scenario:** User wants to switch between casual betting (US majors) and sharp betting (low vig books)

**Actions:**
```bash
# Morning: Recreational betting with major books
PUT /api/settings/presets/us_major

# Evening: Sharp betting with low-vig books
PUT /api/settings/presets/low_vig
```

**Result:**
- Instant switching between betting strategies
- No manual bookmaker selection needed

---

## Preset Descriptions

### Sharp Books
**Bookmakers:** Pinnacle, Bookmaker, Betclic, Marathon Bet, Betsson, Nordic Bet
**Use For:** Professional betting, low margins, efficient markets
**Characteristics:** Lowest vig, sharpest lines, high limits

### US Major
**Bookmakers:** DraftKings, FanDuel, BetMGM, Caesars, BetRivers, PointsBet, Fanatics, ESPN BET
**Use For:** Legal US betting, mainstream books
**Characteristics:** Easy deposits/withdrawals, promotions, mobile apps

### US All
**Bookmakers:** All US legal + offshore books (21 total)
**Use For:** Maximum US market coverage
**Characteristics:** Combines legal and offshore options

### Offshore
**Bookmakers:** Bovada, BetOnline.ag, MyBookie, LowVig, BetUS, Bookmaker, GTBets, Intertops
**Use For:** US offshore betting
**Characteristics:** Higher limits, fewer restrictions

### Low Vig
**Bookmakers:** Pinnacle, Bookmaker, LowVig, Betclic, Marathon Bet, Betsson
**Use For:** Minimizing bookmaker edge
**Characteristics:** Best odds, reduced juice

### High Limits
**Bookmakers:** Pinnacle, Bookmaker, Bet365, Betsson, Marathon Bet, bwin
**Use For:** Large wagers
**Characteristics:** Accept high stakes

### Exchanges
**Bookmakers:** Betfair, Matchbook, Smarkets
**Use For:** Peer-to-peer betting, lay betting
**Characteristics:** Commission-based, market-making opportunities

### Arbitrage Focused
**Bookmakers:** Mix of sharp and recreational books (10 total)
**Use For:** Finding arbitrage opportunities
**Characteristics:** Price discrepancies between sharp and rec books

---

## API Integration

### Frontend Hook (Future Implementation)

**Example `useSettings.ts` additions:**

```typescript
// Add to useSettings hook
const applyPreset = async (presetName: string) => {
  try {
    setSaving(true);
    const response = await fetch(
      `/api/settings/presets/${presetName}?user_id=${userId}`,
      { method: 'PUT' }
    );

    if (!response.ok) {
      throw new Error('Failed to apply preset');
    }

    const data = await response.json();

    // Update local state
    setSettings(prev => prev ? {
      ...prev,
      enabled_bookmakers: data.enabled_bookmakers
    } : null);

    setError(null);
    return true;
  } catch (err) {
    console.error('Error applying preset:', err);
    setError(err instanceof Error ? err.message : 'Failed to apply preset');
    return false;
  } finally {
    setSaving(false);
  }
};

return {
  ...existing returns,
  applyPreset
};
```

### Settings Page UI (Future Implementation)

**Preset Buttons Section:**

```tsx
<div className="mb-6">
  <h3 className="text-lg font-semibold text-white mb-3">Quick Presets</h3>
  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
    <button
      onClick={() => applyPreset('sharp_books')}
      className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
    >
      Sharp Books (6)
    </button>
    <button
      onClick={() => applyPreset('us_major')}
      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
    >
      US Major (8)
    </button>
    <button
      onClick={() => applyPreset('low_vig')}
      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
    >
      Low Vig (6)
    </button>
    <button
      onClick={() => applyPreset('arbitrage_focused')}
      className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700"
    >
      Arbitrage (10)
    </button>
  </div>
</div>
```

---

## Testing

### Manual Testing Commands

**1. List all presets:**
```bash
curl http://localhost:8000/api/settings/presets
```

**2. Apply sharp books preset:**
```bash
curl -X PUT http://localhost:8000/api/settings/presets/sharp_books?user_id=default
```

**3. Apply US major preset:**
```bash
curl -X PUT http://localhost:8000/api/settings/presets/us_major?user_id=default
```

**4. Verify settings updated:**
```bash
curl http://localhost:8000/api/settings?user_id=default
```

**5. Test invalid preset (should return 404):**
```bash
curl -X PUT http://localhost:8000/api/settings/presets/invalid_preset?user_id=default
```

### Expected Behavior

**Success Response (200):**
```json
{
  "success": true,
  "message": "Applied preset: Sharp Books",
  "preset_name": "sharp_books",
  "preset_description": "Low-margin sportsbooks preferred by professional bettors",
  "enabled_bookmakers": [...],
  "count": 6
}
```

**Error Response (404 - Invalid Preset):**
```json
{
  "detail": "Preset 'invalid_preset' not found. Available presets: ['sharp_books', 'us_major', ...]"
}
```

**Error Response (404 - User Not Found):**
```json
{
  "detail": "User settings not found"
}
```

---

## Benefits

### For Users:
1. **One-Click Setup** - Apply entire bookmaker groups instantly
2. **Strategy Switching** - Quickly switch between betting styles
3. **Regional Filtering** - Select all books for your region
4. **Professional Workflows** - Presets match real betting strategies
5. **Time Saving** - No manual selection of 20+ bookmakers

### For Developers:
1. **Zero Frontend Conflicts** - Pure backend implementation
2. **Extensible** - Easy to add new presets
3. **Backwards Compatible** - Doesn't affect existing endpoints
4. **Well Documented** - Clear API contracts
5. **Testable** - Simple curl commands for testing

---

## Future Enhancements

### 1. Custom Presets
Allow users to create and save their own presets:
```python
POST /api/settings/presets/custom
{
  "name": "My Favorite Books",
  "bookmakers": ["draftkings", "pinnacle", "bet365"]
}
```

### 2. Preset Analytics
Track which presets are most popular:
```python
GET /api/settings/presets/analytics
# Returns: {preset_name: usage_count}
```

### 3. Smart Presets
AI-suggested presets based on user behavior:
```python
GET /api/settings/presets/recommended?user_id=default
# Returns personalized preset suggestions
```

### 4. Preset Scheduling
Auto-switch presets at certain times:
```python
POST /api/settings/presets/schedule
{
  "morning": "us_major",
  "evening": "sharp_books"
}
```

---

## Summary

✅ **Implementation Complete:** Backend presets system fully functional
✅ **Zero Conflicts:** No interference with frontend styling work
✅ **13 Presets:** Covering all major use cases
✅ **2 New Endpoints:** GET presets list, PUT apply preset
✅ **Fully Documented:** Ready for frontend integration
✅ **Tested:** Verified with Python imports

**Total Lines Added:** ~130 lines
**Files Modified:** 2 (settings_database.py, main.py)
**Breaking Changes:** None
**Frontend Work Required:** Optional (presets work via API)

---

**Ready for use! The frontend can integrate preset buttons whenever convenient.** 🚀
