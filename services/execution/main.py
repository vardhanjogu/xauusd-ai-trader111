from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time
import random

app = FastAPI(title="Execution Engine Service")

class TradeOrder(BaseModel):
    symbol: str
    signal: str  # BUY / SELL
    lot_size: float
    stop_loss: float
    take_profit: float
    mode: str = "SIMULATION"

@app.get("/")
def read_root():
    return {"status": "ok", "service": "execution"}

@app.post("/trade/open")
def open_trade(order: TradeOrder):
    # Depending on mode, route to Oanda API or Simulation
    if order.mode == "LIVE":
        # Call active broker integration (e.g. Oanda)
        ticket_id = f"OANDA_{uuid.uuid4().hex[:8].upper()}"
    else:
        # Paper / Simulation mode
        ticket_id = f"SIM_{uuid.uuid4().hex[:8].upper()}"

    return {
        "status": "success",
        "ticket_id": ticket_id,
        "entry_details": {
            "symbol": order.symbol,
            "type": order.signal,
            "lot_size": order.lot_size,
            "sl": order.stop_loss,
            "tp": order.take_profit,
            "status": "OPEN",
            "mode": order.mode,
            "timestamp": time.time(),
        },
    }

@app.post("/trade/close/{ticket_id}")
def close_trade(ticket_id: str, close_price: float):
    pnl = round(random.uniform(-100, 200), 2)
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "closed_at": close_price,
        "pnl": pnl,
    }
