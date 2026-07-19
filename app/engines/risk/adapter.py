def build_risk_factors(asset_data: dict) -> dict:

    confidence = asset_data.get(
        "confidence",
        50
    )

    risk = asset_data.get(
        "risk",
        "MEDIUM"
    )


    volatility_risk = 50

    if risk == "HIGH":
        volatility_risk = 80

    elif risk == "LOW":
        volatility_risk = 30


    return {

        "market_risk": 50,

        "volatility_risk": volatility_risk,

        "macro_risk": 50,

        "liquidity_risk": 40,

        "geopolitical_risk": 50,

        "data_confidence_risk": 100 - confidence

    }
