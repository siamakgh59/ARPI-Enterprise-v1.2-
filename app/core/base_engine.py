from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """
    کلاس پایه‌ی مشترک برای همه‌ی Engine های ARPI
    (GoldEngine, MacroEngine, RiskEngine و بعدی‌ها).

    هدف: تضمین یک رابط یکسان برای Fusion Engine / Dashboard تا
    بتوانند بدون دانستن جزئیات داخلی هر Engine، همه را یکسان صدا بزنند:

        for engine in [GoldEngine(), MacroEngine(), RiskEngine()]:
            result = engine.run(payload)

    نکته‌ی مهم: متد اختصاصی هر Engine (مثل analyze) دست‌نخورده باقی
    می‌ماند تا کدهای فعلی (API routers و غیره) که مستقیماً analyze
    را با امضای خاص خودش صدا می‌زنند، بدون تغییر کار کنند.
    run() صرفاً یک لایه‌ی adapter روی همان analyze است.
    """

    #: نام نمایشی Engine — باید در هر زیرکلاس مقداردهی شود
    NAME: str = "BaseEngine"

    #: نسخه‌ی Engine — باید در هر زیرکلاس مقداردهی شود
    VERSION: str = "0.0.0"

    @abstractmethod
    def run(self, payload: dict) -> dict:
        """
        نقطه‌ی ورود یکسان برای همه‌ی Engine ها.

        payload : دیکشنری ورودی خام (از Provider یا Fusion Engine)
        خروجی   : دیکشنری قابل serialize (معمولاً model_dump() یک Report)
        """
        raise NotImplementedError
