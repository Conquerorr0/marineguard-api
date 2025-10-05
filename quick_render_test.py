"""
Render.com API'sini hizli test et - URL parametre olarak alinir.

Kullanim:
    python quick_render_test.py https://marineguard-api.onrender.com 
"""

import sys
import requests
import json

def quick_test(base_url):
    """Hizli API testi - sentetik veri ile."""
    print("=" * 70)
    print("NASA EarthData API - Render.com Hizli Test")
    print("=" * 70)
    print(f"URL: {base_url}\n")
    
    # Test 1: Health Check
    print("[1/4] Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print(f"    BASARILI - Status: {response.json()['status']}")
        else:
            print(f"    HATA - Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"    HATA - {str(e)}")
        return False
    
    # Test 2: Events
    print("\n[2/4] Events Listesi...")
    try:
        response = requests.get(f"{base_url}/events", timeout=10)
        if response.status_code == 200:
            events = response.json()['events']
            print(f"    BASARILI - {len(events)} event mevcut")
        else:
            print(f"    HATA - Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"    HATA - {str(e)}")
        return False
    
    # Test 3: Sentetik Veri - Istanbul
    print("\n[3/4] Sentetik Veri Testi (Istanbul)...")
    try:
        payload = {
            "lat": 41.0082,
            "lon": 28.9784,
            "month": 8,
            "day": 15,
            "events": ["wind_high", "wave_high", "sst_high"],
            "use_synthetic": True
        }
        response = requests.post(
            f"{base_url}/calculate_probability",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            data = result.get('data', result)  # Yeni format (data wrapper) veya eski format
            print(f"    BASARILI - {len(data['probabilities'])} event hesaplandi")
            print(f"    Olasiliklar:")
            for event, prob in data['probabilities'].items():
                print(f"      - {event}: {prob:.2%}")
        else:
            print(f"    HATA - Status Code: {response.status_code}")
            print(f"    Response: {response.text}")
            return False
    except Exception as e:
        print(f"    HATA - {str(e)}")
        return False
    
    # Test 4: Sentetik Veri - Tum Eventler (Antalya)
    print("\n[4/4] Tum Eventler Testi (Antalya)...")
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
        response = requests.post(
            f"{base_url}/calculate_probability",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            data = result.get('data', result)  # Yeni format (data wrapper) veya eski format
            print(f"    BASARILI - {len(data['probabilities'])} event hesaplandi")
            print(f"    Ornek olasiliklar:")
            for i, (event, prob) in enumerate(list(data['probabilities'].items())[:3]):
                print(f"      - {event}: {prob:.2%}")
            print(f"      ... ve {len(data['probabilities']) - 3} event daha")
        else:
            print(f"    HATA - Status Code: {response.status_code}")
            print(f"    Response: {response.text}")
            return False
    except Exception as e:
        print(f"    HATA - {str(e)}")
        return False
    
    print("\n" + "=" * 70)
    print("TUM TESTLER BASARILI!")
    print("=" * 70)
    print("\nAPI'niz Render.com'da basariyla calisiyor!")
    print("\nONEMLI NOTLAR:")
    print("- Sentetik veri hizli ve guvenilir (1-2 saniye)")
    print("- Gercek NASA verisi cok yavas (60-180 saniye)")
    print("- Render.com Free tier icin SENTETIK kullanin")
    print("\nAPI hazir! Frontend entegrasyonu icin bu URL'yi kullanin:")
    print(f"  {base_url}/calculate_probability")
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("KULLANIM: python quick_render_test.py <RENDER_URL>")
        print("\nOrnek:")
        print("  python quick_render_test.py https://nasa-probability-api.onrender.com")
        print("\nRender URL'nizi Render Dashboard'dan kopyalayin.")
        sys.exit(1)
    
    url = sys.argv[1].rstrip("/")
    if not url.startswith("http"):
        url = f"https://{url}"
    
    success = quick_test(url)
    sys.exit(0 if success else 1)

