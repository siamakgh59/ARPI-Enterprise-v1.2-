def market_to_risk_factors(
    asset_analysis: dict
) -> dict:


    confidence = asset_analysis.get(
        "confidence",
        50
    )


    signal = asset_analysis.get(
        "signal",
        "HOLD"
    )


    risk = asset_analysis.get(
        "risk",
        "MEDIUM"
    )


    market_risk = 50


    if signal == "SELL":
        market_risk = 70

    elif signal == "BUY":
        market_risk = 30



    volatility_risk = 50


    if risk == "HIGH":
        volatility_risk = 80

    elif risk == "LOW":
        volatility_risk = 30



    return {

        "market_risk": market_risk,

        "volatility_risk": volatility_risk,

        "macro_risk": 50,

        "liquidity_risk": 40,

        "geopolitical_risk": 50,

        "data_confidence_risk": 100 - confidence

    }
