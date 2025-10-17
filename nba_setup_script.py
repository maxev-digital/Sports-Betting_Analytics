#!/usr/bin/env python3
"""
NBA Live Betting System Setup Script
Creates complete folder structure and files
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = r"C:\Users\nashr\backend\scrapers\nba"

# File contents
FILES = {
    # Backend files
    "backend/config.py": '''"""Configuration for NBA Live Betting System"""
import os

# Odds API
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "3b91452fcbaa6deffecb2e5843655099")
ODDS_API_BASE = "https://api.the-odds-api.com/v4"
SPORT = "basketball_nba"
REGION = "us"
MARKET = "totals"

# Polling
POLL_INTERVAL = 15  # seconds

# Edge detection
MIN_EDGE = 5.0  # points
''',

    "backend/models.py": '''"""Pydantic models for type safety"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Team(BaseModel):
    name: str
    score: Optional[int] = None

class GameState(BaseModel):
    id: str
    home_team: Team
    away_team: Team
    commence_time: datetime
    status: str  # 'upcoming', 'live', 'final'
    quarter: Optional[int] = None
    time_remaining: Optional[str] = None  # "5:23" format
    
class GameOdds(BaseModel):
    bookmaker: str
    total: float
    over_price: int
    under_price: int
    
class GameProjection(BaseModel):
    current_total: int
    projected_final: float
    pregame_total: float
    current_live_total: Optional[float] = None
    edge: Optional[float] = None
    confidence: str  # 'LOW', 'MEDIUM', 'HIGH'
    recommendation: Optional[str] = None  # 'OVER', 'UNDER', None

class LiveGame(BaseModel):
    state: GameState
    odds: list[GameOdds]
    projection: GameProjection
''',

    "backend/requirements.txt": '''fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.1
pydantic==2.5.0
python-dotenv==1.0.0
''',

    "backend/odds_client.py": '''"""Odds API Client"""
import httpx
from typing import List
from models import GameState, GameOdds, Team
from config import ODDS_API_KEY, ODDS_API_BASE, SPORT, REGION, MARKET
import logging

logger = logging.getLogger(__name__)

class OddsAPIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.base_url = ODDS_API_BASE
        
    async def get_live_games(self) -> List[dict]:
        """Fetch all NBA games with odds"""
        url = f"{self.base_url}/sports/{SPORT}/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": REGION,
            "markets": MARKET,
            "oddsFormat": "american"
        }
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            # Log API usage
            remaining = response.headers.get('x-requests-remaining', 'unknown')
            logger.info(f"API requests remaining: {remaining}")
            
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching odds: {e}")
            return []
    
    async def get_game_scores(self) -> dict:
        """Fetch live scores from Odds API"""
        url = f"{self.base_url}/sports/{SPORT}/scores"
        params = {
            "apiKey": ODDS_API_KEY,
            "daysFrom": 1
        }
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return {game['id']: game for game in response.json()}
        except Exception as e:
            logger.error(f"Error fetching scores: {e}")
            return {}
    
    async def close(self):
        await self.client.aclose()
''',

    "backend/projector.py": '''"""Game projection algorithm"""
from models import GameState, GameProjection
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class GameProjector:
    """Simple projection algorithm - v1"""
    
    @staticmethod
    def calculate_time_elapsed_seconds(quarter: int, time_remaining: str) -> int:
        """Calculate seconds elapsed in game"""
        QUARTER_LENGTH = 720  # 12 minutes in seconds
        
        # Parse time_remaining "5:23" -> 323 seconds
        try:
            parts = time_remaining.split(":")
            minutes = int(parts[0])
            seconds = int(parts[1])
            remaining_in_quarter = (minutes * 60) + seconds
        except:
            remaining_in_quarter = QUARTER_LENGTH / 2
        
        # Calculate elapsed
        if quarter <= 4:
            elapsed = ((quarter - 1) * QUARTER_LENGTH) + (QUARTER_LENGTH - remaining_in_quarter)
        else:
            # Overtime
            regular_time = 4 * QUARTER_LENGTH
            ot_time = (quarter - 4) * 300
            elapsed = regular_time + ot_time + (300 - remaining_in_quarter)
        
        return elapsed
    
    @staticmethod
    def project_final_total(
        current_score: int,
        time_elapsed_seconds: int,
        pregame_total: float,
        quarter: int
    ) -> GameProjection:
        """Project final total using pace-based model"""
        TOTAL_GAME_TIME = 2880  # 48 minutes
        
        # Calculate current pace
        if time_elapsed_seconds > 0:
            current_pace_total = (current_score / time_elapsed_seconds) * TOTAL_GAME_TIME
        else:
            current_pace_total = pregame_total
        
        # Weight based on quarter
        if quarter == 1:
            projected = (0.7 * pregame_total) + (0.3 * current_pace_total)
            confidence = "LOW"
        elif quarter == 2:
            projected = (0.5 * pregame_total) + (0.5 * current_pace_total)
            confidence = "MEDIUM"
        elif quarter == 3:
            projected = (0.3 * pregame_total) + (0.7 * current_pace_total)
            confidence = "MEDIUM"
        else:
            projected = (0.2 * pregame_total) + (0.8 * current_pace_total)
            confidence = "HIGH"
        
        return GameProjection(
            current_total=current_score,
            projected_final=round(projected, 1),
            pregame_total=pregame_total,
            confidence=confidence
        )
    
    @staticmethod
    def calculate_edge(
        projected_total: float,
        live_total: Optional[float],
        pregame_total: float
    ) -> tuple[Optional[float], Optional[str]]:
        """Calculate edge and recommendation"""
        if live_total is None:
            live_total = pregame_total
        
        edge = abs(projected_total - live_total)
        
        if edge >= 5.0:
            if projected_total > live_total:
                recommendation = "OVER"
            else:
                recommendation = "UNDER"
            return round(edge, 1), recommendation
        
        return None, None
''',

    "backend/game_tracker.py": '''"""Game tracking and state management"""
from models import GameState, LiveGame, GameOdds, Team, GameProjection
from odds_client import OddsAPIClient
from projector import GameProjector
from typing import Dict, List
import asyncio
import logging

logger = logging.getLogger(__name__)

class GameTracker:
    def __init__(self):
        self.odds_client = OddsAPIClient()
        self.projector = GameProjector()
        self.games: Dict[str, LiveGame] = {}
        self.running = False
        
    async def start(self):
        """Start tracking games"""
        self.running = True
        while self.running:
            try:
                await self.update_games()
                await asyncio.sleep(15)  # Poll every 15 seconds
            except Exception as e:
                logger.error(f"Error in game tracker: {e}")
                await asyncio.sleep(5)
    
    async def update_games(self):
        """Fetch and update all games"""
        logger.info("Updating games...")
        
        # Fetch odds and scores
        odds_data = await self.odds_client.get_live_games()
        scores_data = await self.odds_client.get_game_scores()
        
        new_games = {}
        
        for game_data in odds_data:
            game_id = game_data['id']
            
            # Parse odds
            bookmakers = game_data.get('bookmakers', [])
            odds_list = []
            pregame_total = None
            
            for book in bookmakers:
                for market in book.get('markets', []):
                    if market['key'] == 'totals':
                        outcomes = market['outcomes']
                        over_outcome = next((o for o in outcomes if o['name'] == 'Over'), None)
                        under_outcome = next((o for o in outcomes if o['name'] == 'Under'), None)
                        
                        if over_outcome:
                            odds_list.append(GameOdds(
                                bookmaker=book['title'],
                                total=over_outcome['point'],
                                over_price=over_outcome['price'],
                                under_price=under_outcome['price'] if under_outcome else 0
                            ))
                            if pregame_total is None:
                                pregame_total = over_outcome['point']
            
            if not odds_list:
                continue
            
            # Parse game state
            score_info = scores_data.get(game_id, {})
            home_score = score_info.get('scores', [{}])[0].get('score')
            away_score = score_info.get('scores', [{}])[1].get('score') if len(score_info.get('scores', [])) > 1 else None
            
            is_live = score_info.get('completed') == False and home_score is not None
            
            game_state = GameState(
                id=game_id,
                home_team=Team(name=game_data['home_team'], score=home_score),
                away_team=Team(name=game_data['away_team'], score=away_score),
                commence_time=game_data['commence_time'],
                status='live' if is_live else 'upcoming',
                quarter=2 if is_live else None,  # TODO: Parse from API
                time_remaining="5:23" if is_live else None  # TODO: Parse from API
            )
            
            # Calculate projection
            if game_state.status == 'live' and game_state.quarter and game_state.time_remaining:
                current_score = (game_state.home_team.score or 0) + (game_state.away_team.score or 0)
                time_elapsed = self.projector.calculate_time_elapsed_seconds(
                    game_state.quarter,
                    game_state.time_remaining
                )
                
                projection = self.projector.project_final_total(
                    current_score,
                    time_elapsed,
                    pregame_total,
                    game_state.quarter
                )
                
                # Get current live total
                if odds_list:
                    avg_live_total = sum(o.total for o in odds_list) / len(odds_list)
                    projection.current_live_total = avg_live_total
                    
                    # Calculate edge
                    edge, recommendation = self.projector.calculate_edge(
                        projection.projected_final,
                        avg_live_total,
                        pregame_total
                    )
                    projection.edge = edge
                    projection.recommendation = recommendation
            else:
                projection = GameProjection(
                    current_total=0,
                    projected_final=pregame_total,
                    pregame_total=pregame_total,
                    confidence="LOW"
                )
            
            new_games[game_id] = LiveGame(
                state=game_state,
                odds=odds_list,
                projection=projection
            )
        
        self.games = new_games
        logger.info(f"Updated {len(self.games)} games")
    
    async def stop(self):
        """Stop tracking"""
        self.running = False
        await self.odds_client.close()
    
    def get_all_games(self) -> List[LiveGame]:
        """Get all tracked games"""
        return list(self.games.values())
    
    def get_game(self, game_id: str) -> LiveGame:
        """Get specific game"""
        return self.games.get(game_id)
''',

    "backend/main.py": '''"""FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from game_tracker import GameTracker
from models import LiveGame
from typing import List
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NBA Live Betting API")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game tracker instance
tracker = GameTracker()

@app.on_event("startup")
async def startup():
    """Start game tracking on app startup"""
    logger.info("Starting NBA Live Betting API...")
    asyncio.create_task(tracker.start())

@app.on_event("shutdown")
async def shutdown():
    """Stop tracking on shutdown"""
    await tracker.stop()

@app.get("/")
async def root():
    return {"message": "NBA Live Betting API", "status": "running"}

@app.get("/api/games", response_model=List[LiveGame])
async def get_games():
    """Get all live games"""
    return tracker.get_all_games()

@app.get("/api/games/{game_id}", response_model=LiveGame)
async def get_game(game_id: str):
    """Get specific game"""
    game = tracker.get_game(game_id)
    if not game:
        return {"error": "Game not found"}
    return game

@app.get("/api/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "games_tracked": len(tracker.games)
    }
''',

    "README.md": '''# NBA Live Betting System

## Setup Instructions

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Set API Key (Optional)
```bash
export ODDS_API_KEY=your_key_here
```

### 3. Start Backend
```bash
cd backend
uvicorn main:app --reload
```

### 4. Test Endpoints
- http://localhost:8000/ - API info
- http://localhost:8000/api/games - All games
- http://localhost:8000/api/health - Health check

### 5. Setup Frontend (Later)
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
nba-live-betting/
├── backend/           # FastAPI backend
│   ├── main.py       # API endpoints
│   ├── game_tracker.py
│   ├── odds_client.py
│   ├── projector.py
│   ├── models.py
│   └── config.py
└── frontend/         # React frontend (to be built)
```

## Features

- ✅ Fetches live NBA odds
- ✅ Calculates game projections
- ✅ Detects betting edges (5+ points)
- ✅ Auto-updates every 15 seconds
- ✅ REST API for frontend
''',

    ".gitignore": '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
.env

# Node
node_modules/
dist/
.cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
'''
}

def create_structure():
    """Create complete folder structure and files"""
    print("=" * 70)
    print("NBA LIVE BETTING SYSTEM - SETUP")
    print("=" * 70)
    print(f"\nBase directory: {BASE_DIR}")
    print()
    
    # Create base directory
    base_path = Path(BASE_DIR)
    base_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created base directory: {BASE_DIR}")
    
    # Create additional directories
    dirs = [
        "backend",
        "frontend",
        "frontend/src",
        "frontend/src/components",
        "frontend/src/lib"
    ]
    
    for dir_name in dirs:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_name}")
    
    print()
    
    # Create files
    print("Creating files...")
    for file_path, content in FILES.items():
        full_path = base_path / file_path
        
        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {file_path}")
    
    print()
    print("=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print(f"1. cd {BASE_DIR}\\backend")
    print("2. pip install -r requirements.txt")
    print("3. uvicorn main:app --reload")
    print()
    print("Then test:")
    print("  http://localhost:8000/")
    print("  http://localhost:8000/api/games")
    print("  http://localhost:8000/api/health")
    print()
    print("=" * 70)

if __name__ == "__main__":
    create_structure()
