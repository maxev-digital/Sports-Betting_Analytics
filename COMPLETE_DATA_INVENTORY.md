# COMPLETE DATA INVENTORY - ALL 5 SPORTS

**Date**: December 1, 2025
**Status**: ✅ ALL SPORTS HAVE TRAINING DATA

---

## DATA SUMMARY BY SPORT

| Sport  | Games | Features | Data Quality | Status |
|--------|-------|----------|--------------|--------|
| NBA    | 3,690 | 66       | ✅ Real historical | READY |
| NCAAB  | 16,338| TBD      | ✅ Real historical | Need to fix loader |
| NHL    | 1,000 | 32       | ⚠️  Sample data   | READY (upgrade later) |
| NFL    | 816   | 34       | ⚠️  Sample data   | READY (upgrade later) |
| NCAAF  | 1,500 | 36       | ⚠️  Sample data   | READY (upgrade later) |

**TOTAL**: 23,344 games across all sports

---

## DETAILED BREAKDOWN

### ✅ NBA - EXCELLENT DATA
**File**: `/data/historical/nba/nba_historical_latest.csv`
**Records**: 3,690 games
**Features**: 66 columns

**Key Features Include**:
- Team stats: PPG, opponent PPG, point differential
- Shooting: FG%, 3PT%, FT%
- Advanced: rebounds, assists, turnovers, steals, blocks
- Momentum: last 5/10 game PPG, last 5/10 wins
- Efficiency: pace, offensive rating, defensive rating
- Differentials: win%, PPG diff, turnover diff, etc.
- Targets: actual_total, home_score, away_score, home_margin

**Data Loader**: ✅ Works perfectly
**Feature Engineer**: ✅ Produces 32 features from 66 available
**Ready to Train**: YES

---

### ✅ NCAAB - EXCELLENT DATA (NEEDS LOADER FIX)
**Files**:
- `/data/historical/ncaab/games_2023.csv` - 5,446 games
- `/data/historical/ncaab/games_2024.csv` - 5,431 games
- `/data/historical/ncaab/games_2025.csv` - 5,461 games

**Total Records**: 16,338 games
**KenPom Integration**: Daily scraper running (latest: Nov 28)

**KenPom Features**:
- AdjO (Adjusted Offensive Efficiency)
- AdjD (Adjusted Defensive Efficiency)
- AdjT (Adjusted Tempo/Pace)
- Strength of Schedule
- Team Rankings

**Data Loader**: ❌ Returns 0 games (needs fix)
**KenPom Scraper**: ✅ Working (daily updates)
**Ready to Train**: After fixing loader

---

### ⚠️ NHL - SAMPLE DATA (WORKING)
**File**: `/data/historical/nhl/sample_training_data.csv`
**Records**: 1,000 games
**Features**: 32 columns

**Key Features**:
- Goals per game (GPG)
- Goals against per game (GAPG)
- Shots per game
- Power play %, penalty kill %
- Save percentage
- Season, home/away indicators
- Targets: home_goals, away_goals, total_goals

**Data Loader**: ✅ Loads successfully
**Feature Engineer**: ✅ Works
**Ready to Train**: YES (can upgrade to real data later)

**Future Enhancement**:
- BallDontLie NHL API available
- Can scrape more historical data

---

### ⚠️ NFL - SAMPLE DATA (WORKING)
**File**: `/data/historical/nfl/sample_training_data.csv`
**Records**: 816 games
**Features**: 34 columns

**Key Features**:
- Season, week
- Home/away team stats
- Scores, totals
- TeamRankings metrics

**Data Loader**: ⚠️  Expects different filename
**TeamRankings Cache**: ✅ Available (Nov 30)
**Ready to Train**: YES (after minor loader fix)

**Future Enhancement**:
- ESPN FPI scraper available
- TeamRankings scraper ready
- Can expand to 3-5 seasons

---

### ⚠️ NCAAF - SAMPLE DATA (WORKING)
**File**: `/data/historical/ncaaf/sample_training_data.csv`
**Records**: 1,500 games
**Features**: 36 columns

**Key Features**:
- Conference data
- Week-by-week stats
- Home/away splits
- TeamRankings integration

**Data Loader**: ⚠️  Returns sample data
**TeamRankings Cache**: ✅ Available (Nov 22)
**Ready to Train**: YES

**Future Enhancement**:
- TeamRankings scraper ready
- Can expand to full historical seasons

---

## LIVE DATA SOURCES (For Predictions)

### BallDontLie API
- **NBA**: Team standings, win/loss records
- **NHL**: Team stats, standings
- **Note**: Does NOT provide season averages (pace, efficiency)

### KenPom (NCAAB)
- Daily scraper: ✅ WORKING
- Last run: Nov 28, 2025
- Provides: AdjO, AdjD, AdjT, rankings

### TeamRankings Cache
- **NBA**: 36K cache (Nov 30) - `/data/raw/nba/teamrankings_cache.json`
- **NFL**: Cache available
- **NCAAF**: Cache available (Nov 22)

### ESPN APIs
- Injuries scraper: Available
- NFL FPI: Available

---

## IMMEDIATE ACTION PLAN

### 1. Fix NCAAB Data Loader (5-10 min)
**Issue**: Returns 0 games despite having 16,338 game files

**Solution**: Update `ml/data_loaders/ncaab_data_loader.py` to:
- Read from `/data/historical/ncaab/games_*.csv`
- Combine 2023, 2024, 2025 seasons
- Integrate KenPom ratings from `/data/raw/ncaab/kenpom_ratings_*.csv`

### 2. Verify Feature Counts (5 min)
Run test to confirm each sport's feature engineer output:
```python
from ml.feature_engineering.nba_features import NBAFeatureEngineer
# Test with sample game data
# Confirm 32 features for totals
```

### 3. Retrain All 5 Sports (30-60 min)
Using `TRAIN_NOW.sh` with corrected data loaders:

**Expected Feature Counts**:
- NBA: 66 features → 32 for totals model ✅
- NCAAB: ~40 features → 25-30 for totals model
- NHL: 32 features → fit to model
- NFL: 34 features → fit to model
- NCAAF: 36 features → fit to model

### 4. Models Will Train With Correct Dimensions
- XGBoost: Adapts to feature count
- LightGBM: Adapts to feature count
- Random Forest: Adapts to feature count
- Linear: Adapts to feature count
- **PyTorch TabularNet**: Need to pass `input_dim` parameter
- **CatBoost**: Adapts to feature count
- **Neural Ensemble**: Need to set `n_models=6`

---

## CRITICAL FIX NEEDED

### PyTorch TabularNet Architecture
**Current Issue**: Hardcoded to 78 features
```python
class TabularNet(nn.Module):
    def __init__(self, input_dim=78, ...):  # ❌ Hardcoded
```

**Fix**: Make dynamic
```python
class TabularNet(nn.Module):
    def __init__(self, input_dim, ...):  # ✅ Dynamic
```

This is in: `/root/sporttrader/backend/ml/pytorch_models/tabular_net.py`

---

## TRAINING COMMAND (After Fixes)

```bash
cd /mnt/c/Users/nashr/max-ev-sports
./TRAIN_NOW.sh
```

**Expected Output**:
- NBA: 7 models (XGB, LGB, RF, Linear, PyTorch, CatBoost, Ensemble)
- NCAAB: 7 models
- NHL: 7 models
- NFL: 7 models
- NCAAF: 7 models

**Total**: 35 models trained with REAL data dimensions

---

## VERIFICATION CHECKLIST

After retraining:

```bash
# Check model files exist
ssh root@148.230.87.135 "ls -lh /root/sporttrader/backend/ml/models/*totals_latest* | wc -l"
# Should show: 35 files (7 per sport × 5 sports)

# Check feature dimensions match
ssh root@148.230.87.135 "cd /root/sporttrader/backend && python3 -c '
import joblib
nba_model = joblib.load(\"ml/models/nba_xgboost_totals_latest.joblib\")
print(f\"NBA XGBoost expects: {nba_model.n_features_in_} features\")
'"
# Should match what feature engineer produces (32 for NBA)

# Test predictions
ssh root@148.230.87.135 "cd /root/sporttrader/backend && source venv/bin/activate && timeout 60 python3 run_enhanced_predictions_all_sports.py"
# Should generate predictions without dimension errors
```

---

## DATA QUALITY COMPARISON

### NBA (BEST)
- ✅ 3,690 real historical games
- ✅ 66 rich features
- ✅ Multiple seasons
- ✅ Pace, efficiency ratings, momentum
- **Grade**: A+

### NCAAB (BEST - after fix)
- ✅ 16,338 real games (largest dataset!)
- ✅ KenPom integration
- ✅ 3 full seasons
- **Grade**: A+

### NHL (GOOD)
- ⚠️  1,000 sample games
- ✅ 32 useful features
- ⚠️  Can expand with BallDontLie
- **Grade**: B

### NFL (GOOD)
- ⚠️  816 sample games
- ✅ TeamRankings integration ready
- ⚠️  Can expand significantly
- **Grade**: B

### NCAAF (GOOD)
- ⚠️  1,500 sample games
- ✅ Conference data
- ✅ TeamRankings ready
- **Grade**: B+

---

## NEXT STEPS (IN ORDER)

1. ✅ **DONE**: Identified all data sources
2. ⏳ **NOW**: Fix NCAAB data loader
3. ⏳ **THEN**: Fix PyTorch TabularNet input_dim
4. ⏳ **THEN**: Retrain all 5 sports with real data
5. ⏳ **FINALLY**: Test enhanced prediction system

**ETA**: 45-60 minutes total
