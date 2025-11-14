# Current Data Inventory - XGBoost ML Feasibility Analysis

## Executive Summary

**Current State:** Basic team statistics (offense, defense, differentials)
**ML Readiness:** ⚠️ **PARTIALLY READY** - Need more features for robust XGBoost models
**Feasibility:** ✅ **YES** - With enhancements, excellent for ML

---

## Currently Scraped Data (TeamRankings.com)

### **NBA (30 teams)**

| Feature | Description | ML Value | Type |
|---------|-------------|----------|------|
| `pts_per_game` | Points scored per game | ✅ HIGH | Continuous |
| `pts_allowed` | Points allowed per game | ✅ HIGH | Continuous |
| `point_diff` | Average scoring margin | ✅ **CRITICAL** | Continuous |
| `wins` | Season wins | ✅ HIGH | Discrete |
| `losses` | Season losses | ✅ HIGH | Discrete |
| `games_played` | Total games | ✅ MEDIUM | Discrete |
| `win_pct` | Win percentage | ✅ HIGH | Continuous |
| `net_rating` | Net rating (point diff proxy) | ✅ **CRITICAL** | Continuous |
| `off_rating` | Offensive rating (PPG proxy) | ⚠️ MEDIUM | Continuous |
| `def_rating` | Defensive rating (Opp PPG proxy) | ⚠️ MEDIUM | Continuous |

**Total Features: 10**

---

### **NFL (32 teams)**

| Feature | Description | ML Value | Type |
|---------|-------------|----------|------|
| `pts_per_game` | Points scored per game | ✅ HIGH | Continuous |
| `pts_allowed` | Points allowed per game | ✅ HIGH | Continuous |
| `point_diff` | Average scoring margin | ✅ **CRITICAL** | Continuous |
| `wins` | Season wins | ✅ HIGH | Discrete |
| `losses` | Season losses | ✅ HIGH | Discrete |
| `games_played` | Total games | ✅ MEDIUM | Discrete |
| `win_pct` | Win percentage | ✅ HIGH | Continuous |
| `yards_per_game` | Total offensive yards | ✅ HIGH | Continuous |
| `yards_allowed` | Total defensive yards | ✅ HIGH | Continuous |
| `turnovers_lost` | Turnovers per game | ✅ **CRITICAL** | Continuous |
| `turnovers_gained` | Takeaways per game | ✅ **CRITICAL** | Continuous |
| `turnover_diff` | Turnover differential | ✅ **CRITICAL** | Continuous |
| `net_rating` | Net rating (point diff proxy) | ✅ **CRITICAL** | Continuous |
| `off_rating` | Offensive rating (PPG proxy) | ⚠️ MEDIUM | Continuous |
| `def_rating` | Defensive rating (Opp PPG proxy) | ⚠️ MEDIUM | Continuous |

**Total Features: 15**

---

### **NCAAF (136 teams)**

| Feature | Description | ML Value | Type |
|---------|-------------|----------|------|
| `pts_per_game` | Points scored per game | ✅ HIGH | Continuous |
| `pts_allowed` | Points allowed per game | ✅ HIGH | Continuous |
| `point_diff` | Average scoring margin | ✅ **CRITICAL** | Continuous |
| `yards_per_game` | Total offensive yards | ✅ HIGH | Continuous |
| `yards_allowed` | Total defensive yards | ✅ HIGH | Continuous |
| `net_rating` | Net rating (point diff proxy) | ✅ **CRITICAL** | Continuous |
| `off_rating` | Offensive rating (PPG proxy) | ⚠️ MEDIUM | Continuous |
| `def_rating` | Defensive rating (Opp PPG proxy) | ⚠️ MEDIUM | Continuous |

**Total Features: 8**

---

### **MLB (30 teams)**

| Feature | Description | ML Value | Type |
|---------|-------------|----------|------|
| `runs_per_game` | Runs scored per game | ✅ HIGH | Continuous |
| `runs_allowed` | Runs allowed per game | ✅ HIGH | Continuous |
| `run_diff` | Average run differential | ✅ **CRITICAL** | Continuous |
| `batting_avg` | Team batting average | ✅ HIGH | Continuous |
| `era` | Team ERA (pitching) | ✅ **CRITICAL** | Continuous |
| `net_rating` | Net rating (run diff proxy) | ✅ **CRITICAL** | Continuous |
| `off_rating` | Offensive rating (runs proxy) | ⚠️ MEDIUM | Continuous |
| `def_rating` | Defensive rating (runs allowed proxy) | ⚠️ MEDIUM | Continuous |

**Total Features: 8**

---

## Summary: Current Data Coverage

| Sport | Teams | Features | Quality |
|-------|-------|----------|---------|
| NBA | 30 | 10 | ⚠️ Basic |
| NFL | 32 | 15 | ✅ Good |
| NCAAF | 136 | 8 | ⚠️ Basic |
| MLB | 30 | 8 | ⚠️ Basic |

**Total Dataset Size:** 198 teams, 41 unique features

---

## What's MISSING for Robust XGBoost Models

### **Critical Missing Features (HIGH PRIORITY):**

#### **All Sports:**
1. ❌ **Pace/Tempo Metrics** - Game speed is critical for totals betting
2. ❌ **Recent Form** - Last 5/10 games performance (recency bias matters)
3. ❌ **Home/Away Splits** - Home court/field advantage varies by team
4. ❌ **Rest Days** - Fatigue impacts performance significantly
5. ❌ **Head-to-Head History** - Matchup-specific trends
6. ❌ **Streaks** - Win/loss streaks impact momentum
7. ❌ **Line Movement** - Sharp money tracking
8. ❌ **Closing Line Value (CLV)** - Are we beating the market?
9. ❌ **Historical Bet Outcomes** - Ground truth for training

#### **NBA Specific:**
10. ❌ **Pace** - Possessions per 48 minutes (available on TeamRankings!)
11. ❌ **True Shooting %** - Shooting efficiency
12. ❌ **Rebounds Per Game** - Second chance points
13. ❌ **Assists Per Game** - Ball movement
14. ❌ **Blocks/Steals** - Defensive metrics
15. ❌ **Back-to-Back Games** - Critical for fatigue analysis

#### **NFL Specific:**
16. ❌ **3rd Down Conversion %** - Sustaining drives
17. ❌ **Red Zone Efficiency** - Scoring in red zone
18. ❌ **Sacks** - Pass rush pressure
19. ❌ **Time of Possession** - Ball control
20. ❌ **Weather Data** - Wind, temp, precipitation

#### **NCAAF Specific:**
21. ❌ **Conference Strength** - Power 5 vs mid-major
22. ❌ **Recruiting Rankings** - Talent level proxy

#### **MLB Specific:**
23. ❌ **Starting Pitcher Stats** - ERA, WHIP, K/9
24. ❌ **Bullpen Stats** - Relief pitcher strength
25. ❌ **Park Factors** - Hitter-friendly vs pitcher-friendly
26. ❌ **Weather** - Wind impacts fly balls
27. ❌ **Day vs Night Games** - Performance splits

---

## What TeamRankings ALSO Offers (Easy to Add!)

### **Immediately Available on TeamRankings:**

#### **NBA:**
- ✅ Pace (possessions per game)
- ✅ Offensive rebounds per game
- ✅ Assists per game
- ✅ Turnovers per game
- ✅ Steals per game
- ✅ Blocks per game
- ✅ Field goal %
- ✅ 3-point %
- ✅ Free throw %
- ✅ Home/away splits

#### **NFL:**
- ✅ 3rd down conversion %
- ✅ Red zone scoring %
- ✅ Sacks per game
- ✅ Sacks allowed per game
- ✅ Time of possession
- ✅ Penalties per game
- ✅ Pass yards per game
- ✅ Rush yards per game
- ✅ Home/away splits

#### **NCAAF:**
- ✅ 3rd down conversion %
- ✅ Red zone scoring %
- ✅ Sacks per game
- ✅ Time of possession
- ✅ Pass yards per game
- ✅ Rush yards per game

#### **MLB:**
- ✅ Home runs per game
- ✅ Strikeouts per game
- ✅ Walks per game
- ✅ WHIP (walks + hits per inning)
- ✅ On-base percentage
- ✅ Slugging percentage

**Estimated Additional Features: 50-75 more!**

---

## External Data Sources Needed

### **Already Have:**
- ✅ The Odds API - Live betting lines
- ✅ ESPN API - Live scores, quarter scores
- ✅ KenPom - NCAAB advanced metrics

### **Should Add:**

#### **High Priority:**
1. **Weather API** (OpenWeather, WeatherAPI)
   - NFL: Wind, temperature, precipitation
   - MLB: Wind speed/direction, temperature
   - **Cost:** $0-$50/month

2. **Rest/Schedule Data** (ESPN API or Sports Data IO)
   - Days of rest between games
   - Back-to-back situations
   - Travel distance
   - **Cost:** FREE (ESPN) or included in current API

3. **Historical Betting Data** (Sports Data IO or manual logging)
   - Our bet outcomes
   - Closing lines
   - Line movement
   - **Cost:** FREE (log our own bets)

4. **Injury Data** (ESPN API or Sports Data IO)
   - Key player injuries
   - Injury impact on team strength
   - **Cost:** FREE (ESPN)

#### **Nice to Have:**
5. **Player Props Data** (The Odds API)
   - Individual player statistics
   - Prop bet markets
   - **Cost:** Already have access

6. **Advanced Metrics** (Basketball Reference, Football Outsiders, FanGraphs)
   - NBA: True shooting %, usage rate
   - NFL: DVOA, EPA
   - MLB: WAR, FIP
   - **Cost:** $0-$100/year

---

## XGBoost ML Feasibility Assessment

### **✅ FEASIBLE - Here's Why:**

#### **1. Sufficient Sample Size**
- NBA: 30 teams × 82 games = **2,460 games/season**
- NFL: 32 teams × 17 games = **544 games/season**
- NCAAF: 136 teams × 12 games = **1,632 games/season**
- MLB: 30 teams × 162 games = **4,860 games/season**

**Total: ~9,500 games/season across all sports** ✅

**XGBoost typically needs:**
- Minimum: 500-1,000 samples
- Optimal: 10,000+ samples

**We can achieve this with:**
- Single season: 9,500 games
- 2-3 seasons: 20,000-30,000 games
- With multiple strategies: 50,000+ training examples

#### **2. Feature Quality**
- ✅ Point differential = **CRITICAL** feature (highest correlation with wins)
- ✅ Turnover differential (NFL) = **CRITICAL** for game outcomes
- ✅ ERA (MLB) = **CRITICAL** for totals betting

**Current features are HIGH QUALITY, just need MORE of them.**

#### **3. Target Variables Are Clear**
- **Classification:** Did bet win/lose/push? ✅
- **Regression:** What was the actual total/spread? ✅
- **Binary:** Over/under, spread cover? ✅

#### **4. XGBoost Strengths Align Perfectly**
- ✅ Handles missing data gracefully
- ✅ Feature importance ranking (tells us what matters)
- ✅ Non-linear relationships (pace × efficiency interactions)
- ✅ Robust to outliers (blowouts don't ruin model)
- ✅ Fast training (minutes, not hours)
- ✅ Excellent for tabular data (which we have)

---

## Recommended Enhancement Plan

### **Phase 1: Expand TeamRankings Scraping** (1-2 days)
**Add these features (all available on TeamRankings):**

**NBA:**
- Pace
- Offensive rebounds
- Assists
- Turnovers
- Steals/Blocks
- Shooting percentages (FG%, 3P%, FT%)
- Home/away splits

**NFL:**
- 3rd down conversion %
- Red zone scoring %
- Sacks/Sacks allowed
- Time of possession
- Pass/rush yards splits
- Home/away splits

**Result:** 30-40 additional features ✅

---

### **Phase 2: Add External Data Sources** (3-5 days)

1. **Weather API** - OpenWeather or WeatherAPI
   - Game-time temperature, wind, precipitation
   - **Impact:** NFL & MLB totals accuracy +5-10%

2. **Rest/Schedule Data** - ESPN API
   - Days of rest
   - Back-to-back games
   - Travel distance
   - **Impact:** NBA & NFL accuracy +3-7%

3. **Historical Bet Logging** - Build our own database
   - Track every bet we make
   - Closing line value
   - Actual outcomes
   - **Impact:** Ground truth for training ✅

**Result:** 10-15 additional features ✅

---

### **Phase 3: Build XGBoost Pipeline** (1 week)

**Components:**
1. Data preprocessing pipeline
2. Feature engineering (derived features, interactions)
3. Train/test split (time-based, not random)
4. Hyperparameter tuning (GridSearchCV or Optuna)
5. Model evaluation (accuracy, ROI, Sharpe ratio)
6. Feature importance analysis
7. Model deployment (integrate with game_tracker)

**Libraries:**
- `xgboost` - Core model
- `pandas` - Data manipulation
- `scikit-learn` - Preprocessing, evaluation
- `optuna` - Hyperparameter optimization (optional)

**Result:** Production-ready ML models ✅

---

### **Phase 4: Strategy Optimization** (Ongoing)

1. **Retrain models weekly** with new game data
2. **A/B test ML predictions** vs rule-based strategies
3. **Track CLV** (are we beating closing lines?)
4. **Ensemble models** (combine multiple strategies)
5. **Auto-tune Kelly sizing** based on confidence

---

## Feature Importance (Predicted)

Based on betting literature and domain knowledge, here's what XGBoost will likely find:

### **Top 10 Most Important Features (Expected):**
1. **Point/Run Differential** - 🔥 **CRITICAL** (30-40% importance)
2. **Turnover Differential (NFL)** - 🔥 **CRITICAL** (15-20%)
3. **Pace (NBA)** - 🔥 **CRITICAL** for totals (10-15%)
4. **ERA (MLB)** - 🔥 **CRITICAL** for totals (15-20%)
5. **Home/Away Split** - 🔥 HIGH (8-12%)
6. **Rest Days** - 🔥 HIGH (5-10%)
7. **Win Percentage** - 🔥 HIGH (5-8%)
8. **Recent Form (Last 5 games)** - 🔥 HIGH (5-8%)
9. **Yards Allowed (NFL)** - 🔥 MEDIUM (3-5%)
10. **Weather (NFL/MLB)** - 🔥 MEDIUM (2-5%)

**The rest:** Contribute 10-20% collectively

---

## Expected ML Performance Gains

### **Current Rule-Based Strategies:**
- Quarter Reversal: 55.3% win rate, +12.1% ROI
- Favorite Comeback: 60.3% win rate, +18% ROI (estimated)

### **With XGBoost Enhancement:**
- **Expected improvement:** +3-8% win rate
- **Predicted performance:** 58-65% win rate, +18-25% ROI
- **ROI boost:** +50-100% over baseline

### **Why the Boost?**
1. **Better feature interactions** - Discovers non-linear relationships
2. **Adaptive thresholds** - Auto-adjusts filters (e.g., talent gap)
3. **Confidence calibration** - More accurate probability estimates
4. **Pattern discovery** - Finds hidden edges we missed

---

## XGBoost Use Cases for Our Platform

### **1. Strategy Confidence Scoring** ✅
**Current:** Rule-based confidence (HIGH/MEDIUM/LOW)
**ML:** Probability-based confidence (0.0-1.0)

**Example:**
```python
# Current
if talent_diff < 2:
    confidence = "HIGH"  # +8% boost

# ML
confidence_score = xgb_model.predict_proba(features)[0][1]
# Returns: 0.68 (68% win probability)
```

### **2. Feature Importance for New Strategies** ✅
**Discover what matters most:**
- XGBoost tells us: "Pace matters 15% for totals"
- Build new strategy: "High Pace Games Over Detector"

### **3. Optimal Bet Sizing** ✅
**Kelly Criterion refinement:**
```python
# Current Kelly
kelly_fraction = edge / odds

# ML-Enhanced Kelly
ml_confidence = xgb_model.predict_proba(features)[0][1]
adjusted_kelly = (ml_confidence - (1 - ml_confidence)) / odds
```

### **4. Auto-Filter Weak Bets** ✅
**Current:** Hard-coded filters (e.g., talent gap > 12)
**ML:** Dynamic filtering based on learned thresholds

### **5. Live Bet Recommendations** ✅
**Real-time predictions during games:**
- Ingest live stats (quarter scores, momentum)
- Predict 2H outcome
- Alert if edge detected

---

## Data Storage Requirements

### **Current:**
- Cache files: ~100 KB total

### **With ML Enhancements:**
- Expanded cache: ~500 KB-1 MB
- Historical game data (1 season): ~50 MB
- Historical game data (3 seasons): ~150 MB
- Trained XGBoost models: ~10-50 MB each

**Total: ~250 MB for full ML system** ✅

Still tiny! No storage concerns.

---

## Recommended Architecture

```
Data Layer:
├── TeamRankings scrapers (team stats) ← Already have
├── The Odds API (betting lines) ← Already have
├── ESPN API (live scores) ← Already have
├── Weather API (conditions) ← Add
└── Bet logging DB (outcomes) ← Build

Feature Engineering:
├── Raw features → Derived features
├── Interaction terms (pace × efficiency)
├── Recent form (rolling averages)
└── Time-based features (day of week, rest)

ML Models:
├── XGBoost Classifier (win/loss/push)
├── XGBoost Regressor (actual totals)
├── Ensemble (combine multiple models)
└── Feature importance tracker

Strategy Layer:
├── Rule-based strategies (current)
├── ML-enhanced strategies (confidence)
├── Pure ML strategies (discover new edges)
└── Hybrid strategies (rules + ML)
```

---

## Conclusion: Is This Feasible? **YES! ✅**

### **Summary:**

| Component | Status | Timeline |
|-----------|--------|----------|
| **Data Volume** | ✅ Sufficient | Already have |
| **Data Quality** | ⚠️ Good, need more | 1-2 weeks |
| **XGBoost Ready** | ✅ Yes | Can start now |
| **ROI Improvement** | ✅ Expected +50-100% | 2-4 weeks |
| **Storage** | ✅ Tiny (~250 MB) | No concern |
| **Cost** | ✅ Minimal ($0-$50/mo) | Negligible |

### **Action Plan:**

**Week 1:**
- Expand TeamRankings scrapers (add 30-40 features)
- Add weather API integration
- Build bet logging database

**Week 2:**
- Collect historical game data (1-2 seasons)
- Build XGBoost training pipeline
- Train initial models

**Week 3:**
- Integrate ML predictions with strategies
- A/B test ML vs rule-based
- Optimize hyperparameters

**Week 4+:**
- Deploy to production
- Monitor performance
- Iterate and improve

---

**Bottom Line:** You have a solid foundation. With the enhancements above, XGBoost will significantly improve strategy accuracy and discover new edges.

**ROI Projection:** +50-100% improvement over current rule-based strategies within 4-6 weeks.

**Next Step:** Expand TeamRankings scrapers to capture 30-40 additional features?
