#!/bin/bash

# NASA EarthData Probability API - Heroku Deployment Script
# Bu script Heroku'ya deploy için gerekli tüm komutları içerir

echo "=========================================="
echo "HEROKU DEPLOYMENT - NASA Probability API"
echo "=========================================="
echo ""

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Git Repository Başlatma
echo -e "${YELLOW}[1/7] Git Repository Başlatılıyor...${NC}"
echo "Komut: git init"
echo "Açıklama: Yeni bir Git repository'si oluşturur"
echo ""
git init
echo -e "${GREEN}✓ Git repository başlatıldı${NC}"
echo ""

# 2. Heroku Login
echo -e "${YELLOW}[2/7] Heroku'ya Login...${NC}"
echo "Komut: heroku login"
echo "Açıklama: Heroku hesabınıza giriş yapar (tarayıcı açılacak)"
echo ""
heroku login
echo -e "${GREEN}✓ Heroku login başarılı${NC}"
echo ""

# 3. Heroku App Oluşturma
echo -e "${YELLOW}[3/7] Heroku App Oluşturuluyor...${NC}"
echo "Komut: heroku create nasa-probability-api"
echo "Açıklama: Heroku'da yeni bir uygulama oluşturur"
echo "Not: Eğer isim kullanımdaysa, farklı bir isim deneyin"
echo ""
heroku create nasa-probability-api
echo -e "${GREEN}✓ Heroku app oluşturuldu${NC}"
echo ""

# 4. Environment Variables (Opsiyonel)
echo -e "${YELLOW}[4/7] Environment Variables Ayarlanıyor (Opsiyonel)...${NC}"
echo "Komutlar:"
echo "  heroku config:set EARTHDATA_USERNAME=your_username"
echo "  heroku config:set EARTHDATA_PASSWORD=your_password"
echo "Açıklama: NASA Earthdata kimlik bilgilerini ayarlar"
echo "Not: Şimdilik atlıyoruz (sentetik veri kullanabilirsiniz)"
echo ""
# heroku config:set EARTHDATA_USERNAME=your_username
# heroku config:set EARTHDATA_PASSWORD=your_password
echo -e "${GREEN}✓ Environment variables atlandı (opsiyonel)${NC}"
echo ""

# 5. Git Add
echo -e "${YELLOW}[5/7] Dosyalar Git'e Ekleniyor...${NC}"
echo "Komut: git add ."
echo "Açıklama: Tüm dosyaları staging area'ya ekler (.gitignore hariç)"
echo ""
git add .
echo -e "${GREEN}✓ Dosyalar eklendi${NC}"
echo ""

# 6. Git Commit
echo -e "${YELLOW}[6/7] Commit Oluşturuluyor...${NC}"
echo "Komut: git commit -m 'Initial deploy: Flask API with NASA EarthData integration'"
echo "Açıklama: Değişiklikleri kalıcı olarak kaydeder"
echo ""
git commit -m "Initial deploy: Flask API with NASA EarthData integration"
echo -e "${GREEN}✓ Commit oluşturuldu${NC}"
echo ""

# 7. Heroku'ya Push (Deploy)
echo -e "${YELLOW}[7/7] Heroku'ya Deploy Ediliyor...${NC}"
echo "Komut: git push heroku main"
echo "Açıklama: Kodu Heroku'ya gönderir ve build sürecini başlatır"
echo "Not: Bu işlem birkaç dakika sürebilir"
echo ""
git push heroku main
echo -e "${GREEN}✓ Deploy tamamlandı${NC}"
echo ""

# 8. Dyno Scale
echo -e "${YELLOW}[Bonus] Dyno Scale Ediliyor...${NC}"
echo "Komut: heroku ps:scale web=1"
echo "Açıklama: 1 web dyno başlatır"
echo ""
heroku ps:scale web=1
echo -e "${GREEN}✓ Dyno başlatıldı${NC}"
echo ""

# Özet
echo "=========================================="
echo "DEPLOYMENT TAMAMLANDI!"
echo "=========================================="
echo ""
echo "Sonraki Adımlar:"
echo "1. Uygulamayı aç:     heroku open"
echo "2. Logları görüntüle: heroku logs --tail"
echo "3. Test et:           python test_all_datasets.py"
echo ""
echo "Faydalı Komutlar:"
echo "  heroku info          # Uygulama bilgileri"
echo "  heroku config        # Environment variables"
echo "  heroku restart       # Uygulamayı yeniden başlat"
echo "  heroku ps            # Dyno durumu"
echo ""
echo "=========================================="

