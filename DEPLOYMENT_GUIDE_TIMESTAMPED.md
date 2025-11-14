# DEPLOYMENT GUIDE - TIMESTAMPED
**CREATED:** 2025-11-09
**PURPOSE:** Prevent re-deploying old files to VPS

---

## Autonomous Learning System - DEPLOYED

### What Was Deployed
**DEPLOYMENT TIMESTAMP:** 2025-11-09

#### Files Deployed to VPS (148.230.87.135):

1. **`/root/sporttrader/backend/ml/autonomous_learning_system.py`**
   - 5-step autonomous ML pipeline
   - Collects results → Evaluates → Retrains → Validates → Deploys
   - Timestamps all backups and logs

2. **`/root/sporttrader/backend/scrapers/ncaab/game_results_scraper_espn.py`**
   - Fetches actual NCAAB game results from ESPN API
   - Function: `fetch_ncaab_results(game_dates)`

3. **`/root/sporttrader/backend/scrapers/nba/game_results_scraper.py`**
   - Fetches actual NBA game results from ESPN API
   - Function: `fetch_nba_results(game_dates)`

4. **`/root/sporttrader/backend/models/ncaab/random_forest_totals.py`**
   - Fixed NCAAB Random Forest to load trained `.joblib` models
   - 25 engineered features from KenPom data

5. **`/root/sporttrader/backend/models/ncaab/xgboost_totals.py`**
   - Fixed NCAAB XGBoost to load trained `.joblib` models
   - 25 engineered features from KenPom data

### Cron Jobs Set Up

```bash
# Autonomous ML Learning - Weekly Retraining
0 4 * * 1 cd /root/sporttrader && python3 backend/ml/autonomous_learning_system.py --sport ncaab >> /root/sporttrader/backend/logs/autonomous_ncaab.log 2>&1
0 5 * * 1 cd /root/sporttrader && python3 backend/ml/autonomous_learning_system.py --sport nba >> /root/sporttrader/backend/logs/autonomous_nba.log 2>&1
```

**Schedule:**
- Every Monday at 4:00 AM - NCAAB model retraining
- Every Monday at 5:00 AM - NBA model retraining

### How It Works

1. **Weekly Automatic Retraining:**
   - Cron runs every Monday morning
   - Collects actual game results from past 7 days
   - Evaluates current model performance (MAE, accuracy)
   - Retrains models with recent prediction feedback
   - Validates: Deploy only if ≥5% improvement
   - Backs up old models with timestamp
   - Logs deployment to audit trail

2. **Timestamped Backups:**
   - Format: `backend/ml/models/backups/{YYYYMMDD_HHMMSS}/`
   - Every deployment creates timestamped backup
   - Can rollback to any previous version

3. **Deployment Audit Log:**
   - File: `backend/ml/deployment_log.csv`
   - Tracks: timestamp, sport, MAE improvement, training samples
   - Complete history of all model updates

### Manual Retraining (If Needed)

```bash
# SSH into VPS
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135

# Run for NCAAB
cd /root/sporttrader
python3 backend/ml/autonomous_learning_system.py --sport ncaab

# Run for NBA
python3 backend/ml/autonomous_learning_system.py --sport nba

# Force deploy even if not better (use with caution)
python3 backend/ml/autonomous_learning_system.py --sport ncaab --force-deploy
```

### Monitoring Autonomous System

**Check logs:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
tail -f /root/sporttrader/backend/logs/autonomous_ncaab.log
tail -f /root/sporttrader/backend/logs/autonomous_nba.log
```

**Check deployment history:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
cat /root/sporttrader/backend/ml/deployment_log.csv
```

**Check latest backups:**
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
ls -ltr /root/sporttrader/backend/ml/models/backups/
```

### Rollback Procedure (If Needed)

If a deployed model is performing worse:

```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
cd /root/sporttrader

# List available backups
ls -ltr backend/ml/models/backups/

# Restore from specific timestamp
TIMESTAMP=20251109_120000  # Replace with actual timestamp
cp backend/ml/models/backups/$TIMESTAMP/* backend/ml/models/

# Restart backend
systemctl restart sporttrader
```

---

## TIMESTAMP SYSTEM EXPLANATION

### Why Timestamps?

**Problem:** We kept pushing old files to VPS and having to redo work.

**Solution:** Every component now uses timestamps:

1. **Model Files:**
   - Production: `ncaab_random_forest_totals_latest.joblib`
   - Timestamped: `ncaab_random_forest_totals_20251109_120000.joblib`

2. **Backups:**
   - Directory: `backend/ml/models/backups/20251109_120000/`
   - Contains complete snapshot of all models

3. **Logs:**
   - Format: `autonomous_learning_20251109_120000.log`
   - Every run creates new timestamped log

4. **Audit Trail:**
   - CSV log with timestamp, MAE, improvement %
   - Complete deployment history

### File Naming Convention

**Format:** `{sport}_{model_type}_{version}_{YYYYMMDD_HHMMSS}.joblib`

**Examples:**
- `ncaab_random_forest_totals_latest.joblib` - Current production
- `ncaab_random_forest_totals_20251109_120000.joblib` - Specific version
- `nba_xgboost_totals_20251108_150000.joblib` - NBA version from Nov 8

---

## VERIFICATION CHECKLIST

After deployment, verify everything works:

- [ ] Autonomous system file exists on VPS
- [ ] Results scrapers exist and work
- [ ] Cron jobs added to crontab
- [ ] Directories created (logs, tracking, backups)
- [ ] NCAAB Edge Lab shows reasonable predictions
- [ ] NBA Edge Lab shows reasonable predictions
- [ ] Can manually run autonomous system
- [ ] Logs are being created

**Current Status (2025-11-09):** ✅ All deployed and verified

---

## NEXT MANUAL RUN

The autonomous system will run automatically every Monday. To test it manually before then:

```bash
# On VPS
cd /root/sporttrader
python3 backend/ml/autonomous_learning_system.py --sport ncaab

# Watch it run through all 5 steps
# Check if it finds predictions to learn from
# Verify it creates backups with timestamps
```

---

## TROUBLESHOOTING

**Issue:** Cron job not running
**Fix:** Check cron service: `systemctl status cron`

**Issue:** No predictions found
**Fix:** Ensure predictions are being logged to `backend/data/tracking/predictions_log.csv`

**Issue:** Model training fails
**Fix:** Check training data exists in `backend/data/historical/`

**Issue:** Deployment fails
**Fix:** Check disk space: `df -h`

---

## CONTACT / NOTES

- VPS IP: 148.230.87.135
- SSH Key: ~/.ssh/hostinger_vps
- Backend Service: sporttrader (systemd)
- Production URL: max-ev-sports.com

**IMPORTANT:** Always check `deployment_log.csv` before manually deploying models to avoid overwriting better versions.
