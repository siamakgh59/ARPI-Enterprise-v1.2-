from typing import Dict, List


class MacroRiskCalculator:
    """
    Calculates macro risk score based on economic indicators.
    """

    def calculate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:

        score = 50

        drivers: List[str] = []

        # Monetary Policy
        fed_rate = factors.get("fed_rate")

        if fed_rate is not None:
            if fed_rate >= 5:
                score += 10
                drivers.append("High interest rate environment")
            elif fed_rate <= 2:
                score -= 5
                drivers.append("Low interest rate environment")


        # Inflation
        cpi = factors.get("cpi")

        if cpi is not None:
            if cpi >= 4:
                score += 10
                drivers.append("High inflation pressure")
            elif cpi <= 2:
                score -= 5
                drivers.append("Inflation controlled")


        # Dollar Index
        dxy = factors.get("dxy")

        if dxy is not None:
            if dxy >= 105:
                score += 10
                drivers.append("Strong USD pressure")
            elif dxy <= 95:
                score -= 5
                drivers.append("USD weakness support")


        # Treasury Yield
        yield10 = factors.get("us10y_yield")

        if yield10 is not None:
            if yield10 >= 4.5:
                score += 10
                drivers.append("High bond yield pressure")


        # Gold ETF Flow
        etf_flow = factors.get("gold_etf_flow")

        if etf_flow is not None:
            if etf_flow < 0:
                score += 5
                drivers.append("Gold ETF outflow")
            elif etf_flow > 0:
                score -= 5
                drivers.append("Gold ETF inflow")


        # Normalize score
        score = max(0, min(score, 100))


        if score >= 75:
            trend = "BEARISH"
        elif score >= 55:
            trend = "CAUTIOUS"
        elif score <= 35:
            trend = "BULLISH"
        else:
            trend = "NEUTRAL"


        confidence = min(
            95,
            50 + len(drivers) * 10
        )


        return {
            "macro_score": round(score, 2),
            "macro_risk": round(score, 2),
            "trend": trend,
            "confidence": confidence,
            "drivers": drivers
        }
