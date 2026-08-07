from app.shared.contracts import ARPIIntelligenceContract


def gold_to_contract(
    report: dict
) -> ARPIIntelligenceContract:
    """
    Convert Gold Engine output into the
    central ARPI Intelligence Contract.

    This adapter does NOT calculate:
    - Gold score
    - Risk score
    - Signal
    - Confidence

    It only normalizes the Gold Engine output.
    """

    data_quality = report.get(
        "data_quality",
        "UNKNOWN"
    )

    # -----------------------------------------
    # Normalize data quality
    # -----------------------------------------

    if data_quality == "WEAK":
        data_quality = "LOW"

    # -----------------------------------------
    # Build central contract
    # -----------------------------------------

    return ARPIIntelligenceContract(

        engine=report.get(
            "engine",
            "Gold Intelligence Engine"
        ),

        version=report.get(
            "version",
            "UNKNOWN"
        ),

        domain="GOLD",

        asset="gold",

        # Gold intelligence score
        score=report.get(
            "gold_score"
        ),

        # Risk belongs to Risk Engine.
        risk_score=None,

        risk_level=None,

        signal=report.get(
            "signal"
        ),

        trend=report.get(
            "trend"
        ),

        confidence=report.get(
            "confidence",
            0
        ),

        drivers=report.get(
            "drivers",
            []
        ),

        risks=report.get(
            "risks",
            []
        ),

        warnings=[],

        data_quality=data_quality,

        available_inputs=report.get(
            "available_inputs",
            0
        ),

        missing_inputs=report.get(
            "missing_inputs",
            []
        ),

        metadata={
            "market_regime": report.get(
                "market_regime"
            ),

            "source_engine":
                "Gold Intelligence Engine",

            "adapter_version":
                "1.0.0"
        },

        timestamp=report.get(
            "timestamp"
        )

    )
