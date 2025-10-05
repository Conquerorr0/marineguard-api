# 🚀 Render.com'a 5 Dakikada Deploy

## Hızlı Adımlar

### 1. GitHub'a Push (1 dakika)
```bash
# GitHub'da repo oluştur: nasa-probability-api

git remote add origin https://github.com/YOUR_USERNAME/nasa-probability-api.git
git push -u origin main
```

### 2. Render.com'da Service Oluştur (2 dakika)

1. https://dashboard.render.com → **"New +" → "Web Service"**

2. **GitHub repo'nuzu bağla ve seç**

3. **Ayarlar:**
   - Name: `nasa-probability-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --timeout 300 --workers 2 --bind 0.0.0.0:$PORT`
   - Plan: **Free** ✅

4. **Environment Variables ekle:**
   - `EARTHDATA_USERNAME` = `FatihAltuntas`
   - `EARTHDATA_PASSWORD` = (şifreniz)

5. **"Create Web Service"** tıkla

### 3. Test Et (1 dakika)

Deploy tamamlanınca (2-3 dakika):

```bash
# Health check
curl https://nasa-probability-api.onrender.com/health

# Test
curl -X POST https://nasa-probability-api.onrender.com/calculate_probability \
  -H "Content-Type: application/json" \
  -d '{"lat":40,"lon":29,"month":7,"day":15,"events":["wind_high"],"use_synthetic":true}'
```

## ✅ Bitti!

API'niz şu adreste çalışıyor:
```
https://nasa-probability-api.onrender.com
```

**Heroku'dan daha hızlı ve daha az timeout!** 🎉

