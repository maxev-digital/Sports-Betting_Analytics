# Monte Carlo Simulation Integration Plan

## Status
Monte Carlo simulation API is working (`/api/simulation/monte-carlo`) and has been deployed to production.

## What's Missing
The frontend components exist but aren't fully integrated with GameCard:

1. **SimulationModal.tsx** - Exists but doesn't pass team stats to the simulation
2. **GameCard.tsx** - Doesn't have a button to trigger the simulation
3. **useMonteCarloSimulation hook** - Updated to accept team stats, but SimulationModal needs to use them

## Required Changes

### 1. Update SimulationModal.tsx
**Location**: `frontend/src/components/SimulationModal.tsx`

**Problem**: Lines 42-46 call `runSimulation()` but don't pass team stats

**Fix**: Add team stats from the game prop:

```typescript
// In SimulationModal, around line 42-46:
runSimulation({
  game_id: game.state.id,
  current_state: currentState,
  home_stats: game.home_stats ? {
    pace: game.home_stats.pace,
    off_rating: game.home_stats.off_rating,
    def_rating: game.home_stats.def_rating,
  } : undefined,
  away_stats: game.away_stats ? {
    pace: game.away_stats.pace,
    off_rating: game.away_stats.off_rating,
    def_rating: game.away_stats.def_rating,
  } : undefined,
  market_total: game.markets?.totals?.over_under,
  n_simulations: 10000,
});
```

**Update interface** around line 5-25 to include team stats:
```typescript
interface SimulationModalProps {
  isOpen: boolean;
  onClose: () => void;
  game: {
    state: {
      id: string;
      home_team: string;
      away_team: string;
      home_score?: number;
      away_score?: number;
      period?: string;
      time_remaining?: string;
      status: 'live' | 'upcoming';
    };
    markets?: {
      totals?: {
        over_under: number;
      };
    };
    home_stats?: {
      pace: number;
      off_rating: number;
      def_rating: number;
    };
    away_stats?: {
      pace: number;
      off_rating: number;
      def_rating: number;
    };
  };
}
```

### 2. Add Simulation Button to GameCard.tsx
**Location**: `frontend/src/components/GameCard.tsx`

**What to Add**:

1. **Import SimulationModal** at top of file (around line 1-13):
```typescript
import { SimulationModal } from './SimulationModal';
```

2. **Add state for modal** in GameCard component (find where useState is used):
```typescript
const [showSimulation, setShowSimulation] = useState(false);
```

3. **Add simulation button** - Find where the "Analytics" or "Advanced Systems" buttons are and add this button nearby:
```typescript
<button
  onClick={() => setShowSimulation(true)}
  className="px-3 py-1.5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-lg font-semibold transition-all duration-200 flex items-center gap-2 shadow-lg"
>
  <span>🎲</span>
  <span>Monte Carlo</span>
</button>
```

4. **Add SimulationModal component** at the end of the GameCard return statement (before the closing `</div>`):
```typescript
<SimulationModal
  isOpen={showSimulation}
  onClose={() => setShowSimulation(false)}
  game={{
    state: game.state,
    markets: {
      totals: {
        over_under: game.odds?.[0]?.totals?.over_under || 0
      }
    },
    home_stats: game.home_team_stats,
    away_stats: game.away_team_stats,
  }}
/>
```

## Testing
1. Start frontend: `cd frontend && npm run dev`
2. Backend should already be running on port 8000
3. Go to Live Games page
4. Click "Monte Carlo" button on any game card
5. Should see simulation running with 10,000 iterations
6. Results should show probability distributions, EV calculations, Kelly sizing

## Known Issues
- Monte Carlo simulator was designed for basketball (NBA/NCAAB)
- Other sports (NFL, NHL) may show incorrect totals due to different scoring systems
- For now, focus on NBA/NCAAB games for testing

## API Endpoint
`POST /api/simulation/monte-carlo`

Request:
```json
{
  "game_id": "nba_20251110_LAL_BOS",
  "current_state": {
    "quarter": 3,
    "time_remaining": "4:32",
    "home_score": 82,
    "away_score": 78
  },
  "home_stats": {
    "pace": 100.5,
    "off_rating": 118.2,
    "def_rating": 110.5
  },
  "away_stats": {
    "pace": 98.3,
    "off_rating": 115.8,
    "def_rating": 108.9
  },
  "market_total": 235.5,
  "n_simulations": 10000
}
```

Response: See `backend/routes/simulation.py` for full response structure
