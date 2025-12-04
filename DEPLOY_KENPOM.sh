#!/bin/bash

# Deploy KenPom Scraper to VPS with Automated Daily Runs
# Run: bash DEPLOY_KENPOM.sh

VPS_IP="148.230.87.135"
VPS_USER="root"
VPS_PATH="/root/sporttrader"

echo "🏀 Deploying KenPom Scraper to VPS..."
echo "VPS: $VPS_USER@$VPS_IP"
echo ""

# Step 1: Upload runner script
echo "[1/2] Uploading KenPom runner script..."
scp -i ~/.ssh/hostinger_vps backend/run_kenpom_scraper.py $VPS_USER@$VPS_IP:$VPS_PATH/backend/
echo "✅ Runner uploaded"

# Step 2: Set up on VPS
echo "[2/2] Setting up automated daily runs..."
ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP << 'EOF'
cd /root/sporttrader

# Make executable
chmod +x backend/run_kenpom_scraper.py

# Ensure logs directory exists
mkdir -p backend/logs

# Test the scraper
echo ""
echo "Testing KenPom scraper..."
python3 backend/run_kenpom_scraper.py

# Set up cron job for KenPom (8 AM CST = 2 PM UTC, runs after TeamRankings at 7 AM)
echo ""
echo "Setting up daily cron job for 8:00 AM CST..."
(crontab -l 2>/dev/null | grep -v "run_kenpom_scraper.py") > /tmp/cron.tmp
echo "0 14 * * * cd /root/sporttrader && python3 backend/run_kenpom_scraper.py >> /root/sporttrader/backend/logs/kenpom_scraper.log 2>&1" >> /tmp/cron.tmp
crontab /tmp/cron.tmp
rm /tmp/cron.tmp

echo ""
echo "✅ KenPom deployment complete!"
echo ""
echo "Cron jobs configured:"
crontab -l | grep -E "(run_all_scrapers|run_kenpom_scraper)"
EOF

echo ""
echo "========================================"
echo "🎉 KenPom Scraper Deployed!"
echo "========================================"
echo ""
echo "Schedule:"
echo "  7:00 AM CST - TeamRankings scrapers (NBA, NFL, NCAAF, MLB)"
echo "  8:00 AM CST - KenPom scraper (NCAAB)"
echo ""
echo "Check logs:"
echo "  ssh -i ~/.ssh/hostinger_vps $VPS_USER@$VPS_IP 'tail -f /root/sporttrader/backend/logs/kenpom_scraper.log'"
echo ""
echo "Total Features Now Available:"
echo "  NBA: 22 | NFL: 29 | NCAAF: 21 | MLB: 20 | NCAAB: 13"
echo "  TOTAL: 105 features across 593 teams"
echo ""
