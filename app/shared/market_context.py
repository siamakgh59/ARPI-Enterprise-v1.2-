from datetime import datetime

from app.data.providers import get_best_market_data

from .models import MarketContext


def build_market_context() -> MarketContext:
    """
    Build shared global market snapshot
    """

    market_data = get_best_market_data()


    xau_usd = None
    dxy = None
    us10y_yield = None


    try:

        gold = market_data.get(
            "gold",
            []
        )

        if gold:
            xau_usd = gold[0].get(
                "price"
            )


        usd = market_data.get(
            "usd_index",
            []
        )

        if usd:
            dxy = usd[0].get(
                "price"
            )


    except Exception as e:

        print(
            "MARKET CONTEXT ERROR:",
            e
        )


    return MarketContext(

        xau_usd=xau_usd,

        dxy=dxy,

        us10y_yield=us10y_yield,

        timestamp=datetime.utcnow()

    )
