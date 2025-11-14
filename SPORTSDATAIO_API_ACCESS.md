# Sports Data IO API Access Summary
## Generated: November 7, 2024

---

## ✅ FULL ACCESS (Premium Tier)

### NBA (National Basketball Association)
**Competition Feeds:**
- ✅ Teams (30 teams)
- ✅ Standings (by season)
- ✅ Games/Schedule (1,248 games for 2025 season)

**Betting Feeds:**
- ✅ Game Odds by Date (10+ sportsbooks)
- ✅ Alternate Market Lines (quarters, halves, alternate spreads)
- ✅ Live/In-Game Odds
- ✅ Player Props (633 props per game day)
- ✅ Futures (season-long bets)

**Player/Stats Feeds:**
- ✅ Player Season Stats (587 players)
- ✅ Team Season Stats (30 teams)
- ✅ Player Game Stats by Date (108 players per day)

---

### NHL (National Hockey League)
**Competition Feeds:**
- ✅ Teams (32 teams)
- ✅ Standings (by season)
- ✅ Games/Schedule (1,314 games for 2025 season)

**Betting Feeds:**
- ✅ Game Odds by Date (10+ sportsbooks)
- ✅ Alternate Market Lines (periods, alternate spreads)
- ✅ Player Props (1,218 props per game day)
- ✅ Futures (season-long bets)

**Player/Stats Feeds:**
- ✅ Player Season Stats (1,084 players)
- ✅ Team Season Stats (32 teams)

---

### CBB (College Basketball / NCAA)
**Competition Feeds:**
- ✅ Teams (1,322 teams)
- ✅ Games/Schedule (6,328 games for 2025 season)

**Betting Feeds:**
- ✅ Game Odds by Date (10+ sportsbooks)

**Player/Stats Feeds:**
- ✅ Player Season Stats (5,394 players)
- ✅ Team Season Stats (702 teams)
- ✅ Player Game Stats by Date (715 players per day)

---

## ❌ LIMITED ACCESS (Basic/Free Tier)

### NFL (National Football League)
**Available:**
- ✅ Teams (32 teams)

**NOT Available:**
- ❌ Scores/Games
- ❌ Standings
- ❌ Odds/Betting
- ❌ Player Stats
- ❌ Team Stats

**Note:** Only basic team roster data available. No stats or betting data.

---

### CFB (College Football)
**Available:**
- ✅ Teams (272 teams)

**NOT Available:**
- ❌ Scores/Games
- ❌ Standings
- ❌ Odds/Betting
- ❌ Player Stats
- ❌ Team Stats

**Note:** Only basic team roster data available. No stats or betting data.

---

## 📊 Data Coverage by Feed Type

### Competition Feeds
| Sport | Teams | Standings | Games/Schedule |
|-------|-------|-----------|----------------|
| NBA   | ✅ 30  | ✅ Yes    | ✅ 1,248       |
| NHL   | ✅ 32  | ✅ Yes    | ✅ 1,314       |
| CBB   | ✅ 1,322 | ❌ No   | ✅ 6,328       |
| NFL   | ✅ 32  | ❌ No     | ❌ No          |
| CFB   | ✅ 272 | ❌ No     | ❌ No          |

### Betting Feeds
| Sport | Game Odds | Player Props | Alternate Lines | Futures |
|-------|-----------|--------------|-----------------|---------|
| NBA   | ✅ Yes    | ✅ 633/day   | ✅ Yes          | ✅ Yes  |
| NHL   | ✅ Yes    | ✅ 1,218/day | ✅ Yes          | ✅ Yes  |
| CBB   | ✅ Yes    | ❌ No        | ❌ No           | ❌ No   |
| NFL   | ❌ No     | ❌ No        | ❌ No           | ❌ No   |
| CFB   | ❌ No     | ❌ No        | ❌ No           | ❌ No   |

### Player/Stats Feeds
| Sport | Player Season Stats | Team Stats | Player Game Stats |
|-------|--------------------|-----------|--------------------|
| NBA   | ✅ 587 players     | ✅ 30 teams | ✅ 108/day        |
| NHL   | ✅ 1,084 players   | ✅ 32 teams | ❌ No             |
| CBB   | ✅ 5,394 players   | ✅ 702 teams | ✅ 715/day       |
| NFL   | ❌ No              | ❌ No      | ❌ No             |
| CFB   | ❌ No              | ❌ No      | ❌ No             |

---

## 🔑 Key Endpoints by Sport

### NBA Endpoints
```
# Competition
GET /v3/nba/scores/json/teams
GET /v3/nba/scores/json/Standings/2025
GET /v3/nba/scores/json/Games/2025

# Betting
GET /v3/nba/odds/json/GameOddsByDate/2024-11-07
GET /v3/nba/odds/json/AlternateMarketGameOddsByDate/2024-11-07
GET /v3/nba/odds/json/LiveGameOddsByDate/2024-11-07
GET /v3/nba/odds/json/PlayerPropsByDate/2024-11-07
GET /v3/nba/odds/json/BettingFuturesBySeason/2025

# Stats
GET /v3/nba/stats/json/PlayerSeasonStats/2025
GET /v3/nba/stats/json/TeamSeasonStats/2025
GET /v3/nba/stats/json/PlayerGameStatsByDate/2024-11-07
```

### NHL Endpoints
```
# Competition
GET /v3/nhl/scores/json/Teams
GET /v3/nhl/scores/json/Standings/2025
GET /v3/nhl/scores/json/Games/2025

# Betting
GET /v3/nhl/odds/json/GameOddsByDate/2024-11-07
GET /v3/nhl/odds/json/AlternateMarketGameOddsByDate/2024-11-07
GET /v3/nhl/odds/json/PlayerPropsByDate/2024-11-07
GET /v3/nhl/odds/json/BettingFuturesBySeason/2025

# Stats
GET /v3/nhl/stats/json/PlayerSeasonStats/2025
GET /v3/nhl/stats/json/TeamSeasonStats/2025
```

### CBB Endpoints
```
# Competition
GET /v3/cbb/scores/json/Teams
GET /v3/cbb/scores/json/Games/2025

# Betting
GET /v3/cbb/odds/json/GameOddsByDate/2024-11-07

# Stats
GET /v3/cbb/stats/json/PlayerSeasonStats/2025
GET /v3/cbb/stats/json/TeamSeasonStats/2025
GET /v3/cbb/stats/json/PlayerGameStatsByDate/2024-11-07
```

---

## 💡 Recommendations

### Immediate Integration Priority
1. **NBA** - Full suite of data available, highest priority
   - Game odds + player props (massive edge potential)
   - Player/team stats for predictions
   - Alternate lines for middle opportunities

2. **NHL** - Full betting + stats suite
   - Player props (1,200+ per day!)
   - Game odds and alternate lines
   - Full season stats

3. **CBB** - Good coverage but limited betting
   - 1,300+ teams, 6,300+ games
   - Game odds available
   - Player/team stats for predictions

### Future Considerations
- **NFL/CFB**: Limited to teams only. Consider upgrading subscription or using alternative data sources for football.

---

## 📈 Business Value

### High-Value Data You're NOT Using Yet:
1. **Player Props** (NBA: 633/day, NHL: 1,218/day)
   - Massive arbitrage opportunities
   - EV+ props based on player stats
   - Injury-based edges

2. **Alternate Lines** (NBA, NHL)
   - Middle opportunities
   - Reduced-juice lines
   - Quarter/period betting

3. **Live Odds** (NBA)
   - In-game betting opportunities
   - Regression to mean plays
   - Momentum shifts

4. **Player Stats** (5,394 CBB players!)
   - Build player prop models
   - Matchup advantages
   - Usage rate edges

---

**Next Steps:** Build comprehensive Sports Data IO client to leverage ALL available data across NBA, NHL, and CBB.
