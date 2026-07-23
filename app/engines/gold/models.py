from typing import List


class GoldReport(BaseModel):
    """
    Gold Intelligence Engine output
    """

    engine: str = "Gold Intelligence Engine"

    version: str = "1.0.0"


    gold_score: float = 0


    trend: str = "NEUTRAL"


    signal: str = "HOLD"


    confidence: float = 0


    drivers: List[str] = Field(
        default_factory=list
    )


    risks: List[str] = Field(
        default_factory=list
    )


    data_quality: str = "UNKNOWN"


    available_inputs: int = 0


    missing_inputs: List[str] = Field(
        default_factory=list
    )
