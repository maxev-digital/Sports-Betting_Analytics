# Max EV Sports - Multi-Sport Live Betting Platform

## 🎯 Platform Overview

Max EV Sports is a comprehensive real-time sports betting analytics platform that tracks live games, odds movements, arbitrage opportunities, and provides actionable betting alerts across multiple sports leagues.  Ios and Android Apps Coming Soon

## 🏗️ Architecture

### Current Beta Model Technology Stack

**Backend:**
- **Framework:** FastAPI (Python)
- **Database:** SQLite with async support
- **Real-time Updates:** WebSocket connections
- **External APIs:** The Odds API for live odds data
- **Data Processing:** Pandas, NumPy for analytics

Next Tech Stack Addition After Beta Launch 
The jump-ahead stack delivers Phase 4+ capabilities (ML, mobile, social) from launch,
optimized for low initial demand (500 concurrent users) using AWS’s pay-as-you-go model
and Sportradar’s sub-second feeds.
• Data Provider: Sportradar (Odds Comparison + Probabilities APIs, $1,200/month)
– Unified feeds: Pre/live odds (150+ bookmakers), game states (scores, play-byplay), stats (player/team, injuries), rankings/standings.
– Sub-second latency (< 1s push notifications), 15–30s polling fallback.
– Supports ML true odds, arbitrage, and sharp money detection.
• Compute:
– AWS Fargate (ECS, 4 vCPUs/8GB, $120/month): Serverless backend for FastAPI,
scales to 5,000+ users.
– EC2 G5 Spot (48hrs/month, $29): ML training (XGBoost/LSTM for true odds).
– EC2 G4dn Spot (730hrs/month, $131): Real-time inference (< 1ms).
– Lambda (750K requests, $15): Backup inference for traffic spikes.
• Storage/Streaming:
– RDS PostgreSQL (db.t3.micro, 20GB, $25): Stores game data, user profiles.
– ElastiCache Redis (cache.t3.micro, 0.5GB, $15): Caches live odds for < 50ms
access.
– MSK Serverless (150GB, $75): Kafka for Sportradar WebSocket streaming.
– EMR Serverless (30hrs/month, $30): Spark for historical analytics.
• Mobile/Social/Notifications:
– CloudFront CDN (1TB/month, $100): Fast React/React Native asset delivery.
– SNS (1M push/SMS, $50): Real-time notifications for alerts.
– Redis (leaderboards, included in ElastiCache): Social feature foundation.
• Monitoring/Other:
– CloudWatch ($15): Metrics, logs, alarms.
– Hostinger VPS (VPS 6, $30): Fallback/dev environment.


**Frontend:**
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **UI Components:** Custom components with sport-specific theming
- **State Management:** React Context API
- **Routing:** React Router

### Project Structure

```
MAX-EV-Sports Platform
├── backend/
│   ├── main.py                 # FastAPI server with all endpoints
│   ├── database.py             # Database models and operations
│   ├── odds_fetcher.py         # Real-time odds fetching logic
│   └── .env.production.example # Environment configuration template
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameCard.tsx           # Main game display component
│   │   │   ├── Navigation.tsx         # Top navigation with fire emoji home
│   │   │   └── GoaliePullAlert.tsx    # NHL goalie pull notifications
│   │   ├── pages/
│   │   │   ├── LiveGames.tsx          # Main games dashboard
│   │   │   ├── Alerts.tsx             # Betting alerts & opportunities
│   │   │   └── Login.tsx              # Authentication page
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx        # User authentication state
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript type definitions
│   │   └── utils/
│   │       └── sportDetection.ts      # Sport emoji and branding utilities
│   ├── public/
│   │   └── assets/
│   │       └── bookmaker-logos/       # Sportsbook logo assets
│   └── vite.config.ts
│
└── docs/
    ├── README.md                      # Main project documentation
    ├── PLATFORM_OVERVIEW.md           # This file
    ├── Live Betting System NBA.md     # NBA-specific betting logic
    ├── nba_betting_roadmap.guide.txt  # Development roadmap
    ├── SERVER_MIGRATION_GUIDE.md      # Deployment instructions
    └── RESTRUCTURE_PROJECT.md         # Architecture decisions
```

## 🎨 Design System

### Color Scheme & Branding

**Background:**
- Main pages: Solid black (`bg-black`)
- Alerts page: Black & gold gradient (`bg-gradient-to-br from-black via-yellow-900 to-black`)

**Sport-Specific Card Styling:**

1. **NCAAF (College Football)**
   - Gradient: `from-red-900 to-black`
   - Border: `border-red-600`
   - Premium red theme with dark fade

2. **NBA (Basketball)**
   - Gradient: `from-blue-900 to-slate-800`
   - Border: `border-blue-500`
   - Professional blue theme

3. **NFL/Other Sports**
   - Various sport-specific gradients
   - Consistent 4px borders
   - Dark-to-black gradient pattern

**Alert Categories (Color-Coded):**
- **Arbitrage Opportunities:** Red/black gradient (`from-red-900 to-black` + `border-red-600`)
- **Steam Moves:** Blue/black gradient (`from-blue-900 to-slate-800` + `border-blue-500`)
- **Line Movements:** Green/black gradient (`from-green-900 to-black` + `border-green-600`)

**Navigation:**
- Red gradient header: `bg-red-900 border-red-800`
- Fire emoji home button: Gold border on hover
- Sport filter tabs: Blue active state, slate inactive

### Typography
- **Headers:** Bold, tracking-wide, white text
- **Body:** Slate-300 to Slate-400 for secondary text
- **Emphasis:** Gold accents for premium features

## 🔥 Core Features

### 1. Live Games Dashboard (`/live-games`)

**Multi-Sport Coverage:**
- NFL (American Football)
- NCAAF (College Football)
- NBA (Basketball)
- NCAAB (College Basketball)
- NHL (Hockey)
- MLB (Baseball)
- PGA (Golf)
- ATP/WTA (Tennis)
- MMA (Mixed Martial Arts)
- WNBA (Women's Basketball)
- NASCAR (Racing)

**Game Display Features:**
- Real-time score updates
- Live game status indicators (pulsing red dot)
- Sport-specific emojis and branding
- Bookmaker odds comparison
- Best available odds highlighting
- EV (Expected Value) calculations
- Kelly Criterion bet sizing recommendations

**Sport Filtering:**
- Tab-based sport selection
- "All Games" view for complete overview
- Individual sport filters
- Tennis games grouped by tournament
- Live games prioritized over upcoming

**Tennis-Specific Features:**
- Tournament grouping (e.g., "US Open", "Wimbledon")
- Match-level details
- Tournament header with match counts
- Live tournament indicators

### 2. Live Alerts Dashboard (`/alerts`)

**Alert Types:**

1. **Arbitrage Opportunities**
   - Cross-bookmaker profit scenarios
   - Guaranteed profit calculations
   - Stake distribution per book
   - Profit percentage display
   - Expiration countdown
   - Real-time opportunity tracking

2. **Steam Moves**
   - Rapid line movements across multiple books
   - Consensus percentage tracking
   - Original vs new line comparison
   - Bookmaker movement lists
   - Sharp money indicators

3. **Line Movements**
   - Individual bookmaker line changes
   - Movement percentage calculations
   - Historical line tracking
   - Significant movement alerts

4. **NHL Goalie Pull Alerts** (Special Feature)
   - Real-time goalie pull notifications
   - Live betting opportunity signals
   - Time-sensitive alerts
   - Integration with live NHL data

**Alert Dashboard Features:**
- Auto-refresh toggle (10-second intervals)
- Manual refresh button
- Live statistics cards
- Tabbed interface for alert types
- Time-stamped alerts
- Sport-specific badges
- Market type indicators

### 3. Authentication System

**Current Implementation:**
- Login page with authentication
- User session management
- Protected routes
- Default user support for development

**Future Enhancement Areas:**
- Multi-user support
- User preferences storage
- Custom alert thresholds
- Betting history tracking

## 🔌 API Architecture

### Backend Endpoints

**Base URL:** `http://localhost:8000` (development)

#### Game Data Endpoints

```
GET /api/games
- Returns all live and upcoming games
- Query params: user_id (optional)
- Response: Array of LiveGame objects with odds data
- Updates: Every 5 seconds via odds fetcher
```

#### Alert Endpoints

```
GET /api/alerts/all
- Returns all active alerts
- Query params: user_id (optional)
- Response: {
    arbitrage: { count, alerts[] },
    steam_moves: { count, alerts[] },
    line_movements: { count, alerts[] }
  }
- Real-time detection of betting opportunities
```

```
GET /api/alerts/arbitrage
- Arbitrage opportunities only
- Includes stake calculations and profit projections
```

```
GET /api/alerts/steam-moves
- Steam move alerts only
- Includes consensus data and book movement lists
```

```
GET /api/alerts/line-movements
- Line movement alerts only
- Includes percentage change calculations
```

#### NHL-Specific Endpoints

```
GET /api/nhl/goalie-pulls
- Real-time goalie pull alerts
- WebSocket support for instant notifications
- Critical for live betting timing
```

### Data Models

**LiveGame Object:**
```typescript
interface LiveGame {
  state: {
    id: string;
    sport_key: string;
    sport_title: string;
    commence_time: string;
    home_team: string;
    away_team: string;
    status: 'live' | 'upcoming';
    tournament?: string; // Tennis only
  };
  bookmakers: Array<{
    key: string;
    title: string;
    markets: Array<{
      key: string;
      outcomes: Array<{
        name: string;
        price: number;
        point?: number;
      }>;
    }>;
  }>;
}
```

**Alert Objects:**
```typescript
interface ArbitrageAlert {
  game_id: string;
  sport: string;
  home_team: string;
  away_team: string;
  market_type: string;
  book_a: string;
  book_b: string;
  odds_a: number;
  odds_b: number;
  profit_percent: number;
  stake_a: number;
  stake_b: number;
  total_stake: number;
  guaranteed_profit: number;
  timestamp: string;
  expires_in: number;
}

interface SteamMoveAlert {
  game_id: string;
  sport: string;
  home_team: string;
  away_team: string;
  market_type: string;
  side: string;
  original_line: number;
  new_line: number;
  movement: number;
  books_moved: string[];
  consensus_percent: number;
  timestamp: string;
}

interface LineMovementAlert {
  game_id: string;
  sport: string;
  home_team: string;
  away_team: string;
  market_type: string;
  bookmaker: string;
  original_line: number;
  new_line: number;
  movement: number;
  movement_percent: number;
  timestamp: string;
}
```

## 📊 Data Flow

### Real-Time Updates Pipeline

1. **Odds Fetcher Service** (`odds_fetcher.py`)
   - Polls The Odds API every 5 seconds
   - Fetches live odds for all configured sports
   - Updates SQLite database with new data
   - Calculates EV and best odds

2. **Alert Detection Engine**
   - Continuously monitors odds changes
   - Identifies arbitrage opportunities
   - Detects steam moves (3+ books moving)
   - Tracks significant line movements
   - Stores alerts with expiration times

3. **Frontend Polling**
   - Games page: Polls `/api/games` every 5 seconds
   - Alerts page: Polls `/api/alerts/all` every 10 seconds
   - Auto-refresh toggleable by user
   - Manual refresh available

4. **WebSocket Support** (NHL Goalie Pulls)
   - Instant push notifications
   - Sub-second alert delivery
   - Critical for time-sensitive live betting

## 🎯 Key Features & Algorithms

### Expected Value (EV) Calculation

```python
def calculate_ev(odds, implied_probability, true_probability):
    """
    EV = (probability_of_winning * amount_won) - (probability_of_losing * amount_risked)
    """
    american_odds = odds
    if american_odds > 0:
        decimal_odds = (american_odds / 100) + 1
    else:
        decimal_odds = (100 / abs(american_odds)) + 1
    
    ev = (true_probability * (decimal_odds - 1)) - ((1 - true_probability) * 1)
    return ev * 100  # Return as percentage
```

### Kelly Criterion Bet Sizing

```python
def kelly_criterion(odds, win_probability, bankroll):
    """
    Kelly % = (bp - q) / b
    Where:
    - b = decimal odds - 1
    - p = probability of winning
    - q = probability of losing (1 - p)
    """
    decimal_odds = convert_to_decimal(odds)
    b = decimal_odds - 1
    p = win_probability
    q = 1 - p
    
    kelly_percent = (b * p - q) / b
    kelly_bet = bankroll * kelly_percent
    
    # Use fractional Kelly for safety
    return kelly_bet * 0.25  # Quarter Kelly
```

### Arbitrage Detection

```python
def find_arbitrage(game_odds):
    """
    Arbitrage exists when:
    (1/odds_a) + (1/odds_b) < 1
    """
    for book_a in game_odds:
        for book_b in game_odds:
            if book_a != book_b:
                for outcome_a in book_a.outcomes:
                    for outcome_b in book_b.outcomes:
                        if outcome_a.name != outcome_b.name:
                            implied_a = 1 / decimal_odds(outcome_a.price)
                            implied_b = 1 / decimal_odds(outcome_b.price)
                            
                            if implied_a + implied_b < 1:
                                profit = (1 / (implied_a + implied_b)) - 1
                                return create_arbitrage_alert(
                                    book_a, book_b,
                                    outcome_a, outcome_b,
                                    profit
                                )
```

### Steam Move Detection

```python
def detect_steam_move(line_history):
    """
    Steam move criteria:
    - 3+ books move in same direction
    - Movement > 0.5 points (spreads/totals) or 10% (moneyline)
    - Within 5-minute window
    - 70%+ consensus on one side
    """
    recent_moves = get_moves_last_5_min(line_history)
    
    if len(recent_moves) >= 3:
        direction = get_movement_direction(recent_moves)
        magnitude = calculate_avg_movement(recent_moves)
        consensus = calculate_consensus(recent_moves)
        
        if magnitude > threshold and consensus > 0.70:
            return create_steam_alert(recent_moves, consensus)
```

## 🔮 Future Roadmap

### Phase 1: Enhanced Analytics (Q1 2025)
- [ ] Historical odds tracking and charting
- [ ] Line movement graphs
- [ ] Betting history and P&L tracking
- [ ] Advanced EV calculators
- [ ] Custom alert threshold settings

### Phase 2: Machine Learning Integration (Q2 2025)
- [ ] Predictive models for line movements
- [ ] AI-powered arbitrage prediction
- [ ] Sharp money detection algorithms
- [ ] Game outcome probability models
- [ ] Automated bet recommendations

### Phase 3: Social Features (Q3 2025)
- [ ] User betting communities
- [ ] Shared betting strategies
- [ ] Leaderboards and competitions
- [ ] Expert picks integration
- [ ] Social proof for betting trends

### Phase 4: Mobile & Notifications (Q4 2025)
- [ ] React Native mobile app
- [ ] Push notifications for alerts
- [ ] SMS alerts for critical opportunities
- [ ] Apple Watch integration
- [ ] Android widget support

### Phase 5: Advanced Betting Tools
- [ ] Parlay optimizer
- [ ] Hedge calculator
- [ ] Middling opportunity finder
- [ ] Live betting automation tools
- [ ] API access for power users

## 🚀 Deployment

### Current Setup
- **Backend:** FastAPI server on port 8000
- **Frontend:** Vite dev server on port 5173
- **Database:** SQLite (local file)
- **Environment:** Development mode

### Production Deployment (Planned)
- **Backend:** Docker container on AWS ECS/Fargate
- **Frontend:** Vercel or Netlify CDN
- **Database:** PostgreSQL on AWS RDS
- **Caching:** Redis for real-time data
- **CDN:** CloudFront for static assets
- **Domain:** Custom domain with SSL

### Environment Variables
```bash
# Backend (.env)
ODDS_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./betting.db
CORS_ORIGINS=http://localhost:5173
SECRET_KEY=your_secret_key

# Frontend (.env)
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

## 📝 Development Guidelines

### Code Style
- **Python:** PEP 8, type hints, async/await patterns
- **TypeScript:** Strict mode, functional components, proper typing
- **React:** Hooks-based, no class components
- **CSS:** Tailwind utilities, minimal custom CSS

### Component Patterns
- Keep components small and focused
- Extract reusable logic to custom hooks
- Use Context for global state
- Prop drilling max 2 levels deep

### Performance Considerations
- Memoize expensive calculations
- Use React.memo for static components
- Implement virtual scrolling for large lists
- Lazy load images and components
- Debounce API calls

### Testing Strategy
- Unit tests for utility functions
- Integration tests for API endpoints
- E2E tests for critical user flows
- Manual testing for UI/UX

## 🐛 Known Issues & Technical Debt

### Current Issues
1. No persistent user sessions (uses default user)
2. SQLite may not scale for high traffic
3. No error boundaries in React app
4. Limited mobile responsiveness
5. No API rate limiting
6. No data validation on frontend inputs

### Technical Debt
1. Need to migrate to PostgreSQL
2. Implement proper authentication system
3. Add comprehensive error handling
4. Set up CI/CD pipeline
5. Add monitoring and logging
6. Implement data backup strategy

## 📚 Resources & Documentation

### External APIs
- **The Odds API:** https://the-odds-api.com/
  - Sports covered: 15+ major leagues
  - Update frequency: 5-second intervals
  - Data included: Live odds, spreads, totals, props

### Libraries & Frameworks
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **Tailwind CSS:** https://tailwindcss.com/
- **Vite:** https://vitejs.dev/

### Related Documentation Files
- `README.md` - Setup and installation
- `Live Betting System NBA.md` - NBA betting strategies
- `nba_betting_roadmap.guide.txt` - Development roadmap
- `SERVER_MIGRATION_GUIDE.md` - Deployment guide

## 🤝 Contributing

This is currently a private project. For questions or collaboration opportunities, please contact the project maintainer.

---

**Last Updated:** January 22, 2025  
**Version:** 2.0  
**Status:** Active Development
