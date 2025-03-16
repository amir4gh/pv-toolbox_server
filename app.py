from flask import Flask, request, jsonify
import pandas as pd
import pvlib
from timezonefinder import TimezoneFinder

app = Flask(__name__)


def get_timezone(lat, lon):
    """Find timezone based on latitude and longitude."""
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lon, lat=lat)


@app.route("/solar", methods=["GET"])
def get_solar_irradiance():
    """Get solar irradiance and peak sun hours for a given location and date."""

    # Get query parameters
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


if __name__ == "__main__":
    from waitress import serve  # Use Waitress (better than Flask default server)

    serve(app, host="0.0.0.0", port=10000)
