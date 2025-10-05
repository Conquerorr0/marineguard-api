# Heroku Güncellemesi - Root Endpoint Eklendi

## Yapılan Değişiklikler

1. ✅ **Root `/` endpoint eklendi** - Artık `heroku open` çalışacak
2. ✅ **`.python-version` dosyası eklendi** - Heroku uyarısı giderildi  
3. ✅ **Test script'i oluşturuldu** - `quick_heroku_test.py`

## Heroku'ya Push Komutları

```bash
# 1. Değişiklikleri ekle
git add .

# 2. Commit et
git commit -m "Add root endpoint and .python-version file"

# 3. Heroku'ya push et
git push heroku main

# 4. Test et
python quick_heroku_test.py
```

## Yeni Root Endpoint Response

Şimdi `https://nasa-probability-api-2b173d22b072.herokuapp.com/` açtığınızda:

```json
{
  "message": "Welcome to NASA EarthData Probability API",
  "version": "1.0.0",
  "endpoints": {
    "health": {
      "method": "GET",
      "path": "/health",
      "description": "Health check endpoint"
    },
    "events": {
      "method": "GET",
      "path": "/events",
      "description": "Get available events and their configurations"
    },
    "calculate_probability": {
      "method": "POST",
      "path": "/calculate_probability",
      "description": "Calculate event probabilities for a location and date",
      "example": {
        "lat": 40.0,
        "lon": 29.0,
        "month": 7,
        "day": 15,
        "events": ["wind_high", "wave_high"],
        "use_synthetic": true
      }
    }
  },
  "documentation": "See README_API.md for detailed documentation",
  "status": "online"
}
```

## Manuel Test Komutları

### 1. Root Endpoint (Browser'da da açılabilir):
```bash
curl https://nasa-probability-api-2b173d22b072.herokuapp.com/
```

### 2. Health Check:
```bash
curl https://nasa-probability-api-2b173d22b072.herokuapp.com/health
```

### 3. Available Events:
```bash
curl https://nasa-probability-api-2b173d22b072.herokuapp.com/events
```

### 4. Calculate Probability:
```bash
curl -X POST https://nasa-probability-api-2b173d22b072.herokuapp.com/calculate_probability \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 40.0,
    "lon": 29.0,
    "month": 7,
    "day": 15,
    "events": ["wind_high", "wave_high", "sst_high"],
    "use_synthetic": true
  }'
```

## Python Test Script

```bash
python quick_heroku_test.py
```

Bu script otomatik olarak tüm endpoint'leri test eder.

## Windows PowerShell için POST Test

```powershell
$body = @{
    lat = 40.0
    lon = 29.0
    month = 7
    day = 15
    events = @("wind_high", "wave_high")
    use_synthetic = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://nasa-probability-api-2b173d22b072.herokuapp.com/calculate_probability" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## Beklenen Sonuç

Artık `heroku open` komutu ile doğrudan API ana sayfasını göreceksiniz ve 404 hatası almayacaksınız! 🎉

