from typing import Dict


class GoldCalculator:

    """
    ARPI Gold Calculator v4.2

    Dynamic Gold Market Scoring Engine

    Inputs:
    Iran Market
    Global Gold
    USD
    Risk Regime

    Output:
    score
    regime
    signal
    confidence
    """


    VERSION = "4.2.0"


    def calculate(
        self,
        data: Dict
    ) -> Dict:


        score = 50

        drivers = []

        risks = []



        # =========================
        # Gold18 Price
        # =========================

        if data.get("gold18_price"):

            score += 8

            drivers.append(
                "Gold18 price available"
            )



        # =========================
        # Mesghal
        # =========================

        if data.get("mesghal_price"):

            score += 5

            drivers.append(
                "Mesghal data available"
            )



        # =========================
        # USD Support
        # =========================

        usd_change = data.get(
            "usd_change"
        )


        if usd_change:

            if usd_change > 0:

                score += 6

                drivers.append(
                    "USD market support"
                )


            else:

                score -= 3



        # =========================
        # USD Momentum
        # =========================

        if usd_change:

            if usd_change > 1:

                score += 5

                drivers.append(
                    "Positive USD momentum"
                )



        # =========================
        # Volume
        # =========================

        if data.get("volume"):

            score += 3

            drivers.append(
                "Market volume available"
            )



        # =========================
        # Global Gold
        # =========================

        xau = data.get(
            "xau_usd"
        )


        if xau:


            if xau > 4000:

                score += 8

                drivers.append(
                    "Strong global gold price"
                )



        # =========================
        # Gold Momentum
        # =========================

        daily = data.get(
            "gold_daily_change"
        )


        if daily is not None:


            if daily < 0:

                score -= 5

                risks.append(
                    "Negative gold momentum"
                )


            else:

                score += 4



        # =========================
        # Coin Bubble
        # =========================

        bubble_percent = data.get(
            "coin_bubble_percent"
        )


        if bubble_percent:


            if bubble_percent > 2:

                score -= 8

                risks.append(
                    "High coin bubble risk"
                )


            elif bubble_percent > 1:

                score -= 4

                risks.append(
                    "Medium coin bubble risk"
                )


            else:

                drivers.append(
                    "Controlled coin bubble"
                )



        # =========================
        # Bond Yield
        # =========================

        yield10 = data.get(
            "us10y_yield"
        )


        if yield10:


            if yield10 > 4.5:

                score -= 5

                risks.append(
                    "High bond yield pressure"
                )



        # =========================
        # Market Regime
        # =========================


        if score < 65:

            regime = "GOLD_STRESS"

            drivers.append(
                "Gold stress regime"
            )


        elif score > 80:

            regime = "GOLD_BULL"

        else:

            regime = "BALANCED"



        # =========================
        # Normalize
        # =========================

        score = max(
            0,
            min(
                100,
                score
            )
        )



        # =========================
        # Signal
        # =========================


        if score >= 75:

            signal = "BUY"


        elif score >= 60:

            signal = "HOLD"


        else:

            signal = "SELL"



        confidence = 75



        return {

            "gold_score": score,

            "signal": signal,

            "market_regime": regime,

            "confidence": confidence,

            "drivers": drivers,

            "risks": risks,

        }
