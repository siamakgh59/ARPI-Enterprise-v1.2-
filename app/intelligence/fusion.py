from .technical import analyze_technical


def calculate_confidence(responses):

    valid = [
        r for r in responses
        if r.get("success")
    ]

    if not valid:
        return 0

    confidence = 50 + (len(valid) * 10)

    return min(confidence, 95)


def analyze_asset(name, responses):

    confidence = calculate_confidence(responses)

    if not responses:
        return {
            "asset": name,
            "signal": "NO_DATA",
            "confidence": 0,
            "risk": "HIGH"
        }

    price = responses[0].get("price", 0)
    change = responses[0].get("change", 0)

    if change > 1:
        signal = "BUY"
    elif change < -1:
        signal = "SELL"
    else:
        signal = "HOLD"

    risk = "LOW"

    if abs(change) > 2:
        risk = "HIGH"
    elif abs(change) > 1:
        risk = "MEDIUM"

    technical = analyze_technical(
        price,
        change
    )

    return {
        "asset": name,
        "price": price,
        "change": change,
        "signal": signal,
        "confidence": confidence,
        "risk": risk,
        "providers": [
            r.get("provider")
            for r in responses
        ],
        "technical": technical
    }


def fusion_market(data):

    result = {}

    for name, responses in data.items():

        result[name] = analyze_asset(
            name,
            responses
        )

    return result
