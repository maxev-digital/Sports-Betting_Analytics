# Max EV Sports - Sound Effects Implementation Guide

## ✅ What's Been Implemented

### 1. Sound Effect Generator
- **File**: `backend/utils/generate_sound_effects.py`
- **Generated**: 46 sound effects using Eleven Labs API
- **Total Sounds**: 48 (including existing bull.mp3 and flame.mp3)
- **Location**: `frontend/public/*.mp3`

### 2. Custom React Hook
- **File**: `frontend/src/hooks/useSoundEffect.ts`
- **Usage**: Makes it easy to add sounds to any component
- **Example**:
```typescript
import { useSoundEffect } from '../hooks/useSoundEffect';

// In your component
const playAlertBell = useSoundEffect('alert-bell.mp3', 0.3); // 30% volume

// Call it anywhere
playAlertBell();
```

### 3. Sound Preview Page
- **Route**: `http://localhost:5177/sound-preview`
- **Features**:
  - Test all 48 sounds interactively
  - Volume control slider
  - Organized by category
  - Click any button to play

### 4. Strategy Settings Page - IMPLEMENTED ✅
- **File**: `backend/scrapers/nba/frontend/src/pages/StrategySettings.tsx`
- **Sounds Added**:
  - `toggle-on.mp3` - When enabling a strategy
  - `toggle-off.mp3` - When disabling a strategy
  - `save.mp3` - After settings save (500ms delay)
- **Volume**: 25-30% (subtle and professional)
- **User Experience**:
  - Instant audio feedback when clicking toggles
  - Satisfying "save" confirmation sound

---

## 🎯 Sounds Available (48 Total)

### Dashboard/Home
- `cash-register.mp3` - Cash register cha-ching
- `coins.mp3` - Coins clinking
- `whoosh.mp3` - Quick air swoosh
- `bull.mp3` - Bull market sound

### Alerts
- `alert-bell.mp3` - Notification bell
- `notification.mp3` - Modern app alert
- `siren.mp3` - Brief alert siren
- `whistle.mp3` - Referee whistle

### Props
- `swish.mp3` - Basketball net swish
- `swoosh.mp3` - Quick air swoosh
- `success.mp3` - Success chime

### Analytics
- `data-ping.mp3` - Digital ping
- `calculate.mp3` - Calculation sound
- `scan.mp3` - Electronic sweep

### Odds
- `tick.mp3` - Clock tick
- `click.mp3` - Mouse click
- `line-move.mp3` - Rising pitch tone
- `lock.mp3` - Mechanical lock

### Tools
- `power-up.mp3` - Power up sound
- `success-chime.mp3` - Success chime
- `tool-select.mp3` - Interface click

### Pricing
- `upgrade.mp3` - Achievement unlock
- `level-up.mp3` - Video game level up
- `checkout.mp3` - Purchase complete
- `unlock.mp3` - Achievement unlocked

### Strategy Settings (**IMPLEMENTED**)
- `toggle-on.mp3` ✅ - Toggle switch on
- `toggle-off.mp3` ✅ - Toggle switch off
- `save.mp3` ✅ - Save confirmation

### Multi-Sport
- `sport-switch.mp3` - Interface transition
- `buzzer.mp3` - Basketball buzzer
- `horn.mp3` - Hockey horn
- `whistle-nfl.mp3` - Football whistle

### Navigation
- `tab-switch.mp3` - Subtle tab switch
- `dropdown.mp3` - Dropdown menu open
- `logout.mp3` - Closing sound

### Bet Tracking
- `bet-placed.mp3` - Bet confirmation
- `win.mp3` - Celebration sound
- `victory.mp3` - Triumphant fanfare
- `loss.mp3` - Gentle descending tone
- `push.mp3` - Neutral beep

### Live Games
- `game-start.mp3` - Game start horn
- `buzzer-quarter.mp3` - Quarter end buzzer
- `goal.mp3` - Goal celebration
- `final-whistle.mp3` - Final whistle

### Learn/Education
- `page-turn.mp3` - Paper flip
- `lightbulb.mp3` - Bright ding
- `graduate.mp3` - Ascending scale

### Login/Signup
- `bull.mp3` - Login page (**already implemented**)
- `flame.mp3` - SignUp page (**already implemented**)

---

## 🚀 How to Add Sounds to Other Pages

### Example 1: Add Alert Sound to Alerts Page

```typescript
// At the top of Alerts.tsx
import { useSoundEffect } from '../hooks/useSoundEffect';

export function Alerts() {
  // Add the hook
  const playAlertBell = useSoundEffect('alert-bell.mp3', 0.3);

  // Play it when new alerts arrive
  useEffect(() => {
    if (alertsData && alertsData.arbitrage.count > 0) {
      playAlertBell();
    }
  }, [alertsData?.arbitrage.count]);

  // ... rest of component
}
```

### Example 2: Add Cash Register to Dashboard (High EV Plays)

```typescript
// In Dashboard.tsx or LiveGames.tsx
import { useSoundEffect } from '../hooks/useSoundEffect';

export function Dashboard() {
  const playCashRegister = useSoundEffect('cash-register.mp3', 0.35);

  // Play when displaying a HIGH confidence play
  const renderGameCard = (game) => {
    if (game.confidence === 'HIGH' && game.edge > 5) {
      playCashRegister();
    }
    return <GameCard {...game} />;
  };
}
```

### Example 3: Add Navigation Sounds to Dropdowns

```typescript
// In Navigation.tsx
import { useSoundEffect } from '../hooks/useSoundEffect';

export function Navigation() {
  const playDropdown = useSoundEffect('dropdown.mp3', 0.2);

  const handleDropdownOpen = () => {
    setSettingsDropdownOpen(!settingsDropdownOpen);
    playDropdown();
  };

  return (
    <button onClick={handleDropdownOpen}>
      Settings
    </button>
  );
}
```

### Example 4: Add Win/Loss Sounds to Bet Tracking

```typescript
// When recording bet results
import { useSoundEffect } from '../hooks/useSoundEffect';

const playWin = useSoundEffect('win.mp3', 0.4);
const playLoss = useSoundEffect('loss.mp3', 0.25);
const playPush = useSoundEffect('push.mp3', 0.2);

const recordBetResult = (result: 'win' | 'loss' | 'push') => {
  if (result === 'win') playWin();
  else if (result === 'loss') playLoss();
  else playPush();

  // ... save to backend
};
```

---

## 📊 Recommended Next Implementations

### Priority 1 (High Impact)
1. **Alerts Page** - Play `alert-bell.mp3` when new alerts appear
2. **Dashboard/LiveGames** - Play `cash-register.mp3` for HIGH confidence plays
3. **Props Page** - Play `swish.mp3` when loading NBA props

### Priority 2 (Enhanced UX)
4. **Navigation** - Play `dropdown.mp3` when opening Settings/Learn dropdowns
5. **Odds Page** - Play `line-move.mp3` when detecting sharp money
6. **Multi-Sport** - Play `sport-switch.mp3` when changing sports

### Priority 3 (Polish)
7. **Pricing** - Play `upgrade.mp3` on "Subscribe" button click
8. **Analytics** - Play `calculate.mp3` when running filters
9. **Tools** - Play `power-up.mp3` when activating a tool

---

## 🎛️ Volume Recommendations

- **Toggles/Clicks**: 20-25% (very subtle)
- **Alerts/Notifications**: 30-35% (noticeable but not loud)
- **Wins/Success**: 35-40% (celebratory but not obnoxious)
- **Losses**: 20-25% (sympathetic, quiet)

---

## 🧪 Testing Your Sounds

### Option 1: Sound Preview Page
Visit: `http://localhost:5177/sound-preview`

### Option 2: Test in Your Browser Console
```javascript
const audio = new Audio('/alert-bell.mp3');
audio.volume = 0.3;
audio.play();
```

### Option 3: Test Live on Strategy Settings
1. Go to `http://localhost:5177/strategy-settings`
2. Toggle any strategy on/off
3. Listen for the toggle-on/toggle-off sounds
4. Wait 500ms to hear the save confirmation sound

---

## 🔧 Regenerating or Adding New Sounds

If you want to add more sounds or regenerate existing ones:

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source ../venv/bin/activate  # Mac/Linux
../venv/Scripts/activate     # Windows

# Edit the SOUND_EFFECTS dictionary in utils/generate_sound_effects.py
# Then run:
python utils/generate_sound_effects.py
```

All new sounds will appear in `frontend/public/` and be immediately available to use!

---

## 📝 Summary

**What Works Right Now:**
- ✅ 48 high-quality sound effects generated and ready
- ✅ Easy-to-use React hook (`useSoundEffect`)
- ✅ Strategy Settings page has toggle sounds implemented
- ✅ Login page has bull.mp3 (already working)
- ✅ SignUp page has flame.mp3 (already working)
- ✅ Sound preview page for testing (`/sound-preview`)

**Next Steps (Your Choice):**
1. Test the Strategy Settings page to hear the sounds in action
2. Visit `/sound-preview` to test all sounds
3. Let me know which pages you want sounds added to next, and I'll implement them!

---

**Created**: 2025-10-24
**Sound Files**: All located in `frontend/public/`
**Documentation**: `backend/utils/SOUND_EFFECTS_GUIDE.md`
