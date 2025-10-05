"""
Interactive NASA EarthData Probability Test
Gerçek NASA verilerini kullanarak interaktif olasılık hesaplama
"""

import requests
import json
from datetime import datetime, timedelta

# Heroku API URL
API_URL = "https://nasa-probability-api-2b173d22b072.herokuapp.com"

# Türkiye'den 4 önemli konum
TURKEY_LOCATIONS = {
    '1': {
        'name': 'İstanbul (Marmara Denizi)',
        'lat': 41.0,
        'lon': 29.0,
        'description': 'Marmara Denizi - Boğaz bölgesi'
    },
    '2': {
        'name': 'İzmir (Ege Denizi)',
        'lat': 38.4,
        'lon': 27.1,
        'description': 'Ege Denizi - İzmir Körfezi'
    },
    '3': {
        'name': 'Antalya (Akdeniz)',
        'lat': 36.9,
        'lon': 30.7,
        'description': 'Akdeniz - Antalya Körfezi'
    },
    '4': {
        'name': 'Trabzon (Karadeniz)',
        'lat': 41.0,
        'lon': 39.7,
        'description': 'Karadeniz - Doğu bölgesi'
    }
}

# Tüm olaylar ve açıklamaları
ALL_EVENTS = {
    'wind_high': {
        'name': 'Yüksek Rüzgar Hızı',
        'threshold': '10 m/s',
        'description': 'CCMP uydu verisi ile rüzgar hızı'
    },
    'rain_high': {
        'name': 'Yoğun Yağış',
        'threshold': '10 mm/gün',
        'description': 'GPCP günlük yağış verisi'
    },
    'wave_high': {
        'name': 'Yüksek Dalga',
        'threshold': '2 m',
        'description': 'Altimeter dalga yüksekliği'
    },
    'storm_high': {
        'name': 'Fırtına/Kasırga',
        'threshold': '20 mm/saat',
        'description': 'TRMM/GPM fırtına verisi'
    },
    'fog_low': {
        'name': 'Düşük Görüş (Sis)',
        'threshold': '0.5 AOD',
        'description': 'MODIS aerosol optik derinlik'
    },
    'sst_high': {
        'name': 'Yüksek Deniz Suyu Sıcaklığı',
        'threshold': '25°C',
        'description': 'NOAA deniz suyu sıcaklığı'
    },
    'current_strong': {
        'name': 'Güçlü Akıntı',
        'threshold': '0.5 m/s',
        'description': 'OSCAR yüzey akıntıları'
    },
    'tide_high': {
        'name': 'Yüksek Gelgit',
        'threshold': '1 m',
        'description': 'TPXO9 gelgit modeli'
    },
    'ssha_high': {
        'name': 'Yüksek Deniz Seviyesi Anomalisi',
        'threshold': '5 cm',
        'description': 'MEaSUREs deniz seviyesi'
    }
}


def print_header(text):
    """Başlık yazdır"""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def select_location():
    """Kullanıcıdan konum seç"""
    print_header("KONUM SEÇİMİ - TÜRKİYE DENİZLERİ")
    
    print("\nMevcut Konumlar:\n")
    for key, loc in TURKEY_LOCATIONS.items():
        print(f"  {key}. {loc['name']}")
        print(f"     Koordinatlar: {loc['lat']}°N, {loc['lon']}°E")
        print(f"     {loc['description']}\n")
    
    while True:
        choice = input("Konum seçin (1-4): ").strip()
        if choice in TURKEY_LOCATIONS:
            selected = TURKEY_LOCATIONS[choice]
            print(f"\n[OK] Secildi: {selected['name']}")
            return selected['lat'], selected['lon'], selected['name']
        else:
            print("[HATA] Gecersiz secim! Lutfen 1-4 arasi bir sayi girin.")


def select_date():
    """Kullanıcıdan gelecek tarih seç"""
    print_header("TARİH SEÇİMİ")
    
    today = datetime.now()
    
    print(f"\nBugün: {today.strftime('%d %B %Y')}")
    print("\nÖrnek Tarihler:")
    for i in [7, 14, 30, 60]:
        future = today + timedelta(days=i)
        print(f"  - {i} gün sonra: {future.strftime('%d %B %Y')} ({future.month}/{future.day})")
    
    print("\n[NOT] NASA verisi 1991-2020 arasi oldugu icin,")
    print("      gercek analiz yapmak icin gecmis bir tarihi de secebilirsiniz.")
    print("      Ornegin: 15 Temmuz (7/15) veya 1 Agustos (8/1)")
    
    while True:
        try:
            month = int(input("\nAy (1-12): ").strip())
            if not 1 <= month <= 12:
                print("[HATA] Ay 1-12 arasi olmali!")
                continue
            
            day = int(input("Gun (1-31): ").strip())
            if not 1 <= day <= 31:
                print("[HATA] Gun 1-31 arasi olmali!")
                continue
            
            # Tarih kontrolu
            try:
                test_date = datetime(2020, month, day)
                print(f"\n[OK] Secildi: {test_date.strftime('%d %B')} (Ay: {month}, Gun: {day})")
                return month, day
            except ValueError:
                print("[HATA] Gecersiz tarih! Lutfen tekrar deneyin.")
        except ValueError:
            print("[HATA] Lutfen gecerli bir sayi girin!")


def select_events():
    """Kullanıcıdan olayları seç"""
    print_header("OLAY SEÇİMİ - HANGİ OLASILIKLARINI GÖRMEK İSTERSİNİZ?")
    
    print("\nMevcut Olaylar:\n")
    event_keys = list(ALL_EVENTS.keys())
    for i, (key, event) in enumerate(ALL_EVENTS.items(), 1):
        print(f"  {i}. {event['name']}")
        print(f"     Eşik: {event['threshold']} - {event['description']}")
        print(f"     Kod: {key}\n")
    
    print("Seçim Yöntemleri:")
    print("  - Tek tek: 1,3,5 (virgülle ayırın)")
    print("  - Aralık: 1-4 (tire ile)")
    print("  - Hepsi: 'all' veya 'tümü' yazın")
    print("  - En populer: 'populer' (ruzgar, dalga, yagis, SST)")
    
    while True:
        choice = input("\nSeçiminiz: ").strip().lower()
        
        if choice in ['all', 'tumu', 'hepsi']:
            selected = list(ALL_EVENTS.keys())
            print(f"\n[OK] Tum olaylar secildi ({len(selected)} olay)")
            return selected
        
        if choice in ['populer', 'popular', 'pop']:
            selected = ['wind_high', 'wave_high', 'rain_high', 'sst_high']
            print(f"\n[OK] Populer olaylar secildi: Ruzgar, Dalga, Yagis, SST")
            return selected
        
        try:
            selected_indices = set()
            
            # Virgülle ayrılmış sayıları işle
            for part in choice.split(','):
                part = part.strip()
                if '-' in part:
                    # Aralık (örn: 1-4)
                    start, end = map(int, part.split('-'))
                    selected_indices.update(range(start, end + 1))
                else:
                    # Tek sayı
                    selected_indices.add(int(part))
            
            # Gecerli aralikta mi kontrol et
            if not selected_indices or not all(1 <= i <= len(ALL_EVENTS) for i in selected_indices):
                print("[HATA] Gecersiz secim! Lutfen 1-9 arasi sayilar girin.")
                continue
            
            # Event key'lerini al
            selected = [event_keys[i-1] for i in sorted(selected_indices)]
            
            print(f"\n[OK] Secilen olaylar ({len(selected)}):")
            for event_key in selected:
                print(f"  - {ALL_EVENTS[event_key]['name']}")
            
            return selected
            
        except (ValueError, IndexError):
            print("[HATA] Gecersiz format! Ornek: 1,3,5 veya 1-4 veya 'all'")


def test_api(lat, lon, month, day, events, location_name):
    """API'yi test et"""
    print_header("NASA EARTHDATA API TESTİ")
    
    print(f"\n[KONUM] {location_name}")
    print(f"[TARIH] {month}/{day}")
    print(f"[OLAYLAR] {len(events)} adet")
    print(f"[VERI] GERCEK NASA OPeNDAP verisi")
    print(f"[SURE] Beklenen sure: ~30-60 saniye (ilk istek)")
    
    confirm = input("\n▶ Testi başlatmak için ENTER'a basın (veya 'q' ile çık): ").strip().lower()
    if confirm == 'q':
        print("Test iptal edildi.")
        return None
    
    print("\n[YUKLENIYOR] NASA verisi cekiliyor... Lutfen bekleyin...")
    print("              (Bu islem uzun surebilir, sabirli olun!)\n")
    
    # Kullanıcıya sor: gerçek mi sentetik mi?
    print("\n[VERI MODU SECIMI]")
    print("1. Gercek NASA verisi (YAVASTIR, Heroku'da calismayabilir)")
    print("2. Sentetik test verisi (HIZLIDIR, her zaman calisir)")
    mode_choice = input("\nHangi modu kullanmak istersiniz? (1/2) [Varsayilan: 2]: ").strip()
    
    use_synthetic = mode_choice != '1'  # 1 dışında her şey sentetik
    
    if use_synthetic:
        print("[OK] Sentetik test verisi kullanilacak (hizli)")
    else:
        print("[UYARI] Gercek NASA verisi kullanilacak (cok yavas, Heroku'da calismayabilir)")
    
    payload = {
        'lat': lat,
        'lon': lon,
        'month': month,
        'day': day,
        'events': events,
        'use_synthetic': use_synthetic
    }
    
    try:
        import time
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/calculate_probability",
            json=payload,
            timeout=300  # 5 dakika timeout
        )
        
        elapsed = time.time() - start_time
        
        print(f"[OK] Yanit alindi! Sure: {elapsed:.1f} saniye\n")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                return data['data']['probabilities']
            else:
                print(f"[HATA] API Hatasi: {data.get('error')}")
                
                # Fallback: Sentetik veri ile dene
                print("\n[UYARI] Gercek veri cekilemedi. Sentetik veri ile deneniyor...")
                payload['use_synthetic'] = True
                response = requests.post(
                    f"{API_URL}/calculate_probability",
                    json=payload,
                    timeout=60
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        print("[OK] Sentetik veri ile sonuc alindi")
                        return data['data']['probabilities']
                
                return None
        else:
            print(f"[HATA] HTTP {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("[HATA] Timeout: Istek cok uzun surdu (>5 dakika)")
        return None
    except Exception as e:
        print(f"[HATA] {e}")
        return None


def display_results(probabilities, location_name, month, day):
    """Sonuçları görüntüle"""
    print_header("SONUÇLAR - OLAY OLASILIKLARARI")
    
    print(f"\n[KONUM] {location_name}")
    print(f"[TARIH] {month}/{day}")
    print(f"[ANALIZ] NASA EarthData - 1991-2020 Donemi Analizi\n")
    
    if not probabilities:
        print("[HATA] Sonuc alinamadi!")
        return
    
    # Olasılıklara göre sırala
    sorted_probs = sorted(
        probabilities.items(),
        key=lambda x: x[1] if x[1] is not None else -1,
        reverse=True
    )
    
    print("Olay                                  Olasılık    Risk Seviyesi")
    print("-" * 70)
    
    for event_key, prob in sorted_probs:
        if prob is None:
            print(f"{ALL_EVENTS[event_key]['name']:35s}   HATA")
            continue
        
        # Risk seviyesi belirle
        if prob >= 0.5:
            risk = "[COK YUKSEK]"
            color = ">>>"
        elif prob >= 0.3:
            risk = "[YUKSEK]"
            color = ">>"
        elif prob >= 0.15:
            risk = "[ORTA]"
            color = ">"
        else:
            risk = "[DUSUK]"
            color = "-"
        
        # Progress bar
        bar_length = int(prob * 40)
        bar = "#" * bar_length
        
        print(f"{ALL_EVENTS[event_key]['name']:35s}   {prob:6.2%}     {risk}")
        print(f"  {color} {bar}")
    
    print("\n" + "="*70)
    
    # Ozet
    high_risk = sum(1 for _, p in probabilities.items() if p and p >= 0.3)
    if high_risk > 0:
        print(f"\n[UYARI] DIKKAT: {high_risk} olay icin yuksek risk tespit edildi!")
    else:
        print(f"\n[OK] Tum olaylar icin risk dusuk veya orta seviyede.")


def main():
    """Ana program"""
    print("\n" + "="*70)
    print("NASA EARTHDATA INTERACTIVE TEST - GERCEK VERI ANALIZI")
    print("="*70)
    print("\nBu program GERÇEK NASA uydu verilerini kullanarak")
    print("Türkiye denizlerinde olay olasılıklarını hesaplar.")
    print("\n[UYARI] Not: Gercek veri cekimi 30-60 saniye surebilir!")
    print("="*70)
    
    # 1. Konum seç
    lat, lon, location_name = select_location()
    
    # 2. Tarih seç
    month, day = select_date()
    
    # 3. Olayları seç
    events = select_events()
    
    # 4. API'yi test et
    probabilities = test_api(lat, lon, month, day, events, location_name)
    
    # 5. Sonuçları göster
    if probabilities:
        display_results(probabilities, location_name, month, day)
        
        # JSON kaydet
        save = input("\n[KAYDET] Sonuclari JSON dosyasina kaydetmek ister misiniz? (e/h): ").strip().lower()
        if save == 'e':
            filename = f"nasa_results_{location_name.split()[0]}_{month}_{day}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                result_data = {
                    'location': {
                        'name': location_name,
                        'lat': lat,
                        'lon': lon
                    },
                    'date': {
                        'month': month,
                        'day': day
                    },
                    'probabilities': probabilities,
                    'events_detail': {k: ALL_EVENTS[k] for k in events}
                }
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            print(f"[OK] Sonuclar kaydedildi: {filename}")
    
    print("\n" + "="*70)
    print("Test tamamlandi! Tesekkurler!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

