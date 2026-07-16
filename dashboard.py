from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/dashboard")


@router.get("/", response_class=HTMLResponse)
async def dashboard():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARPI Enterprise</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
        body{
            font-family:Arial;
            background:#111827;
            color:white;
            padding:20px;
        }

        .card{
            background:#1f2937;
            border-radius:15px;
            padding:20px;
            margin:15px 0;
        }

        .buy{
            color:#22c55e;
        }

        .sell{
            color:#ef4444;
        }

        .hold{
            color:#eab308;
        }

        </style>
    </head>

    <body>

    <h1>ARPI Enterprise</h1>

    <div class="card">
    <h2>Market Status</h2>
    <h3 class="buy">🟢 ACTIVE</h3>
    </div>


    <div class="card">
    <h2>AI Signals</h2>

    <p>Gold : <span class="sell">SELL</span> | Confidence 60%</p>
    <p>Silver : <span class="sell">SELL</span> | Confidence 60%</p>
    <p>Oil Brent : <span class="sell">SELL</span> | Confidence 70%</p>
    <p>USD Index : <span class="buy">BUY</span> | Confidence 60%</p>

    </div>


    <div class="card">
    <h2>ARPI Decision Engine</h2>
    <p>
    Multi Engine Analysis Active
    </p>
    </div>


    </body>
    </html>
    """


@router.get("/summary")
async def dashboard_summary():

    return {
        "application": "ARPI Enterprise",
        "dashboard": "summary",
        "status": "active",
        "version": "1.4.0"
    }
