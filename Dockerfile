# 1️⃣ Python'un hafif bir versiyonunu kullan
FROM python:3.10-slim

# 2️⃣ Çalışma dizinini belirle
WORKDIR /app

# 3️⃣ Gerekli bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Servis dosyalarını kopyala
COPY ./app/ app/

# 5️⃣ Servisi başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
