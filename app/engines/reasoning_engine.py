def generate_reasoning(asset, signal, confidence, risk, data=None):
    reasons = []

    if signal == "SELL":
        reasons.append("Momentum weakness detected")

    if asset in ["gold", "silver"]:
        reasons.append("USD pressure detected")

    if risk == "LOW":
        reasons.append("Risk condition controlled")

    return {
        "asset": asset,
        "signal": signal,
        "confidence": confidence,
        "risk": risk,
        "reasoning": reasons
    }
