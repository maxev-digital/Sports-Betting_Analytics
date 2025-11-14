# Monte Carlo Simulation - Backend Tasks for C1

## Overview
The frontend is now ready with:
- ✅ MonteCarloSimulation component (displays results)
- ✅ SimulationModal component (modal wrapper)
- ✅ useMonteCarloSimulation hook (API integration)

**C1 needs to build the backend API endpoint that powers these components.**

---

## Phase 1: Monte Carlo Simulation Endpoint (PRIORITY 1 - Build This FIRST)

### File to Create
`backend/simulation/monte_carlo_totals.py`

### Endpoint Specification

**Route:** `POST /api/simulation/monte-carlo`

**Request Body:**
```json
{
  "game_id": "nba_20251108_LAL_BOS",
  "current_state": {
    "quarter": 3,
    "time_remaining": "4:32",
    "home_score": 82,
    "away_score": 78
  },
  "n_simulations": 10000
}
```

**Note:** `current_state` is OPTIONAL - if not provided, simulate the entire game.

### Response Format (EXACT - Frontend Depends On This)

```json
{
  "current_total": 160,
  "simulations_run": 10000,
  "mean_final_total": 227.3,
  "median_final_total": 227.1,
  "std_dev": 8.4,

  "percentiles": {
    "p10": 216.5,
    "p25": 221.8,
    "p50": 227.1,
    "p75": 232.9,
    "p90": 238.2
  },

  "market_analysis": {
    "market_line": 228.5,
    "over_probability": 0.437,
    "under_probability": 0.563,
    "push_probability": 0.001,
    "implied_over_odds": 128,
    "market_over_odds": -110,
    "edge": -3.2,
    "recommendation": "UNDER",
    "kelly_fraction": 0.032
  },

  "distribution_buckets": {
    "210-215": 156,
    "215-220": 892,
    "220-225": 2134,
    "225-230": 3891,
    "230-235": 2245,
    "235-240": 583,
    "240-245": 99
  },

  "confidence_intervals": {
    "90%": [216.5, 238.2],
    "95%": [213.1, 241.5],
    "99%": [206.8, 247.8]
  }
}
```

### Implementation Steps

#### Step 1: Calculate Remaining Game Parameters

```python
def calculate_remaining_possessions(game_state, team_pace_stats):
    """
    Calculate how many possessions remain in the game

    Args:
        game_state: {quarter, time_remaining, home_score, away_score}
        team_pace_stats: {home_pace, away_pace} (possessions per 48 min)

    Returns:
        int: Estimated remaining possessions
    """
    # If pre-game (no current_state), use full 48 minutes
    if game_state is None:
        minutes_remaining = 48.0
    else:
        # Parse quarter and time
        quarter = game_state['quarter']
        time_parts = game_state['time_remaining'].split(':')
        minutes_in_quarter = float(time_parts[0]) + float(time_parts[1]) / 60

        # Calculate total remaining time
        quarters_remaining = 4 - quarter
        minutes_remaining = (quarters_remaining * 12) + minutes_in_quarter

    # Average team paces
    avg_pace = (team_pace_stats['home_pace'] + team_pace_stats['away_pace']) / 2

    # Possessions = (pace / 48) * minutes_remaining
    remaining_possessions = (avg_pace / 48) * minutes_remaining

    return int(remaining_possessions)
```

#### Step 2: Run Possession-by-Possession Simulation

```python
import numpy as np

def simulate_game_possession_by_possession(
    home_stats,
    away_stats,
    remaining_possessions,
    current_scores=(0, 0),
    n_simulations=10000
):
    """
    Run Monte Carlo simulation possession-by-possession

    Args:
        home_stats: {ppp: float, ppp_std: float}  # points per possession
        away_stats: {ppp: float, ppp_std: float}
        remaining_possessions: int
        current_scores: (home_score, away_score) tuple
        n_simulations: int

    Returns:
        np.array: Array of final total scores from all simulations
    """
    results = []

    for sim in range(n_simulations):
        home_score, away_score = current_scores

        # Simulate each remaining possession
        for poss in range(remaining_possessions):
            # Alternate possessions (home first)
            if poss % 2 == 0:
                # Home team possession
                points = np.random.normal(home_stats['ppp'], home_stats['ppp_std'])
                points = max(0, points)  # Can't score negative
                home_score += points
            else:
                # Away team possession
                points = np.random.normal(away_stats['ppp'], away_stats['ppp_std'])
                points = max(0, points)
                away_score += points

        # Store final total
        final_total = home_score + away_score
        results.append(final_total)

    return np.array(results)
```

#### Step 3: Calculate Probabilities and Edge

```python
def calculate_market_analysis(simulation_results, market_line):
    """
    Calculate over/under probabilities and betting edge

    Args:
        simulation_results: np.array of final totals
        market_line: float (e.g., 228.5)

    Returns:
        dict with probabilities, edge, recommendation, kelly fraction
    """
    # Calculate probabilities
    over_probability = np.mean(simulation_results > market_line)
    under_probability = np.mean(simulation_results < market_line)
    push_probability = np.mean(simulation_results == market_line)

    # Convert probabilities to American odds
    if over_probability >= 0.5:
        implied_over_odds = int(-100 * (over_probability / (1 - over_probability)))
    else:
        implied_over_odds = int(100 * ((1 - over_probability) / over_probability))

    # Calculate edge (assuming -110 market odds)
    market_implied_prob = 110 / 210  # -110 = 52.38% implied

    if over_probability > market_implied_prob:
        edge = ((over_probability - market_implied_prob) / market_implied_prob) * 100
        recommendation = "OVER"
        kelly_fraction = (over_probability - (1 - over_probability)) / 1  # Kelly Criterion
    elif under_probability > market_implied_prob:
        edge = ((under_probability - market_implied_prob) / market_implied_prob) * 100
        recommendation = "UNDER"
        kelly_fraction = (under_probability - (1 - under_probability)) / 1
    else:
        edge = 0
        recommendation = "PASS"
        kelly_fraction = 0

    # Use half Kelly for safety
    kelly_fraction = kelly_fraction / 2
    kelly_fraction = max(0, min(kelly_fraction, 0.10))  # Cap at 10%

    return {
        "market_line": market_line,
        "over_probability": round(over_probability, 3),
        "under_probability": round(under_probability, 3),
        "push_probability": round(push_probability, 3),
        "implied_over_odds": implied_over_odds,
        "market_over_odds": -110,
        "edge": round(edge, 1),
        "recommendation": recommendation,
        "kelly_fraction": round(kelly_fraction, 3)
    }
```

#### Step 4: Create Distribution Buckets

```python
def create_distribution_buckets(simulation_results, bucket_size=5):
    """
    Group simulation results into buckets for histogram display

    Args:
        simulation_results: np.array of final totals
        bucket_size: int (default 5 points per bucket)

    Returns:
        dict: {"210-215": 156, "215-220": 892, ...}
    """
    min_val = int(np.min(simulation_results))
    max_val = int(np.max(simulation_results))

    buckets = {}
    current = (min_val // bucket_size) * bucket_size

    while current <= max_val:
        bucket_label = f"{current}-{current + bucket_size}"
        count = np.sum((simulation_results >= current) & (simulation_results < current + bucket_size))
        buckets[bucket_label] = int(count)
        current += bucket_size

    return buckets
```

#### Step 5: FastAPI Endpoint

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import numpy as np

router = APIRouter(prefix="/api/simulation", tags=["simulation"])

class SimulationRequest(BaseModel):
    game_id: str
    current_state: Optional[Dict] = None  # {quarter, time_remaining, home_score, away_score}
    n_simulations: int = 10000

@router.post("/monte-carlo")
async def run_monte_carlo_simulation(request: SimulationRequest):
    """
    Run Monte Carlo simulation for game totals

    Returns probability distribution and betting recommendations
    """
    try:
        # 1. Fetch team stats (pace, PPP, etc.)
        team_stats = get_team_stats_for_game(request.game_id)

        # 2. Fetch current market line
        market_line = get_market_total_line(request.game_id)

        # 3. Calculate remaining possessions
        remaining_possessions = calculate_remaining_possessions(
            request.current_state,
            team_stats
        )

        # 4. Run simulation
        current_scores = (0, 0)
        if request.current_state:
            current_scores = (
                request.current_state['home_score'],
                request.current_state['away_score']
            )

        simulation_results = simulate_game_possession_by_possession(
            home_stats=team_stats['home'],
            away_stats=team_stats['away'],
            remaining_possessions=remaining_possessions,
            current_scores=current_scores,
            n_simulations=request.n_simulations
        )

        # 5. Calculate statistics
        current_total = sum(current_scores)
        percentiles = {
            'p10': float(np.percentile(simulation_results, 10)),
            'p25': float(np.percentile(simulation_results, 25)),
            'p50': float(np.percentile(simulation_results, 50)),
            'p75': float(np.percentile(simulation_results, 75)),
            'p90': float(np.percentile(simulation_results, 90)),
        }

        market_analysis = calculate_market_analysis(simulation_results, market_line)
        distribution_buckets = create_distribution_buckets(simulation_results)

        # 6. Build response
        return {
            "current_total": current_total,
            "simulations_run": request.n_simulations,
            "mean_final_total": round(float(np.mean(simulation_results)), 1),
            "median_final_total": round(float(np.median(simulation_results)), 1),
            "std_dev": round(float(np.std(simulation_results)), 1),
            "percentiles": percentiles,
            "market_analysis": market_analysis,
            "distribution_buckets": distribution_buckets,
            "confidence_intervals": {
                "90%": [percentiles['p10'], percentiles['p90']],
                "95%": [float(np.percentile(simulation_results, 2.5)), float(np.percentile(simulation_results, 97.5))],
                "99%": [float(np.percentile(simulation_results, 0.5)), float(np.percentile(simulation_results, 99.5))]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")
```

---

## Phase 2: Random Forest Model (PRIORITY 2)

### File to Create
`backend/models/random_forest_totals.py`

### Why Random Forest for NBA Totals?
Per the guide:
- Handles non-linear relationships (pace × efficiency)
- Captures interaction effects (matchups)
- Less prone to overfitting than XGBoost
- Works with limited features

### Endpoint Specification

**Route:** `POST /api/models/random-forest/predict`

**Request:**
```json
{
  "game_id": "nba_20251108_LAL_BOS"
}
```

**Response:**
```json
{
  "predicted_total": 226.8,
  "confidence": 0.75,
  "feature_importance": {
    "home_pace": 0.25,
    "away_pace": 0.23,
    "home_off_rating": 0.18,
    "away_off_rating": 0.17,
    "rest_days": 0.10,
    "home_court": 0.07
  },
  "model_performance": {
    "mae": 7.8,
    "rmse": 10.1,
    "r2": 0.42
  }
}
```

### Implementation Template

```python
from sklearn.ensemble import RandomForestRegressor
import joblib
import numpy as np

class RandomForestTotalsPredictor:
    def __init__(self, model_path=None):
        if model_path and os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            # Initialize new model
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=10,
                random_state=42
            )

    def prepare_features(self, game_data):
        """
        Extract features for prediction

        Features (in order):
        1. home_pace
        2. away_pace
        3. home_off_rating
        4. away_off_rating
        5. home_def_rating
        6. away_def_rating
        7. home_rest_days
        8. away_rest_days
        9. home_court (1 or 0)
        10. home_l5_pace
        11. away_l5_pace
        """
        features = [
            game_data['home_pace'],
            game_data['away_pace'],
            game_data['home_off_rating'],
            game_data['away_off_rating'],
            game_data['home_def_rating'],
            game_data['away_def_rating'],
            game_data['home_rest_days'],
            game_data['away_rest_days'],
            1,  # home court advantage
            game_data['home_l5_pace'],
            game_data['away_l5_pace']
        ]
        return np.array(features).reshape(1, -1)

    def predict(self, game_data):
        """
        Predict game total using Random Forest
        """
        X = self.prepare_features(game_data)
        prediction = self.model.predict(X)[0]

        # Calculate confidence (using ensemble std dev)
        tree_predictions = [tree.predict(X)[0] for tree in self.model.estimators_]
        std_dev = np.std(tree_predictions)
        confidence = 1 / (1 + std_dev)  # Higher std = lower confidence

        return {
            "predicted_total": round(prediction, 1),
            "confidence": round(confidence, 2),
            "std_dev": round(std_dev, 1)
        }
```

---

## Phase 3: Multi-Model Ensemble (PRIORITY 3)

### Endpoint Specification

**Route:** `POST /api/models/ensemble/predict`

**Response:**
```json
{
  "predictions": {
    "monte_carlo": {"total": 227.3, "confidence": 0.78},
    "random_forest": {"total": 226.8, "confidence": 0.75},
    "xgboost": {"total": 224.2, "confidence": 0.72},
    "linear_regression": {"total": 225.5, "confidence": 0.68},
    "ensemble": {"total": 226.0, "confidence": 0.82}
  },
  "recommendation": "ensemble",
  "market_line": 228.5,
  "edge": -2.5
}
```

---

## Testing Strategy

### 1. Test with Mock Data First
```python
# Test endpoint with fake data before connecting to real game data
mock_request = {
    "game_id": "test_game_001",
    "current_state": {
        "quarter": 2,
        "time_remaining": "6:30",
        "home_score": 55,
        "away_score": 52
    },
    "n_simulations": 1000
}
```

### 2. Validate Response Shape
Ensure every field in the response matches the frontend expectations exactly.

### 3. Performance Test
- 10,000 simulations should complete in < 5 seconds
- If slower, optimize possession loop with NumPy vectorization

---

## Questions for C1?

1. **Do you have access to team pace/efficiency stats?**
   - Need: pace, offensive rating, defensive rating, PPP

2. **Do you have the current market total line for games?**
   - Frontend needs this for edge calculation

3. **Should I build a data fetching layer first?**
   - Or can you use existing game_tracker data?

---

## Summary

**Build these in order:**
1. ✅ Monte Carlo simulation endpoint (Phase 1)
2. Random Forest prediction (Phase 2)
3. Multi-model ensemble (Phase 3)

**Frontend is ready and waiting for Phase 1 endpoint!**

The SimulationModal will automatically call the endpoint when a user clicks the "🎲 Simulate" button on any game card.
