# Deployment Action Plan - Get Site Live in Hours

## Current Situation Analysis

**You have TWO project structures:**

1. **OLD Structure** (`backend/scrapers/nba/`)
   - Branch: `feature/betting-strategies`
   - Has: Stripe integration, subscription system, all latest features
   - Status: Many modified & untracked files (not committed)
   
2. **NEW Structure** (`Max_EV_Sports/`)
   - Branch: `main`
   - Has: Reorganized backend structure
   - Status: Deleted old files, new directories (not committed)

## ⚡ RECOMMENDED APPROACH: Deploy OLD Structure First

**Why?** It has all your working features (Stripe, subscriptions, etc.) and is closer to production-ready. We can restructure later when things are stable.

---

## 🚀 Step-by-Step Deployment Plan (2-3 Hours)

### PHASE 1: Prepare Local Repository (30 mins)

#### Step 1.1: Update .gitignore
```bash
cd backend/scrapers/nba
```

Add to `.gitignore`:
```
# Environment files
.env
.env.local
*.env.local

# Database files
*.db
*.sqlite
*.sqlite3

# User data
users.json
user_activity_log.json
team_stats_cache.json

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
.venv/

# Node
node_modules/
dist/
.dist/
*.tar.gz

# IDE
.vscode/
.idea/

# Logs
*.log

# Test files
test_*.py
*_test.py
```

#### Step 1.2: Check what will be committed
```bash
git status
git diff backend/.env.production.example
```

#### Step 1.3: Stage files strategically
```bash
# Add all code changes
git add backend/*.py
git add backend/strategies/
git add backend/routes/
git add backend/models/
git add backend/storage/

# Add frontend changes
git add frontend/src/
git add frontend/index.html
git add frontend/vite.config.ts

# Add documentation
git add *.md

# Add Stripe integration
git add backend/stripe_service.py
git add backend/subscription_db.py
git add backend/test_stripe.py

# Check what's staged
git status
```

### PHASE 2: Commit & Push (15 mins)

#### Step 2.1: Commit changes
```bash
git commit -m "feat: Complete platform upgrade

- Add Stripe subscription system with 3 tiers
- Implement user authentication and signup
- Add comprehensive betting analytics
- Integrate multiple sport support (NBA, NFL, NHL, MLB, NCAAF)
- Add strategy detectors and alerts
- Update frontend with new pages and components
- Add user settings and preferences
- Implement bet tracking system

Ready for production deployment"
```

#### Step 2.2: Push to GitHub
```bash
# Push feature branch
git push origin feature/betting-strategies

# OR merge to main and push
git checkout main
git merge feature/betting-strategies
git push origin main
```

### PHASE 3: Server Preparation (20 mins)

#### Step 3.1: SSH into server
```bash
ssh root@148.230.87.135
# OR
ssh your_username@148.230.87.135
```

#### Step 3.2: Backup current deployment
```bash
cd /root  # or /home/your_username
cp -r sporttrader sporttrader_backup_$(date +%Y%m%d_%H%M%S)
```

#### Step 3.3: Pull latest changes
```bash
cd sporttrader
# or cd /root/sporttrader-backend

git fetch origin
git pull origin main
# OR
git pull origin feature/betting-strategies
```

### PHASE 4: Backend Setup (30 mins)

#### Step 4.1: Install dependencies
```bash
cd backend

# Activate venv or create new one
python3 -m venv venv
source venv/bin/activate  # On Linux

# Install requirements
pip install -r requirements.txt
```

#### Step 4.2: Configure environment
```bash
# Copy and edit production env
cp .env.production.example .env.production
nano .env.production
```

**Update these critical values:**
```bash
# Your actual Odds API key
ODDS_API_KEY=your_real_odds_api_key

# Stripe keys (production)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...

# Domain (your actual domain)
DOMAIN=https://maxevsports.com
# or
DOMAIN=http://148.230.87.135

# CORS origins
CORS_ORIGINS=https://maxevsports.com,http://148.230.87.135
```

#### Step 4.3: Initialize database
```bash
python -c "from subscription_db import init_subscription_tables; init_subscription_tables()"
```

#### Step 4.4: Test backend
```bash
# Quick test
python main.py &
sleep 5
curl http://localhost:8000/api/health
kill %1
```

### PHASE 5: Frontend Build & Deploy (30 mins)

#### Step 5.1: Install Node dependencies
```bash
cd ../frontend
npm install
```

#### Step 5.2: Update production environment
```bash
nano .env.production
```

**Set:**
```bash
VITE_API_URL=https://api.maxevsports.com
# OR
VITE_API_URL=http://148.230.87.135:8000

VITE_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

#### Step 5.3: Build frontend
```bash
npm run build
```

#### Step 5.4: Deploy to Nginx
```bash
# Copy build to nginx directory
sudo rm -rf /var/www/maxevsports/*
sudo cp -r dist/* /var/www/maxevsports/

# Or wherever your nginx root is
sudo cp -r dist/* /usr/share/nginx/html/
```

### PHASE 6: Configure Services (20 mins)

#### Step 6.1: Update Supervisor config
```bash
sudo nano /etc/supervisor/conf.d/sporttrader.conf
```

**Update paths:**
```ini
[program:sporttrader-backend]
command=/root/sporttrader/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/root/sporttrader/backend
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/sporttrader/backend.err.log
stdout_logfile=/var/log/sporttrader/backend.out.log
environment=ENVIRONMENT="production"
```

#### Step 6.2: Update Nginx config
```bash
sudo nano /etc/nginx/sites-available/maxevsports
```

**Verify configuration:**
```nginx
server {
    listen 80;
    server_name maxevsports.com www.maxevsports.com;
    # or: 148.230.87.135

    # Frontend
    location / {
        root /var/www/maxevsports;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```

### PHASE 7: Start Services (10 mins)

#### Step 7.1: Restart backend
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart sporttrader-backend

# Check status
sudo supervisorctl status
```

#### Step 7.2: Restart Nginx
```bash
sudo nginx -t  # Test config
sudo systemctl restart nginx
```

#### Step 7.3: Check logs
```bash
# Backend logs
sudo tail -f /var/log/sporttrader/backend.out.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### PHASE 8: Verification (15 mins)

#### Step 8.1: Test backend
```bash
curl http://148.230.87.135:8000/api/health
curl http://148.230.87.135:8000/api/live-games
```

#### Step 8.2: Test frontend
- Open browser: `http://148.230.87.135`
- Check all pages load
- Test navigation
- Verify API connections

#### Step 8.3: Test Stripe (if applicable)
- Visit /pricing page
- Click subscribe button
- Check Stripe checkout loads

---

## 🚨 Quick Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
cd backend
source venv/bin/activate
pip list

# Check logs
sudo supervisorctl tail sporttrader-backend stderr
```

### Frontend 404 errors
```bash
# Verify nginx config
sudo nginx -t

# Check file permissions
ls -la /var/www/maxevsports/

# Restart nginx
sudo systemctl restart nginx
```

### CORS errors
- Update backend `CORS_ORIGINS` in `.env.production`
- Restart backend: `sudo supervisorctl restart sporttrader-backend`

### Database errors
```bash
cd backend
python -c "from subscription_db import init_subscription_tables; init_subscription_tables()"
```

---

## 📋 Post-Deployment Checklist

- [ ] Backend responding on port 8000
- [ ] Frontend loading on port 80
- [ ] API endpoints returning data
- [ ] Live games displaying
- [ ] Stripe checkout working
- [ ] User signup working
- [ ] Login/logout working
- [ ] All navigation links working
- [ ] Mobile responsive
- [ ] No console errors

---

## ⏱️ Time Estimate

- **Phase 1-2** (Local prep & push): 45 mins
- **Phase 3-4** (Server backend): 50 mins  
- **Phase 5** (Frontend build): 30 mins
- **Phase 6-7** (Services): 30 mins
- **Phase 8** (Testing): 15 mins

**Total: ~2.5 hours**

---

## 🎯 Next Session: Clean Restructure

After site is live and stable:
1. Create clean `Max_EV_Sports` structure
2. Migrate files properly
3. Update all references
4. Deploy restructured version
5. Update documentation

**For now: GET IT LIVE! 🚀**
