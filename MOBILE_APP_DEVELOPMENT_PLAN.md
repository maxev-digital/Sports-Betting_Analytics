# Mobile App Development Plan - MAX-EV Sports
**Created:** November 12, 2025
**Target:** iOS App Store & Google Play Store

---

## 📊 Current State Analysis

### Existing Codebase
- **Frontend:** React 18 + TypeScript + Vite
- **Components:** 126 files (3.5MB)
- **Pages:** 37 full pages
- **Routing:** React Router with HashRouter
- **Styling:** TailwindCSS
- **Charts:** Recharts
- **Icons:** Lucide React
- **Backend API:** FastAPI at https://max-ev-sports.com/api

### Desktop Setup (Already Exists!)
- ✅ Electron configured (`electron-builder`)
- ✅ Desktop app builds (Windows, Mac, Linux)
- ✅ Desktop-specific features: Window controls, multi-window support

### Key Features to Port
1. **Live Games** - Real-time odds updates (15s polling)
2. **Alerts** - Arbitrage, steam moves, middles detection
3. **Analytics** - Performance tracking, charts
4. **Strategy Results** - 25+ betting strategies with ROI
5. **Odds Comparison** - Multi-sportsbook odds
6. **Edge Lab** - Sharp vs public analysis
7. **Model Performance** - ML predictions tracking
8. **Props** - Player props analysis
9. **Partner Program** - Influencer dashboard
10. **Subscription Management** - Stripe integration

---

## 🎯 Recommended Approach: **Capacitor + React**

### Why Capacitor? (Not React Native)

**Pros:**
- ✅ **Reuse 95%+ of existing React code** - minimal changes needed
- ✅ **Same codebase** for web, iOS, Android, Electron
- ✅ **Faster development** - weeks instead of months
- ✅ **Native features** via plugins (push notifications, biometrics)
- ✅ **Web technologies** - you already know React/TypeScript
- ✅ **Easier maintenance** - one codebase for all platforms

**Cons:**
- ⚠️ Slightly less performant than native (not noticeable for your use case)
- ⚠️ Larger app size than pure native

**React Native Alternative (Not Recommended):**
- ❌ Requires complete rewrite (37 pages × ~2-3 weeks each)
- ❌ Different component library (React Native components, not HTML/CSS)
- ❌ Separate codebase from web app
- ❌ More bugs/fragmentation between iOS and Android
- ✅ Better performance (but you don't need it for data/charts)

**Verdict:** Capacitor lets you ship iOS + Android in 2-4 weeks instead of 6+ months.

---

## 📱 Capacitor Development Plan

### Phase 1: Setup & Configuration (Week 1)

#### 1.1 Install Capacitor
```bash
cd frontend
npm install @capacitor/core @capacitor/cli
npm install @capacitor/ios @capacitor/android
npx cap init "MAX EV SPORTS" "com.maxevsports.app"
```

#### 1.2 Add Platforms
```bash
npx cap add ios
npx cap add android
```

#### 1.3 Configure Capacitor
**File:** `frontend/capacitor.config.ts`
```typescript
import { CapacitorConfig } from '@capacitor/core';

const config: CapacitorConfig = {
  appId: 'com.maxevsports.app',
  appName: 'MAX EV SPORTS',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
    iosScheme: 'capacitor',
    hostname: 'app.maxevsports.com',
    // Production API
    url: 'https://max-ev-sports.com',
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: "#1a1a1a",
      showSpinner: false,
    },
    PushNotifications: {
      presentationOptions: ["badge", "sound", "alert"]
    },
  }
};

export default config;
```

#### 1.4 Update Vite Config for Mobile
**File:** `frontend/vite.config.ts`
```typescript
export default defineConfig({
  // ... existing config ...
  build: {
    outDir: 'dist',
    // Mobile-specific optimizations
    target: 'es2020',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs in production
      }
    },
  },
  // Mobile dev server
  server: {
    port: 5173,
    host: '0.0.0.0', // Allow mobile devices to connect
  }
});
```

#### 1.5 Mobile-Specific Packages
```bash
npm install @capacitor/status-bar @capacitor/splash-screen
npm install @capacitor/push-notifications @capacitor/haptics
npm install @capacitor/app @capacitor/browser
npm install @capacitor/share @capacitor/clipboard
npm install @capacitor/keyboard @capacitor/network
```

---

### Phase 2: Mobile Adaptations (Week 1-2)

#### 2.1 Responsive Design Audit
**Files to update:** All pages with desktop-focused layouts

**Create:** `frontend/src/hooks/useMobile.ts`
```typescript
import { useState, useEffect } from 'react';
import { Capacitor } from '@capacitor/core';

export function useMobile() {
  const [isMobile, setIsMobile] = useState(false);
  const [isNative, setIsNative] = useState(false);
  const [platform, setPlatform] = useState<'ios' | 'android' | 'web'>('web');

  useEffect(() => {
    setIsNative(Capacitor.isNativePlatform());
    setPlatform(Capacitor.getPlatform() as any);
    setIsMobile(window.innerWidth < 768 || Capacitor.isNativePlatform());
  }, []);

  return { isMobile, isNative, platform };
}
```

**Usage in components:**
```typescript
import { useMobile } from '../hooks/useMobile';

function GameCard() {
  const { isMobile, platform } = useMobile();

  return (
    <div className={isMobile ? "p-2" : "p-4"}>
      {/* Mobile-optimized layout */}
    </div>
  );
}
```

#### 2.2 Navigation Updates
**Issue:** Desktop has large sidebar, mobile needs bottom nav

**Create:** `frontend/src/components/MobileNavigation.tsx`
```typescript
import { Home, TrendingUp, Bell, Settings } from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useMobile } from '../hooks/useMobile';

export function MobileNavigation() {
  const { isMobile } = useMobile();
  const location = useLocation();
  const navigate = useNavigate();

  if (!isMobile) return null;

  const tabs = [
    { path: '/live-games', icon: Home, label: 'Games' },
    { path: '/analytics', icon: TrendingUp, label: 'Analytics' },
    { path: '/alerts', icon: Bell, label: 'Alerts' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-gray-900 border-t border-gray-800 pb-safe">
      <div className="flex justify-around items-center h-16">
        {tabs.map(tab => (
          <button
            key={tab.path}
            onClick={() => navigate(tab.path)}
            className={`flex flex-col items-center justify-center w-full h-full
              ${location.pathname === tab.path ? 'text-blue-500' : 'text-gray-400'}`}
          >
            <tab.icon size={24} />
            <span className="text-xs mt-1">{tab.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}
```

#### 2.3 Touch Optimizations
**Issues:**
- Small click targets (need 44px minimum)
- No hover states on mobile
- Swipe gestures needed

**Update:** `frontend/src/index.css`
```css
/* Mobile-specific styles */
@media (max-width: 768px) {
  /* Larger touch targets */
  button, a {
    min-height: 44px;
    min-width: 44px;
  }

  /* Remove hover effects */
  *:hover {
    /* Disable on touch devices */
  }

  /* Safe area insets for notch/island */
  .pb-safe {
    padding-bottom: env(safe-area-inset-bottom);
  }

  .pt-safe {
    padding-top: env(safe-area-inset-top);
  }
}
```

#### 2.4 Charts Optimization
**Issue:** Recharts can be slow on mobile

**Update:** `frontend/src/components/GameCard.tsx` and chart components
```typescript
import { useMobile } from '../hooks/useMobile';

function ChartComponent() {
  const { isMobile } = useMobile();

  return (
    <LineChart
      width={isMobile ? 300 : 600}
      height={isMobile ? 200 : 400}
      data={data}
      // Reduce animation on mobile
      isAnimationActive={!isMobile}
    >
      {/* Simplified chart for mobile */}
    </LineChart>
  );
}
```

#### 2.5 Remove Desktop-Only Features
**Files to update:**
- `ElectronWindowControls.tsx` - Hide on mobile
- Multi-window features - Disable on mobile
- Desktop keyboard shortcuts - Mobile doesn't need

```typescript
import { useMobile } from '../hooks/useMobile';

function ElectronWindowControls() {
  const { isNative, platform } = useMobile();

  // Only show on Electron desktop, hide on iOS/Android
  if (!isNative || platform !== 'web') return null;

  return (/* ... */);
}
```

---

### Phase 3: Mobile-Specific Features (Week 2)

#### 3.1 Push Notifications
**Install:** `@capacitor/push-notifications`

**Create:** `frontend/src/services/pushNotifications.ts`
```typescript
import { PushNotifications } from '@capacitor/push-notifications';

export async function registerPushNotifications() {
  // Request permission
  let permStatus = await PushNotifications.checkPermissions();

  if (permStatus.receive === 'prompt') {
    permStatus = await PushNotifications.requestPermissions();
  }

  if (permStatus.receive !== 'granted') {
    throw new Error('User denied permissions!');
  }

  await PushNotifications.register();
}

export async function setupPushListeners() {
  // On success, send token to backend
  PushNotifications.addListener('registration', (token) => {
    console.log('Push registration success, token: ' + token.value);
    // Send to backend: POST /api/devices/register
  });

  // Handle incoming notifications
  PushNotifications.addListener('pushNotificationReceived', (notification) => {
    console.log('Push received: ' + JSON.stringify(notification));
    // Show in-app alert
  });

  // Handle notification tap
  PushNotifications.addListener('pushNotificationActionPerformed', (action) => {
    console.log('Push action performed: ' + JSON.stringify(action));
    // Navigate to relevant page
  });
}
```

**Backend Integration:**
```python
# backend/routes/push_notifications.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/api/devices/register")
async def register_device(device_token: str, platform: str, user_id: str):
    """Store device token for push notifications"""
    # Save to database
    # Use Firebase Cloud Messaging (FCM) for Android
    # Use Apple Push Notification Service (APNs) for iOS
    pass
```

#### 3.2 Biometric Authentication
**Install:** `@capacitor-community/biometric-auth`

```bash
npm install @capacitor-community/biometric-auth
```

**Create:** `frontend/src/services/biometrics.ts`
```typescript
import { BiometricAuth } from '@capacitor-community/biometric-auth';

export async function enableBiometricLogin() {
  const result = await BiometricAuth.checkBiometry();

  if (result.isAvailable) {
    // Biometrics available (Face ID, Touch ID, Fingerprint)
    return true;
  }
  return false;
}

export async function authenticateWithBiometrics() {
  try {
    const result = await BiometricAuth.authenticate({
      reason: 'Login to MAX EV SPORTS',
      title: 'Biometric Authentication',
      negativeButtonText: 'Cancel',
    });

    if (result.success) {
      // Auto-login user
      return true;
    }
  } catch (error) {
    console.error('Biometric auth failed:', error);
  }
  return false;
}
```

#### 3.3 Haptic Feedback
**Install:** `@capacitor/haptics`

```typescript
import { Haptics, ImpactStyle } from '@capacitor/haptics';

// Use for bet placement, alerts, etc.
export function triggerHaptic(type: 'light' | 'medium' | 'heavy' = 'medium') {
  Haptics.impact({ style: ImpactStyle.Medium });
}

// Example usage in bet placement
function placeBet() {
  triggerHaptic('heavy');
  // Place bet logic...
}
```

#### 3.4 Share Functionality
**Install:** `@capacitor/share`

```typescript
import { Share } from '@capacitor/share';

export async function shareStrategy(strategyName: string, roi: number) {
  await Share.share({
    title: `${strategyName} Strategy`,
    text: `Check out this ${roi}% ROI betting strategy on MAX EV SPORTS!`,
    url: 'https://max-ev-sports.com',
    dialogTitle: 'Share Strategy',
  });
}
```

#### 3.5 Status Bar Styling
**Install:** `@capacitor/status-bar`

```typescript
import { StatusBar, Style } from '@capacitor/status-bar';

// Dark status bar for dark app
export async function configureStatusBar() {
  await StatusBar.setStyle({ style: Style.Dark });
  await StatusBar.setBackgroundColor({ color: '#1a1a1a' });
}
```

---

### Phase 4: iOS Specific (Week 3)

#### 4.1 Prerequisites
- **Mac required** (or Xcode Cloud)
- **Xcode 15+** installed
- **Apple Developer Account** ($99/year)
- **iOS device** for testing

#### 4.2 iOS Project Setup
```bash
npx cap open ios
```

**Configure in Xcode:**
1. **Bundle Identifier:** `com.maxevsports.app`
2. **Team:** Select your Apple Developer account
3. **Deployment Target:** iOS 14.0+
4. **Capabilities:**
   - Push Notifications: ON
   - Background Modes: Remote notifications, Background fetch
   - Sign in with Apple: ON (if using)
   - In-App Purchase: ON (for subscriptions)

#### 4.3 iOS App Icons & Splash Screen
**Required sizes:**
- App Icon: 1024x1024 (App Store)
- Various sizes: 20x20 to 180x180
- Splash screens: Multiple resolutions

**Tool:** Use https://www.appicon.co/ to generate all sizes

**Place in:** `frontend/ios/App/App/Assets.xcassets/`

#### 4.4 iOS Privacy Strings (Required!)
**File:** `frontend/ios/App/App/Info.plist`

Add these privacy descriptions (Apple requires explanations):
```xml
<key>NSCameraUsageDescription</key>
<string>MAX EV SPORTS needs camera access to scan QR codes for quick bet placement.</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>MAX EV SPORTS uses your location to show relevant sportsbooks in your state.</string>

<key>NSUserTrackingUsageDescription</key>
<string>This allows us to provide personalized betting insights and improve your experience.</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>Save bet slips and strategy screenshots to your photo library.</string>
```

#### 4.5 iOS Build Configuration
**File:** `frontend/ios/App/App.xcodeproj/project.pbxproj`

- **Provisioning Profile:** Automatic (Xcode manages)
- **Code Signing:** Automatic
- **Build Number:** Auto-increment with each build

**Script to auto-increment:**
```bash
# Add to Build Phases -> New Run Script Phase
buildNumber=$(/usr/libexec/PlistBuddy -c "Print CFBundleVersion" "${INFOPLIST_FILE}")
buildNumber=$(($buildNumber + 1))
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $buildNumber" "${INFOPLIST_FILE}"
```

#### 4.6 TestFlight Beta Testing
1. Build app in Xcode: Product → Archive
2. Upload to App Store Connect
3. Submit for TestFlight review (~24 hours)
4. Add beta testers (emails)
5. Test thoroughly before production

#### 4.7 App Store Submission
**Required assets:**
- Screenshots: 6.7", 6.5", 5.5" iPhones (multiple orientations)
- App Preview videos: 15-30 seconds
- Description: Compelling copy
- Keywords: "sports betting, odds, analytics, ev, sharp"
- Privacy Policy URL: https://max-ev-sports.com/privacy
- Support URL: Your support email
- Age Rating: 17+ (gambling content)

**Review time:** 24-48 hours typically

---

### Phase 5: Android Specific (Week 3-4)

#### 5.1 Prerequisites
- **Android Studio** installed (Windows, Mac, or Linux)
- **Google Play Developer Account** ($25 one-time fee)
- **Android device** for testing (or emulator)

#### 5.2 Android Project Setup
```bash
npx cap open android
```

**Configure in Android Studio:**
1. **Package Name:** `com.maxevsports.app`
2. **Min SDK:** 24 (Android 7.0+)
3. **Target SDK:** 34 (latest)
4. **Compile SDK:** 34

#### 5.3 Android Permissions
**File:** `frontend/android/app/src/main/AndroidManifest.xml`

```xml
<manifest>
  <!-- Required permissions -->
  <uses-permission android:name="android.permission.INTERNET" />
  <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

  <!-- Optional permissions -->
  <uses-permission android:name="android.permission.VIBRATE" />
  <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
  <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
  <uses-permission android:name="android.permission.CAMERA" />

  <application
    android:allowBackup="true"
    android:icon="@mipmap/ic_launcher"
    android:label="MAX EV SPORTS"
    android:roundIcon="@mipmap/ic_launcher_round"
    android:theme="@style/AppTheme"
    android:usesCleartextTraffic="false">
    <!-- Activities... -->
  </application>
</manifest>
```

#### 5.4 Android App Icons & Splash
**Required sizes:**
- `mipmap-mdpi`: 48x48
- `mipmap-hdpi`: 72x72
- `mipmap-xhdpi`: 96x96
- `mipmap-xxhdpi`: 144x144
- `mipmap-xxxhdpi`: 192x192
- Play Store: 512x512

**Adaptive Icons:** Required for Android 8.0+
- Foreground layer
- Background layer

**Tool:** Use Android Studio → Image Asset Studio

#### 5.5 Android Signing (Required for Release)
**Generate keystore:**
```bash
keytool -genkey -v -keystore maxev-release.keystore \
  -alias maxev-key -keyalg RSA -keysize 2048 -validity 10000
```

**File:** `frontend/android/key.properties` (DON'T COMMIT!)
```properties
storePassword=YOUR_STORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=maxev-key
storeFile=../maxev-release.keystore
```

**File:** `frontend/android/app/build.gradle`
```gradle
android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile file(keystoreProperties['storeFile'])
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

#### 5.6 Android Build Types
**Debug build:**
```bash
cd android
./gradlew assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk
```

**Release build (for Play Store):**
```bash
./gradlew bundleRelease
# Output: app/build/outputs/bundle/release/app-release.aab
```

#### 5.7 Google Play Console Setup
1. Create app at https://play.google.com/console
2. **App details:**
   - Name: MAX EV SPORTS
   - Category: Sports
   - Content rating: Everyone (or appropriate)
3. **Store listing:**
   - Screenshots: Phone + Tablet (min 2, max 8)
   - Feature graphic: 1024x500
   - Description: Compelling copy with keywords
   - Privacy policy URL
4. **Pricing:** Free (with in-app purchases for subscriptions)
5. **Countries:** Select target countries

#### 5.8 Internal Testing Track
1. Upload AAB file
2. Add testers (emails or Google Groups)
3. Test thoroughly (5-10 testers recommended)
4. Fix bugs, iterate

#### 5.9 Production Release
1. Promote from Internal → Alpha → Beta → Production
2. **Review time:** Usually 1-3 days
3. **Staged rollout:** Start with 10%, then 25%, 50%, 100%

---

### Phase 6: App Store Optimization (ASO)

#### 6.1 App Name & Subtitle
**iOS:**
- **Name:** MAX EV SPORTS (30 chars max)
- **Subtitle:** Sports Betting Analytics & Odds (30 chars max)

**Android:**
- **Name:** MAX EV SPORTS - Betting Analytics (50 chars max)

#### 6.2 Keywords (iOS)
100 character limit, comma-separated:
```
sports betting,odds,analytics,ev,sharp,arbitrage,prop bets,live odds,betting tips,nba,nfl,mlb,nhl
```

#### 6.3 Description (Both Platforms)
**First 3 lines critical** (shown before "more"):
```
MAX EV SPORTS - Your Edge in Sports Betting

Real-time odds from 15+ sportsbooks. Advanced analytics.
ML-powered predictions. Arbitrage alerts. Sharp betting strategies.

🎯 LIVE ODDS COMPARISON
• 15+ sportsbooks (DraftKings, FanDuel, BetMGM, etc.)
• Real-time line movement tracking
• Best available lines highlighted
• Opening lines vs current odds

📊 ADVANCED ANALYTICS
• 87 ML models (XGBoost, LightGBM, Random Forest)
• Daily predictions for NBA, NFL, MLB, NHL, NCAAB, NCAAF
• 60%+ win rate strategies
• Historical backtesting

⚡ INSTANT ALERTS
• Arbitrage opportunities (guaranteed profit)
• Steam moves (sharp money tracking)
• Middle opportunities
• Line value detection

💰 25+ BETTING STRATEGIES
• Goalie Pull Timing (80.4% ROI)
• NBA Quarter Reversals
• Favorite Comeback System
• And 22 more...

📈 MODEL PERFORMANCE
• Track all predictions vs actual results
• Confidence levels (HIGH/MEDIUM/LOW)
• ROI tracking by strategy
• Transparent results

🏆 TRUSTED BY SHARPS
• Used by professional handicappers
• Partner program for influencers
• Educational content & articles

FREE FEATURES:
✓ Live odds comparison
✓ Basic analytics
✓ 3 strategies

ELITE SUBSCRIPTION:
✓ All 25+ strategies
✓ ML predictions (all 5 sports)
✓ Advanced analytics
✓ Priority alerts
✓ API access

Try 7 days free, cancel anytime.

Age 18+. Gamble responsibly.
```

#### 6.4 Screenshots Strategy
**Required:** 3-8 screenshots per device size

**Recommended order:**
1. **Live Games** - Show real-time odds, multiple games
2. **Best Play Alert** - Highlight arbitrage opportunity
3. **Analytics Dashboard** - Charts, ROI, performance
4. **Strategy Results** - Show 80.4% ROI Goalie Pull
5. **Edge Lab** - Sharp vs public analysis
6. **Model Predictions** - ML consensus picks

**Design tips:**
- Add text overlays with benefits
- Use high contrast (dark backgrounds)
- Show real data (not lorem ipsum)
- Include app frame mockups

#### 6.5 App Preview Videos (Optional but Recommended)
**iOS:** 15-30 seconds
**Android:** 30 seconds to 2 minutes

**Script:**
1. (0-5s) Open app → Live Games page
2. (5-10s) Tap game → Show odds from multiple books
3. (10-15s) Alert notification appears → Arbitrage opportunity
4. (15-20s) Navigate to Analytics → Show ROI chart
5. (20-25s) Strategy Results → Highlight 80.4% ROI
6. (25-30s) Logo + "Download FREE on App Store"

---

### Phase 7: Subscription Integration

#### 7.1 iOS In-App Purchases
**Setup in App Store Connect:**
1. Agreements, Tax, Banking → Complete
2. In-App Purchases → Create
3. **Product Type:** Auto-Renewable Subscription
4. **Product IDs:**
   - `com.maxevsports.elite.monthly` - $49.99/month
   - `com.maxevsports.elite.yearly` - $499.99/year

**Install:** `@capacitor-community/in-app-purchases`

```bash
npm install @capacitor-community/in-app-purchases
```

**Create:** `frontend/src/services/iap.ts`
```typescript
import { InAppPurchase2 } from '@capacitor-community/in-app-purchases';

export async function initIAP() {
  await InAppPurchase2.initialize({
    products: [
      {
        id: 'com.maxevsports.elite.monthly',
        type: InAppPurchase2.ProductType.PAID_SUBSCRIPTION,
      },
      {
        id: 'com.maxevsports.elite.yearly',
        type: InAppPurchase2.ProductType.PAID_SUBSCRIPTION,
      },
    ],
  });
}

export async function purchaseElite(productId: string) {
  const result = await InAppPurchase2.purchase({
    productId,
  });

  if (result.success) {
    // Send receipt to backend for verification
    await verifyPurchase(result.transactionId, result.receipt);
  }
}

async function verifyPurchase(transactionId: string, receipt: string) {
  // POST to backend: /api/subscription/verify-ios
  await fetch('https://max-ev-sports.com/api/subscription/verify-ios', {
    method: 'POST',
    body: JSON.stringify({ transactionId, receipt }),
  });
}
```

**Backend verification:**
```python
# backend/routes/subscription.py
from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.post("/api/subscription/verify-ios")
async def verify_ios_purchase(transaction_id: str, receipt: str):
    """Verify iOS receipt with Apple servers"""
    # Send receipt to Apple for verification
    apple_url = "https://buy.itunes.apple.com/verifyReceipt"
    response = requests.post(apple_url, json={
        "receipt-data": receipt,
        "password": "YOUR_SHARED_SECRET",  # From App Store Connect
    })

    if response.json()["status"] == 0:
        # Valid purchase, grant subscription
        # Update user's subscription_tier to 'elite'
        return {"success": True}
    else:
        raise HTTPException(400, "Invalid receipt")
```

#### 7.2 Android In-App Billing
**Setup in Google Play Console:**
1. Monetize → Products → Subscriptions → Create
2. **Product IDs:**
   - `elite_monthly` - $49.99/month
   - `elite_yearly` - $499.99/year
3. Configure billing periods, pricing, free trials

**Same plugin as iOS** - `@capacitor-community/in-app-purchases` handles both!

**Backend verification for Android:**
```python
@router.post("/api/subscription/verify-android")
async def verify_android_purchase(purchase_token: str, product_id: str):
    """Verify Android purchase with Google Play"""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    # Use Google Play Developer API
    credentials = service_account.Credentials.from_service_account_file(
        'google-play-api-key.json',
        scopes=['https://www.googleapis.com/auth/androidpublisher']
    )

    service = build('androidpublisher', 'v3', credentials=credentials)
    result = service.purchases().subscriptions().get(
        packageName='com.maxevsports.app',
        subscriptionId=product_id,
        token=purchase_token
    ).execute()

    if result['purchaseState'] == 0:  # 0 = purchased
        # Grant subscription
        return {"success": True}
    else:
        raise HTTPException(400, "Invalid purchase")
```

#### 7.3 Subscription Status Sync
**Challenge:** User might subscribe on web with Stripe, but app needs to know.

**Solution:** Backend consolidation
```python
@router.get("/api/subscription/status")
async def get_subscription_status(user_id: str):
    """Check subscription from ALL sources"""
    # Check Stripe (web subscriptions)
    stripe_sub = check_stripe_subscription(user_id)

    # Check iOS subscriptions
    ios_sub = check_ios_subscription(user_id)

    # Check Android subscriptions
    android_sub = check_android_subscription(user_id)

    # Return highest tier
    if stripe_sub or ios_sub or android_sub:
        return {"tier": "elite", "source": "stripe|ios|android"}
    else:
        return {"tier": "free"}
```

---

### Phase 8: Testing & QA

#### 8.1 Device Testing Matrix
**iOS (minimum):**
- iPhone SE (small screen)
- iPhone 14 Pro (standard)
- iPhone 15 Pro Max (large + Dynamic Island)
- iPad Air (tablet layout)

**Android (minimum):**
- Samsung Galaxy S21 (standard)
- Google Pixel 7 (stock Android)
- Samsung Galaxy S23 Ultra (large screen)
- Budget device (e.g., Moto G) - test low-end performance

#### 8.2 Test Cases Checklist
- [ ] Login/Signup flow works
- [ ] Biometric login works (Face ID, Touch ID, Fingerprint)
- [ ] Live games update in real-time
- [ ] Charts render correctly on small screens
- [ ] Alerts fire and show notifications
- [ ] Push notifications work when app is closed
- [ ] Subscription purchase flow (both platforms)
- [ ] Deep links work (e.g., open strategy from notification)
- [ ] Offline mode handles gracefully
- [ ] App doesn't crash on network errors
- [ ] Battery usage is reasonable
- [ ] App size is acceptable (<100MB ideal)
- [ ] All 37 pages load correctly
- [ ] Navigation works (back button, gestures)
- [ ] Keyboard handling (no input covered by keyboard)
- [ ] Landscape mode (if supported)
- [ ] Dark mode only (your app is dark theme)

#### 8.3 Performance Benchmarks
**Target metrics:**
- App launch: <3 seconds (cold start)
- Page navigation: <500ms
- API calls: <2 seconds (network dependent)
- Chart rendering: <1 second
- Battery drain: <5% per hour active use
- App size: <80MB (iOS), <60MB (Android)

#### 8.4 Beta Testing
**Recommended testers:** 20-50 people
- Mix of iOS and Android users
- Different experience levels (sharp bettors + casual)
- Different device types
- Different network conditions (WiFi, 4G, 5G)

**Collect feedback:**
- Crash reports (automatic via TestFlight/Play Console)
- Bug reports (in-app feedback button)
- Feature requests
- Performance issues

---

### Phase 9: Launch & Marketing

#### 9.1 Soft Launch Strategy
1. **Week 1:** Internal testing only
2. **Week 2-3:** Beta testing (20-50 users)
3. **Week 4:** Soft launch to existing web users
4. **Week 5+:** Full public launch

#### 9.2 App Store Launch Checklist
- [ ] App approved on App Store
- [ ] App approved on Play Store
- [ ] All subscriptions active and tested
- [ ] Push notification infrastructure ready
- [ ] Support email/chat configured
- [ ] Privacy policy updated for mobile
- [ ] Terms of service updated
- [ ] Press kit prepared (screenshots, description, logo)
- [ ] Landing page updated: "Download our mobile app!"
- [ ] Email campaign to existing users
- [ ] Social media posts scheduled
- [ ] App Store screenshots optimized
- [ ] Keywords researched and implemented

#### 9.3 Marketing Assets
**Create:**
- App launch video (30-60s)
- App Store screenshot graphics
- Social media graphics (Instagram, Twitter/X, Facebook)
- Email template: "MAX EV SPORTS is now on mobile!"
- Blog post: Feature overview
- Press release (optional)

**Messaging:**
- "Your edge, in your pocket"
- "Live alerts. Instant bets. Maximum EV."
- "Pro-level betting analytics on the go"

#### 9.4 User Acquisition
**Channels:**
1. **Email list** - Announce to existing 34+ users
2. **Social media** - Twitter/X sports betting community
3. **Reddit** - r/sportsbook (check rules first!)
4. **Partner influencers** - Use your referral program
5. **App Store SEO** - Optimize keywords, description
6. **Paid ads** (optional):
   - Apple Search Ads ($100/day budget)
   - Google App Campaigns ($100/day budget)
   - Target keywords: "sports betting app", "odds comparison"

---

### Phase 10: Post-Launch Operations

#### 10.1 Monitoring & Analytics
**Install:** Firebase Analytics (free, cross-platform)
```bash
npm install @capacitor-firebase/analytics
```

**Track:**
- Daily Active Users (DAU)
- Monthly Active Users (MAU)
- Retention (Day 1, Day 7, Day 30)
- Session length
- Most used features
- Crash rate (<0.5% target)
- ANR rate (Android Not Responding) (<0.1% target)

#### 10.2 Crash Reporting
**Install:** Sentry or Crashlytics
```bash
npm install @sentry/capacitor
```

**Monitor:**
- Crash-free sessions (>99.5% target)
- Error types and frequency
- Affected devices/OS versions

#### 10.3 App Updates
**Release cadence:**
- **Hotfixes:** As needed (critical bugs)
- **Minor updates:** Every 2-4 weeks (bug fixes, small features)
- **Major updates:** Every 2-3 months (new features)

**Update process:**
1. Fix bugs/add features
2. Increment version number (e.g., 1.0.0 → 1.1.0)
3. Build new version
4. Submit to App Store (24-48h review)
5. Submit to Play Store (1-3 day review)
6. Staged rollout (10% → 50% → 100%)
7. Monitor crash reports

#### 10.4 Customer Support
**Setup:**
- In-app chat (e.g., Intercom, Zendesk)
- Support email: support@max-ev-sports.com
- FAQ section in app
- Video tutorials

**Common issues:**
- Login problems
- Subscription not activating
- Notifications not working
- App crashes
- Performance issues

#### 10.5 Legal Compliance
**Age gates:** Must verify 18+ in gambling states
**Geo-blocking:** Block users in restricted states/countries
**Responsible gambling:** Add links to help resources
**Data privacy:** GDPR, CCPA compliance
**App Store policies:** No real money gambling, analytics only

---

## 📅 Development Timeline

### Conservative Estimate (One Developer)

| Phase | Tasks | Duration |
|-------|-------|----------|
| **Phase 1** | Capacitor setup, config | 3 days |
| **Phase 2** | Mobile adaptations, responsive design | 7 days |
| **Phase 3** | Mobile features (push, biometrics) | 5 days |
| **Phase 4** | iOS setup, icons, App Store submission | 5 days |
| **Phase 5** | Android setup, Play Store submission | 5 days |
| **Phase 6** | ASO, screenshots, descriptions | 3 days |
| **Phase 7** | Subscription integration (IAP) | 7 days |
| **Phase 8** | Testing, QA, bug fixes | 10 days |
| **Phase 9** | Beta testing feedback, iterations | 7 days |
| **Phase 10** | Launch prep, marketing | 3 days |
| **TOTAL** | | **55 days (~8 weeks)** |

### Aggressive Estimate (Experienced Developer)
- **4-5 weeks** if you already know React Native/Capacitor
- **6 weeks** if learning as you go

### Team of 2 (Frontend + Mobile Dev)
- **3-4 weeks** with parallel iOS/Android work

---

## 💰 Cost Breakdown

### Development Costs
- **Developer time:** 55 days × $500/day = **$27,500** (if outsourced)
- **OR:** Do it yourself (free, but time investment)

### Platform Fees
- **Apple Developer:** $99/year
- **Google Play:** $25 one-time
- **TOTAL:** $124 first year, $99/year after

### Infrastructure
- **Push notifications:**
  - Firebase Cloud Messaging (free up to 100K/month)
  - Apple Push Notification Service (free)
- **Analytics:** Firebase Analytics (free)
- **Crash reporting:** Sentry (free tier: 5K events/month)

### App Store Fees (30% cut of subscriptions)
- **Year 1:** Apple/Google take 30% of subscription revenue
- **Year 2+:** Reduced to 15% for subscribers >1 year
- **Example:** $49.99/month subscription
  - You receive: $34.99 (Year 1), $42.49 (Year 2+)

### Marketing (Optional)
- **Apple Search Ads:** $100-500/day
- **Google App Campaigns:** $100-500/day
- **Social media ads:** $500-2000/month
- **Influencer partnerships:** Variable

---

## 🎯 Success Metrics

### Month 1 Targets
- 100 downloads
- 20 daily active users
- 50% Day 1 retention
- 5 elite subscription conversions
- <1% crash rate

### Month 3 Targets
- 500 downloads
- 100 daily active users
- 40% Day 7 retention
- 25 elite subscriptions
- 4.5+ star rating (both stores)

### Month 6 Targets
- 2,000 downloads
- 400 daily active users
- 30% Day 30 retention
- 100 elite subscriptions
- Featured in App Store (goal)

---

## 🚨 Potential Challenges

### Technical Challenges
1. **Chart performance on mobile** - Recharts can be slow
   - Solution: Simplify charts, reduce animations
2. **Large bundle size** - React app might be >50MB
   - Solution: Code splitting, lazy loading
3. **Battery drain** - Live polling every 15s
   - Solution: Reduce polling when app in background
4. **Push notification setup** - APNs and FCM are complex
   - Solution: Use Firebase, well-documented

### Business Challenges
1. **App Store rejection** - Gambling-related apps scrutinized
   - Solution: Position as "analytics only", no real money betting
2. **Subscription conversion** - Users reluctant to pay in-app
   - Solution: Offer 7-day free trial
3. **Competition** - Other sports betting apps exist
   - Solution: Emphasize unique features (ML models, 25+ strategies)

### Legal Challenges
1. **State-by-state regulations** - Gambling laws vary
   - Solution: Geo-block users in restricted states
2. **Age verification** - Must be 18+
   - Solution: Require DOB on signup, verify
3. **Responsible gambling** - Must include warnings
   - Solution: Add "Gamble Responsibly" links, self-exclusion

---

## 🏁 Next Steps (This Week)

### Priority 1: Setup Capacitor (Day 1-2)
```bash
cd frontend
npm install @capacitor/core @capacitor/cli
npm install @capacitor/ios @capacitor/android
npx cap init "MAX EV SPORTS" "com.maxevsports.app"
npx cap add ios
npx cap add android
```

### Priority 2: Create Mobile Hook (Day 2)
Create `frontend/src/hooks/useMobile.ts` and start adapting layouts.

### Priority 3: Test on Real Device (Day 3)
```bash
npm run build
npx cap sync
npx cap open ios  # or npx cap open android
```

Run on physical device, verify basic functionality works.

### Priority 4: Plan Mobile-Specific Features (Day 3-5)
- Push notifications architecture
- Biometric authentication flow
- Mobile navigation redesign

---

## 📚 Resources

### Official Documentation
- **Capacitor:** https://capacitorjs.com/docs
- **iOS Human Interface Guidelines:** https://developer.apple.com/design/human-interface-guidelines/
- **Android Material Design:** https://m3.material.io/
- **App Store Connect:** https://developer.apple.com/app-store-connect/
- **Google Play Console:** https://play.google.com/console/

### Tutorials
- **Capacitor + React:** https://capacitorjs.com/docs/getting-started/environment-setup
- **iOS App Store submission:** https://www.youtube.com/watch?v=SkHsMJyNnVc
- **Android Play Store submission:** https://www.youtube.com/watch?v=QwP0lmF1bwI

### Communities
- **Capacitor Discord:** https://discord.gg/UPYYRhtyzp
- **r/iOSProgramming:** Reddit community
- **r/androiddev:** Reddit community

---

## ✅ Decision Summary

**Recommended Approach:** Capacitor + React

**Why:**
- ✅ Reuse 95%+ existing React codebase
- ✅ Ship iOS + Android in 4-6 weeks
- ✅ One codebase for web, iOS, Android, Electron
- ✅ Native features via plugins
- ✅ Faster time to market

**Alternative (Not Recommended):**
- React Native: Complete rewrite (6+ months)
- Flutter: Learn new framework (4+ months)
- Native (Swift/Kotlin): Two separate codebases (8+ months)

**Next Action:** Install Capacitor this week, start Phase 1.

---

**Created:** November 12, 2025 @ 5:37 AM CST
**Status:** Ready to start Phase 1
**Timeline:** 6-8 weeks to launch
**Cost:** $124 (platform fees) + time investment
