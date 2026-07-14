def calculate_technical_score(change: float):

    score = 50

    if change > 2:
        score += 25
    elif change > 0:
        score += 10

    elif change < -2:
        score -= 25
    elif change < 0:
        score -= 10

    return max(0, min(score, 100))


def technical_signal(score: int):

    if score >= 70:
        return "BUY"

    if score <= 30:
        return "SELL"

    return "HOLD"


def analyze_technical(price, change):

    score = calculate_technical_score(
        change
    )

    return {
        "technical_score": score,
        "technical_signal": technical_signal(score),
        "trend": (
            "BULLISH"
            if score > 55
            else "BEARISH"
            if score < 45
            else "NEUTRAL"
        )
    }
