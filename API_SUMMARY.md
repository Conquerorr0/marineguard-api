# Flask API - Proje Özeti

## 🎯 Tamamlanan Çalışma

Flask tabanlı REST API başarıyla oluşturuldu ve test edildi!

## 📦 Oluşturulan Dosyalar

### 1. **`app.py`** (Ana API Dosyası - 315 satır)
Flask tabanlı REST API servisi:

**Endpoints:**
- ✅ `GET /health` - Sağlık kontrolü
- ✅ `GET /events` - Desteklenen olaylar listesi
- ✅ `POST /calculate_probability` - Olasılık hesaplama (ana endpoint)

**Özellikler:**
- ✅ CORS etkinleştirildi (flask-cors ile)
- ✅ JSON request/response
- ✅ Kapsamlı hata yönetimi (400, 404, 405, 500)
- ✅ Input validasyonu (lat/lon/month/day aralıkları)
- ✅ Logging sistemi
- ✅ calculate_probabilities fonksiyonu entegrasyonu
- ✅ Özel threshold desteği

### 2. **`requirements.txt`** (Güncellenmiş)
Yeni eklenen paketler:
```txt
flask>=3.0.0
flask-cors>=4.0.0
gunicorn>=21.2.0
```

### 3. **`test_api.py`** (Test Suite - 295 satır)
10 farklı test senaryosu:
- GET endpoint testleri
- Başarılı POST istekleri
- Hata senaryoları (400 Bad Request)
- Curl örnekleri

### 4. **`README_API.md`** (API Dokümantasyonu)
Detaylı API dokümantasyonu:
- Endpoint açıklamaları
- Request/Response örnekleri
- cURL komutları
- Python/JavaScript örnekleri
- Production deployment talimatları

### 5. **`postman_collection.json`** (Postman Collection)
8 hazır API isteği:
- Health check
- Available events
- Basic calculation
- Custom thresholds
- All events
- Error scenarios

### 6. **`.gitignore`**
Python/Flask projeleri için standart .gitignore

## 🚀 Kullanım

### API'yi Başlatma
```bash
# Development
python app.py

# Production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Test Etme
```bash
# Health check
curl http://localhost:5000/health

# Basic request
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

# Test suite
python test_api.py
```

## ✅ Test Sonuçları

### Başarılı Testler:

**1. Health Check**
```json
{
  "status": "healthy",
  "service": "NASA EarthData Probability API",
  "version": "1.0.0"
}
```

**2. Available Events**
```json
{
  "success": true,
  "total_events": 9,
  "events": {...}
}
```

**3. Basic Calculation (İstanbul, 15 Temmuz)**
```json
{
  "success": true,
  "data": {
    "location": {"lat": 40.0, "lon": 29.0},
    "date": {"month": 7, "day": 15},
    "probabilities": {
      "wind_high": 0.1481,
      "wave_high": 0.1538
    },
    "metadata": {
      "total_events": 2,
      "custom_thresholds": false,
      "synthetic_data": true
    }
  }
}
```

**4. Custom Thresholds (Antalya, 1 Ağustos)**
```json
{
  "success": true,
  "data": {
    "location": {"lat": 36.9, "lon": 30.7},
    "date": {"month": 8, "day": 1},
    "probabilities": {
      "wind_high": 0.0,
      "rain_high": 0.0
    },
    "metadata": {
      "total_events": 2,
      "custom_thresholds": true,
      "synthetic_data": true
    }
  }
}
```

**5. Error Handling (Geçersiz Enlem)**
```json
{
  "success": false,
  "error": "lat must be between -90 and 90, got 100.0"
}
```

## 🎨 API Özellikleri

### Request Format
```json
{
  "lat": 40.0,              // Zorunlu: -90 ile 90 arası
  "lon": 29.0,              // Zorunlu: -180 ile 180 arası
  "month": 7,               // Zorunlu: 1-12
  "day": 15,                // Zorunlu: 1-31
  "events": [...],          // Zorunlu: En az 1 olay
  "thresholds": {...},      // Opsiyonel: Özel threshold'lar
  "use_synthetic": false    // Opsiyonel: Test verisi
}
```

### Response Format (Başarılı)
```json
{
  "success": true,
  "data": {
    "location": {...},
    "date": {...},
    "probabilities": {...},
    "metadata": {...}
  }
}
```

### Response Format (Hata)
```json
{
  "success": false,
  "error": "Error message"
}
```

## 🔒 Validasyon Kuralları

API aşağıdaki kontrolleri yapar:
- ✅ Content-Type: application/json kontrolü
- ✅ Zorunlu alan kontrolü (lat, lon, month, day, events)
- ✅ Parametre tipi kontrolü (float/int)
- ✅ Aralık kontrolü (lat: -90/90, lon: -180/180, month: 1-12, day: 1-31)
- ✅ Events listesi boş olmamalı
- ✅ Geçersiz event isimleri kontrolü
- ✅ Thresholds dict formatı kontrolü

## 🌐 CORS Yapılandırması

CORS tüm originler için etkinleştirildi:
```python
CORS(app)  # Tüm originler için
```

Production'da belirli originlere sınırlandırılabilir:
```python
CORS(app, origins=["https://yourdomain.com"])
```

## 📊 Desteklenen Olaylar

| Olay | Varsayılan Threshold |
|------|---------------------|
| `wind_high` | 10.0 m/s |
| `rain_high` | 10.0 mm/gün |
| `wave_high` | 2.0 m |
| `storm_high` | 20.0 mm/h |
| `fog_low` | 0.5 AOD |
| `sst_high` | 25.0 °C |
| `current_strong` | 0.5 m/s |
| `tide_high` | 1.0 m |
| `ssha_high` | 0.05 m |

## 🐛 Hata Kodları

| Kod | Durum | Örnek |
|-----|-------|-------|
| 200 | Başarılı | Normal işlem |
| 400 | Bad Request | Eksik/geçersiz parametreler |
| 404 | Not Found | Geçersiz endpoint |
| 405 | Method Not Allowed | Yanlış HTTP metodu |
| 500 | Internal Server Error | Beklenmeyen hatalar |

## 🚀 Production Deployment

### Gunicorn ile
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Docker ile
```bash
docker build -t nasa-probability-api .
docker run -p 5000:5000 nasa-probability-api
```

### Nginx Reverse Proxy
```nginx
location /api/ {
    proxy_pass http://localhost:5000/;
    proxy_set_header Host $host;
    proxy_connect_timeout 120s;
}
```

## 📁 Proje Yapısı

```
marineguard-api/
├── app.py                           # Flask API
├── calculate_ocean_probabilities.py # Olasılık hesaplama modülü
├── requirements.txt                 # Python bağımlılıkları
├── test_api.py                      # Test suite
├── README_API.md                    # API dokümantasyonu
├── README_PROBABILITIES.md          # Modül dokümantasyonu
├── SUMMARY.md                       # Genel proje özeti
├── postman_collection.json          # Postman collection
├── .gitignore                       # Git ignore
└── example_usage.py                 # Örnek kullanımlar
```

## 🔗 İlgili Endpoint'ler

1. **GET /health** → API durumu
2. **GET /events** → Mevcut olaylar
3. **POST /calculate_probability** → Olasılık hesaplama

## 📝 Örnek Request/Response

### Python
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

### JavaScript
```javascript
fetch('http://localhost:5000/calculate_probability', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    lat: 40.0,
    lon: 29.0,
    month: 7,
    day: 15,
    events: ['wind_high', 'wave_high'],
    use_synthetic: true
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
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

## ✨ Öne Çıkan Özellikler

1. ✅ **RESTful Design** - Standart HTTP metodları ve durum kodları
2. ✅ **JSON API** - JSON request ve response formatı
3. ✅ **CORS Enabled** - Frontend entegrasyonu hazır
4. ✅ **Error Handling** - Kapsamlı hata yönetimi
5. ✅ **Input Validation** - Tüm parametreler validate edilir
6. ✅ **Logging** - Detaylı log kaydı
7. ✅ **Documented** - Kapsamlı dokümantasyon
8. ✅ **Tested** - 10 test senaryosu ile test edildi
9. ✅ **Production Ready** - Gunicorn desteği
10. ✅ **Postman Collection** - Hazır API test collection'ı

## 🎯 Sonuç

Flask API başarıyla oluşturuldu ve test edildi! API:
- ✅ Çalışıyor ve erişilebilir (http://localhost:5000)
- ✅ Tüm endpoint'ler test edildi
- ✅ Hata yönetimi doğrulandı
- ✅ CORS etkinleştirildi
- ✅ JSON formatında veri alıp dönüyor
- ✅ Production-ready (Gunicorn desteği)

**API Durumu:** 🟢 ONLINE  
**Test Durumu:** ✅ BAŞARILI  
**Dokümantasyon:** 📚 TAMAMLANDI

---

**Oluşturma Tarihi:** 5 Ekim 2025  
**API Versiyonu:** 1.0.0  
**Python Versiyonu:** 3.11+  
**Flask Versiyonu:** 3.0+

