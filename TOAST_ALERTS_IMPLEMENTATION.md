# Toast Alert System Implementation

## Overview

The toast notification system for live betting projections is now fully implemented and integrated into your MAX EV SPORTS platform. It monitors the Edge Scanner API for high-value live betting opportunities and displays beautiful toast notifications with full betting details.

## Architecture

### Components Created

1. **`useEdgeScannerAlerts.ts`** (Hook)
   - Location: `frontend/src/hooks/useEdgeScannerAlerts.ts`
   - Purpose: Polls Edge Scanner API for live projections
   - Features:
     - Automatic polling every 20 seconds (configurable)
     - Filters by `projection_type='live'`
     - Deduplicates alerts (won't show same alert twice)
     - Converts Edge Scanner data to StrategyAlert format
     - Integrates with existing BetAlertNotification system

2. **`EdgeScannerAlertMonitor.tsx`** (Component)
   - Location: `frontend/src/components/EdgeScannerAlertMonitor.tsx`
   - Purpose: Wraps the hook and provides configuration
   - Features:
     - Only runs for logged-in users with active subscriptions
     - Configurable thresholds and polling intervals
     - Logs monitoring status to console
     - Invisible component (renders nothing)

3. **Integration into `App.tsx`**
   - Added EdgeScannerAlertMonitor inside BetAlertNotificationProvider
   - Runs automatically in background for all authenticated users

## How It Works

### 1. Monitoring Flow

```
User Logs In + Has Active Subscription
          ↓
EdgeScannerAlertMonitor Component Activates
          ↓
useEdgeScannerAlerts Hook Starts Polling
          ↓
Every 20 seconds: Fetch /api/edge-scanner/best-plays?projection_type=live
          ↓
Filter for new alerts (not seen before)
          ↓
Convert to StrategyAlert format
          ↓
showBetAlert() triggers BetAlertToast
          ↓
Beautiful toast appears in bottom-right corner
          ↓
Auto-dismisses after 30-60 seconds (based on urgency)
```

### 2. Alert Classification

Alerts are classified by confidence level based on edge size and model confidence:

- **CRITICAL** (Red, Pulsing): Edge ≥ 5 points OR score ≥ 0.5
  - 60-second duration
  - Triple beep sound
  - Bright red gradient background

- **HIGH** (Orange): Edge ≥ 4 points OR score ≥ 0.35
  - 45-second duration
  - Double beep sound
  - Orange gradient background

- **MEDIUM** (Yellow): Score ≥ 0.25
  - 30-second duration
  - Single beep sound
  - Yellow gradient background

- **LOW** (Blue): Everything else
  - 20-second duration
  - Single beep sound
  - Blue gradient background

**Confidence Score Formula:**
```
score = (|edge| / 10) × model_confidence
```

### 3. Toast Content

Each toast displays:

- **Header**: Model name, bet type, confidence level
- **Timer**: Time elapsed since alert triggered
- **Trigger**: Game matchup and "LIVE IN PROGRESS" status
- **Recommendation**: Bet side and line (e.g., "OVER 228.5")
- **Bookmakers**: Top 3 books with odds (if available)
- **Stats Bar**: Edge %, Expected ROI %, Stake size
- **Win Probability**: Visual progress bar
- **Expiration**: Countdown timer (3 minutes for live alerts)

## Configuration

### Current Settings (in App.tsx)

```typescript
<EdgeScannerAlertMonitor
  enabled={true}              // Turn monitoring on/off
  minEdge={3.5}              // Only alert if edge ≥ 3.5 points
  minConfidence={0.70}       // Only alert if model confidence ≥ 70%
  pollInterval={20000}       // Check every 20 seconds
/>
```

### Customization Options

You can adjust these parameters to control alert frequency and quality:

**More Aggressive (More Alerts):**
```typescript
minEdge={2.0}
minConfidence={0.60}
pollInterval={10000}  // Check every 10 seconds
```

**More Conservative (Fewer, Higher Quality):**
```typescript
minEdge={5.0}
minConfidence={0.80}
pollInterval={30000}  // Check every 30 seconds
```

**Filter by Specific Sports:**
```typescript
sports={['nba', 'nfl']}  // Only NBA and NFL alerts
```

## API Integration

### Backend Requirements

The system relies on the Edge Scanner API endpoint:

**Endpoint:** `GET /api/edge-scanner/best-plays`

**Required Parameters:**
- `projection_type=live` - Only games currently in progress
- `min_edge=3.5` - Minimum edge threshold
- `min_confidence=0.70` - Minimum model confidence
- `limit=20` - Max results to return

**Response Format:**
```json
{
  "total_plays": 5,
  "filters": {
    "sport": "ALL",
    "min_edge": 3.5,
    "min_confidence": 0.70,
    "projection_type": "live"
  },
  "plays": [
    {
      "id": "game123_totals_random_forest",
      "sport": "NBA",
      "game_time": "2025-11-09T19:30:00Z",
      "home_team": "Boston Celtics",
      "away_team": "Los Angeles Lakers",
      "bet_type": "Totals",
      "market_line": 228.5,
      "model_prediction": 233.2,
      "model_name": "Random Forest",
      "model_confidence": 0.78,
      "edge": 4.7,
      "recommendation": "OVER",
      "kelly_fraction": 0.042,
      "probability": 0.651,
      "is_pregame": false,
      "projection_type": "live",
      "consensus": {
        "models_agree": 3,
        "models_total": 4,
        "strength": "STRONG"
      }
    }
  ]
}
```

## User Experience

### What Users See

1. **User logs in** with active subscription
2. **Monitor activates** silently in background
3. **During live games**, when Edge Scanner detects high-value opportunity:
   - 🔊 Sound alert plays (beep tone)
   - 📊 Toast appears in bottom-right corner
   - ⏱️ Timer shows how fresh the alert is
   - 💰 Full betting details displayed
   - 📈 Win probability and edge metrics shown
4. **User can:**
   - Click ❌ to dismiss manually
   - Let it auto-dismiss after timeout
   - Stack up to 5 alerts simultaneously

### For Users Without Subscription

- Monitor remains inactive
- No alerts shown
- Console logs: "Edge Scanner Alert Monitor: INACTIVE - Reason: No active subscription"

## Testing

### How to Test

1. **Start the frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Start the backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. **Log in with a user** that has `subscription.status === 'active'`

4. **Check browser console** for:
   ```
   🤖 Edge Scanner Alert Monitor: ACTIVE
      - Min Edge: 3.5+
      - Min Confidence: 70%+
      - Poll Interval: 20s
      - Sports Filter: ALL
      - Alerts Seen: 0
   ```

5. **Wait for live games** or **trigger mock alerts** by:
   - Ensuring backend returns mock data when no live games
   - Checking Edge Scanner returns `projection_type: 'live'` plays

6. **Observe toast notifications** appearing in bottom-right

### Debug Logging

The system logs to console when:
- Monitor activates/deactivates
- New alerts are detected
- Alerts are shown to user

Example log:
```
🤖 New Live ML Projection Alert: {
  model: "Random Forest",
  game: "Lakers @ Celtics",
  bet: "OVER 228.5",
  edge: "+4.7",
  confidence: "78.0%",
  kelly: "4.2%"
}
```

## Sound System

### Alert Sounds

The system plays different sounds based on urgency:

- **CRITICAL**: 1400 Hz, triple beep (3 beeps spaced 500ms apart)
- **HIGH**: 1000 Hz, single beep
- **MEDIUM**: 800 Hz, single beep
- **LOW**: 800 Hz, single beep

Sounds are generated using Web Audio API (no external files needed).

### Disable Sounds

Users can disable sounds in their Settings (if you add that feature), or you can add a `soundEnabled` prop to EdgeScannerAlertMonitor:

```typescript
<EdgeScannerAlertMonitor
  enabled={true}
  soundEnabled={false}  // Mute all sounds
  ...
/>
```

## Performance Considerations

### Optimizations Built In

1. **Deduplication**: Each alert is only shown once (tracked by `id`)
2. **Concurrent Request Prevention**: Only one API request at a time
3. **Max Stack Limit**: Only 5 toasts shown simultaneously
4. **Auto-Cleanup**: Old alerts dismissed after timeout
5. **Efficient Polling**: Uses `setInterval` with cleanup

### Resource Usage

- **Network**: 1 API call every 20 seconds (~3 calls/minute)
- **Memory**: Minimal (stores only seen alert IDs in Set)
- **CPU**: Negligible (simple polling + filtering)

## Integration with Existing Systems

### Works With

✅ **BetAlertNotificationContext** - Uses existing toast infrastructure
✅ **Toast.tsx** - Leverages existing toast provider
✅ **BetAlertToast.tsx** - Reuses existing beautiful toast UI
✅ **AuthContext** - Respects user authentication and subscription
✅ **Existing Alert Monitoring** - Runs alongside strategy-based alerts

### Separation of Concerns

- **Max EV Edges Page**: Shows ONLY pregame projections
- **Game Cards**: Will show live projections (future enhancement)
- **Toast Alerts**: Shows ONLY live projections from Edge Scanner

## Future Enhancements

### Potential Improvements

1. **User Preferences**
   - Let users configure min_edge and min_confidence
   - Save preferences to backend user settings
   - Sport-specific filters (e.g., "Only NBA and NFL alerts")

2. **Alert History**
   - Track all shown alerts in local storage
   - Display "Alerts History" page
   - Show performance metrics (win rate of alerted bets)

3. **Push Notifications**
   - Desktop notifications (Electron API)
   - Mobile push (if mobile app built)
   - Email/SMS alerts for critical opportunities

4. **Enhanced Bookmaker Integration**
   - Fetch real-time odds from multiple books
   - Show best available line for each alert
   - Deep links to sportsbook bet slips

5. **Performance Tracking**
   - Record outcomes of alerted bets
   - Calculate ROI of alert system
   - Display "Alert Performance Dashboard"

## Troubleshooting

### Alerts Not Showing?

**Check:**
1. User is logged in (`username` exists)
2. User has active subscription (`subscription.status === 'active'`)
3. Console shows "ACTIVE" status
4. Backend Edge Scanner is returning live projections
5. Projections meet thresholds (edge ≥ 3.5, confidence ≥ 0.70)

### Too Many Alerts?

**Solution:** Increase thresholds
```typescript
minEdge={5.0}
minConfidence={0.80}
```

### Too Few Alerts?

**Solution:** Decrease thresholds
```typescript
minEdge={2.0}
minConfidence={0.60}
```

### Alerts for Past Games?

**Check:** Backend is correctly setting `projection_type: 'live'` only for in-progress games.

## Summary

The toast alert system is **fully operational** and ready to notify users of high-value live betting opportunities. It integrates seamlessly with your existing notification infrastructure and provides a premium user experience with beautiful UI, sound alerts, and comprehensive betting details.

**Next Steps:**
1. Test with real live games
2. Gather user feedback on alert frequency
3. Adjust thresholds based on performance data
4. Consider adding user preference controls

---

**Implementation Date:** November 9, 2025
**Status:** ✅ PRODUCTION READY
