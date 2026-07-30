ملف deploy.sh:
#!/bin/bash

# متغيرات
export BOT_TOKEN="8348183979:AAFMAzyBi5KQzdYEFTEtz1ktnhqnmclat7Q"
export IMAGE="knhfdsjj/mohamed-alamia:v3"
export SERVICE_NAME="mohamed-bot"
export REGION="us-central1"

# تمكين الخدمات
gcloud services enable run.googleapis.com containerregistry.googleapis.com --quiet

# النشر مباشرة من الصورة الموجودة
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars="BOT_TOKEN=$BOT_TOKEN" \
  --quiet

# عرض رابط الخدمة
echo "✅ تم النشر!"
gcloud run services describe $SERVICE_NAME \
  --region $REGION \
  --format="value(status.url)"
