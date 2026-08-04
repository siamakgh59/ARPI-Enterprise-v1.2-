from typing import Dict, List


class DynamicGoldCalculator:
    """
    ARPI Dynamic Gold Intelligence Calculator v4.0

    Features:
    - Market regime detection
    - Dynamic factor weighting
    - Risk adjustment
    - Confidence intelligence
    """


    VERSION = "4.0.0"



    def calculate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:


        score = 50

        drivers: List[str] = []

        risks: List[str] = []



        # ---------------------------------
        # Market Regime Detection
        # ---------------------------------

        xau = factors.get("xau_usd")

        dxy = factors.get("dxy")

        yield10 = factors.get("us10y_yield")

        usd_change = factors.get("usd_change")



        regime = "NORMAL"



        if (
            xau is not None
            and xau >= 3000
            and yield10 is not None
            and yield10 >= 4.5
        ):

            regime = "GOLD_STRESS"



        elif (
            usd_change is not None
            and usd_change > 1
        ):

            regime = "LOCAL_INFLATION"



        elif (
            dxy is not None
            and dxy < 95
        ):

            regime = "GLOBAL_GOLD_SUPPORT"



        # ---------------------------------
        # Gold18
        # ---------------------------------

        gold18 = factors.get(
            "gold18_price"
        )


        if gold18 is not None:

            score += 5

            drivers.append(
                "Gold18 price available"
            )

        else:

            risks.append(
                "Gold18 price missing"
            )



        # ---------------------------------
        # Mesghal
        # ---------------------------------

        mesghal = factors.get(
            "mesghal_price"
        )


        if mesghal is not None:

            score += 5

            drivers.append(
                "Mesghal data available"
            )



        # ---------------------------------
        # USD Dynamic Impact
        # ---------------------------------

        usd = factors.get(
            "usd_free_rate"
        )


        if usd is not None:

            if regime == "LOCAL_INFLATION":

                score += 15

                drivers.append(
                    "Strong local currency pressure"
                )

            else:

                score += 10

                drivers.append(
                    "USD market support"
                )



        # USD Momentum

        if usd_change is not None:


            if usd_change > 0:

                score += 3

                drivers.append(
                    "Positive USD momentum"
                )



        # ---------------------------------
        # Gold Momentum
        # ---------------------------------

        change = factors.get(
            "gold_daily_change"
        )


        if change is not None:


            if change > 0:

                score += 10

                drivers.append(
                    "Positive gold momentum"
                )


            elif change < 0:

                score -= 10

                risks.append(
                    "Negative gold momentum"
                )



        # ---------------------------------
        # Volume
        # ---------------------------------

        volume = factors.get(
            "volume"
        )


        if volume is not None:

            score += 2

            drivers.append(
                "Market volume available"
            )



        # ---------------------------------
        # Coin Bubble
        # ---------------------------------

        bubble = factors.get(
            "coin_bubble"
        )


        if bubble is not None:


            if bubble > 2500000:

                score -= 10

                risks.append(
                    "High coin bubble risk"
                )


            elif bubble > 1500000:

                score -= 3

                risks.append(
                    "Medium coin bubble risk"
                )


            else:

                drivers.append(
                    "Controlled coin bubble"
                )



        # ---------------------------------
        # Global Gold
        # ---------------------------------

        if xau is not None:


            if xau >= 3000:

                score += 10

                drivers.append(
                    "Strong global gold price"
                )



        # ---------------------------------
        # Bond Yield
        # ---------------------------------

        if yield10 is not None:


            if yield10 >= 4.5:

                score -= 5

                risks.append(
                    "High bond yield pressure"
                )



        # ---------------------------------
        # Regime Bonus
        # ---------------------------------

        if regime == "GOLD_STRESS":

            score += 2

            drivers.append(
                "Gold stress regime"
            )



        # Clamp

        score = max(
            0,
            min(
                100,
                score
            )
        )



        # ---------------------------------
        # Trend
        # ---------------------------------

        if score >= 75:

            trend = "BULLISH"

        elif score >= 55:

            trend = "CAUTIOUS"

        elif score <= 35:

            trend = "BEARISH"

        else:

            trend = "NEUTRAL"



        # ---------------------------------
        # Signal
        # ---------------------------------

        if score >= 70:

            signal = "BUY"

        elif score <= 40:

            signal = "SELL"

        else:

            signal = "HOLD"



        # ---------------------------------
        # Confidence
        # ---------------------------------

        confidence = min(
            95,
            40 + len(drivers) * 5
        )



        return {

            "gold_score":
                round(
                    score,
                    2
                ),

            "trend":
                trend,

            "signal":
                signal,

            "confidence":
                confidence,

            "drivers":
                drivers,

            "risks":
                risks,

            "market_regime":
                regime,

            "calculator_version":
                self.VERSION

        }
