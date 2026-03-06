from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Risk Manager Service")

class RiskRequest(BaseModel):
    symbol: str
    signal: str # BUY / SELL
    account_balance: float
    current_price: float
    atr: float

@app.get("/")
def read_root():
    return {"status": "ok", "service": "risk_manager"}

@app.post("/calculate")
def calculate_risk(request: RiskRequest):
    risk_percent = 0.01  # 1% risk per trade
    risk_amount = request.account_balance * risk_percent
    
    # Stop loss based on 1.5x ATR
    stop_loss_distance = request.atr * 1.5
    
    # 1:2 Risk Reward
    take_profit_distance = stop_loss_distance * 2
    
    if request.signal == "BUY":
        stop_loss = request.current_price - stop_loss_distance
        take_profit = request.current_price + take_profit_distance
    elif request.signal == "SELL":
        stop_loss = request.current_price + stop_loss_distance
        take_profit = request.current_price - take_profit_distance
    else:
        return {"error": "Invalid signal"}
        
    # Basic lot sizing calculation (simplified for standard lots without pip value specifics)
    # In production, this needs pip_value calculation based on the pair
    pip_value_approx = 10 # Rough approximation for per-standard lot move on major pairs
    lot_size = round((risk_amount / (stop_loss_distance * 10)) / pip_value_approx, 2)
    lot_size = max(0.01, min(lot_size, 100)) # Clamping
    
    return {
        "symbol": request.symbol,
        "lot_size": lot_size,
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "risk_amount": round(risk_amount, 2),
        "risk_reward_ratio": "1:2"
    }
