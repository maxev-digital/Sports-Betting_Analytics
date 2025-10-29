# Stripe Promo Code Setup Guide

## Overview

Instead of creating duplicate discounted products, we're using Stripe's built-in **Promotion Codes** feature to apply the 50% OFF FOR LIFE beta discount. This is cleaner, more flexible, and easier to manage.

---

## Benefits of Using Promo Codes

✅ **No Duplicate Products** - Keep your existing price IDs
✅ **Easy to Enable/Disable** - Turn off promo when beta ends
✅ **Track Usage** - See how many beta members signed up
✅ **Works with All Billing Cycles** - Automatically applies to monthly and annual
✅ **Forever Discount** - Can be set to apply to all future renewals

---

## Step-by-Step Setup

### 1. Log into Stripe Dashboard

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Toggle to **"View live data"** (production mode) in the top right

### 2. Create a Coupon (50% OFF Forever)

1. Navigate to **Products** → **Coupons**
2. Click **"Create coupon"**
3. Fill in the details:

   **Coupon Settings:**
   - **Name**: `Beta Launch - 50% OFF FOR LIFE`
   - **ID**: `beta-50-off-lifetime` (optional custom ID)
   - **Type**: `Percentage`
   - **Percentage off**: `50%`
   - **Duration**: `Forever` ⭐ (this makes it apply to all renewals)
   - **Redemption limit**: Leave unchecked (or set to 100 if you want to limit)

4. Click **"Create coupon"**

### 3. Create a Promotion Code

1. After creating the coupon, click **"Add promotion code"**
2. Fill in the details:

   **Promotion Code Settings:**
   - **Code**: `BETA50` (or your preferred code - this is what users see)
   - **Coupon**: Select the coupon you just created
   - **Active**: ✅ Enabled
   - **First time orders**: Leave unchecked (applies to all)
   - **Minimum amount**: Leave empty
   - **Expiration date**: Optional - set when you want beta to end
   - **Max redemptions**: Optional - set to 100 for first 100 users

3. Click **"Create promotion code"**
4. **Copy the Promotion Code ID** (format: `promo_xxxxxxxxxxxxx`)

### 4. Update Environment Variables

Edit `backend/.env` and add:

```env
# Stripe Promo Code for Beta Launch (50% OFF FOR LIFE)
STRIPE_BETA_PROMO_CODE=promo_xxxxxxxxxxxxx  # Paste the ID from step 3

# Also update to production keys if not already done:
STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxxx  # Production secret key
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxxxxxxxxxx  # Production publishable key
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx  # Production webhook secret
```

### 5. Restart Backend Server

The promo code will be loaded from the environment and automatically applied to all checkout sessions where `apply_beta_discount=true`.

---

## How It Works

### Frontend (Pricing.tsx)
```typescript
body: JSON.stringify({
  price_id: STRIPE_PRICE_IDS[tier],
  user_id: username,
  user_email: `${username.replace(/\s+/g, '.')}@max-ev-sports.com`,
  apply_beta_discount: true  // ← Automatically applies promo code
})
```

### Backend (stripe_service.py)
```python
if apply_beta_discount and STRIPE_BETA_PROMO_CODE:
    session_params['discounts'] = [{
        'promotion_code': STRIPE_BETA_PROMO_CODE
    }]
```

### Stripe Checkout
When users reach the Stripe checkout page, they will see:
- Original price (e.g., $29/month)
- **"Beta Launch - 50% OFF FOR LIFE"** discount applied
- Final price: $15/month
- Message: "This discount will apply to all future invoices"

---

## Testing the Promo Code

### Test Mode First

Before going live, test in Stripe test mode:

1. Create a test coupon and promotion code
2. Update `.env` with test promo code ID
3. Use Stripe test card: `4242 4242 4242 4242`
4. Verify:
   - ✅ Discount shows on checkout page
   - ✅ Final amount is 50% less
   - ✅ Subscription created with coupon applied
   - ✅ Invoice shows discounted amount

### Production Testing

1. Use a real card with small amount
2. Immediately cancel the subscription
3. Issue refund in Stripe Dashboard

---

## Managing the Beta Promotion

### View Usage Statistics

**Stripe Dashboard** → **Products** → **Coupons** → Click your coupon

You'll see:
- Total times redeemed
- Total amount discounted
- List of customers using it

### Disable After Beta Ends

Two options:

**Option 1: Deactivate Promotion Code**
- Go to the promotion code in Stripe
- Click **"Deactivate"**
- Existing users keep their discount, new signups pay full price

**Option 2: Remove from Code**
- Set `STRIPE_BETA_PROMO_CODE=""` in `.env`
- Restart backend server
- Checkout sessions will no longer auto-apply the promo

**Option 3: Set Expiration Date**
- Edit promotion code in Stripe
- Set "Expiration date" to when beta ends
- Stripe automatically stops accepting it after that date

---

## Important Notes

### Duration: "Forever" vs "Once" vs "Repeating"

- **Forever**: Discount applies to ALL future renewals (recommended for "50% OFF FOR LIFE")
- **Once**: Discount only on first payment (not suitable for our promotion)
- **Repeating**: Discount for X months then reverts to full price

### Promo Code vs Coupon

- **Coupon**: The actual discount (50% off)
- **Promotion Code**: The user-facing code (BETA50) that references the coupon
- You need BOTH - the coupon defines the discount, the promo code is how it's applied

### Users Can Still See the Promo Code Field

Even with auto-applied promo codes, Stripe shows a "Add promotion code" link on checkout. This is normal Stripe behavior. The code is pre-applied, but users could technically remove it or enter a different one if they have one.

---

## Troubleshooting

### "Invalid promotion code" Error

**Cause**: The `STRIPE_BETA_PROMO_CODE` in `.env` doesn't match Stripe's records

**Fix**:
1. Verify the promo code ID in Stripe Dashboard
2. Ensure you're using the promo code ID (starts with `promo_`), not the coupon ID
3. Check you're in the correct mode (test vs live)

### Discount Not Showing on Checkout

**Cause**: Promo code not being applied to session

**Fix**:
1. Check backend logs for "Applying beta promo code: ..."
2. Verify `apply_beta_discount: true` is in the frontend request
3. Ensure `STRIPE_BETA_PROMO_CODE` is set in `.env`

### "Coupon expired" Error

**Cause**: Promotion code has passed its expiration date

**Fix**:
1. Update expiration date in Stripe Dashboard
2. Or create a new promotion code

---

## Security Considerations

- ✅ Promo code ID stored in `.env` (not committed to Git)
- ✅ Applied server-side, not client-side (prevents tampering)
- ✅ Can set redemption limits to prevent abuse
- ✅ Can be deactivated instantly if issues arise

---

## Example: Full Setup

```env
# backend/.env

# Production Stripe Keys
STRIPE_SECRET_KEY=sk_live_51ABC123...
STRIPE_PUBLISHABLE_KEY=pk_live_51ABC123...
STRIPE_WEBHOOK_SECRET=whsec_abc123...

# Existing Price IDs (unchanged)
STRIPE_STARTER_PRICE_ID=price_1SL6DfR4L082TOJBCtBGFXgA
STRIPE_SEMIPRO_PRICE_ID=price_1SL6D2R4L082TOJBUP6iO2g7
STRIPE_PROFESSIONAL_PRICE_ID=price_1SL6E4R4L082TOJBLphpsfhx
STRIPE_ELITE_PRICE_ID=price_1SL6ERR4L082TOJBz91Q9hBM
STRIPE_ELITEPRO_PRICE_ID=price_1SL6EtR4L082TOJB2Pzx9Mgq

# Beta Promo Code (50% OFF FOR LIFE)
STRIPE_BETA_PROMO_CODE=promo_1ABC123XYZ456
```

---

## Next Steps

1. ✅ Create coupon in Stripe (50% off, forever duration)
2. ✅ Create promotion code linked to coupon
3. ✅ Copy promotion code ID
4. ✅ Update `backend/.env` with `STRIPE_BETA_PROMO_CODE`
5. ✅ Restart backend server
6. ✅ Test checkout flow
7. ✅ Go live!

---

**Resources:**
- [Stripe Coupons Documentation](https://stripe.com/docs/billing/subscriptions/coupons)
- [Stripe Promotion Codes Guide](https://stripe.com/docs/billing/subscriptions/discounts/codes)
- [Stripe Testing Coupons](https://stripe.com/docs/testing#coupons)
