from fastapi import FastAPI, BackgroundTasks
import asyncio
import random
import time
from datetime import datetime

app = FastAPI(title="Market Data Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "market_data"}

@app.post("/ingest/historical")
def ingest_historical(symbol: str = "XAUUSD", timeframe: str = "1h"):
    # In a real app we would call TwelveData / AlphaVantage here
    return {"message": f"Started historical ingestion for {symbol} on {timeframe}"}

def simulate_tick():
    return {
        "symbol": "XAUUSD",
        "price": round(random.uniform(2000, 2050), 2),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/latest")
def get_latest_price(symbol: str = "XAUUSD"):
    # Fallback to simulated data for basic functionality
    return simulate_tick()

