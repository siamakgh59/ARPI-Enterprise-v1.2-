from fastapi import APIRouter

from .models import GoldData, GoldReport
from .engine import GoldIntelligenceEngine

from .providers import FarazGoldProvider
from .providers.global_gold_provider import GlobalGoldProvider


gold_router = APIRouter(
    prefix="/gold",
    tags=["Gold Intelligence Engine"]
)


engine = GoldIntelligenceEngine()

faraz_provider = FarazGoldProvider()

global_provider = GlobalGoldProvider()



@gold_router.post(
    "/analyze",
    response_model=GoldReport
)
def analyze_gold(
    data: GoldData
):

    return engine.analyze(
        data.model_dump()
    )



@gold_router.get(
    "/live",
    response_model=GoldReport
)
def live_gold():

    # -----------------------------
    # Iran Gold Market
    # -----------------------------

    faraz_data = (
        faraz_provider.fetch_gold_data()
    )


    # -----------------------------
    # Global Gold Market
    # -----------------------------

    global_data = (
        global_provider.fetch_global_data()
    )


    # -----------------------------
    # Merge Providers
    # -----------------------------

    market_data = {}


    market_data.update(
        faraz_data
    )


    market_data.update(
        global_data
    )


    print(
        "######## GOLD MERGED DATA ########"
    )

    print(
        market_data
    )

    print(
        "##################################"
    )


    gold_data = GoldData(
        **market_data
    )


    return engine.analyze(
        gold_data.model_dump()
    )
