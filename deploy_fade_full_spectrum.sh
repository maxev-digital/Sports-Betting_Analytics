#!/bin/bash

# Deploy 40% Fade - Full Spectrum
# Date: 2025-11-15

VPS_IP="148.230.87.135"
VPS_USER="root"
VPS_PATH="/root/sporttrader"

echo "========================================"
echo "40% FADE - FULL SPECTRUM DEPLOYMENT"
echo "========================================"
echo "VPS: $VPS_USER@$VPS_IP"
echo ""

# Step 1: Deploy Backend - Fade Strategy Module
echo "[1/8] Deploying fade strategy module..."
ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP "mkdir -p $VPS_PATH/backend/strategies/fade"
scp -i ~/.ssh/hostinger_vps -r "D:/Max_EV_Sports/reorganized/backend/strategies/fade/"* $VPS_USER@$VPS_IP:$VPS_PATH/backend/strategies/fade/
echo "[OK] Fade strategy module deployed"

# Step 2: Deploy Database Module
echo "[2/8] Deploying fade positions database..."
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/reorganized/backend/database/fade_positions_db.py" $VPS_USER@$VPS_IP:$VPS_PATH/backend/database/
echo "[OK] Database module deployed"

# Step 3: Deploy API Routes
echo "[3/8] Deploying fade API routes..."
ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP "mkdir -p $VPS_PATH/backend/api/routes"
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/reorganized/backend/api/routes/fade.py" $VPS_USER@$VPS_IP:$VPS_PATH/backend/api/routes/
echo "[OK] API routes deployed"

# Step 4: Deploy Game Enrichment Module
echo "[4/8] Deploying fade game enrichment..."
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/reorganized/backend/fade_game_enrichment.py" $VPS_USER@$VPS_IP:$VPS_PATH/backend/
echo "[OK] Game enrichment deployed"

# Step 5: Deploy Frontend Components
echo "[5/8] Deploying frontend components..."
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/components/FadeAlertCard.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/components/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/pages/FadePositions.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/pages/
echo "[OK] Frontend components deployed"

# Step 6: Update main.py to register fade router
echo "[6/8] Registering fade router in main.py..."
ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP << 'EOF'
cd /root/sporttrader/backend

# Backup main.py
cp main.py main.py.backup_fade_$(date +%Y%m%d_%H%M%S)

# Add fade router import and registration after volatility router
python3 << 'PYTHON_EOF'
import re

with open('main.py', 'r') as f:
    content = f.read()

# Check if already added
if 'from api.routes.fade import router as fade_router' in content:
    print('[SKIP] Fade router already registered')
    exit(0)

# Add import after volatility import
import_pattern = r'(from api\.routes\.volatility_arb import router as volatility_arb_router)'
import_replacement = r'\1\nfrom api.routes.fade import router as fade_router'

if re.search(import_pattern, content):
    content = re.sub(import_pattern, import_replacement, content)
    print('[OK] Added fade router import')
else:
    print('[ERROR] Could not find volatility import')
    exit(1)

# Add router registration after volatility registration
register_pattern = r'(app\.include_router\(volatility_arb_router\)[\s\S]*?print\("DEBUG: Volatility arb router registered[^"]*"\))'
register_replacement = r'''\1

# Import and register Fade router
try:
    print("DEBUG: About to import fade router...")
    app.include_router(fade_router)
    print("DEBUG: Fade router registered - 40% Fade system ready")
except Exception as e:
    print(f"ERROR importing/registering fade router: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()'''

if re.search(register_pattern, content):
    content = re.sub(register_pattern, register_replacement, content)
    print('[OK] Added fade router registration')
else:
    print('[ERROR] Could not find volatility registration')
    exit(1)

# Write back
with open('main.py', 'w') as f:
    f.write(content)

print('[OK] Main.py updated with fade router')
PYTHON_EOF

EOF

echo "[OK] Fade router registered"

# Step 7: Add fade enrichment to /api/games endpoint
echo "[7/8] Adding fade enrichment to /api/games..."
ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP << 'EOF'
cd /root/sporttrader/backend

python3 << 'PYTHON_EOF'
import re

with open('main.py', 'r') as f:
    content = f.read()

# Check if already added
if 'from fade_game_enrichment import enrich_games_with_fade' in content:
    print('[SKIP] Fade enrichment already added')
    exit(0)

# Add import after volatility detector import
import_pattern = r'(from volatility_detector_simple import detect_volatility_opportunities)'
import_replacement = r'\1\nfrom fade_game_enrichment import enrich_games_with_fade, serialize_games_with_fade'

content = re.sub(import_pattern, import_replacement, content)

# Replace serialize_games_with_volatility with version that handles both
pattern = r'def serialize_games_with_volatility\(games\):[\s\S]*?return games_dicts'
replacement = '''def serialize_games_with_volatility(games):
    """Serialize games to dicts, preserving volatility_opportunity and fade_opportunity"""
    games_dicts = []
    for game in games:
        game_dict = game.model_dump()
        # Add volatility_opportunity if present
        if hasattr(game, '__dict__') and 'volatility_opportunity' in game.__dict__:
            game_dict['volatility_opportunity'] = game.__dict__['volatility_opportunity']
        # Add fade_opportunity if present
        if hasattr(game, '__dict__') and 'fade_opportunity' in game.__dict__:
            game_dict['fade_opportunity'] = game.__dict__['fade_opportunity']
        games_dicts.append(game_dict)
    return games_dicts'''

content = re.sub(pattern, replacement, content)

# Add fade enrichment call after volatility enrichment
pattern = r'(# Detect volatility opportunities\s+filtered_games = detect_volatility_opportunities\(filtered_games\))'
replacement = r'''\1

        # Detect fade opportunities
        filtered_games = enrich_games_with_fade(filtered_games)'''

content = re.sub(pattern, replacement, content)

# Also add to show_all branch
pattern2 = r'(games = detect_volatility_opportunities\(games\))'
replacement2 = r'''\1
            # Detect fade opportunities
            games = enrich_games_with_fade(games)'''

content = re.sub(pattern2, replacement2, content)

# Write back
with open('main.py', 'w') as f:
    f.write(content)

print('[OK] Fade enrichment added to /api/games')
PYTHON_EOF

EOF

echo "[OK] Fade enrichment integrated"

# Step 8: Build frontend and restart services
echo "[8/8] Building frontend and restarting services..."
ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP << 'EOF'
cd /root/sporttrader

# Update App.tsx to add FadePositions route
cd frontend/src
if ! grep -q "FadePositions" App.tsx; then
    python3 << 'PYTHON_EOF'
import re

with open('App.tsx', 'r') as f:
    content = f.read()

# Add import
if 'FadePositions' not in content:
    pattern = r'(import VolatilityPositions from.*)'
    replacement = r"\1\nimport FadePositions from './pages/FadePositions'"
    content = re.sub(pattern, replacement, content)

    # Add route
    pattern2 = r'(<Route path="/volatility-positions" element={<VolatilityPositions />} />)'
    replacement2 = r'\1\n          <Route path="/fade-positions" element={<FadePositions />} />'
    content = re.sub(pattern2, replacement2, content)

    with open('App.tsx', 'w') as f:
        f.write(content)

    print('[OK] Added FadePositions route to App.tsx')
else:
    print('[SKIP] FadePositions already in App.tsx')
PYTHON_EOF
fi

cd /root/sporttrader

echo "Building frontend..."
cd frontend
npm run build

echo "Copying build to web directory..."
rm -rf /var/www/sporttrader/*
cp -r dist/* /var/www/sporttrader/

echo "Restarting backend service..."
systemctl restart sporttrader

echo "Reloading nginx..."
systemctl reload nginx

echo "Checking service status..."
sleep 3
systemctl status sporttrader --no-pager -l | head -20

echo ""
echo "[OK] Services restarted"
EOF

echo ""
echo "========================================"
echo "40% FADE DEPLOYMENT COMPLETE"
echo "========================================"
echo ""
echo "[OK] Backend: Fade strategy module deployed"
echo "[OK] Backend: Fade router registered"
echo "[OK] Backend: Game enrichment integrated"
echo "[OK] Frontend: Components deployed and built"
echo "[OK] Services: Restarted and running"
echo ""
echo "Access at: https://max-ev-sports.com"
echo ""
echo "ENDPOINTS:"
echo "  GET  /api/fade/info           - Strategy info"
echo "  GET  /api/games               - Games with fade opportunities"
echo "  POST /api/fade/positions      - Create fade position"
echo "  GET  /api/fade/positions      - Get your positions"
echo "  GET  /api/fade/performance    - Performance by tier"
echo "  POST /api/fade/kelly          - Kelly stake calculator"
echo ""
echo "FRONTEND:"
echo "  /#/fade-positions             - Track positions"
echo "  /#/live-games                 - See fade alerts on game cards"
echo ""
echo "Test API:"
echo "  curl https://max-ev-sports.com/api/fade/info"
echo ""

