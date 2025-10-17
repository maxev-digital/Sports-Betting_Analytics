# Sports Betting Analytics - DigitalOcean Deployment Guide

## Why DigitalOcean + Hostinger Domain?

**Recommended Setup:**
- **Domain**: Purchase from Hostinger (cheap, includes email)
- **Hosting**: DigitalOcean Droplet (better for Python apps, easier setup)

**Benefits:**
- Simple one-click setup options
- Better documentation for Python/FastAPI
- Excellent performance ($6-12/month)
- Easy scaling
- Managed databases available
- Better community support
- Simpler backups/snapshots

---

## Quick Cost Comparison

### DigitalOcean
- **Basic Droplet**: $6/month (1GB RAM, 1 vCPU) - Perfect for starting
- **Standard Droplet**: $12/month (2GB RAM, 1 vCPU) - Recommended
- **Domain from Hostinger**: ~$10/year (first year often free)
- **Total**: ~$7-13/month

### Alternative: Hostinger VPS
- **VPS 1**: $3.99/month - Limited resources
- **VPS 2**: $5.99/month - Comparable to DO
- **Domain**: Included with plan
- **Total**: ~$6/month

**Verdict**: DigitalOcean is slightly more expensive but much easier to manage for Python apps.

---

## Deployment Options

### Option 1: Manual Deployment (Full Control)
Best for learning, complete customization

### Option 2: Docker Deployment (Recommended)
Best for consistency, easier updates, portable

### Option 3: DigitalOcean App Platform (Easiest)
Best for simplicity, automatic scaling, managed SSL

---

## Option 1: Manual Deployment on DigitalOcean Droplet

### Step 1: Create DigitalOcean Droplet

1. **Sign up at digitalocean.com**
   - Get $200 free credit for 60 days (new accounts)

2. **Create a Droplet:**
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($6 or $12/month)
   - **Datacenter**: Closest to your target users
   - **Authentication**: SSH key (recommended) or Password
   - **Hostname**: `sportsapp-prod`

3. **Optional Add-ons:**
   - ✓ Managed Databases (if needed later)
   - ✓ Backups (recommended, +20% of Droplet cost)
   - ✓ Monitoring (free)

### Step 2: Initial Server Setup

**Connect to your Droplet:**
```bash
ssh root@your-droplet-ip
```

**Update system:**
```bash
apt update && apt upgrade -y
```

**Install required software:**
```bash
# Python 3.12
apt install python3.12 python3.12-venv python3-pip -y

# Nginx
apt install nginx -y

# Supervisor
apt install supervisor -y

# Redis (for caching)
apt install redis-server -y

# Node.js (for frontend building)
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# Git
apt install git -y

# Certbot (SSL)
apt install certbot python3-certbot-nginx -y
```

**Create application user:**
```bash
adduser sportsapp
usermod -aG sudo sportsapp
su - sportsapp
```

### Step 3: Deploy Application

**Clone or upload your code:**
```bash
cd /home/sportsapp
git clone https://github.com/yourusername/yourrepo.git app
cd app
```

**Set up backend:**
```bash
cd backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
nano .env
# Add your production environment variables
```

**Build frontend:**
```bash
cd ../frontend
npm install
npm run build
```

### Step 4: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/sportsapp
```

**Add configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    root /home/sportsapp/app/frontend/dist;
    index index.html;

    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/sportsapp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Configure Supervisor

```bash
sudo nano /etc/supervisor/conf.d/sportsapp.conf
```

```ini
[program:sportsapp-backend]
command=/home/sportsapp/app/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4
directory=/home/sportsapp/app/backend
user=sportsapp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/sportsapp/backend.log
stderr_logfile=/var/log/sportsapp/backend-error.log
environment=PATH="/home/sportsapp/app/backend/venv/bin"
```

**Start service:**
```bash
sudo mkdir -p /var/log/sportsapp
sudo chown -R sportsapp:sportsapp /var/log/sportsapp
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start sportsapp-backend
```

### Step 6: Configure DNS at Hostinger

**In Hostinger DNS Management:**
```
Type    Name    Value (your DigitalOcean IP)    TTL
A       @       123.456.789.012                  14400
A       www     123.456.789.012                  14400
```

Wait 1-2 hours for DNS propagation.

### Step 7: Install SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Done!** Your site should now be live at `https://yourdomain.com`

---

## Option 2: Docker Deployment (RECOMMENDED)

### Why Docker?
- Consistent environment (works same locally and in production)
- Easy updates (rebuild and restart)
- Easy rollback if something breaks
- Can move to any cloud provider easily

### Step 1: Create Dockerfile for Backend

**Create `backend/Dockerfile`:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Step 2: Create Dockerfile for Frontend

**Create `frontend/Dockerfile`:**
```dockerfile
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build app
COPY . .
RUN npm run build

# Production image
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Create `frontend/nginx.conf`:**
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
}
```

### Step 3: Create docker-compose.yml

**Create `docker-compose.yml` in project root:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: sportsapp-backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      - ODDS_API_KEY=${ODDS_API_KEY}
      - REDIS_URL=redis://redis:6379
    env_file:
      - ./backend/.env
    depends_on:
      - redis
    volumes:
      - ./backend:/app
    networks:
      - app-network

  frontend:
    build: ./frontend
    container_name: sportsapp-frontend
    restart: always
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    networks:
      - app-network
    volumes:
      - ./ssl:/etc/nginx/ssl

  redis:
    image: redis:7-alpine
    container_name: sportsapp-redis
    restart: always
    networks:
      - app-network
    volumes:
      - redis-data:/data

networks:
  app-network:
    driver: bridge

volumes:
  redis-data:
```

### Step 4: Deploy with Docker

**On DigitalOcean Droplet:**

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Clone your code
cd /home/sportsapp
git clone https://github.com/yourusername/yourrepo.git app
cd app

# Create .env file
nano backend/.env
# Add your production variables

# Build and run
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**Update deployment:**
```bash
cd /home/sportsapp/app
git pull
docker-compose down
docker-compose up -d --build
```

---

## Option 3: DigitalOcean App Platform (EASIEST)

### What is App Platform?
- Fully managed platform (like Heroku but cheaper)
- Automatic HTTPS/SSL
- Auto-scaling
- GitHub integration
- Zero server management

### Cost
- **Basic**: $5/month per container
- **Professional**: $12/month per container
- **Total for this app**: ~$10-24/month (frontend + backend)

### Setup Steps

1. **Prepare Your Code**

**Update `backend/requirements.txt`** to include:
```
fastapi
uvicorn[standard]
httpx
pydantic
python-dotenv
nba_api
redis
```

**Create `backend/gunicorn_conf.py`:**
```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
```

**Update `backend/main.py` CORS to allow your frontend:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will be restricted by App Platform network
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Push Code to GitHub**
```bash
cd C:\Users\nashr\backend\scrapers\nba
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/yourrepo.git
git push -u origin main
```

3. **Create App on DigitalOcean**

- Go to DigitalOcean App Platform
- Click "Create App"
- Connect GitHub repository
- DigitalOcean will auto-detect Python and Node.js

4. **Configure Components**

**Backend Component:**
- **Name**: backend
- **Source Directory**: `/backend`
- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `gunicorn -c gunicorn_conf.py main:app`
- **HTTP Port**: 8000
- **Environment Variables**: Add all from `.env`

**Frontend Component:**
- **Name**: frontend
- **Source Directory**: `/frontend`
- **Build Command**: `npm install && npm run build`
- **Output Directory**: `dist`
- **HTTP Port**: (automatic)

5. **Add Custom Domain**

- In App settings, add your domain from Hostinger
- DigitalOcean provides DNS instructions
- Automatic SSL certificate

6. **Deploy**

- Click "Create Resources"
- Wait 5-10 minutes
- Your app is live!

**Future updates:**
- Push to GitHub
- Automatic deployment triggers

---

## Recommended Setup: Docker on DigitalOcean Droplet

**Best balance of:**
- Control (you manage the server)
- Simplicity (Docker handles dependencies)
- Cost ($6-12/month)
- Flexibility (easy to migrate)

### Quick Start Command Reference

```bash
# Initial setup
ssh root@your-droplet-ip
curl -fsSL https://get.docker.com | sh
apt install docker-compose git -y
git clone https://github.com/yourusername/yourrepo.git /app
cd /app
nano backend/.env  # Add production vars
docker-compose up -d

# Updates
cd /app
git pull
docker-compose restart

# View logs
docker-compose logs -f backend

# Stop everything
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

---

## Security Checklist

### Firewall Setup
```bash
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### SSH Security
```bash
# Disable password auth (use SSH keys only)
nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
systemctl restart ssh
```

### Docker Security
```bash
# Don't run as root in containers
# Already handled in Dockerfiles above
```

### Environment Variables
```bash
# Never commit .env files
# Add to .gitignore
echo "*.env" >> .gitignore
echo ".env" >> .gitignore
```

---

## Monitoring & Maintenance

### DigitalOcean Monitoring (Free)
- Enable in Droplet settings
- CPU, memory, disk usage
- Email alerts

### Application Monitoring

**Health check endpoint** (add to main.py):
```python
@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
```

**Use UptimeRobot:**
- Monitor: `https://yourdomain.com/api/health`
- Check every 5 minutes
- Email alert if down

### Log Management

**View Docker logs:**
```bash
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Limit log size** (add to docker-compose.yml):
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

---

## Backup Strategy

### DigitalOcean Droplet Snapshots
- Manual snapshots: Free
- Automated backups: +20% of Droplet cost
- Recommended: Weekly automated backups

### Application Backup Script

**Create `/home/sportsapp/backup.sh`:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
docker-compose exec backend tar -czf /tmp/backup-$DATE.tar.gz /app
docker cp sportsapp-backend:/tmp/backup-$DATE.tar.gz ./backups/
```

**Schedule with cron:**
```bash
crontab -e
# Add: 0 2 * * * /home/sportsapp/backup.sh
```

---

## Scaling Options

### Vertical Scaling (Bigger Droplet)
**Easy upgrade path:**
- $6/month → $12/month: 2x RAM, better performance
- $12/month → $24/month: 4x RAM, 2x CPU
- Can resize anytime (few minutes downtime)

### Horizontal Scaling (Multiple Droplets)
**When needed:**
- Load balancer: $10/month
- 2+ Droplets: $6-12/month each
- Managed Redis: $15/month

### Database Scaling
**Options:**
- SQLite (current): Good for < 1000 concurrent users
- Managed PostgreSQL: $15/month (when needed)
- Redis only: Current setup (sufficient)

---

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs backend
```

**Common issues:**
- Missing environment variables
- Port conflicts
- Permission errors

**Solution:**
```bash
docker-compose down
docker-compose up -d --build
```

### High Memory Usage

**Check usage:**
```bash
docker stats
```

**Solutions:**
- Limit workers in uvicorn (currently 4)
- Add memory limits to docker-compose.yml
- Upgrade Droplet

### Slow Performance

**Check response times:**
```bash
curl -w "@-" -o /dev/null -s https://yourdomain.com/api/health <<'EOF'
time_total: %{time_total}s
EOF
```

**Solutions:**
- Enable Redis caching (already implemented)
- Use Cloudflare CDN
- Upgrade Droplet
- Optimize database queries

---

## Next Steps When Ready

1. **Choose your deployment method:**
   - Docker (recommended)
   - Manual setup
   - App Platform

2. **Purchase domain from Hostinger**
   - Choose memorable name
   - Get domain + email

3. **Create DigitalOcean account**
   - Get $200 credit (new accounts)
   - Choose Basic Droplet ($6 or $12)

4. **I'll help you with:**
   - Creating Dockerfiles
   - Setting up the Droplet
   - Configuring DNS
   - Installing SSL
   - Testing deployment
   - Monitoring setup

Just let me know when you're ready and what domain name you choose!

---

**Last Updated**: 2025-10-16
