from typing import Dict


class GoldScoringEngine:
    """
    ARPI Gold Intelligence Engine
    Scoring Module v2.0

    Responsible for:
    - Factor scoring
    - Weight calculation
    - Final gold score generation
    """

    VERSION = "2.0.0"

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
        """
        Calculate Gold Score
        """

        scores = {}
        drivers = []
        risks = []


        # Gold 18 Price

        gold18 = data.get("gold18_price")

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


        # Mesghal

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



        # USD Free Rate

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


        # Daily Change

        change = data.get(
            "gold_daily_change"
        )

        if change:

            if change > 0:

                scores[
                    "gold_daily_change"
                ] = 75

                drivers.append(
                    "Positive gold momentum"
                )

            else:

                scores[
                    "gold_daily_change"
                ] = 35

                risks.append(
                    "Negative gold momentum"
                )

        else:

            scores[
                "gold_daily_change"
            ] = 50



        # Volume

        volume = data.get(
            "volume"
        )

        if volume:

            scores[
                "volume"
            ] = 65

        else:

            scores[
                "volume"
            ] = 50



        # Coin Bubble

        bubble = data.get(
            "coin_bubble"
        )

        if bubble:

            if bubble > 20:

                scores[
                    "coin_bubble"
                ] = 30

                risks.append(
                    "High coin bubble"
                )

            else:

                scores[
                    "coin_bubble"
                ] = 70

        else:

            scores[
                "coin_bubble"
            ] = 50



        # Global Factor Placeholder

        scores[
            "global_factor"
        ] = 50



        # Weighted Score

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


        return {

            "gold_score": round(
                final_score,
                2
            ),

            "factor_scores": scores,

            "drivers": drivers,

            "risks": risks,

            "engine_version": self.VERSION

        }
