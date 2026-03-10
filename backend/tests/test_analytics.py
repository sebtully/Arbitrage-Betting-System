from analytics import OddsQuote, RiskTier, build_recommendation, detect_two_way_arbitrage, expected_value


def test_expected_value_positive():
    assert round(expected_value(0.62, 2.25), 3) == 0.395


def test_two_way_arbitrage_detected():
    quotes = [
        OddsQuote(bookmaker="Bet365", outcome="Team A", odds=2.1),
        OddsQuote(bookmaker="Unibet", outcome="Team B", odds=2.1),
    ]
    is_arb, margin = detect_two_way_arbitrage(quotes)
    assert is_arb is True
    assert margin < 0


def test_recommendation_shape():
    rec = build_recommendation(
        market="Saka over 1.5 shots on target",
        odds=2.25,
        model_probability=0.62,
        predicted_closing_odds=1.95,
        bankroll_units=100,
    )
    assert rec.expected_value > 0
    assert rec.bet_size_units > 0
    assert rec.risk_tier == RiskTier.LOW
