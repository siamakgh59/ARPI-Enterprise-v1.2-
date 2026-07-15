import pandas as pd


def analyze_technical(prices):

    if not prices or len(prices) < 50:
        return {
            "technical_score": 50,
            "technical_signal": "NO_DATA",
            "trend": "NO_TREND",
            "RSI14": 50,
            "EMA20": 0,
            "EMA50": 0
        }


    series = pd.Series(prices)

    ema20 = series.ewm(
        span=20,
        adjust=False
    ).mean().iloc[-1]

    ema50 = series.ewm(
        span=50,
        adjust=False
    ).mean().iloc[-1]


    score = 70 if ema20 > ema50 else 30

    signal = "BUY" if score >= 70 else "SELL"

    return {
        "technical_score": score,
        "technical_signal": signal,
        "trend": "BULLISH" if ema20 > ema50 else "BEARISH",
        "RSI14": 50,
        "EMA20": round(float(ema20), 2),
        "EMA50": round(float(ema50), 2)
    }


