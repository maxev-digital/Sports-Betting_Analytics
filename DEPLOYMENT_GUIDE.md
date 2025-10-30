# Deployment Guide for MAX-EV-SPORTS

## Quick Deploy (One Command)

```bash
./deploy.sh "Your commit message here"
```

That's it! The script automatically:
1. ✅ Commits your changes to Git
2. ✅ Rebuilds the frontend (clean build)
3. ✅ Deploys backend to VPS
4. ✅ Deploys frontend to VPS
5. ✅ Restarts the backend service
6. ✅ Verifies everything is working

## Examples

**Deploy with custom message:**
```bash
./deploy.sh "Add new NBA momentum feature"
```

**Deploy with default message:**
```bash
./deploy.sh
```
*(Uses: "Update backend and frontend")*

## What Gets Deployed

### Backend Files:
- main.py - Main API server
- game_tracker.py - Live game tracking
- stripe_service.py - Payment processing
- espn_nba_client.py - NBA data fetching
- config.py - Configuration
- alert_monitor.py - Real-time alerts
- auth.py - Authentication

### Frontend Files:
- Entire frontend/dist/ folder (rebuilt fresh)
- All React components
- All images and assets
- SliderImages for pricing page

## Troubleshooting

**If deployment fails:**
1. Check the error message - script will show exactly where it failed
2. View backend logs:
   ```bash
   ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "journalctl -u sporttrader -n 50"
   ```

**Need Help?**
- Check backend logs: ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "journalctl -u sporttrader -f"
- Restart service: ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"
