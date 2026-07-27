from typing import Dict

class GoldScoringEngine:
    """
    ARPI Gold Intelligence Engine
    Scoring Module v3.2

    Responsible for:
    - Factor scoring
    - Weight calculation
    - Final gold score generation
    """

    VERSION = "3.2.0"

    WEIGHTS = {
        "gold18_price": 0.20,
        "mesghal_price": 0.15,
        "usd_free_rate": 0.20,
        "gold_daily_change": 0.15,
        "volume": 0.10,
        "coin_bubble": 0.10,
        "global_factor": 0.10,
    }

    def analyze(
        self,
        data: Dict
    ) -> Dict:

        scores = {}

        drivers = []

        risks = []

        # ---------------------------------
        # Gold18
        # ---------------------------------

        gold18 = data.get(
            "gold18_price"
        )

        if gold18:

            scores["gold18_price"] = 70

            drivers.append(
                "Gold18 price available"
            )

        else:

            scores["gold18_price"] = 50

            risks.append(
                "Gold18 price missing"
            )

        # ---------------------------------
        # Mesghal
        # ---------------------------------

        mesghal = data.get(
            "mesghal_price"
        )

        if mesghal:

            scores["mesghal_price"] = 70

            drivers.append(
                "Mesghal data available"
            )

        else:

            scores["mesghal_price"] = 50

        # ---------------------------------
        # USD
        # ---------------------------------

        usd = data.get(
            "usd_free_rate"
        )

        if usd:

            scores["usd_free_rate"] = 65

            drivers.append(
                "USD market support"
            )

        else:

            scores["usd_free_rate"] = 50

            risks.append(
                "USD data missing"
            )

        # ---------------------------------
        # Daily Change
        # ---------------------------------

        change = data.get(
            "gold_daily_change"
        )

        if change is not None:

            if change > 0:

                scores["gold_daily_change"] = 75

                drivers.append(
                    "Positive gold momentum"
                )

            elif change < 0:

                scores["gold_daily_change"] = 35

                risks.append(
                    "Negative gold momentum"
                )

            else:

                scores["gold_daily_change"] = 50

        else:

            scores["gold_daily_change"] = 50

        # ---------------------------------
        # Volume
        # ---------------------------------

        volume = data.get(
            "volume"
        )

        if volume:

            scores["volume"] = 65

            drivers.append(
                "Market volume available"
            )

        else:

            scores["volume"] = 50

        # ---------------------------------
        # Coin Bubble
        # ---------------------------------

        bubble = data.get(
            "coin_bubble"
        )

        if bubble is None:

            scores[
                "coin_bubble"
            ] = 50

        else:

            # اگر مقدار حباب ریالی باشد
            # تبدیل به درصد واقعی

            if bubble > 1000:

                coin = data.get(
                    "coin_emami"
                )

                mesghal = data.get(
                    "mesghal_price"
                )

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

            # درصد واقعی حباب

            if bubble < 2:

                scores[
                    "coin_bubble"
                ] = 85

            elif bubble < 5:

                scores[
                    "coin_bubble"
                ] = 60

                risks.append(
                    "Medium coin bubble risk"
                )

            else:

                scores[
                    "coin_bubble"
                ] = 30

                risks.append(
                    "High coin bubble risk"
                )

        # ---------------------------------
        # Global Factor
        # ---------------------------------

        scores[
            "global_factor"
        ] = 50

        # ---------------------------------
        # Weighted Final Score
        # ---------------------------------

        final_score = 0

        for factor, weight in self.WEIGHTS.items():

            final_score += (

                scores.get(
                    factor,
                    50
                )

                *

                weight

            )

        final_score = round(
            final_score,
            2
        )

        # ---------------------------------
        # Trend
        # ---------------------------------

        if final_score >= 75:

            trend = "BULLISH"

        elif final_score >= 55:

            trend = "CAUTIOUS"

        else:

            trend = "BEARISH"

        # ---------------------------------
        # Return
        # ---------------------------------

        return {

            "gold_score": final_score,

            "factor_scores": scores,

            "trend": trend,

            "drivers": drivers,

            "risks": risks,

            "engine_version": self.VERSION

        }
