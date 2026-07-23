from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class GoldData(BaseModel):
    """
    Gold Intelligence Engine Input Model
    Iran + Global Gold Market
    """

    # Global Market

    xau_usd: Optional[float] = None

    dxy: Optional[float] = None

    us10y_yield: Optional[float] = None


    # Iran Market

    usd_free_rate: Optional[float] = None

    usd_change: Optional[float] = None

    gold18_price: Optional[float] = None

    mesghal_price: Optional[float] = None

    coin_emami: Optional[float] = None

    coin_bahar: Optional[float] = None

    coin_bubble: Optional[float] = None


    # Market Behavior

    gold_daily_change: Optional[float] = None

    volume: Optional[float] = None


    timestamp: Optional[datetime] = None



class GoldReport(BaseModel):
    """
    Gold Intelligence Engine Output
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
