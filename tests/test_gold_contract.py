from app.engines.gold.adapters.contract import gold_to_contract


def test_gold_contract():

    gold_report = {

        "engine": "Gold Intelligence Engine",

        "version": "4.2.0",

        "gold_score": 78,

        "trend": "BULLISH",

        "signal": "BUY",

        "market_regime": "GOLD_BULL",

        "confidence": 85,

        "drivers": [

            "Positive gold momentum",

            "USD market support"

        ],

        "risks": [

            "High bond yield pressure"

        ],

        "data_quality": "GOOD",

        "available_inputs": 9,

        "missing_inputs": [

            "gold_etf_flow"

        ]

    }


    contract = gold_to_contract(
        gold_report
    )


    print(
        contract.model_dump()
    )


    assert contract.domain == "GOLD"

    assert contract.asset == "gold"

    assert contract.score == 78

    assert contract.signal == "BUY"

    assert contract.confidence == 85

    assert contract.data_quality == "GOOD"
