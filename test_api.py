"""
Flask API Test Script
Test different scenarios for the /calculate_probability endpoint
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"


def print_response(response, title):
    """Pretty print API response"""
    print("\n" + "="*70)
    print(title)
    print("="*70)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "TEST 1: Health Check")


def test_get_events():
    """Test get available events endpoint"""
    response = requests.get(f"{BASE_URL}/events")
    print_response(response, "TEST 2: Get Available Events")


def test_basic_calculation():
    """Test basic probability calculation"""
    payload = {
        "lat": 40.0,
        "lon": 29.0,
        "month": 7,
        "day": 15,
        "events": ["wind_high", "wave_high"],
        "use_synthetic": True  # Test için sentetik veri
    }
    
    response = requests.post(
        f"{BASE_URL}/calculate_probability",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "TEST 3: Basic Calculation (Istanbul, July 15)")


def test_custom_thresholds():
    """Test with custom thresholds"""
    payload = {
        "lat": 36.9,
        "lon": 30.7,
        "month": 8,
        "day": 1,
        "events": ["wind_high", "rain_high", "sst_high"],
        "thresholds": {
            "wind_high": 15.0,
            "rain_high": 15.0,
            "sst_high": 28.0
        },
        "use_synthetic": True
    }
    
    response = requests.post(
        f"{BASE_URL}/calculate_probability",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "TEST 4: Custom Thresholds (Antalya, Aug 1)")


def test_all_events():
    """Test with all available events"""
    payload = {
        "lat": 38.4,
        "lon": 27.1,
        "month": 6,
        "day": 20,
        "events": [
            "wind_high", "rain_high", "wave_high", "storm_high",
            "fog_low", "sst_high", "current_strong", "tide_high", "ssha_high"
        ],
        "use_synthetic": True
    }
    
    response = requests.post(
        f"{BASE_URL}/calculate_probability",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "TEST 5: All Events (Izmir, June 20)")


def test_missing_field():
    """Test error handling - missing required field"""
    payload = {
        "lat": 40.0,
        "lon": 29.0,
        "month": 7
        # Missing 'day' and 'events'
    }
    
    response = requests.post(
        f"{BASE_URL}/calculate_probability",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "TEST 6: Error - Missing Fields")


def test_invalid_lat():
    """Test error handling - invalid latitude"""
    payload = {
        "lat": 100.0,  # Invalid: > 90
        "lon": 29.0,
        "month": 7,
        "day": 15,
        "events": ["wind_high"],
        "use_synthetic": True
    }
    
    response = requests.post(
        f"{BASE_URL}/calculate_probability",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "TEST 7: Error - Invalid Latitude")


def test_invalid_event():
    """Test error handling - invalid event name"""
    payload = {
        "lat": 40.0,
        "lon": 29.0,
        "month": 7,
        "day": 15,
        "events": ["wind_high", "invalid_event", "tsunami"],  # Invalid events
        "use_synthetic": True
    }
    
    response = requests.post(
        f"{BASE_URL}/calculate_probability",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "TEST 8: Error - Invalid Event Names")


def test_non_json_request():
    """Test error handling - non-JSON request"""
    response = requests.post(
        f"{BASE_URL}/calculate_probability",
        data="This is not JSON",
        headers={"Content-Type": "text/plain"}
    )
    
    print_response(response, "TEST 9: Error - Non-JSON Request")


def test_empty_events_list():
    """Test error handling - empty events list"""
    payload = {
        "lat": 40.0,
        "lon": 29.0,
        "month": 7,
        "day": 15,
        "events": [],  # Empty list
        "use_synthetic": True
    }
    
    response = requests.post(
        f"{BASE_URL}/calculate_probability",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "TEST 10: Error - Empty Events List")


def test_curl_examples():
    """Print curl command examples"""
    print("\n" + "="*70)
    print("CURL COMMAND EXAMPLES")
    print("="*70)
    
    print("\n1. Basic Request:")
    print("""curl -X POST http://localhost:5000/calculate_probability \\
  -H "Content-Type: application/json" \\
  -d '{
    "lat": 40.0,
    "lon": 29.0,
    "month": 7,
    "day": 15,
    "events": ["wind_high", "wave_high"],
    "use_synthetic": true
  }'""")
    
    print("\n2. With Custom Thresholds:")
    print("""curl -X POST http://localhost:5000/calculate_probability \\
  -H "Content-Type: application/json" \\
  -d '{
    "lat": 36.9,
    "lon": 30.7,
    "month": 8,
    "day": 1,
    "events": ["wind_high", "rain_high"],
    "thresholds": {"wind_high": 15.0, "rain_high": 15.0},
    "use_synthetic": true
  }'""")
    
    print("\n3. Get Available Events:")
    print("curl http://localhost:5000/events")
    
    print("\n4. Health Check:")
    print("curl http://localhost:5000/health")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("NASA EARTHDATA PROBABILITY API - TEST SUITE")
    print("="*70)
    print("\nMake sure the Flask server is running:")
    print("  python app.py")
    print("\nStarting tests...")
    
    try:
        # GET endpoint tests
        test_health_check()
        test_get_events()
        
        # Valid POST requests
        test_basic_calculation()
        test_custom_thresholds()
        test_all_events()
        
        # Error handling tests
        test_missing_field()
        test_invalid_lat()
        test_invalid_event()
        test_non_json_request()
        test_empty_events_list()
        
        # Curl examples
        test_curl_examples()
        
        print("\n" + "="*70)
        print("ALL TESTS COMPLETED")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to API server.")
        print("Please make sure the Flask server is running:")
        print("  python app.py")
        print("\nThen run the tests again:")
        print("  python test_api.py\n")


if __name__ == "__main__":
    main()

