from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import requests

router = APIRouter(prefix="/dashboard")


MARKET_URL = "http://127.0.0.1:8080/market/live"


@router.get("/", response_class=HTMLResponse)
async def dashboard():

    try:
        data = requests.get(MARKET_URL, timeout=10).json()
        analysis = data.get("analysis", {})

    except Exception:
        analysis = {}


    gold = analysis.get("gold", {})
    silver = analysis.get("silver", {})
    bitcoin = analysis.get("bitcoin", {})
    usd = analysis.get("usd_index", {})


    return f"""
    <!DOCTYPE html>
    <html>

    <head>
    <title>ARPI Enterprise Dashboard</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>

    body {{
        font-family: Arial;
        background:#111827;
        color:white;
        padding:20px;
    }}

    .grid {{
        display:grid;
        grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
        gap:20px;
    }}

    .card {{
        background:#1f2937;
        border-radius:18px;
        padding:20px;
    }}

    .buy {{
        color:#22c55e;
    }}

    .sell {{
        color:#ef4444;
    }}

    .hold {{
        color:#eab308;
    }}

    </style>

    </head>


    <body>


    <h1>ARPI Enterprise</h1>

    <h3>AI Risk & Prediction Intelligence</h3>


    <div class="grid">


    <div class="card">
    <h2>Gold</h2>

    <h3>
    Price:
    {gold.get("price","-")}
    </h3>

    <p>
    Signal:
    {gold.get("signal","-")}
    </p>

    <p>
    Confidence:
    {gold.get("confidence","-")}%
    </p>

    </div>



    <div class="card">

    <h2>Silver</h2>

    <h3>
    Price:
    {silver.get("price","-")}
    </h3>

    <p>
    Signal:
    {silver.get("signal","-")}
    </p>

    <p>
    Confidence:
    {silver.get("confidence","-")}%
    </p>

    </div>




    <div class="card">

    <h2>Bitcoin</h2>

    <h3>
    Price:
    {bitcoin.get("price","-")}
    </h3>

    <p>
    Signal:
    {bitcoin.get("signal","-")}
    </p>

    <p>
    Confidence:
    {bitcoin.get("confidence","-")}%
    </p>

    </div>




    <div class="card">

    <h2>USD Index</h2>

    <h3>
    Price:
    {usd.get("price","-")}
    </h3>

    <p>
    Signal:
    {usd.get("signal","-")}
    </p>

    </div>


    </div>


    </body>

    </html>
    """


@router.get("/data")
async def dashboard_data():

    try:
        return requests.get(MARKET_URL, timeout=10).json()

    except Exception as e:

        return {
            "status":"error",
            "message":str(e)
        }


@router.get("/summary")
async def dashboard_summary():

    return {
        "application":"ARPI Enterprise",
        "dashboard":"active",
        "version":"1.5.0"
    }
