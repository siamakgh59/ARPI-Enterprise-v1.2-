 import pandas as pd


def calculate_rsi(
    prices,
    period=14
):

    series = pd.Series(prices)

    delta = series.diff()

    gain = delta.clip(
        lower=0
    )

    loss = -delta.clip(
        upper=0
    )


    avg_gain = (
        gain
        .rolling(period)
        .mean()
    )

    avg_loss = (
        loss
        .rolling(period)
        .mean()
    )


    rs = avg_gain / avg_loss


    rsi = 100 - (
        100 /
        (1+rs)
    )


    return float(
        rsi.iloc[-1]
    )



def calculate_ema(
    prices,
    period
):

    series = pd.Series(prices)

    ema = series.ewm(
        span=period,
        adjust=False
    ).mean()


    return float(
        ema.iloc[-1]
    )



def analyze_technical(
    prices
):

    if not prices or len(prices) < 50:

        return {

            "technical_score":50,
            "technical_signal":"NO_DATA",
            "trend":"UNKNOWN"

        }



    rsi = calculate_rsi(
        prices,
        14
    )


    ema20 = calculate_ema(
        prices,
        20
    )


    ema50 = calculate_ema(
        prices,
        50
    )


    current = prices[-1]


    score = 50


    if rsi < 30:
        score += 20

    elif rsi > 70:
        score -= 20



    if ema20 > ema50:
        score += 20
        trend="BULLISH"

    else:
        score -=20
        trend="BEARISH"



    score=max(
        0,
        min(score,100)
    )


    if score >=70:
        signal="BUY"

    elif score <=30:
        signal="SELL"

    else:
        signal="HOLD"



    return {

        "technical_score":score,

        "technical_signal":signal,

        "trend":trend,

        "RSI14":round(rsi,2),

        "EMA20":round(ema20,2),

        "EMA50":round(ema50,2),

        "price":current

    }
