#!/bin/bash

# Cleanup Duplicate API Server (Port 8000)
# This script safely removes the unused port 8000 server

set -e

VPS_HOST="root@148.230.87.135"

echo "🔍 API Server Cleanup Script"
echo "============================="
echo ""
echo "This script will:"
echo "  1. Verify port 8888 is working (your production server)"
echo "  2. Stop port 8000 server (unused duplicate)"
echo "  3. Remove unused nginx config"
echo "  4. Clean up old frontend directory"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "📊 Step 1: Verifying Port 8888 (Production) is Running..."
ssh ${VPS_HOST} << 'EOF'
if ps aux | grep -q "[u]vicorn.*8888"; then
    echo "✅ Port 8888 is running"
    ps aux | grep "[u]vicorn.*8888" | head -1
else
    echo "❌ ERROR: Port 8888 is NOT running!"
    echo "This is your production server. DO NOT PROCEED."
    exit 1
fi
EOF

echo ""
echo "🧪 Step 2: Testing Port 8888 API Response..."
ssh ${VPS_HOST} << 'EOF'
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888/api/ui/best-plays 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "422" ]; then
    echo "✅ Port 8888 API responding (HTTP $HTTP_CODE)"
else
    echo "⚠️  Port 8888 returned HTTP $HTTP_CODE"
    echo "Proceeding anyway (may be normal if endpoint requires auth)"
fi
EOF

echo ""
echo "🛑 Step 3: Stopping Port 8000 Server..."
ssh ${VPS_HOST} << 'EOF'
if ps aux | grep -q "[u]vicorn.*8000"; then
    echo "Found port 8000 process:"
    ps aux | grep "[u]vicorn.*8000"
    echo ""
    echo "Killing process..."
    pkill -f "uvicorn.*8000" || true
    sleep 2

    if ps aux | grep -q "[u]vicorn.*8000"; then
        echo "⚠️  Process still running, trying force kill..."
        pkill -9 -f "uvicorn.*8000" || true
        sleep 1
    fi

    if ! ps aux | grep -q "[u]vicorn.*8000"; then
        echo "✅ Port 8000 stopped successfully"
    else
        echo "❌ Failed to stop port 8000"
        exit 1
    fi
else
    echo "ℹ️  Port 8000 was not running"
fi
EOF

echo ""
echo "🗑️  Step 4: Removing Unused Nginx Config..."
ssh ${VPS_HOST} << 'EOF'
if [ -L "/etc/nginx/sites-enabled/sporttrader" ]; then
    echo "Removing /etc/nginx/sites-enabled/sporttrader"
    rm /etc/nginx/sites-enabled/sporttrader
    echo "✅ Removed symlink"
else
    echo "ℹ️  Nginx config already removed or not found"
fi

echo ""
echo "Testing nginx configuration..."
if nginx -t 2>&1 | grep -q "successful"; then
    echo "✅ Nginx config is valid"
    echo "Reloading nginx..."
    nginx -s reload
    echo "✅ Nginx reloaded"
else
    echo "❌ Nginx config has errors!"
    nginx -t
    exit 1
fi
EOF

echo ""
echo "🧹 Step 5: Backing Up Old Frontend Directory..."
ssh ${VPS_HOST} << 'EOF'
if [ -d "/var/www/sporttrader" ]; then
    BACKUP_NAME="sporttrader.backup.$(date +%Y%m%d_%H%M%S)"
    echo "Moving /var/www/sporttrader to /var/www/$BACKUP_NAME"
    mv /var/www/sporttrader "/var/www/$BACKUP_NAME"
    echo "✅ Backed up to /var/www/$BACKUP_NAME"
else
    echo "ℹ️  Directory /var/www/sporttrader not found (already cleaned)"
fi
EOF

echo ""
echo "✅ Step 6: Final Verification..."
ssh ${VPS_HOST} << 'EOF'
echo "Checking running uvicorn processes:"
ps aux | grep "[u]vicorn"

echo ""
echo "Checking nginx config:"
ls -la /etc/nginx/sites-enabled/

echo ""
echo "Testing website:"
curl -I https://max-ev-sports.com/ 2>&1 | head -5
EOF

echo ""
echo "🎉 Cleanup Complete!"
echo ""
echo "Summary:"
echo "  ✅ Port 8000 stopped (was unused)"
echo "  ✅ Port 8888 still running (production)"
echo "  ✅ Unused nginx config removed"
echo "  ✅ Old frontend directory backed up"
echo ""
echo "Your site should now work from:"
echo "  - API: Port 8888 only"
echo "  - Frontend: /root/sporttrader/frontend/dist/"
echo "  - Nginx: maxevsports config only"
echo ""
echo "Test your site: https://max-ev-sports.com"
