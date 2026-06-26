#!/bin/bash

# TeamRankings Scrapers - VPS Deployment Script
# This script deploys all scrapers to your VPS and sets up automation

# Configuration
VPS_IP="YOUR_VPS_IP"  # Change this to your VPS IP
VPS_USER="root"
VPS_PATH="/root/sporttrader"

echo "========================================"
echo "TeamRankings Scrapers - VPS Deployment"
echo "========================================"
echo ""

# Check if VPS_IP is set
if [ "$VPS_IP" == "YOUR_VPS_IP" ]; then
    echo "❌ ERROR: Please set your VPS_IP in this script first"
    echo "   Edit deploy_scrapers_to_vps.sh and change VPS_IP=\"YOUR_VPS_IP\" to your actual IP"
    exit 1
fi

echo "VPS: $VPS_USER@$VPS_IP"
echo "Path: $VPS_PATH"
echo ""

# Step 1: Copy scraper files
echo "[1/5] Copying scraper files..."
scp backend/scrapers/teamrankings_*.py $VPS_USER@$VPS_IP:$VPS_PATH/backend/scrapers/
if [ $? -ne 0 ]; then
    echo "❌ Failed to copy scraper files"
    exit 1
fi
echo "✅ Scraper files copied"

# Step 2: Copy master runner
echo ""
echo "[2/5] Copying master runner script..."
scp backend/run_all_scrapers.py $VPS_USER@$VPS_IP:$VPS_PATH/backend/
if [ $? -ne 0 ]; then
    echo "❌ Failed to copy runner script"
    exit 1
fi
echo "✅ Runner script copied"

# Step 3: Make executable and test
echo ""
echo "[3/5] Making scripts executable and testing..."
ssh $VPS_USER@$VPS_IP << 'EOF'
cd /root/sporttrader
chmod +x backend/run_all_scrapers.py

echo "Testing scrapers..."
python3 backend/run_all_scrapers.py --force

if [ $? -eq 0 ]; then
    echo "✅ Scrapers tested successfully"
else
    echo "❌ Scraper test failed"
    exit 1
fi
EOF

if [ $? -ne 0 ]; then
    echo "❌ Testing failed"
    exit 1
fi

# Step 4: Set up cron job
echo ""
echo "[4/5] Setting up daily cron job (7:00 AM CST)..."
ssh $VPS_USER@$VPS_IP << 'EOF'
# Add cron job if it doesn't exist
(crontab -l 2>/dev/null | grep -q "run_all_scrapers.py") || \
(crontab -l 2>/dev/null; echo "0 13 * * * cd /root/sporttrader && /root/sporttrader/backend/venv/bin/python backend/run_all_scrapers.py >> /root/sporttrader/backend/logs/cron_scraper.log 2>&1") | crontab -

echo "✅ Cron job configured"
echo ""
echo "Current cron jobs:"
crontab -l | grep "run_all_scrapers.py"
EOF

# Step 5: Summary
echo ""
echo "========================================"
echo "Deployment Complete! ✅"
echo "========================================"
echo ""
echo "Scrapers will run daily at 7:00 AM CST"
echo ""
echo "Useful commands:"
echo "  - View logs: ssh $VPS_USER@$VPS_IP 'tail -f /root/sporttrader/backend/logs/scraper_runs.log'"
echo "  - Run manually: ssh $VPS_USER@$VPS_IP 'cd /root/sporttrader && python3 backend/run_all_scrapers.py'"
echo "  - Check cron: ssh $VPS_USER@$VPS_IP 'crontab -l'"
echo ""
