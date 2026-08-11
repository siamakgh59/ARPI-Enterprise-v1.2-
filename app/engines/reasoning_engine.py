def generate_reasoning(asset, signal, confidence, risk, data=None, base_reasoning=None):
    """
    دلایل واقعی تحلیل هر asset (که قبلاً توسط Gold Engine یا
    Technical Analysis محاسبه شده) را می‌گیرد و فقط یک لایه‌ی
    نظر بر اساس سطح ریسک به آن اضافه می‌کند — دیگر دلیل ساختگی
    بر اساس اسم asset نمی‌سازد.
    """

    reasons = list(base_reasoning) if base_reasoning else []

    if risk == "LOW":
        reasons.append("Risk condition controlled")

    elif risk == "HIGH":
        reasons.append("Elevated risk condition")

    elif risk == "CRITICAL":
        reasons.append("Critical risk condition")

    return {
        "asset": asset,
        "signal": signal,
        "confidence": confidence,
        "risk": risk,
        "reasoning": reasons
    }
