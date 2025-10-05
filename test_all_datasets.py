"""
Comprehensive Test Script for NASA EarthData Probability API
Tests all 9 datasets with both synthetic and real OPeNDAP data
"""

import requests
import json
import logging
import time
from typing import Dict, List

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API base URL (local veya production)
API_URL = "http://localhost:5000"

# Tüm desteklenen olaylar
ALL_EVENTS = [
    'wind_high',      # CCMP Wind Speed
    'rain_high',      # GPCP Daily Precipitation
    'wave_high',      # Merged Altimeter SWH
    'storm_high',     # TRMM/GPM TCPF
    'fog_low',        # MODIS AOD
    'sst_high',       # NOAA OI SST V2
    'current_strong', # OSCAR Surface Currents
    'tide_high',      # TPXO9 Tide Model
    'ssha_high'       # MEaSUREs Gridded SSHA
]


def test_health_check():
    """Test API sağlık kontrolü"""
    logger.info("Testing health check endpoint...")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        
        if response.status_code == 200:
            logger.info(f"✅ Health check passed: {response.json()}")
            return True
        else:
            logger.error(f"❌ Health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to API. Make sure it's running.")
        return False
    except Exception as e:
        logger.error(f"❌ Health check error: {e}")
        return False


def test_get_events():
    """Test available events endpoint"""
    logger.info("Testing get events endpoint...")
    
    try:
        response = requests.get(f"{API_URL}/events", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Get events passed: {data['total_events']} events available")
            return True
        else:
            logger.error(f"❌ Get events failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Get events error: {e}")
        return False


def test_calculate_probability(
    lat: float,
    lon: float,
    month: int,
    day: int,
    events: List[str],
    thresholds: Dict[str, float] = None,
    use_synthetic: bool = True,
    test_name: str = "Test"
):
    """
    Test calculate_probability endpoint
    
    Args:
        lat: Latitude
        lon: Longitude
        month: Month (1-12)
        day: Day (1-31)
        events: List of events to check
        thresholds: Optional custom thresholds
        use_synthetic: Use synthetic data for testing
        test_name: Name of the test
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"TEST: {test_name}")
    logger.info(f"{'='*70}")
    logger.info(f"Location: ({lat}, {lon}), Date: {month}/{day}")
    logger.info(f"Events: {events}")
    logger.info(f"Synthetic: {use_synthetic}")
    
    payload = {
        'lat': lat,
        'lon': lon,
        'month': month,
        'day': day,
        'events': events,
        'use_synthetic': use_synthetic
    }
    
    if thresholds:
        payload['thresholds'] = thresholds
        logger.info(f"Custom thresholds: {thresholds}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/calculate_probability",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=120  # 2 dakika timeout (gerçek veri için)
        )
        elapsed_time = time.time() - start_time
        
        logger.info(f"Response time: {elapsed_time:.2f}s")
        logger.info(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                probabilities = data['data']['probabilities']
                logger.info("✅ Test PASSED")
                logger.info("\nProbabilities:")
                
                for event, prob in probabilities.items():
                    if prob is not None:
                        logger.info(f"  - {event:20s}: {prob:6.4f} ({prob*100:5.1f}%)")
                    else:
                        logger.warning(f"  - {event:20s}: ERROR")
                
                return True, data
            else:
                logger.error(f"❌ Test FAILED: {data.get('error', 'Unknown error')}")
                return False, data
                
        elif response.status_code == 400:
            data = response.json()
            logger.warning(f"⚠️  Bad Request: {data.get('error')}")
            return False, data
            
        elif response.status_code == 500:
            data = response.json()
            logger.error(f"❌ Server Error: {data.get('error')}")
            return False, data
            
        else:
            logger.error(f"❌ Unexpected status code: {response.status_code}")
            return False, None
            
    except requests.exceptions.Timeout:
        logger.error("❌ Request timeout (>120s)")
        return False, None
        
    except requests.exceptions.ConnectionError:
        logger.error("❌ Connection error")
        return False, None
        
    except Exception as e:
        logger.error(f"❌ Test error: {e}", exc_info=True)
        return False, None


def test_all_events_synthetic():
    """Test all 9 events with synthetic data (Istanbul, July 15)"""
    return test_calculate_probability(
        lat=40.0,
        lon=30.0,
        month=7,
        day=15,
        events=ALL_EVENTS,
        use_synthetic=True,
        test_name="All 9 Events - Synthetic Data (Istanbul)"
    )


def test_subset_events_synthetic():
    """Test subset of events with synthetic data (Antalya, August 1)"""
    return test_calculate_probability(
        lat=36.9,
        lon=30.7,
        month=8,
        day=1,
        events=['wind_high', 'rain_high', 'wave_high', 'sst_high'],
        use_synthetic=True,
        test_name="4 Events - Synthetic Data (Antalya)"
    )


def test_custom_thresholds():
    """Test with custom thresholds"""
    custom_thresholds = {
        'wind_high': 15.0,
        'rain_high': 15.0,
        'sst_high': 28.0
    }
    
    return test_calculate_probability(
        lat=38.4,
        lon=27.1,
        month=6,
        day=20,
        events=['wind_high', 'rain_high', 'sst_high'],
        thresholds=custom_thresholds,
        use_synthetic=True,
        test_name="Custom Thresholds (Izmir)"
    )


def test_real_opendap_data():
    """Test with real OPeNDAP data (will likely fallback to synthetic if no credentials)"""
    logger.info("\n" + "="*70)
    logger.info("⚠️  REAL DATA TEST - This may take 30-60 seconds")
    logger.info("⚠️  Will fallback to synthetic if OPeNDAP fails")
    logger.info("="*70)
    
    return test_calculate_probability(
        lat=40.0,
        lon=30.0,
        month=7,
        day=15,
        events=['wind_high', 'sst_high'],  # Test sadece 2 olay
        use_synthetic=False,  # Gerçek veri dene
        test_name="Real OPeNDAP Data Test (2 Events)"
    )


def test_error_invalid_latitude():
    """Test error handling - invalid latitude"""
    return test_calculate_probability(
        lat=100.0,  # Invalid: > 90
        lon=30.0,
        month=7,
        day=15,
        events=['wind_high'],
        use_synthetic=True,
        test_name="Error Test - Invalid Latitude"
    )


def test_error_invalid_event():
    """Test error handling - invalid event name"""
    return test_calculate_probability(
        lat=40.0,
        lon=30.0,
        month=7,
        day=15,
        events=['wind_high', 'tsunami', 'earthquake'],  # Invalid events
        use_synthetic=True,
        test_name="Error Test - Invalid Event Names"
    )


def test_error_missing_fields():
    """Test error handling - missing required fields"""
    logger.info("\n" + "="*70)
    logger.info("TEST: Error Test - Missing Fields")
    logger.info("="*70)
    
    payload = {
        'lat': 40.0,
        'lon': 30.0
        # Missing month, day, events
    }
    
    try:
        response = requests.post(
            f"{API_URL}/calculate_probability",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        logger.info(f"Status code: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            logger.info(f"✅ Error handling works: {data.get('error')}")
            return True, data
        else:
            logger.error(f"❌ Expected 400, got {response.status_code}")
            return False, None
            
    except Exception as e:
        logger.error(f"❌ Test error: {e}")
        return False, None


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*70)
    print("NASA EARTHDATA PROBABILITY API - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print("\nAPI URL:", API_URL)
    print("\nTest Categories:")
    print("  1. Basic endpoint tests (health, events)")
    print("  2. Synthetic data tests (all 9 datasets)")
    print("  3. Custom threshold tests")
    print("  4. Real OPeNDAP data test (optional)")
    print("  5. Error handling tests")
    print("\n" + "="*70 + "\n")
    
    results = []
    
    # Basic endpoint tests
    logger.info("\n### CATEGORY 1: Basic Endpoint Tests ###\n")
    results.append(("Health Check", test_health_check()))
    results.append(("Get Events", test_get_events()))
    
    # Synthetic data tests
    logger.info("\n### CATEGORY 2: Synthetic Data Tests ###\n")
    success, _ = test_all_events_synthetic()
    results.append(("All 9 Events - Synthetic", success))
    
    success, _ = test_subset_events_synthetic()
    results.append(("Subset Events - Synthetic", success))
    
    # Custom thresholds
    logger.info("\n### CATEGORY 3: Custom Thresholds ###\n")
    success, _ = test_custom_thresholds()
    results.append(("Custom Thresholds", success))
    
    # Real data test (optional)
    logger.info("\n### CATEGORY 4: Real OPeNDAP Data ###\n")
    success, _ = test_real_opendap_data()
    results.append(("Real OPeNDAP Data", success))
    
    # Error handling tests
    logger.info("\n### CATEGORY 5: Error Handling ###\n")
    success, _ = test_error_invalid_latitude()
    results.append(("Error - Invalid Latitude", not success))  # Should fail with 400
    
    success, _ = test_error_invalid_event()
    results.append(("Error - Invalid Event", not success))  # Should fail with 400
    
    success, _ = test_error_missing_fields()
    results.append(("Error - Missing Fields", success))  # Should return 400 correctly
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status:10s} | {test_name}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*70 + "\n")
    
    return passed == total


def main():
    """Main test runner"""
    success = run_all_tests()
    
    if success:
        logger.info("✅ All tests passed!")
        return 0
    else:
        logger.warning("⚠️  Some tests failed. Check logs above.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

