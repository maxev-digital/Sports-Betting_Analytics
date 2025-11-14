# Stress Test Analysis: 1000 New Signups Campaign

**Date:** 2025-11-12
**Current Load:** 12 active connections, 0.42 load average
**Target:** Handle 1000 new signups from X campaign

---

## Current Infrastructure

### VPS Specifications
- **Provider:** Hostinger VPS (148.230.87.135)
- **CPU:** 2 cores (AMD EPYC 9354P)
- **RAM:** 8GB (6.8GB available)
- **Disk:** 96GB (84GB free)
- **Current Load:** 0.42 (very light)
- **Current RAM Usage:** 991MB (12%)

### Software Stack
- **Backend:** Single Uvicorn worker (FastAPI + Python)
- **Frontend:** Nginx (4 workers)
- **Database:** SQLite (multiple .db files)
- **Storage:** File-based (JSON + SQLite)
- **WebSockets:** Enabled for real-time updates

### Current Usage
- **Active Connections:** 12 established
- **Backend CPU:** 47% (HIGH for current load!)
- **Backend RAM:** 419MB (5.1%)
- **Port 8000 Connections:** 146 (mostly TIME_WAIT from nginx proxy)

---

## Bottleneck Analysis

### 🔴 CRITICAL BOTTLENECKS

#### 1. **Single Uvicorn Worker** (HIGHEST PRIORITY)
**Current:** 1 worker handling all requests
**Problem:**
- Python GIL (Global Interpreter Lock) limits to 1 CPU core
- Can only handle ~100-200 concurrent requests
- Already using 47% CPU at LOW load
- **WILL FAIL** with 1000 concurrent users

**Impact at 1000 users:**
- Expected load: 500-1000+ concurrent requests during peak
- Response times: 5-30 seconds (currently <1s)
- Timeout rate: 60-80% of requests
- Service crashes likely

**Solution:**
```bash
# Update systemd service to use 4 workers
ExecStart=/root/sporttrader/backend/venv/bin/uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --timeout-keep-alive 30
```

**Cost:** FREE (software change only)
**Time:** 5 minutes
**Impact:** 4x capacity increase

---

#### 2. **SQLite Database Under Concurrent Load**
**Current:** Multiple SQLite databases (users.db, subscriptions.db, sessions.json, etc.)
**Problem:**
- SQLite locks entire database for writes
- No connection pooling
- File I/O becomes bottleneck at scale
- Sessions stored in JSON (no locking mechanism)

**Impact at 1000 users:**
- Database lock contention
- Failed writes (especially sessions, referrals)
- Data corruption risk with JSON files
- Average query time: 500ms-2s (currently <10ms)

**Immediate Solution (LOW EFFORT):**
```python
# Add connection pooling and WAL mode
import sqlite3
conn = sqlite3.connect('database.db', check_same_thread=False)
conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging
conn.execute('PRAGMA synchronous=NORMAL')
conn.execute('PRAGMA cache_size=10000')
```

**Long-term Solution (RECOMMENDED):**
- Migrate to PostgreSQL (can handle 10,000+ connections)
- Cost: FREE (self-hosted) or $25/mo (managed)
- Time: 4-8 hours migration
- Impact: 100x capacity increase

---

#### 3. **External API Rate Limits**
**Current APIs:**
- **The Odds API:** 500 requests/day (FREE tier)
- **SportsDataIO:** Unknown limits
- **TeamRankings:** Web scraping (no official API)

**Problem at 1000 users:**
- Odds API: 500/day ÷ 1000 users = **0.5 requests per user per day**
- Current usage: ~2000 requests/day (4x over limit!)
- Will hit rate limits in first hour

**Solutions:**

**A) Upgrade Odds API (REQUIRED)**
- Competitor Plan: $79/mo = 10,000 requests/day
- Professional Plan: $199/mo = 50,000 requests/day
- **Recommendation:** Professional ($199/mo)
- Impact: Handles 50 requests/user/day

**B) Implement Aggressive Caching**
```python
# Cache odds for 30 seconds (currently refreshing every 5s)
ODDS_CACHE_TTL = 30  # seconds
# Reduces API calls by 83%
```

**C) Shared Data Model**
- All users see same odds data
- Update once, serve to all
- Current: Working correctly
- Just need to ensure cache is respected

---

### 🟡 MODERATE BOTTLENECKS

#### 4. **WebSocket Connection Limits**
**Current:** Broadcasting to all connected clients every 3 seconds
**Problem at 1000 users:**
- 1000 WebSocket connections = ~200MB RAM
- Broadcast overhead: 1000 messages every 3s = 333 msg/sec
- Network bandwidth: ~5 Mbps outbound

**VPS Network:** Likely 100-1000 Mbps (sufficient)
**Risk Level:** MEDIUM

**Solution:**
- Implement connection throttling
- Use Redis pub/sub for scalability
- Consider WebSocket load balancer

---

#### 5. **ML Model Predictions CPU Usage**
**Current:** 87 ML models running predictions
**Problem:**
- Each prediction: 10-50ms CPU time
- 1000 users requesting predictions concurrently
- 2 CPU cores = bottleneck

**Current behavior:**
- Models cached for 6 hours
- Predictions shared across users
- **Good design!**

**Improvement:**
- Move heavy predictions to background workers
- Use Redis queue for async processing
- Pre-generate predictions for popular games

---

### 🟢 MINOR CONCERNS

#### 6. **Nginx Performance**
**Current:** 4 workers, reverse proxy to backend
**Capacity:** Can handle 10,000+ requests/sec
**Verdict:** NOT a bottleneck

#### 7. **Disk Space**
**Current:** 13% used (13GB / 96GB)
**Growth:** ~100MB per 1000 users
**Verdict:** Sufficient for 100,000+ users

#### 8. **RAM**
**Current:** 6.8GB available
**Need:** ~2GB for 4 workers + 200MB WebSockets = 2.2GB
**Verdict:** Sufficient

---

## Projected Performance at 1000 Users

### WITHOUT CHANGES (Current Setup)
| Metric | Current | At 1000 Users | Status |
|--------|---------|---------------|--------|
| Response Time | <1s | 5-30s | 🔴 FAIL |
| Error Rate | <0.1% | 60-80% | 🔴 FAIL |
| CPU Usage | 47% | 100% (pinned) | 🔴 FAIL |
| Database Locks | 0 | 500+/sec | 🔴 FAIL |
| API Rate Limits | OK | Hit in 1 hour | 🔴 FAIL |
| **System Status** | **Healthy** | **CRASH** | 🔴 **DOWN** |

### WITH CRITICAL FIXES (Uvicorn Workers + API Upgrade)
| Metric | With Fixes | Status |
|--------|------------|--------|
| Response Time | 1-3s | 🟡 SLOW |
| Error Rate | 10-20% | 🟡 DEGRADED |
| CPU Usage | 85-95% | 🟡 HIGH |
| Database Locks | 100+/sec | 🟡 DEGRADED |
| API Rate Limits | OK | 🟢 OK |
| **System Status** | **DEGRADED** | 🟡 **LIMPING** |

### WITH ALL RECOMMENDED FIXES
| Metric | Fully Optimized | Status |
|--------|----------------|--------|
| Response Time | <1s | 🟢 OK |
| Error Rate | <1% | 🟢 OK |
| CPU Usage | 40-60% | 🟢 OK |
| Database Response | <50ms | 🟢 OK |
| API Rate Limits | OK | 🟢 OK |
| **System Status** | **HEALTHY** | 🟢 **READY** |

---

## Recommended Action Plan

### PHASE 1: CRITICAL (DO BEFORE LAUNCH) ⚠️
**Time Required:** 30 minutes
**Cost:** $199/mo

1. **Add Uvicorn Workers (5 min)**
   ```bash
   # Update /etc/systemd/system/sporttrader.service
   ExecStart=/root/sporttrader/backend/venv/bin/uvicorn main:app \
     --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 30

   systemctl daemon-reload
   systemctl restart sporttrader
   ```

2. **Upgrade Odds API (10 min)**
   - Subscribe to Professional Plan: $199/mo
   - 50,000 requests/day = 50 req/user/day for 1000 users
   - Update API key in .env

3. **Enable SQLite WAL Mode (5 min)**
   ```python
   # Add to database initialization
   PRAGMA journal_mode=WAL
   PRAGMA synchronous=NORMAL
   ```

4. **Increase Cache TTL (5 min)**
   ```python
   # Reduce API calls by caching odds for 30s instead of 5s
   ODDS_CACHE_TTL = 30
   ```

5. **Add Connection Limits (5 min)**
   ```python
   # In main.py, limit WebSocket connections per IP
   MAX_CONNECTIONS_PER_IP = 3
   ```

**Result:** System will handle 1000 users with 10-20% error rate (acceptable for launch)

---

### PHASE 2: OPTIMIZATION (FIRST WEEK)
**Time Required:** 1 day
**Cost:** FREE

1. **Add Redis Caching**
   - Cache user sessions (remove sessions.json)
   - Cache odds data (shared across users)
   - Cache ML predictions

2. **Add Database Connection Pooling**
   ```python
   from sqlalchemy.pool import QueuePool
   engine = create_engine('sqlite:///users.db', poolclass=QueuePool)
   ```

3. **Implement Rate Limiting**
   ```python
   from fastapi_limiter import FastAPILimiter
   # 100 requests per minute per user
   ```

4. **Add Monitoring**
   - Setup Prometheus + Grafana
   - Alert on high error rates
   - Track API usage

---

### PHASE 3: SCALE (IF GROWTH CONTINUES)
**Time Required:** 1 week
**Cost:** $100-300/mo

1. **Migrate to PostgreSQL**
   - Handles 10,000+ concurrent connections
   - Better performance under load
   - Managed service: $25-100/mo

2. **Add CDN for Frontend**
   - Cloudflare (currently using)
   - Offload static assets
   - Cost: FREE tier sufficient

3. **Upgrade VPS**
   - 4 CPU cores + 16GB RAM
   - Cost: ~$50-80/mo more
   - Needed at 3000+ users

4. **Add Load Balancer**
   - 2 VPS instances behind load balancer
   - Cost: $20/mo + $50/mo for 2nd VPS
   - Needed at 5000+ users

---

## Cost Breakdown

### Immediate (Phase 1)
| Item | Cost | Required? |
|------|------|-----------|
| Odds API Upgrade | $199/mo | ✅ REQUIRED |
| Software changes | FREE | ✅ REQUIRED |
| **Total** | **$199/mo** | |

### First Month (Phase 2)
| Item | Cost | Required? |
|------|------|-----------|
| Redis hosting | $15/mo | 🟡 Recommended |
| Monitoring tools | FREE (self-hosted) | 🟡 Recommended |
| **Total** | **$15/mo** | |

### If Growth Continues (Phase 3)
| Item | Cost | Required? |
|------|------|-----------|
| PostgreSQL managed | $25-100/mo | At 2000+ users |
| Upgraded VPS | +$50/mo | At 3000+ users |
| Load balancer | $70/mo | At 5000+ users |
| **Total** | **$145-220/mo** | |

---

## Real-World Scenarios

### Scenario 1: Launch Day Spike
**Situation:** 1000 signups in first 24 hours, 200 concurrent users during peak

**With Phase 1 fixes:**
- ✅ System stays online
- 🟡 Response times: 2-4 seconds (acceptable)
- 🟡 Some users see delays during peak
- ✅ No data loss
- **Verdict:** Acceptable launch experience

**Without Phase 1 fixes:**
- 🔴 System crashes after 50-100 concurrent users
- 🔴 API rate limits hit in first hour
- 🔴 Database locks cause timeouts
- 🔴 Users cannot login/signup
- **Verdict:** Launch failure

---

### Scenario 2: Viral Tweet
**Situation:** Tweet goes viral, 5000 signups in 1 hour, 1000 concurrent users

**With Phase 1 + Phase 2:**
- 🟡 System stays online but slow
- 🟡 Response times: 5-10 seconds
- 🔴 Some features disabled (WebSocket, real-time updates)
- ✅ Core features work (signup, login, viewing games)
- **Verdict:** Degraded but functional

**Recommendation for viral scenario:**
- Have Phase 3 infrastructure ready to deploy
- Can upgrade VPS in 10 minutes if needed
- Contact Odds API for temporary rate limit increase

---

## Monitoring & Alerts

### Key Metrics to Watch

1. **Response Time**
   - Target: <1s
   - Alert: >3s for 5 minutes
   - Action: Add workers or upgrade VPS

2. **Error Rate**
   - Target: <1%
   - Alert: >5% for 5 minutes
   - Action: Check API limits, database locks

3. **API Usage**
   - Target: <80% of daily limit
   - Alert: >90% of daily limit
   - Action: Upgrade plan or reduce polling frequency

4. **Database Connection Pool**
   - Target: <50 active connections
   - Alert: >80 active connections
   - Action: Increase pool size or migrate to PostgreSQL

5. **CPU Usage**
   - Target: <70%
   - Alert: >85% for 10 minutes
   - Action: Add workers or upgrade VPS

---

## Emergency Procedures

### If System Goes Down During Campaign

**Immediate Actions (5 minutes):**
1. Restart backend: `systemctl restart sporttrader`
2. Clear rate limits: `rm /tmp/rate_limit_cache*`
3. Disable WebSockets: Comment out broadcaster in main.py
4. Increase cache TTL to 60s: Reduce API load

**If Still Down (30 minutes):**
1. Enable maintenance mode
2. Upgrade VPS to 4 cores + 16GB RAM (~$50/mo more)
3. Add 2 more Uvicorn workers
4. Re-enable services gradually

**Nuclear Option (If Everything Fails):**
1. Pause campaign (stop accepting new signups)
2. Migrate to PostgreSQL in 4 hours
3. Setup load balancer with 2 VPS instances
4. Resume campaign with 10x capacity

---

## Summary & Recommendation

### Current State
🔴 **NOT READY** for 1000 user influx

### With Phase 1 (30 min + $199/mo)
🟡 **READY** with acceptable degradation

### With Phase 1 + Phase 2 (1 day)
🟢 **READY** with good performance

### Minimum Viable Launch
**Must Do:**
- ✅ Add Uvicorn workers (FREE, 5 min)
- ✅ Upgrade Odds API ($199/mo, 10 min)
- ✅ Enable SQLite WAL mode (FREE, 5 min)

**Total Time:** 20 minutes
**Total Cost:** $199/mo
**Result:** System will handle 1000 users with 10-20% degradation during peak

---

## Timeline Recommendation

### T-minus 24 hours (Before Campaign Launch)
- [ ] Implement Phase 1 critical fixes
- [ ] Test with load testing tool (100 concurrent users)
- [ ] Setup monitoring dashboard
- [ ] Prepare emergency contact list (VPS support, Odds API support)

### T-minus 1 hour
- [ ] Verify all services running
- [ ] Check API limits (start fresh)
- [ ] Clear all caches
- [ ] Increase cache TTL to maximum

### Launch Day
- [ ] Monitor dashboard every 30 minutes
- [ ] Watch for error spikes
- [ ] Be ready to disable non-critical features

### Week 1
- [ ] Implement Phase 2 optimizations
- [ ] Analyze bottlenecks from real usage
- [ ] Plan Phase 3 if growth continues

---

**Bottom Line:** With Phase 1 fixes ($199/mo, 30 minutes), you'll survive the campaign with acceptable performance. Without fixes, expect system failure at 50-100 concurrent users.
