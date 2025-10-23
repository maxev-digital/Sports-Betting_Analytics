# User Bet Tracking System - Implementation Plan

## Overview
Build a comprehensive bet tracking system that automatically logs bets when users click bookmaker deep links, allows manual bet amount entry, and provides dual analytics views (system alerts vs personal bets).

---

## Feature Requirements

### 1. Automatic Bet Logging (Deep Link Click Tracking)
**When a user clicks a bookmaker icon on a game card:**
- Automatically create a "pending bet" record with:
  - Game details (teams, sport, date/time)
  - Bet type (spread, moneyline, total)
  - Recommended side (OVER/UNDER, team name)
  - Bookmaker clicked
  - Odds at time of click
  - Alert confidence level (HIGH/MEDIUM/LOW)
  - System edge calculation
  - Timestamp of click
  - User ID
  - Status: "pending" (waiting for user to enter stake)

### 2. Bet Amount Entry Page
**New page: `/my-bets` or `/bet-tracker`**

**Features:**
- List of all pending bets (clicked but no stake entered yet)
- For each pending bet, show:
  - Game matchup and time
  - Bet type and recommended side
  - Bookmaker
  - Odds
  - Edge %
  - Time clicked
- Input field to enter stake amount
- "Log Bet" button to confirm with stake
- "Remove" button to delete if bet wasn't actually placed
- Filter: Pending / Active / Settled / All
- Sort by: Date, Sport, Stake Size, Edge

**After entering stake:**
- Bet status changes from "pending" to "active"
- Bet is now tracked in analytics
- Calculate potential payout based on odds and stake

### 3. Dual Analytics Page
**Update existing `/analytics` page with two tabs/toggles:**

#### Tab 1: System Alerts Performance
**Tracks all alerts the system generated (whether user bet or not)**
- Overall stats:
  - Total alerts sent
  - Win rate of alerts (based on actual game outcomes)
  - Average edge of alerts
  - ROI if user had bet $100 on every alert
  - Performance by confidence level (HIGH/MEDIUM/LOW)
  - Performance by sport (NBA, NFL, NHL, etc.)
  - Performance by bet type (spread, total, moneyline)
  - Performance by strategy (RLM, Fade Public, etc.)

- Table of all historical alerts:
  - Date/Time
  - Game
  - Bet recommendation
  - Confidence
  - Edge %
  - Odds
  - User bet on it? (Yes/No badge)
  - Result (Win/Loss/Push/Pending)
  - User missed this winner (highlight if user didn't bet but it won)

#### Tab 2: My Bets Performance
**Tracks only the bets the user actually placed**
- Overall stats:
  - Total bets placed
  - Total wagered
  - Total returned (payouts)
  - Net profit/loss
  - ROI %
  - Win rate
  - Average stake
  - Biggest win
  - Biggest loss
  - Performance by sport
  - Performance by bookmaker
  - Performance by confidence level (of bets taken)

- Breakdown sections:
  - By Sport (NBA, NFL, NHL, etc.)
  - By Bet Type (Spread, Total, Moneyline)
  - By Bookmaker (which books are most profitable for user)
  - By Confidence Level (did HIGH confidence bets perform better?)
  - By Strategy (which strategies did user bet on most)

- Table of all user bets:
  - Date/Time placed
  - Game
  - Bet type and side
  - Stake
  - Odds
  - Bookmaker
  - Confidence level
  - Edge %
  - Status (Active/Won/Lost/Push)
  - Payout (if settled)
  - Profit/Loss

### 4. Missed Opportunities View
**Special section showing alerts user didn't bet on:**
- Filter to show only:
  - Alerts user didn't bet that WON (missed profits)
  - Alerts user didn't bet that LOST (good avoids)
- Calculate: "What if I bet $X on every alert I skipped?"
- Helps user see if they're cherry-picking poorly

---

## Database Schema / Data Models

### UserBet Model
```typescript
interface UserBet {
  id: string;
  user_id: string;

  // Game Info
  game_id: string;
  sport: string;
  home_team: string;
  away_team: string;
  commence_time: string;

  // Bet Details
  bet_type: 'spread' | 'total' | 'moneyline' | 'prop';
  bet_side: string;  // "OVER", "UNDER", "Lakers", "Cowboys +3.5", etc.
  stake: number;  // Amount wagered
  odds: number;  // American odds (-110, +150, etc.)
  bookmaker: string;  // "DraftKings", "FanDuel", etc.

  // System Data
  alert_id?: string;  // Link to original alert if from system
  confidence: 'HIGH' | 'MEDIUM' | 'LOW' | null;
  edge_percent: number | null;
  strategy?: string;  // "RLM", "Fade Public", etc.

  // Tracking
  clicked_at: string;  // When deep link was clicked
  logged_at: string;  // When user entered stake
  status: 'pending' | 'active' | 'won' | 'lost' | 'push' | 'cancelled';

  // Settlement
  result?: 'win' | 'loss' | 'push';
  payout?: number;  // Amount returned if won
  profit_loss?: number;  // Net profit or loss
  settled_at?: string;  // When bet was graded
}
```

### Alert Model (enhancement to existing alerts)
```typescript
interface Alert {
  // ... existing fields ...

  // Add tracking fields:
  user_clicked: boolean;  // Did user click a bookmaker link?
  user_bet_on_it: boolean;  // Did user actually log a bet?
  user_bet_id?: string;  // Reference to UserBet if placed

  // Result tracking:
  result?: 'win' | 'loss' | 'push';  // Actual outcome
  settled_at?: string;
}
```

---

## API Endpoints Needed

### Bet Tracking Endpoints

**POST /api/bets/track-click**
- Body: `{ user_id, game_id, alert_id, bet_type, bet_side, odds, bookmaker }`
- Creates pending bet when user clicks bookmaker icon
- Returns: bet_id

**GET /api/bets/pending**
- Query: `?user_id=xxx`
- Returns: All pending bets for user (clicked but no stake entered)

**PUT /api/bets/:bet_id/add-stake**
- Body: `{ stake: number }`
- Updates pending bet with stake amount
- Changes status from "pending" to "active"

**DELETE /api/bets/:bet_id**
- Removes a pending or cancelled bet

**GET /api/bets/my-bets**
- Query: `?user_id=xxx&status=active|settled|all`
- Returns: All user's bets with optional status filter

**PUT /api/bets/:bet_id/settle**
- Body: `{ result: 'win'|'loss'|'push', actual_score?: {} }`
- Grades a bet as won/lost/push
- Calculates payout and profit/loss

### Analytics Endpoints

**GET /api/analytics/system-alerts**
- Query: `?user_id=xxx&sport=xxx&date_from=xxx&date_to=xxx`
- Returns: All system alerts with results and whether user bet on them

**GET /api/analytics/my-performance**
- Query: `?user_id=xxx&date_from=xxx&date_to=xxx`
- Returns: User's bet performance stats and breakdown

**GET /api/analytics/missed-opportunities**
- Query: `?user_id=xxx&show=winners|losers|all`
- Returns: Alerts user didn't bet on with results

---

## Frontend Components Needed

### 1. Enhanced GameCard Component
**Modification: `GameCard.tsx`**
- When bookmaker icon clicked:
  - Call `POST /api/bets/track-click` API
  - Show toast: "Bet tracked! Add stake amount in My Bets page"
  - Visual indicator (badge) if user already has pending bet on this game
  - Different icon color if user already bet on this game

### 2. My Bets Page (NEW)
**File: `frontend/src/pages/MyBets.tsx`**

**Sections:**
- **Pending Bets** (top, most important)
  - Cards showing each pending bet
  - Input to add stake
  - Confirm/Remove buttons

- **Active Bets**
  - Bets with stakes entered, waiting for game result
  - Ability to manually settle if needed

- **Settled Bets**
  - Historical bets with results
  - Sortable/filterable table

**Features:**
- Search/filter by sport, date, bookmaker
- Quick stats at top: Total wagered, Total returned, Net P/L, ROI

### 3. Enhanced Analytics Page
**Modification: `frontend/src/pages/Analytics.tsx`**

**Add toggle/tabs:**
```tsx
<Tabs>
  <Tab label="System Alerts" icon={target}>
    <SystemAlertsAnalytics />
  </Tab>
  <Tab label="My Bets" icon={dollar}>
    <MyBetsAnalytics />
  </Tab>
  <Tab label="Missed Opportunities" icon={search}>
    <MissedOpportunitiesView />
  </Tab>
</Tabs>
```

**SystemAlertsAnalytics Component:**
- Stats cards (total alerts, win rate, ROI if all bet)
- Chart: Win rate by confidence level
- Chart: ROI by sport
- Table: All alerts with results

**MyBetsAnalytics Component:**
- Stats cards (total wagered, returned, P/L, ROI, win rate)
- Chart: Profit over time (line chart)
- Chart: Win rate by sport (bar chart)
- Chart: Profit by bookmaker (bar chart)
- Breakdown tables

**MissedOpportunitiesView Component:**
- Filter: Won only / Lost only / All
- Table: Alerts user didn't bet on
- Calculate: Hypothetical P/L if user bet on all missed alerts

### 4. BetCard Component (NEW)
**File: `frontend/src/components/BetCard.tsx`**
- Reusable card to display a single bet
- Shows all bet details
- Different styling based on status (pending/active/won/lost/push)
- Actions based on status (add stake / settle / view details)

---

## Implementation Phases

### Phase 1: Deep Link Click Tracking
1. Update GameCard to track bookmaker clicks
2. Create POST /api/bets/track-click endpoint
3. Create UserBet database model/table
4. Test: Click bookmaker icon → bet logged as pending

### Phase 2: My Bets Page
1. Create MyBets.tsx page
2. Create GET /api/bets/pending endpoint
3. Build pending bets list UI
4. Create PUT /api/bets/:bet_id/add-stake endpoint
5. Build stake input and confirm flow
6. Test: Add stake to pending bet → becomes active

### Phase 3: Bet Settlement
1. Create PUT /api/bets/:bet_id/settle endpoint
2. Build manual settlement UI in My Bets page
3. Create automatic settlement service (compares with game results)
4. Test: Game finishes → bets auto-graded

### Phase 4: Analytics - System Alerts Tab
1. Enhance Alert model to track user interaction
2. Create GET /api/analytics/system-alerts endpoint
3. Build SystemAlertsAnalytics component
4. Add charts and tables
5. Test: View all alerts with results

### Phase 5: Analytics - My Bets Tab
1. Create GET /api/analytics/my-performance endpoint
2. Build MyBetsAnalytics component
3. Add profit charts and breakdowns
4. Test: View personal betting performance

### Phase 6: Missed Opportunities
1. Create GET /api/analytics/missed-opportunities endpoint
2. Build MissedOpportunitiesView component
3. Add "what if" calculations
4. Test: View alerts user didn't bet on

### Phase 7: Polish & Enhancements
1. Add visual indicators on GameCard for existing bets
2. Add notifications for settled bets
3. Add export functionality (CSV of bets)
4. Add bankroll management suggestions
5. Add streak tracking (win/loss streaks)

---

## Technical Considerations

### Database Choice
- **Backend storage:** SQLite (for quick start) or PostgreSQL (production)
- **Tables needed:** `user_bets`, `alerts` (enhance existing), `users` (existing)

### Authentication
- Already have auth system (from AuthContext)
- Use `user_id` from auth context for all bet tracking

### Odds Calculation
- **American odds to decimal:**
  - If odds > 0: `(odds / 100) + 1`
  - If odds < 0: `(100 / abs(odds)) + 1`
- **Payout calculation:** `stake * decimal_odds`
- **Profit:** `payout - stake`

### Automatic Grading
- After game finishes, compare bet against final score
- For spreads: Did team cover?
- For totals: Was total OVER or UNDER?
- For moneyline: Did team win?
- Set result to 'win', 'loss', or 'push'
- Calculate payout if win

### Data Persistence
- Store bets in backend database (not localStorage)
- Sync across devices for same user
- Regular backups

---

## UI/UX Mockup Notes

### My Bets Page Layout
```
┌─────────────────────────────────────────────────────┐
│  MY BETS                                    [Filter]│
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                     │
│  💰 Quick Stats                                     │
│  ┌──────────┬──────────┬──────────┬──────────┐    │
│  │ Wagered  │ Returned │  Net P/L │   ROI    │    │
│  │ $1,250   │ $1,450   │  +$200   │  +16.0%  │    │
│  └──────────┴──────────┴──────────┴──────────┘    │
│                                                     │
│  ⏳ Pending Bets (3)                               │
│  ┌───────────────────────────────────────────────┐ │
│  │ 🏀 Lakers vs Celtics - OVER 220.5 (-110)     │ │
│  │ DraftKings • HIGH confidence • +7.2% edge    │ │
│  │ Clicked: 2 hours ago                         │ │
│  │ Stake: [$_____] [LOG BET] [REMOVE]           │ │
│  └───────────────────────────────────────────────┘ │
│  ...                                                │
│                                                     │
│  🔴 Active Bets (5)                                │
│  ...                                                │
│                                                     │
│  ✅ Settled Bets (23)                              │
│  [Table with all settled bets]                     │
└─────────────────────────────────────────────────────┘
```

### Analytics Page - My Bets Tab Layout
```
┌─────────────────────────────────────────────────────┐
│  ANALYTICS                                          │
│  [System Alerts] [MY BETS] [Missed Opportunities]   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                     │
│  📊 Overall Performance                             │
│  ┌────┬────┬────┬────┬────┬────┐                  │
│  │Bets│ W  │ L  │ P  │ROI │Win%│                  │
│  │ 47 │ 28 │ 17 │ 2  │18% │60% │                  │
│  └────┴────┴────┴────┴────┴────┘                  │
│                                                     │
│  📈 Profit Over Time                               │
│  [Line chart showing cumulative profit]             │
│                                                     │
│  🏆 Performance by Sport                           │
│  [Bar chart: NBA, NFL, NHL profits]                │
│                                                     │
│  📚 Performance by Bookmaker                       │
│  [Table showing ROI per bookmaker]                 │
│                                                     │
│  🎯 Performance by Confidence Level                │
│  [HIGH: 22% ROI | MEDIUM: 14% ROI | LOW: -2% ROI] │
└─────────────────────────────────────────────────────┘
```

---

## Success Metrics

**User Engagement:**
- % of users who click deep links
- % of clicked bets that get stakes entered
- Average time from click to stake entry
- Frequency of analytics page visits

**Product Value:**
- User retention (do they come back?)
- Avg bets tracked per user per week
- User profitability (are users making money?)
- Feature usage (which analytics views most viewed?)

---

## Future Enhancements

1. **Bankroll Management:**
   - Set starting bankroll
   - Track current bankroll
   - Suggest bet sizes based on Kelly Criterion
   - Alerts if user overbetting

2. **Social Features:**
   - Share your wins
   - Leaderboards (best ROI among users)
   - Follow other successful bettors

3. **Advanced Analytics:**
   - Bet correlation analysis
   - Time-of-day performance
   - Hot/cold streaks visualization
   - Bet size optimization

4. **Integrations:**
   - Import bets from sportsbook APIs (if available)
   - Export to tax software (1099 reporting)
   - Connect to bankroll management apps

5. **Notifications:**
   - Push notification when bet settles
   - Daily summary emails
   - Alerts for unusual betting patterns (losing streak)

---

**Created by MAX-EV-SPORTS**
*Last updated: October 20, 2025*
