from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DEBUG: bool = False

    # GCP
    GCP_PROJECT_ID: str = "local-dev-id"
    GCS_BUCKET_NAME: str = "xauusd-ai-models-bucket"

    # Databases
    DATABASE_URL: str = "postgresql://trading_user:trading_password@postgres_db:5432/xauusd_trading"
    REDIS_URL: str = "redis://redis_cache:6379/0"

    # External APIs
    OANDA_API_KEY: str = ""
    OANDA_ACCOUNT_ID: str = ""
    TWELVEDATA_API_KEY: str = ""
    ALPHAVANTAGE_API_KEY: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
