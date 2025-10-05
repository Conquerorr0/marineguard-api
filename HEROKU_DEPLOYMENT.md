# Heroku Deployment Guide

Flask API'yi Heroku'ya deploy etmek için adım adım rehber.

## 📋 Ön Gereksinimler

1. **Heroku Hesabı:** https://signup.heroku.com/
2. **Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli
3. **Git:** Kurulu olmalı
4. **NASA Earthdata Hesabı:** https://urs.earthdata.nasa.gov/ (opsiyonel, gerçek veri için)

## 🚀 Deployment Adımları

### 1. Git Repository Başlatma

```bash
# Git repository'sini başlat
git init

# .gitignore dosyasını kontrol et (zaten oluşturuldu)
cat .gitignore
```

**Açıklama:** `git init` komutu mevcut dizinde yeni bir Git repository'si oluşturur. Bu, projenizin version control altına alınmasını sağlar.

### 2. Heroku Uygulaması Oluşturma

```bash
# Heroku'ya giriş yap
heroku login

# Yeni Heroku uygulaması oluştur
heroku create nasa-probability-api

# Veya otomatik isim ver
heroku create
```

**Açıklama:** `heroku create` komutu Heroku'da yeni bir uygulama oluşturur ve otomatik olarak Git remote'u ekler. Uygulama ismi benzersiz olmalıdır.

**Çıktı örneği:**
```
Creating ⬢ nasa-probability-api... done
https://nasa-probability-api.herokuapp.com/ | https://git.heroku.com/nasa-probability-api.git
```

### 3. Environment Variables Ayarlama (Opsiyonel)

NASA Earthdata kimlik bilgileri için:

```bash
# Earthdata credentials ekle
heroku config:set EARTHDATA_USERNAME=your_username
heroku config:set EARTHDATA_PASSWORD=your_password

# Veya token kullan
heroku config:set EARTHDATA_TOKEN=your_token

# Environment variables'ı görüntüle
heroku config
```

**Açıklama:** `heroku config:set` komutu Heroku'da environment variable'lar oluşturur. Bu bilgiler güvenli bir şekilde saklanır ve uygulamanız tarafından erişilebilir.

### 4. Dosyaları Git'e Ekleme

```bash
# Tüm dosyaları staging area'ya ekle
git add .

# Hangi dosyaların ekleneceğini kontrol et
git status
```

**Açıklama:** `git add .` komutu mevcut dizindeki tüm değişiklikleri staging area'ya ekler. `.gitignore` dosyasında belirtilen dosyalar hariç tutulur.

### 5. Commit Oluşturma

```bash
# Initial commit oluştur
git commit -m "Initial deploy: Flask API with NASA EarthData integration"

# Commit geçmişini görüntüle
git log --oneline
```

**Açıklama:** `git commit` komutu staging area'daki değişiklikleri kalıcı olarak kaydeder. `-m` flag'i ile commit mesajı eklenir.

### 6. Heroku'ya Push (Deploy)

```bash
# Heroku'ya push et (deploy)
git push heroku main

# Veya master branch kullanıyorsanız
git push heroku master
```

**Açıklama:** `git push heroku main` komutu local repository'nizdeki değişiklikleri Heroku'ya gönderir. Bu, otomatik olarak build ve deploy sürecini başlatır.

**Deploy süreci:**
1. Heroku kodu alır
2. `runtime.txt`'den Python versiyonunu belirler
3. `requirements.txt`'deki paketleri yükler
4. `Procfile`'daki komutu çalıştırır

### 7. Uygulamayı Başlatma

```bash
# En az 1 web dyno çalıştır
heroku ps:scale web=1

# Dyno durumunu kontrol et
heroku ps
```

**Açıklama:** `heroku ps:scale web=1` komutu 1 web dyno'su başlatır. Free tier'da 1 dyno ücretsizdir.

### 8. Uygulamayı Açma

```bash
# Uygulamayı tarayıcıda aç
heroku open

# Veya URL'i manuel olarak ziyaret et
# https://your-app-name.herokuapp.com
```

## 🧪 Deployment Sonrası Test

### API'yi Test Etme

```bash
# Health check
curl https://your-app-name.herokuapp.com/health

# Get events
curl https://your-app-name.herokuapp.com/events

# Calculate probability
curl -X POST https://your-app-name.herokuapp.com/calculate_probability \
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

### Test Script Çalıştırma

```bash
# Local test (Heroku URL ile)
# test_all_datasets.py dosyasında API_URL'i güncelle
python test_all_datasets.py
```

## 📊 Heroku Komutları

### Log Görüntüleme

```bash
# Canlı log stream
heroku logs --tail

# Son 100 satır
heroku logs -n 100

# Sadece app logları
heroku logs --source app
```

**Açıklama:** Loglar uygulamanızdaki hataları ve aktiviteyi izlemek için kritiktir.

### Uygulama Bilgileri

```bash
# Uygulama bilgilerini görüntüle
heroku info

# Config variables
heroku config

# Add-on'ları listele
heroku addons
```

### Dyno Yönetimi

```bash
# Dyno'ları yeniden başlat
heroku restart

# Dyno durumunu kontrol et
heroku ps

# Dyno tipini değiştir (upgrade)
heroku ps:type web=standard-1x
```

### Database İşlemleri (İleride kullanım için)

```bash
# PostgreSQL ekle
heroku addons:create heroku-postgresql:mini

# Database URL'i görüntüle
heroku config:get DATABASE_URL

# PostgreSQL'e bağlan
heroku pg:psql
```

## 🔧 Yapılandırma Dosyaları

### 1. Procfile
```
web: gunicorn app:app
```
- `web`: Dyno tipi
- `gunicorn app:app`: Çalıştırılacak komut
- `app:app`: `app.py` dosyasındaki `app` Flask instance'ı

### 2. runtime.txt
```
python-3.12.3
```
- Heroku'nun kullanacağı Python versiyonunu belirtir
- Desteklenen versiyonlar: https://devcenter.heroku.com/articles/python-support

### 3. requirements.txt
```
flask==3.0.0
gunicorn==21.2.0
flask-cors==4.0.1
xarray==2024.6.0
netcdf4==1.6.5
numpy==1.26.4
scipy==1.13.1
dask==2024.5.0
requests==2.31.0
```
- Tüm Python bağımlılıklarını spesifik versiyonlarla listeler

## ⚙️ Environment Variables

### .netrc Dosyası Oluşturma (Heroku'da)

NASA Earthdata için credentials:

```bash
# Setup script çalıştır
heroku run python setup_netrc.py

# Veya manuel olarak
heroku run bash
> cat > ~/.netrc << EOF
machine urs.earthdata.nasa.gov
    login your_username
    password your_password
EOF
> chmod 600 ~/.netrc
> exit
```

## 🐛 Troubleshooting

### Problem: Application Error

```bash
# Logları kontrol et
heroku logs --tail

# Dyno'ları yeniden başlat
heroku restart
```

### Problem: Slow Response

```bash
# Timeout artır (Procfile'da)
# web: gunicorn app:app --timeout 120

# Veya daha fazla worker ekle
# web: gunicorn app:app --workers 4
```

### Problem: Memory Limit

```bash
# Dyno'yu upgrade et
heroku ps:type web=standard-1x

# Memory kullanımını kontrol et
heroku ps -a your-app-name
```

### Problem: Build Failure

```bash
# Requirements.txt'yi kontrol et
cat requirements.txt

# Cache'i temizle ve yeniden deploy et
heroku repo:purge_cache
git commit --allow-empty -m "Rebuild"
git push heroku main
```

## 📈 Monitoring ve Analytics

### Heroku Dashboard

```bash
# Dashboard'u aç
heroku dashboard
```

### Metrics (Ücretli)

```bash
# Heroku Metrics ekle
heroku addons:create heroku-metrics

# Metrics görüntüle
heroku metrics
```

### Logs Draining (İleride)

```bash
# Papertrail ekle (log management)
heroku addons:create papertrail

# Logları görüntüle
heroku addons:open papertrail
```

## 🔄 Güncelleme ve Yeniden Deploy

```bash
# Değişiklikleri yap
# ...kod değişiklikleri...

# Git'e commit et
git add .
git commit -m "Update: Added new feature"

# Heroku'ya push et
git push heroku main

# Logları izle
heroku logs --tail
```

## 💰 Maliyet Optimizasyonu

### Free Tier Limits

- **Dyno Hours:** 550 saat/ay (credit card eklerseniz 1000 saat)
- **Slug Size:** Max 500 MB
- **Sleep:** 30 dakika inaktiviteden sonra uyur

### Tips

1. **Tek dyno kullanın** (free tier)
2. **Cache ekleyin** (Redis - ileride)
3. **Auto-sleep'e izin verin** (free tier'da otomatik)
4. **Lightweight dependencies** kullanın

## 📚 Faydalı Linkler

- **Heroku Python Docs:** https://devcenter.heroku.com/articles/getting-started-with-python
- **Heroku Config Vars:** https://devcenter.heroku.com/articles/config-vars
- **Heroku Logs:** https://devcenter.heroku.com/articles/logging
- **Heroku Pricing:** https://www.heroku.com/pricing

## ✅ Checklist

Deploy öncesi kontrol listesi:

- [ ] `Procfile` oluşturuldu
- [ ] `runtime.txt` oluşturuldu
- [ ] `requirements.txt` güncellendi (spesifik versiyonlar)
- [ ] `.gitignore` yapılandırıldı
- [ ] Environment variables belirlendi
- [ ] Git repository başlatıldı
- [ ] Heroku CLI kuruldu
- [ ] Heroku'ya login yapıldı
- [ ] Test edildi (local)

Deploy sonrası kontrol:

- [ ] Uygulama başarıyla deploy edildi
- [ ] Health check endpoint çalışıyor
- [ ] API endpoint'leri test edildi
- [ ] Loglar kontrol edildi
- [ ] Environment variables doğru ayarlandı

## 🎯 Özet

**Tam Deploy Komut Dizisi:**

```bash
# 1. Git başlat
git init

# 2. Heroku uygulaması oluştur
heroku login
heroku create nasa-probability-api

# 3. Environment variables (opsiyonel)
heroku config:set EARTHDATA_USERNAME=your_username
heroku config:set EARTHDATA_PASSWORD=your_password

# 4. Git'e ekle ve commit et
git add .
git commit -m "Initial deploy: Flask API with NASA EarthData integration"

# 5. Heroku'ya push
git push heroku main

# 6. Dyno'yu scale et
heroku ps:scale web=1

# 7. Aç ve test et
heroku open
heroku logs --tail
```

---

**Not:** Bu rehber Heroku free tier'ı hedeflemektedir. Production kullanım için Hobby ($7/ay) veya Professional ($25+/ay) tier'ları düşünün.

