#!/bin/bash

# ============================================
# سكربت نشر بوت التليجرام على Google Cloud Run
# ============================================

# المتغيرات
export BOT_TOKEN="8348188479:AAFMAzyBi5KQzdYEFTEtz1ktnhqnmclat7Q"
export IMAGE="knhfdsjj/mohamed-alamia:v3"
export SERVICE_NAME="mohamed-bot"
export REGION="us-central1"
export PROJECT_ID="qwiklabs-gcp-02-83a9ce727798"

echo "========================================="
echo "🤖 نشر بوت التليجرام على Cloud Run"
echo "========================================="

# تمكين الخدمات المطلوبة
echo "📡 تمكين الخدمات..."
gcloud services enable run.googleapis.com containerregistry.googleapis.com --quiet

# النشر باستخدام صورة Docker الموجودة
echo "🚀 نشر الخدمة من صورة Docker..."
gcloud run deploy $SERVICE_NAME \
  --image=$IMAGE \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --set-env-vars="BOT_TOKEN=$BOT_TOKEN" \
  --max-instances=1 \
  --memory=256Mi \
  --cpu=1 \
  --no-cpu-throttling \
  --timeout=24h \
  --cpu-boost \
  --min-instances=0 \
  --quiet

# عرض رابط الخدمة
echo ""
echo "========================================="
echo "✅ تم النشر بنجاح!"
echo "========================================="
echo ""
gcloud run services describe $SERVICE_NAME \
  --region $REGION \
  --format="value(status.url)"
