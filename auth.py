"""JWT authentication for Apple APIs"""
from authlib.jose import jwt, JsonWebKey
import time
import requests
import logging
from app_config import WEATHER_KEY_ID, TEAM_ID, SERVICE_ID, MAP_KEY_ID

logger = logging.getLogger(__name__)


def load_private_key(private_key_path):
    """Load a private key from a .p8 file."""
    try:
        with open(private_key_path, 'r') as file:
            private_key_data = file.read()
        return JsonWebKey.import_key(private_key_data, {'kty': 'EC'})
    except Exception as e:
        logger.error(f"Error loading private key from {private_key_path}: {e}")
        raise


def generate_jwt_token(private_key, key_id, duration=300):
    """Generate a JWT token for Apple APIs."""
    iat = int(time.time())
    exp = iat + duration
    
    header = {'alg': 'ES256', 'kid': key_id, 'typ': 'JWT'}
    payload = {
        'iss': TEAM_ID,
        'iat': iat,
        'exp': exp,
        'sub': SERVICE_ID
    }
    
    # For MapKit, we don't need the 'sub' field
    if key_id == MAP_KEY_ID:
        del payload['sub']
    
    token = jwt.encode(header, payload, private_key).decode('utf-8').strip()
    return token


def request_maps_access_token(jwt_token):
    """Request a Maps access token using the JWT token."""
    url = "https://maps-api.apple.com/v1/token"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        maps_access_token = data.get('accessToken')
        if not maps_access_token:
            raise Exception("Error: 'accessToken' not found in the response.")
        return maps_access_token
    else:
        raise Exception(f"Failed to obtain Maps Access Token: {response.status_code} {response.text}")
