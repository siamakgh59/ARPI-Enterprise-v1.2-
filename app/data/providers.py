import statistics
import yfinance as yf


class ProviderResponse:

    def __init__(self, provider, symbol, price=0.0, change=0.0, success=False):

        self.provider = provider
        self.symbol = symbol
        self.price = price
        self.change = change
        self.success = success

    def to_dict(self):

        return {
            "provider": self.provider,
            "symbol": self.symbol,
            "price": self.price,
            "change": self.change,
            "success": self.success
        }


class YahooProvider:

    name = "Yahoo Finance"

    def get_price(self, symbol):

        try:

            ticker = yf.Ticker(symbol)

            data = ticker.history(
                period="1d",
                interval="1m"
            )

            if data.empty:

                return ProviderResponse(
                    self.name,
                    symbol,
                    success=False
                )

            last_price = float(data["Close"].iloc[-1])

            first_price = float(data["Close"].iloc[0])

            change = ((last_price - first_price) / first_price) * 100

            return ProviderResponse(
                self.name,
                symbol,
                round(last_price, 4),
                round(change, 2),
                True
            )

        except Exception:

            return ProviderResponse(
                self.name,
                symbol,
                success=False
            )


class AlphaVantageProvider:

    name = "Alpha Vantage"

    def get_price(self, symbol):

        return ProviderResponse(
            self.name,
            symbol,
            success=False
        )


class TwelveDataProvider:

    name = "Twelve Data"

    def get_price(self, symbol):

        return ProviderResponse(
            self.name,
            symbol,
            success=False
        )


class FMPProvider:

    name = "Financial Modeling Prep"

    def get_price(self, symbol):

        return ProviderResponse(
            self.name,
            symbol,
            success=False
        )

class MarketDataManager:

    def __init__(self):

        self.providers = [
            YahooProvider(),
            AlphaVantageProvider(),
            TwelveDataProvider(),
            FMPProvider()
        ]

    def get_best_price(self, symbol):

        responses = []

        for provider in self.providers:

            result = provider.get_price(symbol)

            if result.success and result.price > 0:

                responses.append(result)

        if len(responses) == 0:

            return {
                "symbol": symbol,
                "price": 0,
                "change": 0,
                "confidence": 0,
                "provider": "No Data"
            }

        prices = [r.price for r in responses]

        if len(prices) == 1:

            final_price = prices[0]

            confidence = 60

        elif len(prices) == 2:

            final_price = round(sum(prices) / 2, 4)

            confidence = 80

        else:

            final_price = round(statistics.median(prices), 4)

            confidence = 95

        avg_change = round(
            sum(r.change for r in responses) / len(responses),
            2
        )

        providers = [r.provider for r in responses]

        return {
            "symbol": symbol,
            "price": final_price,
            "change": avg_change,
            "confidence": confidence,
            "providers": providers
        }


def get_best_market_data():

    manager = MarketDataManager()

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

        result[name] = manager.get_best_price(symbol)

    return result
