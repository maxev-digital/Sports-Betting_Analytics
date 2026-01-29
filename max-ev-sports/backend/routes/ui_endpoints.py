"""
UI Endpoints - BULLETPROOF ARCHITECTURE
==============================================
SACRED CONTRACT - Frontend ONLY calls these endpoints
All data is pre-computed. Frontend is 100% dumb - just renders.

Required Routes (per bulletproof spec):
- /api/ui/best-plays        - Daily edges/best plays
- /api/ui/model-performance - Model performance stats
- /api/ui/live-games        - Live game data
- /api/ui/props-edges       - Player props edges
- /api/ui/historical-predictions - Past predictions
- /api/ui/odds-comparison   - Odds across books
- /api/ui/analytics-summary - Dashboard analytics
"""

from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
from backend_utils.timezone import get_cst_now, get_cst_today
import pandas as pd
import numpy as np
import sqlite3
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ui", tags=["UI Endpoints - Bulletproof"])

# Data directories
DATA_DIR = Path("/root/sporttrader/backend/data")
TRACKING_DIR = DATA_DIR / "tracking"
PREDICTIONS_DIR = DATA_DIR / "predictions"
RESULTS_LOG = TRACKING_DIR / "results_log_COMBINED.csv"
PROPS_DB = DATA_DIR / "player_props.db"
PREDICTIONS_DB = Path("/root/sporttrader/backend/ml/predictions.db")  # SINGLE SOURCE OF TRUTH


# ============================================================================
# HELPER FUNCTIONS - All formatting happens here, NOT in frontend
# ============================================================================

def format_percentage(value: float, include_sign: bool = False) -> str:
    """Format a decimal as percentage string"""
    if value is None or np.isnan(value):
        return "N/A"
    pct = value * 100 if abs(value) < 1 else value
    sign = "+" if include_sign and pct > 0 else ""
    return f"{sign}{pct:.1f}%"


def format_units(value: float) -> str:
    """Format units won/lost"""
    if value is None or np.isnan(value):
        return "0.00u"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}u"


def format_money(value: float) -> str:
    """Format as currency"""
    if value is None or np.isnan(value):
        return "$0"
    sign = "+" if value > 0 else "-"
    return f"{sign}${abs(value):,.0f}"


def format_record(wins: int, losses: int, pushes: int = 0) -> str:
    """Format W-L-P record"""
    if pushes > 0:
        return f"{wins}W-{losses}L-{pushes}P"
    return f"{wins}W-{losses}L"


def format_odds(odds: int) -> str:
    """Format American odds"""
    if odds is None:
        return "N/A"
    return f"+{odds}" if odds > 0 else str(odds)


def calculate_kelly(edge_pct: float, odds: int = -110) -> dict:
    """Calculate Kelly criterion fractions - ALL MATH BACKEND ONLY"""
    if edge_pct is None or edge_pct <= 0:
        return {"full": 0, "half": 0, "quarter": 0, "recommended": "0%"}

    decimal_odds = (odds / 100) + 1 if odds > 0 else (100 / abs(odds)) + 1
    implied_prob = 1 / decimal_odds
    true_prob = implied_prob + (edge_pct / 100)
    b = decimal_odds - 1

    kelly_pct = max(0, (b * true_prob - (1 - true_prob)) / b)
    full_kelly = min(kelly_pct * 100, 25)  # Cap at 25%

    return {
        "full": round(full_kelly, 2),
        "half": round(full_kelly * 0.5, 2),
        "quarter": round(full_kelly * 0.25, 2),
        "recommended": f"{full_kelly * 0.5:.1f}%"  # Half Kelly recommended
    }


def get_confidence_color(confidence: str) -> str:
    """Return color for confidence level"""
    colors = {
        "HIGH": "#22c55e",      # green
        "MEDIUM": "#eab308",    # yellow
        "LOW": "#ef4444"        # red
    }
    return colors.get(confidence.upper(), "#6b7280")


def get_result_color(result: str) -> str:
    """Return color for result"""
    colors = {
        "WIN": "#22c55e",
        "LOSS": "#ef4444",
        "PUSH": "#6b7280",
        "PENDING": "#3b82f6"
    }
    return colors.get(result.upper(), "#6b7280")


# ============================================================================
# ROUTE 1: /api/ui/best-plays (alias: daily-edges)
# ============================================================================


# Helper functions for NULL-safe string operations
def safe_str_upper(val):
    """Safely convert value to uppercase string, handling None/NULL"""
    if val is None or (isinstance(val, str) and val.strip() == ''):
        return ''
    return str(val).upper()

def safe_str_title(val):
    """Safely convert value to title case string, handling None/NULL"""
    if val is None or (isinstance(val, str) and val.strip() == ''):
        return ''
    return str(val).title()

def safe_str(val):
    """Safely convert value to string, handling None/NULL"""
    if val is None:
        return ''
    return str(val)

@router.get("/best-plays")
@router.get("/daily-edges")  # Alias for backwards compatibility
async def get_best_plays(
    sport: str = Query(None, description="Filter by sport"),
    min_edge: float = Query(2.0, description="Minimum edge percentage"),
    confidence: str = Query(None, description="Filter by confidence level"),
    bet_type: str = Query(None, description="Filter by bet type (spreads, totals, moneyline)"),
    limit: int = Query(50, description="Maximum results")
):
    """
    Returns today's best betting plays from predictions.db - SINGLE SOURCE OF TRUTH.
    Frontend just renders this data.
    """
    try:
        from zoneinfo import ZoneInfo
        CST = ZoneInfo("America/Chicago")
        today_cst = datetime.now(CST).strftime("%Y-%m-%d")

        conn = sqlite3.connect(PREDICTIONS_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Calculate next Sunday for NFL/NCAAF week filter
        from datetime import timedelta
        now_cst = datetime.now(CST)
        days_until_sunday = (6 - now_cst.weekday()) % 7
        if days_until_sunday == 0:  # If today is Sunday
            days_until_sunday = 7  # Go to next Sunday
        next_sunday = (now_cst + timedelta(days=days_until_sunday)).strftime("%Y-%m-%d")

        # SMART DATE FILTERING: Sport-specific date ranges
        # NBA, NHL, NCAAB: Show today's games + tomorrow's early games (before 6am)
        # NFL, NCAAF: Show next 6 days (they play weekly on weekends)
        # Calculate all date offsets upfront
        tomorrow = (now_cst + timedelta(days=1)).strftime("%Y-%m-%d")
        six_days_out = (now_cst + timedelta(days=6)).strftime("%Y-%m-%d")
        seven_days_out = (now_cst + timedelta(days=7)).strftime("%Y-%m-%d")
        current_time = now_cst.strftime("%H:%M")

        # FIX: Match API sport codes (basketball_nba, icehockey_nhl, etc) AND account for DB date offset
        sport_upper = sport.upper() if sport else ""

        if sport_upper in ['AMERICANFOOTBALL_NFL', 'NFL', 'AMERICANFOOTBALL_NCAAF', 'NCAAF']:
            # NFL/NCAAF: Show upcoming games within next 6 days (weekly schedule)
            where_clauses = ["game_date >= ? AND game_date <= ?", "ABS(edge) >= ?"]
            params = [today_cst, six_days_out, min_edge]
        elif sport_upper in ['BASKETBALL_NBA', 'NBA', 'ICEHOCKEY_NHL', 'NHL', 'BASKETBALL_NCAAB', 'NCAAB']:
            # NBA/NHL/NCAAB: Show ONLY today's games (daily schedule)
            # FIX: DB dates are 1 day ahead - tomorrow in DB = today's games
            where_clauses = ["game_date = ?", "ABS(edge) >= ?"]
            params = [tomorrow, min_edge]  # FIX: Use tomorrow instead of today_cst
        else:
            # All sports: Show today + next 6 days for full view
            # FIX: Since NBA/NHL/NCAAB dates are +1, show tomorrow to 7 days out
            where_clauses = ["game_date >= ? AND game_date <= ?", "ABS(edge) >= ?"]
            params = [tomorrow, seven_days_out, min_edge]  # FIX: Start from tomorrow

        if sport:
            where_clauses.append("UPPER(sport) = ?")
            params.append(sport.upper())
        if confidence:
            where_clauses.append("UPPER(confidence) = ?")
            params.append(confidence.upper())
        if bet_type:
            where_clauses.append("LOWER(bet_type) = ?")
            params.append(bet_type.lower())

        where_sql = " AND ".join(where_clauses)
        params.append(limit)

        query = f"""
            SELECT * FROM predictions
            WHERE {where_sql}
            ORDER BY ABS(edge) DESC
            LIMIT ?
        """

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        plays = []
        for row in rows:
            edge = row["edge"] or 0
            bet_type = (row["bet_type"] or "").lower()

            # Use stored Kelly from database (already calculated correctly)
            stored_kelly_pct = row["kelly_pct"] if "kelly_pct" in row.keys() else 0.0

            # Convert to Kelly fractions for display
            # Database stores full Kelly (e.g., 0.05 = 5%)
            # Frontend expects half Kelly for "recommended"
            kelly = {
                "full": round(stored_kelly_pct * 100, 2),
                "half": round(stored_kelly_pct * 100 * 0.5, 2),
                "quarter": round(stored_kelly_pct * 100 * 0.25, 2),
                "recommended": f"{stored_kelly_pct * 100 * 0.5:.1f}%"
            }

            # Default odds for display
            odds = -110

            # Calculate edge percentage (points * 2.5% for totals/spreads)
            if bet_type in ['totals', 'spreads']:
                edge_pct = abs(edge) * 2.5
            else:  # moneyline
                edge_pct = abs(edge)

            # Convert probability from decimal to percentage
            model_prob = (row["over_probability"] or 0.5) * 100

            plays.append({
                # Frontend-expected fields (MaxEvEdges.tsx compatibility)
                "id": row["prediction_id"] or "",
                "recommendation": row["recommendation"] or "",
                "model_prediction": row["predicted_value"],
                "market_line": row["market_value"],
                "edge_percentage": round(edge_pct, 2),
                "model_confidence": round(row["over_probability"] or 0.5, 3),
                "kelly_fraction": kelly["half"] / 100 if kelly["half"] else 0,
                "model_name": row["model"] or "ensemble",
                "consensus": {
                    "models_agree": row["models_agree"] if "models_agree" in row.keys() else 1,
                    "models_total": row["models_total"] if "models_total" in row.keys() else 1,
                    "strength": row["consensus_strength"] if "consensus_strength" in row.keys() else "MODERATE"
                },
                "game_id": row["prediction_id"] or "",
                "market": (row["bet_type"] or "").title(),
                "edge": round(abs(edge), 2),
                "suggested_bet_size": kelly["recommended"],
                "probability": round(model_prob, 1),
                "features_used": {},
                "model_performance": {},
                "score": round(abs(edge) * (row["over_probability"] or 0.5), 2),
                
                # Additional fields for display
                "sport": (row["sport"] or "").upper(),
                "game_date": row["game_date"] or today_cst,
                "game_time": row["game_time"] or "TBD",
                "home_team": row["home_team"] or "",
                "away_team": row["away_team"] or "",
                "matchup": f"{row['away_team'] or ''} @ {row['home_team'] or ''}",
                "bet_type": (row["bet_type"] or "").title(),
                "odds": odds,
                "display_odds": format_odds(odds),
                "display_edge": format_percentage(abs(edge)),
                "confidence": (row["confidence"] or "MEDIUM").upper(),
                "confidence_color": get_confidence_color(row["confidence"] or "MEDIUM"),
                "kelly": kelly,
                "display_kelly": kelly["recommended"],
                "best_book": "FanDuel",
            })

        return {
            "plays": plays,
            "count": len(plays),
            "date": today_cst,
            "filters": {"sport": sport, "min_edge": min_edge, "confidence": confidence, "bet_type": bet_type},
            "source": "predictions.db",
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in best-plays: {e}")
        import traceback
        traceback.print_exc()
        return {"plays": [], "count": 0, "error": str(e), "generated_at": datetime.utcnow().isoformat()}


# ============================================================================
# ROUTE 2: /api/ui/model-performance
# ============================================================================

@router.get("/model-performance")
async def get_model_performance(
    sport: str = Query(None),
    model: str = Query(None),
    bet_type: str = Query(None),
    days: int = Query(30),
    unit_size: int = Query(100),
    bankroll: int = Query(10000)
):
    """
    Returns FULLY FORMATTED model performance data.
    Frontend should just render - no calculations.
    """
    try:
        # BULLETPROOF: Read from predictions.db results table - SINGLE SOURCE OF TRUTH
        if not PREDICTIONS_DB.exists():
            return {"error": "No data available", "generated_at": datetime.utcnow().isoformat()}

        conn = sqlite3.connect(PREDICTIONS_DB)

        # Calculate cutoff date
        cutoff = (get_cst_now().replace(tzinfo=None) - timedelta(days=days)).strftime('%Y-%m-%d')

        # Load results from database (DATABASE_CLEANUP_PLAN_DEC17_2025.md - filter invalid predictions)
        query = """
            SELECT
                prediction_id, sport, bet_type, game_date,
                away_team, home_team, predicted_value, market_value,
                recommendation, confidence, result, profit_loss, model
            FROM results
            WHERE game_date >= ?
              AND result IN ('WIN', 'LOSS', 'PUSH')
              AND (valid_prediction IS NULL OR valid_prediction = 1)
        """
        df = pd.read_sql_query(query, conn, params=[cutoff])
        conn.close()

        df['game_date'] = pd.to_datetime(df['game_date'], format='mixed', errors='coerce')

        # Add edge column for compatibility
        if 'edge' not in df.columns:
            df['edge'] = df['predicted_value'] - df['market_value']

        # Store unfiltered df for moneyline analysis (needs all bet types)
        df_unfiltered = df.copy()

        # Apply filters
        if sport:
            df = df[df['sport'].str.lower() == sport.lower()]
            df_unfiltered = df_unfiltered[df_unfiltered['sport'].str.lower() == sport.lower()]
        if model:
            df = df[df['model'].str.lower() == model.lower()]
            df_unfiltered = df_unfiltered[df_unfiltered['model'].str.lower() == model.lower()]
        if bet_type:
            df = df[df['bet_type'].str.lower() == bet_type.lower()]
            # Don't filter df_unfiltered by bet_type - we need all for the matrices

        if len(df) == 0:
            return {"error": "No data for selected filters", "generated_at": datetime.utcnow().isoformat()}

        # Calculate metrics
        total = len(df)
        wins = len(df[df['result'] == 'WIN'])
        losses = len(df[df['result'] == 'LOSS'])
        pushes = len(df[df['result'] == 'PUSH'])
        decided = wins + losses
        win_rate = wins / decided if decided > 0 else 0

        # Calculate P&L from filtered dataset (respects user's model selection)
        # No capping - use actual profit_loss values to show true moneyline profitability
        units_won = (df['profit_loss'].sum() / 100) if 'profit_loss' in df.columns else 0
        roi = (units_won / total) if total > 0 else 0
        avg_edge = df['edge'].abs().mean() if 'edge' in df.columns else 0
        kelly = calculate_kelly(avg_edge)
        pnl_dollars = units_won * unit_size

        # By sport breakdown
        by_sport = {}
        for sport_name in df['sport'].dropna().unique():
            s_df = df[df['sport'] == sport_name]
            s_wins = len(s_df[s_df['result'] == 'WIN'])
            s_losses = len(s_df[s_df['result'] == 'LOSS'])
            s_pushes = len(s_df[s_df['result'] == 'PUSH'])
            s_decided = s_wins + s_losses
            s_wr = s_wins / s_decided if s_decided > 0 else 0
            s_units = (s_df['profit_loss'].sum() / 100) if 'profit_loss' in s_df.columns else 0

            by_sport[sport_name.upper()] = {
                "total": len(s_df),
                "wins": s_wins,
                "losses": s_losses,
                "pushes": s_pushes,
                "record": format_record(s_wins, s_losses, s_pushes),
                "win_rate": round(s_wr, 4),
                "display_win_rate": format_percentage(s_wr),
                "units": round(s_units, 2),
                "display_units": format_units(s_units),
                "roi": round((s_units / len(s_df)) if len(s_df) > 0 else 0, 4),
                "display_roi": format_percentage((s_units / len(s_df)) * 100 if len(s_df) > 0 else 0, include_sign=True),
                "pnl_dollars": round(s_units * unit_size, 0),
                "display_pnl": format_money(s_units * unit_size)
            }

        # By model breakdown
        by_model = {}
        for model_name in df['model'].dropna().unique():
            m_df = df[df['model'] == model_name]
            m_wins = len(m_df[m_df['result'] == 'WIN'])
            m_losses = len(m_df[m_df['result'] == 'LOSS'])
            m_pushes = len(m_df[m_df['result'] == 'PUSH'])
            m_decided = m_wins + m_losses
            m_wr = m_wins / m_decided if m_decided > 0 else 0
            m_units = (m_df['profit_loss'].sum() / 100) if 'profit_loss' in m_df.columns else 0

            by_model[model_name.lower()] = {
                "total": len(m_df),
                "wins": m_wins,
                "losses": m_losses,
                "pushes": m_pushes,
                "record": format_record(m_wins, m_losses, m_pushes),
                "win_rate": round(m_wr, 4),
                "display_win_rate": format_percentage(m_wr),
                "units": round(m_units, 2),
                "display_units": format_units(m_units)
            }

        # By confidence breakdown
        by_confidence = {}
        for conf in ['HIGH', 'MEDIUM', 'LOW']:
            c_df = df[df['confidence'] == conf]
            if len(c_df) > 0:
                c_wins = len(c_df[c_df['result'] == 'WIN'])
                c_losses = len(c_df[c_df['result'] == 'LOSS'])
                c_pushes = len(c_df[c_df['result'] == 'PUSH'])
                c_decided = c_wins + c_losses
                c_wr = c_wins / c_decided if c_decided > 0 else 0

                by_confidence[conf.lower()] = {
                    "total": len(c_df),
                    "wins": c_wins,
                    "losses": c_losses,
                    "pushes": c_pushes,
                    "record": format_record(c_wins, c_losses, c_pushes),
                    "win_rate": round(c_wr, 4),
                    "display_win_rate": format_percentage(c_wr),
                    "color": get_confidence_color(conf)
                }


        # DAILY BREAKDOWN for charts (BULLETPROOF)
        df['date'] = df['game_date'].dt.date
        history_data = []
        cumulative_units = 0
        
        for date_val in sorted(df['date'].dropna().unique()):
            day_df = df[df['date'] == date_val]
            day_wins = len(day_df[day_df['result'] == 'WIN'])
            day_losses = len(day_df[day_df['result'] == 'LOSS'])
            day_decided = day_wins + day_losses
            day_wr = day_wins / day_decided if day_decided > 0 else 0
            day_units = (day_df['profit_loss'].sum() / 100) if 'profit_loss' in day_df.columns else 0
            cumulative_units += day_units
            
            history_data.append({
                "period": str(date_val),
                "predictions": len(day_df),
                "wins": day_wins,
                "losses": day_losses,
                "win_rate": round(day_wr, 4),
                "daily_win_rate": round(day_wr, 4),
                "roi": round((cumulative_units / total) if total > 0 else 0, 4),
                "daily_roi": round((day_units / len(day_df)) if len(day_df) > 0 else 0, 4),
                "units_won": round(cumulative_units, 2),
                "pnl_dollars": round(cumulative_units * unit_size, 0)
            })
        
        # RECENT PREDICTIONS for table (BULLETPROOF)
        recent_preds = df.sort_values('game_date', ascending=False).head(50)
        predictions_list = []
        for _, row in recent_preds.iterrows():
            predictions_list.append({
                "prediction_id": row.get('prediction_id', ''),
                "game_date": str(row.get('game_date', '')),
                "sport": row.get('sport', ''),
                "away_team": row.get('away_team', ''),
                "home_team": row.get('home_team', ''),
                "bet_type": row.get('bet_type', ''),
                "predicted_value": round(float(row.get('predicted_value', 0)), 1),
                "market_value": round(float(row.get('market_value', 0)), 1),
                "edge": round(float(row.get('edge', 0)), 1),
                "recommendation": row.get('recommendation', ''),
                "confidence": row.get('confidence', ''),
                "model": row.get('model', ''),
                "result": row.get('result', 'PENDING'),
                "profit_loss": int(row.get('profit_loss', 0))
            })
        
        # MODELS LIST (BULLETPROOF)
        models_list = [
            {"name": "all", "description": "All Models Combined", "type": "meta"},
            {"name": "ensemble", "description": "Neural Ensemble", "type": "deep_learning"},
            {"name": "pytorch", "description": "PyTorch TabularNet", "type": "deep_learning"},
            {"name": "catboost", "description": "CatBoost", "type": "ml"},
            {"name": "xgboost", "description": "XGBoost", "type": "ml"},
            {"name": "lightgbm", "description": "LightGBM", "type": "ml"},
            {"name": "random_forest", "description": "Random Forest", "type": "ml"},
            {"name": "linear", "description": "Linear Regression", "type": "baseline"}
        ]

        # ============================================================================
        # DETAILED BREAKDOWNS - Matching MD Report Format
        # Use df_unfiltered to show all bet types even when filtering
        # ============================================================================

        # By Bet Type Breakdown
        by_bet_type = {}
        for bet_type_name in df_unfiltered['bet_type'].dropna().unique():
            bt_df = df_unfiltered[df_unfiltered['bet_type'] == bet_type_name]
            bt_wins = len(bt_df[bt_df['result'] == 'WIN'])
            bt_losses = len(bt_df[bt_df['result'] == 'LOSS'])
            bt_pushes = len(bt_df[bt_df['result'] == 'PUSH'])
            bt_decided = bt_wins + bt_losses
            bt_wr = bt_wins / bt_decided if bt_decided > 0 else 0
            bt_units = (bt_df['profit_loss'].sum() / 100) if 'profit_loss' in bt_df.columns else 0
            bt_roi = (bt_units / len(bt_df)) * 100 if len(bt_df) > 0 else 0

            by_bet_type[bet_type_name.lower()] = {
                "total": len(bt_df),
                "wins": bt_wins,
                "losses": bt_losses,
                "pushes": bt_pushes,
                "record": format_record(bt_wins, bt_losses, bt_pushes),
                "win_rate": round(bt_wr, 4),
                "units": round(bt_units, 2),
                "roi": round(bt_roi, 2),
                "avg_profit_per_bet": round((bt_units * unit_size) / len(bt_df), 2) if len(bt_df) > 0 else 0
            }

        # Sport × Bet Type Matrix
        sport_bet_matrix = {}
        for sport_name in df_unfiltered['sport'].dropna().unique():
            sport_bet_matrix[sport_name.upper()] = {}
            for bet_type_name in df_unfiltered['bet_type'].dropna().unique():
                sb_df = df_unfiltered[(df_unfiltered['sport'] == sport_name) & (df_unfiltered['bet_type'] == bet_type_name)]
                if len(sb_df) > 0:
                    sb_wins = len(sb_df[sb_df['result'] == 'WIN'])
                    sb_losses = len(sb_df[sb_df['result'] == 'LOSS'])
                    sb_pushes = len(sb_df[sb_df['result'] == 'PUSH'])
                    sb_decided = sb_wins + sb_losses
                    sb_wr = sb_wins / sb_decided if sb_decided > 0 else 0
                    sb_units = (sb_df['profit_loss'].sum() / 100) if 'profit_loss' in sb_df.columns else 0
                    sb_roi = (sb_units / len(sb_df)) * 100 if len(sb_df) > 0 else 0

                    sport_bet_matrix[sport_name.upper()][bet_type_name.lower()] = {
                        "total": len(sb_df),
                        "wins": sb_wins,
                        "losses": sb_losses,
                        "pushes": sb_pushes,
                        "win_rate": round(sb_wr, 4),
                        "units": round(sb_units, 2),
                        "roi": round(sb_roi, 2)
                    }

        # Sport × Model Matrix
        sport_model_matrix = {}
        for sport_name in df_unfiltered['sport'].dropna().unique():
            sport_model_matrix[sport_name.upper()] = {}
            for model_name in df_unfiltered['model'].dropna().unique():
                sm_df = df_unfiltered[(df_unfiltered['sport'] == sport_name) & (df_unfiltered['model'] == model_name)]
                if len(sm_df) > 0:
                    sm_wins = len(sm_df[sm_df['result'] == 'WIN'])
                    sm_losses = len(sm_df[sm_df['result'] == 'LOSS'])
                    sm_decided = sm_wins + sm_losses
                    sm_wr = sm_wins / sm_decided if sm_decided > 0 else 0
                    sm_units = (sm_df['profit_loss'].sum() / 100) if 'profit_loss' in sm_df.columns else 0

                    sport_model_matrix[sport_name.upper()][model_name.lower()] = {
                        "total": len(sm_df),
                        "wins": sm_wins,
                        "losses": sm_losses,
                        "win_rate": round(sm_wr, 4),
                        "units": round(sm_units, 2)
                    }

        # Moneyline Analysis (Favorite vs Underdog with Odds Ranges)
        moneyline_analysis = {}
        ml_df = df_unfiltered[df_unfiltered['bet_type'] == 'moneyline']
        if len(ml_df) > 0:
            # Separate favorites and underdogs based on actual odds used
            favorites = []
            underdogs = []

            for _, row in ml_df.iterrows():
                # Skip if no odds available
                home_ml = row['home_ml'] if 'home_ml' in row else None
                away_ml = row['away_ml'] if 'away_ml' in row else None

                # Check for NaN first (pandas converts SQL NULL to NaN)
                if pd.isna(home_ml) or pd.isna(away_ml):
                    continue

                # Determine which team was recommended and get their odds
                recommendation = row['recommendation'] if 'recommendation' in row else ''
                home_team = row['home_team'] if 'home_team' in row else ''
                away_team = row['away_team'] if 'away_team' in row else ''

                # Recommendation can be "HOME", "AWAY", or the actual team name
                if recommendation == 'HOME' or recommendation == home_team:
                    odds = home_ml
                elif recommendation == 'AWAY' or recommendation == away_team:
                    odds = away_ml
                else:
                    continue

                row_dict = row.to_dict()
                row_dict['actual_odds_used'] = int(odds)

                if odds < 0:
                    favorites.append(row_dict)
                else:
                    underdogs.append(row_dict)

            # Calculate favorite stats
            if favorites:
                fav_df = pd.DataFrame(favorites)
                fav_wins = len(fav_df[fav_df['result'] == 'WIN'])
                fav_losses = len(fav_df[fav_df['result'] == 'LOSS'])
                fav_decided = fav_wins + fav_losses
                fav_wr = fav_wins / fav_decided if fav_decided > 0 else 0
                fav_units = (fav_df['profit_loss'].sum() / 100) if 'profit_loss' in fav_df.columns else 0

                moneyline_analysis['favorites'] = {
                    "total": len(fav_df),
                    "wins": fav_wins,
                    "losses": fav_losses,
                    "win_rate": round(fav_wr, 4),
                    "units": round(fav_units, 2),
                    "roi": round((fav_units / len(fav_df)) * 100, 2) if len(fav_df) > 0 else 0
                }

            # Calculate underdog stats
            if underdogs:
                dog_df = pd.DataFrame(underdogs)
                dog_wins = len(dog_df[dog_df['result'] == 'WIN'])
                dog_losses = len(dog_df[dog_df['result'] == 'LOSS'])
                dog_decided = dog_wins + dog_losses
                dog_wr = dog_wins / dog_decided if dog_decided > 0 else 0
                dog_units = (dog_df['profit_loss'].sum() / 100) if 'profit_loss' in dog_df.columns else 0

                moneyline_analysis['underdogs'] = {
                    "total": len(dog_df),
                    "wins": dog_wins,
                    "losses": dog_losses,
                    "win_rate": round(dog_wr, 4),
                    "units": round(dog_units, 2),
                    "roi": round((dog_units / len(dog_df)) * 100, 2) if len(dog_df) > 0 else 0
                }

                # Odds ranges for underdogs (matching MD report)
                odds_ranges = {
                    "100-300": (100, 300),
                    "301-500": (301, 500),
                    "501-1000": (501, 1000),
                    "1001+": (1001, 100000)
                }

                by_odds_range = {}
                for range_name, (low, high) in odds_ranges.items():
                    range_rows = [r for r in underdogs if low <= r.get('actual_odds_used', 0) <= high]
                    if range_rows:
                        range_df = pd.DataFrame(range_rows)
                        r_wins = len(range_df[range_df['result'] == 'WIN'])
                        r_losses = len(range_df[range_df['result'] == 'LOSS'])
                        r_decided = r_wins + r_losses
                        r_wr = r_wins / r_decided if r_decided > 0 else 0
                        r_units = (range_df['profit_loss'].sum() / 100) if 'profit_loss' in range_df.columns else 0

                        by_odds_range[range_name] = {
                            "total": len(range_df),
                            "wins": r_wins,
                            "losses": r_losses,
                            "win_rate": round(r_wr, 4),
                            "units": round(r_units, 2),
                            "avg_profit_per_bet": round((r_units * unit_size) / len(range_df), 2) if len(range_df) > 0 else 0
                        }

                moneyline_analysis['by_odds_range'] = by_odds_range

        return {
            "summary": {
                "total_predictions": total,
                "wins": wins,
                "losses": losses,
                "pushes": pushes,
                "record": format_record(wins, losses, pushes),
                "win_rate": round(win_rate, 4),
                "display_win_rate": format_percentage(win_rate),
                "units_won": round(units_won, 2),
                "display_units": format_units(units_won),
                "roi": round(roi, 2),
                "display_roi": format_percentage(roi, include_sign=True),
                "pnl_dollars": round(pnl_dollars, 0),
                "display_pnl": format_money(pnl_dollars),
                "avg_edge": round(avg_edge, 2),
                "kelly": kelly,
                "time_period": f"Last {days} days"
            },
            "by_sport": by_sport,
            "by_model": by_model,
            "by_confidence": by_confidence,
            "by_bet_type": by_bet_type,
            "sport_bet_matrix": sport_bet_matrix,
            "sport_model_matrix": sport_model_matrix,
            "moneyline_analysis": moneyline_analysis,
            "history": history_data,
            "predictions": predictions_list,
            "predictions_total": len(df),
            "models": models_list,
            "filters": {"sport": sport, "model": model, "bet_type": bet_type, "days": days},
            "settings": {"unit_size": unit_size, "bankroll": bankroll},
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in model-performance: {e}")
        return {"error": str(e), "generated_at": datetime.utcnow().isoformat()}


# ============================================================================
# ROUTE 3: /api/ui/live-games
# ============================================================================

@router.get("/live-games")
async def get_live_games(
    sport: str = Query(None, description="Filter by sport")
):
    """
    Returns live/upcoming games with predictions - FULLY FORMATTED.
    """
    try:
        today = get_cst_now().strftime("%Y-%m-%d")
        predictions_file = PREDICTIONS_DIR / f"all_predictions_{today}.csv"

        if not predictions_file.exists():
            pred_files = list(PREDICTIONS_DIR.glob("all_predictions_*.csv"))
            if pred_files:
                predictions_file = max(pred_files, key=lambda x: x.stat().st_mtime)
            else:
                return {"games": [], "count": 0, "generated_at": datetime.utcnow().isoformat()}

        df = pd.read_csv(predictions_file)

        if sport:
            df = df[df['sport'].str.upper() == sport.upper()]

        # Group by game
        games = []
        for game_id in df['game_id'].unique():
            game_df = df[df['game_id'] == game_id]
            first_row = game_df.iloc[0]

            # Get predictions for this game
            preds = []
            for _, row in game_df.iterrows():
                preds.append({
                    "bet_type": row.get('bet_type', '').title(),
                    "pick": row.get('recommendation', ''),
                    "edge": round(row.get('edge', 0), 2),
                    "display_edge": format_percentage(row.get('edge', 0)),
                    "confidence": row.get('confidence', 'MEDIUM').upper(),
                    "confidence_color": get_confidence_color(row.get('confidence', 'MEDIUM'))
                })

            games.append({
                "game_id": game_id,
                "sport": first_row.get('sport', '').upper(),
                "game_time": first_row.get('game_time', ''),
                "home_team": first_row.get('home_team', ''),
                "away_team": first_row.get('away_team', ''),
                "matchup": f"{first_row.get('away_team', '')} @ {first_row.get('home_team', '')}",
                "status": "upcoming",
                "predictions": preds
            })

        return {
            "games": games,
            "count": len(games),
            "sport_filter": sport,
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in live-games: {e}")
        return {"games": [], "count": 0, "error": str(e), "generated_at": datetime.utcnow().isoformat()}


# ============================================================================
# ROUTE 4: /api/ui/props-edges
# ============================================================================

@router.get("/props-edges")
async def get_props_edges(
    sport: str = Query("nba", description="Sport (nba, nfl, nhl)"),
    min_edge: float = Query(5.0, description="Minimum edge percentage"),
    limit: int = Query(50, description="Maximum results")
):
    """
    Returns player props edges - FULLY FORMATTED.
    """
    try:
        if not PROPS_DB.exists():
            return {"props": [], "count": 0, "error": "Props database not found", "generated_at": datetime.utcnow().isoformat()}

        conn = sqlite3.connect(str(PROPS_DB))

        query = """
            SELECT * FROM player_props_predictions
            WHERE date(prediction_date) >= date('now', '-2 days')
            AND ABS(edge_pct) >= ?
            ORDER BY ABS(edge_pct) DESC
            LIMIT ?
        """

        df = pd.read_sql_query(query, conn, params=[min_edge, limit])
        conn.close()

        props = []
        for _, row in df.iterrows():
            edge = row.get('edge_pct', 0)
            kelly = calculate_kelly(abs(edge))

            # Convert confidence from float to category
            conf_val = row.get('confidence', 50.0)
            if isinstance(conf_val, (int, float)):
                if conf_val >= 80:
                    conf_str = 'HIGH'
                elif conf_val >= 60:
                    conf_str = 'MEDIUM'
                else:
                    conf_str = 'LOW'
            else:
                conf_str = str(conf_val).upper()

            # Determine over/under odds based on recommendation
            if row.get('recommendation', '') == 'OVER':
                over_odds = -110
                under_odds = None
            elif row.get('recommendation', '') == 'UNDER':
                over_odds = None
                under_odds = -110
            else:
                over_odds = -110
                under_odds = -110

            props.append({
                "player_name": row.get('player_name', ''),
                "team": row.get('team', ''),
                "opponent": row.get('opponent', ''),
                "home_away": row.get('home_away', 'HOME'),
                "prop_type": row.get('prop_type', '').replace('_', ' ').title(),
                "market_line": row.get('market_line', 0),
                "predicted_value": row.get('predicted_value', row.get('market_line', 0)),
                "edge": round(row.get('edge', 0), 1),
                "edge_pct": round(abs(edge), 1),
                "recommendation": row.get('recommendation', ''),
                "confidence": round(conf_val, 1),
                "over_odds": over_odds,
                "under_odds": under_odds,
                "bookmaker": 'DraftKings',
                "models_used": [],
                "date": row.get('prediction_date', ''),
                # Legacy fields for backwards compatibility
                "pick": row.get('recommendation', ''),
                "odds": -110,
                "display_odds": format_odds(-110),
                "display_edge": format_percentage(abs(edge)),
                "model_probability": round(conf_val, 1),
                "confidence_color": get_confidence_color(conf_str),
                "kelly": kelly,
                "display_kelly": kelly["recommended"],
                "best_book": 'DraftKings',
                "game_time": ''
            })

        return {
            "date": datetime.utcnow().strftime('%Y-%m-%d'),
            "time_generated": datetime.utcnow().isoformat(),
            "total_props_analyzed": len(props),
            "props_with_edge": len(props),
            "min_edge_pct": min_edge,
            "props": props,
            "edges": props,  # Also include 'edges' for frontend compatibility
            "count": len(props),
            "total": len(props),  # For frontend compatibility
            "filters": {"sport": sport, "min_edge": min_edge},
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in props-edges: {e}")
        return {"props": [], "count": 0, "error": str(e), "generated_at": datetime.utcnow().isoformat()}


# ============================================================================
# ROUTE 5: /api/ui/historical-predictions
# ============================================================================

# Best model configuration - which model is best for each sport/bet_type
BEST_MODELS_CONFIG = {
    'NBA': {'totals': 'xgboost', 'moneyline': 'lightgbm', 'spreads': 'xgboost'},
    'NHL': {'totals': 'xgboost', 'moneyline': 'random_forest', 'spreads': 'xgboost'},
    'NCAAB': {'totals': 'xgboost', 'moneyline': 'xgboost', 'spreads': 'xgboost'},
    'NFL': {'totals': 'ensemble', 'moneyline': 'ensemble', 'spreads': 'ensemble'},
    'NCAAF': {'totals': 'ensemble', 'moneyline': 'ensemble', 'spreads': 'ensemble'},
}

def is_best_model(sport: str, bet_type: str, model: str) -> bool:
    """Check if this model is the best for this sport/bet_type combo"""
    sport_upper = (sport or '').upper()
    bet_type_lower = (bet_type or '').lower()
    model_lower = (model or '').lower()
    best = BEST_MODELS_CONFIG.get(sport_upper, {}).get(bet_type_lower, '')
    return model_lower == best.lower() if best else False


@router.get("/historical-predictions")
async def get_historical_predictions(
    sport: str = Query(None),
    days: int = Query(7),
    result: str = Query(None, description="WIN, LOSS, PUSH, or PENDING"),
    limit: int = Query(100),
    model: str = Query(None, description="Filter by model: xgboost, lightgbm, ensemble, etc."),
    best_model_only: bool = Query(False, description="Only show predictions from the best model for each sport/bet_type")
):
    """
    Returns historical predictions - FULLY FORMATTED.
    BULLETPROOF: Uses predictions.db as single source of truth

    New features:
    - best_model_only: Filter to only show predictions from the designated best model
    - is_best_model: Flag on each prediction showing if it's from the best model
    - Includes scores, odds, and actual results
    """
    try:
        if not PREDICTIONS_DB.exists():
            return {"predictions": [], "count": 0, "generated_at": datetime.utcnow().isoformat()}

        # Connect to database
        conn = sqlite3.connect(PREDICTIONS_DB)

        # Calculate cutoff date
        cutoff = (get_cst_now().replace(tzinfo=None) - timedelta(days=days)).strftime('%Y-%m-%d')

        # Build query with filters - NOW INCLUDES SCORES AND ODDS
        query = """
            SELECT
                r.prediction_id,
                r.sport,
                r.bet_type,
                r.game_date,
                r.away_team,
                r.home_team,
                r.predicted_value,
                r.market_value,
                r.recommendation,
                r.confidence,
                r.result,
                r.profit_loss,
                r.model,
                r.away_score,
                r.home_score,
                r.actual_total,
                r.home_ml,
                r.away_ml,
                (r.predicted_value - r.market_value) as edge
            FROM results r
            WHERE r.game_date >= ?
        """

        params = [cutoff]

        if sport:
            query += " AND UPPER(r.sport) = UPPER(?)"
            params.append(sport)

        if result:
            query += " AND UPPER(r.result) = UPPER(?)"
            params.append(result)

        if model:
            query += " AND LOWER(r.model) = LOWER(?)"
            params.append(model)

        query += " ORDER BY r.game_date DESC LIMIT ?"
        params.append(limit * 3 if best_model_only else limit)  # Fetch more if filtering
        
        # Load data from database
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        if len(df) == 0:
            return {"predictions": [], "count": 0, "generated_at": datetime.utcnow().isoformat()}
        
        df['game_date'] = pd.to_datetime(df['game_date'], format='mixed', errors='coerce')

        predictions = []
        for _, row in df.iterrows():
            # Safely extract values with NULL handling
            sport_val = safe_str_upper(row.get("sport"))
            bet_type_val = safe_str_title(row.get("bet_type"))
            confidence_val = safe_str_upper(row.get("confidence")) or "MEDIUM"
            result_val = safe_str_upper(row.get("result"))

            # Calculate proper edge percentage (not just point difference)
            predicted_value = float(row.get("predicted_value") or 0)
            market_value = float(row.get("market_value") or 0)

            # For totals/spreads: edge is the difference in implied probabilities
            # We approximate this using a simple heuristic based on how far off the prediction is
            # A larger difference = higher edge
            raw_diff = abs(predicted_value - market_value)

            # Edge calculation:
            # For totals/spreads at -110 odds, each point difference roughly = 2-3% edge
            # This is a simplified model, but works for display purposes
            if bet_type_val.lower() in ['totals', 'spreads']:
                edge_pct = raw_diff * 2.5  # Points difference * 2.5% per point
            else:  # Moneyline
                # For moneylines, use profit_loss to infer edge
                # This is already calculated with actual odds
                edge_pct = abs(raw_diff) if raw_diff > 0 else 0

            # Model probability (approximation based on confidence)
            # HIGH confidence = 60-65%, MEDIUM = 55-60%, LOW = 52-55%
            confidence_map = {
                'HIGH': 0.625,
                'MEDIUM': 0.575,
                'LOW': 0.535
            }
            model_prob = confidence_map.get(confidence_val, 0.55)

            # Calculate Kelly (using standard -110 odds for totals/spreads)
            kelly_result = calculate_kelly(edge_pct, -110)

            # Get model name and check if it's the best model for this sport/bet_type
            model_name = safe_str(row.get("model")) or "ensemble"
            is_best = is_best_model(sport_val, bet_type_val, model_name)

            # Skip if best_model_only filter is on and this isn't the best model
            if best_model_only and not is_best:
                continue

            # Get market odds (use home_ml or away_ml based on recommendation)
            recommendation = safe_str(row.get("recommendation"))
            home_ml = row.get("home_ml")
            away_ml = row.get("away_ml")
            if bet_type_val.lower() == 'moneyline':
                if recommendation and 'home' in recommendation.lower():
                    market_odds_val = int(home_ml) if pd.notna(home_ml) else None
                else:
                    market_odds_val = int(away_ml) if pd.notna(away_ml) else None
            else:
                # For totals/spreads, use standard -110 odds
                market_odds_val = -110

            predictions.append({
                "prediction_id": safe_str(row.get("prediction_id")),
                "game_date": row["game_date"].strftime("%Y-%m-%d") if pd.notna(row.get("game_date")) else "",
                "game_time": "",
                "sport": sport_val,
                "away_team": safe_str(row.get("away_team")),
                "home_team": safe_str(row.get("home_team")),
                "bet_type": bet_type_val,
                "model": model_name,
                "predicted_value": predicted_value,
                "market_value": market_value,
                "edge": round(edge_pct, 2),  # Now percentage edge
                "model_prob": round(model_prob * 100, 1),  # Model probability as percentage
                "kelly": kelly_result["quarter"],  # Quarter Kelly (conservative)
                "recommendation": recommendation,
                "confidence": confidence_val,
                "bet_placed": "",
                "actual_total": float(row.get("actual_total") or 0) if pd.notna(row.get("actual_total")) else None,
                "away_score": int(row.get("away_score") or 0) if pd.notna(row.get("away_score")) else None,
                "home_score": int(row.get("home_score") or 0) if pd.notna(row.get("home_score")) else None,
                "result": result_val if result_val else None,
                "profit_loss": float(row.get("profit_loss") or 0),
                "market_odds": market_odds_val,
                "odds_source": "fanduel",
                "is_best_model": is_best  # NEW: Flag indicating if this is the best model pick
            })

            # Stop if we've reached the limit after filtering
            if len(predictions) >= limit:
                break

        return {
            "predictions": predictions,
            "count": len(predictions),
            "filters": {"sport": sport, "days": days, "result": result, "model": model, "best_model_only": best_model_only},
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in historical-predictions: {e}")
        return {"predictions": [], "count": 0, "error": str(e), "generated_at": datetime.utcnow().isoformat()}


# ============================================================================
# ROUTE 6: /api/ui/odds-comparison
# ============================================================================

@router.get("/odds-comparison")
async def get_odds_comparison(
    sport: str = Query(None),
    game_id: str = Query(None)
):
    """
    Returns odds comparison across sportsbooks - FULLY FORMATTED.
    """
    try:
        # For now, return placeholder structure
        # TODO: Integrate with odds API data
        return {
            "games": [],
            "books": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "PointsBet"],
            "sport_filter": sport,
            "generated_at": datetime.utcnow().isoformat(),
            "note": "Odds comparison data coming soon"
        }

    except Exception as e:
        logger.error(f"Error in odds-comparison: {e}")
        return {"games": [], "error": str(e), "generated_at": datetime.utcnow().isoformat()}


# ============================================================================
# ROUTE 7: /api/ui/analytics-summary
# ============================================================================

@router.get("/analytics-summary")
async def get_analytics_summary(
    days: int = Query(30)
):
    """
    Returns dashboard analytics summary - FULLY FORMATTED.
    """
    try:
        # BULLETPROOF: Read from predictions.db results table - SINGLE SOURCE OF TRUTH
        if not PREDICTIONS_DB.exists():
            return {"error": "No data available", "generated_at": datetime.utcnow().isoformat()}

        conn = sqlite3.connect(PREDICTIONS_DB)

        # Calculate cutoff date
        cutoff = (get_cst_now().replace(tzinfo=None) - timedelta(days=days)).strftime('%Y-%m-%d')

        # Load results from database
        query = """
            SELECT
                prediction_id, sport, bet_type, game_date,
                away_team, home_team, predicted_value, market_value,
                recommendation, confidence, result, profit_loss, model
            FROM results
            WHERE game_date >= ?
        """
        df = pd.read_sql_query(query, conn, params=[cutoff])
        conn.close()

        df['game_date'] = pd.to_datetime(df['game_date'], format='mixed', errors='coerce')

        # Add edge column for compatibility
        if 'edge' not in df.columns:
            df['edge'] = df['predicted_value'] - df['market_value']

        if len(df) == 0:
            return {"error": "No data for period", "generated_at": datetime.utcnow().isoformat()}

        # Overall stats
        total = len(df)
        wins = len(df[df['result'] == 'WIN'])
        losses = len(df[df['result'] == 'LOSS'])
        decided = wins + losses
        win_rate = wins / decided if decided > 0 else 0

        # Use ensemble for P&L
        ensemble_df = df[df['model'] == 'ensemble'] if 'model' in df.columns else df
        units_won = (ensemble_df['profit_loss'].sum() / 100) if 'profit_loss' in ensemble_df.columns else 0
        roi = (units_won / total) if total > 0 else 0

        # Daily breakdown for chart
        daily_data = []
        df_by_date = df.groupby(df['game_date'].dt.date).agg({
            'result': lambda x: (x == 'WIN').sum(),
            'profit_loss': 'sum'
        }).reset_index()

        cumulative_units = 0
        for _, row in df_by_date.iterrows():
            cumulative_units += row['profit_loss'] / 100
            daily_data.append({
                "date": str(row['game_date']),
                "wins": int(row['result']),
                "cumulative_units": round(cumulative_units, 2)
            })

        return {
            "summary": {
                "total_predictions": total,
                "win_rate": round(win_rate, 4),
                "display_win_rate": format_percentage(win_rate),
                "units_won": round(units_won, 2),
                "display_units": format_units(units_won),
                "roi": round(roi, 2),
                "display_roi": format_percentage(roi, include_sign=True),
                "time_period": f"Last {days} days"
            },
            "daily_data": daily_data,
            "sports_active": list(df['sport'].dropna().unique()),
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in analytics-summary: {e}")
        return {"error": str(e), "generated_at": datetime.utcnow().isoformat()}


# ============================================================================
# ROUTE 8: /api/ui/injury-alerts
# ============================================================================

@router.get("/injury-alerts")
async def get_injury_alerts():
    """
    Returns recent injury prop alerts - FULLY FORMATTED.
    """
    try:
        alerts_file = DATA_DIR / "alerts" / "injury_alerts.json"

        if not alerts_file.exists():
            return {
                "alerts": [],
                "count": 0,
                "message": "No injury alerts available",
                "generated_at": datetime.utcnow().isoformat()
            }

        # Read alerts file
        with open(alerts_file, 'r') as f:
            alerts_data = json.load(f)

        # Ensure it's a list
        if isinstance(alerts_data, dict):
            alerts_data = [alerts_data]

        # Filter to recent alerts (last 24 hours)
        recent_alerts = []
        cutoff_time = datetime.utcnow() - timedelta(hours=24)

        for alert in alerts_data:
            try:
                alert_time = datetime.fromisoformat(alert.get('timestamp', '2000-01-01'))
                if alert_time >= cutoff_time:
                    recent_alerts.append(alert)
            except:
                # If timestamp parsing fails, include the alert anyway
                recent_alerts.append(alert)

        return {
            "alerts": recent_alerts,
            "count": len(recent_alerts),
            "total_opportunities": sum(alert.get('opportunities_count', 0) for alert in recent_alerts),
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in injury-alerts: {e}")
        return {
            "alerts": [],
            "count": 0,
            "error": str(e),
            "generated_at": datetime.utcnow().isoformat()
        }


# ============================================================================
# ROUTE 9: /api/ui/line-movements (alias: alerts/line-movements)
# ============================================================================

@router.get("/line-movements")
@router.get("/alerts/line-movements")  # Alias for frontend compatibility
async def get_line_movements():
    """
    Returns current line movements showing model prediction vs market line.
    Shows where our models see value - like tracking sharp money movement.
    """
    try:
        from zoneinfo import ZoneInfo
        CST = ZoneInfo("America/Chicago")
        today_cst = datetime.now(CST).strftime("%Y-%m-%d")

        # Get today's plays with significant edges from predictions.db
        conn = sqlite3.connect(PREDICTIONS_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get predictions with edge >= 2 points
        query = """
            SELECT sport, home_team, away_team, bet_type,
                   predicted_value, market_value, edge, confidence
            FROM predictions
            WHERE game_date = ?
              AND ABS(edge) >= 2
            ORDER BY ABS(edge) DESC
            LIMIT 20
        """

        cursor.execute(query, [today_cst])
        rows = cursor.fetchall()
        conn.close()

        alerts = []
        for row in rows:
            # Format as line movement data
            sport = (row["sport"] or "").upper()
            bet_type = (row["bet_type"] or "").lower()
            predicted = row["predicted_value"] or 0
            market = row["market_value"] or 0
            edge = row["edge"] or 0

            # Calculate movement (difference between model and market)
            movement = predicted - market

            # Format market type
            if bet_type == "totals":
                market_type = "TOT"
            elif bet_type == "spreads":
                market_type = "SPR"
            else:
                market_type = "ML"

            alerts.append({
                "home_team": row["home_team"] or "",
                "away_team": row["away_team"] or "",
                "sport": sport,
                "market_type": market_type,
                "bookmaker": "Model",  # Our model vs market
                "original_line": market,  # Market line
                "new_line": predicted,    # Model prediction
                "movement": round(movement, 1),
                "edge": round(edge, 1),
                "confidence": (row["confidence"] or "MEDIUM").upper()
            })

        return {
            "alerts": alerts,
            "count": len(alerts),
            "date": today_cst,
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error in line-movements: {e}")
        return {
            "alerts": [],
            "count": 0,
            "error": str(e),
            "generated_at": datetime.utcnow().isoformat()
        }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def ui_health():
    """Health check for UI endpoints"""
    return {
        "status": "healthy",
        "endpoints": [
            "/api/ui/best-plays",
            "/api/ui/model-performance",
            "/api/ui/live-games",
            "/api/ui/props-edges",
            "/api/ui/historical-predictions",
            "/api/ui/odds-comparison",
            "/api/ui/analytics-summary",
            "/api/ui/injury-alerts",
            "/api/ui/line-movements"
        ],
        "architecture": "BULLETPROOF",
        "generated_at": datetime.utcnow().isoformat()
    }
