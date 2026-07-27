from typing import Dict, List


class GoldCalculator:
    """
    ARPI Gold Intelligence Calculator v3.2

    Responsible for:
    - Gold factor analysis
    - Weighted scoring
    - Trend generation
    - Signal generation
    - Confidence estimation
    - Coin bubble normalization
    """


    VERSION = "3.2.0"



    def calculate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:


        score = 50

        drivers: List[str] = []

        risks: List[str] = []



        # --------------------------------
        # Gold 18 Price
        # --------------------------------

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



        # --------------------------------
        # Mesghal Price
        # --------------------------------

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



        # --------------------------------
        # USD Free Rate
        # --------------------------------

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



        # --------------------------------
        # Gold Daily Momentum
        # --------------------------------

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



        # --------------------------------
        # Volume
        # --------------------------------

        volume = factors.get(
            "volume"
        )


        if volume is not None:

            drivers.append(
                "Market volume available"
            )



        # --------------------------------
        # Coin Bubble Normalization
        # --------------------------------

        bubble = factors.get(
            "coin_bubble"
        )


        coin = factors.get(
            "coin_emami"
        )


        if bubble is not None:


            # Faraz ممکن است مقدار ریالی بدهد
            # تبدیل به درصد واقعی

            if bubble > 1000:


                if coin and mesghal:


                    theoretical_price = (
                        mesghal * 0.235
                    )


                    bubble = (
                        (
                            coin
                            -
                            theoretical_price
                        )
                        /
                        theoretical_price
                    ) * 100


                    bubble = round(
                        bubble,
                        2
                    )


                    print(
                        "NORMALIZED COIN BUBBLE %",
                        bubble
                    )



            # تحلیل درصد حباب

            if bubble >= 10:

                score -= 10

                risks.append(
                    "High coin bubble risk"
                )


            elif bubble >= 5:

                score -= 5

                risks.append(
                    "Medium coin bubble risk"
                )


            else:

                drivers.append(
                    "Controlled coin bubble"
                )



        # --------------------------------
        # Global Gold (XAU/USD)
        # --------------------------------

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



        # --------------------------------
        # Dollar Index
        # --------------------------------

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



        # --------------------------------
        # US10Y Yield
        # --------------------------------

        yield10 = factors.get(
            "us10y_yield"
        )


        if yield10 is not None:


            if yield10 >= 4.5:

                score -= 5

                risks.append(
                    "High bond yield pressure"
                )



        # --------------------------------
        # Normalize
        # --------------------------------

        score = max(
            0,
            min(
                100,
                score
            )
        )



        # --------------------------------
        # Trend
        # --------------------------------

        if score >= 75:

            trend = "BULLISH"


        elif score >= 55:

            trend = "CAUTIOUS"


        elif score <= 35:

            trend = "BEARISH"


        else:

            trend = "NEUTRAL"



        # --------------------------------
        # Signal
        # --------------------------------

        if score >= 70:

            signal = "BUY"


        elif score <= 40:

            signal = "SELL"


        else:

            signal = "HOLD"



        # --------------------------------
        # Confidence
        # --------------------------------

        confidence = (
            40
            +
            (len(drivers) * 5)
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
