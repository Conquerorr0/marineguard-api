"""
Render API response'unu debug et - tam response'u goster.
"""

import requests
import json

# Test URL
url = "https://marineguard-api.onrender.com"

print("=" * 70)
print("DEBUG: Render API Response Testi")
print("=" * 70)
print(f"URL: {url}\n")

# Test payload
payload = {
    "lat": 41.0082,
    "lon": 28.9784,
    "month": 8,
    "day": 15,
    "events": ["wind_high", "wave_high", "sst_high"],
    "use_synthetic": True
}

print("Request Payload:")
print(json.dumps(payload, indent=2))
print("\nIstek gonderiliyor...\n")

try:
    response = requests.post(
        f"{url}/calculate_probability",
        json=payload,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nRaw Response Text:")
    print(response.text)
    
    print(f"\n" + "=" * 70)
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("Parsed JSON:")
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"JSON parse hatasi: {e}")
    
except Exception as e:
    print(f"Request hatasi: {e}")
    import traceback
    traceback.print_exc()

