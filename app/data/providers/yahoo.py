import yfinance as yf

from .base import BaseProvider
from .models import ProviderResponse


class YahooFinanceProvider(BaseProvider):

    name = "Yahoo Finance"


    def get_price(self, symbol: str):

        try:

            ticker = yf.Ticker(symbol)

            data = ticker.history(
                period="3mo",
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


            last_price = float(
                data["Close"].iloc[-1]
            )


            first_price = float(
                data["Close"].iloc[-2]
            )


            change = (
                (last_price-first_price)
                /
                first_price
            ) * 100


            return ProviderResponse(
                provider=self.name,
                symbol=symbol,
                price=round(last_price,4),
                change=round(change,2),
                success=True,
                history=data["Close"].tolist()
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
