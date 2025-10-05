# NASA EarthData Probability API

Flask tabanlı REST API - Belirli konum ve tarih için okyanus/atmosfer olaylarının olasılıklarını hesaplar.

## 🚀 Hızlı Başlangıç

### Kurulum
```bash
pip install -r requirements.txt
```

### API'yi Başlatma

**Development Modu:**
```bash
python app.py
```

**Production Modu (Gunicorn):**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

API varsayılan olarak `http://localhost:5000` adresinde çalışır.

## 📡 API Endpoints

### 1. Health Check
Sağlık kontrolü endpoint'i.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "NASA EarthData Probability API",
  "version": "1.0.0"
}
```

**Örnek:**
```bash
curl http://localhost:5000/health
```

---

### 2. Available Events
Desteklenen tüm olayları ve detaylarını döner.

**Endpoint:** `GET /events`

**Response:**
```json
{
  "success": true,
  "total_events": 9,
  "events": {
    "wind_high": {
      "name": "CCMP Wind Speed",
      "threshold": 10.0,
      "year_range": [1991, 2020],
      "description": "CCMP Wind Speed - Default threshold: 10.0"
    },
    "rain_high": {
      "name": "GPCP Daily Precipitation",
      "threshold": 10.0,
      "year_range": [1991, 2020],
      "description": "GPCP Daily Precipitation - Default threshold: 10.0"
    }
  }
}
```

**Örnek:**
```bash
curl http://localhost:5000/events
```

---

### 3. Calculate Probability (Ana Endpoint)
Belirli konum ve tarih için olay olasılıklarını hesaplar.

**Endpoint:** `POST /calculate_probability`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "lat": 40.0,              // Enlem (-90 ile 90 arası)
  "lon": 29.0,              // Boylam (-180 ile 180 arası)
  "month": 7,               // Ay (1-12)
  "day": 15,                // Gün (1-31)
  "events": [               // Olay listesi (zorunlu)
    "wind_high",
    "rain_high"
  ],
  "thresholds": {           // Opsiyonel: Özel threshold'lar
    "rain_high": 15.0
  },
  "use_synthetic": false    // Opsiyonel: Test verisi (varsayılan: false)
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "location": {
      "lat": 40.0,
      "lon": 29.0
    },
    "date": {
      "month": 7,
      "day": 15
    },
    "probabilities": {
      "wind_high": 0.25,
      "rain_high": 0.15
    },
    "metadata": {
      "total_events": 2,
      "custom_thresholds": true,
      "synthetic_data": false
    }
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Missing required fields: events"
}
```

---

## 📝 Kullanım Örnekleri

### Örnek 1: Temel Kullanım
İstanbul için 15 Temmuz'da yüksek rüzgar ve dalga olasılığı:

```bash
curl -X POST http://localhost:5000/calculate_probability \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 40.0,
    "lon": 29.0,
    "month": 7,
    "day": 15,
    "events": ["wind_high", "wave_high"],
    "use_synthetic": true
  }'
```

**Python ile:**
```python
import requests

response = requests.post(
    'http://localhost:5000/calculate_probability',
    json={
        'lat': 40.0,
        'lon': 29.0,
        'month': 7,
        'day': 15,
        'events': ['wind_high', 'wave_high'],
        'use_synthetic': True
    }
)

print(response.json())
```

### Örnek 2: Özel Threshold'larla
Antalya için özel eşik değerleriyle:

```bash
curl -X POST http://localhost:5000/calculate_probability \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 36.9,
    "lon": 30.7,
    "month": 8,
    "day": 1,
    "events": ["wind_high", "rain_high", "sst_high"],
    "thresholds": {
      "wind_high": 15.0,
      "rain_high": 15.0,
      "sst_high": 28.0
    },
    "use_synthetic": true
  }'
```

### Örnek 3: Tüm Olaylar
İzmir için tüm 9 olay:

```bash
curl -X POST http://localhost:5000/calculate_probability \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 38.4,
    "lon": 27.1,
    "month": 6,
    "day": 20,
    "events": [
      "wind_high", "rain_high", "wave_high", "storm_high",
      "fog_low", "sst_high", "current_strong", "tide_high", "ssha_high"
    ],
    "use_synthetic": true
  }'
```

### Örnek 4: JavaScript Fetch
Frontend'den API çağrısı:

```javascript
fetch('http://localhost:5000/calculate_probability', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    lat: 40.0,
    lon: 29.0,
    month: 7,
    day: 15,
    events: ['wind_high', 'wave_high'],
    use_synthetic: true
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

---

## 🔍 Test Etme

### Manuel Test (curl)
```bash
# Health check
curl http://localhost:5000/health

# Available events
curl http://localhost:5000/events

# Calculate probability
curl -X POST http://localhost:5000/calculate_probability \
  -H "Content-Type: application/json" \
  -d '{"lat": 40.0, "lon": 29.0, "month": 7, "day": 15, "events": ["wind_high"], "use_synthetic": true}'
```

### Otomatik Test Script
Test suite çalıştırma:

```bash
# API'yi başlat (terminal 1)
python app.py

# Test'leri çalıştır (terminal 2)
python test_api.py
```

Test script 10 farklı senaryoyu test eder:
- ✅ Health check
- ✅ Available events
- ✅ Temel hesaplama
- ✅ Özel threshold'lar
- ✅ Tüm olaylar
- ❌ Eksik alan hatası
- ❌ Geçersiz enlem
- ❌ Geçersiz olay ismi
- ❌ Non-JSON request
- ❌ Boş events listesi

---

## 🛡️ Hata Yönetimi

### Hata Kodları

| Kod | Açıklama |
|-----|----------|
| 200 | Başarılı |
| 400 | Bad Request (geçersiz parametreler) |
| 404 | Endpoint bulunamadı |
| 405 | Method not allowed |
| 500 | Internal server error |

### Hata Response Formatı
```json
{
  "success": false,
  "error": "Hata mesajı"
}
```

### Yaygın Hatalar

**1. Eksik Alan:**
```json
{
  "success": false,
  "error": "Missing required fields: day, events"
}
```

**2. Geçersiz Enlem/Boylam:**
```json
{
  "success": false,
  "error": "lat must be between -90 and 90, got 100"
}
```

**3. Geçersiz Olay İsmi:**
```json
{
  "success": false,
  "error": "Invalid events: tsunami, earthquake. Valid events: wind_high, rain_high, ..."
}
```

**4. JSON Değil:**
```json
{
  "success": false,
  "error": "Request body must be JSON"
}
```

---

## 🌍 CORS Desteği

API, tüm originler için CORS desteği sağlar. Frontend uygulamalarından güvenle çağrılabilir.

**Desteklenen:**
- Tüm originler (`*`)
- GET, POST metodları
- JSON content type

---

## 📊 Desteklenen Olaylar

| Olay | Açıklama | Varsayılan Threshold |
|------|----------|---------------------|
| `wind_high` | Yüksek rüzgar hızı | 10 m/s |
| `rain_high` | Yoğun yağış | 10 mm/gün |
| `wave_high` | Yüksek dalga | 2 m |
| `storm_high` | Fırtına/kasırga | 20 mm/h |
| `fog_low` | Düşük görüş/sis | 0.5 AOD |
| `sst_high` | Yüksek deniz suyu sıcaklığı | 25 °C |
| `current_strong` | Güçlü akıntı | 0.5 m/s |
| `tide_high` | Yüksek gelgit | 1.0 m |
| `ssha_high` | Yüksek deniz seviyesi anomalisi | 0.05 m |

---

## 🚀 Production Deployment

### Gunicorn ile Çalıştırma
```bash
# 4 worker process ile
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Timeout ayarı ile (uzun süren istekler için)
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Docker ile Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
docker build -t nasa-probability-api .
docker run -p 5000:5000 nasa-probability-api
```

### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 120s;
        proxy_read_timeout 120s;
    }
}
```

---

## 📈 Performans Notları

- **İlk İstek:** NASA OPeNDAP'tan veri çekme nedeniyle yavaş olabilir (~30-60 saniye)
- **Sentetik Mod:** Test için hızlı yanıt (<1 saniye)
- **Cache:** İleride eklenebilir (Redis/Memcached)
- **Paralel İşleme:** Birden fazla worker kullanın (`gunicorn -w 4`)

---

## 🔒 Güvenlik Notları

1. **Rate Limiting:** Production'da rate limiting ekleyin (Flask-Limiter)
2. **API Key:** Gerekirse API key authentication ekleyin
3. **Input Validation:** Tüm input'lar validate edilir
4. **CORS:** Production'da specific originler kullanın

---

## 📚 İlgili Dosyalar

- `app.py` - Flask API ana dosyası
- `calculate_ocean_probabilities.py` - Olasılık hesaplama modülü
- `test_api.py` - API test script'i
- `requirements.txt` - Python bağımlılıkları
- `README_PROBABILITIES.md` - Olasılık modülü dokümantasyonu

---

## 📝 Lisans

NASA açık veri politikasına uygun olarak hazırlanmıştır.

**Versiyon:** 1.0.0  
**Son Güncelleme:** 5 Ekim 2025

