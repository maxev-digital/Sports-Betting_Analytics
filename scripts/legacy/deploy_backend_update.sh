#!/bin/bash
# Deploy updated backend code to production VPS
# VPS IP: 148.230.87.135

set -e

VPS_IP="148.230.87.135"
VPS_USER="root"
SSH_KEY="~/.ssh/hostinger_vps"
LOCAL_BACKEND="C:/Users/nashr/backend"
LOCAL_FRONTEND_DIST="C:/Users/nashr/frontend/dist"

echo "========================================="
echo "Deploying Backend Updates to Production"
echo "========================================="

# Step 1: Backup current main.py
echo "[1/5] Creating backup of current main.py..."
ssh -i $SSH_KEY $VPS_USER@$VPS_IP "cd /root/sporttrader/backend && cp main.py main.py.backup_\$(date +%Y%m%d_%H%M%S)"
echo "✓ Backup created"

# Step 2: Upload updated main.py
echo "[2/5] Uploading updated main.py..."
scp -i $SSH_KEY "$LOCAL_BACKEND/main.py" $VPS_USER@$VPS_IP:/root/sporttrader/backend/main.py
echo "✓ main.py uploaded"

# Step 3: Upload other backend files if needed
echo "[3/5] Uploading subscription_db.py and stripe_service.py..."
scp -i $SSH_KEY "$LOCAL_BACKEND/subscription_db.py" $VPS_USER@$VPS_IP:/root/sporttrader/backend/subscription_db.py
scp -i $SSH_KEY "$LOCAL_BACKEND/stripe_service.py" $VPS_USER@$VPS_IP:/root/sporttrader/backend/stripe_service.py
echo "✓ Backend files uploaded"

# Step 4: Restart backend service
echo "[4/5] Restarting sporttrader service..."
ssh -i $SSH_KEY $VPS_USER@$VPS_IP "systemctl restart sporttrader && sleep 3 && systemctl status sporttrader --no-pager -l | head -20"
echo "✓ Service restarted"

# Step 5: Deploy updated frontend
echo "[5/5] Deploying updated frontend..."
ssh -i $SSH_KEY $VPS_USER@$VPS_IP "rm -rf /var/www/sporttrader/* && mkdir -p /var/www/sporttrader"
scp -i $SSH_KEY -r "$LOCAL_FRONTEND_DIST"/* $VPS_USER@$VPS_IP:/var/www/sporttrader/
ssh -i $SSH_KEY $VPS_USER@$VPS_IP "systemctl reload nginx"
echo "✓ Frontend deployed"

echo ""
echo "========================================="
echo "✓ DEPLOYMENT COMPLETE!"
echo "========================================="
echo ""
echo "Check webhook status at:"
echo "  https://dashboard.stripe.com/webhooks"
echo ""
echo "Test at:"
echo "  https://max-ev-sports.com"
echo ""
