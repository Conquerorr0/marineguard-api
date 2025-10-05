"""
NASA EarthData Olasılık Hesaplama - Örnek Kullanım
"""

from calculate_ocean_probabilities import calculate_probabilities, DATASET_CONFIG
import json


def example_1_basic():
    """Temel kullanım: İstanbul için Temmuz ayı"""
    print("\n" + "="*70)
    print("ÖRNEK 1: Temel Kullanım - İstanbul (40°N, 29°E) - 15 Temmuz")
    print("="*70)
    
    results = calculate_probabilities(
        lat=40.0,
        lon=29.0,
        month=7,
        day=15,
        events=['wind_high', 'wave_high', 'sst_high'],
        use_synthetic=True  # Test için sentetik veri
    )
    
    print("\n[SONUCLAR]")
    for event, prob in results.items():
        print(f"  - {event}: %{prob*100:.1f} olasilik")
    
    return results


def example_2_custom_thresholds():
    """Özel threshold'larla kullanım"""
    print("\n" + "="*70)
    print("ÖRNEK 2: Özel Threshold'lar - Antalya (36.9°N, 30.7°E) - 1 Ağustos")
    print("="*70)
    
    # Daha yüksek rüzgar ve SST threshold'ları
    custom_thresholds = {
        'wind_high': 15.0,   # 15 m/s üzeri (varsayılan: 10)
        'sst_high': 28.0,    # 28°C üzeri (varsayılan: 25)
        'wave_high': 3.0     # 3 m üzeri (varsayılan: 2)
    }
    
    print("\n[OZEL THRESHOLDLAR]")
    for event, threshold in custom_thresholds.items():
        default = DATASET_CONFIG[event]['threshold']
        print(f"  - {event}: {threshold} (varsayilan: {default})")
    
    results = calculate_probabilities(
        lat=36.9,
        lon=30.7,
        month=8,
        day=1,
        events=list(custom_thresholds.keys()),
        thresholds=custom_thresholds,
        use_synthetic=True
    )
    
    print("\n[SONUCLAR]")
    for event, prob in results.items():
        if prob is not None:
            print(f"  - {event}: %{prob*100:.1f} olasilik")
        else:
            print(f"  - {event}: HATA")
    
    return results


def example_3_all_events():
    """Tüm olaylar için hesaplama"""
    print("\n" + "="*70)
    print("ÖRNEK 3: Tüm Olaylar - İzmir (38.4°N, 27.1°E) - 20 Haziran")
    print("="*70)
    
    all_events = list(DATASET_CONFIG.keys())
    
    print(f"\n[TOPLAM {len(all_events)} OLAY KONTROL EDILIYOR]")
    
    results = calculate_probabilities(
        lat=38.4,
        lon=27.1,
        month=6,
        day=20,
        events=all_events,
        use_synthetic=True
    )
    
    print("\n[SONUCLAR - Yuksekten Dusuge]")
    sorted_results = sorted(results.items(), key=lambda x: x[1] if x[1] else 0, reverse=True)
    
    for i, (event, prob) in enumerate(sorted_results, 1):
        if prob is not None:
            bar = "#" * int(prob * 50)  # Gorsel bar
            print(f"  {i:2d}. {event:20s}: %{prob*100:5.1f} {bar}")
    
    return results


def example_4_comparison():
    """Farklı lokasyonları karşılaştır"""
    print("\n" + "="*70)
    print("ÖRNEK 4: Lokasyon Karşılaştırması - Temmuz Ayı")
    print("="*70)
    
    locations = {
        'İstanbul': (41.0, 29.0),
        'İzmir': (38.4, 27.1),
        'Antalya': (36.9, 30.7),
        'Trabzon': (41.0, 39.7)
    }
    
    events_to_check = ['wind_high', 'wave_high', 'sst_high']
    
    print(f"\n[{len(locations)} FARKLI LOKASYON KARSILASTIRILIYOR]")
    print(f"[Tarih: 15 Temmuz]")
    print(f"[Olaylar: {', '.join(events_to_check)}]\n")
    
    comparison_results = {}
    
    for city, (lat, lon) in locations.items():
        results = calculate_probabilities(
            lat=lat,
            lon=lon,
            month=7,
            day=15,
            events=events_to_check,
            use_synthetic=True
        )
        comparison_results[city] = results
    
    # Her olay icin karsilastirma tablosu
    for event in events_to_check:
        print(f"\n[{event.upper()}]")
        city_probs = [(city, results[event]) for city, results in comparison_results.items()]
        city_probs.sort(key=lambda x: x[1] if x[1] else 0, reverse=True)
        
        for city, prob in city_probs:
            if prob is not None:
                bar = "#" * int(prob * 30)
                print(f"  {city:15s}: %{prob*100:5.1f} {bar}")
    
    return comparison_results


def example_5_seasonal():
    """Mevsimsel karşılaştırma"""
    print("\n" + "="*70)
    print("ÖRNEK 5: Mevsimsel Analiz - İstanbul")
    print("="*70)
    
    seasons = {
        'Kış (15 Ocak)': (1, 15),
        'İlkbahar (15 Nisan)': (4, 15),
        'Yaz (15 Temmuz)': (7, 15),
        'Sonbahar (15 Ekim)': (10, 15)
    }
    
    event_to_check = 'wind_high'
    
    print(f"\n[Mevsimsel {event_to_check} analizi yapiliyor...]")
    print(f"[Konum: Istanbul (41N, 29E)]\n")
    
    seasonal_results = {}
    
    for season, (month, day) in seasons.items():
        result = calculate_probabilities(
            lat=41.0,
            lon=29.0,
            month=month,
            day=day,
            events=[event_to_check],
            use_synthetic=True
        )
        seasonal_results[season] = result[event_to_check]
    
    print("\n[MEVSIMSEL OLASILIKLAR]")
    for season, prob in seasonal_results.items():
        if prob is not None:
            bar = "#" * int(prob * 40)
            print(f"  {season:25s}: %{prob*100:5.1f} {bar}")
    
    return seasonal_results


def example_6_json_export():
    """JSON formatında sonuç kaydetme"""
    print("\n" + "="*70)
    print("ÖRNEK 6: JSON Export")
    print("="*70)
    
    # Birden fazla lokasyon ve olay için veri topla
    data = {
        'metadata': {
            'calculation_date': '2025-10-05',
            'description': 'NASA EarthData olasılık analizi',
            'period': '1991-2020',
            'threshold_type': 'default'
        },
        'locations': []
    }
    
    locations = [
        {'name': 'İstanbul', 'lat': 41.0, 'lon': 29.0},
        {'name': 'İzmir', 'lat': 38.4, 'lon': 27.1}
    ]
    
    events = ['wind_high', 'wave_high', 'sst_high']
    
    print("\n[JSON verisi hazirlaniyor...]\n")
    
    for loc in locations:
        results = calculate_probabilities(
            lat=loc['lat'],
            lon=loc['lon'],
            month=7,
            day=15,
            events=events,
            use_synthetic=True
        )
        
        loc_data = {
            'name': loc['name'],
            'coordinates': {'lat': loc['lat'], 'lon': loc['lon']},
            'date': {'month': 7, 'day': 15},
            'probabilities': results
        }
        
        data['locations'].append(loc_data)
    
    # JSON olarak kaydet
    json_output = json.dumps(data, indent=2, ensure_ascii=False)
    
    # Dosyaya yaz
    with open('probability_results.json', 'w', encoding='utf-8') as f:
        f.write(json_output)
    
    print("[OK] Sonuclar 'probability_results.json' dosyasina kaydedildi\n")
    print("[JSON ICERIGI]")
    print(json_output)
    
    return data


def main():
    """Tüm örnekleri çalıştır"""
    print("\n" + "="*70)
    print("NASA EARTHDATA OLASILIK HESAPLAMA - ORNEK KULLANIMLAR")
    print("="*70)
    
    # Tüm örnekleri çalıştır
    example_1_basic()
    example_2_custom_thresholds()
    example_3_all_events()
    example_4_comparison()
    example_5_seasonal()
    example_6_json_export()
    
    print("\n" + "="*70)
    print("[OK] Tum ornekler basariyla tamamlandi!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

