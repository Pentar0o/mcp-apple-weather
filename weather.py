"""Apple WeatherKit integration"""
import requests
import json
import logging
from app_config import LANGUAGE, TIMEZONE, WEATHER_KEY_FILE, WEATHER_KEY_ID
from auth import generate_jwt_token, load_private_key
from utils import format_date, set_french_locale
from maps import get_location_coordinates

logger = logging.getLogger(__name__)

# Weather condition translations
CONDITION_TRANSLATIONS = {
    "clear": "ensoleillé",
    "mostly clear": "principalement ensoleillé",
    "mostlyclear": "principalement ensoleillé",
    "partly cloudy": "partiellement nuageux",
    "cloudy": "nuageux",
    "overcast": "couvert",
    "rain": "pluvieux",
    "light rain": "pluie légère",
    "heavy rain": "forte pluie",
    "snow": "neigeux",
    "sleet": "grésil",
    "hail": "grêle",
    "thunderstorm": "orageux",
    "fog": "brumeux",
    "windy": "venteux"
}


def get_weather_data(jwt_token, latitude, longitude, country_code):
    """
    Retrieve weather data for the specified location.
    
    Args:
        jwt_token: JWT authentication token
        latitude: Location latitude
        longitude: Location longitude
        country_code: Country code
        
    Returns:
        Weather data dict or None
    """
    url = f"https://weatherkit.apple.com/api/v1/weather/{LANGUAGE}/{latitude}/{longitude}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json"
    }
    params = {
        "countryCode": country_code,
        "timezone": TIMEZONE,
        "dataSets": "forecastDaily"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to retrieve weather data: {response.status_code} {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return None


def weatherkit_tool(city_name: str, country: str = "FR") -> str:
    """
    Get daily weather forecast via Apple WeatherKit.
    
    Args:
        city_name: Name of the city
        country: Country code (default: "FR")
        
    Returns:
        JSON string with weather forecast or error message
    """
    try:
        # Set French locale for date formatting
        set_french_locale()
        
        # Load WeatherKit credentials
        weather_private_key = load_private_key(WEATHER_KEY_FILE)
        weather_token = generate_jwt_token(weather_private_key, WEATHER_KEY_ID)
        
        # Get location coordinates
        location = get_location_coordinates(city_name, country)
        if not location or not all(location):
            return "Erreur : Impossible d'obtenir les coordonnées pour la ville spécifiée."
        
        latitude, longitude, country_code = location
        
        # Get weather data
        weather_data = get_weather_data(weather_token, latitude, longitude, country_code)
        if not weather_data:
            return "Erreur : Échec de récupération des données météo."
        
        # Process daily forecast
        forecast_daily = weather_data.get("forecastDaily", {})
        days = forecast_daily.get("days", [])
        
        if not days:
            return "Erreur : Aucune prévision quotidienne disponible pour cette localisation."
        
        # Format weather report
        weather_report = []
        for day in days:
            # Get and translate weather condition
            condition_code = day.get("conditionCode", "")
            condition = CONDITION_TRANSLATIONS.get(condition_code.lower(), condition_code)
            
            # Extract weather metrics with proper rounding
            temp_max = day.get("temperatureMax")
            temp_min = day.get("temperatureMin")
            precipitation = day.get("precipitationAmount", 0)
            precipitation_chance = day.get("precipitationChance", 0)
            wind_speed = day.get("windSpeedMax", 0)
            
            weather_report.append({
                "date": format_date(day.get("forecastStart", "")),
                "condition": condition,
                "temperature_max": round(temp_max) if temp_max is not None else "N/D",
                "temperature_min": round(temp_min) if temp_min is not None else "N/D",
                "precipitations": round(precipitation, 1),
                "chance_precipitations": round(precipitation_chance * 100),
                "vitesse_vent": round(wind_speed)
            })
        
        return json.dumps(weather_report, ensure_ascii=False, indent=2)
        
    except FileNotFoundError as e:
        logger.error(f"Certificate file not found: {e}")
        return f"Erreur : Fichier de certificat introuvable - {e}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Erreur lors de l'exécution : {e}"
