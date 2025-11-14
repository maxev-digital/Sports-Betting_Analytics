# FIX: Enable OAuth 1.0a for DM Sending

## Problem
Your X API credentials are correct format, but getting **401 Unauthorized** because:
- OAuth 1.0a is not enabled in your app settings
- OR Access tokens don't have "Read and Write" permissions

---

## Solution (5 minutes)

### Step 1: Go to X Developer Portal
https://developer.x.com/en/portal/dashboard

### Step 2: Select Your App
Click on your app name

### Step 3: Go to Settings Tab
Click the **"Settings"** tab at the top

### Step 4: Set Up User Authentication
Scroll down to **"User authentication settings"**

Click **"Set up"** (or "Edit" if already configured)

### Step 5: Configure OAuth 1.0a

**App permissions:**
- Select: **"Read and Write and Direct Messages"**

**Type of App:**
- Select: **"Web App, Automated App or Bot"**

**App info:**
- Callback URI: `https://max-ev-sports.com/callback` (can be anything)
- Website URL: `https://max-ev-sports.com`

Click **"Save"**

### Step 6: Regenerate Access Tokens

**IMPORTANT:** After changing permissions, you MUST regenerate tokens!

1. Go to **"Keys and tokens"** tab
2. Under "Access Token and Secret", click **"Regenerate"**
3. Copy the new tokens:
   - Access Token (starts with numbers)
   - Access Token Secret

### Step 7: Update Your .env File

Replace the old Access Token & Secret in `backend/.env`:

```env
# Keep API Key/Secret the same
X_API_KEY=dVlDZ1JUMFV0THRjWUpnYk9IczU6MTpjaQ
X_API_SECRET=38KaglxVizBmIQ_muQ5ByXVrsZAki4aQ9X6kIGYDcnXSswB1lA

# Replace these with NEW tokens
X_ACCESS_TOKEN=your_new_access_token_here
X_ACCESS_SECRET=your_new_access_secret_here
```

### Step 8: Test Again

```bash
python test_x_detailed.py
```

You should see:
```
[OK] Authenticated as: @YourHandle
[OK] DM permission working
```

---

## Quick Checklist

- [ ] Go to Developer Portal → Your App → Settings
- [ ] Enable "Read and Write and Direct Messages"
- [ ] Set Type of App to "Web App, Automated App or Bot"
- [ ] Click Save
- [ ] Go to Keys and tokens tab
- [ ] Regenerate Access Token & Secret
- [ ] Copy new tokens
- [ ] Update backend/.env
- [ ] Test with: `python test_x_detailed.py`

---

## Why This Happens

X apps default to "Read only" permissions. When you generate Access Tokens with "Read only", they're permanently locked to that permission level even if you change app settings later.

**Solution:** Regenerate tokens AFTER changing permissions.

---

Once this is done, you'll be ready to send DMs! 🚀
