# DEPLOYMENT REMINDER ⚠️
**CRITICAL: Always deploy to the correct directory!**

---

## ✅ CORRECT Deployment Location

```bash
# Frontend deployment (CORRECT)
/var/www/sporttrader/
```

**Why**: This is a symlink to `/root/sporttrader/frontend/dist`
- Nginx serves from: `/var/www/sporttrader`
- Auto-updates when frontend is rebuilt

---

## ❌ INCORRECT Location (PURGED)

```bash
# DO NOT USE THIS PATH
/var/www/max-ev-sports/  ❌ REMOVED
```

**Status**: Permanently deleted on December 3, 2025 @ 3:22 PM CST

---

## Correct Deployment Commands

### Frontend Deployment
```bash
# Option 1: Deploy to symlink (RECOMMENDED)
scp -r /c/Users/nashr/max-ev-sports/frontend/dist/* root@148.230.87.135:/root/sporttrader/frontend/dist/

# Option 2: Deploy directly to web directory
scp -r /c/Users/nashr/max-ev-sports/frontend/dist/* root@148.230.87.135:/var/www/sporttrader/
```

### Backend Deployment
```bash
scp /c/Users/nashr/max-ev-sports/backend/routes/model_performance.py root@148.230.87.135:/root/sporttrader/backend/routes/
```

---

## Verification After Deployment

### Check Nginx Config
```bash
ssh root@148.230.87.135 "cat /etc/nginx/sites-enabled/maxevsports | grep 'root'"
# Should show: root /var/www/sporttrader;
```

### Verify Files Are in Correct Location
```bash
ssh root@148.230.87.135 "ls -lah /var/www/sporttrader/index.html"
ssh root@148.230.87.135 "ls -lah /var/www/sporttrader/assets/"
```

### Check Bundle Version
```bash
curl -s https://max-ev-sports.com/ | grep -o "index-[^\"]*\.js" | head -1
```

---

## Directory Structure (VPS)

```
/var/www/
├── html/                              # Default nginx (not used)
├── sporttrader/                       # ✅ CORRECT - nginx serves from here
│   └── (symlink to /root/sporttrader/frontend/dist/)
├── sporttrader_backup_20251026/       # Old backup
└── venv/                              # Virtual environment

/root/sporttrader/
├── backend/
│   ├── routes/                        # Backend API routes
│   ├── ml/
│   │   └── predictions.db             # Main database
│   └── main.py                        # FastAPI app
└── frontend/
    └── dist/                          # Built frontend (symlinked to /var/www/sporttrader)
        ├── index.html
        └── assets/
```

---

## Why the Mistake Happened

On December 3, 2025, changes weren't visible because files were deployed to `/var/www/max-ev-sports/` but nginx serves from `/var/www/sporttrader/`.

**Evidence**:
```
Old bundle: index-D0fyFuG_-1764788170243.js ❌ (wrong location)
New bundle: index-0-4Oyca4-1764796305419.js ✅ (correct location)
```

---

## Hard Refresh After Deployment

Users must clear browser cache to see changes:
- **Windows**: Ctrl + F5
- **Mac**: Cmd + Shift + R
- **Linux**: Ctrl + Shift + R

---

**Document Created**: December 3, 2025 @ 3:22 PM CST
**Status**: `/var/www/max-ev-sports/` has been permanently removed
**Correct Path**: Always use `/var/www/sporttrader/` or `/root/sporttrader/`
