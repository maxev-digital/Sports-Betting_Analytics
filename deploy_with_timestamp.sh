#!/bin/bash
# Timestamped Deployment Script
# Prevents deploying old files by tracking versions

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
VPS_HOST="148.230.87.135"
SSH_KEY="$HOME/.ssh/hostinger_vps"
DEPLOY_LOG="deployment_history.log"

echo "=========================================="
echo "MAX-EV SPORTS DEPLOYMENT SCRIPT"
echo "TIMESTAMP: $TIMESTAMP"
echo "=========================================="

# Log deployment
echo "" >> $DEPLOY_LOG
echo "=== DEPLOYMENT $TIMESTAMP ===" >> $DEPLOY_LOG
date >> $DEPLOY_LOG

# Function to deploy file with timestamp verification
deploy_file() {
    local_file="$1"
    remote_path="$2"
    description="$3"

    echo ""
    echo "→ Deploying: $description"
    echo "  Local:  $local_file"
    echo "  Remote: $remote_path"

    # Add timestamp comment to Python files
    if [[ $local_file == *.py ]]; then
        # Add deployment timestamp at top of file
        temp_file=$(mktemp)
        echo "# DEPLOYED: $TIMESTAMP" > $temp_file
        cat "$local_file" >> $temp_file

        # Deploy
        scp -i "$SSH_KEY" "$temp_file" "root@$VPS_HOST:$remote_path"
        rm "$temp_file"
    else
        # Deploy as-is
        scp -i "$SSH_KEY" "$local_file" "root@$VPS_HOST:$remote_path"
    fi

    if [ $? -eq 0 ]; then
        echo "  ✅ Deployed successfully"
        echo "  - $description ($TIMESTAMP)" >> $DEPLOY_LOG
    else
        echo "  ❌ Deployment failed"
        echo "  - FAILED: $description" >> $DEPLOY_LOG
    fi
}

# Deploy autonomous learning system
deploy_file \
    "C:/Users/nashr/backend/ml/autonomous_learning_system.py" \
    "/root/sporttrader/backend/ml/autonomous_learning_system.py" \
    "Autonomous Learning System"

# Deploy NCAAB results scraper
deploy_file \
    "C:/Users/nashr/backend/scrapers/ncaab/game_results_scraper_espn.py" \
    "/root/sporttrader/backend/scrapers/ncaab/game_results_scraper_espn.py" \
    "NCAAB Results Scraper"

# Deploy NBA results scraper
deploy_file \
    "C:/Users/nashr/backend/scrapers/nba/game_results_scraper.py" \
    "/root/sporttrader/backend/scrapers/nba/game_results_scraper.py" \
    "NBA Results Scraper"

# Deploy NCAAB models
deploy_file \
    "C:/Users/nashr/backend/models/ncaab/random_forest_totals_FIXED.py" \
    "/root/sporttrader/backend/models/ncaab/random_forest_totals.py" \
    "NCAAB Random Forest Model"

deploy_file \
    "C:/Users/nashr/backend/models/ncaab/xgboost_totals_FIXED.py" \
    "/root/sporttrader/backend/models/ncaab/xgboost_totals.py" \
    "NCAAB XGBoost Model"

echo ""
echo "=========================================="
echo "Restarting backend service..."
ssh -i "$SSH_KEY" "root@$VPS_HOST" "systemctl restart sporttrader"

if [ $? -eq 0 ]; then
    echo "✅ Service restarted successfully"
    echo "Service restarted: OK" >> $DEPLOY_LOG
else
    echo "❌ Service restart failed"
    echo "Service restarted: FAILED" >> $DEPLOY_LOG
fi

echo ""
echo "=========================================="
echo "DEPLOYMENT COMPLETE"
echo "Timestamp: $TIMESTAMP"
echo "Log: $DEPLOY_LOG"
echo "=========================================="

# Show recent deployments
echo ""
echo "Recent Deployments:"
tail -20 $DEPLOY_LOG
