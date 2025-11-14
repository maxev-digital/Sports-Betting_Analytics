# 🛡️ CLOUDFLARE PRO SECURITY SETUP GUIDE
**MAX EV SPORTS - Complete Security Configuration**

---

## 🎯 OVERVIEW

**Your Site:** max-ev-sports.com
**Package:** Cloudflare Pro
**Goal:** Maximum security + performance

**Cloudflare Pro Features:**
- ✅ Advanced DDoS protection
- ✅ Web Application Firewall (WAF)
- ✅ Rate limiting (10 rules)
- ✅ Advanced SSL/TLS
- ✅ Image optimization
- ✅ Mobile optimization
- ✅ 20+ Page Rules

---

## 📋 COMPLETE SECURITY CHECKLIST

### ✅ PHASE 1: SSL/TLS SECURITY (5 minutes)

#### Step 1.1: Enable Full (Strict) SSL
1. Login to Cloudflare Dashboard: https://dash.cloudflare.com/
2. Select your domain: **max-ev-sports.com**
3. Go to **SSL/TLS** tab
4. Select **Full (strict)** mode
   - This encrypts traffic between Cloudflare and your origin server
   - Validates your origin SSL certificate

**Why:** Prevents man-in-the-middle attacks

#### Step 1.2: Enable Always Use HTTPS
1. Still in **SSL/TLS** tab
2. Go to **Edge Certificates**
3. Enable **Always Use HTTPS**
4. Enable **Automatic HTTPS Rewrites**

**Why:** Forces all HTTP traffic to HTTPS

#### Step 1.3: Enable HTTP Strict Transport Security (HSTS)
1. In **SSL/TLS** → **Edge Certificates**
2. Scroll to **HTTP Strict Transport Security (HSTS)**
3. Click **Enable HSTS**
4. Configure:
   ```
   Max Age Header: 6 months
   Apply HSTS policy to subdomains: Yes
   Preload: Yes (optional but recommended)
   No-Sniff Header: Yes
   ```

**⚠️ WARNING:** Only enable HSTS if you're 100% sure you'll always use HTTPS. Cannot be easily reversed.

#### Step 1.4: Minimum TLS Version
1. In **SSL/TLS** → **Edge Certificates**
2. Set **Minimum TLS Version** to **TLS 1.2** or higher
3. Disable older, insecure protocols

---

### ✅ PHASE 2: FIREWALL & WAF (10 minutes)

#### Step 2.1: Enable Web Application Firewall (WAF)
1. Go to **Security** → **WAF**
2. Enable **Managed Rules**
3. Enable these rulesets:
   - ✅ **Cloudflare Managed Ruleset** (set to High sensitivity)
   - ✅ **OWASP ModSecurity Core Rule Set**
   - ✅ **Cloudflare Specials**

**Why:** Protects against SQL injection, XSS, and other common attacks

#### Step 2.2: Create Firewall Rules

**Go to Security → WAF → Firewall rules**

**Rule #1: Block Known Bad Bots**
```
Name: Block Bad Bots
Field: Known Bots
Operator: equals
Value: Bad Bot
Action: Block
```

**Rule #2: Challenge Suspicious Countries (Optional)**
```
Name: Challenge High-Risk Countries
Field: Country
Operator: is in
Value: [Countries with high attack rates - adjust as needed]
Action: Managed Challenge
```

**Rule #3: Block Common Attack Patterns**
```
Name: Block SQL Injection Attempts
Field: URI Path
Operator: contains
Value: union select OR ' OR 1=1 OR <script> OR ../
Action: Block
```

**Rule #4: Protect Admin/Login Pages**
```
Name: Extra Protection for Admin
Field: URI Path
Operator: contains
Value: /admin OR /login OR /api/auth
Action: Managed Challenge
```

**Rule #5: Rate Limit API Endpoints**
```
Name: API Rate Limiting
Field: URI Path
Operator: starts with
Value: /api/
Action: Rate Limit (see Step 2.3)
```

#### Step 2.3: Configure Rate Limiting
1. Go to **Security** → **WAF** → **Rate limiting rules**
2. Click **Create rule**

**Rate Limit Rule #1: API Protection**
```
Rule name: API Rate Limit
When incoming requests match:
  - URI Path starts with /api/

With the same value of:
  - IP Address

Count requests:
  - Requests: 100 requests
  - Period: 10 seconds

Then take action:
  - Block
  - For duration: 1 hour
```

**Rate Limit Rule #2: Login Protection**
```
Rule name: Login Brute Force Protection
When incoming requests match:
  - URI Path contains /login OR /api/auth/login

With the same value of:
  - IP Address

Count requests:
  - Requests: 5 requests
  - Period: 5 minutes

Then take action:
  - Block
  - For duration: 15 minutes
```

**Rate Limit Rule #3: Signup Protection**
```
Rule name: Signup Abuse Protection
When incoming requests match:
  - URI Path contains /signup OR /api/auth/register

With the same value of:
  - IP Address

Count requests:
  - Requests: 3 requests
  - Period: 1 hour

Then take action:
  - Block
  - For duration: 24 hours
```

---

### ✅ PHASE 3: DDoS PROTECTION (5 minutes)

#### Step 3.1: Enable Advanced DDoS Protection
1. Go to **Security** → **DDoS**
2. Verify **Advanced DDoS Protection** is enabled (included with Pro)
3. Configure **HTTP DDoS Attack Protection**
   - Sensitivity: High
   - Action: Block

#### Step 3.2: Enable Bot Fight Mode
1. Go to **Security** → **Bots**
2. Enable **Bot Fight Mode**
3. Configure:
   ```
   Definitely automated: Block
   Likely automated: Challenge
   Verified bots: Allow (Google, Bing, etc.)
   ```

**Why:** Stops automated attacks and scrapers

---

### ✅ PHASE 4: CONTENT SECURITY (10 minutes)

#### Step 4.1: Configure Security Headers
1. Go to **Rules** → **Transform Rules** → **Modify Response Header**
2. Create rule: **Security Headers**

**Add these headers:**
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline';
```

**How to add:**
- Click **Create rule**
- Rule name: "Security Headers"
- When incoming requests match: All incoming requests
- Then: Set static → Add header for each above

#### Step 4.2: Enable Browser Integrity Check
1. Go to **Security** → **Settings**
2. Enable **Browser Integrity Check**

**Why:** Blocks requests from sources that don't have a user agent or are commonly associated with abusive traffic

#### Step 4.3: Enable Security Level
1. Still in **Security** → **Settings**
2. Set **Security Level** to **High**

**Why:** More aggressive challenge for suspicious visitors

---

### ✅ PHASE 5: PERFORMANCE & OPTIMIZATION (5 minutes)

#### Step 5.1: Enable Caching
1. Go to **Caching** → **Configuration**
2. Set **Caching Level** to **Standard**
3. Enable **Always Online**
4. Set **Browser Cache TTL** to **4 hours**

#### Step 5.2: Create Page Rules for Static Assets
1. Go to **Rules** → **Page Rules**
2. Click **Create Page Rule**

**Page Rule #1: Cache Static Assets**
```
URL pattern: max-ev-sports.com/assets/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
  - Browser Cache TTL: 1 month
```

**Page Rule #2: Cache Images**
```
URL pattern: max-ev-sports.com/*.{jpg,jpeg,png,gif,svg,webp}
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
```

**Page Rule #3: Extra Security for Admin**
```
URL pattern: max-ev-sports.com/admin*
Settings:
  - Security Level: High
  - Cache Level: Bypass
  - Disable Performance
```

**Page Rule #4: API Rate Limiting**
```
URL pattern: max-ev-sports.com/api/*
Settings:
  - Cache Level: Bypass
  - Security Level: High
```

#### Step 5.3: Enable Auto Minify
1. Go to **Speed** → **Optimization**
2. Enable **Auto Minify** for:
   - ✅ JavaScript
   - ✅ CSS
   - ✅ HTML

#### Step 5.4: Enable Brotli Compression
1. Still in **Speed** → **Optimization**
2. Enable **Brotli** compression

---

### ✅ PHASE 6: MONITORING & ALERTS (5 minutes)

#### Step 6.1: Configure Security Notifications
1. Go to **Notifications**
2. Enable these alerts:
   - ✅ **DDoS Attack Alerts**
   - ✅ **WAF Alerts** (when rules trigger)
   - ✅ **Rate Limiting Alerts**
   - ✅ **SSL/TLS Certificate Expiration**
   - ✅ **Origin Error Rate Increased**

#### Step 6.2: Set Up Email Notifications
1. In **Notifications** → **Destinations**
2. Add email: your admin email
3. Add webhook (optional): for Slack/Discord

---

### ✅ PHASE 7: ORIGIN SERVER PROTECTION (10 minutes)

#### Step 7.1: Whitelist Cloudflare IPs Only
**On your Hostinger server, configure firewall to only allow Cloudflare IPs:**

This prevents attackers from bypassing Cloudflare and hitting your origin directly.

**Cloudflare IP Ranges (IPv4):**
```
173.245.48.0/20
103.21.244.0/22
103.22.200.0/22
103.31.4.0/22
141.101.64.0/18
108.162.192.0/18
190.93.240.0/20
188.114.96.0/20
197.234.240.0/22
198.41.128.0/17
162.158.0.0/15
104.16.0.0/13
104.24.0.0/14
172.64.0.0/13
131.0.72.0/22
```

**How to implement:**
1. SSH into your Hostinger server:
   ```bash
   ssh root@your-server-ip
   ```

2. Create firewall script:
   ```bash
   nano /etc/cloudflare-whitelist.sh
   ```

3. Add this script:
   ```bash
   #!/bin/bash

   # Clear existing rules
   iptables -F

   # Allow Cloudflare IPs
   for ip in 173.245.48.0/20 103.21.244.0/22 103.22.200.0/22 103.31.4.0/22 141.101.64.0/18 108.162.192.0/18 190.93.240.0/20 188.114.96.0/20 197.234.240.0/22 198.41.128.0/17 162.158.0.0/15 104.16.0.0/13 104.24.0.0/14 172.64.0.0/13 131.0.72.0/22; do
     iptables -A INPUT -p tcp --dport 80 -s $ip -j ACCEPT
     iptables -A INPUT -p tcp --dport 443 -s $ip -j ACCEPT
   done

   # Allow localhost
   iptables -A INPUT -i lo -j ACCEPT

   # Allow established connections
   iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

   # Allow SSH (important!)
   iptables -A INPUT -p tcp --dport 22 -j ACCEPT

   # Drop everything else
   iptables -A INPUT -p tcp --dport 80 -j DROP
   iptables -A INPUT -p tcp --dport 443 -j DROP

   # Save rules
   iptables-save > /etc/iptables/rules.v4
   ```

4. Make executable and run:
   ```bash
   chmod +x /etc/cloudflare-whitelist.sh
   ./etc/cloudflare-whitelist.sh
   ```

#### Step 7.2: Restore Real Visitor IP
**Update your backend to see real visitor IPs (not Cloudflare IPs):**

**In your FastAPI backend (`main.py`):**
```python
from fastapi import Request

@app.middleware("http")
async def get_real_ip(request: Request, call_next):
    # Get real IP from Cloudflare header
    real_ip = request.headers.get("CF-Connecting-IP")
    if real_ip:
        request.state.real_ip = real_ip
    else:
        request.state.real_ip = request.client.host

    response = await call_next(request)
    return response
```

---

### ✅ PHASE 8: BACKUP & RECOVERY (5 minutes)

#### Step 8.1: Enable Cloudflare Analytics
1. Go to **Analytics & Logs** → **Analytics**
2. Review baseline traffic patterns
3. Set up custom dashboards

#### Step 8.2: Document Your Configuration
1. Take screenshots of all settings
2. Save this guide
3. Document any custom rules

#### Step 8.3: Test Your Security
1. Use SSL Labs: https://www.ssllabs.com/ssltest/
   - Should get **A+ rating**
2. Use Security Headers: https://securityheaders.com/
   - Should get **A rating**
3. Test WAF: Try basic SQL injection (on test endpoint)
4. Test rate limiting: Make 100+ API calls rapidly

---

## 🔥 CRITICAL SECURITY RULES SUMMARY

### Must-Have Settings:

**SSL/TLS:**
- ✅ Full (Strict) mode
- ✅ Always Use HTTPS
- ✅ HSTS enabled
- ✅ TLS 1.2 minimum

**Firewall:**
- ✅ WAF enabled (High sensitivity)
- ✅ Bot Fight Mode enabled
- ✅ Rate limiting on /api/, /login, /signup
- ✅ Security level: High

**Headers:**
- ✅ X-Frame-Options: DENY
- ✅ X-Content-Type-Options: nosniff
- ✅ Content-Security-Policy configured

**Origin Protection:**
- ✅ Whitelist Cloudflare IPs only
- ✅ Restore real visitor IPs

---

## 📊 EXPECTED RESULTS

**After configuration:**
- ✅ SSL Labs: A+ rating
- ✅ Security Headers: A rating
- ✅ DDoS protection: Automatic
- ✅ Bot traffic: 90% reduction
- ✅ SQL injection: Blocked
- ✅ Brute force: Prevented
- ✅ Page load: 30-50% faster

---

## 🚨 EMERGENCY PROCEDURES

### If Under Attack:

**Step 1: Enable "I'm Under Attack" Mode**
1. Go to **Security** → **Settings**
2. Enable **Under Attack Mode**
3. All visitors will see a challenge page for 5 seconds

**Step 2: Review Firewall Events**
1. Go to **Security** → **Events**
2. Identify attack patterns
3. Create blocking rules

**Step 3: Block Attack Source**
1. Go to **Security** → **WAF** → **Tools**
2. Block by:
   - IP address
   - Country
   - ASN (Autonomous System Number)
   - User Agent

---

## 🧪 TESTING CHECKLIST

After setup, test these:

- [ ] Visit https://max-ev-sports.com (should work)
- [ ] Visit http://max-ev-sports.com (should redirect to HTTPS)
- [ ] Test SSL: https://www.ssllabs.com/ssltest/analyze.html?d=max-ev-sports.com
- [ ] Test headers: https://securityheaders.com/?q=max-ev-sports.com
- [ ] Try login 6 times fast (should block after 5)
- [ ] Make 101 API calls (should block after 100)
- [ ] Check analytics (should see traffic)
- [ ] Verify origin server only accepts Cloudflare IPs

---

## 📱 MOBILE APP / API CONSIDERATIONS

If you have a mobile app or API:

**Add these IPs to allowlist:**
- Your development IPs
- Your CI/CD pipeline IPs
- Your monitoring service IPs

**API Token Security:**
- Use JWT tokens with short expiration
- Rotate API keys regularly
- Monitor for unusual API usage patterns

---

## 💰 COST OPTIMIZATION

**Cloudflare Pro: $20/month**

**What you get:**
- Advanced DDoS protection
- WAF with managed rulesets
- 10 rate limiting rules
- 20 page rules
- Image optimization
- Mobile optimization
- Priority support

**Worth it?** Absolutely for a production app with paying users.

---

## 🔗 USEFUL LINKS

- Cloudflare Dashboard: https://dash.cloudflare.com/
- SSL Test: https://www.ssllabs.com/ssltest/
- Security Headers Test: https://securityheaders.com/
- Cloudflare Status: https://www.cloudflarestatus.com/
- Cloudflare Docs: https://developers.cloudflare.com/

---

## ✅ FINAL CHECKLIST

Before marking complete:

- [ ] SSL/TLS set to Full (Strict)
- [ ] HSTS enabled
- [ ] WAF enabled with managed rules
- [ ] Rate limiting configured (3 rules minimum)
- [ ] Bot Fight Mode enabled
- [ ] Security headers added
- [ ] Page rules created
- [ ] Origin server whitelisting Cloudflare IPs
- [ ] Real IP restoration in backend
- [ ] Notifications configured
- [ ] Tested all security measures
- [ ] SSL Labs A+ rating achieved
- [ ] Security Headers A rating achieved

---

**Configuration Time: 45-60 minutes**
**Security Level After: Enterprise-grade**
**ROI: Prevents thousands in damages from attacks**

---

Created: October 29, 2025
For: MAX EV SPORTS - Cloudflare Pro Security Setup
Domain: max-ev-sports.com
