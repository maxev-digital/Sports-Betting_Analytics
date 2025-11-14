# STRATEGY INPUT DEFINITIONS FOR WIN RATE VERIFICATION

This document defines the required inputs for each of the 25 betting strategies to calculate accurate win rates, ROI, and EV.

---

## 📋 INPUT TEMPLATE (For Each Strategy)

For accurate backtest calculations, we need:

1. **Strategy ID & Name**
2. **Trigger Logic** - When does the strategy fire?
3. **Applicable Sports & Leagues** - NBA, NFL, NHL, NCAA, MLB
4. **Backtest Date Range** - Which seasons to analyze
5. **Data Sources** - Where to pull game data from
6. **Odds Source** - Where to get betting odds
7. **Outcome Metric** - What defines a "win"
8. **Current Status** - Real data vs Mock data
9. **Known Win Rate** (if verified)
10. **Known Sample Size** (if verified)

---

## ✅ STRATEGIES WITH VERIFIED DATA (3)

### **Strategy #6: Goalie Pull Alert**

**Status:** ✅ VERIFIED - Real Moneypuck Data

| Field | Value |
|-------|-------|
| **Trigger Logic** | Trailing team pulls goalie with 3+ minutes remaining |
| **Sports** | NHL only |
| **Date Range** | 2023-24 NHL Season (Oct 2023 - Apr 2024) |
| **Data Source** | Moneypuck.com - Goalie pull database |
| **Odds Source** | N/A (betting on "at least 1 goal scored") |
| **Outcome Metric** | Did trailing team score ≥1 goal after pulling goalie? |
| **Sample Size** | 581 goalie pulls |
| **Win Rate** | 80.4% (467 wins, 114 losses, 0 pushes) |
| **ROI** | 55.2% |

**ChatGPT Query:**
```
Pull all NHL 2023-24 season games from Moneypuck.com where trailing team pulled goalie with 3+ minutes remaining. Count how many times the trailing team scored at least 1 goal vs scored 0 goals. Calculate win rate and ROI assuming -110 odds.
```

---

### **Strategy #14: Quarter Reversal Strategy**

**Status:** ✅ VERIFIED - Real balldontlie.io Data

| Field | Value |
|-------|-------|
| **Trigger Logic** | Team wins 2 consecutive quarters, bet opponent to win next quarter |
| **Sports** | NBA only |
| **Date Range** | 2023-24 NBA Season (Oct 2023 - Jun 2024) |
| **Data Source** | balldontlie.io API - Quarter-by-quarter scores |
| **Odds Source** | Historical quarter spread lines (assume -110) |
| **Outcome Metric** | Did opponent win the next quarter? |
| **Sample Size** | 1,230 opportunities (669 wins, 511 losses, 50 pushes) |
| **Win Rate** | 54.4% |
| **ROI** | 13.6% (disputed - calculate as 7.9% at -110) |

**Three Sub-Scenarios:**
- **Q1-Q2 → Q3:** Team wins Q1 & Q2, bet opponent Q3 (55.3% win rate, +12.1% ROI)
- **Q2-Q3 → Q4:** Team wins Q2 & Q3, bet opponent Q4 (52.7% win rate, +8.9% ROI)
- **Q3-Q4 → OT:** Team wins Q3 & Q4, bet opponent OT (60.7% win rate, +35.2% ROI)

**ChatGPT Query:**
```
For 2023-24 NBA season, identify all games where a team won 2 consecutive quarters. For each scenario (Q1-Q2→Q3, Q2-Q3→Q4, Q3-Q4→OT), track if the opponent won the following quarter. Calculate win rates and ROI at -110 odds for each scenario and overall.
```

---

### **Strategy #8: End-Game Unders**

**Status:** ⚠️ NEEDS REVISION - Real Data But Losing Strategy

| Field | Value |
|-------|-------|
| **Trigger Logic** | Game has 15+ point differential after Q3, bet Q4 under |
| **Sports** | NBA only |
| **Date Range** | 2023-24 NBA Season |
| **Data Source** | ESPN API - Quarter scores |
| **Odds Source** | Historical Q4 total lines |
| **Outcome Metric** | Did Q4 total go under the line? |
| **Sample Size** | 1,160 Q4 situations (413 wins, 700 losses, 47 pushes) |
| **Win Rate** | 35.6% ❌ |
| **ROI** | -28.0% ❌ |

**Issues:** Strategy is losing money - needs refinement or removal

**ChatGPT Query:**
```
For 2023-24 NBA season, identify games with 15+ point differential after Q3. Get Q4 total betting line and actual Q4 score. Calculate under bet win rate. If under 50%, revise trigger conditions (try 20+ point differential, or Q3 + Q4 combined).
```

---

## 🔄 STRATEGIES NEEDING VERIFICATION (22)

### **Strategy #1: The Hot-Shooting Fade**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Team shoots 15%+ above season average in previous game |
| **Sports** | NBA, NCAA Basketball |
| **Date Range** | ❓ Need to define (suggest: 2022-23 + 2023-24 seasons) |
| **Data Source** | ❓ NBA: stats.nba.com or balldontlie.io / NCAA: Sports Reference |
| **Odds Source** | ❓ Historical spreads or totals |
| **Outcome Metric** | ❓ Does opposing team cover spread? Or game total goes under? |
| **Current Status** | Mock data (56.1% win rate, 280 bets) |

**What We Need:**
1. Define "unusually hot shooting" threshold (15%? 20%?)
2. Bet type: Fade team spread? Bet opponent spread? Bet under?
3. How many days lookback (previous game only? Last 3 games?)

**ChatGPT Query to Define:**
```
For 2022-24 NBA seasons, identify games where Team A shot ≥15% above their season FG% average. In their NEXT game, track:
- Team A's performance (win/loss, point differential)
- Opposing team spread coverage
- Game total vs season average
Determine optimal bet type (fade team, bet opponent, or under).
```

---

### **Strategy #2: Momentum Shift Betting**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Bet on team immediately after key event (ejection, injury timeout, flagrant foul) |
| **Sports** | NBA, NFL, NHL |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Play-by-play data with event tagging |
| **Odds Source** | ❓ Live odds API (The Odds API, FanDuel API) |
| **Outcome Metric** | ❓ Does team cover next-quarter spread? Win rest of game? |
| **Current Status** | Mock data (52.5% win rate, 297 bets) |

**What We Need:**
1. Define "key events" specifically (ejection only? All flagrants? Star player injury?)
2. Timing window (bet immediately within 30 seconds? 1 minute?)
3. Which team to bet (affected team or opponent?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify all player ejections and flagrant fouls. Track score differential before/after event (next 5 minutes). Determine if affected team or opponent benefits. Test betting opponent's next-quarter spread.
```

---

### **Strategy #3: Injury Cascade Props**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Star player exits mid-game, bet role player props to go over |
| **Sports** | NBA, NFL |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Injury reports + play-by-play (when star exits) |
| **Odds Source** | ❓ Live player props (FanDuel, DraftKings) |
| **Outcome Metric** | ❓ Does replacement player exceed over on points/rebounds/assists? |
| **Current Status** | Mock data (53.4% win rate, 191 bets) |

**What We Need:**
1. Define "star player" (All-Star? Team's leading scorer?)
2. Which props to bet (points only? Rebounds? All?)
3. Which replacement players qualify (immediate substitute? All bench?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify games where team's leading scorer exited early (<30 minutes played). Track substitute player's performance vs their season averages. Identify which prop types (PTS, REB, AST) exceeded averages most frequently.
```

---

### **Strategy #4: The Pace Trap**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Slow-paced team (rank 25-30) trails by 10+ points, bet over |
| **Sports** | NBA, NCAA Basketball |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Live scores + team pace rankings |
| **Odds Source** | ❓ Live total lines |
| **Outcome Metric** | ❓ Does game total go over? Or 2H total? |
| **Current Status** | Mock data (54.7% win rate, 373 bets) |

**What We Need:**
1. Define deficit threshold (10+ points? 12+? 15+?)
2. When to trigger (after Q1? Q2? Halftime?)
3. Bet type (full game over? 2H over? Q3/Q4 over?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify slowest 6 teams by pace. Find games where they trailed by 10+ points at halftime. Compare actual 2H pace vs season average. Calculate 2H over bet win rate.
```

---

### **Strategy #5: Foul Trouble Overs**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Elite defender picks up 2-3 fouls in Q1, bet opponent team total over |
| **Sports** | NBA, NCAA Basketball |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Play-by-play foul tracking |
| **Odds Source** | ❓ Live team totals |
| **Outcome Metric** | ❓ Does opponent team exceed their total? |
| **Current Status** | Mock data (53.6% win rate, 276 bets) |

**What We Need:**
1. Define "elite defender" (All-Defense team? DRTG top 20?)
2. Foul threshold (2 fouls in Q1? 3 by halftime?)
3. Bet timing (immediately? Wait until defender benched?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify top 20 defenders by DRTG. Track games where they picked up 2+ fouls in Q1. Measure opponent scoring differential with defender on vs off court. Calculate opponent team total over win rate.
```

---

### **Strategy #7: Blowout Contrarian Spreads**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Underdog down 20-25 at halftime but "showing fight", bet 2H spread |
| **Sports** | NBA, NFL |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Halftime scores |
| **Odds Source** | ❓ 2H spread lines |
| **Outcome Metric** | ❓ Does underdog cover 2H spread? |
| **Current Status** | Mock data (52.6% win rate, 251 bets) |

**What We Need:**
1. Define "showing fight" (within 15 in Q2? Positive Q2 margin?)
2. Deficit range (20-25 points? 15-30?)
3. Bet type (2H spread? 2H moneyline?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, find games where underdog trailed by 20-25 at halftime. Segment by Q2 performance (positive vs negative margin). Calculate 2H spread coverage rate for each segment.
```

---

### **Strategy #9: Overtime Total Resets**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Regulation goes way over, bet OT under |
| **Sports** | NBA, NFL, NHL |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Regulation totals |
| **Odds Source** | ❓ OT total lines |
| **Outcome Metric** | ❓ Does OT total go under? |
| **Current Status** | Mock data (52.1% win rate, 213 bets) |

**What We Need:**
1. Define "way over" (10+ points? 15+? Percentage?)
2. Sport-specific OT rules (NBA 5min, NFL 10min, NHL 5min)
3. Bet type (OT total under? Or avoid betting?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify OT games where regulation went 10+ points over the total. Track OT scoring vs expected (1/10th of regulation pace). Calculate OT under win rate.
```

---

### **Strategy #10: Fatigue Spreads (Back-to-Backs)**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Team on 2nd night of B2B vs rested opponent, fade B2B team |
| **Sports** | NBA, NHL |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Schedule data (rest days) |
| **Odds Source** | ❓ Spread lines |
| **Outcome Metric** | ❓ Does rested team cover spread? |
| **Current Status** | Mock data (55.6% win rate, 205 bets) |

**What We Need:**
1. Home vs away impact (worse on road B2B?)
2. Travel distance factor (cross-country flight?)
3. Bet type (spread? Moneyline? Total under?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, find games where Team A played B2B and Team B had 2+ days rest. Segment by home/away and travel distance. Calculate spread coverage, moneyline, and under rates.
```

---

### **Strategy #11: Coaching Timeout Value**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Team burns all timeouts early, bet against them late game |
| **Sports** | NBA, NFL |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Play-by-play timeout tracking |
| **Odds Source** | ❓ Live spreads/moneylines |
| **Outcome Metric** | ❓ Does opponent win Q4 or close margin? |
| **Current Status** | Mock data (51.4% win rate, 105 bets) |

**What We Need:**
1. Define "early" (all timeouts by Q3? By halftime?)
2. Game situation (close game only? Any?)
3. Bet type (Q4 spread? Moneyline?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify teams that used all timeouts before start of Q4. Track Q4 performance vs opponent. Measure win rate and point differential in close games (<5 points entering Q4).
```

---

### **Strategy #12: Weather-Driven Live Totals**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Sudden weather change (rain, wind, snow), bet under |
| **Sports** | NFL, MLB |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Weather API + live scores |
| **Odds Source** | ❓ Live totals |
| **Outcome Metric** | ❓ Does game go under? |
| **Current Status** | Mock data (52.7% win rate, 226 bets) |

**What We Need:**
1. Weather thresholds (wind >15mph? Rain >0.1in/hr?)
2. Sport-specific impacts (NFL wind vs MLB rain)
3. Bet timing (pregame? Live during weather change?)

**ChatGPT Query to Define:**
```
For 2023 NFL season, get weather data for all outdoor games. Identify games with wind >15mph or rain. Calculate under win rate vs games with calm weather. Test different wind/rain thresholds.
```

---

### **Strategy #13: Favorite Comeback Detection**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Favorite trails underdog after underdog hot start, bet favorite |
| **Sports** | NBA |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Quarter scores + team rankings |
| **Odds Source** | ❓ Live spreads/moneylines |
| **Outcome Metric** | ❓ Does favorite cover 2H spread? Win game? |
| **Current Status** | Mock data (55.0% win rate, 231 bets) |

**What We Need:**
1. Define "favorite" (betting favorite? Better record?)
2. Define "hot start" (up 10+ after Q1? 15+ at half?)
3. Talent gap minimum (5+ PPG differential?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, find games where betting favorite trailed by 10+ after Q1. Measure 2H performance and spread coverage. Segment by talent gap (point differential in season averages).
```

---

### **Strategy #15: Line Movement Arbitrage**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Line moves 2+ points, bet middle opportunity |
| **Sports** | NBA, NFL, NHL, MLB |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Historical line movement data |
| **Odds Source** | ❓ Multiple sportsbooks |
| **Outcome Metric** | ❓ Does result land in middle? Or win both bets? |
| **Current Status** | Mock data (55.5% win rate, 247 bets) |

**What We Need:**
1. Line movement threshold (2 points? 3 points? 5%?)
2. Timing (how fast must it move? Minutes? Hours?)
3. Profit calculation (middle wins + one-side wins)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, track spread line movements from open to close. Identify games with 2+ point moves. Calculate middle opportunity hit rate and expected profit vs vig cost.
```

---

### **Strategy #16: Middle Opportunity Detection**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Spread discrepancy between books ≥2 points, bet both sides |
| **Sports** | NBA, NFL, NHL, MLB |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Real-time odds comparison |
| **Odds Source** | ❓ Multiple sportsbooks |
| **Outcome Metric** | ❓ Does result land in middle? Net profit after vig? |
| **Current Status** | Mock data (57.6% win rate, 340 bets) |

**What We Need:**
1. Book combinations to monitor (how many books?)
2. Minimum spread gap (2 points? 2.5?)
3. Middle hit rate target (>15% to be profitable)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, compare spreads across 5+ sportsbooks per game. Identify games with 2+ point discrepancies. Calculate middle hit rate and ROI after vig (assume -110 both sides).
```

---

### **Strategy #17: Sharp Money Tracking**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Line moves against public betting percentage (reverse line movement) |
| **Sports** | NBA, NFL, NHL, MLB |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Public betting % + line movement data |
| **Odds Source** | ❓ Sportsbook line histories |
| **Outcome Metric** | ❓ Does "sharp" side cover? |
| **Current Status** | Mock data (53.0% win rate, 117 bets) |

**What We Need:**
1. Reverse line movement definition (line moves 1+ point against 60%+ public?)
2. Timing (track movement over what window?)
3. Sport-specific thresholds

**ChatGPT Query to Define:**
```
For 2023-24 NFL season, get public betting percentages from Action Network. Identify reverse line movements (line moves toward side with <40% public bets). Calculate cover rate for sharp side.
```

---

### **Strategy #18: CLV Tracker (Closing Line Value)**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Bet early line, measure value vs closing line |
| **Sports** | NBA, NFL, NHL, MLB |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Opening + closing lines |
| **Odds Source** | ❓ Historical odds database |
| **Outcome Metric** | ❓ Positive CLV AND bet wins |
| **Current Status** | Mock data (52.4% win rate, 189 bets) |

**What We Need:**
1. When to bet (opening line? 24 hours before? 12 hours?)
2. Minimum CLV threshold (0.5 points? 1 point?)
3. Which direction (bet opening favorites? Underdogs? Both?)

**ChatGPT Query to Define:**
```
For 2023-24 NFL season, compare opening lines to closing lines. Bet opening line and measure CLV. Calculate win rate for bets with +1.0 or better CLV vs negative CLV.
```

---

### **Strategy #19: Home/Away Splits Strategy**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Team with extreme home/away split is away (or home), bet accordingly |
| **Sports** | NBA, NFL, NHL, MLB |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Team season splits |
| **Odds Source** | ❓ Game lines |
| **Outcome Metric** | ❓ Does extreme split team cover? |
| **Current Status** | Mock data (55.5% win rate, 299 bets) |

**What We Need:**
1. Define "extreme split" (10+ PPG difference? 15+?)
2. Which teams qualify (how many teams per season?)
3. Bet type (spread? Moneyline? Total?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, calculate home/away point differential for all teams. Identify teams with 10+ PPG splits. Bet against them on road (or with them at home). Calculate cover rates.
```

---

### **Strategy #20: Divisional Rivalries Strategy**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Division rivals meet, bet under (games are closer/grindier) |
| **Sports** | NBA, NFL, NHL |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Schedule (divisional matchups) |
| **Odds Source** | ❓ Game totals |
| **Outcome Metric** | ❓ Does total go under? |
| **Current Status** | Mock data (54.7% win rate, 258 bets) |

**What We Need:**
1. All divisional matchups only? Or heated rivalries only?
2. Bet type (under? Underdog spread?)
3. Home/away difference

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify all divisional matchup games. Calculate under win rate vs non-divisional games. Segment by rivalry intensity (how many times they meet per season).
```

---

### **Strategy #21: Key Numbers Strategy (NFL)**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Spread crosses key number (3, 7, 10), bet accordingly |
| **Sports** | NFL only |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ NFL game results |
| **Odds Source** | ❓ Historical spreads |
| **Outcome Metric** | ❓ Does result land on key number? Bet wins? |
| **Current Status** | Mock data (57.0% win rate, 337 bets) |

**What We Need:**
1. Which key numbers to target (3, 7 only? Also 4, 6, 10?)
2. Buy points strategy (buy onto key number? Off key number?)
3. Home/favorite/underdog differences

**ChatGPT Query to Define:**
```
For 2023 NFL season, analyze final margins. Calculate frequency of 3, 4, 6, 7, 10-point margins. Test betting strategy: when spread is 2.5, buy to 3. When spread is 3, sell to 2.5. Calculate ROI.
```

---

### **Strategy #22: Low-Hold Opportunities**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Two sportsbooks have <2% hold (near arbitrage), bet both sides |
| **Sports** | NBA, NFL, NHL, MLB |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Real-time odds comparison |
| **Odds Source** | ❓ Multiple sportsbooks |
| **Outcome Metric** | ❓ Guaranteed profit or minimize loss |
| **Current Status** | Mock data (55.7% win rate, 375 bets) |

**What We Need:**
1. Hold threshold (<2%? <1.5%? <1%?)
2. Book combinations to monitor
3. Bet sizing to lock profit

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, compare moneylines across sportsbooks. Calculate hold percentages. Identify <2% hold opportunities. Calculate guaranteed profit or expected loss vs single bet ROI.
```

---

### **Strategy #23: Halftime Tracker**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Team leads at halftime, bet them to cover 2H |
| **Sports** | NBA, NCAA Basketball |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Halftime scores |
| **Odds Source** | ❓ 2H spreads |
| **Outcome Metric** | ❓ Does team cover 2H? |
| **Current Status** | Mock data (unknown) |

**What We Need:**
1. Lead threshold (any lead? 5+ points? 10+?)
2. Favorites vs underdogs (does it matter?)
3. Bet type (2H spread? 2H moneyline?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify halftime leaders. Calculate 2H spread coverage rate. Segment by halftime lead size (1-5, 6-10, 11-15, 16+ points).
```

---

### **Strategy #24: Momentum Detector**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Team on scoring run (12-0, 15-2, etc.), bet opponent next quarter |
| **Sports** | NBA, NHL |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Play-by-play scoring runs |
| **Odds Source** | ❓ Live quarter spreads |
| **Outcome Metric** | ❓ Does opponent outscore hot team next quarter? |
| **Current Status** | Mock data (unknown) |

**What We Need:**
1. Scoring run definition (12-0? 15-2? 18-4?)
2. When to bet (immediately? Wait for timeout?)
3. Period-specific (Q1-Q4 differences?)

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, identify scoring runs of 12+ to 0-2 points. Track next 5-minute performance. Calculate if opponent outscores or hot team cools off. Test betting opponent next quarter spread.
```

---

### **Strategy #25: Pace Mismatch Detector**

| Field | Value/Need |
|-------|------------|
| **Trigger Logic** | ❓ Fast-paced team vs slow-paced team, bet total based on matchup |
| **Sports** | NBA, NCAA Basketball |
| **Date Range** | ❓ Need to define |
| **Data Source** | ❓ Team pace rankings |
| **Odds Source** | ❓ Game totals |
| **Outcome Metric** | ❓ Does total go over/under based on pace? |
| **Current Status** | Mock data (unknown) |

**What We Need:**
1. Pace mismatch threshold (20+ possessions/game difference?)
2. Bet direction (always over? Under when slow team home?)
3. Home/away impact

**ChatGPT Query to Define:**
```
For 2023-24 NBA season, calculate pace mismatches (top 5 fastest vs bottom 5 slowest teams). Measure actual game pace vs season averages. Determine if total goes over (fast pace dominates) or under (slow pace dominates).
```

---

## 📊 SUMMARY: DATA COLLECTION STATUS

| Status | Count | Strategies |
|--------|-------|-----------|
| ✅ Verified Real Data | 3 | Goalie Pull (#6), Quarter Reversal (#14), End Game Unders (#8) |
| ❓ Need Definition | 22 | All others |
| ❌ Failing Strategy | 1 | End Game Unders (#8) - needs revision |

---

## 🎯 NEXT STEPS

### Phase 1: Define Trigger Logic (Week 1)
- Review each strategy with betting experts
- Define exact trigger conditions
- Specify data requirements

### Phase 2: Data Collection (Week 2-3)
- Acquire historical data sources
- Pull game data for backtest periods
- Get historical odds data

### Phase 3: ChatGPT Calculations (Week 3-4)
- Feed data + trigger logic to ChatGPT
- Calculate win rates for each strategy
- Generate ROI reports

### Phase 4: Database Update (Week 4)
- Replace mock data with real calculations
- Update win rates, ROI, sample sizes
- Deploy to production

---

## 📁 FILES TO CREATE

1. **strategy_01_hot_shooting_fade_inputs.json** - Detailed input spec
2. **strategy_02_momentum_shift_inputs.json** - Detailed input spec
3. ... (one for each strategy)
4. **chatgpt_batch_queries.txt** - All queries ready to paste
5. **backtest_results_verified.csv** - Output format for ChatGPT

---

**END OF INPUT DEFINITIONS**
