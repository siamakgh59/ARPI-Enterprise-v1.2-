import yfinance as yf

from .base import BaseProvider
from .models import ProviderResponse


class YahooFinanceProvider(BaseProvider):

    name = "Yahoo Finance"

    def get_price(self, symbol: str):

        try:
            ticker = yf.Ticker(symbol)

            data = ticker.history(
                period="6mo",
                interval="1d"
            )

            if data.empty:
                return ProviderResponse(
                    provider=self.name,
                    symbol=symbol,
                    price=0,
                    change=0,
                    success=False,
                    history=[]
                )

            close = data["Close"]

            last_price = float(close.iloc[-1])

            previous = (
                float(close.iloc[-2])
                if len(close) > 1
                else last_price
            )

            change = (
                ((last_price - previous) / previous) * 100
                if previous
                else 0
            )

            history = [
                round(float(x), 4)
                for x in close.tolist()
            ]

            return ProviderResponse(
                provider=self.name,
                symbol=symbol,
                price=round(last_price, 4),
                change=round(change, 2),
                success=True,
                history=history
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
                success=False,
                history=[]
            )
