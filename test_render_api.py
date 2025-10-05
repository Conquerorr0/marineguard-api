"""
Render.com'da deploy edilen NASA EarthData Probability API'sini test eden script.
"""

import requests
import json
from datetime import datetime

def test_render_api(base_url):
    """
    Render.com'da deploy edilen API'yi test et.
    
    Args:
        base_url: Render.com URL'si (örnek: https://marineguard-api.onrender.com )
    """
    print("=" * 70)
    print("NASA EarthData Probability API - Render.com Test")
    print("=" * 70)
    print(f"Base URL: {base_url}\n")
    
    # Test 1: Root endpoint (/)
    print("[Test 1] Root Endpoint")
    print("-" * 70)
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"API Version: {data.get('version', 'N/A')}")
            print(f"Status: {data.get('status', 'N/A')}")
            print("BASARILI")
        else:
            print(f"HATA: {response.text}")
    except Exception as e:
        print(f"HATA: {str(e)}")
    print()
    
    # Test 2: Health check
    print("[Test 2] Health Check")
    print("-" * 70)
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status', 'N/A')}")
            print("BASARILI")
        else:
            print(f"HATA: {response.text}")
    except Exception as e:
        print(f"HATA: {str(e)}")
    print()
    
    # Test 3: Events endpoint
    print("[Test 3] Available Events")
    print("-" * 70)
    try:
        response = requests.get(f"{base_url}/events", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', {})
            print(f"Toplam Event Sayisi: {len(events)}")
            print("Mevcut Eventler:")
            for event_name in events.keys():
                print(f"  - {event_name}")
            print("BASARILI")
        else:
            print(f"HATA: {response.text}")
    except Exception as e:
        print(f"HATA: {str(e)}")
    print()
    
    # Test 4: Sentetik veri ile olasılık hesaplama (İstanbul)
    print("[Test 4] Olasilik Hesaplama - Sentetik Veri (Istanbul)")
    print("-" * 70)
    try:
        payload = {
            "lat": 41.0082,
            "lon": 28.9784,
            "month": 8,
            "day": 15,
            "events": ["wind_high", "wave_high", "sst_high"],
            "use_synthetic": True
        }
        print(f"Request Payload: {json.dumps(payload, indent=2)}")
        print("\nİstek gonderiliyor...")
        
        response = requests.post(
            f"{base_url}/calculate_probability",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("\nSonuclar:")
            print(f"  Lokasyon: {data['location']}")
            print(f"  Tarih: {data['date']}")
            print(f"  Veri Modu: {'Sentetik' if data['use_synthetic'] else 'Gercek NASA'}")
            print(f"\n  Olasiliklar:")
            for event, prob in data['probabilities'].items():
                print(f"    {event}: {prob:.2%}")
            print("\nBASARILI")
        else:
            print(f"HATA: {response.text}")
    except requests.exceptions.Timeout:
        print("HATA: Request timeout (30 saniye)")
    except Exception as e:
        print(f"HATA: {str(e)}")
    print()
    
    # Test 5: Sentetik veri ile tüm eventler (Antalya)
    print("[Test 5] Tum Eventler - Sentetik Veri (Antalya)")
    print("-" * 70)
    try:
        payload = {
            "lat": 36.8969,
            "lon": 30.7133,
            "month": 7,
            "day": 20,
            "events": [
                "wind_high", "rain_high", "wave_high", 
                "storm_high", "fog_low", "sst_high",
                "current_strong", "tide_high", "ssha_high"
            ],
            "use_synthetic": True
        }
        print(f"Lokasyon: Antalya (36.8969, 30.7133)")
        print(f"Tarih: 20 Temmuz")
        print(f"Event Sayisi: {len(payload['events'])}")
        print("\nİstek gonderiliyor...")
        
        response = requests.post(
            f"{base_url}/calculate_probability",
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("\nSonuclar:")
            print(f"  Hesaplanan Event Sayisi: {len(data['probabilities'])}")
            print(f"\n  Olasiliklar:")
            for event, prob in data['probabilities'].items():
                print(f"    {event}: {prob:.2%}")
            print("\nBASARILI")
        else:
            print(f"HATA: {response.text}")
    except requests.exceptions.Timeout:
        print("HATA: Request timeout (30 saniye)")
    except Exception as e:
        print(f"HATA: {str(e)}")
    print()
    
    # Test 6: Gerçek NASA verisi ile test (TEK event - hızlı test)
    print("[Test 6] Gercek NASA Verisi - TEK Event (Izmir)")
    print("-" * 70)
    print("UYARI: Gercek NASA verisi yavas olabilir (60-120 saniye).")
    user_input = input("Gercek veri testini calistirmak istiyor musunuz? (e/h) [h]: ").strip().lower()
    
    if user_input == 'e':
        try:
            payload = {
                "lat": 38.4237,
                "lon": 27.1428,
                "month": 6,
                "day": 10,
                "events": ["sst_high"],  # En hızlı veri seti
                "use_synthetic": False
            }
            print(f"Lokasyon: Izmir (38.4237, 27.1428)")
            print(f"Tarih: 10 Haziran")
            print(f"Event: sst_high (en hizli veri seti)")
            print("\nİstek gonderiliyor... (Lutfen bekleyin, 60-120 saniye surebilir)")
            
            response = requests.post(
                f"{base_url}/calculate_probability",
                json=payload,
                timeout=180  # 3 dakika timeout
            )
            
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("\nSonuclar:")
                print(f"  Lokasyon: {data['location']}")
                print(f"  Tarih: {data['date']}")
                print(f"  Veri Modu: {'Sentetik' if data['use_synthetic'] else 'Gercek NASA'}")
                print(f"\n  Olasilik:")
                for event, prob in data['probabilities'].items():
                    print(f"    {event}: {prob:.2%}")
                print("\nBASARILI - Gercek NASA verisi basariyla cekildi!")
            else:
                print(f"HATA: {response.text}")
        except requests.exceptions.Timeout:
            print("HATA: Request timeout (180 saniye)")
            print("Render.com Free tier icin gercek NASA verisi cok yavas olabilir.")
        except Exception as e:
            print(f"HATA: {str(e)}")
    else:
        print("Atlandi.")
    print()
    
    # Özet
    print("=" * 70)
    print("Test Tamamlandi!")
    print("=" * 70)
    print("\nONERILER:")
    print("- Render.com Free tier icin SENTETIK VERI kullanin (hizli, guvenilir)")
    print("- Gercek NASA verisi yavas ve zaman asimina ugreyabilir")
    print("- Birden fazla event icin mutlaka use_synthetic: true kullanin")
    print()


if __name__ == "__main__":
    print("\n")
    print("=" * 70)
    print("Render.com API Test Script")
    print("=" * 70)
    
    # Kullanıcıdan Render URL'sini al
    default_url = "https://nasa-probability-api.onrender.com"
    print(f"\nRender.com URL'nizi girin (varsayilan: {default_url})")
    user_url = input("URL: ").strip()
    
    if not user_url:
        base_url = default_url
    else:
        # http:// veya https:// yoksa ekle
        if not user_url.startswith("http"):
            base_url = f"https://{user_url}"
        else:
            base_url = user_url
    
    # Trailing slash varsa kaldır
    base_url = base_url.rstrip("/")
    
    print(f"\nTest edilecek URL: {base_url}")
    input("\nDevam etmek icin Enter'a basin...")
    print("\n")
    
    # Testleri çalıştır
    test_render_api(base_url)

