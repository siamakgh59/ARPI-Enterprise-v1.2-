from fastapi import APIRouter

from .engine import MacroEngine
from .models import MacroData


macro_router = APIRouter(
    prefix="/macro",
    tags=["Macro Intelligence Engine"]
)


engine = MacroEngine()


@macro_router.post("/analyze")
def analyze_macro(data: MacroData):

    report = engine.analyze(
        data
    )

    return report
