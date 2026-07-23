from fastapi import APIRouter

from .models import GoldData, GoldReport
from .engine import GoldEngine
from .providers import FarazGoldProvider


gold_router = APIRouter(
    prefix="/gold",
    tags=["Gold Intelligence Engine"]
)


engine = GoldEngine()

provider = FarazGoldProvider()



@gold_router.post(
    "/analyze",
    response_model=GoldReport
)
def analyze_gold(
    data: GoldData
):

    return engine.analyze(data)



@gold_router.get(
    "/live",
    response_model=GoldReport
)
def live_gold():

    market_data = provider.fetch_gold_data()


    gold_data = GoldData(
        **market_data
    )


    return engine.analyze(
        gold_data
    )
