#!/usr/bin/bash
# Train all sports with enhanced 7-model architecture

VPS_HOST="root@148.230.87.135"
VPS_DIR="/root/sporttrader/backend"

SPORTS="nba ncaab nhl nfl ncaaf"

for SPORT in $SPORTS; do
    echo "========================================"
    echo "Training $SPORT with 7 models..."
    echo "========================================"

    ssh $VPS_HOST "cd $VPS_DIR && source venv/bin/activate && python3 ml/autonomous_learning_system.py --sport $SPORT --enhanced"

    echo "✓ $SPORT complete"
    echo ""
done

echo "ALL SPORTS TRAINED WITH ENHANCED ARCHITECTURE"
