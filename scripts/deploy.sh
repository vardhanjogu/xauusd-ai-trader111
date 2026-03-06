#!/bin/bash
set -e

PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
REPO_NAME="xauusd-trader"

if [ -z "$PROJECT_ID" ]; then
  echo "GCP Project ID not set. Please run: gcloud config set project <your-project-id>"
  exit 1
fi

echo "Deploying to Project: $PROJECT_ID"

# Create Artifact Registry if it doesn't exist
if ! gcloud artifacts repositories describe $REPO_NAME --location=$REGION >/dev/null 2>&1; then
  echo "Creating Artifact Registry repository..."
  gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for XAUUSD AI Trader"
fi

SERVICES=(
  "api_gateway"
  "market_data"
  "data_pipeline"
  "ai_model"
  "strategy_engine"
  "risk_manager"
  "execution"
  "backtesting"
)

# Build and Push
for SERVICE in "${SERVICES[@]}"; do
  echo "Building and Deploying $SERVICE..."
  IMAGE_URL="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE}:latest"
  
  # Build and push to Artifact Registry
  echo "Building image for $SERVICE..."
  gcloud builds submit --tag "$IMAGE_URL" "services/${SERVICE}"
  
  # Deploy to Cloud Run
  echo "Deploying $SERVICE to Cloud Run..."
  gcloud run deploy "$SERVICE" \
    --image "$IMAGE_URL" \
    --region "$REGION" \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars GCP_PROJECT_ID="$PROJECT_ID"
done

echo "All services deployed successfully!"
