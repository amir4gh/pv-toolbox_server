from flask import Flask, request, jsonify
import pandas as pd
import pvlib
from timezonefinder import TimezoneFinder
import requests  # For Nominatim API

app = Flask(__name__)


# Function to get timezone from latitude & longitude
def get_timezone(lat, lon):
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lon, lat=lat)


# ✅ New Route: Get latitude & longitude from city & country
@app.route("/location", methods=["GET"])
def get_location():
    """
    Get latitude & longitude from city and country using Nominatim API.
    """
    city = request.args.get("city", type=str)
    country = request.args.get("country", type=str)

    if not city or not country:
        return jsonify({"error": "Missing parameters. Provide city and country."}), 400

    try:
        # Call Nominatim API
        url = f"https://nominatim.openstreetmap.org/search"
        params = {"city": city, "country": country, "format": "json"}
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            return jsonify({"error": "Location not found."}), 404

        # Extract first result
        latitude = float(data[0]["lat"])
        longitude = float(data[0]["lon"])

        return jsonify(
            {
                "city": city,
                "country": country,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Existing Route: Get solar data from lat, lon & date
@app.route("/solar", methods=["GET"])
def get_solar_irradiance():
    """
    Get solar irradiance and peak sun hours for a given location and date.
    """

    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    date = request.args.get("date", type=str)

    if None in [latitude, longitude, date]:
        return (
            jsonify(
                {"error": "Missing parameters. Provide latitude, longitude, and date."}
            ),
            400,
        )

    try:
        # Get the timezone automatically
        tz = get_timezone(latitude, longitude)
        if not tz:
            return jsonify({"error": "Could not determine timezone."}), 400

        # Generate hourly timestamps
        times = pd.date_range(date, freq="1H", periods=24, tz=tz)
        solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
        airmass = pvlib.atmosphere.get_relative_airmass(solpos["zenith"])
        linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(
            times, latitude, longitude
        )
        clearsky = pvlib.clearsky.ineichen(
            solpos["apparent_zenith"], airmass, linke_turbidity
        )

        daily_ghi = clearsky["ghi"].sum()
        psh = daily_ghi / 1000
        noon_irradiance = clearsky["ghi"][times.hour == 12].values[0]

        return jsonify(
            {
                "latitude": latitude,
                "longitude": longitude,
                "timezone": tz,
                "date": date,
                "irradiance_at_noon": round(noon_irradiance, 2),
                "peak_sun_hours": round(psh, 2),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the app using Waitress for production
if __name__ == "__main__":
    from waitress import serve

    print("Starting production server...")
    serve(app, host="0.0.0.0", port=10000)
