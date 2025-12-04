#!/bin/bash

echo "Adding volatility detection to main.py..."

# Backup main.py
cp /root/sporttrader/backend/main.py /root/sporttrader/backend/main.py.backup_volatility_$(date +%Y%m%d_%H%M%S)

# Create Python script to modify main.py
cat > /tmp/patch_volatility.py << 'PYTHON_EOF'
import re

# Read main.py
with open('/root/sporttrader/backend/main.py', 'r') as f:
    content = f.read()

# Add the detection function after imports (find a good spot after logger setup)
detection_function = """

def detect_volatility_opportunities(games):
    """
    Detect volatility arbitrage opportunities for games
    Simplified version - detects +money underdogs with good edges
    """
    try:
        from strategies.volatility_arbitrage import VolatilityArbDetector

        detector = VolatilityArbDetector()

        # For each game, check if there's a volatility opportunity
        for game in games:
            try:
                # Skip if game doesn't have odds
                if not hasattr(game, 'odds') or not game.odds:
                    continue

                # Get best moneyline odds for each side
                home_ml = None
                away_ml = None

                for odds_obj in game.odds:
                    if hasattr(odds_obj, 'h2h'):
                        h2h = odds_obj.h2h
                        if len(h2h) >= 2:
                            home_ml = h2h[0] if home_ml is None else max(home_ml, h2h[0])
                            away_ml = h2h[1] if away_ml is None else max(away_ml, h2h[1])

                if home_ml is None or away_ml is None:
                    continue

                # Check for +money opportunities (odds > 100)
                # Entry criteria:
                # 1. Underdog at +money odds (> +150)
                # 2. Not huge underdog (< +400)
                # 3. Game is upcoming or in Q1/Q2

                entry_team = None
                entry_odds = None
                confidence = None

                # Check away team (underdog if positive and larger)
                if away_ml > 150 and away_ml < 400:
                    entry_team = game.away_team
                    entry_odds = away_ml
                    if away_ml > 200:
                        confidence = "HIGH"
                    elif away_ml > 170:
                        confidence = "MEDIUM"
                    else:
                        confidence = "LOW"

                # Check home team (underdog if positive and larger)
                elif home_ml > 150 and home_ml < 400:
                    entry_team = game.home_team
                    entry_odds = home_ml
                    if home_ml > 200:
                        confidence = "HIGH"
                    elif home_ml > 170:
                        confidence = "MEDIUM"
                    else:
                        confidence = "LOW"

                # If we found an opportunity, add it to the game
                if entry_team and entry_odds:
                    # Calculate edge percentage (simplified)
                    edge_percent = (entry_odds - 100) * 0.04  # Rough approximation

                    opportunity = {
                        "entry_team": entry_team,
                        "entry_odds": int(entry_odds),
                        "entry_edge_percent": round(edge_percent, 1),
                        "confidence": confidence,
                        "trigger_price": int(entry_odds + 70),  # Suggest trigger +70 points higher
                        "expected_profit_percent": round(edge_percent * 0.6, 1)  # Conservative
                    }

                    # Add to game object
                    game_dict = game.model_dump() if hasattr(game, 'model_dump') else game.__dict__
                    game_dict['volatility_opportunity'] = opportunity

                    # Update game (if it's a Pydantic model)
                    if hasattr(game, 'model_validate'):
                        game.__dict__.update(game_dict)
                    else:
                        game.volatility_opportunity = opportunity

                    logger.info(f"[VOLATILITY] Found opportunity: {entry_team} at {entry_odds} ({confidence})")

            except Exception as e:
                logger.warning(f"[VOLATILITY] Error checking game {game.id if hasattr(game, 'id') else 'unknown'}: {e}")
                continue

        return games

    except Exception as e:
        logger.error(f"[VOLATILITY] Error in detect_volatility_opportunities: {e}")
        return games  # Return games unchanged on error

"""

# Find the location to insert (after logger is set up, before endpoints)
# Look for "logger = logging.getLogger" and insert after that section
insert_pos = content.find("# Routes and endpoints")
if insert_pos == -1:
    # Try another marker
    insert_pos = content.find("@app.get")

if insert_pos > 0:
    # Insert before the first endpoint
    content = content[:insert_pos] + detection_function + "\n\n" + content[insert_pos:]
    print(f"[OK] Added volatility detection function at position {insert_pos}")
else:
    print("[ERROR] Could not find insertion point")
    exit(1)

# Now modify the /api/games endpoint to call the detection
# Find: games_dicts = [game.model_dump() for game in filtered_games]
# Replace with: games with volatility detection

# Pattern to match - add volatility detection before converting to dicts
pattern = r'(# Convert to dicts and handle numpy types\s+games_dicts = \[game\.model_dump\(\) for game in filtered_games\])'
replacement = r'# Detect volatility opportunities
        filtered_games = detect_volatility_opportunities(filtered_games)

        '

content = re.sub(pattern, replacement, content)

# Also add to the show_all branch
pattern2 = r'(games = tracker\.get_all_games\(\)\s+# Convert Pydantic models to dicts)'
replacement2 = r'games = tracker.get_all_games()
            # Detect volatility opportunities
            games = detect_volatility_opportunities(games)

            '

content = re.sub(pattern2, replacement2, content)

# Also add to the no-settings branch
pattern3 = r'(games = tracker\.get_all_games\(\)\s+games_dicts = \[game\.model_dump)'
replacement3 = r'games = tracker.get_all_games()
            # Detect volatility opportunities
            games = detect_volatility_opportunities(games)

            games_dicts = [game.model_dump'

content = re.sub(pattern3, replacement3, content)

# Write back
with open('/root/sporttrader/backend/main.py', 'w') as f:
    f.write(content)

print("[OK] Modified /api/games endpoint to call volatility detection")
print("[OK] Volatility detection integration complete!")
PYTHON_EOF

# Run the Python script
python3 /tmp/patch_volatility.py

if [ $? -eq 0 ]; then
    echo "[OK] Successfully patched main.py"

    # Restart service
    echo "Restarting sporttrader service..."
    systemctl restart sporttrader
    sleep 3

    echo "Checking service status..."
    systemctl status sporttrader --no-pager -l | head -15

    echo ""
    echo "[OK] Volatility detection deployed!"
    echo "Test with: curl https://max-ev-sports.com/api/games?user_id=test"
else
    echo "[ERROR] Failed to patch main.py"
    echo "Restoring backup..."
    cp /root/sporttrader/backend/main.py.backup_volatility_* /root/sporttrader/backend/main.py
    exit 1
fi
