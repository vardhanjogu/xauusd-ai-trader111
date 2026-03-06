from fastapi import FastAPI
from pydantic import BaseModel
import random
import time

app = FastAPI(title="AI Model Service")

class PredictionRequest(BaseModel):
    symbol: str
    timeframe: str
    features: dict

@app.get("/")
def read_root():
    return {"status": "ok", "service": "ai_model"}

@app.post("/train")
def train_model(algorithm: str = "RandomForest"):
    time.sleep(2) # Simulate training time
    return {
        "status": "success",
        "algorithm": algorithm,
        "version": f"v1.0.{random.randint(100, 999)}",
        "accuracy": round(random.uniform(0.60, 0.85), 4)
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    signals = ["BUY", "SELL", "HOLD"]
    weights = [0.3, 0.3, 0.4]  # Slightly bias toward HOLD for stability
    
    prediction = random.choices(signals, weights=weights)[0]
    confidence = round(random.uniform(0.51, 0.99), 2)
    
    return {
        "symbol": request.symbol,
        "prediction": prediction,
        "confidence": confidence,
        "model_version": "v1.0.123"
    }

