CREATE TABLE matches (
  id BIGSERIAL PRIMARY KEY,
  home_team TEXT NOT NULL,
  away_team TEXT NOT NULL,
  competition TEXT NOT NULL,
  venue TEXT,
  kickoff_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE odds_ticks (
  id BIGSERIAL PRIMARY KEY,
  match_id BIGINT REFERENCES matches(id),
  bookmaker TEXT NOT NULL,
  market_type TEXT NOT NULL,
  market_key TEXT NOT NULL,
  outcome TEXT NOT NULL,
  decimal_odds NUMERIC(8,3) NOT NULL,
  liquidity_estimate NUMERIC(12,2),
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_odds_ticks_market_time ON odds_ticks (market_key, captured_at DESC);
CREATE INDEX idx_odds_ticks_bookmaker_time ON odds_ticks (bookmaker, captured_at DESC);

CREATE TABLE bets (
  id BIGSERIAL PRIMARY KEY,
  match_id BIGINT REFERENCES matches(id),
  market_key TEXT NOT NULL,
  outcome TEXT NOT NULL,
  bookmaker TEXT NOT NULL,
  odds_taken NUMERIC(8,3) NOT NULL,
  stake_units NUMERIC(8,3) NOT NULL,
  closing_odds NUMERIC(8,3),
  result TEXT,
  placed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  settled_at TIMESTAMPTZ
);
