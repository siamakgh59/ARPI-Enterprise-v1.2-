from typing import Dict, List


class GoldCalculator:
    """
    ARPI Gold Intelligence Calculator v3.4

    Responsibilities:

    - Gold factor analysis
    - Dynamic weighted scoring
    - Trend generation
    - Signal generation
    - Confidence estimation

    Input:
        Normalized Gold Data

    Output:
        Intelligence Score
    """


    VERSION = "3.4.0"



    def calculate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:


        score = 50


        drivers: List[str] = []

        risks: List[str] = []



        # =================================================
        # Local Gold Market
        # =================================================


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



        # =================================================
        # USD Market
        # =================================================


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



        usd_change = factors.get(
            "usd_change"
        )


        if usd_change is not None:


            if usd_change > 1:

                score += 3

                drivers.append(
                    "Positive USD momentum"
                )


            elif usd_change < -1:

                score -= 3

                risks.append(
                    "USD weakness"
                )



        # =================================================
        # Gold Momentum
        # =================================================


        gold_change = factors.get(
            "gold_daily_change"
        )


        if gold_change is not None:


            if gold_change > 0:

                score += 10

                drivers.append(
                    "Positive gold momentum"
                )


            elif gold_change < 0:

                score -= 10

                risks.append(
                    "Negative gold momentum"
                )



        # =================================================
        # Volume
        # =================================================


        volume = factors.get(
            "volume"
        )


        if volume is not None:

            score += 2

            drivers.append(
                "Market volume available"
            )



        # =================================================
        # Coin Bubble
        # =================================================


        bubble = factors.get(
            "coin_bubble"
        )


        coin = factors.get(
            "coin_emami"
        )


        bubble_percent = None



        if (
            bubble is not None
            and
            coin is not None
            and
            coin > 0
        ):

            bubble_percent = (
                bubble
                /
                coin
            ) * 100



            if bubble_percent >= 12:


                score -= 10


                risks.append(
                    "High coin bubble risk"
                )


            elif bubble_percent >= 7:


                score -= 5


                risks.append(
                    "Medium coin bubble risk"
                )


            else:


                drivers.append(
                    "Controlled coin bubble"
                )



        # =================================================
        # Global Gold Market
        # =================================================


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



        # =================================================
        # Dollar Index
        # =================================================


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



        # =================================================
        # US Treasury Yield
        # =================================================


        us10y = factors.get(
            "us10y_yield"
        )


        if us10y is not None:


            if us10y >= 4.5:


                score -= 5


                risks.append(
                    "High bond yield pressure"
                )



        # =================================================
        # Normalize Score
        # =================================================


        score = max(
            0,
            min(
                100,
                score
            )
        )



        # =================================================
        # Trend
        # =================================================


        if score >= 75:

            trend = "BULLISH"


        elif score >= 55:

            trend = "CAUTIOUS"


        elif score <= 35:

            trend = "BEARISH"


        else:

            trend = "NEUTRAL"



        # =================================================
        # Signal
        # =================================================


        if score >= 70:

            signal = "BUY"


        elif score <= 40:

            signal = "SELL"


        else:

            signal = "HOLD"



        # =================================================
        # Confidence
        # =================================================


        confidence = (
            40
            +
            len(drivers) * 5
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


            "confidence":
                confidence,


            "drivers":
                drivers,


            "risks":
                risks,


            "calculator_version":
                self.VERSION

        }
