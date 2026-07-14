class ProviderResponse:

    def __init__(
        self,
        provider: str,
        symbol: str,
        price: float = 0.0,
        change: float = 0.0,
        success: bool = False,
        history: list = None,
    ):
        self.provider = provider
        self.symbol = symbol
        self.price = price
        self.change = change
        self.success = success
        self.history = history or []

    def to_dict(self):

        return {
            "provider": self.provider,
            "symbol": self.symbol,
            "price": self.price,
            "change": self.change,
            "success": self.success,
            "history": self.history
        }

