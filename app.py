from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def generate_mock_asset(asset_id, healthy=True):
    base_v = 48.0 if healthy else 42.0
    soh = random.uniform(88, 96) if healthy else random.uniform(60, 75)
    temp = random.uniform(25, 32) if healthy else random.uniform(35, 42)
    return {
        "asset_id": asset_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "nominal" if healthy else "attention",
        "metrics": {
            "voltage": round(base_v + random.uniform(-1, 1), 1),
            "current": round(random.uniform(2, 5) if healthy else random.uniform(0.5, 2), 1),
            "temperature": round(temp, 1),
            "state_of_health": round(soh, 1),
            "cycle_count": random.randint(100, 200) if healthy else random.randint(800, 1000),
            "internal_resistance": round(8 + random.random()*2 if healthy else 15 + random.random()*5, 1)
        },
        "alerts": [] if healthy else ["voltage_low", "elevated_temp"],
        "location": {"zone": "Warehouse-B" if healthy else "Refurb-Station", "rack": f"R{random.randint(1,10)}"}
    }

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    assets = [
        generate_mock_asset("SG-VID-8842", healthy=True),
        generate_mock_asset("SG-VID-7319", healthy=False),
        generate_mock_asset("SG-VID-9011", healthy=True),
    ]
    return templates.TemplateResponse("index.html", {"request": request, "assets": assets})

@app.get("/api/assets")
async def api_assets():
    return [
        generate_mock_asset("SG-VID-8842", healthy=True),
        generate_mock_asset("SG-VID-7319", healthy=False)
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info")