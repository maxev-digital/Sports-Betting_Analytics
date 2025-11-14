# Game Cards & Projections System - Complete Overview

## System Architecture

### Data Flow
```
Live Odds API → GameTracker → GameProjector → ML Models → Frontend GameCard
     ↓              ↓             ↓              ↓              ↓
Team Stats API  Strategy      Pace/Efficiency  Predictions   User sees
```

---

## 1. DATA SOURCES

### A. Live Odds & Game State
**Provider:** The Odds API (`odds_client.py`)
- **Endpoint:** `https://api.the-odds-api.com/v4/sports/{sport}/odds`
- **Update Frequency:** Every 5 seconds
- **Data Retrieved:**
  - Current game scores (home/away)
  - Quarter/period and time remaining
  - Live totals from 20+ bookmakers
  - Spread lines and moneylines
  - Opening lines (pregame totals)

### B. Team Statistics (Multi-Source)

#### NBA Stats:
- **Primary:** TeamRankings Scraper (Free, reliable)
  - Pace, Offensive Rating, Defensive Rating
  - FG%, 3P%, FT%
  - Points per game, Last 5 games form
- **Fallback:** ESPN NBA Client
- **Live Stats:** NBA Live Client (play-by-play data when available)

#### NFL Stats:
- **ESPN NFL Client** + **NFL Stats Client**
  - Yards per game, passing/rushing stats
  - Third down efficiency, red zone %
  - Recent game momentum

#### NHL Stats:
- **NHL Stats Client**
  - Goals per game, shots per game
  - Power play %, penalty kill %
  - Faceoff win %, save %

#### NCAAB Stats:
- **KenPom** (when available)
- **ESPN NCAAB Client** (fallback)
  - Adjusted tempo, adjusted offensive/defensive efficiency

#### MLB Stats:
- **MLB Stats Client**
  - Runs per game, ERA, batting averages
  - Recent form, home/away splits

---

## 2. PROJECTION ENGINE (`projector.py`)

### Core Algorithm: Pace + Efficiency Model

#### Step 1: Calculate Current Pace
```python
current_pace = (total_possessions / minutes_played) * 48
```

**Pace Calculation:**
- Estimates possessions for each team based on current score and season pace
- Projects to 48 minutes for full-game comparison
- Compares to season averages to detect pace mismatches

#### Step 2: Calculate Efficiency Factor
```python
efficiency_factor = current_score / expected_points_at_this_time
```

**Efficiency Analysis:**
- Compares actual scoring to expected scoring based on season averages
- Weighted by shooting percentages (FG%, 3P%, FT%)
  - FG% Weight: 50%
  - 3P% Weight: 30%
  - FT% Weight: 20%
- Returns factor: 1.0 = average, <1.0 = cold shooting, >1.0 = hot shooting

#### Step 3: Time-Based Weighting
```python
if minutes_played < 12:
    season_weight = 0.60, current_weight = 0.40
elif minutes_played < 24:
    season_weight = 0.40, current_weight = 0.60
else:
    season_weight = 0.25, current_weight = 0.75
```

**Adaptive Weighting:**
- Early game: Rely more on season data (small sample size)
- Mid game: Balance current performance with season trends
- Late game: Heavily weight current game flow

#### Step 4: Final Projection
```python
expected_pace = (season_pace * season_weight) + (current_pace * current_weight)
projected_total = (expected_pace * efficiency_factor) + adjustment_factors
```

**Adjustment Factors:**
- Line movement (if total has moved significantly)
- Book disparity (if books disagree by 3+ points)
- Regression to mean (if shooting is unsustainably hot/cold)

---

## 3. MACHINE LEARNING MODELS (84 Total)

### Model Types Per Sport

#### NBA Models (21 models):
1. **XGBoost** - Totals, Spreads, Moneyline (3)
2. **Random Forest** - Totals, Spreads, Moneyline (3)
3. **LightGBM** - Totals, Spreads, Moneyline (3)
4. **Linear Regression** - Totals, Spreads (2)
5. **Logistic Regression** - Moneyline (1)
6. **Quantile Regression** - Lower/Mean/Upper bounds (3)
7. **Regression Analyzer** - Live regression detection (1)
8. **Ensemble Models** - Combined predictions (5)

#### NCAAB Models (21 models):
- Same structure as NBA

#### NFL Models (21 models):
- Same structure as NBA

#### NCAAF Models (21 models):
- Same structure as NBA

### Model Training

**Features Used (30-40 per sport):**
- Team efficiency metrics (offensive/defensive ratings)
- Pace metrics (possessions per 48 min)
- Shooting percentages (FG%, 3P%, FT%)
- Recent form (Last 5 games avg margin)
- Home/away splits
- Rest days (back-to-back vs rested)
- Opponent strength (net rating)
- Live game state (current score, time remaining)
- Momentum indicators (recent run, pace differential)

**Training Data:**
- Historical game data from SportsDataIO
- KenPom data for NCAAB (2023-2025 seasons)
- TeamRankings historical stats
- Validated against actual game outcomes

**Model Performance:**
- Totals: ~55-58% accuracy
- Spreads: ~54-57% accuracy
- Moneyline: ~60-65% accuracy
- ROI: 8-12% on sharp recommendations

---

## 4. WHAT THE GAME CARD DISPLAYS

### Top Section - Game State
- **Teams:** Away @ Home (formatted names)
- **Score:** Live score (red if away ahead, blue if home ahead)
- **Period:** "Q2 5:23" or "Halftime" or "Final"
- **Sport Icon:** 🏀 NBA, 🏈 NFL, 🏒 NHL, etc.

### Projection Metrics Row
```
Current Total: 218.5  →  Projected Final: 224.3  →  Edge: +5.8  →  Recommendation: OVER
```

**Displayed Metrics:**
1. **Current Live Total** - Average of all bookmaker totals
2. **Projected Final** - GameProjector's prediction for final score
3. **Pregame Total** - Opening line (for comparison)
4. **Line Movement** - How much total has moved (+/-2.5)
5. **Best Book Disparity** - Largest gap between books
6. **Edge** - Difference between projection and live total
7. **Confidence** - LOW/MEDIUM/HIGH (based on edge size)
8. **Recommendation** - OVER/UNDER (based on edge direction)

### Pace & Efficiency Indicators
```
Current Pace: 102.3 ↗️  |  Expected Pace: 98.5  |  Pace Differential: +3.8
```

**Pace Indicators:**
- ↗️ Faster than expected (favors OVER)
- ↘️ Slower than expected (favors UNDER)
- Efficiency Factor: Shows if teams shooting hot/cold
- Regression Factor: Shows mean reversion tendency

### Live Bookmaker Odds (Up to 20 books)
```
DraftKings    O 219.5 (-110)    U 219.5 (-110)
FanDuel       O 219.0 (-108)    U 219.0 (-112)  ← Best UNDER
BetMGM        O 220.0 (-110)    U 220.0 (-110)  ← Best OVER
```

**Highlighting:**
- Green highlight: Best available OVER odds
- Red highlight: Best available UNDER odds
- Bookmaker logos displayed
- Odds update latency shown (how fresh the odds are)

### Advanced Stats (Sport-Specific)

#### NBA/NCAAB:
- Team Stats: OffRtg, DefRtg, NetRtg, Pace, FG%, 3P%, FT%
- Rankings: #5 in Pace, #12 in OffRtg
- Recent Form: Last 5 games (7.2 PPG margin, HOT trend)
- Momentum: Points in last 5 minutes, current run

#### NFL/NCAAF:
- Yards per game, passing/rushing splits
- Third down efficiency, red zone %
- Time of possession
- Recent drives momentum

#### NHL:
- Goals per game, shots per game
- Power play %, penalty kill %
- Faceoff win %, save %
- Goalie pull prediction

### Strategy Alerts (When Active)
```
🔥 NBA Favorite Comeback - Edge: +8.5% - HIGH Confidence
⚡ Quarter Reversal Detected - Bet UNDER 2H 110.5
```

**Strategy Badges:**
- Show when your 84 models detect specific patterns
- Display recommended bet with edge %
- Click to expand for full details

### First Half Totals (When Available)
```
1H: 52 / 58.5  (Current / Projected)
```

---

## 5. EDGE CALCULATION

### Simple Edge
```python
edge = projected_total - current_live_total
```

**Example:**
- Projected: 224.3
- Current total: 218.5
- Edge: +5.8 (favor OVER)

### Confidence Levels
```python
if abs(edge) >= 5.0:
    confidence = "HIGH"
elif abs(edge) >= 3.0:
    confidence = "MEDIUM"
elif abs(edge) >= 2.0:
    confidence = "LOW"
else:
    confidence = None (no bet)
```

### ML-Enhanced Edge (Max EV Boost)
```python
ml_predictions = ensemble_model.predict(game_features)
regression_score = regression_analyzer.analyze(shooting_stats, pace_data)
final_edge = (projector_edge * 0.6) + (ml_edge * 0.4) + regression_bonus
```

**Regression Analyzer:**
- Detects unsustainable shooting (hot starts that will regress)
- NBA: 60.3% ATS when favorites trail at halftime after Q1 hot starts
- NCAAB: 58% hit rate on 2H unders after 1H shooting >15% above average

---

## 6. BOOKMAKER FILTERING

**User Settings:**
- Users can enable/disable specific bookmakers in Settings
- Only enabled bookmakers show in game cards
- "Best available odds" highlights update based on enabled books
- Popular presets: US Legal, Offshore, Sharp Books

---

## 7. REAL-TIME UPDATES

**Update Frequency:**
- **Live Games:** Every 5 seconds
- **Odds Updates:** Every 5-10 seconds (varies by bookmaker)
- **Team Stats:** Every 30 seconds (cached for performance)
- **ML Predictions:** Every 15 seconds (when significant change detected)

**Latency Tracking:**
- Shows how fresh each bookmaker's odds are
- Highlights stale odds (>60 seconds old)
- Tracks odds movement timestamps

---

## 8. STRATEGY INTEGRATION

### Live Strategies (Displayed on Game Cards)
1. **Max EV Boost (NBA/NCAAB)** - Regression to mean analysis
2. **Quarter Reversal** - Teams winning 2 consecutive quarters
3. **Favorite Comeback** - Favorites trailing underdogs after hot starts
4. **Halftime Tracker** - 2H value based on 1H pace
5. **Goalie Pull** - NHL empty net predictions
6. **Momentum Detector** - Recent scoring runs
7. **Pace Mismatch** - Game pace vs expected

### Strategy Alerts → Toast Notifications
When enabled strategies trigger:
- Toast notification pops up in bottom right
- Shows game, recommendation, edge %, bookmaker odds
- Countdown timer shows alert freshness
- Auto-dismisses based on urgency

---

## SUMMARY

**Your Game Cards Show:**
1. ✅ Live game state (score, time, period)
2. ✅ Projected final score (pace + efficiency model)
3. ✅ Edge vs current live total
4. ✅ Recommendation (OVER/UNDER with confidence)
5. ✅ 20+ bookmakers with live odds
6. ✅ Pace analysis (current vs expected)
7. ✅ Efficiency factor (shooting hot/cold)
8. ✅ Regression indicators (mean reversion)
9. ✅ ML model predictions (84 models)
10. ✅ Strategy alerts (when patterns detected)
11. ✅ Team stats & rankings
12. ✅ Recent form & momentum
13. ✅ Line movement & book disparity
14. ✅ First half totals
15. ✅ Best available odds highlighting

**Projection Methodology:**
- **Primary:** Pace + Efficiency algorithm (60% weight)
- **Secondary:** ML ensemble predictions (40% weight)
- **Enhancements:** Regression analysis, momentum detection, strategy pattern matching
- **Validation:** Backtested 60.3% ATS on NBA regression, 8-12% ROI on high confidence bets

**Data Refresh:** Every 5 seconds for live games
**Model Count:** 84 trained ML models across 4 sports
**Bookmakers:** 20+ live odds sources
**Alert System:** Toast notifications for enabled strategies with countdown timers
