ملف dockerfile :
# استخدم الصورة الموجودة مباشرة
FROM knhfdsjj/mohamed-alamia:v3

# لا نحتاج لأي إضافات، فقط نستخدم الصورة كما هي
CMD ["sh", "-c", "echo '✅ Container is running...' && tail -f /dev/null"]
