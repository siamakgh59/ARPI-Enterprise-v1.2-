from fastapi import APIRouter

from .engine import MacroEngine
from .models import MacroData
from .provider import MacroProvider


macro_router = APIRouter(
    prefix="/macro",
    tags=["Macro Intelligence Engine"]
)


engine = MacroEngine()
provider = MacroProvider()


@macro_router.post("/analyze")
def analyze_macro(data: MacroData):

    report = engine.analyze(data)

    return report


@macro_router.get("/live")
def live_macro():

    data = provider.fetch()

    report = engine.analyze(
        data
    )

    return report
