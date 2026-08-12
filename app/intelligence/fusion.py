from .technical import analyze_technical

from app.engines.gold.engine import GoldIntelligenceEngine
from app.engines.gold.providers import FarazGoldProvider


gold_engine = GoldIntelligenceEngine()
gold_provider = FarazGoldProvider()



def calculate_confidence(score):

    confidence = 50 + abs(score) * 5

    return min(max(confidence, 0), 95)




def analyze_gold():

    try:

        gold_data = (
            gold_provider.fetch_gold_data()
        )


        result = (
            gold_engine.analyze(
                gold_data
            )
        )


        return {

            "asset": "gold",

            "signal":
                result["signal"],

            "confidence":
                result["confidence"],

            "risk":
                (
                    "HIGH"
                    if result["gold_score"] < 40
                    else
                    "MEDIUM"
                    if result["gold_score"] < 70
                    else
                    "LOW"
                ),

            "reasoning":
                result["drivers"],

            "gold_score":
                result["gold_score"],

            "drivers":
                result["drivers"],

            "risks":
                result["risks"],

            "engine":
                result["engine"],

            # اعداد خام واقعی، برای نمایش در داشبورد
            "metrics": {
                "gold18_price": gold_data.get("gold18_price"),
                "mesghal_price": gold_data.get("mesghal_price"),
                "coin_emami": gold_data.get("coin_emami"),
                "usd_free_rate": gold_data.get("usd_free_rate"),
                "xau_usd": gold_data.get("xau_usd"),
                "coin_bubble_percent": gold_data.get("coin_bubble_percent"),
            }

        }


    except Exception as e:


        print(
            "GOLD FUSION ERROR:",
            e
        )


        return {

            "asset": "gold",

            "signal": "NO_DATA",

            "confidence": 0,

            "risk": "HIGH",

            "metrics": {}

        }





def analyze_asset(name, responses):


    if name == "gold":

        return analyze_gold()



    if not responses:

        return {

            "asset": name,

            "signal": "NO_DATA",

            "confidence": 0,

            "risk": "HIGH",

            "metrics": {}

        }



    data = responses[0]


    price = data.get(
        "price",
        0
    )


    change = data.get(
        "change",
        0
    )


    history = data.get(
        "history",
        []
    )



    technical = analyze_technical(
        history
    )


    score = 0

    reasoning = []



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



    rsi = technical.get(
        "RSI14",
        50
    )



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



    ema20 = technical.get(
        "EMA20",
        0
    )

    ema50 = technical.get(
        "EMA50",
        0
    )



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



    if score >= 2:

        signal = "BUY"


    elif score <= -2:

        signal = "SELL"


    else:

        signal = "HOLD"



    confidence = calculate_confidence(
        score
    )



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

        ],

        # اعداد خام واقعی، برای نمایش در داشبورد
        "metrics": {
            "price": price,
            "change_pct": change,
            "rsi14": technical.get("RSI14"),
            "ema20": technical.get("EMA20"),
            "ema50": technical.get("EMA50"),
        }

    }




def fusion_market(data):


    result = {}


    for name, responses in data.items():


        result[name] = analyze_asset(
            name,
            responses
        )


    return result
