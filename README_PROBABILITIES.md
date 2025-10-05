# NASA EarthData Olasılık Hesaplama Modülü

Bu modül, NASA EarthData OPeNDAP servislerinden 1991-2020 arası okyanus ve atmosfer verilerini kullanarak belirli bir konum ve tarih için empirik olay olasılıklarını hesaplar.

## Özellikler

- **9 Farklı Veri Seti Desteği:**
  - `wind_high`: Yüksek rüzgar hızı (CCMP V2.0)
  - `rain_high`: Yoğun yağış (GPCP Daily V3.2)
  - `wave_high`: Yüksek dalga (Merged Altimeter SWH)
  - `storm_high`: Fırtına/kasırga (TRMM/GPM TCPF)
  - `fog_low`: Düşük görüş/sis (MODIS AOD)
  - `sst_high`: Yüksek deniz suyu sıcaklığı (NOAA OI SST)
  - `current_strong`: Güçlü akıntı (OSCAR V2.0)
  - `tide_high`: Yüksek gelgit (TPXO9)
  - `ssha_high`: Yüksek deniz seviyesi anomalisi (MEaSUREs)

- **Empirik Olasılık Hesaplama:** 30 yıllık geçmiş veriden threshold'u aşan olay frekansını hesaplar
- **Konum ve Tarih Bazlı:** Belirli enlem/boylam ve ay/gün için veri çeker
- **NaN Filtreleme:** Eksik verileri otomatik filtreler
- **Hata Yönetimi:** Kapsamlı logging ve try-except blokları
- **Sentetik Test Verisi:** Gerçek veriye erişim olmadan test yapma imkanı
- **Özelleştirilebilir Threshold:** Her olay için özel eşik değeri belirleme

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

### Temel Kullanım

```python
from calculate_ocean_probabilities import calculate_probabilities

# İstanbul (40°N, 29°E) için 15 Temmuz'da rüzgar ve dalga olasılıkları
results = calculate_probabilities(
    lat=40.0,
    lon=29.0,
    month=7,
    day=15,
    events=['wind_high', 'wave_high']
)

print(results)
# Çıktı: {'wind_high': 0.25, 'wave_high': 0.18}
```

### Özel Threshold ile Kullanım

```python
# Özel eşik değerleri ile
custom_thresholds = {
    'wind_high': 12.0,  # 12 m/s üzeri
    'sst_high': 28.0    # 28°C üzeri
}

results = calculate_probabilities(
    lat=40.0,
    lon=29.0,
    month=7,
    day=15,
    events=['wind_high', 'sst_high'],
    thresholds=custom_thresholds
)
```

### Sentetik Veri ile Test

```python
# Gerçek veriye erişim olmadan test
results = calculate_probabilities(
    lat=40.0,
    lon=29.0,
    month=7,
    day=15,
    events=['wind_high', 'rain_high'],
    use_synthetic=True
)
```

### Tüm Olayları Hesaplama

```python
from calculate_ocean_probabilities import DATASET_CONFIG

# Tüm mevcut olaylar için
all_events = list(DATASET_CONFIG.keys())

results = calculate_probabilities(
    lat=40.0,
    lon=29.0,
    month=7,
    day=15,
    events=all_events,
    use_synthetic=True  # Test için
)
```

## Fonksiyon İmzası

```python
def calculate_probabilities(
    lat: float,              # Enlem (-90 ile 90)
    lon: float,              # Boylam (-180 ile 180)
    month: int,              # Ay (1-12)
    day: int,                # Gün (1-31)
    events: List[str],       # Hesaplanacak olaylar
    thresholds: Optional[Dict[str, float]] = None,  # Özel threshold'lar
    use_synthetic: bool = False  # Sentetik veri kullan
) -> Dict[str, float]:
    """
    Returns:
        Dictionary: {'event_name': probability, ...}
        
    Örnek:
        {'wind_high': 0.23, 'rain_high': 0.15, 'wave_high': 0.18}
    """
```

## Veri Setleri ve Varsayılan Threshold'lar

| Olay | Veri Seti | Değişken | Threshold | Birim |
|------|-----------|----------|-----------|-------|
| `wind_high` | CCMP V2.0 | sqrt(u² + v²) | 10 | m/s |
| `rain_high` | GPCP V3.2 | precip | 10 | mm/gün |
| `wave_high` | Merged Alt SWH | swh | 2 | m |
| `storm_high` | TRMM/GPM TCPF | rain_rate | 20 | mm/h |
| `fog_low` | MODIS AOD | optical_depth | 0.5 | - |
| `sst_high` | NOAA OI SST | sst | 25 | °C |
| `current_strong` | OSCAR V2.0 | sqrt(u² + v²) | 0.5 | m/s |
| `tide_high` | TPXO9 | harmonics | 1.0 | m |
| `ssha_high` | MEaSUREs | ssha | 0.05 | m |

## Test Çalıştırma

```bash
python calculate_ocean_probabilities.py
```

Bu komut 3 farklı test senaryosu çalıştırır:
1. Tüm olaylar için sentetik veri testi
2. Özel threshold'larla test
3. Gerçek veri çekme denemesi (fallback sentetik)

## Önemli Notlar

1. **NASA Earthdata Kimlik Doğrulama:** Gerçek verilere erişim için NASA Earthdata hesabı ve `.netrc` yapılandırması gerekebilir.

2. **Veri Kapsamı:** Her veri setinin başlangıç yılı farklıdır:
   - 1991: CCMP, GPCP, NOAA SST
   - 1993: Altimeter, OSCAR, MEaSUREs
   - 1998: TRMM
   - 2000: MODIS

3. **Performans:** Her olay için 30 yıllık veri çekildiğinden işlem uzun sürebilir. İlk çalıştırmada cache oluşturulur.

4. **Hata Yönetimi:** URL'lere erişim başarısız olursa otomatik olarak sentetik veriye geçer ve uyarı verir.

## Logging

Detaylı log çıktısı için:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Örnek Çıktı

```json
{
  "wind_high": 0.2333,
  "rain_high": 0.1667,
  "wave_high": 0.1852,
  "storm_high": 0.0870,
  "fog_low": 0.1200,
  "sst_high": 0.6667,
  "current_strong": 0.2222,
  "tide_high": 0.2000,
  "ssha_high": 0.1481
}
```

## Lisans

Bu modül NASA açık veri politikasına uygun olarak hazırlanmıştır. Veri kullanımında ilgili veri setlerinin kullanım koşullarına uyulmalıdır.

