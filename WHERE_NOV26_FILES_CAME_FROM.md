# Where the November 26 Files Came From

## Answer: They Came From Git Commits on Nov 26, 2025

### The Timeline

**November 26, 2025**
- Multiple commits made to the repository with frontend updates
- Files modified and committed to git
- These commits are **ac135b3**, **af0c59e**, **b126cd6**, **447a8b0**, **ce7f922**, **beadbc7**

**November 29, 2025**
- VPS created a **BACKUP** in commit `dd46a72`
- Backup stored at: `/root/sporttrader/BACK UP MODEL Files/`
- This backup contains Nov 29 working versions of:
  - MaxEvEdges.tsx
  - ModelPerformance.tsx
  - PredictionsDatabase.tsx
  - ui_endpoints.py
  - model_performance.py

**December 3-4, 2025 (Local)**
- You made extensive improvements locally
- 12+ frontend files updated
- New features added (pricing page, cache buster, etc.)
- Committed to local git as commits: **f1d5e41**, **90d9d81**, **148cb61**

**December 4, 2025 - 3:09 PM CST (VPS Event)**
- Something touched these files on VPS at 15:09 (3:09 PM):
  - DfsCrusher.tsx
  - MaxEvEdges.tsx
  - ModelPerformance.tsx
  - Props.tsx
- BUT they were set to the Nov 26 versions from git

---

## Where November 26 Files Are Stored

### 1. In Git History (Primary Source)
The Nov 26 files live in git commits on the VPS:

```bash
VPS Git Repository: /root/sporttrader/.git
Commits from Nov 26:
  - ac135b3 "Fix Player Props Infrastructure"
  - af0c59e "Add TRENDS VIEW to GameCard"
  - b126cd6 "Resolve merge conflict"
  - 447a8b0 "Add enhanced My Betting Performance"
  - ce7f922 "Add Props Performance Dashboard"
  - beadbc7 "Add multi-sport filtering"
```

### 2. In the BACKUP Directory (Nov 29 versions)
A later backup exists on VPS:

```
/root/sporttrader/BACK UP MODEL Files/
├── frontend/src/pages/
│   ├── MaxEvEdges.tsx (Nov 29 version - NEWER than Nov 26)
│   ├── ModelPerformance.tsx (Nov 29 version)
│   └── PredictionsDatabase.tsx (Nov 29 version)
├── backend/routes/
│   ├── ui_endpoints.py (Nov 29 ENHANCED version)
│   └── model_performance.py (Nov 29 version)
└── docs/
    └── BACKUP_MANIFEST.md (explains Nov 29 Bulletproof Architecture)
```

**Note**: This backup is from Nov 29, NOT Nov 26. The Nov 29 versions are actually better than Nov 26.

### 3. Currently Deployed on VPS (Working Directory)

```
/root/sporttrader/frontend/src/pages/
```

Most files show **Nov 26, 14:26** timestamp, which corresponds to git commit `ac135b3`.

However, 4 files show **Dec 4, 15:09** timestamp:
- DfsCrusher.tsx
- MaxEvEdges.tsx
- ModelPerformance.tsx
- Props.tsx

These were recently touched but contain OLD content.

---

## What Happened on December 4 at 3:09 PM

Someone (likely Claude or a git operation) did one of these:

### Possibility 1: Git Reset
```bash
cd /root/sporttrader
git reset --hard <some-old-commit>
```

This would restore files to an old commit state.

### Possibility 2: Git Checkout
```bash
git checkout ac135b3 -- frontend/src/pages/*.tsx
```

This would selectively restore files from Nov 26 commit.

### Possibility 3: Merge/Pull Gone Wrong
```bash
git pull origin main
# Merge conflict occurred
# Old versions kept instead of new ones
```

### Possibility 4: File Copy from Git
```bash
git show ac135b3:frontend/src/pages/Props.tsx > frontend/src/pages/Props.tsx
```

This would manually extract files from old commit.

---

## The Evidence

### File Timestamps on VPS
```
Dec 4, 15:09 - DfsCrusher.tsx
Dec 4, 15:09 - MaxEvEdges.tsx
Dec 4, 15:09 - ModelPerformance.tsx
Dec 4, 15:09 - Props.tsx
Nov 29, 13:38 - PropsPerformance.tsx
Nov 29, 12:13 - PredictionsDatabase.tsx
Nov 28, 22:24 - Settings.tsx, Login.tsx, GoaliePull.tsx, ArticleDetail.tsx, Pricing.tsx
Nov 26, 14:26 - Most other files (Tools.tsx, Terms.tsx, etc.)
```

### Git Status on VPS
```
Current HEAD: dd46a72 (Nov 29, 2025)
Working directory: Has modified files (not committed)
```

The VPS git shows **modified** status for many files, meaning the working directory doesn't match the last commit (dd46a72 from Nov 29).

---

## Why These Files Were Deployed

### Theory: Git Operation During Dec 4 Sync
When you documented the Dec 4 sync in `COMPLETE_SYSTEM_SYNC_DEC_4_2025.md`, you were syncing FROM VPS TO Local.

At that time, VPS was already in this mixed state:
- Some files from Nov 26
- Some files from Nov 28
- Some files from Nov 29
- Modified working directory

Then at 3:09 PM on Dec 4, something triggered a git operation that touched 4 specific files and restored them to old versions.

---

## The Nov 26 Git Commits

### What Was in Those Commits

**ac135b3** (Nov 26) - "Fix Player Props Infrastructure"
- Modified: backend/routes/player_props.py
- Modified: backend/scrapers/props/results_tracker.py
- Modified: frontend/src/pages/PropsPerformance.tsx

**af0c59e** (Nov 26) - "Add TRENDS VIEW to GameCard"
- Modified: frontend/src/components/GameCard.tsx
- Added: NHL stats display improvements

**b126cd6** (Nov 26) - "Resolve merge conflict - use remote GameCard.tsx"
- Resolved merge conflict in GameCard.tsx

**447a8b0** (Nov 26) - "Add enhanced My Betting Performance analytics tab"
- Modified: frontend analytics components

**ce7f922** (Nov 26) - "Add Props Performance Dashboard aligned with ModelPerformance"
- Modified: frontend/src/pages/PropsPerformance.tsx

**beadbc7** (Nov 26) - "Add multi-sport filtering to player props endpoints"
- Modified: backend/routes/props endpoints

---

## Summary: Storage Locations

### ✅ Nov 26 Files Stored In:
1. **VPS Git Repository**: `/root/sporttrader/.git` (commits ac135b3 through beadbc7)
2. **VPS Working Directory**: `/root/sporttrader/frontend/src/pages/*.tsx` (current state)

### ✅ Nov 29 Files Stored In:
1. **VPS Git Repository**: `/root/sporttrader/.git` (commit dd46a72)
2. **VPS Backup Directory**: `/root/sporttrader/BACK UP MODEL Files/`

### ✅ Dec 3-4 Files Stored In:
1. **Your Local Machine**: `C:\Users\nashr\max-ev-sports\` (commits f1d5e41, 90d9d81, 148cb61)
2. **Your Local Git**: `C:\Users\nashr\max-ev-sports\.git`
3. **GitHub Origin** (if you pushed): `origin/main`

---

## Why VPS Doesn't Have Your Dec 3-4 Improvements

The VPS is currently on commit **dd46a72** (Nov 29), and you have **6 newer commits** locally:

```
Local:  148cb61 → 90d9d81 → f1d5e41 → 134a10e → beadbc7 → ce7f922 → [dd46a72]
                                                                           ↑
VPS:                                                                  [dd46a72]
```

Your Dec 3-4 improvements were never pushed to VPS (or to origin, or VPS never pulled them).

---

## The Fix

To get your Dec 3-4 improvements on VPS, you need to:

1. Push your local commits to origin (GitHub):
   ```bash
   git push origin main
   ```

2. Pull them on VPS:
   ```bash
   ssh root@148.230.87.135
   cd /root/sporttrader
   git fetch origin
   git reset --hard origin/main
   git pull origin main
   ```

3. Rebuild frontend on VPS:
   ```bash
   cd /root/sporttrader/frontend
   npm install
   npm run build
   ```

---

## Nov 26 Files - Exact Location Path

**Stored in Git Object Database:**
```
/root/sporttrader/.git/objects/
  └── (Git stores files as compressed blobs - not human readable)

Access via Git commands:
git show ac135b3:frontend/src/pages/Props.tsx
git show af0c59e:frontend/src/components/GameCard.tsx
```

**Currently Checked Out in Working Directory:**
```
/root/sporttrader/frontend/src/pages/
  ├── AdminDashboard.tsx (Nov 26, 14:26)
  ├── AlertPreferences.tsx (Nov 26, 14:26)
  ├── Alerts.tsx (Nov 26, 14:26)
  ├── Analytics.tsx (Nov 26, 14:26)
  └── [many more Nov 26 files...]
```

**In Nov 29 Backup (Better Versions):**
```
/root/sporttrader/BACK UP MODEL Files/frontend/src/pages/
  ├── MaxEvEdges.tsx (Nov 29 - includes Bulletproof Architecture)
  ├── ModelPerformance.tsx (Nov 29 - single API call)
  └── PredictionsDatabase.tsx (Nov 29 - ui/historical-predictions)
```

---

## Recommendation

**Don't restore Nov 26 files** - they're old.

**Don't restore Nov 29 files** - they're also old.

**Deploy your Dec 3-4 local files** - they have all the latest improvements!

---

**Document Created**: December 4, 2025, 3:15 PM CST
**Question Answered**: Where Nov 26 files were stored that got deployed
**Answer**: In VPS git repository commits from Nov 26, 2025
