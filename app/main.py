from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.dashboard.router import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("========================================")
    print("ARPI Enterprise v1.2 Stable Starting...")
    print("========================================")
    yield
    print("ARPI Enterprise Stopped")


app = FastAPI(
    title="ARPI Enterprise",
    description="AI Risk & Prediction Intelligence",
    version="1.2.0",
    lifespan=lifespan,
)


app.include_router(api_router)
app.include_router(dashboard_router)
print("========== ARPI ROUTES ==========")
for route in app.routes:
    print(route.path)
print("================================")
