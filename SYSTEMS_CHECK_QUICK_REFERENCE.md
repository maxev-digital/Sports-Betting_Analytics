# Comprehensive Systems Check - Quick Reference

**Daily at 11:00 PM CST** - Checks 24 components, sends email report

---

## 🚀 Quick Commands

```bash
# Deploy from local machine (Windows)
bash deploy_comprehensive_systems_check.sh

# Manual run on VPS
ssh root@148.230.87.135
cd /root/sporttrader/backend
python3 comprehensive_daily_systems_check.py

# View logs
tail -f /root/sporttrader/backend/logs/systems_check.log

# Check cron job
crontab -l | grep comprehensive
```

---

## ✅ 24 Components Checked

### 📡 Data Collection (4)
1. Odds Scrapers (7:00 AM)
2. Enhanced Scrapers (6:30 AM)
3. KenPom Scraper (7:30 AM) - CRITICAL for NCAAB
4. Props Stats Scrapers

### 🤖 ML Predictions (3)
5. Enhanced ML (7 models × 5 sports) - 8:05 AM
6. Player Props (NBA/NHL/NFL) - 10:30 AM
7. DFS Crusher - 11:00 AM

### 🧠 Model Health (2)
8. 35 Enhanced Models (7 per sport)
9. Feature Dimensions (NBA:60, NCAAB:14, NHL:27, NFL:30, NCAAF:30)

### 💾 Database (2)
10. predictions.db integrity
11. Database size

### ✅ Grading (2)
12. Prediction Grading (6:00 AM)
13. Props Grading (3:00 AM)

### 🌐 API (2)
14. FastAPI Servers (8000, 8888)
15. Critical Endpoints

### ⚙️ Resources (2)
16. Disk Space
17. Memory Usage

---

## 📧 Email Report

**To**: `$ADMIN_EMAIL` from .env (default: gte.apw@gmail.com)

**Subject Examples:**
- ✅ `Daily Systems Check: ALL OPERATIONAL`
- ⚠️ `Daily Systems Check: 2 Systems Need Attention`
- ❌ `Daily Systems Check: 5 SYSTEMS FAILING`

**Contains:**
- Executive summary (pass/fail counts)
- Component status by category
- Platform stats
- Action items (if failures)

---

## 🔍 Key Files

```
/root/sporttrader/backend/
├── comprehensive_daily_systems_check.py  # Main script
├── logs/
│   ├── systems_check.log                 # Check output
│   ├── ml_predictions_ENHANCED.log       # ML predictions
│   ├── cron_scraper.log                  # Odds scrapers
│   ├── kenpom_scraper.log                # KenPom
│   ├── dfs_crusher.log                   # DFS combos
│   ├── props_grading.log                 # Props grading
│   └── db_grading.log                    # Prediction grading
└── ml/
    └── predictions.db                     # Main database
```

---

## 🚨 Troubleshooting

### No Email Received
```bash
# Check API key
ssh root@148.230.87.135 "cat /root/sporttrader/backend/.env | grep BREVO_API_KEY"

# Check admin email
ssh root@148.230.87.135 "cat /root/sporttrader/backend/.env | grep ADMIN_EMAIL"

# Check email logs
ssh root@148.230.87.135 "grep -i 'email' /root/sporttrader/backend/logs/systems_check.log | tail -20"
```

### Component Failing
```bash
# View specific component logs
ssh root@148.230.87.135

# Data collection
tail -50 /root/sporttrader/backend/logs/cron_scraper.log
tail -50 /root/sporttrader/backend/logs/kenpom_scraper.log

# ML predictions
tail -100 /root/sporttrader/backend/logs/ml_predictions_ENHANCED.log

# Database
sqlite3 /root/sporttrader/backend/ml/predictions.db "SELECT COUNT(*) FROM predictions WHERE datetime(created_at) >= datetime('now', '-24 hours');"

# API
ps aux | grep uvicorn
curl http://localhost:8000/api/ui/best-plays
```

### Update Script
```bash
# From local machine
# 1. Edit comprehensive_daily_systems_check.py
# 2. Deploy
bash deploy_comprehensive_systems_check.sh
```

---

## 📊 Status Thresholds

**Overall Status:**
- ✅ Green: 0 failures
- ⚠️ Yellow: 1-3 failures
- ❌ Red: 4+ failures

**Disk Space:**
- ✅ > 10 GB free
- ⚠️ 5-10 GB free
- ❌ < 5 GB free

**Memory:**
- ✅ < 80% used
- ⚠️ 80-90% used
- ❌ > 90% used

---

## 🎯 Critical Components

**Must be operational:**
1. API Servers (port 8000)
2. Main Database (predictions.db)
3. Enhanced ML Predictions (8:05 AM)

**Should be operational:**
4. KenPom Scraper (affects NCAAB)
5. Player Props Predictions
6. Prediction Grading

**Nice to have:**
7. DFS Crusher
8. Test API (port 8888)
9. Enhanced scrapers

---

## 📅 Daily Timeline

```
03:00 AM - Props Grading
06:00 AM - Prediction Grading
06:30 AM - Enhanced Scrapers
07:00 AM - Odds Scrapers
07:30 AM - KenPom Scraper
08:05 AM - Enhanced ML Predictions (ALL SPORTS)
10:30 AM - Player Props Predictions
10:45 AM - Multi-Sport Props
11:00 AM - DFS Crusher
---
11:00 PM - COMPREHENSIVE SYSTEMS CHECK
          - Reviews all above
          - Sends email report
```

---

## 🔗 More Info

**Full Documentation**: `COMPREHENSIVE_SYSTEMS_CHECK_README.md`

**Related Docs**:
- ML System: `COMPLETE_ML_SYSTEM_DOCS/00_README_START_HERE.md`
- Player Props: `COMPLETE_PLAYER_PROPS_SYSTEM_DOCS/00_README_START_HERE.md`
- Cron Schedule: `COMPLETE_ML_SYSTEM_DOCS/CRON_SCHEDULE_OVERVIEW.md`

---

**Version**: 2.0 | **Status**: ✅ DEPLOYED | **Updated**: Dec 4, 2025
