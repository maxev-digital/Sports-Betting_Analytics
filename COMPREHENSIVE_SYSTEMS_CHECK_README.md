# Comprehensive Daily Systems Check - Complete Documentation

**Version**: 2.0
**Date**: December 4, 2025
**Status**: ✅ PRODUCTION READY

---

## 📋 Overview

This script performs a **complete health check** of the entire MAX-EV Sports platform, monitoring 24 critical components from data collection to API delivery.

### What It Checks

#### 1. **Data Collection Layer** (4 checks)
- ✅ Odds API Scrapers (run_all_scrapers.py)
- ✅ Enhanced Scrapers (TeamRankings, ESPN, BBRef)
- ✅ KenPom Scraper (critical for NCAAB)
- ✅ Player Props Stats Scrapers (NBA/NHL/NFL)

#### 2. **ML Prediction Layer** (3 checks)
- ✅ Enhanced ML Predictions (7 models × 5 sports)
- ✅ Player Props Predictions (NBA/NHL/NFL)
- ✅ DFS Crusher Combo Generation

#### 3. **Model Health** (2 checks)
- ✅ 35 Enhanced Models (7 per sport)
- ✅ Feature Dimensions (NBA:60, NCAAB:14, NHL:27, NFL:30, NCAAF:30)

#### 4. **Database Layer** (2 checks)
- ✅ Main predictions.db integrity
- ✅ Database size and growth

#### 5. **Grading & Results** (2 checks)
- ✅ Prediction Grading (ESPN API)
- ✅ Props Grading (BallDontLie API)

#### 6. **API Health** (2 checks)
- ✅ FastAPI Servers (ports 8000, 8888)
- ✅ Critical Endpoints (/api/ui/best-plays, etc.)

#### 7. **System Resources** (2 checks)
- ✅ Disk Space
- ✅ Memory Usage

---

## 🚀 Quick Start

### Deploy to VPS

```bash
# From your local machine (Windows)
bash deploy_comprehensive_systems_check.sh
```

This will:
1. Upload the script to VPS
2. Make it executable
3. Test it once
4. Update crontab to run daily at 11 PM CST

### Manual Execution

```bash
# SSH to VPS
ssh root@148.230.87.135

# Navigate to backend
cd /root/sporttrader/backend

# Run the check
python3 comprehensive_daily_systems_check.py
```

---

## 📧 Email Reports

### When Emails Are Sent

Daily at **11:00 PM CST** after all systems have had time to run:
- Scrapers: 6:30 AM - 7:30 AM
- ML Predictions: 8:05 AM
- Props Predictions: 10:30 AM - 11:00 AM
- Grading: 3:00 AM, 6:00 AM

### Email Content

**Subject Line Examples:**
- ✅ `Daily Systems Check: ALL OPERATIONAL` (0 failures)
- ⚠️ `Daily Systems Check: 2 Systems Need Attention` (1-3 failures)
- ❌ `Daily Systems Check: 5 SYSTEMS FAILING` (4+ failures)

**Body Includes:**
1. **Executive Summary** - Pass/Fail counts
2. **Component Status** - Organized by category
3. **Platform Stats** - Models, sports, bet types
4. **Action Items** - Details on failures (if any)

### Who Receives Email

Email is sent to: `ADMIN_EMAIL` from your `.env` file

Default: `gte.apw@gmail.com`

---

## 📊 What Gets Checked in Detail

### Data Collection

**Odds Scrapers**
- Log: `/root/sporttrader/backend/logs/cron_scraper.log`
- Checks: Activity today, success indicators, error messages
- Cron: 7:00 AM daily

**Enhanced Scrapers**
- Log: `/root/sporttrader/backend/logs/enhanced_scrapers.log`
- Checks: Log freshness (< 24h), recent updates
- Cron: 6:30 AM daily

**KenPom Scraper** (CRITICAL for NCAAB)
- Log: `/root/sporttrader/backend/logs/kenpom_scraper.log`
- Checks: Daily scrape success, data saved
- Cron: 7:30 AM daily

**Props Stats Scrapers**
- Files: `stats_scraper_nba_balldontlie.py`, `stats_scraper_nhl_moneypuck.py`, `stats_scraper_nfl.py`
- Checks: File existence (indirect check via props predictions)

### ML Predictions

**Enhanced ML Predictions (7 Models)**
- Log: `/root/sporttrader/backend/logs/ml_predictions_ENHANCED.log`
- Models: XGBoost, LightGBM, Random Forest, Linear, PyTorch TabularNet, CatBoost, Neural Ensemble
- Sports: NBA, NCAAB, NHL, NFL, NCAAF
- Checks: Activity today, all 5 sports processed, no errors
- Cron: 8:05 AM daily

**Player Props Predictions**
- Database: `player_prop_predictions` table
- Checks: Predictions in last 24h by sport (NBA/NHL/NFL)
- Cron: 10:30 AM daily

**DFS Crusher**
- Log: `/root/sporttrader/backend/logs/dfs_crusher.log`
- Checks: Log freshness, combo generation activity
- Cron: 11:00 AM daily

### Model Health

**Enhanced Models (35 total)**
- Location: `/root/sporttrader/backend/ml/models/`
- Per sport (5): 7 models each
  - `{sport}_xgboost_totals_enhanced.joblib`
  - `{sport}_lightgbm_totals_enhanced.joblib`
  - `{sport}_random_forest_totals_enhanced.joblib`
  - `{sport}_linear_totals_enhanced.joblib`
  - `{sport}_pytorch_tabular_totals_latest.pt`
  - `{sport}_catboost_totals_enhanced.joblib`
  - `{sport}_neural_ensemble_totals_latest.pt`
- Checks: All 35 files exist (allows 5 missing for flexibility)

**Feature Dimensions**
- Expected features per sport:
  - NBA: 60 features
  - NCAAB: 14 features
  - NHL: 27 features
  - NFL: 30 features
  - NCAAF: 30 features
- Checks: Loads XGBoost model for each sport, verifies `n_features_in_`

### Database

**Main Database**
- Path: `/root/sporttrader/backend/ml/predictions.db`
- Tables: `predictions`, `results`, `player_prop_predictions`
- Checks:
  - Database exists
  - Total predictions/results counts
  - Recent predictions (last 24h) by sport
  - Recent player props (last 24h)
- Success: Any recent predictions or props

**Database Size**
- Checks: File size in MB
- Thresholds:
  - < 5GB: OK ✅
  - > 5GB: Warning (consider archiving) ⚠️

### Grading & Results

**Prediction Grading**
- Log: `/root/sporttrader/backend/logs/db_grading.log`
- Checks: Log freshness (< 24h), grading activity
- Cron: 6:00 AM daily

**Props Grading**
- Log: `/root/sporttrader/backend/logs/props_grading.log`
- Checks: Log freshness (< 24h)
- Cron: 3:00 AM daily

### API Health

**API Servers**
- Production: Port 8000 (REQUIRED)
- Test: Port 8888 (optional)
- Checks: Running uvicorn processes

**Critical Endpoints**
- `/api/ui/best-plays`
- `/api/ui/model-performance`
- `/api/ui/live-games`
- Checks: HTTP status 200 or 422 (422 = missing params but endpoint works)

### System Resources

**Disk Space**
- Path: `/root/sporttrader`
- Thresholds:
  - \> 10 GB free: OK ✅
  - 5-10 GB free: Warning ⚠️
  - < 5 GB free: CRITICAL ❌

**Memory Usage**
- Checks: `free -m` output
- Thresholds:
  - < 80% used: OK ✅
  - 80-90% used: Warning ⚠️
  - \> 90% used: CRITICAL ❌

---

## 🔧 Maintenance

### Viewing Logs

```bash
# Full systems check log
tail -f /root/sporttrader/backend/logs/systems_check.log

# Individual component logs
tail -f /root/sporttrader/backend/logs/ml_predictions_ENHANCED.log
tail -f /root/sporttrader/backend/logs/cron_scraper.log
tail -f /root/sporttrader/backend/logs/kenpom_scraper.log
```

### Manual Test Run

```bash
# SSH to VPS
ssh root@148.230.87.135
cd /root/sporttrader/backend

# Run with color output
python3 comprehensive_daily_systems_check.py
```

### Checking Cron Job

```bash
# View crontab
crontab -l | grep comprehensive

# Should show:
# 0 23 * * * cd /root/sporttrader/backend && /usr/bin/python3 comprehensive_daily_systems_check.py >> logs/systems_check.log 2>&1
```

### Updating the Script

```bash
# From local machine
# 1. Edit comprehensive_daily_systems_check.py
# 2. Deploy
bash deploy_comprehensive_systems_check.sh
```

---

## 🚨 Troubleshooting

### No Email Received

**Check 1: Brevo API Key**
```bash
ssh root@148.230.87.135
cat /root/sporttrader/backend/.env | grep BREVO_API_KEY
```

**Check 2: Admin Email**
```bash
cat /root/sporttrader/backend/.env | grep ADMIN_EMAIL
```

**Check 3: Email Sending Logs**
```bash
grep -i "email" /root/sporttrader/backend/logs/systems_check.log
```

### False Failures

**Issue**: A check fails but system is actually working

**Solution**: Review the specific check logic in the script:
1. Check log file paths
2. Verify log formats haven't changed
3. Adjust thresholds if needed

### Adding New Checks

To add a new component check:

1. Create a check function:
```python
def check_my_new_component():
    """Check my new component"""
    print_header("MY NEW COMPONENT CHECK")

    # Your check logic here

    if all_good:
        print_success("Component working")
        return True, "Status message"
    else:
        print_error("Component failing")
        return False, "Error message"
```

2. Add to main():
```python
results['My Component'], details['My Component'] = check_my_new_component()
```

3. Add to email categories (optional):
```python
categories = {
    "My Category": ["My Component"],
    # ... existing categories
}
```

---

## 📈 Success Metrics

### Ideal State
- ✅ All 17 checks passing
- ✅ Email received daily
- ✅ No action items

### Acceptable State
- ⚠️ 1-3 checks failing
- ⚠️ Non-critical components affected
- ⚠️ Action items can wait until morning

### Critical State
- ❌ 4+ checks failing
- ❌ Critical components down (API, Database, ML predictions)
- ❌ Immediate action required

---

## 🔗 Related Documentation

- **ML System**: `COMPLETE_ML_SYSTEM_DOCS/00_README_START_HERE.md`
- **Player Props**: `COMPLETE_PLAYER_PROPS_SYSTEM_DOCS/00_README_START_HERE.md`
- **Cron Jobs**: `COMPLETE_ML_SYSTEM_DOCS/CRON_SCHEDULE_OVERVIEW.md`
- **Daily Email**: `COMPLETE_ML_SYSTEM_DOCS/DAILY_EMAIL_QUICK_REFERENCE.md`

---

## 📝 Version History

### Version 2.0 (Dec 4, 2025) - Current
- ✅ Comprehensive check of 24 components
- ✅ Organized by 7 categories
- ✅ Enhanced email reports with categories
- ✅ Checks all recent improvements (props, DFS, enhanced models)
- ✅ Production ready

### Version 1.0 (Nov 2025)
- Basic check of 6 components
- Simple email report
- Limited coverage

---

## 🆘 Support

### If All Systems Failing

1. **Check VPS connectivity**: `ping 148.230.87.135`
2. **Check API server**: `ssh root@148.230.87.135 "ps aux | grep uvicorn"`
3. **Check database**: `ssh root@148.230.87.135 "ls -lah /root/sporttrader/backend/ml/predictions.db"`
4. **Review logs**: `ssh root@148.230.87.135 "tail -100 /root/sporttrader/backend/logs/systems_check.log"`

### If Specific Component Failing

See component-specific troubleshooting in the "What Gets Checked in Detail" section above.

### Emergency Contacts

- System Owner: Check ADMIN_EMAIL in .env
- VPS Access: `ssh root@148.230.87.135`
- Documentation: This file + COMPLETE_ML_SYSTEM_DOCS/

---

**Last Updated**: December 4, 2025
**Script Version**: 2.0
**Status**: ✅ DEPLOYED & OPERATIONAL
