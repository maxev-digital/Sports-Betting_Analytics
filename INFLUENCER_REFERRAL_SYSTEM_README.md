# Influencer Referral System - Complete Documentation

## System Overview

A complete influencer affiliate system that allows social media influencers to earn 20% recurring commission on all users they refer to MAX EV Sports. Users get 50% off for the first 2 months when signing up with an influencer code.

## Architecture

### Database (JSON Files)

1. **influencers.json** - Influencer profiles and referral codes
2. **referrals.json** - Tracks which users were referred by which influencer
3. **influencer_earnings.json** - Earnings tracking and payment history

### Backend Components

1. **influencer_system.py** - Core referral system logic
2. **routes/influencer.py** - API endpoints
3. **stripe_service.py** - Automatic coupon creation and discount application
4. **main.py** - Integration with signup process

---

## API Endpoints

### Public Endpoints (No Auth Required)

#### 1. Register New Influencer
```
POST /api/influencer/register
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "social_media_handle": "@johndoe",
  "platform": "Twitter",
  "follower_count": 50000,
  "custom_code": "JOHNDOE",  // optional
  "payment_email": "payment@example.com"  // optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Influencer registered successfully",
  "data": {
    "username": "johndoe",
    "referral_code": "JOHNDOE",
    "email": "john@example.com",
    "full_name": "John Doe",
    "created_at": "2025-11-11T12:00:00"
  }
}
```

#### 2. Influencer Login
```
POST /api/influencer/login
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "abc123...",
  "influencer": {
    "username": "johndoe",
    "referral_code": "JOHNDOE",
    "full_name": "John Doe",
    "total_referrals": 15,
    "total_earnings": 299.80
  }
}
```

#### 3. Validate Referral Code
```
POST /api/influencer/validate-code
```

**Request Body:**
```json
{
  "code": "JOHNDOE"
}
```

**Response:**
```json
{
  "valid": true,
  "influencer_name": "John Doe",
  "discount_percentage": 50,
  "discount_duration_months": 2,
  "message": "Valid! You'll get 50% off for the first 2 months (referred by John Doe)"
}
```

### Protected Endpoints (Influencer Auth Required)

**Authorization Header:**
```
Authorization: Bearer {token_from_login}
```

#### 4. Get Dashboard Data
```
GET /api/influencer/dashboard
```

**Response:**
```json
{
  "success": true,
  "influencer": {
    "username": "johndoe",
    "referral_code": "JOHNDOE",
    "full_name": "John Doe",
    "total_referrals": 15
  },
  "referrals": [
    {
      "referred_username": "user123",
      "subscription_tier": "professional",
      "signup_date": "2025-11-01T10:00:00",
      "status": "active",
      "monthly_commission": 19.99
    }
  ],
  "earnings": {
    "total_monthly_commission": 299.80,
    "active_referrals": 15,
    "total_referrals": 18,
    "annual_projection": 3597.60,
    "breakdown_by_tier": {
      "professional": {
        "count": 10,
        "commission": 199.90
      },
      "elite": {
        "count": 5,
        "commission": 99.95
      }
    }
  }
}
```

#### 5. Get Referrals List
```
GET /api/influencer/referrals
```

#### 6. Get Earnings Breakdown
```
GET /api/influencer/earnings
```

#### 7. Get Profile
```
GET /api/influencer/profile
```

#### 8. Logout
```
POST /api/influencer/logout
```

### Admin Endpoints (Admin Auth Required)

#### 9. Get All Influencers
```
GET /api/influencer/admin/all
```

**Response:**
```json
{
  "success": true,
  "influencers": [
    {
      "username": "johndoe",
      "referral_code": "JOHNDOE",
      "full_name": "John Doe",
      "platform": "Twitter",
      "follower_count": 50000,
      "status": "active",
      "total_referrals": 15,
      "earnings": {
        "total_monthly_commission": 299.80,
        "active_referrals": 15
      }
    }
  ],
  "total": 1
}
```

#### 10. Update Influencer Status
```
PUT /api/influencer/admin/status
```

**Request Body:**
```json
{
  "username": "johndoe",
  "status": "suspended"  // active, paused, suspended
}
```

#### 11. Get User Referral Info
```
GET /api/influencer/admin/referral/{username}
```

---

## User Signup with Referral Code

### Updated Signup Endpoint

```
POST /api/auth/register
```

**Request Body (NEW - includes referral_code):**
```json
{
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "username": "janesmith",
  "password": "SecurePass123",
  "referral_code": "JOHNDOE"  // OPTIONAL
}
```

**What Happens:**
1. System validates referral code
2. If valid, tracks the referral
3. When user upgrades to paid tier, applies 50% discount for 2 months
4. Influencer earns 20% commission on user's subscription

---

## Stripe Integration

### Automatic Discount Application

When a user with a valid referral code proceeds to checkout:

```python
from stripe_service import StripeService

# Create checkout session with referral discount
session = StripeService.create_checkout_session(
    price_id="price_xxx",
    user_id="janesmith",
    user_email="jane@example.com",
    referral_code="JOHNDOE"  # Automatically creates and applies 50% coupon for 2 months
)
```

### Coupon Creation

Coupons are automatically created in Stripe with format: `REFERRAL_{CODE}`

- **Discount:** 50% OFF
- **Duration:** 2 months (repeating)
- **Applied:** Automatically at checkout

---

## Commission Calculation

### Tier Pricing & Commissions

| Tier | Monthly Price | 20% Commission |
|------|--------------|----------------|
| Beta | $9.99 | $2.00 |
| Starter | $29.99 | $6.00 |
| Semi-Pro | $49.99 | $10.00 |
| Professional | $99.99 | $20.00 |
| Elite | $199.99 | $40.00 |
| Elite Pro | $299.99 | $60.00 |

### Commission Rules

1. **Recurring:** Commission continues as long as user maintains subscription
2. **First 2 Months:** User pays 50% (influencer still earns 20% of full price)
3. **After 2 Months:** User pays full price, influencer earns 20%
4. **Cancellation:** Commission stops when user cancels
5. **Upgrade/Downgrade:** Commission adjusts to new tier automatically

### Example Earnings

**Scenario:** Influencer refers 10 users
- 5 on Professional ($99.99/mo) = 5 × $20 = $100/mo
- 3 on Elite ($199.99/mo) = 3 × $40 = $120/mo
- 2 on Semi-Pro ($49.99/mo) = 2 × $10 = $20/mo

**Total Monthly Recurring:** $240/mo
**Annual Projection:** $2,880/year

---

## Frontend Components Needed

### 1. Influencer Registration Page

**Route:** `/influencer-register`

**Form Fields:**
- Full Name
- Email
- Username
- Password
- Social Media Handle (@username)
- Platform (dropdown: Twitter, Instagram, YouTube, TikTok, etc.)
- Follower Count (number)
- Custom Referral Code (optional, shows availability check)
- Payment Email (optional)

**Features:**
- Real-time code availability check
- Auto-generate code from name if custom not provided
- Terms & conditions checkbox

### 2. Influencer Dashboard Page

**Route:** `/influencer-dashboard`

**Sections:**

**A. Stats Overview (Top Cards)**
- Total Referrals
- Active Referrals
- Monthly Earnings
- Annual Projection

**B. Referral Code Display**
- Large display of their code
- Copy to clipboard button
- Share buttons (Twitter, Facebook, Email)
- Custom landing page link

**C. Referrals Table**
- Username
- Signup Date
- Subscription Tier
- Status (Active/Cancelled)
- Monthly Commission
- Actions (view details)

**D. Earnings Breakdown**
- Pie chart by tier
- Monthly trend graph
- Payment history table

**E. Marketing Materials**
- Pre-written social posts
- Banner images
- Email templates

### 3. Updated Signup Page

**Modifications to Existing `/signup` Page:**

**Add Referral Code Field:**
```tsx
<input
  type="text"
  placeholder="Referral Code (Optional)"
  value={referralCode}
  onChange={(e) => handleReferralCodeChange(e.target.value)}
/>
{referralValidation && (
  <div className={referralValidation.valid ? "text-green-500" : "text-red-500"}>
    {referralValidation.message}
  </div>
)}
```

**Validation Function:**
```tsx
const handleReferralCodeChange = async (code: string) => {
  setReferralCode(code);
  if (code.length < 3) return;

  try {
    const response = await fetch('/api/influencer/validate-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    const result = await response.json();
    setReferralValidation(result);
  } catch (error) {
    setReferralValidation({ valid: false, message: 'Error validating code' });
  }
};
```

### 4. Admin Influencer Management Page

**Route:** `/admin/influencers` (admin only)

**Features:**
- List all influencers
- View earnings per influencer
- Update status (active/paused/suspended)
- View referral details
- Export data to CSV

---

## Testing the System

### 1. Register Test Influencer

```bash
curl -X POST http://localhost:8000/api/influencer/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testinfluencer",
    "email": "test@influencer.com",
    "password": "test123",
    "full_name": "Test Influencer",
    "social_media_handle": "@testinfluencer",
    "platform": "Twitter",
    "follower_count": 10000,
    "custom_code": "TEST50"
  }'
```

### 2. Validate Referral Code

```bash
curl -X POST http://localhost:8000/api/influencer/validate-code \
  -H "Content-Type": application/json" \
  -d '{"code": "TEST50"}'
```

### 3. Sign Up New User with Code

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "test123",
    "referral_code": "TEST50"
  }'
```

### 4. Login as Influencer

```bash
curl -X POST http://localhost:8000/api/influencer/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testinfluencer",
    "password": "test123"
  }'
```

### 5. View Dashboard

```bash
curl -X GET http://localhost:8000/api/influencer/dashboard \
  -H "Authorization: Bearer {token_from_login}"
```

---

## Deployment Checklist

### 1. Backend Files to Deploy

```bash
# Core system files
backend/influencer_system.py
backend/routes/influencer.py
backend/stripe_service.py (updated)
backend/main.py (updated)

# Deploy to production
scp -i ~/.ssh/hostinger_vps backend/influencer_system.py root@148.230.87.135:/root/sporttrader/backend/
scp -i ~/.ssh/hostinger_vps backend/routes/influencer.py root@148.230.87.135:/root/sporttrader/backend/routes/
scp -i ~/.ssh/hostinger_vps backend/stripe_service.py root@148.230.87.135:/root/sporttrader/backend/
scp -i ~/.ssh/hostinger_vps backend/main.py root@148.230.87.135:/root/sporttrader/backend/

# Restart backend
ssh -i ~/.ssh/hostinger_vps root@148.230.87.135 "systemctl restart sporttrader"
```

### 2. Frontend Components to Create

- InfluencerRegister.tsx
- InfluencerDashboard.tsx
- InfluencerLogin.tsx
- Update SignUp.tsx (add referral code field)
- AdminInfluencers.tsx

### 3. Environment Variables

Add to `.env`:
```
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 4. Stripe Setup

1. Create coupons will be automatic
2. Set up webhook for subscription events
3. Test in Stripe test mode first

---

## Webhook Integration

When Stripe sends subscription events, update referral commissions:

```python
# In webhook handler (already exists in main.py)
from influencer_system import update_referral_status

# On subscription.updated
if event_type == 'customer.subscription.updated':
    username = get_username_from_customer(customer_id)
    new_tier = get_tier_from_price(price_id)
    update_referral_status(username, 'active', new_tier)

# On subscription.deleted
if event_type == 'customer.subscription.deleted':
    username = get_username_from_customer(customer_id)
    update_referral_status(username, 'cancelled')
```

---

## Security Considerations

1. **Password Hashing:** Influencer passwords hashed with SHA256
2. **Session Tokens:** Secure 32-byte tokens for authentication
3. **Rate Limiting:** Consider adding to registration endpoint
4. **Input Validation:** All inputs validated and sanitized
5. **SQL Injection:** Not applicable (using JSON storage)
6. **CORS:** Already configured in main.py

---

## Future Enhancements

1. **Payment Automation:** Integrate Stripe Connect for automatic payouts
2. **Analytics:** Track click-through rates, conversion rates
3. **Tier System:** Different commission rates for top performers
4. **Bonus System:** Bonuses for hitting referral milestones
5. **Custom Landing Pages:** Generate custom pages for each influencer
6. **Email Campaigns:** Auto-email influencers with performance reports
7. **Tax Forms:** Collect W-9/W-8 forms for tax compliance

---

## Support & Troubleshooting

### Common Issues

**Issue:** Referral code not validating
- Check influencer status is "active"
- Verify code exact match (case-insensitive)
- Check server logs for errors

**Issue:** Discount not applied in Stripe
- Verify coupon created in Stripe dashboard
- Check referral_code passed to create_checkout_session
- Ensure user has valid referral_code in users.json

**Issue:** Commission not tracking
- Verify referral exists in referrals.json
- Check subscription tier in SubscriptionDB
- Ensure webhook events processed correctly

---

## Contact

For questions or issues with the influencer system:
- Check logs: `journalctl -u sporttrader -f`
- Review data files: `influencers.json`, `referrals.json`
- Test endpoints with curl commands above
