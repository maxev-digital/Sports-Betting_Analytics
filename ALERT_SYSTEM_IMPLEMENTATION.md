# Real-Time Alert System Implementation Guide

## Overview

This document outlines the implementation of a premium real-time alert system that monitors betting markets 24/7 and notifies users of opportunities:

- **Arbitrage Opportunities** - Guaranteed profit across books
- **Steam Moves** - When sharp money hits the market
- **Line Movements** - Significant line changes
- **CLV Opportunities** - Lines significantly different from consensus

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   The Odds API                           │
│          (Pulls odds every 60 seconds)                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              Alert Monitor Service                       │
│  - Detects arbitrage (0.5%+ profit)                     │
│  - Detects steam moves (70%+ books moving together)     │
│  - Detects line movements (1.5+ point changes)          │
│  - Tracks line history for each game                    │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│                 FastAPI Backend                          │
│  Endpoints:                                              │
│  - GET /api/alerts/arbitrage                            │
│  - GET /api/alerts/steam-moves                          │
│  - GET /api/alerts/line-movements                       │
│  - GET /api/alerts/all                                  │
│  - WebSocket /ws/alerts (real-time push)                │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              React Frontend                              │
│  - Real-time alert dashboard                             │
│  - Push notifications                                    │
│  - Alert history                                         │
│  - User preferences (sports, minimum profit, etc.)      │
└─────────────────────────────────────────────────────────┘
```

## Implementation Steps

### Step 1: Backend Alert Endpoints (Already Created)

File: `backend/alert_monitor.py`

**Key Components:**
- `AlertMonitor` class - Core monitoring logic
- `detect_arbitrage()` - Finds guaranteed profit opportunities
- `detect_steam_move()` - Detects synchronized line movements
- `detect_line_movement()` - Tracks significant changes
- `scan_for_alerts()` - Main scanning function

### Step 2: Add Endpoints to FastAPI

Add to `backend/main.py`:

```python
from alert_monitor import AlertMonitor
import os

# Initialize alert monitor
alert_monitor = AlertMonitor(
    odds_api_key=os.getenv('ODDS_API_KEY')
)

@app.on_event("startup")
async def startup():
    """Start game tracking and alert monitoring on app startup"""
    logger.info("Starting NBA Live Betting API...")
    asyncio.create_task(tracker.start())

    # Start alert monitoring for NBA, NFL, NHL
    asyncio.create_task(
        alert_monitor.start_monitoring(
            sports=['basketball_nba', 'americanfootball_nfl', 'icehockey_nhl'],
            interval_seconds=60  # Check every 60 seconds
        )
    )

@app.get("/api/alerts/arbitrage")
async def get_arbitrage_alerts():
    """Get current arbitrage opportunities"""
    alerts = alert_monitor.active_alerts.get('arbitrage', [])
    return [
        {
            'game_id': alert.game_id,
            'sport': alert.sport,
            'home_team': alert.home_team,
            'away_team': alert.away_team,
            'market_type': alert.market_type,
            'book_a': alert.book_a,
            'book_b': alert.book_b,
            'odds_a': alert.odds_a,
            'odds_b': alert.odds_b,
            'profit_percent': alert.profit_percent,
            'stake_a': alert.stake_a,
            'stake_b': alert.stake_b,
            'guaranteed_profit': alert.guaranteed_profit,
            'expires_in': alert.expires_in,
            'timestamp': alert.timestamp.isoformat()
        }
        for alert in alerts
    ]

@app.get("/api/alerts/steam-moves")
async def get_steam_move_alerts():
    """Get detected steam moves"""
    alerts = alert_monitor.active_alerts.get('steam_moves', [])
    return [
        {
            'game_id': alert.game_id,
            'sport': alert.sport,
            'home_team': alert.home_team,
            'away_team': alert.away_team,
            'market_type': alert.market_type,
            'side': alert.side,
            'original_line': alert.original_line,
            'new_line': alert.new_line,
            'movement': alert.movement,
            'books_moved': alert.books_moved,
            'consensus_percent': alert.consensus_percent,
            'timestamp': alert.timestamp.isoformat()
        }
        for alert in alerts
    ]

@app.get("/api/alerts/line-movements")
async def get_line_movement_alerts():
    """Get significant line movements"""
    alerts = alert_monitor.active_alerts.get('line_movements', [])
    return [
        {
            'game_id': alert.game_id,
            'sport': alert.sport,
            'home_team': alert.home_team,
            'away_team': alert.away_team,
            'market_type': alert.market_type,
            'bookmaker': alert.bookmaker,
            'original_line': alert.original_line,
            'new_line': alert.new_line,
            'movement': alert.movement,
            'movement_percent': alert.movement_percent,
            'timestamp': alert.timestamp.isoformat()
        }
        for alert in alerts
    ]

@app.get("/api/alerts/all")
async def get_all_alerts():
    """Get all active alerts"""
    return {
        'arbitrage': await get_arbitrage_alerts(),
        'steam_moves': await get_steam_move_alerts(),
        'line_movements': await get_line_movement_alerts(),
        'last_updated': alert_monitor.active_alerts.get('timestamp', datetime.now()).isoformat()
    }
```

### Step 3: WebSocket for Real-Time Alerts

Add to `backend/main.py`:

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set

# Active WebSocket connections
active_connections: Set[WebSocket] = set()

@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """WebSocket endpoint for real-time alerts"""
    await websocket.accept()
    active_connections.add(websocket)

    try:
        while True:
            # Send alerts every time they update
            alerts = {
                'arbitrage': await get_arbitrage_alerts(),
                'steam_moves': await get_steam_move_alerts(),
                'line_movements': await get_line_movement_alerts(),
                'timestamp': datetime.now().isoformat()
            }

            await websocket.send_json(alerts)

            # Wait 5 seconds before next update
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        active_connections.remove(websocket)
```

### Step 4: Frontend Alert Component

Create `frontend/src/components/AlertsDashboard.tsx`:

```typescript
import { useState, useEffect } from 'react';

interface ArbitrageAlert {
  game_id: string;
  sport: string;
  home_team: string;
  away_team: string;
  market_type: string;
  book_a: string;
  book_b: string;
  odds_a: number;
  odds_b: number;
  profit_percent: number;
  stake_a: number;
  stake_b: number;
  guaranteed_profit: number;
  expires_in: number;
  timestamp: string;
}

interface SteamMoveAlert {
  game_id: string;
  sport: string;
  home_team: string;
  away_team: string;
  market_type: string;
  side: string;
  original_line: number;
  new_line: number;
  movement: number;
  books_moved: string[];
  consensus_percent: number;
  timestamp: string;
}

interface LineMovementAlert {
  game_id: string;
  sport: string;
  home_team: string;
  away_team: string;
  market_type: string;
  bookmaker: string;
  original_line: number;
  new_line: number;
  movement: number;
  movement_percent: number;
  timestamp: string;
}

export function AlertsDashboard() {
  const [arbitrageAlerts, setArbitrageAlerts] = useState<ArbitrageAlert[]>([]);
  const [steamMoveAlerts, setSteamMoveAlerts] = useState<SteamMoveAlert[]>([]);
  const [lineMovementAlerts, setLineMovementAlerts] = useState<LineMovementAlert[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket for real-time updates
    const ws = new WebSocket('ws://localhost:8000/ws/alerts');

    ws.onopen = () => {
      console.log('Connected to alerts WebSocket');
      setConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setArbitrageAlerts(data.arbitrage || []);
      setSteamMoveAlerts(data.steam_moves || []);
      setLineMovementAlerts(data.line_movements || []);

      // Show browser notification for new arbitrage
      if (data.arbitrage && data.arbitrage.length > 0) {
        new Notification('Arbitrage Opportunity!', {
          body: `${data.arbitrage[0].home_team} vs ${data.arbitrage[0].away_team} - ${data.arbitrage[0].profit_percent.toFixed(2)}% profit`,
          icon: '/alert-icon.png'
        });
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnected(false);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnected(false);
    };

    // Request notification permission
    if (Notification.permission === 'default') {
      Notification.requestPermission();
    }

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="space-y-6">
      {/* Connection Status */}
      <div className={`flex items-center gap-2 text-sm ${connected ? 'text-green-400' : 'text-red-400'}`}>
        <span className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></span>
        {connected ? 'Live Monitoring Active' : 'Disconnected'}
      </div>

      {/* Arbitrage Alerts */}
      {arbitrageAlerts.length > 0 && (
        <div className="bg-green-900/30 border border-green-500 rounded-lg p-4">
          <h3 className="text-xl font-bold text-green-400 mb-4">
            🎯 Arbitrage Opportunities ({arbitrageAlerts.length})
          </h3>
          <div className="space-y-3">
            {arbitrageAlerts.map((alert, index) => (
              <div key={index} className="bg-slate-800 rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="text-white font-bold">{alert.home_team} vs {alert.away_team}</h4>
                    <p className="text-sm text-slate-400">{alert.market_type}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-green-400">
                      {alert.profit_percent.toFixed(2)}%
                    </div>
                    <div className="text-sm text-slate-400">
                      ${alert.guaranteed_profit.toFixed(2)} profit
                    </div>
                  </div>
                </div>
                <div className="mt-3 grid grid-cols-2 gap-3">
                  <div className="text-sm">
                    <span className="text-slate-400">{alert.book_a}:</span>
                    <span className="text-white font-bold ml-2">{alert.odds_a}</span>
                    <span className="text-green-400 block">${alert.stake_a.toFixed(2)}</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-slate-400">{alert.book_b}:</span>
                    <span className="text-white font-bold ml-2">{alert.odds_b}</span>
                    <span className="text-green-400 block">${alert.stake_b.toFixed(2)}</span>
                  </div>
                </div>
                <div className="mt-2 text-xs text-slate-400">
                  Expires in {Math.floor(alert.expires_in / 60)} minutes
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Steam Move Alerts */}
      {steamMoveAlerts.length > 0 && (
        <div className="bg-red-900/30 border border-red-500 rounded-lg p-4">
          <h3 className="text-xl font-bold text-red-400 mb-4">
            🔥 Steam Moves ({steamMoveAlerts.length})
          </h3>
          <div className="space-y-3">
            {steamMoveAlerts.map((alert, index) => (
              <div key={index} className="bg-slate-800 rounded-lg p-4">
                <div className="flex justify-between">
                  <div>
                    <h4 className="text-white font-bold">{alert.home_team} vs {alert.away_team}</h4>
                    <p className="text-sm text-slate-400">{alert.market_type} - {alert.side}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-red-400">
                      {alert.consensus_percent.toFixed(0)}% Consensus
                    </div>
                    <div className="text-sm text-slate-400">
                      {alert.books_moved.length} books moved
                    </div>
                  </div>
                </div>
                <div className="mt-2 text-sm">
                  <span className="text-slate-400">Line:</span>
                  <span className="text-white ml-2">{alert.original_line} → {alert.new_line}</span>
                  <span className={`ml-2 font-bold ${alert.movement > 0 ? 'text-green-400' : 'text-red-400'}`}>
                    ({alert.movement > 0 ? '+' : ''}{alert.movement.toFixed(1)})
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Line Movement Alerts */}
      {lineMovementAlerts.length > 0 && (
        <div className="bg-blue-900/30 border border-blue-500 rounded-lg p-4">
          <h3 className="text-xl font-bold text-blue-400 mb-4">
            📈 Line Movements ({lineMovementAlerts.length})
          </h3>
          <div className="space-y-2">
            {lineMovementAlerts.map((alert, index) => (
              <div key={index} className="bg-slate-800 rounded-lg p-3 text-sm">
                <div className="flex justify-between">
                  <div>
                    <span className="text-white font-bold">{alert.home_team} vs {alert.away_team}</span>
                    <span className="text-slate-400 ml-2">@ {alert.bookmaker}</span>
                  </div>
                  <div>
                    <span className="text-white">{alert.original_line} → {alert.new_line}</span>
                    <span className={`ml-2 font-bold ${alert.movement > 0 ? 'text-green-400' : 'text-red-400'}`}>
                      ({alert.movement > 0 ? '+' : ''}{alert.movement.toFixed(1)})
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Alerts */}
      {arbitrageAlerts.length === 0 && steamMoveAlerts.length === 0 && lineMovementAlerts.length === 0 && (
        <div className="text-center py-12">
          <div className="text-4xl mb-4">👀</div>
          <h3 className="text-xl font-bold text-white mb-2">Monitoring Markets</h3>
          <p className="text-slate-400">
            We'll alert you when opportunities arise
          </p>
        </div>
      )}
    </div>
  );
}
```

## Features

### 1. **Arbitrage Detection**
- Monitors all markets (spreads, totals, moneylines)
- Detects opportunities with 0.5%+ profit
- Calculates optimal stake distribution
- Shows time until game starts

### 2. **Steam Move Detection**
- Tracks line movements across all books
- Detects when 70%+ of books move together
- Indicates sharp money direction
- Lists which books have moved

### 3. **Line Movement Tracking**
- Alerts on 1.5+ point movements
- Tracks individual book changes
- Shows movement percentage
- Helps identify value before lines adjust

### 4. **Real-Time Updates**
- WebSocket connection for live data
- Browser push notifications
- Auto-refresh every 5 seconds
- Connection status indicator

## Configuration

### Alert Thresholds (in `alert_monitor.py`):

```python
self.arbitrage_min_profit = 0.5  # 0.5% minimum profit
self.steam_move_threshold = 0.7  # 70% of books moving same direction
self.line_movement_threshold = 1.5  # 1.5 point movement
```

### Monitoring Interval:

```python
# In main.py startup
interval_seconds=60  # Check odds every 60 seconds
```

### Sports to Monitor:

```python
sports=['basketball_nba', 'americanfootball_nfl', 'icehockey_nhl']
```

## Monetization

### Premium Feature Pricing:

- **Free Tier**: Manual calculators only
- **Pro Tier ($29/month)**: Real-time alerts, 60-second refresh
- **Elite Tier ($99/month)**: Real-time alerts, 30-second refresh, SMS/Email notifications

### Implementation:

Add user subscription check to endpoints:

```python
from fastapi import Depends, HTTPException

async def verify_subscription(user_id: str):
    # Check user's subscription level
    # Return subscription tier
    pass

@app.get("/api/alerts/arbitrage")
async def get_arbitrage_alerts(subscription = Depends(verify_subscription)):
    if subscription not in ['pro', 'elite']:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    # ... rest of endpoint
```

## API Cost Management

The Odds API charges per request. With monitoring:

- **3 sports** × **1 request/60 seconds** = **4,320 requests/day**
- At 500 free requests/month, you'll need a paid plan
- **$49/month plan**: 25,000 requests (enough for 3 sports at 60-second intervals)
- **Pass cost to users**: $29/month subscription covers API costs

## Next Steps

1. ✅ Create `alert_monitor.py` (DONE)
2. Add endpoints to `main.py`
3. Create `AlertsDashboard.tsx` frontend component
4. Add WebSocket support
5. Implement user subscription system
6. Add email/SMS notification options
7. Create alert history and analytics
8. Add user preferences (min profit %, sports, etc.)

This system will provide massive value to serious bettors and justify premium pricing!
