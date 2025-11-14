# Strategy Alerts Implementation Summary

## ✅ Completed (Frontend)

### 1. **TypeScript Types** (`frontend/src/types.ts`)
- ✅ `StrategyAlert` interface - Complete alert data structure
- ✅ `BetOption` interface - Multiple bet recommendations per alert
- ✅ Added `strategy_alerts?: StrategyAlert[]` to `LiveGame` interface

### 2. **UI Components Created**

#### `StrategyAlertBadge.tsx` - Compact Alert Display
- Shows on game cards
- Color-coded by confidence (CRITICAL/HIGH/MEDIUM/LOW)
- Animated pulse for CRITICAL alerts
- Auto-rotates through multiple alerts (5s intervals)
- Shows key stats: Edge, ROI, Win Rate, Units
- **Audio alerts** for HIGH/CRITICAL confidence
- Click to view details

#### `StrategyAlertDetail.tsx` - Full Alert Modal
- Detailed strategy explanation
- Multiple bet options with:
  - Primary bookmaker button
  - Alternative bookmakers
  - Odds comparison
  - Expected value calculation
  - Kelly Criterion sizing
- Strategy reasoning/justification
- Urgency countdown for expiring alerts

### 3. **Features Implemented**
- ✅ Visual indicators (gradient backgrounds, borders, glows)
- ✅ Animated pulse for urgent alerts
- ✅ Audio alerts (beep tones, double beep for CRITICAL)
- ✅ Multi-alert rotation on cards
- ✅ Expiration countdown timers
- ✅ Confidence-based styling
- ✅ One-click bookmaker opening

---

## 🔧 Next Steps

### Backend Integration Required

The backend needs to analyze games and return strategy alerts. Here's the required data structure:

#### **1. Backend API Response Format**

When returning games via `/api/games`, each game should include:

```python
{
  "state": { ... },  # Existing game state
  "odds": [ ... ],   # Existing odds
  "projection": { ... },  # Existing projection
  # ... other existing fields ...

  # NEW: Strategy alerts
  "strategy_alerts": [
    {
      "strategy_id": "quarter_reversal",
      "strategy_name": "NBA Quarter Reversal",
      "confidence": "HIGH",  # CRITICAL, HIGH, MEDIUM, LOW
      "trigger": "Lakers dominated Q2 by +12 pts, now down in Q3. Historical 60.3% ATS reversal pattern.",
      "recommendation": "Bet UNDER 2H 110.5 total",
      "edge_percentage": 8.5,  # %
      "expected_roi": 12.1,  # %
      "win_probability": 0.603,  # 60.3%
      "stake_recommendation": 1.5,  # units
      "bet_options": [
        {
          "label": "Under 2H 110.5",
          "market_type": "totals",
          "bet_side": "UNDER",
          "line": 110.5,
          "odds": -110,
          "bookmaker": "draftkings",
          "bookmaker_title": "DraftKings",
          "probability": 0.603,
          "expected_value": 0.089,
          "kelly_size": 1.5,
          "alt_bookmakers": [
            {"bookmaker": "fanduel", "bookmaker_title": "FanDuel", "odds": -108},
            {"bookmaker": "betmgm", "bookmaker_title": "BetMGM", "odds": -112}
          ]
        }
      ],
      "reasoning": "When favorites trail after opponent hot start, they typically cover 60.3% ATS at halftime (2005-2023 NBA data). Lakers showing regression indicators: opponent shooting 18% above season avg.",
      "urgency": "HIGH",
      "expires_in": 420,  # seconds (7 minutes)
      "sound_alert": true,
      "timestamp": "2025-11-07T14:30:00Z"
    }
  ]
}
```

#### **2. Backend Strategy Integration Points**

The backend should run these strategies on live/upcoming games:

##### **For LIVE Games:**
1. **Quarter Reversal** (`nba_quarter_reversal.py`)
   - Run at end of Q1, Q2, Q3
   - Check for hot start reversals

2. **Momentum Detector** (`momentum_detector.py`)
   - Run continuously during live games
   - Detect scoring runs, shot streaks

3. **Live Betting Strategy** (`live_betting_strategy.py`)
   - Check for market overreactions
   - Fair value vs current odds

##### **For UPCOMING Games:**
1. **Favorite Comeback** (`favorite_comeback_detector.py`)
   - Run when game goes live (Q1 starts)
   - Check if favorite is trailing

2. **Fatigue Strategy** (`fatigue_strategy.py`)
   - Run 1-2 hours before game
   - Back-to-back, travel, rest days

3. **Halftime Tracker** (`halftime_tracker.py`)
   - Run at halftime
   - 2H betting opportunities

4. **Regression Strategy** (`regression_strategy.py`)
   - Run pregame
   - Identify over/underperforming teams

5. **Player Props** (`player_props_strategy.py`)
   - Run when props are available
   - Usage rates, matchup analysis

#### **3. Backend Implementation Approach**

**Option A: Real-time Strategy Engine**
```python
# In game_tracker.py or similar
def analyze_game_strategies(game_state, odds, stats):
    alerts = []

    # Run applicable strategies
    if game_state['status'] == 'live':
        # Quarter Reversal
        if game_state['quarter'] in [2, 3, 4]:
            qr_alert = check_quarter_reversal(game_state, stats)
            if qr_alert:
                alerts.append(qr_alert)

        # Momentum
        momentum_alert = check_momentum(game_state, stats)
        if momentum_alert:
            alerts.append(momentum_alert)

    elif game_state['status'] == 'upcoming':
        # Fatigue
        fatigue_alert = check_fatigue(game_state, stats)
        if fatigue_alert:
            alerts.append(fatigue_alert)

    return alerts
```

**Option B: Batch Strategy Runner**
```python
# Run every 60 seconds
def run_all_strategies():
    games = get_all_games()
    for game in games:
        game['strategy_alerts'] = analyze_game_strategies(game)
    return games
```

---

## 📊 Strategy Priority List

### **High Priority (Implement First)**
1. ✅ **Quarter Reversal** - Most profitable, clear triggers
2. ✅ **Halftime Tracker** - 60.2% ATS, proven system
3. ✅ **Momentum Detector** - Real-time scoring runs
4. ✅ **Favorite Comeback** - 60.3% ATS at HT

### **Medium Priority**
5. ✅ **Fatigue Strategy** - B2B/travel detection
6. ✅ **Regression Strategy** - Mean reversion
7. ✅ **Live Betting** - Market overreactions
8. ✅ **Injury Cascade** - Star injury overreactions

### **Low Priority (Future)**
9. **Player Props** - Requires props data
10. **Weather** - NFL outdoor games only
11. **Sharp Money Tracker** - Requires line movement data
12. **CLV Tracker** - Requires closing lines

---

## 🎨 Visual Design Summary

### Confidence Level Colors
- **CRITICAL** 🚨 - Red gradient, pulse animation, double beep
- **HIGH** 🔥 - Orange gradient, single beep
- **MEDIUM** ⚡ - Yellow gradient, no sound
- **LOW** 💡 - Blue gradient, no sound

### Alert Card Structure
```
┌─────────────────────────────────────┐
│ 🔥 NBA Quarter Reversal  +8.5% Edge│
│ HIGH CONFIDENCE                     │
├─────────────────────────────────────┤
│ Lakers dominated Q2, now trailing   │
├─────────────────────────────────────┤
│ ROI: +12.1% | Win: 60.3% | 1.5u    │
└─────────────────────────────────────┘
```

---

## 📱 Integration into GameCard

To integrate into `GameCard.tsx`:

```typescript
import { StrategyAlertBadge } from './StrategyAlertBadge';
import { StrategyAlertDetail } from './StrategyAlertDetail';

export function GameCard({ game }: GameCardProps) {
  const [selectedAlert, setSelectedAlert] = useState<StrategyAlert | null>(null);

  return (
    <div className="game-card">
      {/* Strategy Alerts - Show at top of card */}
      {game.strategy_alerts && game.strategy_alerts.length > 0 && (
        <StrategyAlertBadge
          alerts={game.strategy_alerts}
          onAlertClick={(alert) => setSelectedAlert(alert)}
        />
      )}

      {/* Existing game card content */}
      {/* ... teams, stats, odds ... */}

      {/* Alert Detail Modal */}
      {selectedAlert && (
        <StrategyAlertDetail
          alert={selectedAlert}
          onClose={() => setSelectedAlert(null)}
        />
      )}
    </div>
  );
}
```

---

## 🔊 Audio Alert Behavior

- **Plays once per alert** (tracked by `strategy_id`)
- **Only for HIGH/CRITICAL** confidence
- **Different tones:**
  - CRITICAL: 1200 Hz, double beep
  - HIGH: 900 Hz, single beep
- **Volume:** 30% to avoid being jarring
- **Duration:** 0.3 seconds per beep

---

## 🎯 Success Metrics

Once implemented, track:
1. **Alert Accuracy** - % of alerts that hit
2. **User Engagement** - Click-through rate on alerts
3. **ROI** - Actual returns vs predicted
4. **Alert Frequency** - How many alerts per hour
5. **False Positives** - Alerts that don't materialize

---

## 📝 Files Modified/Created

### Frontend
- ✅ `frontend/src/types.ts` - Added StrategyAlert & BetOption types
- ✅ `frontend/src/components/StrategyAlertBadge.tsx` - NEW
- ✅ `frontend/src/components/StrategyAlertDetail.tsx` - NEW
- ⏳ `frontend/src/components/GameCard.tsx` - PENDING integration

### Backend (Required)
- ⏳ `backend/game_tracker.py` - Add strategy analysis
- ⏳ `backend/main.py` - Include strategy_alerts in /api/games response
- ⏳ Create `backend/strategy_engine.py` - Unified strategy runner

---

## 🚀 Next Actions

1. **Backend:** Create unified strategy engine that:
   - Runs appropriate strategies per game
   - Returns formatted alerts matching TypeScript interface
   - Caches results for 60s to avoid recomputation

2. **Frontend:** Integrate StrategyAlertBadge into GameCard.tsx
   - Import components
   - Add state for selected alert
   - Render badge at top of card

3. **Testing:** Use mock data to test UI before backend ready

4. **Production:** Deploy and monitor alert accuracy

---

## 💡 Mock Data for Testing

```typescript
const mockAlert: StrategyAlert = {
  strategy_id: 'quarter_reversal',
  strategy_name: 'NBA Quarter Reversal',
  confidence: 'HIGH',
  trigger: 'Lakers dominated Q2 by +12 pts, now trailing in Q3',
  recommendation: 'Bet UNDER 2H 110.5',
  edge_percentage: 8.5,
  expected_roi: 12.1,
  win_probability: 0.603,
  stake_recommendation: 1.5,
  sound_alert: true,
  timestamp: new Date().toISOString(),
  expires_in: 420,
  bet_options: [{
    label: 'Under 2H 110.5',
    market_type: 'totals',
    bet_side: 'UNDER',
    line: 110.5,
    odds: -110,
    bookmaker: 'draftkings',
    bookmaker_title: 'DraftKings',
    probability: 0.603,
    expected_value: 0.089,
    kelly_size: 1.5
  }]
};
```

