from pydantic import BaseModel
from typing import Dict, List, Any


class DashboardSummary(BaseModel):
    application: str
    version: str
    status: str
    arpi_score: float
    market_status: str
    risk_level: str
    confidence: float
    assets: Dict[str, Any]
    signals: List[str]
