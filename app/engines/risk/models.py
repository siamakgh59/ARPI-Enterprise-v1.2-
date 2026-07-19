from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskRequest(BaseModel):
    asset: str

    market_risk: float = 0
    volatility_risk: float = 0
    macro_risk: float = 0
    liquidity_risk: float = 0
    geopolitical_risk: float = 0
    data_confidence_risk: float = 0


class RiskReport(BaseModel):

    asset: str

    risk_score: float

    risk_level: RiskLevel

    components: dict

    confidence: float

    timestamp: datetime
