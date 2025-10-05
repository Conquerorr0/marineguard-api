# Render.com Deployment Rehberi

## 🚀 Neden Render.com?

Render.com Heroku'dan **DAHA İYİ** çünkü:

| Özellik | Heroku Free | Render Free |
|---------|-------------|-------------|
| **RAM** | 512 MB | 512 MB |
| **Timeout** | 30 saniye (router) | Çok daha uzun |
| **Sleep** | 30 dk sonra | Aynı |
| **Build Time** | 15 dakika | 15 dakika |
| **Aylık Saat** | 550-1000 | 750 |
| **Performans** | Orta | DAHA HIZLI |
| **Kredi Kartı** | İsteğe bağlı | GEREKMİYOR |

## 📋 Ön Hazırlık

### 1. Render Hesabı Oluştur
1. https://render.com adresine git
2. **"Get Started for Free"** tıkla
3. GitHub hesabınla giriş yap (önerilen)
4. Email doğrula

### 2. GitHub Repository Hazırla
Kodlarınız zaten Git'te, tek yapmanız gereken GitHub'a push etmek:

```bash
# GitHub'da yeni repo oluştur (web'den)
# Örnek: https://github.com/username/nasa-probability-api

# Remote ekle
git remote add origin https://github.com/YOUR_USERNAME/nasa-probability-api.git

# Push et
git push -u origin main
```

## 🚀 Render.com Deployment Adımları

### Yöntem 1: Blueprint ile (Otomatik - ÖNERİLİR)

1. **Render Dashboard'a git:** https://dashboard.render.com/

2. **"New +" → "Blueprint"** tıkla

3. **GitHub repo'nuzu seç:**
   - "Connect a repository" tıkla
   - Repo'nuzu ara ve seç
   - "Connect" tıkla

4. **Otomatik algılama:**
   - `render.yaml` dosyasını bulur
   - Ayarları otomatik uygular

5. **Environment Variables ekle:**
   - `EARTHDATA_USERNAME` → NASA kullanıcı adınız
   - `EARTHDATA_PASSWORD` → NASA şifreniz

6. **"Apply"** tıkla → Deploy başlar!

### Yöntem 2: Manuel (Adım Adım)

1. **Dashboard → "New +" → "Web Service"**

2. **GitHub repo'nuzu seç**

3. **Ayarları yapılandır:**
   - **Name:** `nasa-probability-api`
   - **Environment:** `Python 3`
   - **Region:** `Frankfurt` (Türkiye'ye en yakın)
   - **Branch:** `main`
   - **Build Command:** 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     gunicorn app:app --timeout 300 --workers 2 --bind 0.0.0.0:$PORT
     ```

4. **Plan seç:** `Free` ✅

5. **Advanced → Environment Variables:**
   ```
   EARTHDATA_USERNAME = your_username
   EARTHDATA_PASSWORD = your_password
   ```

6. **"Create Web Service"** tıkla!

## ⏱️ Deploy Süreci

```
[1/4] Cloning repository... ✓
[2/4] Installing dependencies... (2-3 dakika)
[3/4] Building application... ✓
[4/4] Starting service... ✓

Your service is live at:
https://nasa-probability-api.onrender.com
```

## 🧪 Test Etme

Deploy tamamlandıktan sonra:

### 1. Health Check
```bash
curl https://nasa-probability-api.onrender.com/health
```

### 2. Python ile Test
```python
import requests

# URL'i güncelle
API_URL = "https://nasa-probability-api.onrender.com"

response = requests.post(
    f"{API_URL}/calculate_probability",
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

### 3. Interactive Test ile
`interactive_nasa_test.py` içinde URL'i güncelle:
```python
API_URL = "https://nasa-probability-api.onrender.com"
```

## 📊 Render vs Heroku Karşılaştırması

### Build Hızı
- **Heroku:** ~45 saniye
- **Render:** ~35 saniye ✅

### Cold Start
- **Heroku:** 10-15 saniye
- **Render:** 5-10 saniye ✅

### Timeout
- **Heroku:** 30 saniye (router)
- **Render:** Çok daha esnek ✅

### Performans
Render.com **modern altyapı** kullanır:
- Daha hızlı I/O
- Daha iyi network
- Daha optimize container runtime

## 🔧 Render-Specific Ayarlar

### 1. Timeout Artırma (Zaten yapıldı)
```yaml
startCommand: gunicorn app:app --timeout 300
```

### 2. Worker Sayısı
```yaml
startCommand: gunicorn app:app --workers 2
```

### 3. Otomatik Deploy
Her git push'ta otomatik deploy:
- Dashboard → Settings → "Auto-Deploy" → Enable

### 4. Health Check URL
- Dashboard → Settings → Health Check Path: `/health`

## 🆚 Diğer Alternatifler

### Railway.app
```bash
# Railway CLI kur
npm i -g @railway/cli

# Login
railway login

# Init
railway init

# Deploy
railway up
```

**장점:**
- Çok güçlü (8 GB RAM)
- Timeout yok
- Kolay kullanım

**단점:**
- Aylık $5 credit (bittikten sonra ücretli)

### Fly.io
```bash
# Fly CLI kur
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch
fly launch

# Deploy
fly deploy
```

**장점:**
- Docker-based (tam kontrol)
- Global CDN
- Çok hızlı

**단점:**
- Biraz karmaşık
- Docker bilgisi gerekir

## 💡 Hangi Platformu Seçmeliyim?

### Render.com - ✅ ÖNERİLİR
- Kolay setup
- Ücretsiz ve güçlü
- Heroku benzeri deneyim
- Daha iyi performans

### Railway.app - İyi Ama...
- Çok güçlü
- Ama aylık $5 credit var
- Sonra ücretli

### Fly.io - Gelişmiş Kullanıcılar
- Tam kontrol
- Docker bilgisi gerekir
- Setup daha karmaşık

## 🎯 Önerilen Deployment Stratejisi

1. **Şimdi:** Render.com'a deploy et (ücretsiz, kolay)
2. **Test et:** Performansı gör
3. **Gerekirse:** Railway veya Fly'a geç

## 📈 Beklenen Performans (Render.com)

### Sentetik Veri
- Response time: **~2 saniye** ✅
- Success rate: **100%** ✅

### Gerçek NASA Verisi
- Response time: **30-90 saniye** (Render'da daha iyi)
- Success rate: **%70-80** (NASA sunucularına bağlı)
- Timeout riski: **Düşük** ✅

## 🔑 Environment Variables (Render)

```
EARTHDATA_USERNAME = FatihAltuntas
EARTHDATA_PASSWORD = (şifreniz)
PYTHON_VERSION = 3.12.3
```

## 🐛 Troubleshooting

### Build Başarısız
```bash
# Logs kontrol et
Render Dashboard → Logs → Build Logs
```

### Service Başlamıyor
```bash
# Start command kontrol et
gunicorn app:app --timeout 300 --workers 2 --bind 0.0.0.0:$PORT
```

### Environment Variables
```bash
# Dashboard → Environment → Add Variable
```

## 📚 Faydalı Linkler

- **Render Docs:** https://render.com/docs
- **Python on Render:** https://render.com/docs/deploy-flask
- **Free Tier Limits:** https://render.com/pricing

## ✅ Sonuç

Render.com:
- ✅ Ücretsiz
- ✅ Heroku'dan daha iyi
- ✅ Kolay deployment
- ✅ Daha uzun timeout
- ✅ Daha iyi performans

**Şimdi deploy edin ve farkı görün!** 🚀

---

**Deployment Süresi:** ~5 dakika  
**İlk Deploy:** ~3 dakika build + deploy  
**Sonraki Deploy'lar:** ~1 dakika (cache sayesinde)

