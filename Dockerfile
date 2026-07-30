# استخدم الصورة الموجودة
FROM knhfdsjj/mohamed-alamia:v3

# نسخ كود البوت
COPY bot.py /app/bot.py
COPY requirements.txt /app/requirements.txt

# تثبيت المتطلبات
RUN pip install -r /app/requirements.txt

# تشغيل البوت
CMD ["python3", "/app/bot.py"]
