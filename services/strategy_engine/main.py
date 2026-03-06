from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Strategy Engine Service")

class SignalRequest(BaseModel):
    symbol: str
    ai_prediction: str  # BUY, SELL, HOLD
    technical_indicators: dict

@app.get("/")
def read_root():
    return {"status": "ok", "service": "strategy_engine"}

@app.post("/evaluate")
def evaluate_strategy(request: SignalRequest):
    # Base logic combining AI and Technicals
    final_signal = "HOLD"
    reason = "Undecided"
    
    rsi = request.technical_indicators.get("rsi", 50)
    macd = request.technical_indicators.get("macd", 0)
    macd_signal = request.technical_indicators.get("macd_signal", 0)
    
    if request.ai_prediction == "BUY" and rsi < 40 and macd > macd_signal:
        final_signal = "BUY"
        reason = "AI Buy confirmation with oversold RSI and bullish MACD cross"
    elif request.ai_prediction == "SELL" and rsi > 60 and macd < macd_signal:
        final_signal = "SELL"
        reason = "AI Sell confirmation with overbought RSI and bearish MACD cross"
        
    return {
        "symbol": request.symbol,
        "final_signal": final_signal,
        "reason": reason,
        "strategy_used": "Combined_AI_Technicals_v1"
    }
