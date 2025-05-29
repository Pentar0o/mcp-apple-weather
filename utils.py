"""Utility functions for weather data formatting"""
import locale
import pytz
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def format_date(date_str, timezone="Europe/Paris"):
    """
    Format date string to a readable format in French.
    
    Args:
        date_str: ISO format date string
        timezone: Target timezone (default: Europe/Paris)
        
    Returns:
        Formatted date string in French
    """
    if not date_str:
        return "Non disponible"
    
    try:
        # Parse UTC datetime
        utc_dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        utc_dt = pytz.utc.localize(utc_dt)
        
        # Convert to local timezone
        local_timezone = pytz.timezone(timezone)
        local_dt = utc_dt.astimezone(local_timezone)
        
        # Format in French
        formatted_date = local_dt.strftime('%A %d %B %Y')
        return formatted_date.capitalize()
    except Exception as e:
        logger.error(f"Error formatting date {date_str}: {e}")
        return "Non disponible"


def set_french_locale():
    """Set the locale to French for date formatting."""
    locale_options = ['fr_FR.UTF-8', 'fr_FR', 'French_France']
    
    for locale_option in locale_options:
        try:
            locale.setlocale(locale.LC_TIME, locale_option)
            logger.info(f"Locale set to {locale_option}")
            return
        except locale.Error:
            continue
    
    logger.warning("Could not set French locale, dates may not be fully translated")
