from typing import Dict, List


class MacroRiskCalculator:
    """
    Calculates macro risk score based on economic indicators.

    ARPI Macro Intelligence Engine v1.1
    """

    def calculate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:

        score = 50

        drivers: List[str] = []


        # -----------------------------
        # Monetary Policy
        # -----------------------------

        fed_rate = factors.get(
            "fed_rate"
        )

        if fed_rate is not None:

            if fed_rate >= 5:
                score += 10
                drivers.append(
                    "High interest rate environment"
                )

            elif fed_rate <= 2:
                score -= 5
                drivers.append(
                    "Low interest rate environment"
                )


        # -----------------------------
        # CPI Inflation
        # -----------------------------

        cpi = factors.get(
            "cpi"
        )

        if cpi is not None:

            if cpi >= 4:
                score += 10
                drivers.append(
                    "High CPI inflation pressure"
                )

            elif cpi <= 2:
                score -= 5
                drivers.append(
                    "Inflation controlled"
                )


        # -----------------------------
        # PCE Inflation
        # -----------------------------

        pce = factors.get(
            "pce"
        )

        if pce is not None:

            if pce >= 3:
                score += 5
                drivers.append(
                    "High PCE inflation pressure"
                )

            elif pce <= 2:
                score -= 3
                drivers.append(
                    "PCE inflation easing"
                )


        # -----------------------------
        # Employment / NFP
        # -----------------------------

        nfp = factors.get(
            "nfp"
        )

        if nfp is not None:

            if nfp < 150000:
                score -= 5
                drivers.append(
                    "Weak labor market"
                )

            elif nfp > 250000:
                score += 5
                drivers.append(
                    "Strong labor market"
                )


        # -----------------------------
        # Dollar Index
        # -----------------------------

        dxy = factors.get(
            "dxy"
        )

        if dxy is not None:

            if dxy >= 105:
                score += 10
                drivers.append(
                    "Strong USD pressure"
                )

            elif dxy <= 95:
                score -= 5
                drivers.append(
                    "USD weakness support"
                )


        # -----------------------------
        # Treasury Yield
        # -----------------------------

        yield10 = factors.get(
            "us10y_yield"
        )

        if yield10 is not None:

            if yield10 >= 4.5:
                score += 10
                drivers.append(
                    "High bond yield pressure"
                )


        # -----------------------------
        # Gold ETF Flow
        # Positive flow = Gold demand
        # -----------------------------

        etf_flow = factors.get(
            "gold_etf_flow"
        )

        if etf_flow is not None:

            if etf_flow > 0:
                score -= 5
                drivers.append(
                    "Gold ETF inflow supports gold demand"
                )

            elif etf_flow < 0:
                score += 5
                drivers.append(
                    "Gold ETF outflow pressure"
                )


        # -----------------------------
        # Central Bank Gold Purchase
        # -----------------------------

        cb_gold = factors.get(
            "central_bank_gold_purchase"
        )

        if cb_gold is not None:

            if cb_gold > 0:
                score -= 5
                drivers.append(
                    "Central bank gold accumulation"
                )


        # -----------------------------
        # Normalize
        # -----------------------------

        score = max(
            0,
            min(score, 100)
        )


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

            "macro_score": round(
                score,
                2
            ),

            "macro_risk": round(
                score,
                2
            ),

            "trend": trend,

            "confidence": confidence,

            "drivers": drivers

        }
