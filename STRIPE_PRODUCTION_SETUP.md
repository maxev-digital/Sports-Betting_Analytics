# Stripe Production Setup Guide

## Current Status

**Issue:** The backend `.env` file has a mismatch between test and live Stripe keys:
- `STRIPE_SECRET_KEY` = `sk_test_...` (TEST MODE)
- `STRIPE_PUBLISHABLE_KEY` = `pk_live_...` (LIVE MODE)

**Required Action:** Switch both keys to production mode and create new price IDs for the discounted beta launch tiers.

---

## Beta Launch Pricing Structure

All prices are **50% OFF FOR LIFE** during beta launch.

### Discounted Monthly Prices
| Plan | Original Price | Discounted Price (50% OFF) |
|------|----------------|---------------------------|
| Starter | $29/mo | **$15/mo** |
| Semi Pro | $79/mo | **$40/mo** |
| Professional | $149/mo | **$75/mo** |
| Elite | $299/mo | **$150/mo** |
| Elite Pro | $799/mo | **$400/mo** |

### Discounted Annual Prices
| Plan | Original Price | Discounted Price (50% OFF) |
|------|----------------|---------------------------|
| Starter | $278/yr | **$139/yr** |
| Semi Pro | $758/yr | **$379/yr** |
| Professional | $1,430/yr | **$715/yr** |
| Elite | $2,870/yr | **$1,435/yr** |
| Elite Pro | $7,670/yr | **$3,835/yr** |

---

## Step-by-Step Setup Instructions

### 1. Get Production Stripe Keys

1. Log in to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Toggle from "Test mode" to "View live data" (switch in top right)
3. Navigate to **Developers** → **API keys**
4. Copy your **Secret key** (starts with `sk_live_...`)
5. Copy your **Publishable key** (starts with `pk_live_...`)

### 2. Create Discounted Price IDs in Stripe

For each plan, you need to create TWO products in Stripe (monthly and annual):

#### Example: Starter Plan

**Monthly Subscription:**
1. Go to **Products** → **Add product**
2. Name: `Max EV Starter - Monthly (Beta 50% OFF)`
3. Description: `Beta launch special: 50% off for life`
4. Price: `$15.00 USD`
5. Billing period: `Monthly`
6. Click **Save product**
7. Copy the Price ID (format: `price_xxxxxxxxxxxxx`)

**Annual Subscription:**
1. Click **Add another price** on the same product
2. Price: `$139.00 USD`
3. Billing period: `Yearly`
4. Click **Save**
5. Copy the Price ID

Repeat this process for all 5 plans.

### 3. Configure Webhook for Production

1. Navigate to **Developers** → **Webhooks**
2. Click **Add endpoint**
3. Endpoint URL: `https://your-production-domain.com/api/webhooks/stripe`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
5. Click **Add endpoint**
6. Copy the **Signing secret** (starts with `whsec_...`)

### 4. Update Environment Variables

Edit `backend/.env` and update these values:

```env
# Replace these with your production values
STRIPE_SECRET_KEY=sk_live_XXXXXXXXXXXXXXXXXXXXX
STRIPE_PUBLISHABLE_KEY=pk_live_XXXXXXXXXXXXXXXXXXXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXXXXXXXXXXXXXXXXXXX

# Add new discounted price IDs
STRIPE_STARTER_MONTHLY_PRICE_ID=price_XXXXXXXXXXXXX
STRIPE_STARTER_ANNUAL_PRICE_ID=price_XXXXXXXXXXXXX

STRIPE_SEMIPRO_MONTHLY_PRICE_ID=price_XXXXXXXXXXXXX
STRIPE_SEMIPRO_ANNUAL_PRICE_ID=price_XXXXXXXXXXXXX

STRIPE_PROFESSIONAL_MONTHLY_PRICE_ID=price_XXXXXXXXXXXXX
STRIPE_PROFESSIONAL_ANNUAL_PRICE_ID=price_XXXXXXXXXXXXX

STRIPE_ELITE_MONTHLY_PRICE_ID=price_XXXXXXXXXXXXX
STRIPE_ELITE_ANNUAL_PRICE_ID=price_XXXXXXXXXXXXX

STRIPE_ELITEPRO_MONTHLY_PRICE_ID=price_XXXXXXXXXXXXX
STRIPE_ELITEPRO_ANNUAL_PRICE_ID=price_XXXXXXXXXXXXX
```

### 5. Update Frontend Configuration

Edit `frontend/src/pages/Pricing.tsx` to use the correct price IDs based on `billingCycle`:

```typescript
// Map plan tier to Stripe price IDs
const getPriceId = (planTier: string, billingCycle: 'monthly' | 'annual') => {
  const priceMap = {
    'starter': {
      monthly: import.meta.env.VITE_STRIPE_STARTER_MONTHLY_PRICE_ID,
      annual: import.meta.env.VITE_STRIPE_STARTER_ANNUAL_PRICE_ID,
    },
    'semi-pro': {
      monthly: import.meta.env.VITE_STRIPE_SEMIPRO_MONTHLY_PRICE_ID,
      annual: import.meta.env.VITE_STRIPE_SEMIPRO_ANNUAL_PRICE_ID,
    },
    // ... add remaining plans
  };

  return priceMap[planTier]?.[billingCycle];
};
```

### 6. Test the Checkout Flow

Before going live:

1. Create a test subscription using a [Stripe test card](https://stripe.com/docs/testing#cards):
   - Card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits

2. Verify in Stripe Dashboard:
   - Subscription was created
   - Webhook events fired correctly
   - Customer record exists

3. Test subscription lifecycle:
   - Successful payment
   - Failed payment handling
   - Cancellation flow

---

## Security Checklist

- [ ] Ensure `.env` file is in `.gitignore` (already configured)
- [ ] Never commit Stripe secret keys to Git
- [ ] Use environment variables for all sensitive data
- [ ] Test webhook signature verification
- [ ] Set up Stripe webhook monitoring/alerts
- [ ] Document key rotation procedure

---

## Rollback Plan

If issues occur after going live:

1. **Immediate:** Toggle Stripe Dashboard back to test mode
2. **Backend:** Revert `.env` to test keys
3. **Frontend:** Update price IDs back to test values
4. **Communicate:** Notify any users who attempted signup

---

## Next Steps After Setup

1. Monitor first 10 signups closely
2. Verify email confirmations are sent
3. Check that trial periods are applied correctly (7 days)
4. Ensure webhook events are processing
5. Test subscription cancellation flow
6. Verify refund process works

---

## Support Resources

- [Stripe Testing Docs](https://stripe.com/docs/testing)
- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Stripe Subscriptions API](https://stripe.com/docs/billing/subscriptions/overview)
- [Stripe Error Codes](https://stripe.com/docs/error-codes)

---

**Note:** This is a one-way migration. Once you switch to production keys and start processing real payments, you cannot roll back without affecting real customer data. Test thoroughly before flipping the switch.
