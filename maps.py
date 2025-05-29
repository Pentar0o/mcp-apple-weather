"""Apple Maps geocoding utilities"""
import requests
import logging
from app_config import MAP_KEY_FILE
from auth import load_private_key, request_maps_access_token, generate_jwt_token, MAP_KEY_ID

logger = logging.getLogger(__name__)


def geocode_city(city_name, maps_access_token):
    """
    Geocode a city name to get its latitude and longitude.
    
    Args:
        city_name: The name of the city to geocode
        maps_access_token: The Maps access token
        
    Returns:
        Tuple of (latitude, longitude, country_code) or (None, None, None)
    """
    url = "https://maps-api.apple.com/v1/geocode"
    headers = {
        "Authorization": f"Bearer {maps_access_token}",
        "Accept": "application/json"
    }
    params = {
        "q": city_name,
        "lang": "fr-FR"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                result = data['results'][0]
                latitude = result['coordinate']['latitude']
                longitude = result['coordinate']['longitude']
                country_code = result.get('countryCode')
                logger.info(f"Geocoded {city_name}: {latitude}, {longitude}, {country_code}")
                return latitude, longitude, country_code
            else:
                logger.warning(f"No results found for city: {city_name}")
                return None, None, None
        else:
            logger.error(f"Geocoding failed: {response.status_code} {response.text}")
            return None, None, None
    except Exception as e:
        logger.error(f"Error during geocoding: {e}")
        return None, None, None


def get_location_coordinates(address, country="FR"):
    """
    Get coordinates for a given address.
    
    Args:
        address: The address to geocode
        country: Country code (default: "FR")
        
    Returns:
        Tuple of (latitude, longitude, country_code) or None
    """
    try:
        # Load private key and generate tokens
        map_private_key = load_private_key(MAP_KEY_FILE)
        map_jwt_token = generate_jwt_token(map_private_key, MAP_KEY_ID)
        maps_access_token = request_maps_access_token(map_jwt_token)

        # Geocode the address
        city_name_full = f"{address},{country}" if country else address
        return geocode_city(city_name_full, maps_access_token)

    except Exception as e:
        logger.error(f"Error getting location coordinates: {e}")
        return None
