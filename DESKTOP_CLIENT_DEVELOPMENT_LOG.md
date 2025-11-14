# MAX EV Sports Desktop Client - Development Log
**Project:** Electron Desktop Application for MAX EV Sports
**Repository:** C:\Users\nashr\frontend\electron\
**Last Updated:** November 5, 2025

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Features Implemented](#features-implemented)
4. [File Structure](#file-structure)
5. [Development Sessions](#development-sessions)
6. [Quick Reference](#quick-reference)

---

## Project Overview

### Purpose
Desktop application that provides:
- Full MAX EV Sports platform access
- Multi-window support for different sections
- Always-on-top alerts widget
- System tray integration
- Native desktop notifications
- Better performance than web version

### Technology Stack
- **Framework:** Electron 27.x
- **Frontend:** React + Vite
- **Backend API:** https://max-ev-sports.com/api
- **Build Tool:** electron-builder
- **Dev Server:** Vite dev server (port 5173)

---

## Architecture

### Multi-Window System
The app supports multiple independent windows, each with its own route:

| Route | Title | Size | Purpose |
|-------|-------|------|---------|
| `live-games` | Live Games | 1400×900 | Main dashboard (default) |
| `alerts` | Alerts | 1200×800 | All betting alerts |
| `analytics` | Analytics | 1400×900 | Performance tracking |
| `props` | Props | 1300×850 | Player props opportunities |
| `tools` | Tools | 1200×800 | Betting calculators |
| `odds` | Odds | 1400×900 | Odds comparison |
| `settings` | Settings | 1000×700 | App configuration |
| `widget` | Alerts Widget | 450×1000 | **Always-on-top compact alerts** |

### Process Architecture
```
Main Process (main.js)
├── Window Management
│   ├── BrowserWindow creation
│   ├── Route handling
│   └── IPC handlers
├── System Tray
│   ├── Context menu
│   └── Window launchers
└── App Menu
    └── Multi-window options

Renderer Process (React App)
├── Vite Dev Server (development)
└── Built HTML (production)

Widget Process (popup-desktop.html)
├── Direct HTML file load
├── API fetching
└── LocalStorage settings
```

---

## Features Implemented

### 1. Multi-Window Support
**Implementation:** frontend/electron/main.js (lines 16-25)

**Features:**
- Create multiple windows simultaneously
- Each window tracks independently
- Prevent duplicate windows for same route
- Focus existing window if already open

**Access:**
- File menu → New Window → [route]
- System tray → [route]
- IPC handler: `open-window`

### 2. System Tray Integration
**Implementation:** frontend/electron/main.js (lines 112-191)

**Features:**
- Persistent tray icon (stays when windows closed)
- Context menu with all routes
- Show/Hide all windows
- Double-click opens main window
- Custom tooltip: "MAX EV SPORTS - Desktop"

**Icon:** frontend/public/logo2.png

### 3. Window Arrangement Tools
**Implementation:** frontend/electron/main.js (lines 289-339)

**Features:**
- **Tile Horizontally:** Stack windows vertically
- **Tile Vertically:** Place windows side-by-side
- **Cascade:** Offset windows diagonally

**Access:** Window menu → Arrange Windows

### 4. Always-On-Top Alerts Widget ⭐ NEW
**Implementation:**
- frontend/electron/main.js (widget configuration)
- frontend/public/extension-widget/popup-desktop.html
- frontend/public/extension-widget/popup-desktop.js

**Features:**
- Extension popup UI in desktop window
- Stays above all other apps
- Auto-refreshes every 10 seconds
- Resizable (300-600px wide, unlimited height)
- Shows all strategy alerts:
  - Arbitrage opportunities
  - Steam moves
  - Middles
  - Goalie pulls
  - Quarter reversals
  - Injury props
- Sound notifications (Web Audio API)
- Voice announcements (Speech Synthesis API)
- LocalStorage settings persistence

**Access:**
- System tray → 📲 Alerts Widget (Always On Top)
- File menu → New Window → Alerts Widget

**API Endpoint:** `https://max-ev-sports.com/api/alerts/all?user_id=default`

**Data Structure:**
```javascript
{
  arbitrage: { count: number, alerts: array },
  steam_moves: { count: number, alerts: array },
  middles: { count: number, alerts: array },
  goalie_pulls: { count: number, alerts: array },
  quarter_reversals: { count: number, alerts: array },
  injury_props: { count: number, alerts: array },
  last_updated: string
}
```

### 5. Development Features
- Hot reload for renderer process (Ctrl+R)
- DevTools access (F12, View menu)
- Console logging for debugging
- Demo mode for analytics screenshots

### 6. Security Features
- Context isolation enabled
- Node integration disabled
- Remote module disabled
- Preload script sandboxing

---

## File Structure

```
frontend/
├── electron/
│   ├── main.js                    # Main Electron process ⭐
│   ├── preload.js                 # Preload script
│   ├── electron-start.js          # Startup script
│   └── debug-electron.js          # Debug launcher
│
├── public/
│   ├── logo2.png                  # App icon
│   └── extension-widget/          # Widget files ⭐ NEW
│       ├── popup-desktop.html     # Widget UI
│       ├── popup-desktop.js       # Widget logic
│       ├── popup.css              # Widget styles
│       ├── popup.html             # Browser extension version
│       ├── popup.js               # Browser extension logic
│       ├── url_builder.js         # Bookmaker URL builder
│       └── logo.png               # Widget icon
│
├── src/
│   ├── components/
│   │   └── GameCard.tsx           # Game card with latency ⭐
│   ├── pages/
│   │   ├── Alerts.tsx             # Alerts page
│   │   ├── Analytics.tsx          # Analytics page
│   │   └── ...
│   ├── config.ts                  # API configuration
│   └── types.ts                   # TypeScript types
│
├── package.json
├── vite.config.ts
├── electron-builder.json5
└── README.md
```

---

## Development Sessions

### Session 1: November 4, 2025
**Focus:** Initial multi-window setup

**Completed:**
- Basic Electron configuration
- Multi-window architecture
- System tray integration
- Window arrangement tools
- IPC handlers

### Session 2: November 5, 2025
**Focus:** Widget and latency features

**Completed:**
1. **Latency Display** (GameCard.tsx)
   - Added color-coded latency display
   - Red (< 1s), Yellow (1-3s), Green (> 3s)
   - Shows seconds format next to bookmaker

2. **Desktop Extension Widget**
   - Created popup-desktop.html/js
   - Replaced Chrome APIs with web APIs
   - Fixed API endpoint integration
   - Made widget resizable (450×1000 default)
   - Added sound/voice controls
   - Implemented auto-refresh (10s interval)

**Bugs Fixed:**
- API endpoint 404 errors → Fixed to use `/api/alerts/all`
- Data structure mismatch → Changed from `.opportunities` to `.alerts`
- Array initialization errors → Added Array.isArray() checks
- Widget size too small → Increased to 450×1000, made resizable

**Files Modified:**
- frontend/electron/main.js
- frontend/src/components/GameCard.tsx

**Files Created:**
- frontend/public/extension-widget/popup-desktop.html
- frontend/public/extension-widget/popup-desktop.js (modified from popup.js)

---

## Quick Reference

### Development Commands

```bash
# Start development server (React)
cd frontend
npm run dev

# Start Electron in development mode
cd frontend
npm run dev:electron:win

# Kill all Electron processes
powershell -Command "Get-Process electron -ErrorAction SilentlyContinue | Stop-Process -Force"

# Build for production
npm run build
npm run build:electron:win
```

### Important Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Reload renderer process (React app) |
| `F12` | Toggle DevTools |
| `Ctrl+Shift+I` | Toggle DevTools (alternate) |
| `F11` | Toggle fullscreen |
| `Ctrl+Q` | Quit application |

**Note:** Main process changes (main.js) require full restart, not just Ctrl+R

### IPC Handlers

```javascript
// Open new window
ipcMain.handle('open-window', (event, route) => {
  createWindow(route);
});

// Get list of open windows
ipcMain.handle('get-open-windows', () => {
  return Array.from(openWindows.keys());
});
```

### Widget Configuration

**Default Size:** 450px × 1000px
**Min Size:** 300px × 400px
**Max Width:** 600px
**Resizable:** Yes
**Always On Top:** Yes
**Refresh Interval:** 10 seconds

**API Endpoint:** `GET https://max-ev-sports.com/api/alerts/all?user_id=default`

**LocalStorage Keys:**
- `soundEnabled` (boolean)
- `voiceEnabled` (boolean)

---

## Known Issues & Future Work

### Known Issues
1. **Widget bookmaker links** - Currently just log to console, need Electron shell integration
2. **Auto-open widget** - Currently enabled for demo, should be optional
3. **Missing strategy data** - Goalie pulls, quarter reversals, injury props not in API response

### Planned Features
1. **Native notifications** - Use Electron Notification API
2. **Window state persistence** - Remember size/position on restart
3. **Multiple monitors support** - Better handling of multi-display setups
4. **Auto-updater** - Electron auto-update integration
5. **Keyboard shortcuts** - Global hotkeys for quick actions
6. **Dock/taskbar integration** - Badge counts for new alerts
7. **More widgets** - Calculator, bet tracker, bankroll manager
8. **Settings panel** - Desktop-specific settings UI
9. **Production build** - Create installer with electron-builder

### Technical Debt
1. Remove debugging console.logs from production
2. Add error boundaries for renderer crashes
3. Implement proper error handling for API failures
4. Add unit tests for window management
5. Document IPC API more thoroughly

---

## API Integration Notes

### Production API Base
```javascript
const API_BASE = 'https://max-ev-sports.com/api';
```

### Vite Proxy (Development Only)
```javascript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'https://max-ev-sports.com',
      changeOrigin: true,
      secure: true,
    }
  }
}
```

### Endpoints Used
- `/api/alerts/all?user_id=default` - All alerts (widget)
- `/api/games` - Live games data
- `/api/opportunities` - Arbitrage opportunities
- `/api/steam-moves` - Line movement alerts
- `/api/middles` - Middle opportunities

---

## Troubleshooting

### Widget Not Showing Alerts
1. Check console logs: `[DESKTOP WIDGET]` messages
2. Verify API response structure
3. Ensure arrays are initialized properly
4. Check network tab for 404 errors

### Window Not Appearing
1. Full restart required for main.js changes
2. Check if window already exists for that route
3. Look for errors in console about window creation
4. Verify route exists in WINDOW_ROUTES

### Electron Won't Start
1. Kill existing processes first
2. Check Node.js version compatibility
3. Verify Electron is installed: `npm list electron`
4. Try: `npm install` to reinstall dependencies

### Hot Reload Not Working
1. Ctrl+R only works for renderer process
2. Main process requires full restart
3. Check Vite dev server is running (port 5173)
4. Look for CORS errors in console

---

## Contact & Support

**Developer:** Nash (claude.ai/code)
**Project Owner:** MAX EV Sports
**Documentation Updated:** November 5, 2025

For issues or questions:
1. Check this log file first
2. Review session logs: `SESSION_LOG_YYYY-MM-DD.md`
3. Check console output for error messages
4. Verify all dependencies are installed

---

## Version History

### v0.2.0 (November 5, 2025)
- Added always-on-top alerts widget
- Restored latency display to game cards
- Widget is resizable and auto-refreshing
- Desktop-specific popup implementation

### v0.1.0 (November 4, 2025)
- Initial Electron setup
- Multi-window architecture
- System tray integration
- Window arrangement tools
- Basic IPC communication

---

**End of Desktop Client Development Log**
