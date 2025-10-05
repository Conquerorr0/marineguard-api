"""
Quick Heroku API Test
Test your deployed API on Heroku
"""

import requests
import json

# Heroku app URL'inizi buraya yazın
HEROKU_URL = "https://nasa-probability-api-2b173d22b072.herokuapp.com"

print("="*70)
print("HEROKU API TEST")
print("="*70)
print(f"\nAPI URL: {HEROKU_URL}\n")

# Test 1: Root endpoint
print("\n[TEST 1] Root Endpoint (/):")
try:
    response = requests.get(f"{HEROKU_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

# Test 2: Health check
print("\n[TEST 2] Health Check (/health):")
try:
    response = requests.get(f"{HEROKU_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

# Test 3: Get events
print("\n[TEST 3] Get Events (/events):")
try:
    response = requests.get(f"{HEROKU_URL}/events")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total events: {data.get('total_events')}")
    print("Events:", list(data.get('events', {}).keys()))
except Exception as e:
    print(f"Error: {e}")

# Test 4: Calculate probability
print("\n[TEST 4] Calculate Probability (POST /calculate_probability):")
try:
    payload = {
        'lat': 40.0,
        'lon': 29.0,
        'month': 7,
        'day': 15,
        'events': ['wind_high', 'wave_high'],
        'use_synthetic': True
    }
    response = requests.post(
        f"{HEROKU_URL}/calculate_probability",
        json=payload,
        timeout=30
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    if data.get('success'):
        print("Probabilities:")
        for event, prob in data['data']['probabilities'].items():
            print(f"  - {event}: {prob:.4f} ({prob*100:.1f}%)")
    else:
        print(f"Error: {data.get('error')}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*70)
print("TESTS COMPLETED")
print("="*70)

