#!/bin/bash
set -e

PROJECT_ID=$1

if [ -z "$PROJECT_ID" ]; then
  echo "Usage: ./setup_gcp.sh <project-id>"
  exit 1
fi

echo "Setting up GCP Infrastructure for AI Trader on project: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# Enable required APIs
echo "Enabling APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  bigquery.googleapis.com \
  storage.googleapis.com \
  pubsub.googleapis.com \
  cloudscheduler.googleapis.com \
  vpcaccess.googleapis.com \
  sqladmin.googleapis.com

# Create GCS Bucket for Models
BUCKET_NAME="${PROJECT_ID}-xauusd-models"
if ! gsutil ls -b "gs://${BUCKET_NAME}" >/dev/null 2>&1; then
  echo "Creating GCS Bucket..."
  gsutil mb -l us-central1 "gs://${BUCKET_NAME}"
fi

# Create BigQuery Dataset
BQ_DATASET="trading_analytics"
if ! bq show "$BQ_DATASET" >/dev/null 2>&1; then
  echo "Creating BigQuery Dataset..."
  bq mk -d --location=US "$BQ_DATASET"
fi

# Create Pub/Sub Topics
TOPICS=("market-ticks" "signals-generated" "trade-updates")
for TOPIC in "${TOPICS[@]}"; do
  if ! gcloud pubsub topics describe "$TOPIC" >/dev/null 2>&1; then
    echo "Creating Pub/Sub Topic: $TOPIC"
    gcloud pubsub topics create "$TOPIC"
  fi
done

echo "GCP Setup Complete."
