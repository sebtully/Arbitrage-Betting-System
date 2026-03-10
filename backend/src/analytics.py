from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence


class RiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class OddsQuote:
    bookmaker: str
    outcome: str
    odds: float


@dataclass(frozen=True)
class BetRecommendation:
    market: str
    odds: float
    model_probability: float
    predicted_closing_odds: float
    expected_value: float
    bet_size_units: float
    risk_tier: RiskTier


def implied_probability(decimal_odds: float) -> float:
    if decimal_odds <= 1:
        raise ValueError("Decimal odds must be > 1")
    return 1 / decimal_odds


def expected_value(model_probability: float, decimal_odds: float) -> float:
    """Return EV per unit staked."""
    if not 0 <= model_probability <= 1:
        raise ValueError("Probability must be between 0 and 1")
    return (model_probability * decimal_odds) - 1


def kelly_fraction(model_probability: float, decimal_odds: float, kelly_multiplier: float = 0.25) -> float:
    """Fractional Kelly sizing with a conservative default (25%)."""
    b = decimal_odds - 1
    q = 1 - model_probability
    raw = ((b * model_probability) - q) / b
    return max(0.0, raw * kelly_multiplier)


def detect_two_way_arbitrage(quotes: Sequence[OddsQuote]) -> tuple[bool, float]:
    """Find if two-way market has arbitrage and return margin.

    Margin < 0 indicates arbitrage edge, e.g. -0.03 => 3% arb.
    """
    if len(quotes) != 2:
        raise ValueError("Two-way arbitrage detector expects exactly two outcomes")

    total = sum(implied_probability(q.odds) for q in quotes)
    return total < 1, total - 1


def classify_risk(model_probability: float, ev: float) -> RiskTier:
    if model_probability >= 0.6 and ev >= 0.05:
        return RiskTier.LOW
    if ev >= 0.02:
        return RiskTier.MEDIUM
    return RiskTier.HIGH


def build_recommendation(
    market: str,
    odds: float,
    model_probability: float,
    predicted_closing_odds: float,
    bankroll_units: float,
) -> BetRecommendation:
    ev = expected_value(model_probability, odds)
    size_fraction = kelly_fraction(model_probability, odds)
    bet_size = round(bankroll_units * size_fraction, 2)
    risk = classify_risk(model_probability, ev)

    return BetRecommendation(
        market=market,
        odds=odds,
        model_probability=model_probability,
        predicted_closing_odds=predicted_closing_odds,
        expected_value=round(ev, 4),
        bet_size_units=bet_size,
        risk_tier=risk,
    )
