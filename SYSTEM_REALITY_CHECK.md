# MAX EV SPORTS - REALITY CHECK & ACTION PLAN
**Date**: December 1, 2025
**Status**: CRITICAL GAPS BETWEEN ROADMAP & REALITY

---

## EXECUTIVE SUMMARY

### What You Asked For (Roadmap):
- ✅ 78+ features per sport (Rest, Travel, Clutch, Injuries, etc.)
- ✅ 7 model types (XGBoost, LightGBM, RF, Linear, **PyTorch TabularNet**, **TFT**, **CatBoost**)
- ✅ Neural ensemble weighter that learns optimal model weights
- ✅ 87+ total models across all sports

### What's Actually Built (Current):
- ❌ 42 features per sport (Pace, Offense, Defense, Shooting, Momentum, Win Quality, Box Score)
- ❌ 4 model types (XGBoost, LightGBM, Random Forest, Linear/Logistic)
- ❌ Simple median ensemble (no neural weighting)
- ✅ 87 trained models (but simpler architecture)

### Frontend Pages Status:
| Page | Data Source | Working? | Issue |
|------|-------------|----------|-------|
| **Max EV Edges** | Port 8000 `/api/ui/best-plays` | ⚠️ YES | Showing NCAAF predictions with -34% edges (predicting 35 vs market 55) |
| **Model Performance** | Port 8000 `/api/ui/model-performance` | ✅ YES | Displaying NBA/NCAAB stats correctly |
| **Predictions Database** | Port 8000 `/api/ui/historical-predictions` | ✅ YES | 10,924 predictions in database |

---

## THE REAL PROBLEM: NCAAF/NFL PREDICTIONS ARE BROKEN

### Evidence from Live Database (Dec 1, 2025):

```sql
Sport    | Predictions | Avg Edge  | Status
---------|-------------|-----------|--------
NBA      | 1,200       | -1.03%    | ✅ Reasonable
NCAAB    | 6,155       | +10.75%   | ✅ Working well
NCAAF    | 2,273       | -18.41%   | ❌ BROKEN
NFL      | 1,026       | -33.35%   | ❌ BROKEN
NHL      | 1,270       | +16.45%   | ⚠️ Old data (last: Nov 29)
```

### Why NCAAF/NFL Are Broken:

**Example**: NCAAF game today
- **Market Total**: 55.0 points
- **Model Prediction**: 35.0 points
- **Edge**: -36% (model says UNDER by 20 points!)
- **Problem**: Model is predicting college basketball scores for college football

**Root Cause**: Feature mismatch in training vs prediction

#### What Happened:
1. **Training Time** (weeks ago):
   - Model trained on games with features: `home_ppg`, `away_ppg`, `home_points_allowed`, etc.
   - Training data had realistic values (NFL: 24 PPG, NCAAF: 28 PPG)

2. **Prediction Time** (today):
   - `run_ml_predictions_all_sports_v2.py` tries to load TeamRankings cache
   - Feature mapping is incorrect:
     - Model expects: `home_points_allowed`
     - Script provides: `home_points_allowed_per_game`
   - **OR** the values are from wrong sport (basketball stats for football)

#### Visual Proof:
```
NCAAF Predictions Today (from curl):
┌───────────────────────────┬────────┬──────────┬─────────┐
│ Game                      │ Market │ Model    │ Edge    │
├───────────────────────────┼────────┼──────────┼─────────┤
│ Jacksonville St vs Kennesaw│ 55.0   │ 35.0     │ -36.4%  │
│ Western Michigan vs Miami  │ 55.0   │ 35.0     │ -36.4%  │
│ Navy vs Army              │ 55.0   │ 35.0     │ -36.4%  │
│ James Madison vs Troy     │ 55.0   │ 36.0     │ -34.5%  │
└───────────────────────────┴────────┴──────────┴─────────┘
```

**EVERY game predicts ~35 points** = Model is broken, outputting constant values

---

## WHAT'S ON THE VPS RIGHT NOW

### Database: `/root/sporttrader/backend/ml/predictions.db`
```bash
Total Predictions: 10,924
- NBA: 1,200 (working)
- NCAAB: 6,155 (working)
- NCAAF: 2,273 (broken - all UNDER at 35 pts)
- NFL: 1,026 (broken - all UNDER at 30 pts)
- NHL: 1,270 (stale - last update Nov 29)
```

### Models Directory: `/root/sporttrader/backend/ml/models/`
```bash
Total Files: 87 .joblib files
Per Sport: 15-20 models each (xgboost, lightgbm, random_forest x 3 bet types)

Example NFL Models:
- nfl_xgboost_totals_latest.joblib
- nfl_lightgbm_totals_latest.joblib
- nfl_random_forest_totals_latest.joblib
- nfl_totals_metadata_latest.joblib ← Contains expected feature names
```

### Feature Engineers: `/root/sporttrader/backend/ml/feature_engineering/`
```bash
- nba_features.py      ✅ Working (Official NBA API)
- ncaab_features.py    ✅ Working (KenPom data)
- nfl_features.py      ❌ Mismatch with models
- ncaaf_features.py    ❌ Mismatch with models
- nhl_features.py      ⚠️ No stats source configured
```

### Prediction Scripts:
```bash
1. run_ml_predictions_all_sports.py       (Current cron job - broken)
2. run_ml_predictions_all_sports_v2.py    (Enhanced - still broken)
3. run_ml_predictions_to_db.py            (Legacy)
```

### Cron Jobs:
```bash
# 7:00 AM - Scrape data
0 7 * * * python3 backend/run_all_scrapers.py

# 8:00 AM - Generate predictions (CURRENTLY RUNNING BROKEN SCRIPT)
0 8 * * * python3 backend/run_ml_predictions_all_sports.py

# Weekly model retraining (Mondays 4-5 AM)
0 4 * * 1 python3 ml/autonomous_learning_system.py --sport ncaab
0 5 * * 1 python3 ml/autonomous_learning_system.py --sport nba
0 5 * * 1 python3 ml/autonomous_learning_system.py --sport nfl
```

---

## ROADMAP vs REALITY BREAKDOWN

### PHASE 1: Foundation (Roadmap - NOT DONE)
❌ PyTorch NOT installed on VPS
❌ CatBoost NOT installed on VPS
❌ `pytorch_models/` directory exists but EMPTY
❌ `enhanced_features/` directory exists but EMPTY

### PHASE 2: Enhanced Features (Roadmap - NOT DONE)
Current features: **42 per sport**
- ✅ Pace (4), Offense (6), Defense (6), Shooting (6)
- ✅ Momentum (8), Win Quality (8), Box Score (4)

Roadmap features (NOT implemented): **+36 more**
- ❌ Rest & Fatigue (6)
- ❌ Travel (4)
- ❌ Clutch Performance (4)
- ❌ Injury Impact (6)
- ❌ Lineup Continuity (4)
- ❌ Head-to-Head (4)
- ❌ Referee Tendencies (4)
- ❌ Shot Quality / Advanced (4)

### PHASE 3: PyTorch Models (Roadmap - NOT DONE)
❌ Tabular Neural Network
❌ Temporal Fusion Transformer (TFT)
❌ CatBoost wrapper

**Current models**: XGBoost, LightGBM, Random Forest, Linear/Logistic (4 types)

### PHASE 4: Neural Ensemble (Roadmap - NOT DONE)
❌ Ensemble weighter neural network
❌ Weekly weight updates

**Current ensemble**: Simple median of 3 models (not learned)

### PHASE 5: Integration (Roadmap - NOT DONE)
❌ No `USE_ENHANCED_78_FEATURE_PIPELINE` flag
❌ No `USE_NEURAL_ENSEMBLE` flag
❌ No `PYTORCH_MODELS_ENABLED` flag

**Current integration**: Basic scikit-learn models only

### PHASE 6: Testing & Validation (Roadmap - NOT DONE)
❌ No backtesting scripts
❌ No A/B testing
❌ No model drift monitoring

---

## FRONTEND PAGES - WHAT THEY ACTUALLY SHOW

### 1. Max EV Edges (`/#/max-ev-edges`)

**What it's supposed to show**: Today's best betting opportunities with +EV edges

**What it actually shows**:
- ❌ NCAAF games predicting 35 points (all UNDER by 20 pts)
- ❌ NFL games predicting 30 points (all UNDER by 15 pts)
- ✅ NBA/NCAAB predictions are reasonable
- ⚠️ Page calls `/api/ui/best-plays` on port 8000 (correct)

**API Endpoint**: `http://148.230.87.135:8000/api/ui/best-plays`
- ✅ Returns JSON with predictions
- ❌ Data is garbage for NCAAF/NFL

**User sees**:
```
NCAAF - Army @ Navy
Market Total: 55.0
Model Prediction: 35.0
Recommendation: UNDER
Edge: -36.4% ← TERRIBLE!
```

### 2. Model Performance (`/#/model-performance`)

**What it's supposed to show**: Win rates, ROI, profit/loss by model & sport

**What it actually shows**:
- ✅ Summary cards (Win Rate, ROI, P&L, etc.)
- ✅ Charts (Win Rate Over Time, ROI Over Time, Units Won)
- ✅ Performance by Model, Confidence, Sport
- ✅ Bankroll tracking, Kelly Criterion, Break-even calculator

**API Endpoint**: `http://148.230.87.135:8000/api/ui/model-performance`
- ✅ Works correctly
- ✅ Shows real stats from predictions.db

**User sees**:
```
NBA Last 30 Days:
- Win Rate: 51.2%
- ROI: +2.3%
- Profit: +$127 (at $100/bet)
```

### 3. Predictions Database (`/#/predictions-database`)

**What it's supposed to show**: Historical predictions with results

**What it actually shows**:
- ✅ Table with all predictions
- ✅ Filters (sport, date, result)
- ✅ Results tracking (WIN/LOSS/PENDING)
- ✅ P&L calculations

**API Endpoint**: `http://148.230.87.135:8000/api/ui/historical-predictions`
- ✅ Works correctly
- ✅ Returns 10,924 predictions from database

---

## THE BIG CONFUSION: PORT 8000 vs PORT 8888

### Port 8000 (Main FastAPI - Predictions.db)
**Purpose**: ML model predictions, historical data, performance tracking

**Endpoints**:
- `/api/ui/best-plays` ← Max EV Edges page uses this
- `/api/ui/model-performance` ← Model Performance page uses this
- `/api/ui/historical-predictions` ← Predictions Database uses this
- `/api/games` ← Game schedule with team stats

**Database**: `/root/sporttrader/backend/ml/predictions.db`

### Port 8888 (Edge Scanner - Odds API)
**Purpose**: Real-time odds arbitrage, line shopping, +EV finder

**Endpoints**:
- `/api/best-plays` ← Different from port 8000!
- `/api/available-sports`
- `/api/odds-comparison`

**Data Source**: Live odds from The Odds API

### The Confusion:
Your **Max EV Edges page** is calling port 8000 (`/api/ui/best-plays`), which returns ML model predictions from predictions.db. But the page name "Max EV Edges" suggests it should show edge scanner data from port 8888.

**Two options**:
1. Keep page as-is (ML predictions) and rename to "Model Predictions"
2. Change page to call port 8888 edge scanner (actual max-EV odds plays)

---

## ACTION PLAN TO FIX EVERYTHING

### IMMEDIATE (This Week) - Fix Broken Predictions

#### Priority 1: Fix NCAAF/NFL Feature Mapping ⚠️ CRITICAL
**Problem**: Models predict 30-35 points for all games (constant values)

**Solution Steps**:
1. Load NFL model metadata: `nfl_totals_metadata_latest.joblib`
2. Print expected feature names
3. Compare with what `nfl_features.py` is outputting
4. Fix the feature engineer to match EXACTLY

**Files to fix**:
- `backend/ml/feature_engineering/nfl_features.py`
- `backend/ml/feature_engineering/ncaaf_features.py`

**Test**:
```bash
ssh root@148.230.87.135
cd /root/sporttrader/backend
python3 -c "
import joblib
metadata = joblib.load('ml/models/nfl_totals_metadata_latest.joblib')
print('Expected features:', metadata.get('feature_names', []))
"
```

Then run prediction script manually and verify totals are 40-50 (not 30).

#### Priority 2: Configure NHL Stats Source
**Problem**: No NHL predictions since Nov 29

**Options**:
- MoneyPuck (data exists in `data/raw/nhl/moneypuck/`)
- MoreHockeyStats (mentioned in docs)
- NHL Official API

**Solution**:
1. Verify MoneyPuck scraper is running
2. Update `nhl_features.py` to load MoneyPuck stats
3. Test NHL predictions

#### Priority 3: Update Cron Job
**Problem**: Running broken script daily

**Fix**:
```bash
# Change cron from:
0 8 * * * python3 run_ml_predictions_all_sports.py

# To (once v2 is fixed):
0 8 * * * python3 run_ml_predictions_all_sports_v2.py
```

---

### SHORT TERM (Next 2 Weeks) - Retrain Models

#### Option A: Quick Fix - Retrain with Current Features
**Effort**: 1-2 days
**Result**: Models work with current 42-feature system

```bash
# Retrain all sports
ssh root@148.230.87.135
cd /root/sporttrader/backend/ml
python3 autonomous_learning_system.py --sport nfl --force
python3 autonomous_learning_system.py --sport ncaaf --force
```

#### Option B: Implement Enhanced Features (Partial Roadmap)
**Effort**: 1-2 weeks
**Result**: Add some easy wins (Rest & Fatigue, H2H, Travel)

**Easy features to add** (+14 features):
- Rest Days (2): `home_rest_days`, `away_rest_days`
- Back-to-Back (2): `home_b2b`, `away_b2b`
- H2H Last 10 (4): Win%, Avg Total, Avg Spread, Cover%
- Travel Miles Last 7D (2): `home_miles_last_7d`, `away_miles_last_7d`
- Timezone Changes (2): `home_tz_changes`, `away_tz_changes`
- Injuries (2): `home_injury_impact`, `away_injury_impact`

**Skip hard features** (for later):
- Clutch Performance (needs play-by-play)
- Lineup Continuity (needs rotation data)
- Referee Tendencies (needs external API)
- Shot Quality (needs tracking data)

---

### LONG TERM (Next Month) - Roadmap Implementation

#### Week 1: Foundation
- Install PyTorch (CPU version): `pip install torch --index-url https://download.pytorch.org/whl/cpu`
- Install CatBoost: `pip install catboost`
- Create directory structure
- Test installations

#### Week 2: Enhanced Features (Partial)
- Implement +14 easy features (Rest, Travel, H2H, Injuries)
- Update all feature engineers
- Test feature extraction

#### Week 3: PyTorch Models
- Implement TabularNet (6-layer residual network)
- Train on NBA/NCAAB first (working data)
- Compare performance vs XGBoost

#### Week 4: Neural Ensemble
- Build ensemble weighter
- Train on recent predictions
- Deploy and test

**IMPORTANT**: Don't do this unless current system is working first!

---

## RECOMMENDED APPROACH

### Path A: PRAGMATIC (Recommended)
**Goal**: Get system working reliably with current architecture

**Steps**:
1. ✅ Fix NCAAF/NFL feature mapping (1 day)
2. ✅ Fix NHL stats source (1 day)
3. ✅ Retrain NFL/NCAAF models (1 day)
4. ✅ Verify all 5 sports generating good predictions (1 day)
5. ✅ Monitor for 1 week to confirm stability
6. → THEN consider enhanced features/PyTorch

**Timeline**: 1 week to working system

### Path B: AMBITIOUS (Risky)
**Goal**: Implement full roadmap (78 features, PyTorch, neural ensemble)

**Steps**:
1. Install PyTorch/CatBoost
2. Build all 36 enhanced features
3. Implement 3 new model types
4. Build neural ensemble
5. Integrate everything
6. Test and validate
7. Fix all the bugs

**Timeline**: 6 weeks, high risk of breaking working parts

---

## MY RECOMMENDATION

### DO THIS NOW (This Week):

1. **Fix the broken NFL/NCAAF predictions** (CRITICAL)
   - Debug feature mismatch
   - Verify models load correctly
   - Test predictions manually

2. **Get NHL working**
   - Configure MoneyPuck data source
   - Test NHL feature engineer
   - Generate test predictions

3. **Verify frontend pages**
   - Max EV Edges showing good data
   - Model Performance tracking correctly
   - Predictions Database displaying results

4. **Monitor for 1 week**
   - Check daily prediction logs
   - Verify edges are reasonable (-5% to +10%)
   - Track actual results

### DO THIS NEXT (Week 2-3):

5. **Add easy enhanced features** (Pick 5-10):
   - Rest days (easiest - just schedule math)
   - Back-to-back games (same as rest)
   - H2H records (query historical DB)
   - Travel distance (city coordinates + math)
   - Basic injury count (if data available)

6. **Retrain models with new features**
   - Test on one sport first (NBA)
   - Compare performance before/after
   - If better, roll out to all sports

### DO THIS LATER (Month 2):

7. **Consider PyTorch only if**:
   - Current system is profitable
   - You have clean, reliable data pipeline
   - You want to experiment with deep learning
   - You have time to debug neural networks

---

## WHAT QUESTIONS TO ASK

Before proceeding, answer these:

1. **What's the goal?**
   - ❓ Working system that generates predictions daily?
   - ❓ OR Cutting-edge ML research platform?

2. **What's the priority?**
   - ❓ Fix broken predictions (NFL/NCAAF) first?
   - ❓ OR Build new features (roadmap) first?

3. **What's the timeline?**
   - ❓ Need working system ASAP?
   - ❓ OR Can spend 6 weeks building enhanced version?

4. **What's the data quality?**
   - ❓ Do you have reliable sources for 36 enhanced features?
   - ❓ OR Stick with current 42 features that work?

---

## CONCLUSION

**You have a working ML system** (NBA, NCAAB) but it's:
1. ❌ Broken for NFL/NCAAF (feature mismatch)
2. ❌ Not updated for NHL (stale data)
3. ❌ Not using enhanced features (roadmap)
4. ❌ Not using PyTorch models (roadmap)
5. ❌ Not using neural ensemble (roadmap)

**Frontend pages work** but show broken data for some sports.

**My strong recommendation**:
1. Fix what's broken (NFL/NCAAF/NHL) - 1 week
2. Verify system is profitable - 1-2 weeks
3. THEN consider roadmap enhancements - Month 2+

**Don't build fancy features on a broken foundation!**

---

**Next Steps**: Tell me which path you want to take:
- **Path A**: Fix broken predictions first (pragmatic)
- **Path B**: Implement full roadmap now (ambitious)
- **Path C**: Something else?
