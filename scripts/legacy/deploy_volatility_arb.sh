#!/bin/bash

# Deploy Volatility Arbitrage System to Production VPS
# Date: 2025-11-15

VPS_IP="148.230.87.135"
VPS_USER="root"
VPS_PATH="/root/sporttrader"

echo "========================================"
echo "🚀 Deploying Volatility Arbitrage to VPS"
echo "========================================"
echo "VPS: $VPS_USER@$VPS_IP"
echo ""

# Step 1: Deploy Backend - Volatility Arbitrage Module
echo "[1/6] Deploying volatility_arbitrage strategy module..."
scp -i ~/.ssh/hostinger_vps -r "D:/Max_EV_Sports/reorganized/backend/strategies/volatility_arbitrage" $VPS_USER@$VPS_IP:$VPS_PATH/backend/strategies/
echo "✅ Strategy module copied"

# Step 2: Deploy Database Module
echo "[2/6] Deploying volatility positions database module..."
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/reorganized/backend/database/volatility_positions_db.py" $VPS_USER@$VPS_IP:$VPS_PATH/backend/database/
echo "✅ Database module copied"

# Step 3: Deploy API Routes
echo "[3/6] Deploying volatility_arb API routes..."
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/reorganized/backend/api/routes/volatility_arb.py" $VPS_USER@$VPS_IP:$VPS_PATH/backend/api/routes/
echo "✅ API routes copied"

# Step 4: Deploy Updated main.py
echo "[4/6] Deploying updated main.py..."
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/reorganized/backend/main.py" $VPS_USER@$VPS_IP:$VPS_PATH/backend/
echo "✅ main.py updated"

# Step 5: Deploy Frontend Components
echo "[5/6] Deploying frontend components..."
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/pages/VolatilityPositions.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/pages/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/components/ToastAlert.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/components/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/components/VolatilityEntryCard.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/components/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/components/HedgeAlertModal.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/components/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/components/VolatilityPerformance.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/components/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/services/volatilityAlertService.ts" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/services/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/App.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/types.ts" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/
scp -i ~/.ssh/hostinger_vps "D:/Max_EV_Sports/current_vps/frontend/src/components/GameCard.tsx" $VPS_USER@$VPS_IP:$VPS_PATH/frontend/src/components/
echo "✅ Frontend components copied"

# Step 6: Build frontend and restart services
echo "[6/6] Building frontend and restarting services..."
ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP << 'EOF'
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
echo "✅ Services restarted"
EOF

echo ""
echo "========================================"
echo "🎉 Deployment Complete!"
echo "========================================"
echo ""
echo "✅ Backend: Volatility arbitrage module deployed"
echo "✅ Frontend: All components deployed and built"
echo "✅ Services: Restarted and running"
echo ""
echo "Access at: http://max-ev-sports.com"
echo ""
echo "Check backend logs:"
echo "  ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP 'journalctl -u sporttrader -n 50 --no-pager'"
echo ""
echo "Test API endpoint:"
echo "  curl http://max-ev-sports.com/api/volatility/info"
echo ""
