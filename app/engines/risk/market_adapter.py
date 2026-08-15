import time

from app.engines.macro.provider import MacroProvider
from app.engines.macro.engine import MacroEngine


_macro_provider = MacroProvider()
_macro_engine = MacroEngine()

# کش ساده: هر ۱۰ دقیقه (۶۰۰ ثانیه) یک‌بار واقعاً از FRED/Yahoo می‌گیرد،
# چون داده‌ی کلان (تورم، نرخ بهره) ثانیه‌به‌ثانیه تغییر نمی‌کند و
# صدا زدن مکرر آن (مثلاً برای هر ۸ asset جدا) کند و بی‌فایده است.
_CACHE_TTL_SECONDS = 600
_cached_macro_risk = 50
_cache_timestamp = 0


def _get_macro_risk() -> float:

    global _cached_macro_risk, _cache_timestamp

    now = time.time()

    if now - _cache_timestamp < _CACHE_TTL_SECONDS:
        return _cached_macro_risk

    try:
        macro_data = _macro_provider.fetch()
        macro_report = _macro_engine.analyze(macro_data)
        _cached_macro_risk = macro_report.macro_risk
        _cache_timestamp = now

    except Exception as e:
        print("MACRO RISK FETCH ERROR:", e)
        # در صورت خطا، مقدار قبلی (یا پیش‌فرض ۵۰) نگه داشته می‌شود

    return _cached_macro_risk


def market_to_risk_factors(
    asset_analysis: dict
) -> dict:


    confidence = asset_analysis.get(
        "confidence",
        50
    )


    signal = asset_analysis.get(
        "signal",
        "HOLD"
    )


    risk = asset_analysis.get(
        "risk",
        "MEDIUM"
    )


    market_risk = 50


    if signal == "SELL":
        market_risk = 70

    elif signal == "BUY":
        market_risk = 30



    volatility_risk = 50


    if risk == "HIGH":
        volatility_risk = 80

    elif risk == "LOW":
        volatility_risk = 30



    return {

        "market_risk": market_risk,

        "volatility_risk": volatility_risk,

        "macro_risk": _get_macro_risk(),

        "liquidity_risk": 40,

        "geopolitical_risk": 50,

        "data_confidence_risk": 100 - confidence

    }
