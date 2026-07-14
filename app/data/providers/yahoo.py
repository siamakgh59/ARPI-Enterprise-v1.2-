import yfinance as yf

from . import MarketProvider, ProviderResponse


class YahooFinanceProvider(MarketProvider):

    name = "Yahoo Finance"

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
                    change=0,
                    provider=self.name
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
            ) * 100 if first_price else 0

            return ProviderResponse(
                symbol=symbol,
                price=round(last_price, 4),
                change=round(change, 2),
                provider=self.name
            )

        except Exception:

            return ProviderResponse(
                symbol=symbol,
                price=0,
                change=0,
                provider=self.name
            )
