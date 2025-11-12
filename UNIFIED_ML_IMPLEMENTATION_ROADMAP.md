# UNIFIED ML IMPLEMENTATION ROADMAP
**Date:** 2025-11-12
**Status:** 🎯 Master Plan - Combines Strategy Integration + Production Hardening
**Purpose:** Prioritized roadmap merging Claude's strategy analysis + GPT's production recommendations

---

## 📋 EXECUTIVE SUMMARY

### **Two Critical Paths Identified:**

#### **PATH A: Strategy Enhancement (Claude's Analysis)**
- **Goal:** Integrate ML models with 25 betting strategies
- **Impact:** +3-5% win rate, +3-5% ROI per strategy
- **Timeline:** 8 weeks
- **Focus:** Better predictions through ML + strategy fusion

#### **PATH B: Production Hardening (GPT's Analysis)**
- **Goal:** Make ML models production-ready and trustworthy
- **Impact:** Reduced false positives, better user trust, regulatory compliance
- **Timeline:** 4-6 weeks
- **Focus:** Calibration, transparency, risk management

### **Unified Approach:**
- **Week 1-2:** Quick wins from BOTH paths (parallel development)
- **Week 3-4:** Foundation work (data + infrastructure)
- **Week 5-6:** Advanced integrations
- **Week 7-8:** Monitoring, optimization, launch

---

## 🎯 PRIORITIZED TASK LIST

### **Priority System:**
- **P0 (CRITICAL):** Must have for launch, blocks everything else
- **P1 (HIGH):** Major impact, should do ASAP
- **P2 (MEDIUM):** Incremental improvements
- **P3 (LOW):** Nice to have, can defer

### **Impact Scoring:**
- 🔥🔥🔥 **Game Changer** (10-20%+ improvement)
- 🔥🔥 **High Impact** (5-10% improvement)
- 🔥 **Medium Impact** (2-5% improvement)
- ⭐ **Low Impact** (<2% improvement)

---

## 🚀 PHASE 1: QUICK WINS (Week 1-2)

### **P0 Tasks - Must Ship First**

#### **1. Add Rolling Stats to Data Loaders** 🔥🔥🔥
**Source:** Claude - ML Strategy Integration
**Effort:** 2-3 days
**Impact:** +2-3% win rate immediately across ALL strategies
**Why P0:** Foundation for everything else

**Implementation:**
```python
# Add to all data loaders (nba_data_loader.py, etc.)
def calculate_rolling_stats(team, games=5):
    recent = team.games[-games:]
    return {
        'ppg_last_5': mean([g.points for g in recent]),
        'ppg_last_10': mean([g.points for g in team.games[-10:]]),
        'ppg_last_15': mean([g.points for g in team.games[-15:]]),
        'fg_pct_last_5': mean([g.fg_pct for g in recent]),
        'pace_last_5': mean([g.pace for g in recent]),
        'def_rating_last_5': mean([g.def_rating for g in recent]),
        'trend': recent[-1].ppg - recent[0].ppg,  # Improving/declining
        'volatility': std([g.points for g in recent])
    }
```

**Dependencies:** None
**Blockers:** None
**Success Metric:** All 87 models can access last_5/10/15 stats

---

#### **2. Post-Slippage ROI + Quote-Age Guard** 🔥🔥
**Source:** GPT - Production Hardening
**Effort:** 2-3 days
**Impact:** Reduces false edges by 15-20%, builds user trust
**Why P0:** Prevents recommending stale/unavailable lines

**Implementation:**
```python
# Quote-age checker
class QuoteAgeGuard:
    MAX_AGE_SECONDS = 10  # 10 second max age for alerts

    def is_quote_fresh(self, odds_data):
        quote_age = (now() - odds_data.timestamp).total_seconds()
        if quote_age > self.MAX_AGE_SECONDS:
            logger.warning(f"Stale quote: {quote_age}s old")
            return False
        return True

    def check_cross_book_dispersion(self, odds_list):
        """High dispersion = pending move, skip alert"""
        if len(odds_list) < 2:
            return True  # Single book, can't check

        odds_range = max(odds_list) - min(odds_list)
        if odds_range > 5:  # >5 point dispersion
            logger.warning(f"High dispersion: {odds_range}")
            return False
        return True

# Slippage model
class SlippageModel:
    SLIPPAGE_BY_BOOK = {
        'draftkings': 2.0,  # cents per $100
        'fanduel': 2.5,
        'betmgm': 3.0,
        'offshore': 5.0
    }

    def calculate_post_slippage_roi(self, roi, book, bet_size):
        slippage = self.SLIPPAGE_BY_BOOK.get(book, 3.0)
        slippage_cost = (bet_size / 100) * slippage
        return roi - (slippage_cost / bet_size)
```

**Dependencies:** Access to real-time odds timestamps
**Blockers:** May need to add timestamp field to odds API
**Success Metric:** No alerts on quotes >10s old, ROI calculations include slippage

---

#### **3. Confidence Intervals + Data Window on Strategy Results** 🔥
**Source:** GPT - Results Transparency
**Effort:** 2 days
**Impact:** Builds trust, shows statistical significance
**Why P0:** Users need to see sample size and confidence

**Implementation:**
```python
# Add to Strategy Results API
def calculate_confidence_interval(wins, losses, confidence_level=0.95):
    """Wilson score interval for win rate"""
    n = wins + losses
    p = wins / n if n > 0 else 0
    z = 1.96  # 95% confidence

    denominator = 1 + z**2/n
    center = (p + z**2/(2*n)) / denominator
    margin = z * sqrt((p*(1-p)/n + z**2/(4*n**2))) / denominator

    return (center - margin, center + margin)

# Strategy response
{
    "strategy_name": "B2B vs Rested",
    "win_rate": 0.566,
    "roi": 0.081,
    "roi_ci_95": (0.052, 0.110),  # NEW
    "sample_size": 145,
    "data_window": "2023-09-01 to 2025-11-12",  # NEW
    "confidence": "HIGH" if sample_size > 200 else "MEDIUM" if sample_size > 100 else "LOW"
}
```

**Dependencies:** None
**Blockers:** None
**Success Metric:** All strategy cards show 95% CI and data window

---

#### **4. Two-Book Confirmation Toggle** 🔥
**Source:** GPT - Execution & Odds Microstructure
**Effort:** 1-2 days
**Impact:** Reduces false edges by 30%, optional for users
**Why P0:** Simple but high impact for reducing trap lines

**Implementation:**
```python
# Settings option
class AlertSettings:
    def __init__(self):
        self.require_two_book_confirmation = True  # Default ON
        self.min_cushion = 0.02  # 2% cushion required

    def validate_edge(self, prediction, market_odds):
        """Check if edge is real across multiple books"""
        if not self.require_two_book_confirmation:
            return True  # User disabled, allow single book

        books_with_edge = []
        for book, odds in market_odds.items():
            fair_price = prediction.fair_odds
            cushion = abs(odds - fair_price) / fair_price

            if cushion >= self.min_cushion:
                books_with_edge.append(book)

        if len(books_with_edge) >= 2:
            return True
        else:
            logger.info(f"Only 1 book has edge, skipping (two-book mode enabled)")
            return False
```

**Dependencies:** Multi-book odds feed
**Blockers:** Need to ensure we have 2+ books per game
**Success Metric:** Users can toggle on/off, default reduces alerts by ~30%

---

#### **5. Probability Calibration (Isotonic)** 🔥🔥
**Source:** GPT - Modeling & Validation
**Effort:** 3-4 days
**Impact:** HIGH confidence bets actually hit 60%+ instead of 52%
**Why P0:** Confidence levels are currently miscalibrated

**Implementation:**
```python
from sklearn.isotonic import IsotonicRegression

class CalibratedModel:
    def __init__(self, base_model):
        self.model = base_model
        self.calibrator = IsotonicRegression(out_of_bounds='clip')
        self.is_calibrated = False

    def calibrate(self, X_val, y_val):
        """Fit calibrator on validation set"""
        raw_probs = self.model.predict_proba(X_val)
        self.calibrator.fit(raw_probs, y_val)
        self.is_calibrated = True

        # Evaluate calibration
        calibrated_probs = self.calibrator.predict(raw_probs)
        brier_before = brier_score_loss(y_val, raw_probs)
        brier_after = brier_score_loss(y_val, calibrated_probs)

        logger.info(f"Brier score: {brier_before:.4f} → {brier_after:.4f}")

    def predict_proba(self, X):
        """Return calibrated probabilities"""
        raw_probs = self.model.predict_proba(X)
        if self.is_calibrated:
            return self.calibrator.predict(raw_probs)
        return raw_probs

    def confidence_buckets(self, X, y):
        """Show calibration by bucket"""
        probs = self.predict_proba(X)
        buckets = {
            'HIGH (60-70%)': {'predicted': [], 'actual': []},
            'MEDIUM (55-60%)': {'predicted': [], 'actual': []},
            'LOW (50-55%)': {'predicted': [], 'actual': []}
        }

        for prob, outcome in zip(probs, y):
            if prob >= 0.60:
                bucket = 'HIGH (60-70%)'
            elif prob >= 0.55:
                bucket = 'MEDIUM (55-60%)'
            else:
                bucket = 'LOW (50-55%)'

            buckets[bucket]['predicted'].append(prob)
            buckets[bucket]['actual'].append(outcome)

        return buckets
```

**Dependencies:** Validation dataset with actual outcomes
**Blockers:** Need to retrain all 87 models with calibration
**Success Metric:** Brier score improves by 0.02+, HIGH confidence hits 60%+

---

### **P1 Tasks - High Impact, Ship Week 2**

#### **6. Fatigue Index** 🔥🔥
**Source:** Claude - ML Strategy Integration
**Effort:** 4-5 days
**Impact:** +2-3% win rate for rest/fatigue strategies (5+ strategies)
**Why P1:** Helps multiple strategies, reusable component

**Implementation:**
```python
class FatigueIndex:
    def calculate(self, team, current_date):
        fatigue_score = 0

        # Games recently
        games_last_7 = count_games(team, days=7)
        fatigue_score += games_last_7 * 10

        # Travel
        travel_miles = calculate_travel_miles(team, days=14)
        fatigue_score += (travel_miles / 1000) * 5

        # Elevation
        elevation_changes = count_altitude_games(team, days=7)
        fatigue_score += elevation_changes * 15

        # Overtime
        ot_games = count_ot_games(team, days=7)
        fatigue_score += ot_games * 20

        # Rest (negative fatigue)
        rest_days = get_rest_days(team, current_date)
        fatigue_score -= rest_days * 8

        # Minutes (starters playing heavy)
        avg_minutes_starters = get_avg_minutes(team.starters, days=5)
        if avg_minutes_starters > 35:
            fatigue_score += 15

        return {
            'score': min(max(fatigue_score, 0), 100),
            'level': self._get_level(fatigue_score),
            'factors': {
                'games': games_last_7,
                'travel_miles': travel_miles,
                'elevation_changes': elevation_changes,
                'ot_games': ot_games,
                'rest_days': rest_days,
                'heavy_minutes': avg_minutes_starters > 35
            }
        }

    def _get_level(self, score):
        if score >= 75: return 'CRITICAL'
        elif score >= 60: return 'HIGH'
        elif score >= 40: return 'MEDIUM'
        else: return 'LOW'
```

**Dependencies:** Travel distance calculator, game schedule data
**Blockers:** May need to build travel distance lookup table
**Success Metric:** Fatigue API endpoint live, B2B strategy uses it

---

#### **7. ML-Enhanced B2B Strategy** 🔥🔥
**Source:** Claude - ML Strategy Integration
**Effort:** 3-4 days (after rolling stats + fatigue index)
**Impact:** +3-5% ROI on most popular strategy
**Why P1:** High user adoption, clear value demonstration

**Implementation:**
```python
class MLEnhancedB2BStrategy:
    def __init__(self, base_strategy, ml_ensemble, fatigue_index):
        self.strategy = base_strategy
        self.ml = ml_ensemble
        self.fatigue = fatigue_index

    def analyze(self, game_data):
        # Get base strategy recommendation
        strategy_rec = self.strategy.analyze_matchup(
            game_data.game_id,
            game_data.sport,
            game_data.home_schedule,
            game_data.away_schedule,
            game_data.spread
        )

        if not strategy_rec:
            return None  # No B2B situation

        # Get ML prediction WITH fatigue
        ml_prediction = self.ml.predict(
            home_team=game_data.home_team,
            away_team=game_data.away_team,
            home_rest=game_data.home_schedule.rest_days,
            away_rest=game_data.away_schedule.rest_days,
            home_fatigue=self.fatigue.calculate(game_data.home_team, game_data.date),
            away_fatigue=self.fatigue.calculate(game_data.away_team, game_data.date)
        )

        # Get ML prediction WITHOUT fatigue (neutral baseline)
        ml_baseline = self.ml.predict(
            home_team=game_data.home_team,
            away_team=game_data.away_team,
            home_rest=2,  # Normalize
            away_rest=2,
            home_fatigue={'score': 30, 'level': 'LOW'},
            away_fatigue={'score': 30, 'level': 'LOW'}
        )

        # Calculate ML-detected B2B impact
        ml_impact = abs(ml_prediction.spread - ml_baseline.spread)
        strategy_impact = strategy_rec.edge_estimate

        # Ensemble prediction
        ml_weight = 0.6
        strategy_weight = 0.4

        combined_edge = (ml_impact * ml_weight) + (strategy_impact * strategy_weight)

        # Confidence based on agreement
        agreement = abs(ml_impact - strategy_impact)
        if agreement < 1.5:
            confidence = 'HIGH'
        elif agreement < 3.0:
            confidence = 'MEDIUM'
        else:
            confidence = 'LOW'

        return {
            'strategy': 'B2B vs Rested (ML-Enhanced)',
            'recommendation': strategy_rec.recommendation,
            'edge': combined_edge,
            'confidence': confidence,
            'contributions': {
                'ml_impact': ml_impact,
                'strategy_impact': strategy_impact,
                'ml_weight': ml_weight,
                'strategy_weight': strategy_weight
            },
            'fatigue_analysis': {
                'fatigued_team': strategy_rec.fatigued_team,
                'fatigue_score': self.fatigue.calculate(
                    game_data.home_team if strategy_rec.recommendation == 'FADE_HOME' else game_data.away_team,
                    game_data.date
                )
            }
        }
```

**Dependencies:** Rolling stats, fatigue index, retrained ML models
**Blockers:** Must complete tasks 1, 6 first
**Success Metric:** B2B strategy win rate increases from 56.6% to 60%+

---

#### **8. Opponent-Adjusted Metrics** 🔥
**Source:** Claude - ML Strategy Integration
**Effort:** 3-4 days
**Impact:** +2-4% win rate for pace/total strategies
**Why P1:** Improves accuracy of totals predictions significantly

**Implementation:**
```python
class OpponentAdjuster:
    def __init__(self, league_averages):
        self.league_avg = league_averages

    def adjust_for_opponent(self, team_stat, opponent_defense_rank, stat_type='ppg'):
        """
        Adjust team stat based on opponent quality

        Example: Team scores 115 PPG but against weak defenses
                 vs Top 5 defense: expect ~108 PPG
        """
        # Opponent factor (1.0 = league average)
        # Top 5 defense = 0.93 (7% reduction)
        # Bottom 5 defense = 1.07 (7% boost)
        if opponent_defense_rank <= 5:
            opponent_factor = 0.93
        elif opponent_defense_rank <= 10:
            opponent_factor = 0.96
        elif opponent_defense_rank >= 25:
            opponent_factor = 1.04
        elif opponent_defense_rank >= 20:
            opponent_factor = 1.07
        else:
            opponent_factor = 1.0

        adjusted_stat = team_stat * opponent_factor

        return {
            'raw': team_stat,
            'adjusted': adjusted_stat,
            'opponent_factor': opponent_factor,
            'adjustment': adjusted_stat - team_stat
        }

    def get_team_stats_vs_quality(self, team):
        """Get team's performance vs top/bottom opponents"""
        return {
            'ppg_vs_top10': self._get_ppg_vs_rank_range(team, 1, 10),
            'ppg_vs_bottom10': self._get_ppg_vs_rank_range(team, 21, 30),
            'ppg_vs_elite_defense': self._get_ppg_vs_rank_range(team, 1, 5),
            'pace_vs_slow_teams': self._get_pace_vs_tempo_range(team, 'slow'),
            'pace_vs_fast_teams': self._get_pace_vs_tempo_range(team, 'fast')
        }
```

**Dependencies:** Opponent ranking data, historical matchup data
**Blockers:** Need to build opponent quality classifier
**Success Metric:** Total predictions accuracy improves by 2+ points

---

## 🏗️ PHASE 2: FOUNDATION (Week 3-4)

### **P1 Tasks - Critical Infrastructure**

#### **9. Feature Store (Lightweight)** 🔥
**Source:** GPT - Feature Governance
**Effort:** 5-7 days
**Impact:** Prevents feature leakage, enables version control
**Why P1:** Critical for production ML, prevents bugs

**Implementation:**
```python
# Postgres feature store
CREATE TABLE feature_store (
    feature_id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50),  -- 'team', 'game', 'player'
    entity_id VARCHAR(100),
    feature_name VARCHAR(100),
    feature_value FLOAT,
    feature_version INT,
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX (entity_id, feature_name, valid_from)
);

# Python API
class FeatureStore:
    def get_features(self, entity_id, feature_names, as_of_date):
        """
        Get features as they existed at as_of_date
        Prevents leakage by enforcing temporal consistency
        """
        query = """
        SELECT feature_name, feature_value
        FROM feature_store
        WHERE entity_id = %s
          AND feature_name = ANY(%s)
          AND valid_from <= %s
          AND (valid_to IS NULL OR valid_to > %s)
        ORDER BY valid_from DESC
        """

        results = self.db.execute(query, [entity_id, feature_names, as_of_date, as_of_date])
        return dict(results)

    def add_feature(self, entity_id, feature_name, value, valid_from):
        """Add new feature value with version control"""
        # Expire previous version
        self.db.execute("""
            UPDATE feature_store
            SET valid_to = %s
            WHERE entity_id = %s AND feature_name = %s AND valid_to IS NULL
        """, [valid_from, entity_id, feature_name])

        # Insert new version
        self.db.execute("""
            INSERT INTO feature_store (entity_id, feature_name, feature_value, valid_from)
            VALUES (%s, %s, %s, %s)
        """, [entity_id, feature_name, value, valid_from])
```

**Dependencies:** Postgres database
**Blockers:** None
**Success Metric:** All features stored with temporal consistency, zero leakage

---

#### **10. Leakage Guards (Grouped CV)** 🔥🔥
**Source:** GPT - Modeling & Validation
**Effort:** 3-4 days
**Impact:** Prevents overfitting, realistic backtest results
**Why P1:** Current validation may be optimistic due to leakage

**Implementation:**
```python
from sklearn.model_selection import GroupKFold, TimeSeriesSplit

class LeakageGuardedValidator:
    def __init__(self):
        self.group_cv = GroupKFold(n_splits=5)
        self.time_cv = TimeSeriesSplit(n_splits=5)

    def validate(self, X, y, model, validation_type='grouped'):
        """
        Validation with leakage guards

        Grouped: Ensures all instances of same game_id in same fold
        Time: Ensures test set is always after train set
        """
        if validation_type == 'grouped':
            # Group by game_id to prevent leakage
            groups = X['game_id']
            scores = []

            for train_idx, test_idx in self.group_cv.split(X, y, groups):
                X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

                # Verify no game_id overlap
                train_games = set(X_train['game_id'])
                test_games = set(X_test['game_id'])
                assert len(train_games & test_games) == 0, "Leakage detected!"

                model.fit(X_train, y_train)
                score = model.score(X_test, y_test)
                scores.append(score)

            return np.mean(scores), np.std(scores)

        elif validation_type == 'time':
            # Time-based splits
            scores = []

            for train_idx, test_idx in self.time_cv.split(X):
                X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

                # Verify test set is after train set
                assert X_train['date'].max() < X_test['date'].min(), "Time leakage!"

                model.fit(X_train, y_train)
                score = model.score(X_test, y_test)
                scores.append(score)

            return np.mean(scores), np.std(scores)

    def check_for_leakage(self, features):
        """Scan features for potential leakage"""
        leakage_patterns = [
            'final_', 'actual_', 'result_', 'outcome_',
            '_post_game', '_closing_line'
        ]

        leaky_features = []
        for feature in features:
            for pattern in leakage_patterns:
                if pattern in feature.lower():
                    leaky_features.append(feature)

        if leaky_features:
            logger.error(f"Potential leakage in features: {leaky_features}")
            raise ValueError("Leakage detected in feature set!")

        return True
```

**Dependencies:** None
**Blockers:** Need to retrain all models with proper validation
**Success Metric:** Zero leakage detected, validation scores are realistic

---

#### **11. Injury Impact Quantification** 🔥🔥
**Source:** Claude - ML Strategy Integration
**Effort:** 5-7 days (requires building injury database)
**Impact:** +4-6% win rate for injury-related strategies
**Why P1:** High impact when injuries occur (frequent in NBA/NFL)

**Implementation:**
```python
class InjuryImpactModel:
    def __init__(self):
        self.injury_db = self._load_injury_database()

    def _load_injury_database(self):
        """Load historical injury impacts"""
        # Build from past seasons
        return pd.read_sql("""
            SELECT
                player_name,
                position,
                injury_type,
                avg(team_ppg_before - team_ppg_after) as ppg_impact,
                avg(team_def_rating_after - team_def_rating_before) as def_impact,
                avg(pace_before - pace_after) as pace_impact,
                count(*) as sample_size
            FROM injury_history
            GROUP BY player_name, position, injury_type
            HAVING count(*) >= 3
        """, self.db)

    def calculate_impact(self, player, injury_type):
        """Calculate expected impact of injury"""
        # Find similar injuries
        similar = self.injury_db[
            (self.injury_db['position'] == player.position) &
            (self.injury_db['injury_type'] == injury_type)
        ]

        if len(similar) == 0:
            # Use position averages
            similar = self.injury_db[self.injury_db['position'] == player.position]

        # Weight by player usage rate
        usage_multiplier = player.usage_rate / 25.0  # 25% = league average

        impact = {
            'ppg_loss': similar['ppg_impact'].mean() * usage_multiplier,
            'def_impact': similar['def_impact'].mean(),
            'pace_impact': similar['pace_impact'].mean(),
            'confidence': 'HIGH' if len(similar) >= 10 else 'MEDIUM' if len(similar) >= 5 else 'LOW'
        }

        return impact

    def team_impact(self, team, injured_players):
        """Calculate total team impact from multiple injuries"""
        total_impact = {
            'ppg_loss': 0,
            'def_rating_change': 0,
            'pace_change': 0,
            'win_prob_change': 0
        }

        for player, injury in injured_players:
            impact = self.calculate_impact(player, injury)
            total_impact['ppg_loss'] += impact['ppg_loss']
            total_impact['def_rating_change'] += impact['def_impact']
            total_impact['pace_change'] += impact['pace_impact']

        # Win probability impact (rough estimate)
        # -10 PPG = -15% win probability
        total_impact['win_prob_change'] = (total_impact['ppg_loss'] / 10) * -0.15

        return total_impact
```

**Dependencies:** Historical injury database
**Blockers:** Need to scrape/buy injury history data
**Success Metric:** Injury Cascade strategy win rate increases to 75%+

---

### **P2 Tasks - Important But Not Blocking**

#### **12. CLV Tracking + Odds Buckets** 🔥
**Source:** GPT - Results Transparency
**Effort:** 3-4 days
**Impact:** Proves timing alpha, builds user trust
**Why P2:** Nice to have but not blocking launch

**Implementation:**
```python
class CLVTracker:
    def track_clv(self, prediction_id, recommendation_odds, closing_odds):
        """
        Track Closing Line Value
        Positive CLV = we beat the closing line
        """
        clv = closing_odds - recommendation_odds

        # Store
        self.db.execute("""
            INSERT INTO clv_tracking (prediction_id, rec_odds, closing_odds, clv)
            VALUES (%s, %s, %s, %s)
        """, [prediction_id, recommendation_odds, closing_odds, clv])

        return {
            'clv': clv,
            'clv_percentage': (clv / closing_odds) * 100,
            'beat_closing': clv > 0
        }

    def get_clv_by_strategy(self, strategy_id):
        """Get average CLV per strategy"""
        return self.db.query("""
            SELECT
                AVG(clv) as avg_clv,
                STDDEV(clv) as clv_std,
                SUM(CASE WHEN clv > 0 THEN 1 ELSE 0 END) / COUNT(*) as beat_closing_pct
            FROM clv_tracking
            WHERE prediction_id IN (
                SELECT id FROM predictions WHERE strategy_id = %s
            )
        """, [strategy_id])

    def get_roi_by_odds_bucket(self, strategy_id):
        """Show ROI performance by odds bucket"""
        return self.db.query("""
            SELECT
                CASE
                    WHEN rec_odds <= -150 THEN 'Heavy Favorite'
                    WHEN rec_odds <= -110 THEN 'Favorite'
                    WHEN rec_odds <= +110 THEN 'Pick Em'
                    WHEN rec_odds <= +150 THEN 'Underdog'
                    ELSE 'Heavy Underdog'
                END as odds_bucket,
                COUNT(*) as bets,
                AVG(profit_loss) as roi
            FROM predictions p
            JOIN results r ON p.id = r.prediction_id
            WHERE p.strategy_id = %s
            GROUP BY odds_bucket
            ORDER BY bets DESC
        """, [strategy_id])
```

**Dependencies:** None
**Blockers:** None
**Success Metric:** CLV sparklines visible on strategy cards

---

#### **13. Model Registry + Canary Deployment** 🔥
**Source:** GPT - Ops & Monitoring
**Effort:** 4-5 days
**Impact:** Safe deployments, rollback capability
**Why P2:** Important for production but not blocking initial launch

**Implementation:**
```python
class ModelRegistry:
    def register_model(self, model, metadata):
        """Register new model version"""
        model_id = str(uuid.uuid4())

        # Serialize model
        model_bytes = pickle.dumps(model)
        model_hash = hashlib.sha256(model_bytes).hexdigest()

        # Store metadata
        self.db.execute("""
            INSERT INTO model_registry (
                model_id, model_name, version, features_hash,
                training_date, validation_score, metadata
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, [
            model_id,
            metadata['name'],
            metadata['version'],
            model_hash,
            datetime.now(),
            metadata['validation_score'],
            json.dumps(metadata)
        ])

        # Store model file
        s3.upload(f"models/{model_id}.pkl", model_bytes)

        return model_id

    def canary_deploy(self, model_id, traffic_percentage=0.10):
        """Deploy model to 10% of traffic"""
        self.db.execute("""
            UPDATE model_deployments
            SET status = 'canary', traffic_pct = %s, deployed_at = NOW()
            WHERE model_id = %s
        """, [traffic_percentage, model_id])

        logger.info(f"Canary deployment: {model_id} at {traffic_percentage*100}% traffic")

    def monitor_canary(self, model_id, hours=24):
        """Monitor canary performance"""
        metrics = self.db.query("""
            SELECT
                COUNT(*) as predictions,
                AVG(CASE WHEN correct = TRUE THEN 1 ELSE 0 END) as accuracy,
                AVG(clv) as avg_clv,
                AVG(roi) as roi
            FROM predictions
            WHERE model_id = %s
              AND created_at >= NOW() - INTERVAL '%s hours'
        """, [model_id, hours])

        # Get baseline (previous model)
        baseline = self.db.query("""
            SELECT accuracy, avg_clv, roi
            FROM model_performance
            WHERE model_id = (
                SELECT model_id FROM model_deployments
                WHERE status = 'production' AND model_name = (
                    SELECT model_name FROM model_registry WHERE model_id = %s
                )
            )
        """, [model_id])

        # Compare
        if metrics['accuracy'] < baseline['accuracy'] - 0.02:
            logger.error(f"Canary performing worse! Accuracy: {metrics['accuracy']:.3f} vs {baseline['accuracy']:.3f}")
            self.rollback_canary(model_id)
        else:
            logger.info(f"Canary performing well: {metrics}")

    def promote_canary(self, model_id):
        """Promote canary to 100% traffic"""
        self.db.execute("""
            UPDATE model_deployments
            SET status = 'production', traffic_pct = 1.0
            WHERE model_id = %s
        """, [model_id])

        logger.info(f"Promoted {model_id} to production")

    def rollback_canary(self, model_id):
        """Rollback canary to previous model"""
        self.db.execute("""
            UPDATE model_deployments
            SET status = 'rolled_back', traffic_pct = 0.0
            WHERE model_id = %s
        """, [model_id])

        logger.warning(f"Rolled back {model_id}")
```

**Dependencies:** S3 or model storage
**Blockers:** None
**Success Metric:** Canary deployments catch regressions before full rollout

---

## 🔬 PHASE 3: ADVANCED FEATURES (Week 5-6)

### **P1 Tasks - High Value Additions**

#### **14. NBA Bonus-Imminent + 2-for-1 Triggers** 🔥🔥
**Source:** GPT - New Signals
**Effort:** 3-4 days
**Impact:** New high-ROI live betting signals
**Why P1:** Quick win, new revenue stream

**Implementation:**
```python
class NBALiveTriggers:
    def detect_bonus_imminent(self, game_state):
        """
        Detect when team is about to enter bonus
        Bonus threshold: 5 fouls in quarter
        """
        for team in ['home', 'away']:
            team_fouls = game_state[f'{team}_fouls_quarter']

            if team_fouls == 4:
                # One foul away from bonus
                return {
                    'trigger': 'bonus_imminent',
                    'team': team,
                    'fouls': team_fouls,
                    'prediction': f'{game_state.opponent(team)} likely to score more (free throws)',
                    'bet_type': 'Over quarter total',
                    'confidence': 'MEDIUM'
                }

        return None

    def detect_two_for_one(self, game_state):
        """
        Detect 2-for-1 opportunity (24-48 seconds left in quarter)
        Team with ball can get 2 possessions
        """
        time_left = game_state.time_remaining_quarter

        if 24 <= time_left <= 48:
            possession_team = game_state.possession

            return {
                'trigger': '2_for_1_opportunity',
                'team': possession_team,
                'time_left': time_left,
                'prediction': f'{possession_team} likely to score (2-for-1 situation)',
                'bet_type': 'Team quarter total Over',
                'confidence': 'HIGH' if time_left >= 35 else 'MEDIUM'
            }

        return None
```

**Dependencies:** Live game state data
**Blockers:** Need reliable play-by-play feed
**Success Metric:** New live betting alerts with 55%+ win rate

---

#### **15. NHL Delayed Penalty + Imminent Goalie Pull** 🔥🔥🔥
**Source:** GPT - New Signals
**Effort:** 4-5 days
**Impact:** Game-changing signal for NHL (80%+ ROI possible)
**Why P1:** NHL goalie pull already #1 strategy, this enhances it

**Implementation:**
```python
class NHLLiveTriggers:
    def detect_delayed_penalty(self, game_state):
        """
        Delayed penalty = 6-on-5 until whistle
        Expect goals at 5x normal rate
        """
        if game_state.delayed_penalty_active:
            attacking_team = game_state.delayed_penalty_team

            # Calculate fair odds for next goal
            time_until_whistle_expected = 8  # seconds avg
            goals_per_second_6v5 = 0.08  # 8% per second
            prob_goal = time_until_whistle_expected * goals_per_second_6v5

            return {
                'trigger': 'delayed_penalty',
                'attacking_team': attacking_team,
                'prob_goal': prob_goal,
                'fair_odds': self._prob_to_odds(prob_goal),
                'bet_type': 'Next Goal',
                'confidence': 'HIGH'
            }

        return None

    def detect_imminent_goalie_pull(self, game_state):
        """
        Predict goalie pull 10-20 seconds before it happens
        Requires: Score, time, possession, zone
        """
        if game_state.period != 3:
            return None

        time_left = game_state.time_remaining
        score_diff = game_state.home_score - game_state.away_score
        trailing_team = 'home' if score_diff < 0 else 'away'

        # Goalie pull likely if:
        # - Trailing by 1-2 goals
        # - 1:30 to 2:30 remaining
        # - Have puck in opponent zone

        if abs(score_diff) in [1, 2] and 90 <= time_left <= 150:
            if game_state.puck_zone == 'offensive' and game_state.possession == trailing_team:
                # Predict pull in next 10-20 seconds
                prob_pull = 0.75

                # Calculate expected value of early bet
                current_odds_over = game_state.market_odds['total_over']

                # After pull, odds will move 15-20 cents
                expected_odds_after_pull = current_odds_over - 18

                return {
                    'trigger': 'imminent_goalie_pull',
                    'trailing_team': trailing_team,
                    'time_until_pull': 15,  # seconds
                    'prob_pull': prob_pull,
                    'recommendation': 'Bet Over NOW before pull',
                    'current_odds': current_odds_over,
                    'expected_odds_after': expected_odds_after_pull,
                    'value': current_odds_over - expected_odds_after_pull,
                    'confidence': 'CRITICAL'
                }

        return None
```

**Dependencies:** Real-time NHL play-by-play, possession tracking
**Blockers:** Need NHL-specific data feed
**Success Metric:** 10-20 second head start on goalie pull bets

---

#### **16. Conformal Prediction Intervals** 🔥
**Source:** GPT - Modeling & Validation
**Effort:** 5-6 days
**Impact:** Show uncertainty bands, better risk management
**Why P1:** Differentiates from competitors, sophisticated

**Implementation:**
```python
from mapie.regression import MapieRegressor

class ConformalPredictor:
    def __init__(self, base_model):
        self.model = base_model
        self.conformal_model = None

    def fit(self, X_train, y_train, X_cal, y_cal):
        """
        Fit base model + conformal wrapper
        X_cal/y_cal = calibration set for conformal
        """
        # Fit base model
        self.model.fit(X_train, y_train)

        # Wrap with conformal predictor
        self.conformal_model = MapieRegressor(self.model, method='plus')
        self.conformal_model.fit(X_train, y_train)

        # Calibrate on validation set
        self.conformal_model.partial_fit(X_cal, y_cal)

    def predict_with_intervals(self, X, alpha=0.10):
        """
        Predict with prediction intervals
        alpha=0.10 → 90% prediction interval
        alpha=0.05 → 95% prediction interval
        """
        y_pred, y_intervals = self.conformal_model.predict(X, alpha=alpha)

        return {
            'prediction': y_pred[0],
            'lower_bound': y_intervals[0, 0, 0],
            'upper_bound': y_intervals[0, 1, 0],
            'interval_width': y_intervals[0, 1, 0] - y_intervals[0, 0, 0],
            'confidence': (1 - alpha) * 100
        }

    def display_prediction(self, game, prediction):
        """Format for user display"""
        return f"""
        Predicted Total: {prediction['prediction']:.1f}
        90% Confidence Interval: [{prediction['lower_bound']:.1f}, {prediction['upper_bound']:.1f}]

        Interpretation:
        - Point prediction: {prediction['prediction']:.1f}
        - Range: ±{prediction['interval_width']/2:.1f} points
        - Market line: {game.market_total}
        - Edge: {abs(prediction['prediction'] - game.market_total):.1f} points
        - Market is {'outside' if game.market_total < prediction['lower_bound'] or game.market_total > prediction['upper_bound'] else 'inside'} our 90% interval
        """
```

**Dependencies:** MAPIE library, calibration dataset
**Blockers:** None
**Success Metric:** Prediction intervals displayed on game cards

---

## 📊 PHASE 4: MONITORING & OPTIMIZATION (Week 7-8)

### **P2 Tasks - Continuous Improvement**

#### **17. Drift & Decay Dashboard** 🔥
**Source:** GPT - Ops & Monitoring
**Effort:** 4-5 days
**Impact:** Early warning system for model degradation
**Why P2:** Important for maintenance, not blocking launch

**Implementation:**
```python
class DriftDetector:
    def detect_feature_drift(self, reference_data, current_data):
        """
        Detect if feature distributions have changed
        Uses Kolmogorov-Smirnov test
        """
        from scipy.stats import ks_2samp

        drift_results = {}

        for column in reference_data.columns:
            if column in ['game_id', 'date']:
                continue

            statistic, p_value = ks_2samp(
                reference_data[column],
                current_data[column]
            )

            drift_results[column] = {
                'statistic': statistic,
                'p_value': p_value,
                'drifted': p_value < 0.05,  # 5% significance
                'severity': 'HIGH' if p_value < 0.01 else 'MEDIUM' if p_value < 0.05 else 'LOW'
            }

        # Alert if multiple features drifting
        drifted_features = [k for k, v in drift_results.items() if v['drifted']]

        if len(drifted_features) >= 5:
            logger.warning(f"Significant drift detected in {len(drifted_features)} features: {drifted_features[:5]}")
            self.alert_retrain_needed()

        return drift_results

    def detect_edge_decay(self):
        """
        Track if edges are shrinking over time
        Market may be adapting to our predictions
        """
        weekly_edges = self.db.query("""
            SELECT
                DATE_TRUNC('week', created_at) as week,
                strategy_id,
                AVG(edge) as avg_edge,
                AVG(roi) as avg_roi
            FROM predictions
            WHERE created_at >= NOW() - INTERVAL '90 days'
            GROUP BY week, strategy_id
            ORDER BY week ASC
        """)

        # Detect trend
        for strategy_id in weekly_edges['strategy_id'].unique():
            strategy_data = weekly_edges[weekly_edges['strategy_id'] == strategy_id]

            # Linear regression to detect decay
            from scipy.stats import linregress
            slope, intercept, r_value, p_value, std_err = linregress(
                range(len(strategy_data)),
                strategy_data['avg_edge']
            )

            if slope < -0.1 and p_value < 0.05:
                logger.warning(f"Edge decay detected for strategy {strategy_id}: {slope:.3f} per week")
                self.alert_strategy_degrading(strategy_id, slope)
```

**Dependencies:** Historical data
**Blockers:** None
**Success Metric:** Automated alerts when drift or decay detected

---

#### **18. Methodology Modal (Transparency)** 🔥
**Source:** GPT - Results Transparency
**Effort:** 2-3 days
**Impact:** Builds trust, reduces skepticism
**Why P2:** Nice to have, improves UX

**Implementation:**
```typescript
// Frontend component
const MethodologyModal = ({ strategy }) => {
  return (
    <Modal>
      <h2>{strategy.name} - Methodology</h2>

      <Section title="Data Window">
        <p>Sample: {strategy.sample_size} bets</p>
        <p>Date range: {strategy.data_window}</p>
        <p>Sports: {strategy.sports.join(', ')}</p>
      </Section>

      <Section title="Entry Criteria">
        <ul>
          {strategy.filters.map(filter => (
            <li>{filter.description}</li>
          ))}
        </ul>
      </Section>

      <Section title="Odds Assumptions">
        <p>Average odds: {strategy.baseline_odds}</p>
        <p>Min odds required: {strategy.min_odds}</p>
        <p>Max odds accepted: {strategy.max_odds}</p>
      </Section>

      <Section title="Slippage">
        <p>Assumed slippage: {strategy.slippage} cents per $100</p>
        <p>Post-slippage ROI: {strategy.roi_after_slippage}%</p>
      </Section>

      <Section title="Confidence Intervals">
        <p>Win rate: {strategy.win_rate}% (95% CI: {strategy.win_rate_ci})</p>
        <p>ROI: {strategy.roi}% (95% CI: {strategy.roi_ci})</p>
      </Section>

      <Section title="Validation Method">
        <p>Cross-validation: {strategy.cv_method}</p>
        <p>Out-of-sample accuracy: {strategy.oos_accuracy}%</p>
      </Section>
    </Modal>
  );
};
```

**Dependencies:** None
**Blockers:** None
**Success Metric:** Reduced user questions about methodology

---

## 📅 WEEKLY BREAKDOWN

### **Week 1: Quick Wins Part 1 (P0 Foundation)**
**Mon-Tue:**
- Task 1: Add rolling stats to data loaders
- Task 5: Probability calibration (isotonic)

**Wed-Thu:**
- Task 2: Post-slippage ROI + quote-age guard
- Task 3: Confidence intervals on tables

**Fri:**
- Task 4: Two-book confirmation toggle
- Deploy Week 1 changes
- Validation and testing

**Expected Outcomes:**
- All 87 models have rolling stats
- ROI calculations realistic (post-slippage)
- No stale quotes in alerts
- Confidence levels properly calibrated

---

### **Week 2: Quick Wins Part 2 (P1 High Impact)**
**Mon-Tue:**
- Task 6: Fatigue index implementation
- Task 8: Opponent-adjusted metrics

**Wed-Thu:**
- Task 7: ML-enhanced B2B strategy
- Retrain models with new features

**Fri:**
- Deploy Week 2 changes
- A/B test enhanced vs original strategies
- Measure improvements

**Expected Outcomes:**
- B2B strategy win rate: 56.6% → 60%+
- Fatigue index API live
- Opponent-adjusted totals more accurate

---

### **Week 3: Foundation (Infrastructure)**
**Mon-Tue:**
- Task 9: Feature store (lightweight)
- Task 10: Leakage guards (grouped CV)

**Wed-Thu:**
- Task 11: Injury impact quantification
- Build injury database

**Fri:**
- Retrain all models with proper validation
- Verify no leakage
- Deploy feature store

**Expected Outcomes:**
- Zero feature leakage
- Injury impacts quantified
- Temporal consistency enforced

---

### **Week 4: More Integrations**
**Mon-Tue:**
- Task 12: CLV tracking + odds buckets
- Deploy CLV sparklines

**Wed-Thu:**
- Task 13: Model registry + canary deployment
- Set up canary infrastructure

**Fri:**
- Integrate 2-3 more strategies with ML
- (Favorite Comeback, Pace Mismatch, Quarter Reversal)

**Expected Outcomes:**
- 5 strategies ML-enhanced
- CLV visible on all strategy cards
- Canary deployment pipeline ready

---

### **Week 5: Advanced Signals**
**Mon-Tue:**
- Task 14: NBA bonus-imminent + 2-for-1
- Test on recent games

**Wed-Thu:**
- Task 15: NHL delayed penalty + imminent goalie pull
- Integrate with goalie pull strategy

**Fri:**
- Deploy new live betting triggers
- Monitor performance

**Expected Outcomes:**
- 2-3 new high-ROI live signals
- Goalie pull strategy enhanced
- NBA quarter betting improved

---

### **Week 6: Prediction Intervals**
**Mon-Tue:**
- Task 16: Conformal prediction intervals
- Calibrate on validation set

**Wed-Thu:**
- Deploy prediction intervals to frontend
- User testing

**Fri:**
- Refine display based on feedback
- Documentation updates

**Expected Outcomes:**
- Prediction intervals shown on all game cards
- Users understand uncertainty
- Differentiates from competitors

---

### **Week 7: Monitoring**
**Mon-Tue:**
- Task 17: Drift & decay dashboard
- Set up automated alerts

**Wed-Thu:**
- Task 18: Methodology modal
- Complete transparency layer

**Fri:**
- Final testing before launch
- Bug fixes

**Expected Outcomes:**
- Monitoring dashboard live
- Methodology transparent
- System hardened

---

### **Week 8: Launch & Optimize**
**Mon-Tue:**
- Production deployment
- Monitor closely

**Wed-Thu:**
- User onboarding
- Support training

**Fri:**
- First optimization iteration
- Collect user feedback

**Expected Outcomes:**
- System live in production
- Users adopting ML-enhanced strategies
- Feedback loop established

---

## 🎯 SUCCESS METRICS

### **Week 1-2 (Quick Wins):**
- ✅ All models use rolling stats
- ✅ Quote-age < 10s on all alerts
- ✅ ROI calculations include slippage
- ✅ HIGH confidence bets hit 60%+ (was 52%)
- ✅ B2B strategy win rate: 56.6% → 60%+

### **Week 3-4 (Foundation):**
- ✅ Zero feature leakage detected
- ✅ Injury impacts quantified (not guessed)
- ✅ CLV tracking showing +1-2 point average
- ✅ 5 strategies ML-enhanced

### **Week 5-6 (Advanced):**
- ✅ NBA/NHL live signals deployed
- ✅ 10-20 second head start on goalie pulls
- ✅ Prediction intervals displayed
- ✅ User satisfaction improves

### **Week 7-8 (Launch):**
- ✅ Drift dashboard operational
- ✅ Methodology transparent
- ✅ Zero critical bugs
- ✅ 60%+ user adoption of ML features

### **Overall Platform Impact (Post-Launch):**
- 🎯 **Average strategy ROI: 8.3% → 11-13%** (+45% profit increase)
- 🎯 **Average win rate: 57.2% → 60-62%** (+3-5%)
- 🎯 **False positives: -25-40% reduction**
- 🎯 **User satisfaction: 4.2 → 4.6/5**
- 🎯 **CLV: +1-2 points average**

---

## 💡 KEY INSIGHTS

### **1. Two Complementary Paths**
- **Claude's Path:** Make strategies smarter (data + ML integration)
- **GPT's Path:** Make ML trustworthy (calibration + transparency)
- **Both are critical** - you need smart AND trustworthy

### **2. Quick Wins First**
- Week 1-2 delivers immediate value
- Rolling stats (+2-3% win rate) in 3 days
- Calibration (+8% confidence accuracy) in 4 days
- **Don't wait for perfect, ship incremental improvements**

### **3. Infrastructure Enables Scale**
- Feature store prevents future bugs
- Model registry enables safe deployments
- Monitoring catches degradation early
- **Invest in Week 3-4 to scale smoothly**

### **4. Transparency Builds Trust**
- Confidence intervals show statistical rigor
- CLV proves timing alpha
- Methodology modals eliminate skepticism
- **Users trust what they understand**

### **5. Live Betting = Highest ROI**
- NBA bonus/2-for-1: New signal, 55%+ expected
- NHL imminent goalie pull: 10-20s head start = $$$
- Delayed penalty: 80% ROI possible
- **Focus on live once pregame is solid**

---

## ⚠️ RISKS & MITIGATION

### **Risk 1: Scope Creep**
**Problem:** Too many features, miss deadlines
**Mitigation:**
- Stick to P0/P1 tasks
- Defer P2/P3 to post-launch
- 8-week hard deadline

### **Risk 2: Data Quality Issues**
**Problem:** Bad data → bad predictions
**Mitigation:**
- Quote-age guard (max 10s)
- Feature store with validation
- Monitoring dashboard catches drift

### **Risk 3: User Confusion**
**Problem:** Too complex, users don't understand ML
**Mitigation:**
- Methodology modals
- Clear confidence levels
- "Show your work" (ML vs strategy breakdown)

### **Risk 4: Performance Regression**
**Problem:** New models perform worse
**Mitigation:**
- Canary deployment (10% traffic)
- Automated rollback if metrics drop
- A/B testing everything

### **Risk 5: Market Adaptation**
**Problem:** Edges shrink as we scale
**Mitigation:**
- Drift dashboard monitors edge decay
- Weekly retraining adapts to market
- Focus on less efficient markets (live, props)

---

## 🏁 FINAL RECOMMENDATIONS

### **Priority Order (Don't Skip Steps):**
1. **Week 1-2:** Quick wins (P0 tasks)
   - Biggest impact for least effort
   - Foundation for everything else

2. **Week 3-4:** Infrastructure (Feature store, leakage guards)
   - Not sexy but critical for scale
   - Prevents catastrophic bugs

3. **Week 5-6:** Advanced features (Live signals, intervals)
   - High ROI signals
   - Competitive differentiation

4. **Week 7-8:** Polish & launch
   - Monitoring, transparency
   - User education

### **Team Allocation:**
**Week 1-2 (Parallel Development):**
- Engineer 1: Rolling stats + calibration
- Engineer 2: Quote-age guard + slippage
- Engineer 3: Frontend (CI, two-book toggle)

**Week 3-4 (Infrastructure):**
- Engineer 1: Feature store
- Engineer 2: Leakage guards + retraining
- Engineer 3: Injury database + CLV

**Week 5-6 (Advanced):**
- Engineer 1: NBA live triggers
- Engineer 2: NHL live triggers
- Engineer 3: Conformal intervals

**Week 7-8 (Launch):**
- All hands on deck: Testing, deployment, monitoring

### **Success = Smart + Trustworthy + Transparent**
- Smart strategies (Claude's ML integration)
- Trustworthy predictions (GPT's calibration)
- Transparent methodology (both)

**Combined, these create an unbeatable platform.**

---

**END OF UNIFIED ROADMAP**

Ready to execute? Start with Week 1, Task 1: Rolling stats. Everything else builds from there.
