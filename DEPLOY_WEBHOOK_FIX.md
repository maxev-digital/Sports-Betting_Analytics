# Deploy Webhook Handler Fix to Production

## Status
- Code committed to Git: 1614b27
- Code pushed to GitHub: https://github.com/anashp78/MaxEvSports.git
- Changes: Updated webhook handler with customer_id lookup fallback

## What This Fixes
The production backend was returning "detail not found" because it didn't have the updated webhook handler code that looks up users by stripe_customer_id when user_id is missing from webhook metadata.

## Deployment Steps

### Step 1: SSH to Production VPS
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
```

### Step 2: Navigate to Application Directory
```bash
cd /root/sporttrader
```

### Step 3: Pull Latest Changes from GitHub
```bash
git pull origin main
```

You should see:
```
Updating b80058a..1614b27
Fast-forward
 backend/main.py | XX files changed
```

### Step 4: Restart Backend Service
```bash
systemctl restart sporttrader
```

### Step 5: Verify Service is Running
```bash
systemctl status sporttrader --no-pager -l | head -20
```

You should see:
```
● sporttrader.service - Sport Trader Backend
     Active: active (running)
```

### Step 6: Check Service Logs
```bash
journalctl -u sporttrader -n 50 --no-pager | tail -20
```

Look for:
```
INFO:     Application startup complete.
```

### Step 7: Exit SSH
```bash
exit
```

## Verify Deployment

### Test Webhook Endpoint
From your local machine:
```bash
curl -X POST https://max-ev-sports.com/api/stripe/webhook
```

You should see a 400 error (expected - missing signature), not "detail not found"

### Check Stripe Dashboard
Visit: https://dashboard.stripe.com/test/webhooks

The webhook endpoint should now show successful responses (200 OK) instead of "detail not found"

### Test Payment Flow
1. Go to https://max-ev-sports.com
2. Log in with admin account
3. Go to Pricing page
4. Click Subscribe on any tier
5. Complete payment with test card: 4242 4242 4242 4242
6. Check that subscription is created in database

## Rollback (If Needed)
If something goes wrong:
```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
cd /root/sporttrader
git reset --hard b80058a
systemctl restart sporttrader
```

## Frontend Deployment (Optional - Later)
The frontend build is ready in `C:/Users/nashr/frontend/dist`. To deploy:

```bash
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
rm -rf /var/www/sporttrader/*
# Then SCP the dist folder
exit

scp -i ~/.ssh/hostinger_vps -r C:/Users/nashr/frontend/dist/* root@148.230.87.135:/var/www/sporttrader/

ssh -i ~/.ssh/hostinger_vps root@148.230.87.135
systemctl reload nginx
```

## Next Steps After Deployment
1. Test real payment end-to-end
2. Verify subscription creation in production database
3. Check feature access is working correctly
4. Monitor webhook events in Stripe Dashboard
