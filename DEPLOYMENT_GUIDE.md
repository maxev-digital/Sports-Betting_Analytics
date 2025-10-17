# Sports Betting Analytics Platform - Deployment Guide

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Hostinger Hosting Options](#hostinger-hosting-options)
3. [Deployment Architecture](#deployment-architecture)
4. [Step-by-Step Deployment](#step-by-step-deployment)
5. [Post-Deployment Tasks](#post-deployment-tasks)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### Domain & Hosting
- [ ] Domain name decided and purchased
- [ ] Hostinger plan selected (VPS recommended)
- [ ] DNS management access confirmed
- [ ] SSL certificate plan (Let's Encrypt recommended)

### Environment Setup
- [ ] Production API keys secured
- [ ] Database credentials ready (if using external DB)
- [ ] Environment variables documented
- [ ] Backup strategy planned

### Code Preparation
- [ ] All features tested locally
- [ ] Production environment variables created
- [ ] Build process tested
- [ ] API endpoints documented

---

## Hostinger Hosting Options

### Option 1: VPS Hosting (RECOMMENDED)
**Best for:** Full control, Python support, scalability

**Pros:**
- Complete control over server configuration
- Can run Python backend and serve React frontend
- SSH access for deployment
- Can install any dependencies

**Cons:**
- Requires server management knowledge
- More expensive ($3.99-$29.99/month)

**Recommended Plan:** VPS 1 or VPS 2

### Option 2: Cloud Hosting
**Best for:** Auto-scaling, managed services

**Pros:**
- Automatic scaling
- Built-in load balancing
- Managed infrastructure

**Cons:**
- Most expensive option
- May require containerization (Docker)

### Option 3: Hybrid Approach
**Best for:** Cost optimization

**Setup:**
- Frontend: Hostinger shared hosting (static files)
- Backend: Railway, Render, or DigitalOcean ($5-10/month)

**Pros:**
- Cost-effective
- Easier backend management
- Frontend on fast CDN

**Cons:**
- Managing two platforms
- CORS configuration needed

---

## Deployment Architecture

### Recommended Architecture (VPS)

```
Domain (yourdomain.com)
         |
    [Cloudflare CDN] (optional)
         |
    [Nginx Reverse Proxy]
         |
    +---------+---------+
    |                   |
[React Frontend]   [FastAPI Backend]
(Static Files)     (Port 8000)
    |                   |
    |              [API Routes]
    |                   |
    |         [External APIs]
    |         - The Odds API
    |         - NBA API
    |         - ESPN API
    |         - NHL API
```

---

## Step-by-Step Deployment

### Phase 1: Prepare the Application

#### 1.1 Create Production Build Configuration

**Create `.env.production` in frontend folder:**
```env
VITE_API_URL=https://api.yourdomain.com
VITE_WS_URL=wss://api.yourdomain.com
```

**Create `.env.production` in backend folder:**
```env
# API Keys
ODDS_API_KEY=your_production_api_key

# CORS Settings
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]

# Server Settings
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Caching
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=your_sentry_dsn_if_using
```

#### 1.2 Build the Frontend

```bash
cd C:\Users\nashr\backend\scrapers\nba\frontend

# Install dependencies
npm install

# Build for production
npm run build

# This creates a 'dist' folder with optimized static files
```

#### 1.3 Prepare Backend for Production

**Create `requirements.txt` in backend folder:**
```bash
cd C:\Users\nashr\backend\scrapers\nba\backend
pip freeze > requirements.txt
```

**Verify critical dependencies are included:**
- fastapi
- uvicorn[standard]
- httpx
- pydantic
- python-dotenv
- nba_api (if used)

---

### Phase 2: Set Up Hostinger VPS

#### 2.1 Initial Server Setup

**Connect via SSH:**
```bash
ssh root@your-server-ip
```

**Update system:**
```bash
apt update && apt upgrade -y
```

**Install required software:**
```bash
# Python 3.12 (match your local version)
apt install python3.12 python3.12-venv python3-pip -y

# Nginx (web server)
apt install nginx -y

# Supervisor (process manager)
apt install supervisor -y

# Redis (optional, for caching)
apt install redis-server -y

# Certbot (SSL certificates)
apt install certbot python3-certbot-nginx -y

# Git (for deployment)
apt install git -y
```

#### 2.2 Create Application User

```bash
# Create non-root user for security
adduser sportsapp
usermod -aG sudo sportsapp

# Switch to new user
su - sportsapp
```

#### 2.3 Set Up Application Directory

```bash
# Create app directory
mkdir -p /home/sportsapp/app
cd /home/sportsapp/app

# Clone or upload your code
# Option A: If using Git
git clone https://github.com/yourusername/yourrepo.git .

# Option B: If uploading manually via SCP
# From your local machine:
# scp -r C:\Users\nashr\backend\scrapers\nba\* sportsapp@your-server-ip:/home/sportsapp/app/
```

---

### Phase 3: Configure Backend

#### 3.1 Create Python Virtual Environment

```bash
cd /home/sportsapp/app/backend

# Create virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3.2 Create Production Environment File

```bash
nano /home/sportsapp/app/backend/.env
```

**Add your production environment variables** (see section 1.1)

#### 3.3 Test Backend Manually

```bash
cd /home/sportsapp/app/backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# Press Ctrl+C to stop after testing
```

---

### Phase 4: Configure Nginx

#### 4.1 Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/sportsapp
```

**Add this configuration:**
```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

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
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    root /home/sportsapp/app/frontend/dist;
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

#### 4.2 Enable the Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/sportsapp /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

### Phase 5: Configure Supervisor (Backend Process Manager)

#### 5.1 Create Supervisor Configuration

```bash
sudo nano /etc/supervisor/conf.d/sportsapp.conf
```

**Add this configuration:**
```ini
[program:sportsapp-backend]
command=/home/sportsapp/app/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/home/sportsapp/app/backend
user=sportsapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/sportsapp/backend.log
stderr_logfile=/var/log/sportsapp/backend-error.log
environment=PATH="/home/sportsapp/app/backend/venv/bin"
```

#### 5.2 Create Log Directory

```bash
sudo mkdir -p /var/log/sportsapp
sudo chown -R sportsapp:sportsapp /var/log/sportsapp
```

#### 5.3 Start the Backend Service

```bash
# Reload supervisor configuration
sudo supervisorctl reread
sudo supervisorctl update

# Start the service
sudo supervisorctl start sportsapp-backend

# Check status
sudo supervisorctl status sportsapp-backend
```

---

### Phase 6: Configure DNS

#### 6.1 Add DNS Records in Hostinger

**In Hostinger DNS Management:**

**A Records:**
- `@` (root domain) → Your VPS IP address
- `www` → Your VPS IP address
- `api` → Your VPS IP address

**Example:**
```
Type    Name    Value               TTL
A       @       123.456.789.012     14400
A       www     123.456.789.012     14400
A       api     123.456.789.012     14400
```

**Wait for DNS propagation** (can take up to 48 hours, usually 1-2 hours)

---

### Phase 7: Configure SSL (HTTPS)

#### 7.1 Install SSL Certificates

```bash
# For main domain
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# For API subdomain
sudo certbot --nginx -d api.yourdomain.com
```

**Follow the prompts:**
- Enter your email address
- Agree to terms of service
- Choose whether to redirect HTTP to HTTPS (recommended: Yes)

#### 7.2 Set Up Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Renewal happens automatically via cron
```

---

### Phase 8: Deploy Frontend

#### 8.1 Upload Frontend Build

**From your local machine:**
```bash
# Build the frontend
cd C:\Users\nashr\backend\scrapers\nba\frontend
npm run build

# Upload dist folder to server
scp -r dist/* sportsapp@your-server-ip:/home/sportsapp/app/frontend/dist/
```

**Or on the server:**
```bash
cd /home/sportsapp/app/frontend

# Install Node.js (if not already installed)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install dependencies and build
npm install
npm run build
```

---

## Post-Deployment Tasks

### 1. Test the Application

**Frontend:**
- Visit `https://yourdomain.com`
- Check all pages load correctly
- Verify assets are loading

**Backend:**
- Visit `https://api.yourdomain.com/docs` (FastAPI auto-docs)
- Test API endpoints
- Check response times

**Integration:**
- Test live game data fetching
- Verify odds updates
- Check team stats display

### 2. Performance Optimization

#### Enable Cloudflare (Optional but Recommended)

**Benefits:**
- Free CDN
- DDoS protection
- Additional SSL
- Caching
- Analytics

**Setup:**
1. Sign up at cloudflare.com
2. Add your domain
3. Update nameservers at Hostinger
4. Configure caching rules

#### Configure Caching

**Backend Caching (Redis):**
```python
# Already implemented in your code
# Verify Redis is running:
redis-cli ping
# Should return: PONG
```

### 3. Set Up Monitoring

#### Application Monitoring

**Create health check endpoint** (add to backend/main.py):
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

**Set up UptimeRobot or similar:**
- Monitor `https://api.yourdomain.com/health`
- Alert via email/SMS if down
- Free tier available

#### Server Monitoring

**Install htop for resource monitoring:**
```bash
sudo apt install htop -y
htop
```

**Check logs:**
```bash
# Backend logs
sudo tail -f /var/log/sportsapp/backend.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# System logs
sudo journalctl -u nginx -f
```

### 4. Set Up Backups

**Create backup script:**
```bash
sudo nano /home/sportsapp/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/sportsapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application code
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /home/sportsapp/app

# Backup environment files
cp /home/sportsapp/app/backend/.env $BACKUP_DIR/env_$DATE.backup

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

**Make executable and schedule:**
```bash
chmod +x /home/sportsapp/backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add line:
0 2 * * * /home/sportsapp/backup.sh >> /var/log/sportsapp/backup.log 2>&1
```

### 5. Security Hardening

**Configure Firewall (UFW):**
```bash
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
sudo ufw status
```

**Change SSH Port (Optional):**
```bash
sudo nano /etc/ssh/sshd_config
# Change: Port 22 to Port 2222
sudo systemctl restart ssh
# Update UFW rule
```

**Disable Root Login:**
```bash
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart ssh
```

**Install Fail2Ban:**
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## Monitoring & Maintenance

### Daily Checks
- [ ] Application is accessible
- [ ] API endpoints responding
- [ ] No error logs
- [ ] SSL certificates valid

### Weekly Checks
- [ ] Review application logs
- [ ] Check disk space usage
- [ ] Review API usage/costs
- [ ] Update dependencies if needed

### Monthly Checks
- [ ] Security updates
- [ ] Performance optimization
- [ ] Backup verification
- [ ] Cost analysis

### Update Deployment Commands

**Update Backend:**
```bash
cd /home/sportsapp/app/backend
git pull origin main  # or upload new files
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart sportsapp-backend
```

**Update Frontend:**
```bash
cd /home/sportsapp/app/frontend
git pull origin main  # or upload new files
npm install
npm run build
# Files automatically served by Nginx
```

---

## Troubleshooting

### Backend Not Starting

**Check logs:**
```bash
sudo supervisorctl tail -f sportsapp-backend
```

**Common issues:**
- Missing environment variables
- Port already in use
- Python dependencies not installed
- Permission issues

**Solution:**
```bash
# Check process on port 8000
sudo lsof -i :8000

# Restart service
sudo supervisorctl restart sportsapp-backend

# Check status
sudo supervisorctl status
```

### Frontend Shows Blank Page

**Check Nginx logs:**
```bash
sudo tail -f /var/log/nginx/error.log
```

**Common issues:**
- Files not in correct directory
- Wrong permissions
- API URL not configured

**Solution:**
```bash
# Check file permissions
ls -la /home/sportsapp/app/frontend/dist

# Set correct permissions
sudo chown -R sportsapp:www-data /home/sportsapp/app/frontend/dist
sudo chmod -R 755 /home/sportsapp/app/frontend/dist

# Restart Nginx
sudo systemctl restart nginx
```

### API Calls Failing (CORS)

**Check CORS configuration in backend:**
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### SSL Certificate Issues

**Renew certificate:**
```bash
sudo certbot renew --force-renewal
```

**Check certificate:**
```bash
sudo certbot certificates
```

### High Server Load

**Check resource usage:**
```bash
htop
```

**Common causes:**
- Too many API requests
- Inefficient database queries
- Memory leaks
- Not enough workers

**Solutions:**
- Implement rate limiting
- Add Redis caching (already in code)
- Increase VPS resources
- Optimize API calls

---

## Cost Estimation

### Hostinger VPS Hosting
- **VPS 1**: $3.99/month (1 vCore, 4GB RAM) - Good for starting
- **VPS 2**: $5.99/month (2 vCore, 8GB RAM) - Recommended
- **VPS 3**: $8.99/month (3 vCore, 12GB RAM) - High traffic

### Additional Costs
- **Domain**: $10-15/year (first year often free with hosting)
- **The Odds API**: Check current pricing tiers
- **Cloudflare**: Free tier sufficient
- **Monitoring**: Free tier (UptimeRobot, etc.)

### Total Monthly Cost Estimate
- **Minimum**: ~$6/month (VPS 1 + domain)
- **Recommended**: ~$8/month (VPS 2 + domain)
- **Plus API costs**: Variable based on usage

---

## Quick Deployment Checklist

**Before deployment:**
- [ ] Test all features locally
- [ ] Create production environment files
- [ ] Build frontend successfully
- [ ] Document all environment variables
- [ ] Choose and purchase domain
- [ ] Set up Hostinger VPS account

**During deployment:**
- [ ] Configure VPS server
- [ ] Install all dependencies
- [ ] Upload/clone application code
- [ ] Configure Nginx
- [ ] Set up Supervisor
- [ ] Configure DNS records
- [ ] Install SSL certificates
- [ ] Deploy frontend build
- [ ] Test all functionality

**After deployment:**
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Implement security measures
- [ ] Enable CDN (Cloudflare)
- [ ] Document deployment process
- [ ] Create rollback plan

---

## Support Contacts

**When you're ready to deploy:**
1. Share your chosen domain name
2. Confirm Hostinger plan selected
3. Mention any specific requirements
4. I'll provide hands-on deployment assistance

**Useful Resources:**
- Hostinger Support: https://www.hostinger.com/support
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Let's Encrypt: https://letsencrypt.org/
- Nginx Documentation: https://nginx.org/en/docs/

---

## Notes

- This guide assumes a Linux-based VPS (Ubuntu/Debian)
- Commands may vary slightly for different Linux distributions
- Always backup before making configuration changes
- Test in staging environment if possible before production
- Keep this document updated with your specific configurations

---

**Created**: 2025-10-16
**Last Updated**: 2025-10-16
**Status**: Ready for deployment when needed
