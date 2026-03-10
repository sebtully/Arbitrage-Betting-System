# Football Betting Intelligence Platform – Blueprint

## Arkitektur (MVP → Scale)

1. **Ingestion layer**
   - Playwright scrapers pr. bookmaker.
   - Normalisering til fælles market model (`match_id`, `market_key`, `outcome`, `odds`, `timestamp`).
   - Redis queue til buffering + retry.

2. **Storage layer**
   - PostgreSQL som source-of-truth.
   - `odds_ticks` tabel som time-series stream.
   - Separate tabeller for `matches`, `bets`, og kontekstdata.

3. **Analytics engines**
   - Odds movement analyzer (velocity, lag, drift).
   - Steam detector (synkrone drops på tværs af books).
   - Sharp money detector (Pinnacle/Betfair/SBO signal før soft books).
   - Arbitrage engine (inverse probability scan).
   - CLV engine (predicted close vs available odds).

4. **ML layer**
   - Feature store (team, player, market microstructure).
   - Klassiske modeller + gradient boosting.
   - Sandsynlighedsoutput kalibreres (Platt/isotonic).

5. **Portfolio & recommendation layer**
   - EV + fractional Kelly sizing i units.
   - Risiko-klassifikation (Low/Medium/High).
   - League profitability ranking baseret på ROI, CLV, variance.

6. **Frontend dashboard**
   - React + TypeScript + Tailwind.
   - Widgets: Best Value Bets, Steam Moves, Arbitrage, Sharp Alerts, Portfolio KPI, League ROI.

## Core KPI'er

- **CLV (Closing Line Value)**
- **ROI i units**
- **Hit-rate**
- **Sharpe-lignende risikojusteret afkast**
- **Model calibration error**

## Prioriteret implementeringsplan (12 uger)

1. Uge 1-2: data model + 2-3 bookmaker scrapers.
2. Uge 3-4: odds movement + arbitrage + alert pipeline.
3. Uge 5-6: baseline ML + bet recommendation engine.
4. Uge 7-8: CLV prediction model + backtesting framework.
5. Uge 9-10: portfolio manager + league profitability AI.
6. Uge 11-12: dashboard, monitoring, og deploy.
