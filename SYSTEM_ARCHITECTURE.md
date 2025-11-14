# MAX EV SPORTS - SYSTEM ARCHITECTURE
**Status:** 🔒 READ ONLY - DO NOT MODIFY WITHOUT EXPLICIT USER APPROVAL
**Last Updated:** November 14, 2025
**Version:** 1.0

---

## ⚠️ CRITICAL - READ THIS FIRST

**This document describes the WORKING production system.**

**BEFORE making ANY changes:**
1. ✋ READ this entire document
2. ✋ READ `CRITICAL_FIXES_DO_NOT_CHANGE.md`
3. ✋ READ `ML_AUTONOMOUS_SYSTEM_REFERENCE.md`
4. ✋ ASK USER before modifying protected code
5. ✋ VERIFY changes won't break production

**The user has experienced MULTIPLE instances of:**
- "Fixes" that break working code
- Data being "lost" (when it was never deployed)
- Protected sections being modified
- The same problems being "solved" repeatedly

**DO NOT be another instance that breaks things. ASK FIRST.**

---

## 📋 TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Infrastructure Architecture](#infrastructure-architecture)
3. [Data Storage Strategy](#data-storage-strategy)
4. [Deployment Pipeline](#deployment-pipeline)
5. [Machine Learning Systems](#machine-learning-systems)
6. [Protected Code Sections](#protected-code-sections)
7. [Common Pitfalls](#common-pitfalls)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## SYSTEM OVERVIEW

### What This Platform Does

Max EV Sports is a **sports betting analytics platform** with:

1. **Game Totals Predictions** (NBA, NCAAB, NHL, NFL, NCAAF)
   - ML models predict game totals (over/under)
   - Daily predictions logged and graded
   - Performance tracked on model performance page

2. **Player Props Predictions** (NBA)
   - ML models predict player stats (points, rebounds, assists, etc.)
   - 28 models (7 prop types × 4 algorithms)
   - 98-100% directional accuracy

3. **Advanced Strategies** (25 different betting strategies)
   - Live alerts during games
   - Monte Carlo simulations
   - Regression to mean detection
   - Empty net situations (NHL)

4. **Edge Lab** (Real-time betting opportunities)
   - Compares predictions to market lines
   - Identifies positive EV opportunities
   - Filters by sport, confidence, edge %

### Key Architecture Principles

1. **Stability > New Features**
   - Working code is sacred
   - Never "optimize" without user approval
   - Test before deploying

2. **Data Redundancy**
   - D: drive is source of truth for databases
   - Daily automated backups
   - Never delete without backups

3. **Incremental Changes**
   - Small, tested changes
   - One system at a time
   - Always have rollback plan

---

## INFRASTRUCTURE ARCHITECTURE

### Three-Tier System

```
┌─────────────────────────────────────────────────────────────┐
│                     LOCAL DEVELOPMENT                        │
│  Location: C:/Users/nashr/                                  │
│  Purpose: Code development, testing, git operations         │
│  What's Here: All .py files, frontend code, ML scripts     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Git Push (Code Only)
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     GITHUB REPOSITORY                        │
│  Purpose: Version control for CODE files only              │
│  What's Tracked: .py, .tsx, .md, .sh, .json                │
│  What's NOT Tracked: .db, .csv (data files), logs          │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Git Pull
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  PRODUCTION VPS (Hostinger)                  │
│  IP: 148.230.87.135                                         │
│  Location: /root/sporttrader/                               │
│  Purpose: Live production serving users                     │
│  What's Here: Code (from git) + Data (from sync script)    │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │ Database Sync (Daily 2 AM CST)
                              │
┌─────────────────────────────────────────────────────────────┐
│                    DATA BACKUP DRIVE                         │
│  Location: D:/backend/                                      │
│  Purpose: Source of truth for ALL database files           │
│  What's Here: .db files, large CSVs, ML training data      │
│  Sync: Automated daily upload to VPS                       │
└─────────────────────────────────────────────────────────────┘
```

### Critical Understanding: Code ≠ Data

**CODE (.py, .tsx, .js, .sh):**
- Lives in git
- Deployed via `git pull` on VPS
- Changes are tracked
- Can be rolled back

**DATA (.db, .csv, large files):**
- Lives on D: drive (NOT in git)
- Deployed via `sync_databases_to_vps.py`
- Changes are NOT tracked in git
- Backup strategy required

**❌ COMMON MISTAKE:**
"I committed the code to git so the data should be on VPS"
- **WRONG:** Data files are NOT in git
- **RIGHT:** Data must be manually synced via script

---

## DATA STORAGE STRATEGY

### Where Different Types of Data Live

| Data Type | Primary Location | Backup Location | Deployed To VPS Via | Git Tracked |
|-----------|-----------------|-----------------|---------------------|-------------|
| **Python Code** | C:/Users/nashr/backend/ | GitHub | git pull | ✅ Yes |
| **Frontend Code** | C:/Users/nashr/frontend/ | GitHub | git pull + build | ✅ Yes |
| **ML Models (.joblib)** | D:/backend/ml/trained_models/ | VPS backups/ | Manual scp | ❌ No |
| **Player Props DB** | D:/backend/data/player_props.db | D:/backend/backups/ | sync_databases_to_vps.py | ❌ No |
| **Predictions Logs** | D:/backend/data/tracking/*.csv | VPS backups/ | sync_databases_to_vps.py | ❌ No |
| **Historical Data** | D:/backend/data/historical/ | VPS (read-only) | Manual copy (one-time) | ❌ No |
| **Application Logs** | VPS /root/sporttrader/backend/logs/ | Rotated (100MB max) | N/A (generated on VPS) | ❌ No |

### Why D: Drive?

**Problem Solved:** User was losing database work when VPS would "reset"
**Root Cause:** Databases were never being deployed (only code via git)
**Solution:** D: drive is source of truth, automated daily sync to VPS

**D: Drive Contents:**
```
D:/backend/
├── data/
│   ├── player_props.db (6.5 MB) - NBA props predictions/results
│   ├── historical/ - 23,000+ games for ML training
│   └── tracking/ - Predictions and results logs
├── ml/
│   └── trained_models/ - 87 ML model files (250 MB)
└── backups/ - Timestamped database snapshots
```

### Backup Strategy (Implemented Nov 14, 2025)

**Automated Daily Sync:**
- **Script:** `backend/sync_databases_to_vps.py`
- **Schedule:** Daily 2:00 AM CST (Windows Task Scheduler)
- **Setup:** Run `SETUP_DATABASE_SYNC.bat` once
- **What it Does:**
  1. Creates timestamped backup on VPS
  2. Uploads D: drive databases to VPS
  3. Verifies file integrity
  4. Cleans up backups >7 days old

**Manual Backups:**
- **Script:** `backend/backup_predictions_daily.py`
- **Schedule:** Daily 1:55 AM CST (before predictions)
- **Purpose:** Backup predictions/results before any scripts run

---

## DEPLOYMENT PIPELINE

### How Code Gets to Production

```
Developer (You) → Local Changes → Git Commit → Git Push → VPS Git Pull → Service Restart
```

**Step-by-Step:**

1. **Local Development** (C:/Users/nashr/)
   ```bash
   # Make changes to .py or .tsx files
   git add backend/routes/new_feature.py
   git commit -m "Add new feature"
   git push origin main
   ```

2. **VPS Deployment** (148.230.87.135)
   ```bash
   ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
   cd /root/sporttrader
   git pull origin main
   systemctl restart sporttrader  # Backend
   # Frontend rebuilds automatically via webhook
   ```

3. **Verify Deployment**
   ```bash
   curl http://localhost:8000/api/health
   systemctl status sporttrader
   ```

### How Data Gets to Production

```
D: Drive → sync_databases_to_vps.py → VPS
```

**Process:**
- **Automatic:** Runs daily at 2 AM CST
- **Manual:** `python sync_databases_to_vps.py`
- **Files Synced:**
  - player_props.db
  - predictions_log.csv
  - results_log.csv
  - (Add more in DATABASE_SYNC_MAP)

### What About ML Models?

**ML Models (.joblib files):**
- **Location:** D:/backend/ml/trained_models/ (250 MB)
- **Deployed Once:** Already on VPS at `/root/sporttrader/backend/ml/models/`
- **Updates:** Only when models are retrained (weekly Monday 4-9 AM)
- **How:** Automatic via autonomous learning system

**DO NOT:**
- ❌ Manually copy model files
- ❌ Delete models without backup
- ❌ Retrain models outside of autonomous system

---

## MACHINE LEARNING SYSTEMS

### Two Separate ML Systems

#### 1. Game Totals Predictions (5 Sports)

**What:** Predict over/under for entire games
**Sports:** NBA, NCAAB, NHL, NFL, NCAAF
**Models:** 87 total (5 sports × multiple markets × 4-5 algorithms)

**Architecture:**
```
Historical Games (23k+)
    ↓
Weekly Retraining (Mondays 4-9 AM CST)
    ↓
Trained Models (.joblib files)
    ↓
Daily Predictions (9-11 AM CST)
    ↓
Predictions Log (CSV)
    ↓
Game Results (1 AM CST next day)
    ↓
Results Log (CSV)
    ↓
Model Performance API
    ↓
Frontend Display
```

**Key Files:**
- Training: `backend/ml/autonomous_learning_system.py`
- Prediction: `backend/run_predictions_and_log.py`
- Grading: `backend/grade_yesterday_predictions.py`
- Models: `/root/sporttrader/backend/ml/models/*.joblib`

**DO NOT MODIFY:**
- ✋ Autonomous learning schedule (working perfectly)
- ✋ Model file structure
- ✋ Prediction/results log format

#### 2. Player Props Predictions (NBA Only)

**What:** Predict player stats (points, rebounds, assists, etc.)
**Sports:** NBA only (for now)
**Models:** 28 total (7 prop types × 4 algorithms)

**Architecture:**
```
Historical Props (15,530 results)
    ↓
Weekly Retraining (Sundays 3 AM CST)
    ↓
Enhanced 22-Feature Models
    ↓
Daily Predictions (not yet automated)
    ↓
SQLite Database (player_props.db)
    ↓
API Endpoints (created, not activated)
    ↓
Frontend (not yet created)
```

**Key Files:**
- Training: `backend/ml/models/nba_props_trainer_enhanced.py`
- Prediction: `backend/ml/predictions/daily_props_predictor_fast.py`
- Database: `D:/backend/data/player_props.db` (6.5 MB)
- Models: `D:/backend/ml/trained_models/*.joblib`

**Status:** 60% complete
- ✅ ML models (98-100% accuracy)
- ✅ Data on VPS in correct format
- ❌ API endpoints (need restart)
- ❌ Frontend UI
- ❌ Daily automation

---

## PROTECTED CODE SECTIONS

### 🔒 DO NOT MODIFY WITHOUT USER APPROVAL

**Reference:** See `CRITICAL_FIXES_DO_NOT_CHANGE.md` for full details

#### 1. Edge Scanner Sport Filtering
**File:** `backend/routes/edge_scanner.py` line 597
**Why:** Correct filtering logic that took multiple attempts to fix
**Status:** WORKING IN PRODUCTION

#### 2. Model Performance Merge Strategy
**File:** `backend/routes/model_performance.py` line 76
**Why:** Complex merge logic between predictions and results
**Status:** WORKING IN PRODUCTION
**Note:** Now has fallback to display results even without matching predictions

#### 3. Charts Cumulative Calculation
**File:** `backend/routes/model_performance.py` line 234
**Why:** Correct cumulative profit/loss calculation
**Status:** WORKING IN PRODUCTION

#### 4. Frontend API Configuration
**File:** `frontend/src/config.ts`
**Why:** Correct API endpoints for production
**Status:** WORKING IN PRODUCTION

#### 5. Time Range Filter Implementation
**File:** `frontend/src/pages/ModelPerformance.tsx`
**Why:** Working date filtering with proper timezone handling
**Status:** WORKING IN PRODUCTION

#### 6. CSV Prediction Format
**File:** `backend/generate_all_sport_predictions.py`
**Why:** Specific format expected by downstream systems
**Status:** WORKING IN PRODUCTION

### ✅ Safe to Modify (With Testing)

- Adding NEW features (don't modify existing)
- Frontend UI improvements (visual only)
- New ML features (in feature engineering files)
- Documentation updates
- New API endpoints (don't break existing)

---

## COMMON PITFALLS

### ❌ Pitfall #1: "I fixed the code and committed to git, why isn't it on VPS?"

**Problem:** Code is committed but VPS still running old version

**Cause:** Forgot to deploy

**Solution:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
cd /root/sporttrader && git pull origin main
systemctl restart sporttrader
```

---

### ❌ Pitfall #2: "I updated the database locally, why is VPS data empty?"

**Problem:** Database changes not on VPS

**Cause:** Databases don't sync via git

**Solution:**
```bash
# If you made database changes on C: drive, move to D: first
# Then run sync script
python C:/Users/nashr/backend/sync_databases_to_vps.py
```

---

### ❌ Pitfall #3: "The predictions format is wrong (probabilities instead of values)"

**Problem:** Props showing 0.267 instead of 4.2 rebounds

**Cause:** Old predictions from before Nov 13 fix

**Solution:**
- Check timestamp: Only use predictions after `2025-11-14 01:00:00`
- Filter query: `WHERE timestamp > '2025-11-14 01:00:00'`
- Correct format: 612 predictions available

---

### ❌ Pitfall #4: "I created an API endpoint but it returns 404"

**Problem:** New endpoint not accessible

**Cause:** FastAPI server not restarted after adding route

**Solution:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
systemctl restart sporttrader
# Wait 5 seconds
curl http://localhost:8000/api/your-new-endpoint
```

---

### ❌ Pitfall #5: "Where did all the predictions go?"

**Problem:** Predictions file seems empty or missing data

**Actual Issue:** You're looking in wrong location

**Solution:**
- **Predictions ARE on D: drive:** Check `D:/backend/data/tracking/`
- **Not on C: drive** (working directory)
- **VPS data:** Synced from D: drive daily at 2 AM

---

### ❌ Pitfall #6: "I want to retrain ML models"

**Problem:** Manually retraining breaks autonomous system

**DON'T:**
```bash
# ❌ Don't do this
python backend/ml/models/nba_props_trainer_enhanced.py
```

**DO:**
```bash
# ✅ Let autonomous system handle it (Mondays 4-9 AM)
# OR if you must test:
python backend/ml/autonomous_learning_system.py --sport nba --dry-run
```

---

## TROUBLESHOOTING GUIDE

### "Model Performance Page Shows No Data"

**Check List:**
1. ✅ VPS has results_log.csv? `ssh ... "wc -l /root/sporttrader/backend/data/tracking/results_log.csv"`
2. ✅ Predictions log has data? `ssh ... "wc -l /root/sporttrader/backend/data/tracking/predictions_log.csv"`
3. ✅ API endpoint working? `curl https://max-ev-sports.com/api/model-performance/overview`
4. ✅ Frontend pointing to correct API? Check `frontend/src/config.ts`

**Fix:**
- If results exist but API returns 0: Check prediction_id format mismatch
- If API works but frontend shows nothing: Clear Cloudflare cache
- If no data at all: Run `sync_databases_to_vps.py`

---

### "Props Predictions Are Probabilities (0.267) Not Values (4.2)"

**Cause:** Viewing old predictions from before Nov 13 fix

**Fix:**
```sql
-- Filter to only correct format predictions
SELECT * FROM player_props_predictions
WHERE timestamp > '2025-11-14 01:00:00'
AND prop_type = 'rebounds';
-- Should show predicted_value around 4-5, not 0.2
```

---

### "Backend Service Won't Start on VPS"

**Debug Steps:**
```bash
# Check service status
systemctl status sporttrader

# Check logs for errors
journalctl -u sporttrader -n 50

# Check if port 8000 is in use
netstat -tulpn | grep 8000

# Try starting manually
cd /root/sporttrader/backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Common Issues:**
- Python import error: Check all dependencies installed
- Port in use: Kill old process
- File permissions: Check ownership

---

### "Database Sync Failed"

**Check:**
```bash
# Test SSH connection
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "echo Connected"

# Check D: drive has file
ls -lh D:/backend/data/player_props.db

# Run sync manually with verbose output
python backend/sync_databases_to_vps.py
```

---

## SYSTEM HEALTH CHECKS

### Daily Health Check (Run This Every Morning)

```bash
# 1. Check VPS is responding
curl -I https://max-ev-sports.com

# 2. Check backend service
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl status sporttrader --no-pager"

# 3. Check predictions were generated
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "tail -5 /root/sporttrader/backend/logs/prediction_runner.log"

# 4. Check yesterday's games were graded
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "tail -5 /root/sporttrader/backend/logs/grading_daily.log"

# 5. Check database sync ran
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "ls -lh /root/sporttrader/backend/data/*.backup_$(date +%Y%m%d)*"
```

---

## VERSION HISTORY

**v1.0 - November 14, 2025**
- Initial architecture documentation
- Documented 3-tier infrastructure
- Data storage strategy defined
- Deployment pipeline documented
- Protected code sections identified
- Common pitfalls cataloged
- Automated database sync implemented

---

## 📚 RELATED DOCUMENTS

**Must Read Before Making Changes:**
1. `CRITICAL_FIXES_DO_NOT_CHANGE.md` - Protected code sections
2. `ML_AUTONOMOUS_SYSTEM_REFERENCE.md` - ML system documentation
3. `CLAUDE.md` - Claude Code instructions
4. `NBA_PROPS_ON_VPS_STATUS.md` - Props system status

**Reference Documentation:**
5. `AUTONOMOUS_SYSTEM_STATUS.md` - Autonomous learning status
6. `COMPLETE_DATA_PIPELINE_SYSTEM.md` - Data pipeline docs
7. `VPS_STATUS_2025-11-14.md` - VPS configuration

---

## 🔒 FINAL WARNING

**This system is WORKING IN PRODUCTION serving REAL USERS.**

**Before making ANY change:**
1. Read this entire document
2. Read related docs
3. Check if code is protected
4. Test locally first
5. Deploy incrementally
6. Have rollback plan
7. **ASK USER if uncertain**

**The user's frustration is valid - they've been told:**
- "We lost the data" (it was never deployed)
- "This is broken" (it was working)
- "I fixed it" (broke working code)

**Don't be the Claude instance that breaks production.**

**When in doubt, ASK. Don't assume. Don't "improve". Don't "optimize".**

**Stability > Features. Working > Perfect.**

---

**END OF SYSTEM ARCHITECTURE - v1.0**
