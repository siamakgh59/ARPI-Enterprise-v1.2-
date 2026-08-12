from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.dashboard.router import router as dashboard_router
from app.dashboard.ui import ui_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("========================================")
    print("ARPI Enterprise v1.4 Stable Starting...")
    print("========================================")
    yield
    print("ARPI Enterprise Stopped")


app = FastAPI(
    title="ARPI Enterprise",
    description="AI Risk & Prediction Intelligence",
    version="1.4.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
app.include_router(dashboard_router)
app.include_router(ui_router)
