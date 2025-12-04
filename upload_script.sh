#!/usr/bin/bash
# Upload enhanced prediction script to VPS

scp C:/Users/nashr/max-ev-sports/backend/run_enhanced_predictions_all_sports.py root@148.230.87.135:/root/sporttrader/backend/run_enhanced_predictions_all_sports.py

ssh root@148.230.87.135 "chmod +x /root/sporttrader/backend/run_enhanced_predictions_all_sports.py && wc -l /root/sporttrader/backend/run_enhanced_predictions_all_sports.py"

echo "✓ Enhanced prediction script uploaded"
