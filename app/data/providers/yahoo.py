import yfinance as yf

from .base import BaseProvider
from .models import ProviderResponse


class YahooFinanceProvider(BaseProvider):

    name = "Yahoo Finance"

    def get_price(self, symbol: str):

        try:
            ticker = yf.Ticker(symbol)

            data = ticker.history(
                period="5d",
                interval="1d"
            )

            if data.empty:
                return ProviderResponse(
                    provider=self.name,
                    symbol=symbol,
                    price=0,
                    change=0,
                    success=False
                )

            close = data["Close"]

            last_price = float(close.iloc[-1])

            if len(close) > 1:
                previous = float(close.iloc[-2])
                change = ((last_price - previous) / previous) * 100
            else:
                change = 0

            return ProviderResponse(
                provider=self.name,
                symbol=symbol,
                price=round(last_price, 4),
                change=round(change, 2),
                success=True
            )

        except Exception as e:

    print(
        "YAHOO ERROR:",
        symbol,
        str(e)
    )

    return ProviderResponse(
        provider=self.name,
        symbol=symbol,
        price=0,
        change=0,
        success=False
    )
