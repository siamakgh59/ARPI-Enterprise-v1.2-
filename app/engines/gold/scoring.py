from typing import Dict, Any


class GoldScoringEngine:
    """
    Gold scoring model v1

    Converts market inputs into
    a normalized gold score.
    """


    def analyze(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        score = 50

        drivers = []

        risks = []


        # Iran gold price strength

        gold18 = data.get(
            "gold18_price"
        )

        mesghal = data.get(
            "mesghal_price"
        )


        if gold18:

            score += 5

            drivers.append(
                "gold18_price_available"
            )


        if mesghal:

            score += 5

            drivers.append(
                "mesghal_price_available"
            )


        # Daily movement

        daily_change = data.get(
            "gold_daily_change"
        )


        if daily_change is not None:

            if daily_change > 0:

                score += 10

                drivers.append(
                    "positive_gold_momentum"
                )


            elif daily_change < 0:

                score -= 10

                risks.append(
                    "negative_gold_momentum"
                )


        # Volume

        volume = data.get(
            "volume"
        )

        if volume:

            drivers.append(
                "volume_available"
            )



        score = max(
            0,
            min(
                100,
                score
            )
        )


        return {

            "gold_score":
                score,

            "drivers":
                drivers,

            "risks":
                risks
        }
