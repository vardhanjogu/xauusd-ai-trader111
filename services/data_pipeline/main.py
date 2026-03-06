from fastapi import FastAPI
import pandas as pd
import ta
import numpy as np

app = FastAPI(title="Data Pipeline Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "data_pipeline"}

@app.post("/features/generate")
def generate_features(symbol: str = "XAUUSD"):
    # Mocking a small dataframe since we don't have DB active yet
    dates = pd.date_range('20230101', periods=100)
    df = pd.DataFrame(np.random.randn(100, 4) * 10 + 2000, index=dates, columns=list('ABCD'))
    df.columns = ['open', 'high', 'low', 'close']
    
    # Generate some standard indicators using the 'ta' library
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['atr'] = ta.volatility.AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()
    
    # Store these back in the DB (PostgreSQL via shared/database.py in a real run)
    
    return {
        "status": "success",
        "symbol": symbol,
        "features_generated": ["rsi", "macd", "macd_signal", "atr"],
        "rows_processed": len(df)
    }

