# Get the CORRECT X API Credentials

## Problem: You Have OAuth 2.0, But Need OAuth 1.0a

**What you currently have:**
- OAuth 2.0 Client ID & Secret (can't send DMs with Tweepy)

**What you need:**
- OAuth 1.0a Consumer Keys (required for DM sending)

---

## Step-by-Step: Get OAuth 1.0a Consumer Keys

### 1. Go to X Developer Portal
https://developer.x.com/en/portal/dashboard

### 2. Click Your App

### 3. Go to "Keys and tokens" Tab

### 4. Look for TWO SECTIONS:

#### Section 1: "Consumer Keys" (OAuth 1.0a) ← GET THESE
```
API Key and Secret
[Regenerate button]

API Key: xxxxxxxxxxxxxxxxxxxx (25 characters, NO colons)
API Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (50 characters)
```

#### Section 2: "Client ID and Client Secret" (OAuth 2.0) ← NOT THESE
```
Client ID: xxxxx:x:xx (has colons - THIS IS WHAT YOU CURRENTLY HAVE)
Client Secret: xxxxxxxxxxxxxxxx
```

---

## What to Copy

From **Section 1** ("Consumer Keys"):

1. **API Key** (also called "Consumer Key")
   - Should be ~25 characters
   - Should NOT have colons
   - Example format: `xvz1evFS4wEEPTGEFPHBog`

2. **API Key Secret** (also called "Consumer Secret")
   - Should be ~50 characters
   - Example format: `L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg`

Then from **"Authentication Tokens"** section below:

3. **Access Token**
   - Format: `1234567890-xxxxxxxxxxxxxxxxx`
   - You already have this: `1853837572327227392-a7l9jcb1GSv5kl78OJAj50tlE6wjjs`

4. **Access Token Secret**
   - You already have this: `cMIwvyE6IZmDNfj6t1yQs03Iym3PmY2kRNT4pHL6LpOhM`

---

## Update .env With Correct Credentials

Replace ONLY the first two lines in `backend/.env`:

```env
# Use Consumer Keys from Section 1 (NOT Client ID)
X_API_KEY=your_25_char_consumer_key_here
X_API_SECRET=your_50_char_consumer_secret_here

# Keep your current Access Token & Secret
X_ACCESS_TOKEN=1853837572327227392-a7l9jcb1GSv5kl78OJAj50tlE6wjjs
X_ACCESS_SECRET=cMIwvyE6IZmDNfj6t1yQs03Iym3PmY2kRNT4pHL6LpOhM
```

---

## Visual Guide

In the X Developer Portal, you should see:

```
┌─────────────────────────────────────────────┐
│ Consumer Keys (OAuth 1.0a)         ← THIS! │
├─────────────────────────────────────────────┤
│ API Key:    xvz1evFS4wE...         [View]  │
│ API Secret: L8qq9PZyRg6...  [Regenerate]   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Authentication Tokens                       │
├─────────────────────────────────────────────┤
│ Access Token:  1234567890-xxx  [Regenerate]│
│ Access Secret: xxxxxxxxx...         [View] │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Client ID and Secret (OAuth 2.0)  ← NOT!   │
├─────────────────────────────────────────────┤
│ Client ID:     xxxxx:1:xx           [View] │
│ Client Secret: xxxxxxxxx     [Regenerate]   │
└─────────────────────────────────────────────┘
```

You currently have credentials from the **bottom box** (OAuth 2.0).
You need credentials from the **top box** (OAuth 1.0a Consumer Keys).

---

## After You Get Them

Once you have the correct Consumer Keys, tell me and I'll update the `.env` file and test immediately!

---

**TL;DR:** Look for "Consumer Keys" section (not "Client ID"), copy the API Key & Secret from there.
