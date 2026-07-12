import statistics
import yfinance as yf


class ProviderResponse:

    def __init__(
        self,
        provider,
        symbol,
        price=0.0,
        change=0.0,
        success=False
    ):
        self.provider = provider
        self.symbol = symbol
        self.price = price
        self.change = change
        self.success = success


class YahooProvider:

    name = "Yahoo Finance"

    def get_price(self, symbol):

        try:

            ticker = yf.Ticker(symbol)

            data = ticker.history(
                period="1d",
                interval="5m"
            )

            if data.empty:
                return ProviderResponse(
                    self.name,
                    symbol,
                    success=False
                )

            last_price = float(
                data["Close"].iloc[-1]
            )

            first_price = float(
                data["Close"].iloc[0]
            )

            change = 0

            if first_price != 0:
                change = (
                    (last_price - first_price)
                    / first_price
                ) * 100

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


class SymbolResolver:

    symbols = {

        "gold": [
            "GC=F",
            "XAUUSD=X",
            "GOLD",
            "GLD",
            "IAU"
        ],

        "silver": [
            "SI=F",
            "XAGUSD=X",
            "SLV"
        ],

        "oil_wti": [
            "CL=F",
            "USO"
        ],

        "oil_brent": [
            "BZ=F",
            "BNO"
        ],

        "usd_index": [
            "DX-Y.NYB",
            "DX=F",
            "UUP"
        ],

        "eurusd": [
            "EURUSD=X"
        ],

        "vix": [
            "^VIX"
        ],

        "bitcoin": [
            "BTC-USD"
        ]
    }


class MarketDataManager:

    def __init__(self):

        self.providers = [
            YahooProvider()
        ]


    def get_asset_price(self, asset):

        candidates = SymbolResolver.symbols[asset]

        responses = []


        for symbol in candidates:

            for provider in self.providers:

                result = provider.get_price(symbol)

                if result.success and result.price > 0:

                    responses.append(result)


        if not responses:

            return {

                "price": 0,
                "change": 0,
                "confidence": 0,
                "provider": "No Data"

            }


        prices = [
            r.price for r in responses
        ]


        if len(prices) == 1:

            final_price = prices[0]
            confidence = 70

        else:

            final_price = round(
                statistics.median(prices),
                4
            )

            confidence = 90


        avg_change = round(
            sum(
                r.change
                for r in responses
            )
            /
            len(responses),
            2
        )


        return {

            "price": final_price,
            "change": avg_change,
            "confidence": confidence,
            "providers": [
                r.provider
                for r in responses
            ],

            "symbols": [
                r.symbol
                for r in responses
            ]

        }



def get_best_market_data():

    manager = MarketDataManager()

    result = {}


    for asset in SymbolResolver.symbols:

        result[asset] = (
            manager
            .get_asset_price(asset)
        )


    return result
