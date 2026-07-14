from .registry import get_providers
from .yahoo import YahooFinanceProvider


def get_best_market_data():

    providers = get_providers()

    assets = {
        "gold": "GC=F",
        "silver": "SI=F",
        "oil_wti": "CL=F",
        "oil_brent": "BZ=F",
        "usd_index": "DX-Y.NYB",
        "eurusd": "EURUSD=X",
        "vix": "^VIX",
        "bitcoin": "BTC-USD"
    }

    result = {}

    for name, symbol in assets.items():

        responses = []

        for provider in providers:

            response = provider.get_price(symbol)

            responses.append(
                response.to_dict()
            )

        result[name] = responses

    return result
