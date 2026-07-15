from .technical import analyze_technical


def calculate_confidence(score):
    confidence = 50 + abs(score) * 5
    return min(max(confidence, 0), 95)


def analyze_asset(name, responses):

    if not responses:
        return {
            "asset": name,
            "signal": "NO_DATA",
            "confidence": 0,
            "risk": "HIGH"
        }

    data = responses[0]

    price = data.get("price", 0)
    change = data.get("change", 0)
    history = data.get("history", [])

    technical = analyze_technical(
        history
    )

    score = 0
    reasoning = []

    # Momentum
    if change > 1:
        score += 1
        reasoning.append(
            "Positive market momentum"
        )

    elif change < -1:
        score -= 1
        reasoning.append(
            "Negative market momentum"
        )


    # RSI
    rsi = technical.get("RSI14", 50)

    if rsi < 30:
        score += 2
        reasoning.append(
            "RSI oversold"
        )

    elif rsi > 70:
        score -= 2
        reasoning.append(
            "RSI overbought"
        )


    # EMA Trend
    ema20 = technical.get("EMA20", 0)
    ema50 = technical.get("EMA50", 0)


    if ema20 > ema50:
        score += 2
        reasoning.append(
            "EMA bullish trend"
        )

    elif ema20 < ema50:
        score -= 2
        reasoning.append(
            "EMA bearish trend"
        )


    # Final Signal

    if score >= 2:
        signal = "BUY"

    elif score <= -2:
        signal = "SELL"

    else:
        signal = "HOLD"


    confidence = calculate_confidence(score)


    risk = "LOW"

    if abs(change) > 2:
        risk = "HIGH"

    elif abs(change) > 1:
        risk = "MEDIUM"


    return {
        "asset": name,
        "price": price,
        "change": change,
        "signal": signal,
        "confidence": confidence,
        "risk": risk,
        "technical": technical,
        "reasoning": reasoning,
        "providers": [
            r.get("provider")
            for r in responses
        ]
    }



def fusion_market(data):

    result = {}

    for name, responses in data.items():

        result[name] = analyze_asset(
            name,
            responses
        )

    return result
