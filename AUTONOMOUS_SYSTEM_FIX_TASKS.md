# AUTONOMOUS SYSTEM FIX - TASK LIST
**Date:** 2025-11-12
**Goal:** Fix autonomous ML system, commit to git, deploy to VPS, backfill results

---

## ✅ COMPLETED (Just Now)

- [x] Deploy `model_performance.py` route to VPS
- [x] Deploy `run_daily_predictions.py` to VPS
- [x] Deploy `run_ncaab_predictions.py` to VPS
- [x] Fix datetime import error in `game_tracker.py`
- [x] Restart backend service on VPS
- [x] Verify prediction generation works (151 predictions across 5 sports)
- [x] Verify model performance API endpoint works

---

## 🔴 TODO TODAY

### PHASE 1: Commit All Fixes to Git (30 min)
- [ ] **Task 1.1:** Stage all modified files locally
  - `backend/routes/model_performance.py`
  - `backend/game_tracker.py` (datetime import fix)
  - `run_daily_predictions.py`
  - `run_ncaab_predictions.py`
  - Any other modified files

- [ ] **Task 1.2:** Create comprehensive git commit
  ```bash
  git add backend/routes/model_performance.py
  git add backend/game_tracker.py
  git add run_daily_predictions.py
  git add run_ncaab_predictions.py
  git commit -m "Fix autonomous ML system - deploy missing routes and prediction runners

  - Add model_performance.py API route for performance tracking
  - Fix datetime import in game_tracker.py (Max EV Boost crashes)
  - Add run_daily_predictions.py for NBA workflow
  - Add run_ncaab_predictions.py for NCAAB workflow
  - Cron jobs now have correct scripts to run
  - Model performance page now loads data

  🤖 Generated with Claude Code
  Co-Authored-By: Claude <noreply@anthropic.com>"
  ```

- [ ] **Task 1.3:** Push to GitHub
  ```bash
  git push origin main
  ```

- [ ] **Task 1.4:** Pull changes on VPS to ensure git sync
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader && git pull origin main"
  ```

---

### PHASE 2: Create Results Backfill Script (45 min)

- [ ] **Task 2.1:** Create `backend/backfill_results.py` script
  - Fetch final scores for completed games
  - Match predictions to actual results
  - Calculate WIN/LOSS/PUSH for each prediction
  - Calculate profit/loss (assuming 1 unit bets at -110 odds)
  - Log results to `data/tracking/results_log.csv`

- [ ] **Task 2.2:** Script Requirements:
  - Process all 2,426 existing predictions
  - Use The Odds API or ESPN API to get final scores
  - Handle date parsing (predictions from Oct 9 - Nov 12)
  - Error handling for games not yet completed
  - Logging/progress output

- [ ] **Task 2.3:** Test script locally
  ```bash
  cd backend
  python backfill_results.py --sport nba --days 30
  ```

- [ ] **Task 2.4:** Verify results_log.csv is populated
  ```bash
  wc -l backend/data/tracking/results_log.csv
  tail -20 backend/data/tracking/results_log.csv
  ```

---

### PHASE 3: Deploy Results Script to VPS (15 min)

- [ ] **Task 3.1:** Add backfill script to git
  ```bash
  git add backend/backfill_results.py
  git commit -m "Add results backfill script for historical predictions"
  git push
  ```

- [ ] **Task 3.2:** Pull on VPS
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader && git pull"
  ```

- [ ] **Task 3.3:** Run backfill script on VPS
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader/backend && source venv/bin/activate && python backfill_results.py"
  ```

- [ ] **Task 3.4:** Verify results on VPS
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "wc -l /root/sporttrader/backend/data/tracking/results_log.csv"
  ```

---

### PHASE 4: Verify Model Performance Page (10 min)

- [ ] **Task 4.1:** Test API endpoint shows data
  ```bash
  curl -s https://max-ev-sports.com/api/model-performance/overview | python -m json.tool
  ```

- [ ] **Task 4.2:** Open browser and check Model Performance page
  - Navigate to: https://max-ev-sports.com/analytics (or wherever the page is)
  - Verify win rate, ROI, and performance by sport/model appear
  - Take screenshot if successful

- [ ] **Task 4.3:** Check performance breakdown
  ```bash
  curl -s https://max-ev-sports.com/api/model-performance/overview?sport=nba
  curl -s https://max-ev-sports.com/api/model-performance/history?days=30
  ```

---

### PHASE 5: Set Up Automatic Result Recording (30 min)

- [ ] **Task 5.1:** Create `backend/record_daily_results.py` script
  - Run daily (via cron at midnight)
  - Fetch yesterday's game scores
  - Match to predictions
  - Log results automatically

- [ ] **Task 5.2:** Add to cron
  ```bash
  # Add to crontab on VPS:
  0 1 * * * cd /root/sporttrader/backend && source venv/bin/activate && python record_daily_results.py >> logs/results_recorder.log 2>&1
  ```

- [ ] **Task 5.3:** Test manual run
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader/backend && source venv/bin/activate && python record_daily_results.py"
  ```

- [ ] **Task 5.4:** Commit to git
  ```bash
  git add backend/record_daily_results.py
  git commit -m "Add automatic daily result recording"
  git push
  ```

---

### PHASE 6: Verify Full Autonomous System (20 min)

- [ ] **Task 6.1:** Check all cron jobs are configured
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "crontab -l"
  ```

- [ ] **Task 6.2:** Verify daily prediction crons
  - ✅ 10am CST - NBA predictions
  - ✅ 11am CST - NCAAB predictions
  - ✅ Other sports as needed

- [ ] **Task 6.3:** Verify weekly training crons
  - ✅ Monday 4am - NCAAB training
  - ✅ Monday 5am - NBA training
  - ✅ Monday 6am - NHL training
  - ✅ Monday 6am - Monte Carlo training
  - ✅ Monday 8am - Regression training

- [ ] **Task 6.4:** Verify result recording cron
  - ✅ Daily 1am - Record previous day results

- [ ] **Task 6.5:** Check log files exist and are writable
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "ls -lh /root/sporttrader/backend/logs/"
  ```

---

### PHASE 7: Create System Documentation (15 min)

- [ ] **Task 7.1:** Update `ML_AUTONOMOUS_SYSTEM_REFERENCE.md`
  - Add today's fixes
  - Document result backfill process
  - Update troubleshooting section

- [ ] **Task 7.2:** Create quick reference card
  - How to check system status
  - How to manually trigger predictions
  - How to view logs
  - How to backfill results

- [ ] **Task 7.3:** Commit documentation
  ```bash
  git add ML_AUTONOMOUS_SYSTEM_REFERENCE.md
  git commit -m "Update autonomous system docs with fixes and result recording"
  git push
  ```

---

### PHASE 8: Final Verification & Testing (20 min)

- [ ] **Task 8.1:** Restart backend service with all changes
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader && systemctl status sporttrader"
  ```

- [ ] **Task 8.2:** Check for errors in logs
  ```bash
  ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "journalctl -u sporttrader -n 50 --no-pager"
  ```

- [ ] **Task 8.3:** Verify all API endpoints work
  - `/api/model-performance/overview` ✅
  - `/api/model-performance/history` ✅
  - `/api/model-performance/models` ✅

- [ ] **Task 8.4:** Test frontend page loads without errors
  - Open Model Performance page
  - Check browser console for errors
  - Verify data displays correctly

- [ ] **Task 8.5:** Create final system health check script
  - `backend/check_system_health.py`
  - Checks cron jobs, logs, API endpoints, data files
  - Run it and save output

---

## 📊 SUCCESS CRITERIA

At the end of today, you should have:

1. ✅ All fixes committed to git (main branch)
2. ✅ VPS fully synced with git repo
3. ✅ 2,426 predictions matched with actual results
4. ✅ Model Performance page showing real data
5. ✅ Automatic daily result recording set up
6. ✅ Cron jobs verified and running
7. ✅ No errors in backend logs
8. ✅ Documentation updated
9. ✅ System health check script created

---

## 🚨 ROLLBACK PLAN (If Something Breaks)

If deployment causes issues:

```bash
# Rollback git
git reset --hard HEAD~1

# Restart backend on VPS
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "cd /root/sporttrader && git reset --hard HEAD~1 && systemctl restart sporttrader"
```

---

## 📝 NOTES

- Current predictions: 2,426 (from Oct 9 - Nov 12)
- Current results: 0 (need to backfill)
- Sports covered: NBA, NCAAB, NHL, NFL, NCAAF
- Models per sport: 5 (ensemble, xgboost, random_forest, lightgbm, linear_regression)
- Total models: 25 (5 sports × 5 models)

---

## ⏰ TIME ESTIMATES

- Phase 1: 30 min (git commits)
- Phase 2: 45 min (create backfill script)
- Phase 3: 15 min (deploy to VPS)
- Phase 4: 10 min (verify UI)
- Phase 5: 30 min (automatic result recording)
- Phase 6: 20 min (verify crons)
- Phase 7: 15 min (documentation)
- Phase 8: 20 min (final testing)

**Total: ~3 hours**

---

## 🎯 START HERE

Begin with Phase 1, Task 1.1. Check off each task as you complete it.
