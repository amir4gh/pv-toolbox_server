import requests
from datetime import datetime
import pytz
from utils.timezone_utils import get_timezone


def get_lat_lon(city, country):
    """
    Get latitude & longitude from city & country using Nominatim API.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"city": city, "country": country, "format": "json"}
    headers = {"User-Agent": "my-flask-app/1.0"}  # Prevent API blocking

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if not data or len(data) == 0:
            return {"error": "Location not found. Check city & country spelling."}

        latitude = float(data[0].get("lat", 0))
        longitude = float(data[0].get("lon", 0))

        return {
            "city": city,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
        }

    except Exception as e:
        return {"error": f"Nominatim API error: {str(e)}"}


def get_location_v2(city, country):
    """
    Get latitude, longitude, timezone, and current date-time from city & country.
    """
    location_data = get_lat_lon(city, country)

    if "error" in location_data:
        return location_data

    latitude = location_data["latitude"]
    longitude = location_data["longitude"]

    # Get timezone
    timezone = get_timezone(latitude, longitude)
    if not timezone:
        return {"error": "Could not determine timezone."}

    # Get current date & time in that timezone
    local_time = datetime.now(pytz.timezone(timezone))
    current_date = local_time.strftime("%Y-%m-%d")
    current_time = local_time.strftime("%H:%M:%S")

    location_data.update(
        {
            "timezone": timezone,
            "current_date": current_date,
            "current_time": current_time,
        }
    )

    return location_data


def get_time_for_location(latitude, longitude):
    """
    Get the current date and time for a given latitude & longitude using timezonefinder.
    """
    timezone = get_timezone(latitude, longitude)
    if not timezone:
        return {"error": "Could not determine timezone."}

    local_time = datetime.now(pytz.timezone(timezone))
    current_date = local_time.strftime("%Y-%m-%d")
    current_time = local_time.strftime("%H:%M:%S")

    return {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "current_date": current_date,
        "current_time": current_time,
    }
