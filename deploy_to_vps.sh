#!/bin/bash
# VPS Deployment Script for Sport Trader
# VPS IP: 72.60.43.168
# Run this script from your local machine

set -e  # Exit on error

VPS_IP="72.60.43.168"
VPS_USER="root"
SSH_KEY="~/.ssh/hostinger_vps"
LOCAL_BACKEND="C:/Users/nashr/backend/scrapers/nba/backend"
LOCAL_FRONTEND="C:/Users/nashr/backend/scrapers/nba/frontend"

echo "========================================="
echo "Sport Trader VPS Deployment Script"
echo "========================================="
echo ""

# Step 1: Update VPS and install software
echo "[1/8] Installing software on VPS..."
ssh -i $SSH_KEY $VPS_USER@$VPS_IP << 'ENDSSH'
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y python3.12 python3.12-venv python3-pip nginx supervisor git curl
systemctl enable nginx
systemctl enable supervisor
echo "✓ Software installed"
ENDSSH

# Step 2: Create app directory
echo "[2/8] Creating application directory..."
ssh -i $SSH_KEY $VPS_USER@$VPS_IP "mkdir -p /root/sporttrader/{backend,frontend}"

# Step 3: Upload backend
echo "[3/8] Uploading backend files..."
scp -i $SSH_KEY -r "$LOCAL_BACKEND"/* $VPS_USER@$VPS_IP:/root/sporttrader/backend/
echo "✓ Backend uploaded"

# Step 4: Set up Python environment
echo "[4/8] Setting up Python environment..."
ssh -i $SSH_KEY $VPS_USER@$VPS_IP << 'ENDSSH'
cd /root/sporttrader/backend
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn[standard] httpx pydantic python-dotenv websockets pandas numpy
echo "✓ Python environment ready"
ENDSSH

# Step 5: Create backend systemd service
echo "[5/8] Creating backend service..."
ssh -i $SSH_KEY $VPS_USER@$VPS_IP << 'ENDSSH'
cat > /etc/systemd/system/sporttrader.service << 'EOF'
[Unit]
Description=Sport Trader Backend
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/sporttrader/backend
Environment="PATH=/root/sporttrader/backend/venv/bin"
ExecStart=/root/sporttrader/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable sporttrader
systemctl start sporttrader
echo "✓ Backend service started"
ENDSSH

# Step 6: Build frontend locally
echo "[6/8] Building frontend..."
cd "$LOCAL_FRONTEND"
npm install
npm run build
echo "✓ Frontend built"

# Step 7: Upload frontend
echo "[7/8] Uploading frontend..."
scp -i $SSH_KEY -r "$LOCAL_FRONTEND"/dist/* $VPS_USER@$VPS_IP:/root/sporttrader/frontend/
echo "✓ Frontend uploaded"

# Step 8: Configure Nginx
echo "[8/8] Configuring Nginx..."
ssh -i $SSH_KEY $VPS_USER@$VPS_IP << 'ENDSSH'
cat > /etc/nginx/sites-available/sporttrader << 'EOF'
server {
    listen 80 default_server;
    server_name _;

    # Frontend
    location / {
        root /root/sporttrader/frontend;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

ln -sf /etc/nginx/sites-available/sporttrader /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
echo "✓ Nginx configured"
ENDSSH

echo ""
echo "========================================="
echo "✓ DEPLOYMENT COMPLETE!"
echo "========================================="
echo ""
echo "Your app is now live at:"
echo "  http://$VPS_IP"
echo ""
echo "Backend API:"
echo "  http://$VPS_IP/api/games"
echo ""
echo "Default login: admin / admin123"
echo ""
