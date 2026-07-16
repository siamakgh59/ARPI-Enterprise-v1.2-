from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary():

    return {
        "application": "ARPI Enterprise",
        "version": "1.2",
        "module": "Dashboard Summary",
        "status": "active",

        "timestamp": datetime.utcnow().isoformat(),

        "arpi_score": {
            "value": 0,
            "status": "initializing"
        },

        "market": {
            "status": "LIVE",
            "source": "ARPI Market Engine"
        },

        "risk": {
            "level": "UNKNOWN",
            "confidence": 0
        },

        "assets": {
            "gold": {
                "price": None,
                "change": None
            },
            "silver": {
                "price": None,
                "change": None
            },
            "oil": {
                "price": None,
                "change": None
            },
            "bitcoin": {
                "price": None,
                "change": None
            }
        },

        "signals": {
            "action": "HOLD",
            "confidence": 0,
            "reason": "Engines not connected yet"
        }
    }
