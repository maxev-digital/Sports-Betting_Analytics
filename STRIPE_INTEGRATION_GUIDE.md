# Stripe Subscription Paywall Integration Guide

## Overview

This guide covers the complete implementation of a Stripe-based subscription paywall for Max EV Sports platform.

## Architecture

### Subscription Tiers

**Free Tier** (Free)
- View live games (limited sports)
- Basic odds comparison
- No alerts access
- Limited to 10 games per day

**Pro Tier** ($49.99/month)
- All sports access
- Live alerts (arbitrage, steam moves, line movements)
- Unlimited game views
- Email notifications
- Priority support

**Elite Tier** ($99.99/month)
- Everything in Pro
- NHL Goalie pull alerts
- API access
- SMS notifications
- Custom alert thresholds
- Advanced analytics

## Implementation Steps

### 1. Stripe Account Setup

1. **Get Stripe API Keys:**
   - Go to https://dashboard.stripe.com/apikeys
   - Copy your Publishable Key (starts with `pk_`)
   - Copy your Secret Key (starts with `sk_`)
   - Copy your Webhook Secret (after creating webhook)

2. **Create Products & Prices:**
   - Go to Products page in Stripe Dashboard
   - Create "Pro Monthly" product with $49.99/month price
   - Create "Elite Monthly" product with $99.99/month price
   - Note the Price IDs (starts with `price_`)

3. **Set Up Webhook:**
   - Go to Developers > Webhooks
   - Add endpoint: `https://yourdomain.com/api/stripe/webhook`
   - Select events:
     - `customer.subscription.created`
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
     - `invoice.payment_succeeded`
     - `invoice.payment_failed`

### 2. Environment Variables

Add to `backend/.env`:
```bash
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Price IDs
STRIPE_PRO_PRICE_ID=price_your_pro_price_id
STRIPE_ELITE_PRICE_ID=price_your_elite_price_id

# Your domain for Stripe redirects
DOMAIN=http://localhost:5173
```

Add to `frontend/.env`:
```bash
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
```

### 3. Backend Dependencies

Install required packages:
```bash
cd backend
pip install stripe==7.0.0
pip install python-dotenv
```

### 4. Database Schema Updates

New tables needed:
- `subscriptions`: Track user subscription status
- `subscription_history`: Audit trail of subscription changes

### 5. API Endpoints

**Create Checkout Session:**
```
POST /api/stripe/create-checkout-session
Body: { price_id: string, user_id: string }
Returns: { session_id: string, url: string }
```

**Create Portal Session:**
```
POST /api/stripe/create-portal-session
Body: { user_id: string }
Returns: { url: string }
```

**Webhook Handler:**
```
POST /api/stripe/webhook
Headers: { Stripe-Signature: string }
Body: Stripe Event Object
Returns: { received: true }
```

**Get Subscription Status:**
```
GET /api/subscription/status
Query: user_id
Returns: { tier: string, status: string, current_period_end: string }
```

### 6. Frontend Components

**New Pages/Components:**
- `/pricing` - Pricing page with tier cards
- `/subscription` - Manage subscription page
- `<SubscriptionGate>` - Component to protect features
- `<PricingCard>` - Individual pricing tier card

### 7. Middleware

**Subscription Check Middleware:**
- Verify user has active subscription
- Check tier level for feature access
- Return 402 Payment Required if needed

### 8. Testing

**Test Cards:**
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- 3D Secure: `4000 0025 0000 3155`

**Use any future expiration date and any CVC**

### 9. Webhook Testing

Use Stripe CLI for local testing:
```bash
stripe listen --forward-to localhost:8000/api/stripe/webhook
stripe trigger customer.subscription.created
```

### 10. Production Checklist

- [ ] Replace test keys with live keys
- [ ] Update webhook endpoint to production URL
- [ ] Test complete payment flow
- [ ] Test subscription cancellation
- [ ] Test upgrade/downgrade flow
- [ ] Set up monitoring for failed payments
- [ ] Configure email notifications
- [ ] Add error handling and logging
- [ ] Implement retry logic for webhooks
- [ ] Add rate limiting to endpoints

## Security Considerations

1. **Never expose secret keys** in frontend code
2. **Verify webhook signatures** to prevent fake events
3. **Use HTTPS only** in production
4. **Implement CSRF protection** on payment endpoints
5. **Sanitize user input** before creating customers
6. **Log all subscription events** for audit trail
7. **Rate limit** subscription creation endpoints
8. **Verify subscription status** on every protected API call

## User Flow

### New Subscription Flow
1. User clicks "Upgrade to Pro" button
2. Frontend calls `/api/stripe/create-checkout-session`
3. Backend creates Stripe Checkout Session
4. User redirected to Stripe hosted checkout page
5. User enters payment details and confirms
6. Stripe processes payment
7. Webhook receives `customer.subscription.created` event
8. Backend updates database with subscription info
9. User redirected back to success page
10. User now has access to Pro features

### Manage Subscription Flow
1. User clicks "Manage Subscription" in settings
2. Frontend calls `/api/stripe/create-portal-session`
3. Backend creates Customer Portal Session
4. User redirected to Stripe hosted portal
5. User can update payment, cancel, or view invoices
6. Changes trigger webhook events
7. Backend updates database accordingly
8. User redirected back to platform

## Feature Gates

### Implementation Example

```typescript
// Frontend - Check before showing feature
const { subscription } = useAuth();

if (subscription.tier === 'free') {
  return <UpgradePrompt feature="Arbitrage Alerts" />;
}

// Backend - Check on API endpoint
@app.get("/api/alerts/arbitrage")
async def get_arbitrage_alerts(user_id: str):
    subscription = await get_subscription(user_id)
    
    if subscription.tier == "free":
        raise HTTPException(402, "Pro subscription required")
    
    return await fetch_arbitrage_alerts()
```

## Pricing Strategy

### Monthly Pricing
- **Free:** $0/month (limited features)
- **Pro:** $49.99/month
- **Elite:** $99.99/month

### Annual Pricing (20% discount)
- **Pro Annual:** $479.99/year (Save $119.89)
- **Elite Annual:** $959.99/year (Save $239.89)

### Trial Period
- 7-day free trial for Pro tier
- No credit card required for Free tier
- Trial converts to paid after 7 days

## Support

### Common Issues

**Payment Failed:**
- Check if card has sufficient funds
- Verify billing address is correct
- Try different payment method
- Contact bank if declined

**Subscription Not Updating:**
- Check webhook delivery in Stripe Dashboard
- Verify webhook signature validation
- Check backend logs for errors
- Retry webhook delivery manually

**Downgrade Not Working:**
- Ensure change is scheduled for period end
- Check proration settings in Stripe
- Verify webhook events are processed

## Monitoring

**Metrics to Track:**
- Conversion rate (Free → Pro)
- Churn rate
- Failed payment rate
- Customer lifetime value
- MRR (Monthly Recurring Revenue)
- Trial conversion rate

**Set up alerts for:**
- Failed webhook deliveries
- High payment failure rates
- Unusual cancellation spikes
- Subscription creation errors

## Resources

- Stripe Documentation: https://stripe.com/docs
- Stripe API Reference: https://stripe.com/docs/api
- Stripe Testing: https://stripe.com/docs/testing
- Webhook Best Practices: https://stripe.com/docs/webhooks/best-practices

---

**Last Updated:** January 22, 2025
**Status:** Implementation Guide
