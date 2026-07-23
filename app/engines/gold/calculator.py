from typing import Dict, List


class GoldCalculator:
    """
    Calculates gold market intelligence score.
    """

    def calculate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:

        score = 50

        drivers: List[str] = []

        risks: List[str] = []


        # Global Gold Price

        xau_usd = factors.get("xau_usd")

        if xau_usd is not None:

            if xau_usd >= 3000:
                score += 15
                drivers.append(
                    "Strong global gold price"
                )

            elif xau_usd <= 2500:
                score -= 5
                risks.append(
                    "Weak global gold price"
                )


        # Iran Dollar

        usd_irr = factors.get("usd_irr")

        if usd_irr is not None:

            if usd_irr >= 900000:
                score += 15
                drivers.append(
                    "High USD/IRR pressure"
                )


        # US Dollar Index

        dxy = factors.get("dxy")

        if dxy is not None:

            if dxy >= 105:
                score -= 10
                risks.append(
                    "Strong dollar pressure"
                )

            elif dxy <= 95:
                score += 5
                drivers.append(
                    "Weak dollar support"
                )


        # US 10Y Yield

        yield10 = factors.get(
            "us10y_yield"
        )

        if yield10 is not None:

            if yield10 >= 4.5:

                score -= 10

                risks.append(
                    "High bond yield pressure"
                )


        # ETF Flow

        etf_flow = factors.get(
            "gold_etf_flow"
        )

        if etf_flow is not None:

            if etf_flow > 0:

                score += 5

                drivers.append(
                    "Gold ETF inflow"
                )

            elif etf_flow < 0:

                score -= 5

                risks.append(
                    "Gold ETF outflow"
                )


        # Coin Bubble Risk

        bubble = factors.get(
            "coin_bubble"
        )

        if bubble is not None:

            if bubble >= 15:

                score -= 10

                risks.append(
                    "High coin bubble risk"
                )


        # Normalize

        score = max(
            0,
            min(score, 100)
        )


        # Trend

        if score >= 75:

            trend = "BULLISH"

        elif score >= 55:

            trend = "CAUTIOUS"

        elif score <= 35:

            trend = "BEARISH"

        else:

            trend = "NEUTRAL"



        # Signal

        if score >= 70:

            signal = "BUY"

        elif score <= 40:

            signal = "SELL"

        else:

            signal = "HOLD"



        confidence = min(
            95,
            50 + (
                len(drivers)
                +
                len(risks)
            ) * 5
        )


        return {

            "gold_score": round(score, 2),

            "trend": trend,

            "signal": signal,

            "confidence": confidence,

            "drivers": drivers,

            "risks": risks

        }
