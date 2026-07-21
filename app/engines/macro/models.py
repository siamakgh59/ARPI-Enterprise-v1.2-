from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Dict


class MacroData(BaseModel):
    """
    Raw macroeconomic input data
    """

    fed_rate: float | None = Field(
        default=None,
        description="Federal Funds Rate"
    )

    cpi: float | None = Field(
        default=None,
        description="Consumer Price Index"
    )

    pce: float | None = Field(
        default=None,
        description="Personal Consumption Expenditures"
    )

    nfp: float | None = Field(
        default=None,
        description="Non Farm Payroll"
    )

    dxy: float | None = Field(
        default=None,
        description="US Dollar Index"
    )

    us10y_yield: float | None = Field(
        default=None,
        description="US 10 Year Treasury Yield"
    )

    gold_etf_flow: float | None = Field(
        default=None,
        description="Gold ETF Net Flow"
    )

    central_bank_gold_purchase: float | None = Field(
        default=None,
        description="Central Bank Gold Purchase"
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


class MacroReport(BaseModel):
    """
    Standard output contract of Macro Intelligence Engine

    Designed for:
    - Dashboard
    - Risk Intelligence Engine (RIE)
    - Fusion AI Engine
    """

    engine: str = "Macro Intelligence Engine"

    version: str = "1.0.0"

    macro_score: float = 0

    macro_risk: float = 0

    trend: str = "NEUTRAL"

    confidence: float = 0

    drivers: List[str] = Field(
        default_factory=list
    )

    # Data quality information
    data_quality: str = "UNKNOWN"

    available_inputs: int = 0

    missing_inputs: List[str] = Field(
        default_factory=list
    )

    # Future expansion:
    # provider name, source timestamp, API status, etc.
    metadata: Dict = Field(
        default_factory=dict
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )
