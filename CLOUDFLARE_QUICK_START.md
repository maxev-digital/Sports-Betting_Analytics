# ⚡ CLOUDFLARE PRO - QUICK START (15 MINUTES)

**Get 80% of security benefits in 15 minutes**

---

## 🚀 IMMEDIATE ACTIONS (Do these NOW)

### ✅ 1. SSL/TLS Security (3 minutes)
1. Go to https://dash.cloudflare.com/
2. Select **max-ev-sports.com**
3. **SSL/TLS** tab → Select **Full (Strict)**
4. **Edge Certificates** → Enable **Always Use HTTPS**
5. **Edge Certificates** → Enable **Automatic HTTPS Rewrites**

### ✅ 2. Enable WAF (2 minutes)
1. **Security** → **WAF** → **Managed Rules**
2. Enable **Cloudflare Managed Ruleset**
3. Enable **OWASP ModSecurity Core Rule Set**

### ✅ 3. Bot Protection (2 minutes)
1. **Security** → **Bots**
2. Enable **Bot Fight Mode**

### ✅ 4. Rate Limiting - Login Protection (3 minutes)
1. **Security** → **WAF** → **Rate limiting rules**
2. Create rule:
```
Name: Login Protection
Match: URI Path contains "/login"
Rate: 5 requests per 5 minutes per IP
Action: Block for 15 minutes
```

### ✅ 5. Security Headers (3 minutes)
1. **Rules** → **Transform Rules** → **Modify Response Header**
2. Create rule: "Security Headers"
3. Add headers:
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

### ✅ 6. Security Level (1 minute)
1. **Security** → **Settings**
2. Set **Security Level** to **High**

### ✅ 7. Enable Notifications (1 minute)
1. **Notifications**
2. Enable **DDoS Attack Alerts**
3. Add your email

---

## 🧪 TEST YOUR SECURITY (5 minutes)

### Test 1: SSL Check
Visit: https://www.ssllabs.com/ssltest/analyze.html?d=max-ev-sports.com

**Target:** A+ rating

### Test 2: Security Headers
Visit: https://securityheaders.com/?q=max-ev-sports.com

**Target:** A rating (after headers added)

### Test 3: Manual Check
- Visit https://max-ev-sports.com ✅ Should work
- Visit http://max-ev-sports.com ✅ Should redirect to HTTPS

---

## 📊 PRIORITY ORDER

**Critical (Do today):**
1. SSL Full (Strict)
2. WAF enabled
3. Rate limiting on login

**Important (Do this week):**
4. Bot Fight Mode
5. Security headers
6. Origin IP whitelisting

**Recommended (Do this month):**
7. Advanced rate limiting
8. Page rules
9. Monitoring setup

---

## 🔥 IF SITE IS DOWN

**Quick fixes:**

1. **Pause Cloudflare temporarily:**
   - Overview → Advanced Actions → Pause Cloudflare on Site
   - This bypasses Cloudflare (use only if emergency)

2. **Check SSL mode:**
   - If site down after enabling Full (Strict)
   - Change to "Full" mode temporarily
   - Fix origin SSL certificate
   - Switch back to Full (Strict)

3. **Disable WAF temporarily:**
   - Security → WAF → Disable
   - Check if site works
   - If yes, WAF rule blocking legitimate traffic
   - Re-enable and adjust rules

---

**Full guide:** `CLOUDFLARE_PRO_SECURITY_SETUP.md`

**Time to complete:** 15 minutes
**Security improvement:** 80%
