# MaxEV Sports - Server Migration & Cleanup Guide

## 🎯 Overview
This guide covers:
1. Migrating from old VPS to new Hostinger VPS
2. Updating all domain references from sporttrader.io to max-ev-sports.com
3. Cleaning up unorganized files
4. Deploying to GitHub and production server

---

## ✅ **COMPLETED CHANGES**

### Updated Files:
- ✅ `frontend/.env.production` - Updated to max-ev-sports.com
- ✅ `backend/.env.production.example` - Updated to max-ev-sports.com

---

## 📋 **STEP 1: Update Server Configuration Files**

### 1.1 Update Nginx Configuration on Server

**SSH into your NEW Hostinger VPS:**
```bash
ssh username@YOUR_NEW_VPS_IP
```

**Edit Nginx configuration:**
```bash
sudo nano /etc/nginx/sites-available/maxevsports
```

**Replace with:**
```nginx
# Backend API
server {
    listen 80;
    server_name api.max-ev-sports.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}

# Frontend
server {
    listen 80;
    server_name max-ev-sports.com www.max-ev-sports.com;

    root /home/username/maxevsports/frontend/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Enable and restart:**
```bash
sudo ln -s /etc/nginx/sites-available/maxevsports /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/sporttrader  # Remove old config
sudo nginx -t
sudo systemctl restart nginx
```

### 1.2 Update Supervisor Configuration

**Edit supervisor config:**
```bash
sudo nano /etc/supervisor/conf.d/maxevsports.conf
```

**Replace with:**
```ini
[program:maxevsports-backend]
command=/home/username/maxevsports/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/home/username/maxevsports/backend
user=username
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/maxevsports/backend.log
stderr_logfile=/var/log/maxevsports/backend-error.log
environment=PATH="/home/username/maxevsports/backend/venv/bin"
```

**Create log directory and restart:**
```bash
sudo mkdir -p /var/log/maxevsports
sudo chown -R username:username /var/log/maxevsports
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl stop sporttrader-backend  # Stop old service
sudo supervisorctl start maxevsports-backend
sudo supervisorctl status
```

### 1.3 Update DNS Records

**In your domain registrar (where you bought max-ev-sports.com):**

Update A Records to point to **YOUR NEW VPS IP**:
```
Type    Name    Value               TTL
A       @       [NEW_VPS_IP]        14400
A       www     [NEW_VPS_IP]        14400
A       api     [NEW_VPS_IP]        14400
```

**Wait 1-2 hours for DNS propagation.**

### 1.4 Update SSL Certificates

```bash
# Remove old certificates
sudo certbot delete --cert-name sporttrader.io
sudo certbot delete --cert-name api.sporttrader.io

# Install new certificates
sudo certbot --nginx -d max-ev-sports.com -d www.max-ev-sports.com
sudo certbot --nginx -d api.max-ev-sports.com

# Test auto-renewal
sudo certbot renew --dry-run
```

---

## 📋 **STEP 2: Update Local Environment**

### 2.1 Update Your .env File on Server

**SSH into server and edit:**
```bash
cd /home/username/maxevsports/backend
nano .env.production
```

**Ensure it contains:**
```env
# MaxEV Sports - Production Environment
ENVIRONMENT=production
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Your actual API key
ODDS_API_KEY=your_actual_key_here

# Update paths
GOOGLE_SHEETS_CREDENTIALS=/home/username/maxevsports/credentials.json
GOOGLE_SHEETS_SHEET_ID=1bFNPXj2wOOBid8d-dnHbKmSs5U90a66X29-PFRmkgvo

# Security
SECRET_KEY=your_actual_secret_key_here
ALLOWED_HOSTS=max-ev-sports.com,www.max-ev-sports.com,api.max-ev-sports.com

# CORS Origins
CORS_ORIGINS=https://max-ev-sports.com,https://www.max-ev-sports.com,https://api.max-ev-sports.com

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/maxevsports/backend.log

# Performance
WORKERS=4
```

---

## 📋 **STEP 3: Clean Up Project Structure**

### 3.1 Files to Keep (Core Application)

**Keep these directories:**
```
backend/scrapers/nba/
├── backend/              # FastAPI backend
│   ├── *.py             # All Python modules
│   ├── requirements.txt
│   ├── .env.production.example
│   ├── routes/
│   ├── models/
│   ├── storage/
│   └── strategies/
│
├── frontend/            # React frontend
│   ├── src/
│   ├── public/
│   ├── .env.production
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
└── Documentation/       # Keep important docs
    ├── README.md
    ├── DEPLOYMENT_GUIDE.md
    ├── SERVER_MIGRATION_GUIDE.md (this file)
    └── nba_betting_roadmap.guide.txt
```

### 3.2 Files to Archive or Remove

**Consider archiving these (move to /archive/ folder):**
```
# Old documentation
- NBA Betting System Chat Cont. .md
- DEVELOPMENT_LOG.md (if outdated)
- advanced_betting_systems.txt

# Development notes
- *.mp3 files (audio notes)
- pace-analysis-spec.md (if implemented)

# One-off scripts
- nba_setup_script.py (if no longer needed)
- schedule_scraper.py (if replaced)
```

**To create archive:**
```bash
mkdir backend/scrapers/nba/archive
# Move old files there
```

### 3.3 Organize by Purpose

**Create clear structure:**
```
backend/scrapers/nba/
├── docs/                   # All documentation
│   ├── deployment/        # Deployment guides
│   ├── strategies/        # Strategy documentation
│   └── api/              # API documentation
│
├── scripts/               # Utility scripts
│   ├── setup/
│   └── maintenance/
│
└── tests/                 # Test files
```

---

## 📋 **STEP 4: Push to GitHub**

### 4.1 Commit Changes

```bash
cd C:\Users\nashr\backend\scrapers\nba

# Stage all changes
git add .

# Commit with clear message
git commit -m "Migration: Update to max-ev-sports.com and new VPS

- Updated frontend/.env.production with max-ev-sports.com domain
- Updated backend/.env.production.example with new configurations
- Updated all sporttrader.io references to max-ev-sports.com
- Added SERVER_MIGRATION_GUIDE.md for deployment
- Cleaned up project structure"

# Push to GitHub
git push origin main
```

### 4.2 Create Deployment Tag

```bash
# Tag this version
git tag -a v1.0.0-maxev -m "MaxEV Sports production release"
git push origin v1.0.0-maxev
```

---

## 📋 **STEP 5: Deploy to New Server**

### 5.1 Pull Latest Code

**On your new VPS:**
```bash
cd /home/username/maxevsports

# If first time, clone:
git clone https://github.com/anashp78/MaxEvSports.git .

# If updating:
git pull origin main
```

### 5.2 Update Backend

```bash
cd /home/username/maxevsports/backend

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Copy and edit production env
cp .env.production.example .env.production
nano .env.production  # Add your actual values

# Restart backend
sudo supervisorctl restart maxevsports-backend
sudo supervisorctl status
```

### 5.3 Update Frontend

```bash
cd /home/username/maxevsports/frontend

# Install dependencies (if needed)
npm install

# Build for production
npm run build

# Files are automatically served by Nginx
```

### 5.4 Verify Deployment

```bash
# Check backend is running
curl http://localhost:8000/health

# Check backend logs
sudo tail -f /var/log/maxevsports/backend.log

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
```

---

## 📋 **STEP 6: Verify Everything Works**

### 6.1 Test Frontend
- Visit: https://max-ev-sports.com
- Check: All pages load
- Verify: No console errors (F12)

### 6.2 Test Backend API
- Visit: https://api.max-ev-sports.com/docs
- Check: API documentation loads
- Test: `/api/games` endpoint

### 6.3 Test WebSocket
- Open frontend
- Check browser console for WebSocket connection
- Verify: Live odds updating

### 6.4 Test Full Integration
- Check: Games loading from API
- Verify: Live stats displaying
- Test: Odds updating in real-time
- Confirm: All sports showing correctly

---

## 🔧 **Troubleshooting**

### DNS Not Resolving
```bash
# Check DNS propagation
nslookup max-ev-sports.com
nslookup api.max-ev-sports.com

# May take up to 48 hours, usually 1-2 hours
```

### Backend Not Starting
```bash
# Check logs
sudo supervisorctl tail -f maxevsports-backend stderr

# Check port
sudo lsof -i :8000

# Restart service
sudo supervisorctl restart maxevsports-backend
```

### CORS Errors
```bash
# Edit backend .env.production
nano /home/username/maxevsports/backend/.env.production

# Ensure CORS_ORIGINS includes all domains:
CORS_ORIGINS=https://max-ev-sports.com,https://www.max-ev-sports.com,https://api.max-ev-sports.com

# Restart backend
sudo supervisorctl restart maxevsports-backend
```

### SSL Issues
```bash
# Check certificates
sudo certbot certificates

# Renew if needed
sudo certbot renew --force-renewal

# Test Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## 📋 **Quick Reference Commands**

### Server Management
```bash
# Restart everything
sudo supervisorctl restart maxevsports-backend
sudo systemctl restart nginx

# Check status
sudo supervisorctl status
sudo systemctl status nginx

# View logs
sudo tail -f /var/log/maxevsports/backend.log
sudo tail -f /var/log/nginx/error.log
```

### Deployment
```bash
# Pull latest code
cd /home/username/maxevsports
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart maxevsports-backend

# Update frontend
cd ../frontend
npm install
npm run build
```

---

## ✅ **Migration Checklist**

### Pre-Migration
- [ ] New VPS IP address noted
- [ ] GitHub repo access confirmed (https://github.com/anashp78/MaxEvSports)
- [ ] Domain DNS access available
- [ ] Backup of old server data created

### Server Configuration
- [ ] Nginx configured for max-ev-sports.com
- [ ] Supervisor configured for new paths
- [ ] SSL certificates installed
- [ ] DNS records updated to new IP
- [ ] Firewall rules configured

### Code Updates
- [ ] frontend/.env.production updated ✅
- [ ] backend/.env.production.example updated ✅
- [ ] All sporttrader references removed
- [ ] Changes committed to GitHub
- [ ] Code pulled to new server

### Testing
- [ ] Frontend accessible at https://max-ev-sports.com
- [ ] API accessible at https://api.max-ev-sports.com
- [ ] WebSocket connections working
- [ ] Live games displaying
- [ ] Odds updating correctly
- [ ] All sports showing data

### Cleanup
- [ ] Old server files archived
- [ ] Old sporttrader configs removed from new server
- [ ] Log files organized
- [ ] Backup verified

---

## 📞 **Support**

**If you encounter issues:**
1. Check the Troubleshooting section above
2. Review logs: `/var/log/maxevsports/backend.log`
3. Check Nginx logs: `/var/log/nginx/error.log`
4. Verify all environment variables are set correctly

**GitHub Repository:**
https://github.com/anashp78/MaxEvSports

---

**Last Updated**: 2025-10-22
**Status**: Ready for migration to new VPS
