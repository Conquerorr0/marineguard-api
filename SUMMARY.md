# NASA EarthData Olasılık Hesaplama Projesi - Özet

## 📋 Proje Hakkında

Bu proje, NASA EarthData OPeNDAP servislerinden 1991-2020 arası okyanus ve atmosfer verilerini kullanarak belirli bir konum ve tarih için empirik olay olasılıklarını hesaplar.

## 📦 Oluşturulan Dosyalar

### 1. `calculate_ocean_probabilities.py` (Ana Modül - 642 satır)
**Ana Fonksiyon:**
```python
def calculate_probabilities(
    lat: float, 
    lon: float, 
    month: int, 
    day: int,
    events: List[str],
    thresholds: Optional[Dict[str, float]] = None,
    use_synthetic: bool = False
) -> Dict[str, float]
```

**Özellikler:**
- ✅ 9 farklı NASA veri seti desteği
- ✅ xarray ile OPeNDAP erişimi
- ✅ Empirik olasılık hesaplama
- ✅ NaN filtreleme
- ✅ Kapsamlı hata yönetimi (try-except)
- ✅ Logging sistemi
- ✅ Sentetik test verisi (numpy.random)
- ✅ Özelleştirilebilir threshold'lar
- ✅ JSON sonuç formatı

### 2. `example_usage.py` (Örnek Kullanım - 264 satır)
**İçerik:**
- 6 farklı kullanım senaryosu
- Temel kullanım örneği
- Özel threshold'larla kullanım
- Tüm olayları kontrol etme
- Lokasyon karşılaştırması
- Mevsimsel analiz
- JSON export

### 3. `requirements.txt` (Bağımlılıklar)
```
xarray>=2023.1.0
numpy>=1.24.0,<2.0.0
netCDF4>=1.6.0
scipy>=1.10.0
dask>=2023.1.0
```

### 4. `README_PROBABILITIES.md` (Detaylı Dokümantasyon)
- Kurulum talimatları
- Kullanım örnekleri
- Veri setleri tablosu
- API dokümantasyonu

## 🌊 Desteklenen Veri Setleri

| # | Olay | Veri Seti | Yıl Aralığı | Threshold |
|---|------|-----------|-------------|-----------|
| 1 | `wind_high` | CCMP V2.0 Wind | 1991-2020 | 10 m/s |
| 2 | `rain_high` | GPCP Daily V3.2 | 1991-2020 | 10 mm/gün |
| 3 | `wave_high` | Merged Altimeter SWH | 1993-2020 | 2 m |
| 4 | `storm_high` | TRMM/GPM TCPF | 1998-2020 | 20 mm/h |
| 5 | `fog_low` | MODIS AOD | 2000-2020 | 0.5 |
| 6 | `sst_high` | NOAA OI SST V2 | 1991-2020 | 25 °C |
| 7 | `current_strong` | OSCAR V2.0 | 1993-2020 | 0.5 m/s |
| 8 | `tide_high` | TPXO9 Tide Model | 1991-2020 | 1.0 m |
| 9 | `ssha_high` | MEaSUREs SSHA | 1993-2020 | 0.05 m |

## 🚀 Hızlı Başlangıç

### Kurulum
```bash
pip install -r requirements.txt
```

### Temel Kullanım
```python
from calculate_ocean_probabilities import calculate_probabilities

# İstanbul için 15 Temmuz'da yüksek rüzgar olasılığı
results = calculate_probabilities(
    lat=40.0,
    lon=29.0,
    month=7,
    day=15,
    events=['wind_high'],
    use_synthetic=True  # Test için
)

print(results)
# Çıktı: {'wind_high': 0.23}  # %23 olasılık
```

### Test Çalıştırma
```bash
# Ana modül testleri (3 test senaryosu)
python calculate_ocean_probabilities.py

# Örnek kullanımlar (6 örnek)
python example_usage.py

# Tek bir örnek
python -c "from example_usage import example_1_basic; example_1_basic()"
```

## 🔬 Teknik Detaylar

### Empirik Olasılık Hesaplama
```
Olasılık = (Threshold'u aşan yıl sayısı) / (Toplam geçerli yıl sayısı)
```

Örnek:
- 30 yıl veri (1991-2020)
- Threshold: 10 m/s rüzgar
- 7 yılda 10 m/s'yi aştı
- Olasılık: 7/30 = 0.233 (%23.3)

### Veri İşleme Süreci
1. **Veri Çekme:** xarray ile OPeNDAP URL'den subset alma
2. **Lokasyon Seçimi:** `ds.sel(lat=lat, lon=lon, method='nearest')`
3. **Tarih Filtreleme:** Her yıl için aynı ay/gün
4. **NaN Filtreleme:** Eksik verileri çıkar
5. **Threshold Karşılaştırma:** `data > threshold`
6. **Olasılık Hesaplama:** `sum / count`

### Türetilmiş Değişkenler
- **Rüzgar/Akıntı Hızı:** `sqrt(u² + v²)` (vektör büyüklüğü)
- **Gelgit Yüksekliği:** M2 ve S2 harmonik bileşenlerinden

## 📊 Örnek Çıktılar

### Test Senaryosu (Sentetik Veri)
```json
{
  "wind_high": 0.2500,
  "rain_high": 0.1379,
  "wave_high": 0.2308,
  "storm_high": 0.2609,
  "fog_low": 0.2778,
  "sst_high": 0.2414,
  "current_strong": 0.2222,
  "tide_high": 0.2308,
  "ssha_high": 0.2400
}
```

### Yorumlama
- `wind_high: 0.25` → Son 30 yılda %25 olasılıkla 10 m/s üzeri rüzgar
- `sst_high: 0.24` → %24 olasılıkla 25°C üzeri deniz suyu sıcaklığı

## ⚠️ Önemli Notlar

### NumPy Uyumluluğu
Mevcut ortamda NumPy 2.x var, ancak xarray/cftime NumPy 1.x gerektiriyor. 
Çözüm: `pip install "numpy>=1.24.0,<2.0.0"`

### NASA Earthdata Kimlik Doğrulama
Gerçek verilere erişim için:
1. NASA Earthdata hesabı: https://urs.earthdata.nasa.gov/
2. `.netrc` dosyası yapılandırması
3. Alternatif: `use_synthetic=True` ile test

### Performans
- Her olay için ~30 URL isteği (1991-2020)
- İlk çalıştırma: ~30-60 saniye
- Sentetik veri ile: <1 saniye

## 🎯 Kullanım Senaryoları

### 1. Denizcilik Risk Analizi
```python
# Karadeniz'de kış fırtına riski
results = calculate_probabilities(
    lat=41.0, lon=41.0, month=1, day=15,
    events=['wind_high', 'wave_high', 'storm_high']
)
```

### 2. Balıkçılık Planlaması
```python
# Akdeniz'de yaz ayı koşulları
results = calculate_probabilities(
    lat=36.0, lon=34.0, month=7, day=1,
    events=['sst_high', 'current_strong']
)
```

### 3. Liman Operasyonları
```python
# Gelgit ve görüş mesafesi
results = calculate_probabilities(
    lat=40.0, lon=29.0, month=12, day=15,
    events=['tide_high', 'fog_low']
)
```

## 📈 Geliştirme Fırsatları

### Kısa Vadeli
- [ ] Cache mekanizması (dosya sistemi)
- [ ] Paralel veri çekme (multiprocessing)
- [ ] Progress bar (tqdm)
- [ ] CLI interface (argparse)

### Orta Vadeli
- [ ] Veritabanı entegrasyonu (PostgreSQL/PostGIS)
- [ ] Web API (FastAPI)
- [ ] Görselleştirme (matplotlib/plotly)
- [ ] Batch processing

### Uzun Vadeli
- [ ] Makine öğrenmesi ile tahmin
- [ ] Zamansal trend analizi
- [ ] İklim değişikliği etkileri
- [ ] Real-time veri entegrasyonu

## 🧪 Test Sonuçları

### Ana Modül Testleri
✅ Test 1: Sentetik veri ile 9 olay (BAŞARILI)
✅ Test 2: Özel threshold'lar (BAŞARILI)
✅ Test 3: Gerçek veri fallback (BAŞARILI)

### Örnek Kullanımlar
✅ Örnek 1: Temel kullanım (BAŞARILI)
✅ Örnek 2: Özel threshold (BAŞARILI)
✅ Örnek 3: Tüm olaylar (BAŞARILI)
✅ Örnek 4: Lokasyon karşılaştırması (BAŞARILI)
✅ Örnek 5: Mevsimsel analiz (BAŞARILI)
✅ Örnek 6: JSON export (BAŞARILI)

## 📚 Referanslar

### NASA Veri Setleri
- CCMP: https://podaac.jpl.nasa.gov/dataset/CCMP_MEASURES_ATLAS_L4_OW_L3_5A_MONTHLY_WIND_VECTORS_FLK
- GPCP: https://disc.gsfc.nasa.gov/datasets/GPCPDAY_3.2/summary
- NOAA OI SST: https://psl.noaa.gov/data/gridded/data.noaa.oisst.v2.highres.html
- OSCAR: https://podaac.jpl.nasa.gov/dataset/OSCAR_L4_OC_third-deg

### Teknolojiler
- xarray: http://xarray.pydata.org/
- OPeNDAP: https://www.opendap.org/
- NumPy: https://numpy.org/

## 📄 Lisans

Bu proje NASA açık veri politikasına uygun olarak hazırlanmıştır. Veri kullanımında ilgili veri setlerinin kullanım koşullarına uyulmalıdır.

---

**Oluşturma Tarihi:** 5 Ekim 2025  
**Son Güncelleme:** 5 Ekim 2025  
**Versiyon:** 1.0.0

