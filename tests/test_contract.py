from app.shared.contracts import ARPIIntelligenceContract


def test_arpi_contract():

    contract = ARPIIntelligenceContract(

        engine="Gold Intelligence Engine",

        version="4.2.0",

        domain="GOLD",

        asset="gold",

        score=75,

        signal="BUY",

        trend="BULLISH",

        confidence=85

    )


    assert contract.engine == "Gold Intelligence Engine"

    assert contract.domain == "GOLD"

    assert contract.score == 75

    assert contract.signal == "BUY"

    assert contract.confidence == 85
