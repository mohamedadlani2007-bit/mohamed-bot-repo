#!/bin/bash

# متغيرات
export BOT_TOKEN="8348188479:AAFMAzyBi5KQzdYEFTEtz1ktnhqnmclat7Q"
export IMAGE="knhfdsjj/mohamed-alamia:v3"
export SERVICE_NAME="mohamed-bot"
export REGION="us-central1"

# تمكين الخدمات
gcloud services enable run.googleapis.com containerregistry.googleapis.com --quiet

# النشر من المصدر (سيقرأ Dockerfile من GitHub)
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars="BOT_TOKEN=$BOT_TOKEN" \
  --max-instances=1 \
  --memory=512Mi \
  --cpu=1 \
  --no-cpu-throttling \
  --quiet

# عرض رابط الخدمة
echo "✅ تم النشر!"
gcloud run services describe $SERVICE_NAME \
  --region $REGION \
  --format="value(status.url)"
