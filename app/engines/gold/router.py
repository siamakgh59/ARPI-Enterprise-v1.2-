from fastapi import APIRouter

from .models import GoldData, GoldReport
from .engine import GoldEngine


gold_router = APIRouter(
    prefix="/gold",
    tags=["Gold Intelligence Engine"]
)


engine = GoldEngine()


@gold_router.post(
    "/analyze",
    response_model=GoldReport
)
def analyze_gold(
    data: GoldData
):

    return engine.analyze(data)
