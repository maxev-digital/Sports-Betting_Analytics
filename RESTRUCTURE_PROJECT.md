# MaxEV Sports - Project Restructuring Guide

## 🎯 Problem

Current directory structure is misleading:
```
C:\Users\nashr\backend\scrapers\nba\
├── backend/         # FastAPI backend
├── frontend/        # React frontend
├── docs/
└── ...
```

**Issues:**
1. ❌ Named "nba" but contains multi-sport platform (NBA, NFL, NHL, NCAAF, MLB, Tennis)
2. ❌ Nested under "backend/scrapers/" which doesn't make sense
3. ❌ Confuses AI models and other developers
4. ❌ Doesn't match GitHub repo name (MaxEvSports)

## ✅ Solution

Restructure to clean, logical directory:
```
C:\Users\nashr\Max_EV_Sports\
├── backend/         # FastAPI backend
├── frontend/        # React frontend
├── docs/           # Documentation
├── scripts/        # Utility scripts
└── tests/          # Tests
```

**Benefits:**
- ✅ Clear project name
- ✅ Matches GitHub repo name
- ✅ No confusing nesting
- ✅ Self-explanatory structure
- ✅ Professional organization

---

## 📋 Step-by-Step Restructuring

### STEP 1: Backup Current Work

```bash
# Commit any uncommitted changes first!
cd C:\Users\nashr\backend\scrapers\nba
git add .
git commit -m "Pre-restructure backup"
git push origin main
```

### STEP 2: Create New Directory Structure

```bash
# Create new root directory
mkdir C:\Users\nashr\Max_EV_Sports
cd C:\Users\nashr\Max_EV_Sports

# Initialize git (if starting fresh)
# OR clone from GitHub
git clone https://github.com/anashp78/MaxEvSports.git .
```

### STEP 3: Move Core Components

**Option A: If starting from scratch with Git clone**
```bash
# Already done! Your GitHub repo will have the right structure
cd C:\Users\nashr\Max_EV_Sports
# Structure is ready to go
```

**Option B: If moving files manually**
```bash
# Move from old location to new
xcopy C:\Users\nashr\backend\scrapers\nba\backend C:\Users\nashr\Max_EV_Sports\backend /E /I
xcopy C:\Users\nashr\backend\scrapers\nba\frontend C:\Users\nashr\Max_EV_Sports\frontend /E /I

# Move documentation
mkdir C:\Users\nashr\Max_EV_Sports\docs
move C:\Users\nashr\backend\scrapers\nba\*.md C:\Users\nashr\Max_EV_Sports\docs\

# Move root files
move C:\Users\nashr\backend\scrapers\nba\README.md C:\Users\nashr\Max_EV_Sports\
move C:\Users\nashr\backend\scrapers\nba\.gitignore C:\Users\nashr\Max_EV_Sports\
```

### STEP 4: Clean New Structure

**Organize documentation:**
```bash
cd C:\Users\nashr\Max_EV_Sports

# Create organized docs structure
mkdir docs\deployment
mkdir docs\strategies
mkdir docs\api
mkdir docs\archive

# Move deployment docs
move docs\DEPLOYMENT_GUIDE.md docs\deployment\
move docs\SERVER_MIGRATION_GUIDE.md docs\deployment\
move docs\DEPLOYMENT_DIGITALOCEAN.md docs\deployment\

# Move strategy docs
move docs\*STRATEGY*.md docs\strategies\
move docs\*IMPLEMENTATION*.md docs\strategies\

# Archive old files
move docs\*Chat*.md docs\archive\
move docs\*.mp3 docs\archive\
```

**Clean up root:**
```bash
# Keep only essential files in root
# Should have:
# - README.md
# - .gitignore
# - backend/
# - frontend/
# - docs/
# - scripts/ (if needed)
```

### STEP 5: Update VS Code Workspace

**Update workspace settings:**
```bash
# Open VS Code at new location
cd C:\Users\nashr\Max_EV_Sports
code .
```

**Update `.vscode/settings.json` (create if doesn't exist):**
```json
{
  "workbench.name": "MaxEV Sports",
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/dist": true,
    "**/.venv": true,
    "**/venv": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.venv": true,
    "**/venv": true
  }
}
```

### STEP 6: Update Git Repository

**If you cloned from GitHub, you're done!**

**If moving manually:**
```bash
cd C:\Users\nashr\Max_EV_Sports

# Initialize new repo
git init
git add .
git commit -m "Restructure: Clean project organization

- Moved from backend/scrapers/nba to Max_EV_Sports
- Organized documentation into docs/ subdirectories
- Cleaned up root directory
- Matches GitHub repo structure"

# Set remote to your GitHub repo
git remote add origin https://github.com/anashp78/MaxEvSports.git

# Force push (since we're restructuring)
git push -f origin main
```

### STEP 7: Update Server Paths

**SSH into your VPS:**
```bash
ssh username@YOUR_VPS_IP
```

**Update deployment path:**
```bash
# Old path: /home/username/sporttrader-backend
# New path: /home/username/maxevsports

# If already deployed, rename:
cd /home/username
mv sporttrader-backend maxevsports
# OR
mv nba maxevsports

# Update git remote
cd /home/username/maxevsports
git remote set-url origin https://github.com/anashp78/MaxEvSports.git
git pull origin main
```

**Update Nginx config:**
```bash
sudo nano /etc/nginx/sites-available/maxevsports

# Update paths:
root /home/username/maxevsports/frontend/dist;
```

**Update Supervisor config:**
```bash
sudo nano /etc/supervisor/conf.d/maxevsports.conf

# Update paths:
command=/home/username/maxevsports/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/home/username/maxevsports/backend
```

**Update .env.production:**
```bash
cd /home/username/maxevsports/backend
nano .env.production

# Update paths:
GOOGLE_SHEETS_CREDENTIALS=/home/username/maxevsports/credentials.json
LOG_FILE=/var/log/maxevsports/backend.log
```

**Restart services:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart maxevsports-backend
sudo systemctl restart nginx
```

### STEP 8: Update Your Local Development

**Update environment:**
```bash
cd C:\Users\nashr\Max_EV_Sports

# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ..\frontend
npm install
```

**Update VS Code workspace:**
```bash
# Close old workspace
# Open new: File > Open Folder > C:\Users\nashr\Max_EV_Sports
```

**Update terminal paths:**
- Update any scripts that reference old paths
- Update documentation with new paths
- Update README.md with correct paths

---

## 📁 Final Directory Structure

```
C:\Users\nashr\Max_EV_Sports\
│
├── backend/                      # FastAPI Backend
│   ├── main.py                  # Main application
│   ├── requirements.txt         # Python dependencies
│   ├── .env.production.example  # Production env template
│   ├── routes/                  # API routes
│   ├── models/                  # Data models
│   ├── strategies/              # Betting strategies
│   └── storage/                 # Data storage
│
├── frontend/                     # React Frontend
│   ├── src/                     # Source code
│   ├── public/                  # Public assets
│   ├── package.json             # NPM dependencies
│   ├── .env.production          # Production environment
│   └── vite.config.ts          # Vite configuration
│
├── docs/                         # Documentation
│   ├── deployment/              # Deployment guides
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   ├── SERVER_MIGRATION_GUIDE.md
│   │   └── DEPLOYMENT_DIGITALOCEAN.md
│   ├── strategies/              # Strategy documentation
│   │   ├── FAVORITE_COMEBACK_STRATEGY_GUIDE.md
│   │   ├── GOALIE_PULL_STRATEGY_GUIDE.md
│   │   └── IMPLEMENTATION_SUMMARY.md
│   ├── api/                     # API documentation
│   └── archive/                 # Old/archived docs
│
├── scripts/                      # Utility Scripts
│   ├── setup/                   # Setup scripts
│   └── maintenance/             # Maintenance scripts
│
├── tests/                        # Tests (future)
│
├── .gitignore                   # Git ignore rules
├── README.md                    # Project README
└── LICENSE                      # License file
```

---

## ✅ Verification Checklist

After restructuring, verify:

### Local Development
- [ ] VS Code opens correct directory
- [ ] Backend runs: `cd backend && python main.py`
- [ ] Frontend runs: `cd frontend && npm run dev`
- [ ] Git repository connected: `git remote -v`
- [ ] All documentation accessible in `docs/`

### Git Repository
- [ ] GitHub repo structure matches local
- [ ] All files committed and pushed
- [ ] No references to old "nba" path
- [ ] Clean commit history

### Server Deployment
- [ ] Nginx serves from new path
- [ ] Supervisor runs from new path
- [ ] .env.production has correct paths
- [ ] Logs writing to new location
- [ ] Site accessible at https://max-ev-sports.com
- [ ] API accessible at https://api.max-ev-sports.com

---

## 🚨 Common Issues

### "Module not found" errors
```bash
# Rebuild Python virtual environment
cd C:\Users\nashr\Max_EV_Sports\backend
rm -rf venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Git issues after move
```bash
# Reset git if needed
cd C:\Users\nashr\Max_EV_Sports
rm -rf .git
git init
git remote add origin https://github.com/anashp78/MaxEvSports.git
git pull origin main
```

### Server not finding files
```bash
# Verify all paths in configs
sudo nano /etc/nginx/sites-available/maxevsports
sudo nano /etc/supervisor/conf.d/maxevsports.conf
nano /home/username/maxevsports/backend/.env.production
```

---

## 📝 Update Documentation References

After restructuring, update these files to reflect new paths:

1. **README.md** - Update all path references
2. **DEPLOYMENT_GUIDE.md** - Update example paths
3. **SERVER_MIGRATION_GUIDE.md** - Update directory references
4. **.env.production.example** - Update path examples

**Find and replace:**
```bash
# Old: backend/scrapers/nba
# New: Max_EV_Sports

# Old: C:\Users\nashr\backend\scrapers\nba
# New: C:\Users\nashr\Max_EV_Sports
```

---

## 🎉 Benefits After Restructuring

1. **Clear Project Identity**
   - Name matches function (MaxEV Sports, not "nba")
   - Professional structure
   - Easy to understand

2. **Better AI Model Context**
   - AI models see "Max_EV_Sports" and understand it's a sports platform
   - No confusion from "nba" folder name
   - Clearer file organization

3. **Easier Collaboration**
   - Logical directory structure
   - Clear separation of concerns
   - Standard project layout

4. **Maintenance**
   - Easier to find files
   - Clear documentation organization
   - Logical component separation

---

**Created**: 2025-10-22
**Status**: Ready for implementation
