import pandas as pd
import pvlib
from utils.timezone_utils import get_timezone


def calculate_solar_irradiance(latitude, longitude, date):
    """
    Calculate solar irradiance & Peak Sun Hours (PSH) for a given location & date.
    """

    # Get timezone from latitude & longitude
    tz = get_timezone(latitude, longitude)
    if not tz:
        return {"error": "Could not determine timezone."}

    # Generate hourly timestamps for the given date
    times = pd.date_range(date, freq="1h", periods=24, tz=tz)

    # Get solar position
    solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
    airmass = pvlib.atmosphere.get_relative_airmass(solpos["zenith"])
    linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(times, latitude, longitude)

    # Get clear-sky irradiance using the Ineichen model
    clearsky = pvlib.clearsky.ineichen(
        solpos["apparent_zenith"], airmass, linke_turbidity
    )

    # Calculate Daily GHI (sum of hourly GHI)
    daily_ghi = clearsky["ghi"].sum()  # in Wh/m²
    psh = daily_ghi / 1000  # Convert Wh/m² to kWh/m²

    # Get irradiance at noon (12:00 PM local time)
    noon_irradiance = clearsky["ghi"][times.hour == 12].values[0]

    return {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": tz,
        "date": date,
        "irradiance_at_noon": round(noon_irradiance, 2),
        "peak_sun_hours": round(psh, 2),
    }


def get_solar_v2(latitude, longitude, date):
    """
    Get sunrise, sunset, hourly solar irradiance, and daily average radiance.
    """
    # Get timezone from lat/lon
    tz = get_timezone(latitude, longitude)
    if not tz:
        return {"error": "Could not determine timezone."}

    # Generate hourly timestamps for the given date
    times = pd.date_range(date, freq="1h", periods=24, tz=tz)

    # Get solar position
    solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)

    # Calculate air mass
    airmass = pvlib.atmosphere.get_relative_airmass(solpos["zenith"])

    # Get Linke turbidity values
    linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(times, latitude, longitude)

    # Get clear-sky irradiance using the Ineichen model
    clearsky = pvlib.clearsky.ineichen(
        solpos["apparent_zenith"], airmass, linke_turbidity
    )

    # Get sunrise and sunset times
    sunrise_time = (
        solpos["apparent_elevation"].idxmax().strftime("%H:%M:%S")
    )  # First sun appearance
    sunset_time = (
        solpos["apparent_elevation"].idxmin().strftime("%H:%M:%S")
    )  # Last sun appearance

    # Collect hourly irradiance
    hourly_radiance = {}
    for hour in range(24):
        hourly_radiance[f"{hour:02d}:00"] = round(clearsky["ghi"].iloc[hour], 2)

    # Calculate daily average irradiance
    avg_irradiance = round(clearsky["ghi"].mean(), 2)

    return {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": tz,
        "date": date,
        "sunrise": sunrise_time,
        "sunset": sunset_time,
        "hourly_radiance": hourly_radiance,
        "average_daily_radiance": avg_irradiance,
    }
