from datetime import datetime
from pydantic import BaseModel


class MarketContext(BaseModel):
    """
    Shared Market Data Context

    Single source of truth for:
    - Gold Engine
    - Macro Engine
    - Risk Engine
    - Fusion Engine
    """

    xau_usd: float | None = None

    dxy: float | None = None

    us10y_yield: float | None = None

    timestamp: datetime = datetime.utcnow()
