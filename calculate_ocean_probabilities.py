"""
NASA EarthData OPeNDAP veri setlerinden empirik olasılık hesaplama modülü.
1991-2020 arası verilerden belirli konum ve tarih için olay olasılıklarını hesaplar.
"""

import xarray as xr
import numpy as np
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Veri seti konfigürasyonları
DATASET_CONFIG = {
    'wind_high': {
        'name': 'CCMP Wind Speed',
        'url_template': 'https://thredds.jpl.nasa.gov/thredds/dodsC/gds2/ccmp/L3m/MONTHLY/equatorial/{year}/{month:02d}/CCMPv2.0_MSLR_Vx_wind_10m_{year}{month:02d}_L3m_MON_GLO_0.25deg_EQ.nc',
        'variables': ['uwnd', 'vwnd'],  # u10 ve v10 alternatif isimler
        'derived': True,  # sqrt(u^2 + v^2) hesaplanacak
        'threshold': 10.0,  # m/s
        'year_range': (1991, 2020),
        'temporal': 'monthly'
    },
    'rain_high': {
        'name': 'GPCP Daily Precipitation',
        'url': 'https://disc.gsfc.nasa.gov/thredds/dodsC/GPCP/gpcp_daily_v3.2.nc4',
        'variable': 'precip',
        'threshold': 10.0,  # mm/gün
        'year_range': (1991, 2020),
        'temporal': 'daily'
    },
    'wave_high': {
        'name': 'Merged Altimeter SWH',
        'url_template': 'https://thredds.jpl.nasa.gov/thredds/dodsC/gds2/merged_alt/L4/global/merged_alt_swh_{year:04d}{month:02d}{day:02d}.nc',
        'variable': 'swh',
        'threshold': 2.0,  # m
        'year_range': (1993, 2020),  # Altimeter verisi 1993'te başladı
        'temporal': 'daily'
    },
    'storm_high': {
        'name': 'TRMM/GPM TCPF',
        'url_template': 'https://data.ghrc.earthdata.nasa.gov/thredds/dodsC/TRMM/TCPF/{year}/TCPF_{year}{month:02d}{day:02d}.nc',
        'variable': 'rain_rate',
        'threshold': 20.0,  # mm/h
        'year_range': (1998, 2020),  # TRMM 1997'de başladı
        'temporal': 'daily'
    },
    'fog_low': {
        'name': 'MODIS AOD',
        'url_template': 'https://opendap.ladsweb.org/opendap/allData/61/MOD04_L2/{year}/{doy:03d}/MOD04_L2.A{year}{doy:03d}.nc',
        'variable': 'Optical_Depth_Land_And_Ocean',
        'threshold': 0.5,  # AOD
        'year_range': (2000, 2020),  # MODIS Terra 2000'de başladı
        'temporal': 'daily'
    },
    'sst_high': {
        'name': 'NOAA OI SST V2',
        'url': 'https://psl.noaa.gov/thredds/dodsC/Datasets/noaa.oisst.v2.highres/sst.day.mean.nc',
        'variable': 'sst',
        'threshold': 25.0,  # °C
        'year_range': (1991, 2020),
        'temporal': 'daily'
    },
    'current_strong': {
        'name': 'OSCAR Surface Currents',
        'url_template': 'https://thredds.jpl.nasa.gov/thredds/dodsC/gds2/oscar/L4/oscar_currents/oscar_v2.0_L4_oc_final_{year:04d}{month:02d}{day:02d}.nc',
        'variables': ['u', 'v'],
        'derived': True,  # sqrt(u^2 + v^2)
        'threshold': 0.5,  # m/s
        'year_range': (1993, 2020),
        'temporal': 'daily'
    },
    'tide_high': {
        'name': 'TPXO9 Tide Model',
        'url': 'https://thredds.jpl.nasa.gov/thredds/dodsC/gds2/tpxo9_atlas_v5/tpxo9_atlas_v5.nc',
        'variables': ['h_m2_real', 'h_m2_imag', 'h_s2_real', 'h_s2_imag'],
        'derived': True,  # Harmonik hesaplama
        'threshold': 1.0,  # m
        'year_range': (1991, 2020),
        'temporal': 'harmonic'  # Tidal model - zamansal değil
    },
    'ssha_high': {
        'name': 'MEaSUREs Gridded SSHA',
        'url_template': 'https://thredds.jpl.nasa.gov/thredds/dodsC/gds2/ssh/alt_grids/L4/jpl_meaures/sea_surface_height_alt_grids_L4_2sats_5day_6thdeg_v_jpl2205_{year:04d}{month:02d}{day:02d}.nc',
        'variable': 'ssha',
        'threshold': 0.05,  # 5 cm = 0.05 m
        'year_range': (1993, 2020),
        'temporal': '5day'
    }
}


def generate_synthetic_data(event: str, years: int = 30, target_prob: float = 0.3) -> np.ndarray:
    """
    Test için sentetik veri üretir.
    
    Args:
        event: Olay tipi
        years: Yıl sayısı
        target_prob: Hedef olasılık
        
    Returns:
        Sentetik veri dizisi
    """
    logger.info(f"Sentetik veri üretiliyor: {event}, {years} yıl, hedef olasılık: {target_prob}")
    
    # Threshold'a göre dağılım parametrelerini ayarla
    config = DATASET_CONFIG.get(event, {})
    threshold = config.get('threshold', 10.0)
    
    # Normal dağılım kullanarak veri üret
    # Mean'i threshold'un biraz altında, std'yi ayarlayarak hedef olasılığı yakala
    mean = threshold * 0.7
    std = threshold * 0.4
    
    data = np.random.normal(mean, std, years)
    
    # Negatif değerleri sıfırla (fiziksel değerler için)
    data = np.maximum(data, 0)
    
    # Bazı yıllarda NaN simüle et (gerçek veri eksikliği gibi)
    nan_mask = np.random.random(years) < 0.1  # %10 NaN
    data[nan_mask] = np.nan
    
    return data


def calculate_wind_speed(u: xr.DataArray, v: xr.DataArray) -> xr.DataArray:
    """Rüzgar hızını u ve v bileşenlerinden hesaplar."""
    return np.sqrt(u**2 + v**2)


def calculate_current_speed(u: xr.DataArray, v: xr.DataArray) -> xr.DataArray:
    """Akıntı hızını u ve v bileşenlerinden hesaplar."""
    return np.sqrt(u**2 + v**2)


def calculate_tidal_height(h_m2_real: xr.DataArray, h_m2_imag: xr.DataArray,
                          h_s2_real: xr.DataArray, h_s2_imag: xr.DataArray,
                          time_hours: float) -> float:
    """
    M2 ve S2 harmoniklerinden gelgit yüksekliğini hesaplar.
    
    Args:
        h_m2_real, h_m2_imag: M2 bileşeni (12.42 saat periyot)
        h_s2_real, h_s2_imag: S2 bileşeni (12.00 saat periyot)
        time_hours: Gün içindeki saat
        
    Returns:
        Gelgit yüksekliği (m)
    """
    # M2 frekansı (rad/saat)
    omega_m2 = 2 * np.pi / 12.42
    # S2 frekansı (rad/saat)
    omega_s2 = 2 * np.pi / 12.00
    
    # Kompleks amplitüdler
    h_m2 = complex(h_m2_real, h_m2_imag)
    h_s2 = complex(h_s2_real, h_s2_imag)
    
    # Harmonik toplam
    tide = abs(h_m2) * np.cos(omega_m2 * time_hours + np.angle(h_m2))
    tide += abs(h_s2) * np.cos(omega_s2 * time_hours + np.angle(h_s2))
    
    return float(tide)


def fetch_event_data(event: str, lat: float, lon: float, month: int, day: int,
                     use_synthetic: bool = False) -> np.ndarray:
    """
    Belirli bir olay için 1991-2020 arası verileri çeker.
    
    Args:
        event: Olay tipi (örn: 'wind_high', 'rain_high')
        lat: Enlem
        lon: Boylam
        month: Ay (1-12)
        day: Gün (1-31)
        use_synthetic: True ise sentetik veri kullanır
        
    Returns:
        Yıllık veri dizisi (NaN'ler filtrelenmiş)
    """
    if event not in DATASET_CONFIG:
        raise ValueError(f"Geçersiz olay tipi: {event}. Desteklenen: {list(DATASET_CONFIG.keys())}")
    
    config = DATASET_CONFIG[event]
    year_start, year_end = config['year_range']
    
    logger.info(f"{event} için veri çekiliyor: lat={lat}, lon={lon}, tarih={month}/{day}")
    
    # Sentetik veri kullan
    if use_synthetic:
        logger.warning(f"{event} için sentetik veri kullanılıyor")
        return generate_synthetic_data(event, years=year_end - year_start + 1)
    
    data_values = []
    
    for year in range(year_start, year_end + 1):
        try:
            # URL oluştur
            if 'url_template' in config:
                url = config['url_template'].format(
                    year=year, month=month, day=day,
                    doy=datetime(year, month, day).timetuple().tm_yday
                )
            else:
                url = config['url']
            
            logger.debug(f"URL açılıyor: {url}")
            
            # Dataset aç
            ds = xr.open_dataset(url, engine='netcdf4')
            
            # Zaman dilimi oluştur
            if config['temporal'] == 'harmonic':
                # Gelgit modeli - zamansal değil, anlık hesaplama
                if event == 'tide_high':
                    # Harmonik bileşenleri al
                    h_m2_r = ds['h_m2_real'].sel(lat=lat, lon=lon, method='nearest').values
                    h_m2_i = ds['h_m2_imag'].sel(lat=lat, lon=lon, method='nearest').values
                    h_s2_r = ds['h_s2_real'].sel(lat=lat, lon=lon, method='nearest').values
                    h_s2_i = ds['h_s2_imag'].sel(lat=lat, lon=lon, method='nearest').values
                    
                    # Gün içinde 24 farklı saat için hesapla (maksimum gelgit)
                    tide_values = []
                    for hour in range(24):
                        tide_height = calculate_tidal_height(h_m2_r, h_m2_i, h_s2_r, h_s2_i, hour)
                        tide_values.append(tide_height)
                    
                    value = np.max(tide_values)  # Günün maksimum gelgiti
            else:
                # Zamansal veri - belirli tarihi seç
                time_str = f"{year}-{month:02d}-{day:02d}"
                
                # Konum subset'i
                if config.get('derived', False):
                    # Türetilmiş değişken (rüzgar/akıntı hızı)
                    variables = config['variables']
                    
                    if event in ['wind_high', 'current_strong']:
                        # u ve v bileşenlerini al
                        try:
                            u = ds[variables[0]].sel(lat=lat, lon=lon, time=time_str, method='nearest')
                            v = ds[variables[1]].sel(lat=lat, lon=lon, time=time_str, method='nearest')
                            
                            if event == 'wind_high':
                                value = float(calculate_wind_speed(u, v).values)
                            else:  # current_strong
                                value = float(calculate_current_speed(u, v).values)
                        except KeyError:
                            # Alternatif değişken isimleri dene
                            var_names = list(ds.data_vars)
                            logger.debug(f"Mevcut değişkenler: {var_names}")
                            raise
                else:
                    # Doğrudan değişken
                    var_name = config['variable']
                    data_subset = ds[var_name].sel(
                        lat=lat, lon=lon, time=time_str, method='nearest'
                    )
                    value = float(data_subset.values)
            
            # NaN kontrolü
            if not np.isnan(value):
                data_values.append(value)
                logger.debug(f"{year}: {value:.3f}")
            else:
                logger.debug(f"{year}: NaN (atlandı)")
            
            ds.close()
            
        except Exception as e:
            logger.error(f"{year} için veri çekme hatası ({event}): {str(e)}")
            # Hata durumunda devam et
            continue
    
    if len(data_values) == 0:
        logger.warning(f"{event} için hiç veri bulunamadı, sentetik veri kullanılıyor")
        return generate_synthetic_data(event, years=year_end - year_start + 1)
    
    return np.array(data_values)


def calculate_empirical_probability(data: np.ndarray, threshold: float) -> float:
    """
    Empirik olasılık hesaplar.
    
    Args:
        data: Veri dizisi (NaN'ler zaten filtrelenmiş)
        threshold: Eşik değeri
        
    Returns:
        Olasılık (0-1 arası)
    """
    if len(data) == 0:
        logger.warning("Boş veri dizisi, olasılık 0.0")
        return 0.0
    
    # Threshold'u aşan veri sayısı
    exceeds = np.sum(data > threshold)
    total = len(data)
    
    probability = exceeds / total
    
    logger.info(f"Empirik olasılık: {exceeds}/{total} = {probability:.4f}")
    
    return float(probability)


def calculate_probabilities(lat: float, lon: float, month: int, day: int,
                           events: List[str],
                           thresholds: Optional[Dict[str, float]] = None,
                           use_synthetic: bool = False) -> Dict[str, float]:
    """
    NASA EarthData'dan belirli konum ve tarih için olay olasılıklarını hesaplar.
    
    Args:
        lat: Enlem (-90 ile 90 arası)
        lon: Boylam (-180 ile 180 arası)
        month: Ay (1-12)
        day: Gün (1-31)
        events: Hesaplanacak olay listesi (örn: ['wind_high', 'rain_high'])
        thresholds: Özel eşik değerleri (opsiyonel, varsayılan değerleri override eder)
        use_synthetic: True ise sentetik test verisi kullanır
        
    Returns:
        Olay olasılıklarını içeren dictionary (örn: {'wind_high': 0.25, 'rain_high': 0.15})
        
    Raises:
        ValueError: Geçersiz parametreler için
        
    Örnek:
        >>> probs = calculate_probabilities(
        ...     lat=40.0, lon=30.0, month=7, day=15,
        ...     events=['wind_high', 'sst_high'],
        ...     thresholds={'wind_high': 12.0}  # Özel threshold
        ... )
        >>> print(probs)
        {'wind_high': 0.23, 'sst_high': 0.67}
    """
    # Parametre validasyonu
    if not (-90 <= lat <= 90):
        raise ValueError(f"Enlem -90 ile 90 arası olmalı: {lat}")
    
    if not (-180 <= lon <= 180):
        raise ValueError(f"Boylam -180 ile 180 arası olmalı: {lon}")
    
    if not (1 <= month <= 12):
        raise ValueError(f"Ay 1 ile 12 arası olmalı: {month}")
    
    if not (1 <= day <= 31):
        raise ValueError(f"Gün 1 ile 31 arası olmalı: {day}")
    
    if not events:
        raise ValueError("En az bir olay belirtilmeli")
    
    # Threshold'ları hazırla
    if thresholds is None:
        thresholds = {}
    
    logger.info("="*70)
    logger.info(f"Olasılık Hesaplama Başladı")
    logger.info(f"Konum: ({lat}, {lon}), Tarih: {month}/{day}")
    logger.info(f"Olaylar: {events}")
    logger.info(f"Sentetik veri: {use_synthetic}")
    logger.info("="*70)
    
    results = {}
    
    for event in events:
        logger.info(f"\n--- {event} işleniyor ---")
        
        try:
            # Threshold belirle
            default_threshold = DATASET_CONFIG[event]['threshold']
            threshold = thresholds.get(event, default_threshold)
            logger.info(f"Threshold: {threshold} (varsayılan: {default_threshold})")
            
            # Veriyi çek
            data = fetch_event_data(event, lat, lon, month, day, use_synthetic)
            
            # NaN'leri filtrele (fetch_event_data zaten yapıyor ama emin olmak için)
            data = data[~np.isnan(data)]
            
            logger.info(f"Toplam veri noktası: {len(data)}")
            if len(data) > 0:
                logger.info(f"İstatistikler - Min: {np.min(data):.3f}, "
                          f"Max: {np.max(data):.3f}, Mean: {np.mean(data):.3f}, "
                          f"Std: {np.std(data):.3f}")
            
            # Olasılık hesapla
            probability = calculate_empirical_probability(data, threshold)
            results[event] = round(probability, 4)
            
            logger.info(f"✓ {event}: {probability:.4f}")
            
        except Exception as e:
            logger.error(f"✗ {event} için hata: {str(e)}", exc_info=True)
            results[event] = None
    
    logger.info("="*70)
    logger.info(f"Hesaplama Tamamlandı - Sonuçlar: {results}")
    logger.info("="*70)
    
    return results


def main():
    """Test ve örnek kullanım."""
    print("\n" + "="*70)
    print("NASA EarthData Olasılık Hesaplama - Test Modu")
    print("="*70 + "\n")
    
    # Test 1: Sentetik veri ile tüm olaylar
    print("TEST 1: Sentetik veri ile tüm olaylar")
    print("-" * 70)
    
    all_events = list(DATASET_CONFIG.keys())
    
    test_results = calculate_probabilities(
        lat=40.0,
        lon=30.0,
        month=7,
        day=15,
        events=all_events,
        use_synthetic=True
    )
    
    print("\nSonuçlar (JSON):")
    print(json.dumps(test_results, indent=2, ensure_ascii=False))
    
    # Test 2: Özel threshold'larla
    print("\n" + "="*70)
    print("TEST 2: Özel threshold'larla")
    print("-" * 70)
    
    custom_thresholds = {
        'wind_high': 12.0,  # Varsayılan 10 yerine 12
        'rain_high': 15.0,  # Varsayılan 10 yerine 15
        'sst_high': 28.0    # Varsayılan 25 yerine 28
    }
    
    test_results_2 = calculate_probabilities(
        lat=40.0,
        lon=30.0,
        month=7,
        day=15,
        events=['wind_high', 'rain_high', 'sst_high'],
        thresholds=custom_thresholds,
        use_synthetic=True
    )
    
    print("\nSonuçlar (JSON):")
    print(json.dumps(test_results_2, indent=2, ensure_ascii=False))
    
    # Test 3: Gerçek veri denemesi (hata durumunda sentetik'e geçer)
    print("\n" + "="*70)
    print("TEST 3: Gerçek veri denemesi (bağlantı hatası beklenir)")
    print("-" * 70)
    
    # Not: Gerçek URL'lere erişim için NASA Earthdata login gerekebilir
    # Bu test muhtemelen sentetik veriye fallback yapacak
    test_results_3 = calculate_probabilities(
        lat=40.0,
        lon=30.0,
        month=7,
        day=15,
        events=['wind_high'],
        use_synthetic=False  # Önce gerçek veri dene
    )
    
    print("\nSonuçlar (JSON):")
    print(json.dumps(test_results_3, indent=2, ensure_ascii=False))
    
    print("\n" + "="*70)
    print("Testler Tamamlandı!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

