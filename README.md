Initial scaffold for en **Football Betting Intelligence Platform** med fokus på odds intelligence, CLV, arbitrage og portfolio management.

## Struktur

- `docs/system_blueprint.md` – overordnet arkitektur og roadmap.
- `sql/schema.sql` – PostgreSQL schema til matches, odds ticks og bets.
- `backend/src/analytics.py` – kerneberegninger (EV, Kelly, arbitrage, risk-tier, recommendation).
- `backend/tests/test_analytics.py` – unit tests for kerneberegninger.

## Hurtigstart (backend)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install pytest
pytest
```

## Hvad der er implementeret nu

- EV beregning fra model probability og odds.
- Fractional Kelly sizing til unit-baseret bankroll management.
- 2-vejs arbitrage detektion.
- Simple risk tiers (low/medium/high).
- Bet recommendation objekt med CLV-input.

## Næste skridt

1. Implementer bookmaker connectors (Playwright/API).
2. Byg ingestion pipeline med Redis queue.
3. Udvid ML feature store + modeltræning.
4. Tilføj real-time alerts til dashboard.
