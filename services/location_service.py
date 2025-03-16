import requests


def get_lat_lon(city, country):
    """
    Get latitude & longitude from city & country using the Nominatim API.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"city": city, "country": country, "format": "json"}
    response = requests.get(url, params=params)
    data = response.json()

    if not data:
        return {"error": "Location not found."}

    latitude = float(data[0]["lat"])
    longitude = float(data[0]["lon"])

    return {
        "city": city,
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
    }
