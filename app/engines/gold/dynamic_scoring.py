from typing import Dict, List


class DynamicGoldScoringEngine:
    """
    ============================================
    ARPI Dynamic Gold Scoring Engine v1.0
    ============================================

    مسئولیت:

    - تبدیل داده‌های بازار به امتیاز هوشمند
    - تولید Drivers
    - تولید Risks
    - تعیین Market Regime
    - آماده برای توسعه AI Layer
    """

    VERSION = "1.0.0"


    def __init__(self):

        self.base_score = 50



    def calculate(
        self,
        data: Dict
    ) -> Dict:


        score = self.base_score

        drivers: List[str] = []

        risks: List[str] = []



        # ==================================
        # Iran Gold Market
        # ==================================

        gold18 = data.get(
            "gold18_price"
        )

        mesghal = data.get(
            "mesghal_price"
        )


        if gold18:

            score += 5

            drivers.append(
                "Gold18 price available"
            )


        if mesghal:

            score += 5

            drivers.append(
                "Mesghal data available"
            )



        # ==================================
        # USD Intelligence
        # ==================================

        usd = data.get(
            "usd_free_rate"
        )

        usd_change = data.get(
            "usd_change"
        )


        if usd:

            score += 5

            drivers.append(
                "USD market support"
            )


        if usd_change and usd_change > 0:

            score += 5

            drivers.append(
                "Positive USD momentum"
            )



        # ==================================
        # Volume
        # ==================================

        volume = data.get(
            "volume"
        )


        if volume:

            score += 3

            drivers.append(
                "Market volume available"
            )



        # ==================================
        # Global Gold
        # ==================================

        xau = data.get(
            "xau_usd"
        )


        if xau:

            if xau > 4000:

                score += 7

                drivers.append(
                    "Strong global gold price"
                )


            elif xau < 3000:

                score -= 5

                risks.append(
                    "Weak global gold price"
                )



        # ==================================
        # Gold Momentum
        # ==================================

        daily = data.get(
            "gold_daily_change"
        )


        if daily is not None:


            if daily > 0:

                score += 5

                drivers.append(
                    "Positive gold momentum"
                )


            elif daily < 0:

                score -= 5

                risks.append(
                    "Negative gold momentum"
                )



        # ==================================
        # Bond Yield Pressure
        # ==================================

        yield10 = data.get(
            "us10y_yield"
        )


        if yield10:

            if yield10 > 4:

                score -= 5

                risks.append(
                    "High bond yield pressure"
                )



        # ==================================
        # Coin Bubble
        # ==================================

        bubble = data.get(
            "coin_bubble_percent"
        )


        if bubble:


            if bubble > 3:

                score -= 8

                risks.append(
                    "High coin bubble risk"
                )


            elif bubble < 2:

                drivers.append(
                    "Controlled coin bubble"
                )



        # ==================================
        # Clamp Score
        # ==================================

        score = max(
            0,
            min(
                100,
                score
            )
        )



        # ==================================
        # Market Regime
        # ==================================

        if score >= 80:

            regime = "BULLISH"


        elif score <= 55:

            regime = "GOLD_STRESS"


        else:

            regime = "BALANCED"



        # ==================================
        # Signal
        # ==================================

        if score >= 70:

            signal = "BUY"

        elif score <= 45:

            signal = "SELL"

        else:

            signal = "HOLD"



        return {

            "gold_score": score,

            "signal": signal,

            "market_regime": regime,

            "confidence": 70,

            "drivers": drivers,

            "risks": risks

        }
