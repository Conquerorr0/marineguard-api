"""
Flask API for NASA EarthData Probability Calculations
Endpoint: POST /calculate_probability
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, List, Optional

from calculate_ocean_probabilities import calculate_probabilities, DATASET_CONFIG

# Flask uygulamasını oluştur
app = Flask(__name__)

# CORS'u etkinleştir (tüm originler için)
CORS(app)

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    """
    API sağlık kontrolü endpoint'i.
    
    Returns:
        JSON response with status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'NASA EarthData Probability API',
        'version': '1.0.0'
    }), 200


@app.route('/events', methods=['GET'])
def get_available_events():
    """
    Desteklenen tüm olayları ve detaylarını döner.
    
    Returns:
        JSON response with available events and their configurations
    """
    events_info = {}
    for event, config in DATASET_CONFIG.items():
        events_info[event] = {
            'name': config['name'],
            'threshold': config['threshold'],
            'year_range': config['year_range'],
            'description': f"{config['name']} - Default threshold: {config['threshold']}"
        }
    
    return jsonify({
        'success': True,
        'total_events': len(events_info),
        'events': events_info
    }), 200


@app.route('/calculate_probability', methods=['POST'])
def calculate_probability():
    """
    Belirli konum ve tarih için olay olasılıklarını hesaplar.
    
    Request Body (JSON):
        {
            "lat": float,              # Enlem (-90 ile 90 arası)
            "lon": float,              # Boylam (-180 ile 180 arası)
            "month": int,              # Ay (1-12)
            "day": int,                # Gün (1-31)
            "events": list[str],       # Olay listesi (örn: ['wind_high', 'rain_high'])
            "thresholds": dict,        # Opsiyonel: Özel threshold'lar (örn: {'rain_high': 15.0})
            "use_synthetic": bool      # Opsiyonel: Test için sentetik veri kullan (varsayılan: False)
        }
    
    Returns:
        JSON response:
        {
            "success": true,
            "data": {
                "location": {"lat": 40.0, "lon": 29.0},
                "date": {"month": 7, "day": 15},
                "probabilities": {
                    "wind_high": 0.25,
                    "rain_high": 0.15
                }
            }
        }
    
    Error Response (400 Bad Request):
        {
            "success": false,
            "error": "Error message"
        }
    """
    try:
        # Request body'den JSON verisini al
        if not request.is_json:
            logger.warning("Request body is not JSON")
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        data = request.get_json()
        
        # Gerekli parametreleri kontrol et
        required_fields = ['lat', 'lon', 'month', 'day', 'events']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            logger.warning(f"Missing required fields: {missing_fields}")
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Parametreleri al
        lat = data.get('lat')
        lon = data.get('lon')
        month = data.get('month')
        day = data.get('day')
        events = data.get('events')
        thresholds = data.get('thresholds', None)
        use_synthetic = data.get('use_synthetic', False)
        
        # Parametre tipi kontrolü
        try:
            lat = float(lat)
            lon = float(lon)
            month = int(month)
            day = int(day)
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid parameter types: {e}")
            return jsonify({
                'success': False,
                'error': 'lat and lon must be numbers, month and day must be integers'
            }), 400
        
        # events listesi kontrolü
        if not isinstance(events, list) or len(events) == 0:
            logger.warning("events must be a non-empty list")
            return jsonify({
                'success': False,
                'error': 'events must be a non-empty list'
            }), 400
        
        # Geçersiz event kontrolü
        invalid_events = [e for e in events if e not in DATASET_CONFIG]
        if invalid_events:
            logger.warning(f"Invalid events: {invalid_events}")
            return jsonify({
                'success': False,
                'error': f'Invalid events: {", ".join(invalid_events)}. Valid events: {", ".join(DATASET_CONFIG.keys())}'
            }), 400
        
        # thresholds dict kontrolü (opsiyonel)
        if thresholds is not None and not isinstance(thresholds, dict):
            logger.warning("thresholds must be a dictionary")
            return jsonify({
                'success': False,
                'error': 'thresholds must be a dictionary'
            }), 400
        
        # Parametre aralık kontrolü
        if not (-90 <= lat <= 90):
            return jsonify({
                'success': False,
                'error': f'lat must be between -90 and 90, got {lat}'
            }), 400
        
        if not (-180 <= lon <= 180):
            return jsonify({
                'success': False,
                'error': f'lon must be between -180 and 180, got {lon}'
            }), 400
        
        if not (1 <= month <= 12):
            return jsonify({
                'success': False,
                'error': f'month must be between 1 and 12, got {month}'
            }), 400
        
        if not (1 <= day <= 31):
            return jsonify({
                'success': False,
                'error': f'day must be between 1 and 31, got {day}'
            }), 400
        
        # Log request
        logger.info(f"Calculate probability request: lat={lat}, lon={lon}, month={month}, day={day}, events={events}")
        
        # Olasılıkları hesapla
        probabilities = calculate_probabilities(
            lat=lat,
            lon=lon,
            month=month,
            day=day,
            events=events,
            thresholds=thresholds,
            use_synthetic=use_synthetic
        )
        
        # Response oluştur
        response = {
            'success': True,
            'data': {
                'location': {
                    'lat': lat,
                    'lon': lon
                },
                'date': {
                    'month': month,
                    'day': day
                },
                'probabilities': probabilities,
                'metadata': {
                    'total_events': len(events),
                    'custom_thresholds': thresholds is not None,
                    'synthetic_data': use_synthetic
                }
            }
        }
        
        logger.info(f"Successfully calculated probabilities: {probabilities}")
        
        return jsonify(response), 200
        
    except ValueError as e:
        logger.error(f"ValueError in calculate_probability: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        logger.error(f"Unexpected error in calculate_probability: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404 hata handler'ı"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """405 hata handler'ı"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """500 hata handler'ı"""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Development server
    logger.info("Starting Flask development server...")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

