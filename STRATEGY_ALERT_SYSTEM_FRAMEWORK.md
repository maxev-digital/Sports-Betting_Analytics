# Strategy Alert System - Complete Framework & Implementation Plan

## Current State Analysis

### 🔴 **CRITICAL ISSUES FOUND**

#### 1. **Two Disconnected Systems**
- **StrategySettings.tsx**: 28 strategies, **NO backend integration**, simulated saves only
- **AlertPreferences.tsx**: 28 systems (ADVANCED_SYSTEMS), **HAS backend integration**, saves to SQLite

#### 2. **Backend Alert System**
✅ **Working Components:**
- `system_alert_preferences.py` - SQLite storage for user preferences
- `alert_monitor.py` - Detects arbitrage, steam moves, middles (FIXED: datetime serialization)
- `useAlertMonitoring.ts` - Monitors live games for projection-based alerts
- Toast notifications for arbitrage and middles (JUST ADDED)

❌ **Missing Components:**
- No detection logic for 25+ other strategies
- No monitoring services for pre-game strategies
- No connection between strategy settings and actual alert triggers

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYERS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │ StrategySettings │◄─────X─│  NO BACKEND CONNECTION  │  │
│  │  (28 strategies) │        │   (LOCAL STATE ONLY)    │  │
│  └──────────────────┘        └─────────────────────────┘  │
│                                                             │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │AlertPreferences  │◄───✓───│   Backend Connected     │  │
│  │(ADVANCED_SYSTEMS)│        │ /api/alert-preferences  │  │
│  └──────────────────┘        └─────────────────────────┘  │
│                                                             │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │ Alerts.tsx       │◄───✓───│ Fetches /api/alerts/all │  │
│  │ (Toast Notifs)   │        │   Every 10 seconds      │  │
│  └──────────────────┘        └─────────────────────────┘  │
│                                                             │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │useAlertMonitoring│◄───✓───│ Monitors live game data │  │
│  │  (Live Games)    │        │  Checks enabled systems │  │
│  └──────────────────┘        └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BACKEND LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │ alert_monitor.py │◄───✓───│  Scans every 10 sec     │  │
│  │  (Arbitrage,     │        │  Detects: Arb, Steam,   │  │
│  │   Steam, Middles)│        │  Middles                │  │
│  └──────────────────┘        └─────────────────────────┘  │
│                                                             │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │system_alert_prefs│◄───✓───│ SQLite: user_settings.db│  │
│  │  (User Settings) │        │ Stores enabled systems  │  │
│  └──────────────────┘        └─────────────────────────┘  │
│                                                             │
│  ┌──────────────────┐        ┌─────────────────────────┐  │
│  │ Strategy Monitors│◄───X───│  MISSING! No monitors   │  │
│  │ (25+ strategies) │        │  for most strategies    │  │
│  └──────────────────┘        └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Strategy Inventory & Implementation Status

### **LIVE STRATEGIES** (6 strategies)

| ID | Strategy | Status | Detection | Alerts |
|----|----------|--------|-----------|--------|
| 1 | Max EV Boost (NBA) | ✅ LIVE | ✅ XGBoost analyzer | ✅ useAlertMonitoring |
| 2 | Max EV Boost (NCAAB) | ✅ LIVE | ✅ XGBoost analyzer | ✅ useAlertMonitoring |
| 6 | Goalie Pull Alert | ✅ PROVEN | ✅ ML model | ✅ Toast on Alerts page |
| 14 | Quarter Reversal | ⚠️ ACTIVE | ✅ API endpoint | ✅ useAlertMonitoring |
| 23 | Halftime Tracker | ⚠️ ACTIVE | ✅ API endpoint | ✅ useAlertMonitoring |
| 24 | Momentum Detector | ⚠️ ACTIVE | ⚠️ Projection data | ✅ useAlertMonitoring |

### **PRE-GAME STRATEGIES** (22 strategies)

| Category | Count | Detection Status | Alert Status |
|----------|-------|------------------|--------------|
| Line Movement | 4 | ❌ Not implemented | ❌ No alerts |
| Schedule/Fatigue | 3 | ❌ Not implemented | ❌ No alerts |
| Public Betting | 2 | ❌ Not implemented | ❌ No alerts |
| Sharp Money | 2 | ❌ Not implemented | ❌ No alerts |
| Weather | 2 | ❌ Not implemented | ❌ No alerts |
| Matchup Analysis | 5 | ❌ Not implemented | ❌ No alerts |
| Situational | 4 | ❌ Not implemented | ❌ No alerts |

### **CURRENTLY WORKING ALERTS**

✅ **Arbitrage** - Detected every 10s, toast notifications ✓
✅ **Middles** - Detected every 10s, toast notifications ✓
✅ **Live Game Projections** - Monitors enabled systems, checks strength thresholds

---

## Complete Implementation Framework

### **PHASE 1: Unify Strategy Management** (Priority: CRITICAL)

#### 1.1 Create Unified Strategy Registry
```typescript
// frontend/src/data/unifiedStrategies.ts
export interface UnifiedStrategy {
  id: string;              // Unique identifier
  systemId: number;        // Maps to ADVANCED_SYSTEMS
  name: string;
  category: 'pregame' | 'live';
  sports: string[];
  description: string;
  sampleSize: string;
  edge: string;
  winRate: string;
  defaultEnabled: boolean;

  // Detection configuration
  detectionType: 'live_monitor' | 'pregame_scanner' | 'api_endpoint';
  detectionEndpoint?: string;  // If using API
  monitorInterval?: number;     // Seconds between checks

  // Alert configuration
  minStrengthThreshold: number;
  notificationMethod: 'toast' | 'modal' | 'both';
  soundEffect?: string;
}
```

#### 1.2 Connect StrategySettings to Backend
**Replace simulated saves with real API calls:**
```typescript
// StrategySettings.tsx line 386-401
const toggleStrategy = async (strategyId: string) => {
  setSaving(true);
  try {
    const strategy = UNIFIED_STRATEGIES.find(s => s.id === strategyId);
    if (!strategy) return;

    // REAL API CALL - not setTimeout!
    await toggleSystemAlerts(username, strategy.systemId);

    setEnabledStrategies(prev => {
      const newSet = new Set(prev);
      if (newSet.has(strategyId)) newSet.delete(strategyId);
      else newSet.add(strategyId);
      return newSet;
    });

    showToast(`Alerts ${isEnabled ? 'disabled' : 'enabled'} for ${strategy.name}`, 'success');
  } catch (error) {
    showToast('Failed to update strategy settings', 'error');
  } finally {
    setSaving(false);
  }
};
```

---

### **PHASE 2: Implement Pre-Game Strategy Monitors** (Priority: HIGH)

#### 2.1 Steam Move Monitor (Already exists in alert_monitor.py)
✅ **Status**: Working
✅ **Endpoint**: Included in /api/alerts/all
⚠️ **Issue**: No toast notifications yet

**Add toast notifications:**
```typescript
// Alerts.tsx - Add steam move alerts
useEffect(() => {
  const currentCount = alertsData?.steam_moves.count || 0;
  if (currentCount > previousCountRef.current.steam && previousCountRef.current.steam >= 0) {
    playArbitrageSound();
    showToast(
      `⚡ ${currentCount - previousCountRef.current.steam} NEW STEAM MOVE${currentCount > 1 ? 'S' : ''} - Sharp Money Alert!`,
      'warning'
    );
  }
  previousCountRef.current.steam = currentCount;
}, [alertsData?.steam_moves.count]);
```

#### 2.2 Sharp Money Tracker
**Backend: `/backend/strategies/sharp_money_tracker.py`**
```python
class SharpMoneyTracker:
    """
    Detects sharp money by monitoring:
    - Line moves AGAINST public betting percentages
    - Sudden line movements without injury news
    - Reverse line movement (RLM)
    """

    def detect_sharp_action(self, game_odds: Dict) -> List[SharpMoneyAlert]:
        """
        Returns alerts when:
        1. Line moves 0.5+ points
        2. Move is opposite public betting direction
        3. No obvious injury/news catalyst
        """
        pass

    async def monitor_loop(self):
        """Run every 60 seconds"""
        while True:
            alerts = await self.scan_all_games()
            # Store alerts via alert_storage
            await asyncio.sleep(60)
```

**Frontend: Add to useAlertMonitoring hook**

#### 2.3 Schedule Fatigue Monitor
**Backend: `/backend/strategies/schedule_fatigue_monitor.py`**
```python
class ScheduleFatigueMonitor:
    """
    Scans upcoming games for:
    - Back-to-back situations (B2B)
    - 3-in-4 nights (NBA/NHL)
    - Rest differentials (3+ days vs 0 days)
    - Travel distance
    """

    def scan_upcoming_games(self) -> List[FatigueAlert]:
        """
        Generates alerts 2 hours before game starts
        Returns alerts when:
        - B2B team faces rested opponent (3+ days)
        - 3-in-4 nights situation
        - Cross-country travel on B2B
        """
        pass

    async def monitor_loop(self):
        """Run every 30 minutes"""
        while True:
            alerts = await self.scan_schedule()
            await asyncio.sleep(1800)  # 30 min
```

#### 2.4 Weather Monitor
**Backend: `/backend/strategies/weather_monitor.py`**
```python
class WeatherMonitor:
    """
    Monitors weather for outdoor games:
    - NFL
    - MLB
    """

    def check_game_weather(self, game: Dict) -> Optional[WeatherAlert]:
        """
        Returns alerts when:
        - Wind > 15 MPH
        - Precipitation during game time
        - Temperature < 32°F or > 85°F
        - Sudden weather change from opening line
        """
        pass

    async def monitor_loop(self):
        """Run every 15 minutes for games starting in next 3 hours"""
        while True:
            alerts = await self.scan_weather()
            await asyncio.sleep(900)  # 15 min
```

---

### **PHASE 3: Create Master Alert Orchestrator** (Priority: HIGH)

#### 3.1 Backend: Alert Orchestrator Service
**Backend: `/backend/services/alert_orchestrator.py`**
```python
class AlertOrchestrator:
    """
    Central service that coordinates all alert monitors
    Manages timing, priorities, and user preferences
    """

    def __init__(self):
        self.monitors = {
            'arbitrage': alert_monitor,
            'steam_moves': alert_monitor,
            'middles': alert_monitor,
            'sharp_money': SharpMoneyTracker(),
            'schedule_fatigue': ScheduleFatigueMonitor(),
            'weather': WeatherMonitor(),
            # Add more monitors...
        }

    async def start_all_monitors(self):
        """Start all monitoring services in parallel"""
        tasks = [
            self.monitors['arbitrage'].start_monitoring(['basketball_nba', 'americanfootball_nfl', 'icehockey_nhl']),
            self.monitors['sharp_money'].monitor_loop(),
            self.monitors['schedule_fatigue'].monitor_loop(),
            self.monitors['weather'].monitor_loop(),
        ]
        await asyncio.gather(*tasks)

    def get_user_relevant_alerts(self, user_id: str) -> Dict:
        """
        Filter all alerts by user's enabled systems
        Returns only alerts user cares about
        """
        enabled_systems = system_alert_prefs.get_enabled_systems(user_id)
        # Filter alerts by system ID...
        pass
```

#### 3.2 Frontend: Unified Alert Display
**Frontend: Create `AlertManager` component**
```typescript
// frontend/src/components/AlertManager.tsx
export function AlertManager() {
  const { username } = useAuth();
  const { showToast } = useToast();
  const [lastAlertCheck, setLastAlertCheck] = useState<number>(Date.now());

  useEffect(() => {
    const checkForAlerts = async () => {
      // Fetch all alerts from all sources
      const [
        liveAlerts,      // Arbitrage, steam, middles
        scheduleAlerts,  // Fatigue, B2B
        weatherAlerts,   // Weather impacts
        projectionAlerts // Live game projections
      ] = await Promise.all([
        fetch('/api/alerts/all'),
        fetch('/api/alerts/schedule-fatigue'),
        fetch('/api/alerts/weather'),
        fetch('/api/alerts/live-projections')
      ]);

      // Show new alerts as toasts
      const newAlerts = filterNewAlerts(allAlerts, lastAlertCheck);
      newAlerts.forEach(alert => showAlertToast(alert));
    };

    const interval = setInterval(checkForAlerts, 10000); // 10s
    return () => clearInterval(interval);
  }, [username]);
}
```

---

### **PHASE 4: Strategy-Specific Detection Implementation**

#### 4.1 Priority Strategies (Implement First)

**LIVE STRATEGIES:**
1. ✅ Max EV Boost (NBA/NCAAB) - Already working
2. ✅ Quarter Reversal - Already working
3. ⚠️ Momentum Detector - Needs enhancement
4. ⚠️ Halftime Tracker - Needs enhancement
5. ❌ Favorite Comeback - Needs implementation

**PRE-GAME STRATEGIES:**
1. ✅ Arbitrage - Working!
2. ✅ Middles - Working!
3. ⚠️ Steam Moves - Working but no toast
4. ❌ Sharp Money Tracking - Needs implementation
5. ❌ Schedule Fatigue (B2B) - Needs implementation

#### 4.2 Implementation Template

For each strategy, create:
```python
# backend/strategies/{strategy_name}_monitor.py

class {Strategy}Monitor:
    """
    Detection logic for {Strategy Name}
    """

    def __init__(self):
        self.alert_storage = alert_storage
        self.system_id = {SYSTEM_ID}

    def detect_opportunities(self, games: List[Dict]) -> List[Alert]:
        """Core detection logic"""
        alerts = []
        for game in games:
            if self.meets_criteria(game):
                alert = self.create_alert(game)
                # Store alert
                self.alert_storage.create_alert(
                    alert_type='{strategy_name}',
                    game_id=game['id'],
                    sport=game['sport'],
                    # ... other fields
                )
                alerts.append(alert)
        return alerts

    async def monitor_loop(self, interval_seconds: int = 60):
        """Continuous monitoring"""
        while True:
            alerts = await self.scan_for_opportunities()
            logger.info(f"Scan complete: {len(alerts)} {strategy_name} alerts")
            await asyncio.sleep(interval_seconds)
```

---

### **PHASE 5: User Experience Enhancements**

#### 5.1 Alert Notification Center
**Create centralized notification hub:**
```typescript
// frontend/src/components/NotificationCenter.tsx
export function NotificationCenter() {
  return (
    <div className="fixed top-20 right-4 z-50 w-80">
      {/* Show last 5 alerts */}
      {recentAlerts.map(alert => (
        <AlertCard
          key={alert.id}
          title={alert.strategyName}
          message={alert.description}
          onClick={() => navigate('/alerts')}
        />
      ))}
    </div>
  );
}
```

#### 5.2 Alert History & Performance
**Track alert performance:**
```typescript
// Show user how alerts performed
interface AlertPerformance {
  strategyName: string;
  alertsGenerated: number;
  alertsActedOn: number;
  wins: number;
  losses: number;
  roi: number;
}
```

#### 5.3 Smart Alert Filtering
```typescript
// Only show alerts that meet user's criteria:
- Minimum edge threshold
- Specific sports
- Specific bookmakers
- Time of day preferences
```

---

## Implementation Timeline

### **Week 1: Foundation** (Critical)
- [ ] Connect StrategySettings to backend API
- [ ] Add steam move toast notifications
- [ ] Create unified strategy registry
- [ ] Test end-to-end alert flow

### **Week 2: Pre-Game Monitors** (High Priority)
- [ ] Implement Sharp Money Tracker
- [ ] Implement Schedule Fatigue Monitor
- [ ] Implement Weather Monitor
- [ ] Add toast notifications for all

### **Week 3: Alert Orchestrator** (High Priority)
- [ ] Create AlertOrchestrator service
- [ ] Implement user preference filtering
- [ ] Create unified /api/alerts/comprehensive endpoint
- [ ] Add alert history tracking

### **Week 4: Remaining Strategies** (Medium Priority)
- [ ] Implement 15+ remaining pre-game strategies
- [ ] Add detection logic for each
- [ ] Connect to alert system
- [ ] Test with real games

### **Week 5: UX Polish** (Medium Priority)
- [ ] Notification center
- [ ] Alert history page
- [ ] Performance tracking
- [ ] Smart filtering

---

## Testing Checklist

### **Per Strategy:**
- [ ] Detection logic triggers correctly
- [ ] Alert stored in database
- [ ] User preference checked
- [ ] Toast notification appears
- [ ] Sound effect plays
- [ ] Alert data accurate
- [ ] No false positives

### **System-Wide:**
- [ ] All monitors running simultaneously
- [ ] No performance degradation
- [ ] Database handles load
- [ ] Frontend stays responsive
- [ ] Cloudflare caching doesn't break polling

---

## Success Metrics

### **Technical Metrics:**
- All 28 strategies have working detection logic
- Alerts trigger within 10 seconds of detection
- 95%+ uptime for monitoring services
- Zero false positives

### **User Metrics:**
- Users enable 5+ strategies on average
- Alert click-through rate > 40%
- Alert-to-bet conversion > 20%
- User satisfaction score > 8/10

---

## Current Priority Actions

### **RIGHT NOW** (Do These First):
1. ✅ Fix datetime serialization (DONE!)
2. ✅ Add arbitrage/middle toast notifications (DONE!)
3. ⚠️ Add steam move toast notifications (NEXT)
4. ❌ Connect StrategySettings to backend API

### **THIS WEEK:**
1. Implement Sharp Money Tracker
2. Implement Schedule Fatigue Monitor
3. Create AlertOrchestrator service
4. Test end-to-end with real games

---

## File Locations Reference

### **Frontend:**
- `frontend/src/pages/StrategySettings.tsx` - Strategy toggle page (needs backend connection)
- `frontend/src/pages/AlertPreferences.tsx` - Alert preferences (working)
- `frontend/src/pages/Alerts.tsx` - Alert display with toast notifications
- `frontend/src/hooks/useAlertMonitoring.ts` - Live game monitoring hook
- `frontend/src/data/advancedSystems.ts` - System definitions

### **Backend:**
- `backend/alert_monitor.py` - Arbitrage/steam/middle detection (working)
- `backend/storage/system_alert_preferences.py` - User preferences storage
- `backend/storage/alert_storage.py` - Alert storage
- `backend/routes/alert_preferences.py` - Preference API routes
- `backend/strategies/` - Strategy detection modules (many missing)

---

## Questions for User

1. **Priority**: Should we focus on fixing StrategySettings first, or implementing more strategy monitors?
2. **Scope**: Which 5 strategies should we prioritize after steam moves?
3. **Notification**: Do you want push notifications, or just in-app toasts?
4. **Performance**: Is 10-second polling acceptable, or should we use WebSockets?
5. **Mobile**: Do you need mobile app support for alerts?
