from abc import ABC, abstractmethod


class MarketProvider(ABC):
    """
    Base interface for all ARPI market data providers
    """

    @abstractmethod
    def get_price(self, symbol: str):
        pass


class ProviderResponse:
    """
    Standard ARPI market response format
    """

    def __init__(
        self,
        symbol: str,
        price: float,
        change: float = 0.0
    ):
        self.symbol = symbol
        self.price = price
        self.change = change

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "price": self.price,
            "change": self.change
        }
