from .models import ProviderResponse


class BaseProvider:
    name = "Base"

    def get_price(self, symbol: str) -> ProviderResponse:
        return ProviderResponse(
            provider=self.name,
            symbol=symbol,
            success=False,
        )
