from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class GoldData(BaseModel):
    """
    Input data model for Gold Intelligence Engine
    """

    xau_usd: Optional[float] = None

    usd_irr: Optional[float] = None

    gold18_price: Optional[float] = None

    coin_emami: Optional[float] = None

    coin_bubble: Optional[float] = None

    dxy: Optional[float] = None

    us10y_yield: Optional[float] = None

    gold_etf_flow: Optional[float] = None

    central_bank_gold_purchase: Optional[float] = None

    timestamp: Optional[datetime] = None



class GoldReport(BaseModel):
    """
    Output report from Gold Intelligence Engine
    """

    engine: str

    version: str

    gold_score: float

    trend: str

    signal: str

    confidence: float

    drivers: List[str]

    risks: List[str]

    data_quality: str

    available_inputs: int

    missing_inputs: List[str]

    timestamp: datetime = datetime.utcnow()
