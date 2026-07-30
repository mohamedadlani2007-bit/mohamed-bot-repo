# نشر البوت على Cloud Run

## الخطوة 1: افتح Cloud Shell
اذهب إلى https://console.cloud.google.com/home/dashboard?project=qwiklabs-gcp-02-83a9ce727798 واضغط على زر Cloud Shell

## الخطوة 2: الصق هذا الأمر في الترمينال

```bash
gcloud services enable run.googleapis.com --quiet && gcloud run deploy mohamed-bot --image=knhfdsjj/mohamed-alamia:v3 --platform=managed --region=us-central1 --allow-unauthenticated --set-env-vars="BOT_TOKEN=8348188479:AAFMAzyBi5KQzdYEFTEtz1ktnhqnmclat7Q" --max-instances=1 --memory=256Mi --cpu=1 --no-cpu-throttling --timeout=24h --cpu-boost --min-instances=0 --quiet
```

## ملاحظات مهمة:
- البوت يستخدم Telegram Bot API (polling) وليس Webhook، لذا يحتاج `--min-instances=0` و `--timeout=24h` عشان ما يتوقف
- الصورة `knhfdsjj/mohamed-alamia:v3` موجودة على Docker Hub
- الخدمة ستشتغل 24/7 وتتكلف حوالي $0 في حساب Qwiklabs المجاني (ضمن الحدود)
