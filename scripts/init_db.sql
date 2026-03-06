-- init_db.sql
CREATE TABLE IF NOT EXISTS market_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    timeframe VARCHAR(5) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    open NUMERIC(15, 6),
    high NUMERIC(15, 6),
    low NUMERIC(15, 6),
    close NUMERIC(15, 6),
    volume NUMERIC(20, 6),
    UNIQUE(symbol, timeframe, timestamp)
);

CREATE TABLE IF NOT EXISTS signals (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    timeframe VARCHAR(5) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    signal_type VARCHAR(10) NOT NULL, -- BUY, SELL, HOLD
    confidence NUMERIC(5, 4),
    model_version VARCHAR(50),
    ai_prediction VARCHAR(10),
    technical_context JSONB
);

CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    ticket_id VARCHAR(100), -- Broker ID
    mode VARCHAR(15) NOT NULL, -- SIMULATION, PAPER, LIVE
    trade_type VARCHAR(5) NOT NULL, -- LONG, SHORT
    entry_price NUMERIC(15, 6) NOT NULL,
    exit_price NUMERIC(15, 6),
    volume NUMERIC(15, 6) NOT NULL,
    stop_loss NUMERIC(15, 6),
    take_profit NUMERIC(15, 6),
    status VARCHAR(15) NOT NULL, -- OPEN, CLOSED, CANCELLED
    opened_at TIMESTAMPTZ NOT NULL,
    closed_at TIMESTAMPTZ,
    pnl NUMERIC(15, 6)
);

CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) UNIQUE NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    trained_at TIMESTAMPTZ NOT NULL,
    accuracy NUMERIC(5, 4),
    features_used JSONB,
    gcs_path VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS backtests (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    initial_balance NUMERIC(15, 2) NOT NULL,
    final_balance NUMERIC(15, 2) NOT NULL,
    total_trades INTEGER NOT NULL,
    win_rate NUMERIC(5, 4) NOT NULL,
    profit_factor NUMERIC(10, 4),
    max_drawdown NUMERIC(5, 4),
    sharpe_ratio NUMERIC(10, 4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    results JSONB
);

CREATE INDEX idx_market_data_sym_tf_ts ON market_data(symbol, timeframe, timestamp);
CREATE INDEX idx_trades_status ON trades(status);
CREATE INDEX idx_signals_sym_ts ON signals(symbol, timestamp);
