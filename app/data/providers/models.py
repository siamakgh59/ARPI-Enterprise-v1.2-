class ProviderResponse:
    def __init__(
        self,
        provider: str,
        symbol: str,
        price: float = 0.0,
        change: float = 0.0,
        success: bool = False,
    ):
        self.provider = provider
        self.symbol = symbol
        self.price = price
        self.change = change
        self.success = success
