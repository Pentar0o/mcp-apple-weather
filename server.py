#!/usr/bin/env python3
"""
MCP Server for Apple WeatherKit Integration

A Model Context Protocol server that provides weather forecast tools
using Apple WeatherKit API.
"""

import json
import logging
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import weather module
try:
    from weather import weatherkit_tool
except ImportError as e:
    logger.error(f"Failed to import weather module: {e}")
    raise

# Initialize FastMCP server
mcp = FastMCP("apple-weather")


def parse_weather_data(weather_data: str) -> Optional[list]:
    """Parse weather data from JSON string."""
    if isinstance(weather_data, str) and weather_data.startswith("Erreur"):
        return None
    
    try:
        return json.loads(weather_data)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse weather data: {weather_data[:100]}...")
        return None


def format_weather_forecast(data: list, city_name: str, country: str) -> str:
    """Format weather forecast data for display."""
    if not data:
        return f"Aucune donnée météo disponible pour {city_name}, {country}"
    
    response = f"Prévisions météo pour {city_name}, {country}:\n\n"
    
    for day in data:
        response += f"Date: {day.get('date', 'Date inconnue')}\n"
        response += f"Condition: {day.get('condition', 'N/D')}\n"
        response += f"Température: {day.get('temperature_min', 'N/D')}°C - {day.get('temperature_max', 'N/D')}°C\n"
        response += f"Précipitations: {day.get('precipitations', 'N/D')} mm "
        response += f"(chance: {day.get('chance_precipitations', 'N/D')}%)\n"
        response += f"Vent max: {day.get('vitesse_vent', 'N/D')} km/h\n"
        response += "-" * 40 + "\n"
    
    return response.rstrip()


@mcp.tool()
async def get_weather_forecast(city_name: str, country: str = "FR") -> str:
    """
    Obtient les prévisions météo quotidiennes pour une ville via Apple WeatherKit.

    Args:
        city_name: Nom de la ville (ex: "Paris", "Lyon")
        country: Code pays à 2 lettres (par défaut "FR")
        
    Returns:
        Prévisions météo formatées ou message d'erreur
    """
    try:
        logger.info(f"Fetching weather for {city_name}, {country}")
        weather_data = weatherkit_tool(city_name, country)
        
        parsed_data = parse_weather_data(weather_data)
        if parsed_data is None:
            return f"Erreur lors de la récupération de la météo pour {city_name}, {country}"
        
        return format_weather_forecast(parsed_data, city_name, country)
        
    except FileNotFoundError as e:
        logger.error(f"Missing certificates: {e}")
        return "Certificats Apple WeatherKit manquants"
    except Exception as e:
        logger.error(f"Weather fetch error: {e}")
        return f"Erreur lors de la récupération de la météo: {str(e)}"


@mcp.tool()
async def get_weather_summary(city_name: str, country: str = "FR") -> str:
    """
    Obtient un résumé météo simplifié pour une ville.

    Args:
        city_name: Nom de la ville (ex: "Paris", "Lyon")
        country: Code pays à 2 lettres (par défaut "FR")
        
    Returns:
        Résumé météo pour aujourd'hui et demain
    """
    try:
        logger.info(f"Fetching weather summary for {city_name}, {country}")
        weather_data = weatherkit_tool(city_name, country)
        
        parsed_data = parse_weather_data(weather_data)
        if parsed_data is None or not parsed_data:
            return f"Aucune donnée météo disponible pour {city_name}, {country}"
        
        summary = f"Météo à {city_name}:\n\n"
        
        # Today
        today = parsed_data[0]
        summary += f"Aujourd'hui ({today.get('date', '')}):\n"
        summary += f"  {today.get('condition', 'N/D')} - "
        summary += f"{today.get('temperature_min', 'N/D')}°C à {today.get('temperature_max', 'N/D')}°C\n"
        
        # Tomorrow
        if len(parsed_data) > 1:
            tomorrow = parsed_data[1]
            summary += f"\nDemain ({tomorrow.get('date', '')}):\n"
            summary += f"  {tomorrow.get('condition', 'N/D')} - "
            summary += f"{tomorrow.get('temperature_min', 'N/D')}°C à {tomorrow.get('temperature_max', 'N/D')}°C\n"
        
        return summary.rstrip()
        
    except FileNotFoundError:
        logger.error("Missing certificates")
        return "Certificats Apple WeatherKit manquants"
    except Exception as e:
        logger.error(f"Weather summary error: {e}")
        return f"Erreur lors de la récupération du résumé météo: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport='stdio')
