# Max EV Sports — Evidence & Architecture

> **Goal:** Collect, process, and predict faster than the market so users can act when **price ≠ true probability**. We measure edge by **calibration, CLV, and timeliness**, then report **realized ROI after costs** with confidence intervals.

---

## 1) Ideal Tech Stack (Built for Speed & Integrity)

### 1.1 Ingestion (Oddslines + Gamestate)
- **Realtime feeds:** Multi-book odds ticks (REST+WebSocket where available), play-by-play / game state (clock, possession, penalties, bonus, goalie pulls, etc.)
- **Broker/Queue:** Kafka or Redpanda (topic per sport/league), with partitioning by event_id.
- **Normalizer:** stateless workers to unify markets (`TOTAL`, `SPREAD`, `ML`, props), fields, and timezones.

**Latency budget:** _Odds tick → broker_ **≤150 ms**; _PBP tick → broker_ **≤200 ms**

---

### 1.2 Feature Store (Low-latency + Versioned)
- **Warm features:** Season/rolling priors (KenPom tempo & efficiencies, half-split EMAs, fatigue index, injury impact tables).
- **Cold features:** Opponent-adjusted forms, park/weather/umpire (MLB), surface (tennis), track (NASCAR).
- **Store:** Postgres/ClickHouse + materialized views; features **versioned** by `model_version` and **time-stamped** to prevent leakage.

**Latency budget:** _Feature join_ **≤20 ms** (in-memory cache for hot keys).

---

### 1.3 Model Serving (Max EV Boost)
- **Serving:** XGBoost/LightGBM in a lightweight service (FastAPI/uvicorn) with model registry.
- **Calibration:** Isotonic/Platt per model_version; always emit **calibrated probability** `cal_p`.
- **Uncertainty:** Conformal intervals for totals/spreads (80%/95% bands).

**Latency budget:** _Request → calibrated prediction_ **≤25 ms** (P95).

---

### 1.4 Pricing & Alerting
- **Fair line:** Convert `cal_p` → fair American odds; map totals point-edge → win prob via empirical curve.
- **Guards:** 
  - **Quote-age** ≤ 4 s (drop stale quotes)
  - **Two-book confirmation** (optional)
  - **Dispersion check** (block if cross-book spread suggests a move is in flight)
- **Execution:** ¼-Kelly with **context caps** (e.g., 0.5–1.0% in volatile live states).
- **Emit:** Alert only if **price ≥ fair + cushion** after costs.

**Latency budget:** _Odds tick → user alert_ **≤450 ms** end-to-end.

---

### 1.5 Storage & Backtesting
- **Ticks:** Immutable `odds_ticks(event_id, ts, book, market, selection, line, price_american)`
- **Model outputs:** `model_outputs(model_id, version, event_id, asof, selection, raw_p, cal_p, features)`
- **Fills:** `fills(..., price_american, fair_american, ev, kelly, stake, result, pnl, clv_cents)`
- **Backtests:** Walk-forward, **post-slippage** and **fill-probability** modeled by quote-age & volatility.

---

### 1.6 Monitoring & Governance
- **Calibration dashboards:** Brier / log-loss by probability bucket.
- **CLV dashboard:** median/mean CLV (cents), bucketed by sport and book.
- **Timeliness:** lead time (seconds) from model shock → market move.
- **Canary deploys:** model_version rollout 10–20% with auto-rollback if CLV/ROI degrades.
- **Audit logs:** snapshot features, fair line, quotes used, guards triggered.

---

## 2) Evidence: What We Measure & Publish

> We don’t promise a fixed ROI. We **prove** model quality and price discovery with standard market metrics; returns are shown **after costs**, with confidence intervals and sample sizes.

### 2.1 Probability Quality (Calibration)
- **KPIs:** Brier score, log-loss, calibration curves (reliability plots) by bucket.
- **Baseline:** Elo/power-rating variants per sport.
- **Claim:** “Across NBA/NHL/NCAAB, Max EV Boost models show **lower Brier/log-loss** than Elo/power baselines in out-of-sample tests.”

**On the page:**  
- Chart: **Calibration plot** (ideal diagonal) with Max EV vs Elo overlay.  
- Table: `Sport | Model | Brier Δ vs Elo | Log-loss Δ vs Elo | N`

---

### 2.2 Pricing Efficiency (Beat the Close / CLV)
- **KPI:** % of fills that **beat the closing line**, median CLV (cents).
- **Why it matters:** Closing prices are the market’s best consensus; beating them indicates true edge even before outcomes.
- **Claim:** “Our live alerts **beat the close more often** than Elo/power-rating baselines; median CLV is **positive** across validated strategies.”

**On the page:**  
- Sparkline: **CLV over time**  
- Table: `Strategy | % Beats Close | Median CLV (¢) | N | Data Window`

---

### 2.3 Timeliness (Speed to Information)
- **KPI:** Median **lead time (s)** from an information shock (injury, pace spike, bonus/empty-net trigger) to our model’s fair price vs. first market move.
- **Claim:** “Model fair price adjusts **faster than the market** during live state changes—especially bonus-imminent (NBA), delayed penalties/goalie pulls (NHL).”

**On the page:**  
- Bar chart: `Signal Type | Lead Time (s) | N`

---

### 2.4 Realized Returns (After Costs)
- **KPI:** **ROI after slippage & rejections**, with **95% CI**, by strategy and odds bucket.
- **Disclosure:** Results vary by sport, season, and user execution. We publish **data windows**, **sample sizes**, and **assumptions** (slippage curves, min-odds rules).

**On the page:**  
- Table: `Strategy | ROI (net) | 95% CI | Sample | Data Window | Avg Odds | Min Odds Rule`
- Toggle: Show/hide strategies with **N < 100** (default hidden).

---

### 2.5 A/B: Strategy-Only vs ML-Enhanced
- **Design:** 10–20% canary of ML-enhanced signals vs Strategy-only baseline.
- **KPIs:** ΔCLV, ΔBrier/log-loss, ΔROI (net), significance.
- **Claim:** “ML-enhanced signals show **higher CLV and better calibration** than strategy-only across our validated set.”

**On the page:**  
- Table: `Strategy | Variant | ΔCLV (¢) | ΔBrier | ΔROI (net) | p-value`

---

## 3) Methodology & Disclosures (Clickable Drawer)

- **Backtest protocol:** Walk-forward by date; grouped CV by event; no tick leakage.
- **Costs:** Slippage by book and quote-age; realistic fill probabilities; cushion applied.
- **Guards:** quote-age ≤ 4s; two-book confirmation; dispersion filter.
- **Calibration:** Isotonic/Platt per model_version; report both raw and calibrated.
- **Uncertainty:** Conformal intervals for totals/spreads (80%/95%).
- **Data windows:** Shown for every chart/table.
- **Disclaimer:** Past performance does not guarantee future results. Availability and fills vary by user, book, and jurisdiction.

---

## 4) Example (How to Read a Strategy Card)

**Live Total Regression — NBA**  
- **Calibrated p(Over)**: 0.612 (fair **-158**)  
- **Best available**: **-120** (2 books, quote-age 1.6s)  
- **Edge**: 38 cents; **¼-Kelly**: 1.2% (cap 1.0%)  
- **CLV last 30d**: +6¢ median (N=412)  
- **Resulting ROI (net)** last 90d: +3.9% (95% CI: +0.8% → +6.7%)

> We trigger only when price ≥ fair + cushion after costs, with live guards enabled.

---

## 5) Why We’ll Beat Slow Books (and Often the Public)

- **Faster state ingestion:** Bonus-imminent, delayed penalties, coach pull tendencies, pace spikes.  
- **Richer features:** Team priors (KenPom), half-split trends, fatigue, injuries, weather/park/umpire.  
- **Better probabilities:** Calibrated model outputs; uncertainty bands.  
- **Execution discipline:** Quote-age, dispersion, 2-book confirmation; ¼-Kelly with context caps.  
- **Proof:** Publish **calibration**, **CLV**, **lead times**, and **net ROI** with CIs.

---

## 6) What We Don’t Claim

- No fixed ROI guarantees.  
- No “always win.”  
- We show **evidence** and **controls** so you can make informed decisions.

---

## 7) Implementation Notes (for Devs)

- **APIs:**  
  - `/calibrated-prob?model_id=...&model_version=...&event_id=...&selection=...`  
  - `/quote-age-check?event_id=...&market=...&selection=...&book=...`  
  - `/aggregates/odds-buckets?model_id=...`  
- **Data sources (examples):**  
  - Odds: multi-book feeds + websockets where available  
  - Game state: league/partners + internal scrapers (where terms allow)  
  - Priors: KenPom (licensed), Sports-Reference/NCAA (half splits ETL), weather/umpire, etc.

---

### Appendix A — Latency Targets (P95)

| Stage | Budget |
|---|---|
| Feed → Broker | ≤ 200 ms |
| Feature join | ≤ 20 ms |
| Model + Calibration | ≤ 25 ms |
| Guards & pricing | ≤ 50 ms |
| Alert emit | ≤ 150 ms |
| **End-to-end** | **≤ 450 ms** |

