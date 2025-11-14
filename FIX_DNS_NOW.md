# 🚨 URGENT - FIX DNS TO RESTORE WEBSITE

**Problem:** Your DNS points to the WRONG server IP address.

**Current DNS:** 148.230.87.135 (DOWN - not responding)
**Correct Server:** 72.60.43.168 (UP - site is working!)

---

## ✅ IMMEDIATE FIX (5 MINUTES)

### Step 1: Login to Cloudflare Dashboard
1. Go to https://dash.cloudflare.com/
2. Login with your credentials
3. Select domain: **max-ev-sports.com**

### Step 2: Update DNS Records
1. Click **DNS** tab on the left
2. Find these A records:
   ```
   A    @    148.230.87.135    (current - WRONG)
   A    www  148.230.87.135    (current - WRONG)
   ```

3. Click **Edit** on each record
4. Change IP to: **72.60.43.168**
5. Keep **Proxy status: Proxied** (orange cloud) ✅
6. Click **Save**

**After the fix:**
```
A    @    72.60.43.168    Proxied (orange cloud)
A    www  72.60.43.168    Proxied (orange cloud)
```

### Step 3: Verify (Wait 2-5 minutes)
```bash
# Test site accessibility
curl -I https://max-ev-sports.com
```

Should return: **HTTP/1.1 200 OK** or **HTTP/2 200**

---

## 🔍 WHAT HAPPENED

**Server Status:**
- ✅ **72.60.43.168** - Working perfectly (nginx running, SSL working)
- ❌ **148.230.87.135** - Not responding (connection timeout)

**Evidence:**
```bash
# Working server
$ ping 72.60.43.168
Reply from 72.60.43.168: bytes=32 time=229ms TTL=46 ✅

# Dead server
$ ping 148.230.87.135
Request timed out. ❌

# Site works on correct IP
$ curl -I -k -H "Host: max-ev-sports.com" https://72.60.43.168
HTTP/1.1 200 OK ✅
```

---

## 🎯 AFTER DNS IS FIXED

Once the site is back online (2-5 minutes after DNS change):

1. **Test the site:**
   - https://max-ev-sports.com ✅ Should load
   - https://www.max-ev-sports.com ✅ Should load

2. **Then proceed with Cloudflare Pro Security Setup:**
   - Follow `CLOUDFLARE_QUICK_START.md` (15 minutes)
   - Or full guide: `CLOUDFLARE_PRO_SECURITY_SETUP.md` (60 minutes)

3. **Logo will load in emails** (previously blocked by site being down)

---

## 🚀 DO THIS NOW

1. [ ] Login to Cloudflare dashboard
2. [ ] Change DNS A records from 148.230.87.135 → 72.60.43.168
3. [ ] Wait 2-5 minutes for propagation
4. [ ] Test: visit https://max-ev-sports.com
5. [ ] Proceed with security configuration

**Time to fix:** 5 minutes
**Site will be live immediately after DNS updates**

---

Created: October 29, 2025
Issue: DNS pointing to wrong server IP
Fix: Update Cloudflare DNS to 72.60.43.168
