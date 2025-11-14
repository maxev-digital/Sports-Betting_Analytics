# Player Props ML System - Backup Quick Reference

## 🔄 How to Backup

### One-Click Backup (Easiest)
```
Double-click: C:\Users\nashr\BACKUP_PROPS.bat
```

### Command Line
```bash
python backup_props_data.py
```

---

## 📁 Backup Location

**D:\backend\**

- `/data/` - Database backups
- `/roadmap/` - Documentation
- `/scrapers/` - Data collection scripts
- `/models/` - ML models (when trained)

---

## ⏰ When to Backup

| Situation | Frequency |
|-----------|-----------|
| Data collection active | Daily |
| Development work | After major changes |
| Before deployment | Always |
| After model training | Immediately |
| Routine maintenance | Weekly minimum |

---

## 🎯 Critical Data

**MOST IMPORTANT:** `player_props.db`
- Contains ALL historical props data
- Required for ML model training
- Cannot be recreated if lost!

**Size:** ~77 KB empty → ~20 MB after 3 months

---

## ✅ Quick Check

After backup, verify:
1. Backup script shows "[OK]" messages
2. D:\backend\data\player_props.db exists
3. Timestamped backup created
4. File size > 0 bytes

---

## 🚨 Recovery

If data lost on C: drive:
```bash
copy "D:\backend\data\player_props.db" "C:\Users\nashr\backend\data\"
```

---

## 📊 Data Collection Progress

**Goal:** 1,000+ props outcomes
**Timeline:** 30-60 days

Check progress: Run backup script (shows record counts)

---

## 🔗 Related Files

- Backup script: `C:\Users\nashr\backup_props_data.py`
- Batch file: `C:\Users\nashr\BACKUP_PROPS.bat`
- Full README: `D:\backend\README_BACKUP.md`
- Implementation plan: `D:\backend\roadmap\PLAYER_PROPS_ML_IMPLEMENTATION_PLAN.md`

---

**REMEMBER:** Backup = Insurance against data loss!
Run it daily during data collection phase.
