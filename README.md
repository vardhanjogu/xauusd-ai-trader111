# XAUUSD AI Trader Platform

A production-ready, cloud-native AI trading platform for Gold (XAUUSD) built with:
- **Python FastAPI** microservices on **Google Cloud Run**
- **PostgreSQL** + **BigQuery** for data storage
- **Next.js** dashboard deployed on **Vercel**
- **Docker Compose** for local development
- **GitHub Actions** for CI/CD

---

## Architecture

```
Vercel (Frontend Next.js)
       │
       ▼
API Gateway :8000  (WebSocket + REST aggregator)
       │
┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│      │      │      │      │      │      │      │
:8001  :8002  :8003  :8004  :8005  :8006  :8007
market data  pipeline  ai_model  strategy  risk  exec  backtest
       │
  PostgreSQL :5432 + Redis :6379
```

---

## Local Development

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd xauusd_ai_trader
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 3. Start all services with Docker Compose
```bash
docker-compose up --build
```

This will spin up:
- PostgreSQL (port 5432)
- Redis (port 6379)
- API Gateway (port 8000)
- Market Data (port 8001)
- Data Pipeline (port 8002)
- AI Model (port 8003)
- Strategy Engine (port 8004)
- Risk Manager (port 8005)
- Execution Engine (port 8006)
- Backtesting Engine (port 8007)

### 4. Run the frontend dashboard
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

---

## Google Cloud Deployment

### Prerequisites
- GCP project with billing enabled
- [`gcloud` CLI](https://cloud.google.com/sdk) installed and authenticated
- Docker installed

### 1. Setup GCP infrastructure
```bash
chmod +x scripts/setup_gcp.sh
./scripts/setup_gcp.sh YOUR_GCP_PROJECT_ID
```

### 2. Build and deploy all services to Cloud Run
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

---

## Vercel Frontend Deployment

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Deploy
```bash
cd frontend
vercel --prod
```

### 3. Set Environment Variables in Vercel Dashboard
| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_URL` | Your Cloud Run API Gateway URL |
| `NEXT_PUBLIC_WS_URL` | `wss://your-api-gateway-url/ws` |

---

## GitHub Actions CI/CD

Add the following secrets to your GitHub repository:

| Secret | Description |
|---|---|
| `GCP_SA_KEY` | GCP Service Account JSON key |
| `GCP_PROJECT_ID` | Your GCP Project ID |
| `VERCEL_TOKEN` | Vercel deploy token |
| `VERCEL_ORG_ID` | Vercel Organization ID |
| `VERCEL_PROJECT_ID` | Vercel Project ID |

Every push to `main` will automatically:
1. Build all Docker images and push to Google Artifact Registry
2. Deploy all services to Cloud Run
3. Deploy the frontend to Vercel

---

## Service Endpoints

| Service | Local Port | Endpoint |
|---|---|---|
| API Gateway | 8000 | `GET /`, `WS /ws` |
| Market Data | 8001 | `GET /latest`, `POST /ingest/historical` |
| Data Pipeline | 8002 | `POST /features/generate` |
| AI Model | 8003 | `POST /train`, `POST /predict` |
| Strategy Engine | 8004 | `POST /evaluate` |
| Risk Manager | 8005 | `POST /calculate` |
| Execution | 8006 | `POST /trade/open`, `POST /trade/close/{id}` |
| Backtesting | 8007 | `POST /run` |
