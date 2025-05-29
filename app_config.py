"""Configuration for Apple WeatherKit MCP Server"""
import os
from pathlib import Path

# Load environment variables from .env file if it exists
if Path(".env").exists():
    from dotenv import load_dotenv
    load_dotenv()

# Apple Developer credentials
WEATHER_KEY_ID = os.getenv("WEATHER_KEY_ID")
MAP_KEY_ID = os.getenv("MAP_KEY_ID")
TEAM_ID = os.getenv("TEAM_ID")  # Added - required for JWT generation
SERVICE_ID = os.getenv("SERVICE_ID")  # Added - required for JWT generation

# API configuration
LANGUAGE = "fr"
TIMEZONE = "Europe/Paris"

# Certificate paths
WEATHER_KEY_FILE = "certificats/AuthKey_Weather.p8"
MAP_KEY_FILE = "certificats/AuthKey_Mapkit.p8"
