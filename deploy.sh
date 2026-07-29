#!/bin/bash
export BOT_TOKEN="8348188479:AAFMAzyBi5KQzdYEFTEtz1ktnhqnmclat7Q"
export IMAGE="knhfdsjj/mohamed-alamia:v3"
export SERVICE_NAME="mohamed-bot"
export REGION="us-central1"
gcloud services enable run.googleapis.com containerregistry.googleapis.com --quiet
gcloud run deploy $SERVICE_NAME --image $IMAGE --platform managed --region $REGION --allow-unauthenticated --set-env-vars="BOT_TOKEN=$BOT_TOKEN" --quiet
echo "✅ تم النشر!"
gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
