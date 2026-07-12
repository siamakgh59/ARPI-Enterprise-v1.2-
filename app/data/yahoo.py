import yfinance as yf

from .providers import MarketProvider, ProviderResponse


class YahooFinanceProvider(MarketProvider):

    def get_price(self, symbol: str):

        try:
            ticker = yf.Ticker(symbol)

            data = ticker.history(
                period="1d",
                interval="1m"
            )

            if data.empty:
                return ProviderResponse(
                    symbol=symbol,
                    price=0,
                    change=0
                )

            last_price = float(
                data["Close"].iloc[-1]
            )

            first_price = float(
                data["Close"].iloc[0]
            )

            change = (
                (last_price - first_price)
                / first_price
            ) * 100

            return ProviderResponse(
                symbol=symbol,
                price=round(last_price, 4),
                change=round(change, 2)
            )

        except Exception:
            return ProviderResponse(
                symbol=symbol,
                price=0,
                change=0
            )


def get_market_snapshot():

    provider = YahooFinanceProvider()

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

        result[name] = (
            provider
            .get_price(symbol)
            .to_dict()
        )

    return result
