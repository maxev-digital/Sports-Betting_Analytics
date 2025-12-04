# API Servers Analysis & Cleanup Plan

**Date**: December 4, 2025
**Issue**: Two API servers running causing frontend deployment confusion
**Goal**: Eliminate one server and standardize deployment

---

## 🔍 Current Situation

You have **TWO separate API servers** running on your VPS:

### Server 1: Port 8000 (OLD/UNUSED)
- **Location**: `/root/sporttrader/backend/`
- **Process**: `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2`
- **Nginx Config**: `/etc/nginx/sites-available/sporttrader`
- **Frontend Served From**: `/var/www/sporttrader/`
- **Domain**: Uses `server_name _;` (catch-all)
- **Status**: ⚠️ **RUNNING BUT NOT USED**

### Server 2: Port 8888 (ACTIVE/PRODUCTION)
- **Location**: `/root/sporttrader/backend/` (same codebase)
- **Process**: `uvicorn main:app --host 0.0.0.0 --port 8888`
- **Nginx Config**: `/etc/nginx/sites-available/maxevsports`
- **Frontend Served From**: `/root/sporttrader/frontend/dist/`
- **Domain**: `max-ev-sports.com` (and www subdomain)
- **Status**: ✅ **THIS IS YOUR PRODUCTION SERVER**

---

## 🧩 The Problem

### Why You're Confused During Frontend Changes

1. **Two Deploy Locations**:
   - `/var/www/sporttrader/` (port 8000's frontend - UNUSED)
   - `/root/sporttrader/frontend/dist/` (port 8888's frontend - ACTIVE)

2. **When you build frontend**, you probably deploy to one location, but users hit the other

3. **Nginx has TWO configs**:
   - `sporttrader` config → Port 8000 (inactive)
   - `maxevsports` config → Port 8888 (active)

4. **Your frontend config (`config.ts`)** says:
   ```typescript
   export const API_BASE_URL = 'https://api.max-ev-sports.com/api';
   ```
   - This goes through Cloudflare
   - Cloudflare proxies to nginx
   - Nginx (maxevsports config) sends API calls to **Port 8888** ✅

---

## 📊 Server Comparison

| Aspect | Port 8000 (OLD) | Port 8888 (PRODUCTION) |
|--------|----------------|----------------------|
| **Domain** | Catch-all `_` | max-ev-sports.com |
| **Frontend Location** | /var/www/sporttrader | /root/sporttrader/frontend/dist |
| **Workers** | 2 workers | 1 worker |
| **Nginx Config** | sporttrader | maxevsports |
| **Actual Usage** | ❌ None | ✅ All traffic |
| **Cron Jobs** | ❌ None | ✅ Yes (points to this) |
| **Database Access** | ✅ Yes (same DB) | ✅ Yes (same DB) |

---

## ✅ Recommendation: **KILL PORT 8000**

**Port 8000 is completely unused and causing confusion.**

### Why Port 8888 is Your Production Server

1. **Domain Mapping**: `max-ev-sports.com` → Port 8888 in nginx
2. **Frontend Config**: Uses Cloudflare which routes to Port 8888
3. **More Connections**: `lsof` shows nginx workers actively connected to 8888
4. **Same Codebase**: Both run same `main.py`, but 8888 is what's actually hit

### Why Port 8000 Can Be Safely Removed

1. **No Traffic**: Nginx doesn't route any domain to it
2. **Duplicate**: Runs same code as Port 8888
3. **Wasting Resources**: 2 workers consuming memory for nothing
4. **Confusion**: Causes deployment issues

---

## 🎯 Cleanup Plan

### Step 1: Verify Port 8888 is Active

```bash
# SSH to VPS
ssh root@148.230.87.135

# Test that port 8888 responds
curl -I http://localhost:8888/api/ui/best-plays

# Should return HTTP 200 or 422 (missing params)
```

### Step 2: Stop Port 8000 Server

```bash
# Find the process
ps aux | grep "uvicorn.*8000"

# You should see something like:
# root 390972 ... uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2

# Kill it
kill 390972
# OR
pkill -f "uvicorn.*8000"
```

### Step 3: Remove Port 8000 from Startup

Port 8000 is likely started by one of these:

**Option A: Systemd Service**
```bash
# Check for systemd service
systemctl list-units --type=service | grep -i uvicorn
systemctl list-units --type=service | grep -i sporttrader

# If found, disable it:
systemctl stop sporttrader
systemctl disable sporttrader
```

**Option B: Cron Job**
```bash
# Check crontab
crontab -l | grep 8000
crontab -l | grep uvicorn

# If found, remove that line from crontab
```

**Option C: Startup Script**
```bash
# Check /etc/rc.local or similar
cat /etc/rc.local
```

### Step 4: Remove Unused Nginx Config

```bash
# Disable the old sporttrader config
rm /etc/nginx/sites-enabled/sporttrader

# Keep the enabled configs
ls -la /etc/nginx/sites-enabled/
# Should only show: maxevsports

# Reload nginx
nginx -t  # Test config
nginx -s reload  # Apply changes
```

### Step 5: Clean Up Old Frontend Directory

```bash
# The /var/www/sporttrader/ directory is no longer used
# Keep as backup or remove

# Option A: Backup and remove
mv /var/www/sporttrader /var/www/sporttrader.backup.$(date +%Y%m%d)

# Option B: Just remove (you have /root/sporttrader/frontend/dist)
# rm -rf /var/www/sporttrader
```

### Step 6: Verify Everything Still Works

```bash
# Check port 8888 is still running
ps aux | grep "uvicorn.*8888"

# Test API
curl -I http://localhost:8888/api/ui/best-plays

# Test from outside
curl -I https://max-ev-sports.com/

# Check nginx is happy
nginx -t
```

---

## 📁 Standardized Deployment Process (After Cleanup)

### Frontend Deployment

**ONLY ONE LOCATION**: `/root/sporttrader/frontend/dist/`

```bash
# On your local machine (Windows):
cd C:\Users\nashr\max-ev-sports\frontend
npm run build

# Deploy to VPS
scp -r dist/* root@148.230.87.135:/root/sporttrader/frontend/dist/

# OR use your existing deployment script (update if needed)
```

### Backend Deployment

**Server runs from**: `/root/sporttrader/backend/`

```bash
# Deploy backend changes
scp your-file.py root@148.230.87.135:/root/sporttrader/backend/

# Restart the API server (port 8888 only)
ssh root@148.230.87.135
cd /root/sporttrader/backend
# Find and restart the uvicorn process for port 8888
ps aux | grep "uvicorn.*8888"
kill <PID>
nohup uvicorn main:app --host 0.0.0.0 --port 8888 &
```

---

## 🚨 Important Notes

### DON'T Kill Port 8888!
- Port 8888 is your **PRODUCTION** server
- All traffic goes here
- Killing this will break your site

### Frontend Config is Correct
Your `frontend/src/config.ts` is already correct:
```typescript
export const API_BASE_URL = 'https://api.max-ev-sports.com/api';
```
This goes through Cloudflare → Nginx → Port 8888 ✅

### After Cleanup
You'll have:
- ✅ One API server (port 8888)
- ✅ One frontend location (/root/sporttrader/frontend/dist/)
- ✅ One nginx config (maxevsports)
- ✅ No confusion during deployments

---

## 🔧 How Port 8888 Started

Check these to see how port 8888 is started (so you know it will restart on reboot):

```bash
# Check systemd services
systemctl list-units --type=service | grep -E "uvicorn|maxev|sport"

# Check cron
crontab -l | grep uvicorn

# Check for startup scripts
cat /etc/rc.local

# If nothing found, you may need to create a systemd service for port 8888
```

---

## 📝 Post-Cleanup Verification Checklist

After removing port 8000, verify:

- [ ] Port 8888 is still running: `ps aux | grep 8888`
- [ ] Website loads: Visit `https://max-ev-sports.com`
- [ ] API works: Check any page that loads data
- [ ] Login works: Test authentication
- [ ] No nginx errors: `nginx -t`
- [ ] Only one frontend location exists
- [ ] Deployment scripts updated (if needed)

---

## 🎯 Summary

**Problem**: Two API servers (8000 and 8888) causing deployment confusion

**Solution**: Remove port 8000 completely

**Benefits**:
- ✅ No more confusion about which server to deploy to
- ✅ Clear deployment process
- ✅ Less resource usage
- ✅ Faster frontend updates (only one location to update)

**Risk**: **VERY LOW** - Port 8000 isn't being used by anything

---

## 🚀 Execute Cleanup Now

```bash
# SSH to VPS
ssh root@148.230.87.135

# 1. Verify port 8888 works
curl -I http://localhost:8888/api/ui/best-plays

# 2. Kill port 8000
pkill -f "uvicorn.*8000"

# 3. Remove nginx config
rm /etc/nginx/sites-enabled/sporttrader
nginx -s reload

# 4. Verify everything still works
curl -I https://max-ev-sports.com/
ps aux | grep uvicorn

# Done! 🎉
```

---

**Next Steps**: After cleanup, update any deployment scripts to only target the one correct location.
