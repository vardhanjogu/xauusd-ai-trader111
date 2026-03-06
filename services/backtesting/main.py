from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="Backtesting Engine Service")

class BacktestRequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    strategy_name: str
    initial_balance: float = 10000.0

@app.get("/")
def read_root():
    return {"status": "ok", "service": "backtesting"}

@app.post("/run")
def run_backtest(request: BacktestRequest):
    # A skeleton that would query historical market_data, run through the strategy engine, 
    # simulate executions, and spit out statistics.
    
    total_trades = random.randint(20, 150)
    win_rate = random.uniform(0.40, 0.70)
    profit_factor = random.uniform(0.8, 2.5)
    
    final_balance = request.initial_balance * (1 + (profit_factor - 1) * 0.1)
    
    # Generate mock equity curve
    equity_curve = [request.initial_balance]
    current = request.initial_balance
    for _ in range(total_trades):
        if random.random() < win_rate:
            current += random.uniform(50, 200)
        else:
            current -= random.uniform(30, 150)
        equity_curve.append(round(current, 2))
        
    return {
        "status": "completed",
        "symbol": request.symbol,
        "strategy": request.strategy_name,
        "metrics": {
            "initial_balance": request.initial_balance,
            "final_balance": round(final_balance, 2),
            "net_profit": round(final_balance - request.initial_balance, 2),
            "total_trades": total_trades,
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "max_drawdown": round(random.uniform(0.05, 0.25), 4)
        },
        "equity_curve": equity_curve
    }
