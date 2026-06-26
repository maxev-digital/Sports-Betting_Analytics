#!/bin/bash

# Quick Deploy Script - TeamRankings Scrapers to VPS
# Edit VPS_IP below, then run: bash DEPLOY_NOW.sh

VPS_IP="148.230.87.135"  # Correct IP
VPS_USER="root"
VPS_PATH="/root/sporttrader"

echo "🚀 Deploying TeamRankings Scrapers to VPS..."
echo "VPS: $VPS_USER@$VPS_IP"
echo ""

# Step 1: Copy scraper files
echo "[1/3] Copying scraper files..."
scp -i ~/.ssh/hostinger_vps backend/scrapers/teamrankings_nba_scraper.py $VPS_USER@$VPS_IP:$VPS_PATH/backend/scrapers/
scp -i ~/.ssh/hostinger_vps backend/scrapers/teamrankings_nfl_scraper.py $VPS_USER@$VPS_IP:$VPS_PATH/backend/scrapers/
scp -i ~/.ssh/hostinger_vps backend/scrapers/teamrankings_ncaaf_scraper.py $VPS_USER@$VPS_IP:$VPS_PATH/backend/scrapers/
scp -i ~/.ssh/hostinger_vps backend/scrapers/teamrankings_mlb_scraper.py $VPS_USER@$VPS_IP:$VPS_PATH/backend/scrapers/
echo "✅ Scrapers copied"

# Step 2: Copy master runner
echo "[2/3] Copying master runner..."
scp -i ~/.ssh/hostinger_vps backend/run_all_scrapers.py $VPS_USER@$VPS_IP:$VPS_PATH/backend/
echo "✅ Runner copied"

# Step 3: Set up on VPS
echo "[3/3] Setting up on VPS..."
ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP << 'EOF'
cd /root/sporttrader

# Make executable
chmod +x backend/run_all_scrapers.py

# Create logs directory
mkdir -p backend/logs

# Test scrapers
echo "Testing scrapers..."
cd /root/sporttrader && python3 backend/run_all_scrapers.py --force

# Set up cron job (7 AM CST = 1 PM UTC)
echo "Setting up daily cron job..."
(crontab -l 2>/dev/null | grep -q "run_all_scrapers.py") || \
(crontab -l 2>/dev/null; echo "0 13 * * * cd /root/sporttrader && python3 backend/run_all_scrapers.py >> /root/sporttrader/backend/logs/cron_scraper.log 2>&1") | crontab -

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Cron job configured:"
crontab -l | grep "run_all_scrapers.py"
EOF

echo ""
echo "========================================"
echo "🎉 Deployment Complete!"
echo "========================================"
echo ""
echo "Scrapers will run daily at 7:00 AM CST"
echo ""
echo "Check logs: ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP 'tail -f /root/sporttrader/backend/logs/scraper_runs.log'"
