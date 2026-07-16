from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.market import get_market_data


router = APIRouter(prefix="/dashboard")


@router.get("/", response_class=HTMLResponse)
async def dashboard():

    try:
        data = get_market_data()
        analysis = data.get("analysis", {})

    except Exception:
        analysis = {}


    assets = [
        "gold",
        "silver",
        "oil_wti",
        "oil_brent",
        "usd_index",
        "eurusd",
        "vix",
        "bitcoin"
    ]


    cards = ""

    for asset in assets:

        item = analysis.get(asset, {})

        signal = item.get("signal", "-")
        confidence = item.get("confidence", "-")
        risk = item.get("risk", "-")
        price = item.get("price", "-")
        trend = item.get("technical", {}).get("trend", "-")

        css = signal.lower()


        cards += f"""
        <div class="card">

        <h2>{asset.upper()}</h2>

        <h3>
        Price: {price}
        </h3>

        <p>
        Signal:
        <span class="{css}">
        {signal}
        </span>
        </p>

        <p>
        Confidence:
        {confidence}%
        </p>

        <p>
        Risk:
        {risk}
        </p>

        <p>
        Trend:
        {trend}
        </p>

        </div>
        """


    return f"""
<!DOCTYPE html>

<html>

<head>

<title>
ARPI Enterprise Dashboard
</title>

<meta name="viewport" content="width=device-width, initial-scale=1">


<style>

body {{

font-family:Arial;
background:#111827;
color:white;
padding:20px;

}}


.grid {{

display:grid;
grid-template-columns:
repeat(auto-fit,minmax(250px,1fr));

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


<h1>
ARPI Enterprise
</h1>


<h3>
AI Risk & Prediction Intelligence
</h3>


<div class="grid">

{cards}

</div>


</body>


</html>
"""


@router.get("/data")
async def dashboard_data():

    try:
        return get_market_data()

    except Exception as e:

        return {
            "status":"error",
            "message":str(e)
        }



@router.get("/summary")
async def dashboard_summary():

    return {

        "application":
        "ARPI Enterprise",

        "dashboard":
        "active",

        "version":
        "1.6.0"

    }
