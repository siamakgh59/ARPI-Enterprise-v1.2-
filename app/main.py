from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.dashboard.router import router as dashboard_router


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

# اجازه می‌دهد داشبورد وب (حتی اگر جدا از این سرور باز شود) بتواند
# به API درخواست بزند.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
app.include_router(dashboard_router)

# داشبورد وب زیبا — از همین سرور، در مسیر /ui قابل مشاهده است
app.mount(
    "/ui",
    StaticFiles(directory="app/dashboard/static", html=True),
    name="dashboard-ui",
)
