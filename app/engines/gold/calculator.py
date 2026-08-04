from typing import Dict, List


class GoldCalculator:
    """
    ARPI Gold Intelligence Calculator v4.1

    Responsibilities:
    - Gold factor analysis
    - Weighted scoring
    - Trend generation
    - Signal generation
    - Confidence estimation
    - Market regime support

    Note:
    Coin bubble is normalized by Provider/Normalizer layer.
    Calculator uses coin_bubble_percent.
    """


    VERSION = "4.1.0"



    def calculate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:



        score = 50


        drivers: List[str] = []

        risks: List[str] = []



        # =============================
        # Gold18 Price
        # =============================

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



        # =============================
        # Mesghal Price
        # =============================

        mesghal = factors.get(
            "mesghal_price"
        )


        if mesghal is not None:

            score += 5

            drivers.append(
                "Mesghal data available"
            )

        else:

            risks.append(
                "Mesghal data missing"
            )



        # =============================
        # USD Market
        # =============================

        usd = factors.get(
            "usd_free_rate"
        )


        if usd is not None:

            score += 10

            drivers.append(
                "USD market support"
            )

        else:

            risks.append(
                "USD market data missing"
            )



        # =============================
        # USD Momentum
        # =============================

        usd_change = factors.get(
            "usd_change"
        )


        if usd_change is not None:


            if usd_change > 0:

                score += 5

                drivers.append(
                    "Positive USD momentum"
                )


            elif usd_change < 0:

                score -= 5

                risks.append(
                    "Negative USD momentum"
                )



        # =============================
        # Gold Momentum
        # =============================

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



        # =============================
        # Volume
        # =============================

        volume = factors.get(
            "volume"
        )


        if volume is not None:

            drivers.append(
                "Market volume available"
            )



        # =============================
        # Coin Bubble Percent
        # =============================

        bubble = factors.get(
            "coin_bubble_percent"
        )


        if bubble is not None:


            if bubble >= 8:

                score -= 10

                risks.append(
                    "High coin bubble risk"
                )


            elif bubble >= 4:

                score -= 5

                risks.append(
                    "Medium coin bubble risk"
                )


            else:

                drivers.append(
                    "Controlled coin bubble"
                )



        # =============================
        # Global Gold Price
        # =============================

        xau = factors.get(
            "xau_usd"
        )


        if xau is not None:


            if xau >= 3000:

                score += 10

                drivers.append(
                    "Strong global gold price"
                )


            elif xau < 2500:

                score -= 5

                risks.append(
                    "Weak global gold price"
                )



        # =============================
        # Dollar Index
        # =============================

        dxy = factors.get(
            "dxy"
        )


        if dxy is not None:


            if dxy >= 105:

                score -= 5

                risks.append(
                    "Strong dollar pressure"
                )


            elif dxy <= 95:

                score += 5

                drivers.append(
                    "Weak dollar support"
                )



        # =============================
        # US Treasury Yield
        # =============================

        yield10 = factors.get(
            "us10y_yield"
        )


        if yield10 is not None:


            if yield10 >= 4.5:

                score -= 5

                risks.append(
                    "High bond yield pressure"
                )



        # =============================
        # Normalize Score
        # =============================

        score = max(
            0,
            min(
                100,
                score
            )
        )



        # =============================
        # Market Regime
        # =============================

        if (
            xau is not None
            and
            yield10 is not None
        ):


            if (
                xau >= 3000
                and
                yield10 >= 4.5
            ):

                market_regime = "GOLD_STRESS"

                drivers.append(
                    "Gold stress regime"
                )


            else:

                market_regime = "NORMAL"


        else:

            market_regime = None



        # =============================
        # Trend
        # =============================

        if score >= 75:

            trend = "BULLISH"


        elif score >= 55:

            trend = "CAUTIOUS"


        elif score <= 35:

            trend = "BEARISH"


        else:

            trend = "NEUTRAL"



        # =============================
        # Signal
        # =============================

        if score >= 70:

            signal = "BUY"


        elif score <= 40:

            signal = "SELL"


        else:

            signal = "HOLD"



        # =============================
        # Confidence
        # =============================

        confidence = (
            40
            +
            (
                len(drivers)
                *
                5
            )
        )


        confidence = min(
            95,
            confidence
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


            "market_regime":
                market_regime,


            "confidence":
                confidence,


            "drivers":
                drivers,


            "risks":
                risks,


            "calculator_version":
                self.VERSION

        }
