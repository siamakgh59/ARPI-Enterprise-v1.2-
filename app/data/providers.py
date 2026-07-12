import statistics
import yfinance as yf
import pandas as pd
print("ARPI PROVIDERS ENGINE v2 LOADED")

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


class BaseProvider:

    name = "Base"

    def get_price(self, symbol):

        return ProviderResponse(
            self.name,
            symbol,
            success=False
        )


class YahooProvider(BaseProvider):

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
                    /
                    first_price
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


class StooqProvider(BaseProvider):

    name = "Stooq"

    symbols = {

        "GC=F": "gc.f",
        "SI=F": "si.f",
        "DX-Y.NYB": "dxy"

    }


    def get_price(self, symbol):

        try:

            if symbol not in self.symbols:

                return ProviderResponse(
                    self.name,
                    symbol,
                    success=False
                )


            url = (
                "https://stooq.com/q/d/l/"
                "?s="
                + self.symbols[symbol]
                + "&i=d"
            )


            data = pd.read_csv(url)


            if data.empty:

                return ProviderResponse(
                    self.name,
                    symbol,
                    success=False
                )


            price = float(
                data["Close"].iloc[-1]
            )


            return ProviderResponse(
                self.name,
                symbol,
                round(price, 4),
                0,
                True
            )


        except Exception:

            return ProviderResponse(
                self.name,
                symbol,
                success=False
            )
            class SymbolResolver:

    assets = {

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

            YahooProvider(),
            StooqProvider()

        ]


    def calculate_confidence(self, responses):

        unique_providers = len(
            set(
                r.provider
                for r in responses
            )
        )


        if unique_providers == 1:

            return 70


        elif unique_providers == 2:

            return 85


        else:

            return 95



    def get_asset_price(self, asset):

        symbols = SymbolResolver.assets[asset]

        responses = []


        for symbol in symbols:

            for provider in self.providers:

                result = provider.get_price(symbol)


                if (
                    result.success
                    and result.price > 0
                ):

                    responses.append(result)



        if not responses:

            return {

                "price": 0,
                "change": 0,
                "confidence": 0,
                "provider": "No Data"

            }



        prices = [

            r.price

            for r in responses

        ]


        final_price = round(
            statistics.median(prices),
            4
        )


        avg_change = round(

            sum(
                r.change
                for r in responses
            )
            /
            len(responses),

            2

        )


        confidence = self.calculate_confidence(
            responses
        )


        providers = sorted(
            set(
                r.provider
                for r in responses
            )
        )


        symbols = sorted(
            set(
                r.symbol
                for r in responses
            )
        )


        return {

            "price": final_price,

            "change": avg_change,

            "confidence": confidence,

            "providers": providers,

            "symbols": symbols

        }
        def get_best_market_data():

    manager = MarketDataManager()

    result = {}


    for asset in SymbolResolver.assets:

        result[asset] = (
            manager
            .get_asset_price(asset)
        )


    return result
