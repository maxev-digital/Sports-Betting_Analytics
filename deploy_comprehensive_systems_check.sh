#!/bin/bash

# Deploy Comprehensive Systems Check to VPS
# This script uploads the new systems check and sets up the cron job

set -e

VPS_HOST="root@148.230.87.135"
VPS_PATH="/root/sporttrader/backend"

echo "🚀 Deploying Comprehensive Daily Systems Check..."

# Upload the script
echo "📤 Uploading comprehensive_daily_systems_check.py..."
scp comprehensive_daily_systems_check.py ${VPS_HOST}:${VPS_PATH}/

# Make it executable
echo "🔧 Making script executable..."
ssh ${VPS_HOST} "chmod +x ${VPS_PATH}/comprehensive_daily_systems_check.py"

# Test the script
echo "🧪 Testing script on VPS..."
ssh ${VPS_HOST} "cd ${VPS_PATH} && python3 comprehensive_daily_systems_check.py"

# Update crontab
echo "⏰ Updating crontab..."
ssh ${VPS_HOST} << 'EOF'
# Backup current crontab
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S).txt

# Remove old daily systems check if exists
crontab -l | grep -v "daily_systems_check.py" | grep -v "daily_systems_check_with_email.py" > /tmp/new_crontab.txt

# Add new comprehensive check at 11 PM CST daily
echo "# Comprehensive Daily Systems Check - Enhanced version checking 24 components" >> /tmp/new_crontab.txt
echo "0 23 * * * cd /root/sporttrader/backend && /usr/bin/python3 comprehensive_daily_systems_check.py >> logs/systems_check.log 2>&1" >> /tmp/new_crontab.txt

# Install new crontab
crontab /tmp/new_crontab.txt

echo "✅ Crontab updated successfully"
crontab -l | grep "comprehensive_daily_systems_check"
EOF

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Summary:"
echo "  - Script deployed to: ${VPS_PATH}/comprehensive_daily_systems_check.py"
echo "  - Cron job: Daily at 11:00 PM CST"
echo "  - Logs: ${VPS_PATH}/logs/systems_check.log"
echo ""
echo "🧪 To test manually:"
echo "  ssh ${VPS_HOST}"
echo "  cd ${VPS_PATH}"
echo "  python3 comprehensive_daily_systems_check.py"
echo ""
echo "📧 Email will be sent to: \$ADMIN_EMAIL (from .env)"
