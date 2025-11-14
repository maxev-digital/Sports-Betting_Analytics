# How to Launch MAX EV SPORTS

## Option 1: WEB APP (RECOMMENDED - Latest Features) ✅

**Open in your browser:**
```
https://max-ev-sports.com
```

**Why use the web version:**
- ✅ Always up-to-date with latest features
- ✅ NCAAB XGBoost Analytics fully integrated (63/82 games)
- ✅ No building or installation needed
- ✅ Same features as desktop app

**Quick Launch**: Double-click this file on your desktop:
`MAX EV SPORTS - Web.url` (created for you)

---

## Option 2: DESKTOP APP (Needs Rebuild)

**Current desktop app**: `C:\Users\nashr\frontend\dist-electron\win-unpacked\MAX EV SPORTS.exe`

**Issue**: This build is from October 28, 2024 - it's missing the new NCAAB analytics

**To rebuild with latest code:**

1. **Close ALL Electron instances** (important!)
   ```cmd
   taskkill /F /IM electron.exe
   taskkill /F /IM "MAX EV SPORTS.exe"
   ```

2. **Clean the dist folder**
   ```cmd
   cd C:\Users\nashr\frontend
   rm -rf dist-electron
   ```

3. **Build fresh**
   ```cmd
   cd C:\Users\nashr\frontend
   npm run build
   npm run electron:dist
   ```

4. **Launch**
   ```cmd
   cd C:\Users\nashr\frontend\dist-electron\win-unpacked
   start "MAX EV SPORTS.exe"
   ```

---

## Recommended Approach

**For now**: Use the **Web App** at https://max-ev-sports.com

It has ALL the latest features including:
- NCAAB XGBoost Analytics (purple Advanced tab)
- All sports (NBA, NHL, NFL, MLB, NCAAF, NCAAB)
- Live game tracking
- Strategy alerts
- Player props
- Odds comparison

**Later**: Rebuild desktop app when you want offline access or system tray features

---

## Testing NCAAB Analytics

1. Go to https://max-ev-sports.com
2. Navigate to "Live Games"
3. Find any NCAAB game card
4. Click the **ADVANCED** tab (purple)
5. You'll see:
   - Direction (OVER/UNDER)
   - Model prediction
   - Confidence %
   - Z-Score & Edge
   - Kelly sizing
   - And more...

**Current analytics**: 63 out of 82 NCAAB games (77% coverage)

---

## Quick Launchers Created

**Desktop shortcuts** (double-click to launch):
- `MAX EV SPORTS - Web.url` → Opens web app
- `MAX EV SPORTS.bat` → Launches desktop app (if built)
